#!/usr/bin/env python3
"""
categorize_structures.py — derive a STRUCTURIFY config from the pack's own
structure_sets, implementing the user's rarity policy + anti-clustering.

Policy (relative to VANILLA spacing, monotonic common->rare):
  LOOT  (dungeon/vault/crypt/treasure...)      ~1.05x  "less rare than the others"
  TOWN  (town/city/castle/fortress/big...)     ~1.30x  "a little more rare than vanilla"
  DEFAULT (everything else)                     1.60x   via global modifier (user's 1.5-1.8)
  RUIN  (ruined/abandoned/lone/small/ambient)  ~2.30x  "more rare" (rarest)

Mechanism (Structurify schema, verified from serializer constants):
  general.global_spacing_and_separation_modifier = 1.6  -> DEFAULT tier (bulk, no per-set entry)
  general.prevent_structure_overlap = true              -> anti-clustering (identical towns)
  per structure_set override (loot/town/ruin only):
     {name, spacing, separation, salt, frequency,
      override_global_spacing_and_separation_modifier:true}
     override flag => set uses its OWN spacing (opts out of the 1.6 global), so the
     per-tier multiplier is exact, not stacked on 1.6.

Only random_spread sets are tuned (concentric_rings = strongholds, left alone).
REFERENCE/REVIEW-FIRST: emits a table to stdout + writes structurify_plan.json;
does NOT overwrite config/structurify.json unless --apply is passed.
"""
import sys, os, glob, zipfile, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS = os.path.join(ROOT, "mods")
CFG  = os.path.join(ROOT, "config", "structurify.json")
PLAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "structurify_plan.json")

GLOBAL_MOD = 1.6      # DEFAULT tier
# LOOT common, TOWN a-little-rarer-than-vanilla, BIG (mega/boss arenas) a bit rarer than towns,
# RUIN rarest. DEFAULT handled by GLOBAL_MOD.
TIER_MULT  = {"LOOT": 1.10, "TOWN": 1.50, "DEFAULT": 1.60, "BIG": 2.00,
              "MASSIVE": 3.50, "FLOAT": 3.50, "DECO": 2.00, "RUIN": 2.30, "RUINED_DECO": 2.50}
# per-set ABSOLUTE multipliers the user set explicitly (final value; the loot bump does NOT stack)
SPECIAL_MULT = {"dungeons_arise:minor_structures": 1.80,
                "dungeons_arise_seven_seas:minor_structures": 1.80,
                # ocean monument = a dungeon you NEED for resources -> deliberately LESS rare (user 1.75)
                "betteroceanmonuments:ocean_monument": 1.75}
# tiers evaluated correctly by the eval workflow (agent judgement from member-names+size);
# used in preference to keyword classify() when present.
_HERE = os.path.dirname(os.path.abspath(__file__))
_TIERS_F = os.path.join(_HERE, "structure_tiers.json")
WORKFLOW_TIERS = json.load(open(_TIERS_F)) if os.path.exists(_TIERS_F) else {}
# persistent MANUAL override layer (survives re-runs of the eval workflow); wins over WORKFLOW_TIERS.
# {set_id: TIER}. This is where hand-corrections + user vetoes live so a re-eval can't clobber them.
_OVR_F = os.path.join(_HERE, "structure_tier_overrides.json")
OVERRIDE_TIERS = json.load(open(_OVR_F)) if os.path.exists(_OVR_F) else {}
# objective+audited loot flag per set ({set_id: bool}); drives the LOOT_BUMP. Falls back to the
# has_loot field in structure_eval_data.json if the dedicated map isn't present yet.
_LOOT_F = os.path.join(_HERE, "structure_loot.json")
if os.path.exists(_LOOT_F):
    HAS_LOOT = json.load(open(_LOOT_F))
else:
    _ed = os.path.join(_HERE, "structure_eval_data.json")
    HAS_LOOT = {s["set"]: s.get("has_loot", False) for s in json.load(open(_ed))["sets"]} \
        if os.path.exists(_ed) else {}
# manual loot corrections (verified false-negatives the scanner missed); win over the baseline
_LOOTOVR_F = os.path.join(_HERE, "structure_loot_overrides.json")
if os.path.exists(_LOOTOVR_F):
    HAS_LOOT.update({k: bool(v) for k, v in json.load(open(_LOOTOVR_F)).items()})
# USER RULE: a structure that HAS LOOT but sits in a non-LOOT tier inherits +25% rarity, so that
# loot overall stays rare (loot is the reward, so reward-bearing structures should be scarcer).
LOOT_BUMP = 1.25
PREVENT_OVERLAP = True
MAX_SPACING = 120     # per-tier clamp so normal tiers don't vanish (bounds the multiplier INCREASE)
MASSIVE_MAX = 281     # MASSIVE/FLOAT cap — they SHOULD be very rare (matches HARD_MAX)
# GLOBAL rarity ceiling (chunks). Nothing in the world is spaced rarer than this — clamps even high
# mod-author spacings (shrine_tower sp600=9.6km, butchers sp361=5.8km) DOWN. sp281 = 4.5km, set JUST
# BEYOND the DH render radius (lodChunkRenderDistanceRadius=256 = 4.1km): the rarest structures
# usually sit just past the render edge but occasionally peek into view — "a chance to be in render
# distance" (user 2026-06-20), the distant-DH-landmark you trek toward.
HARD_MAX = 281
MIN_SCALE_SPACING = 3 # don't scale specials this dense (mineshafts sp1) — they're meant to be everywhere
# WDA "major_structures" = the giant castles/fortresses — user wants these 3-4x rarer (rarer than BIG)
MASSIVE_KW = ("major_structures", "epic_", "legendary_", "mythic_")

# --- keyword classifiers (checked on set id, then member structure ids) ---
RUIN_KW = ("ruin","ruined","abandoned","overgrown","derelict","decay","decayed","rubble",
    "remains","fallen","broken","wreck","collapsed","forgotten","lone","lonely","small_",
    "_small","tiny","ambient","shrine","well","campsite","campfire","pile","fossil","boulder",
    "grave","gravestone","tombstone","scatter","debris","husk","crumbl","weathered","deserted",
    "statue")
LOOT_KW = ("dungeon","vault","treasure","crypt","tomb","catacomb","labyrinth","bunker","hoard",
    "reliquary","loot","mineshaft","cave_dungeon","lab","laboratory","sanctum","chamber",
    "stash","cache","trove","pyramid")
TOWN_KW = ("town","village","city","capital","castle","fortress","keep","mansion","stronghold",
    "citadel","palace","monastery","cathedral","metropolis","kingdom","fort","port","harbor",
    "harbour","settlement","manor","chateau","estate","hall","bastion","stronghold","temple",
    "tavern","guild","colony")
# really-big / boss-arena tier — a bit rarer than towns (user: mega_arenas + Cataclysm boss arenas)
BIG_KW  = ("mega","arena","colosseum","coliseum","colossal","giant","titan","leviathan",
    "behemoth","monstrosity","harbinger","boss","huge","massive","ancient_city")
SMALL_KW = ("small_","_small","tiny")
BIG_NAMESPACES = ("cataclysm",)   # whole mod is boss arenas -> BIG (except explicitly small sets)

def classify(set_id, members, jar):
    """LOOT/TOWN/RUIN/DEFAULT, decided per-SET. SET-ID keywords decide first (authoritative);
    only if the set id gives no signal do member ids vote (majority), so a single loot-y member
    can't hijack a whole village set (e.g. roman_buildings with one catacomb)."""
    # manual override layer wins over everything (hand-corrections + user vetoes survive re-eval)
    if set_id in OVERRIDE_TIERS: return OVERRIDE_TIERS[set_id]
    # workflow evaluation wins next (agent judged from member-names + size)
    if set_id in WORKFLOW_TIERS: return WORKFLOW_TIERS[set_id]
    ns  = set_id.split(":")[0]
    sid = set_id.split(":")[-1].lower()
    def has(kws, text): return any(k in text for k in kws)
    is_small = has(SMALL_KW, sid)
    # --- 0a) MASSIVE (WDA major_structures etc.): rarest of the build tiers (3-4x) ---
    if has(MASSIVE_KW, sid): return "MASSIVE"
    # --- 0b) boss-arena namespaces (Cataclysm): rarer than towns, except explicitly small sets ---
    if ns in BIG_NAMESPACES and not is_small: return "BIG"
    # --- 1) authoritative: the SET id itself (BIG beats RUIN so a mega-ruin still reads big) ---
    if has(BIG_KW, sid) and not is_small: return "BIG"
    if has(RUIN_KW, sid):  return "RUIN"
    if has(LOOT_KW, sid):  return "LOOT"
    if has(TOWN_KW, sid):  return "TOWN"
    # --- 2) fallback: vote across member structure ids ---
    votes = collections.Counter()
    for m in members:
        ml = m.split(":")[-1].lower()
        if   has(BIG_KW, ml) and not has(SMALL_KW, ml): votes["BIG"] += 1
        elif has(TOWN_KW, ml): votes["TOWN"] += 1   # a settlement member is a strong town signal
        elif has(LOOT_KW, ml): votes["LOOT"] += 1
        elif has(RUIN_KW, ml): votes["RUIN"] += 1
    if votes:
        if votes.get("BIG"):  return "BIG"
        if votes.get("TOWN"): return "TOWN"   # building collections read as towns
        return votes.most_common(1)[0][0]
    return "DEFAULT"

def scale(v, mult, lo, cap=MAX_SPACING):
    try: v = int(v)
    except Exception: return None
    if v <= MIN_SCALE_SPACING: return v           # specials (mineshafts sp1) — leave dense
    target = min(cap, max(lo, round(v * mult)))   # multiplier increase, bounded by the per-tier cap
    target = max(target, min(v, HARD_MAX))         # never below vanilla — UNLESS vanilla exceeds the
    return min(target, HARD_MAX)                    # global ceiling, which clamps absurd authors DOWN

# LOOT BUMP — RETIRED 2026-06-20 (user call). The pack is HARD and loot SCALES TO PLAYER LEVEL, so
# abundance isn't exploitable; a +25% rarity penalty on loot-bearers just fought the difficulty curve.
# Loot-bearing structures now follow their PLAIN tier rarity. has_loot is still computed + stored (for
# the Lootr work + reporting) but no longer affects spacing. (To re-enable a bump, reintroduce it here.)
def eff_mult(tier, has_loot=False):
    """effective spacing multiplier vs vanilla — pure tier rarity (loot bump retired)."""
    return TIER_MULT.get(tier, GLOBAL_MOD)

def set_mult(sid, tier, has_loot):
    """final multiplier: an explicit SPECIAL_MULT is ABSOLUTE (e.g. WDA minor 1.8, ocean_monument
    1.75); otherwise the plain tier value."""
    if sid in SPECIAL_MULT:
        return SPECIAL_MULT[sid]
    return eff_mult(tier, has_loot)

# ----------------------------------------------------------------- CristelLib I/O
CRIS = os.path.join(ROOT, "config", "cristellib")

def json5_load(path):
    """tolerant JSON5 read: strip /* */ + // comments and trailing commas, then json.loads."""
    txt = open(path, encoding="utf-8").read()
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r"//[^\n]*", "", txt)
    txt = re.sub(r",(\s*[}\]])", r"\1", txt)
    return json.loads(txt)

def json5_write(path, data):
    """write back in CristelLib's own style (tab indent + generated-by header)."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("/*\nAutomatically generated by Cristel Lib\n*/\n")
        json.dump(data, f, indent="\t")
        f.write("\n")

def load_cristellib(all_set_ids):
    """Index every CristelLib-managed set by its CANONICAL set id (namespace:path).

    The folder under config/cristellib/ is named by CristelLib per registering mod, which is NOT
    always the data namespace the mod registers structure_sets under (e.g. folder
    'mr_dungeons_andtaverns' owns the 'nova_structures:*' sets; datapack-style jars have no modId
    at all). CristelLib keys are fully namespaced ('minecraft:woodland_mansions') or BARE
    ('shrine_tower'). A bare key whose folder != namespace is resolved to the real set whose PATH
    matches, BUT only to a set that is NOT already 'natively owned' (a set whose own namespace has
    its own cristellib folder carrying that key) — that filters out coincidental same-path sets
    from unrelated mods (e.g. 'oreganized/boulder' must NOT grab 'mvs:boulder', which 'mvs' owns).
    For multi-candidate keys we prefer the folder's DOMINANT foreign namespace (the one most of its
    keys point to). This makes each real set owned by exactly ONE system + clamped (no double-tune).

    Returns (index{set_id: (file, original_key)}, parsed{file: dict})."""
    files, parsed = [], {}
    native = collections.defaultdict(set)          # folder -> bare keys it carries (native-ownership test)
    path_to_ids = collections.defaultdict(set)
    for sid in all_set_ids:
        path_to_ids[sid.split(":", 1)[1]].add(sid)
    for f in glob.glob(os.path.join(CRIS, "*", "structure_placement_config.json5")):
        folder = os.path.basename(os.path.dirname(f))
        try: cfg = json5_load(f)
        except Exception: continue
        files.append((f, folder, cfg)); parsed[f] = cfg
        for key in cfg:
            native[folder].add(key.split(":")[-1] if ":" in key else key)
    def unclaimed(key):                            # real ns:key sets whose own ns folder does NOT carry key
        return [c for c in path_to_ids.get(key, ()) if key not in native.get(c.split(":")[0], ())]
    index = {}
    for f, folder, cfg in files:
        votes = collections.Counter()              # folder's dominant foreign namespace
        for key in cfg:
            if ":" in key or f"{folder}:{key}" in all_set_ids: continue
            for c in unclaimed(key): votes[c.split(":")[0]] += 1
        dom = votes.most_common(1)[0][0] if votes else None
        for key in cfg:
            if ":" in key:
                sid = key
            elif f"{folder}:{key}" in all_set_ids:
                sid = f"{folder}:{key}"
            else:
                uc = unclaimed(key)
                if dom and f"{dom}:{key}" in uc:   sid = f"{dom}:{key}"
                elif len(uc) == 1:                 sid = uc[0]
                else:                              sid = f"{folder}:{key}"   # orphan/ambiguous -> fallback
            index[sid] = (f, key)
    return index, parsed

def main():
    apply = "--apply" in sys.argv
    sets = {}        # id -> {jar, placement, members:[ids]}
    for jp in sorted(glob.glob(os.path.join(MODS, "*.jar"))):
        jar = os.path.basename(jp)
        try: z = zipfile.ZipFile(jp)
        except Exception: continue
        with z:
            for n in z.namelist():
                m = re.match(r"data/([^/]+)/worldgen/structure_set/(.+)\.json$", n)
                if not m: continue
                sid = f"{m.group(1)}:{m.group(2)}"
                if sid in sets: continue   # first jar wins (datapack override order is separate)
                try: data = json.loads(z.read(n))
                except Exception: continue
                pl = data.get("placement", {})
                members = [s.get("structure","") for s in data.get("structures",[]) if isinstance(s,dict)]
                sets[sid] = {"jar": jar, "placement": pl, "members": members}

    # CristelLib owns its managed sets; Structurify owns the rest. Global modifier OFF so every
    # set is tuned by exactly ONE system at an explicit absolute value (no double-application).
    cris_index, cris_parsed = load_cristellib(set(sets.keys()))
    cris_dirty = set()                 # files we modified
    tiers = collections.Counter()
    overrides = []                     # Structurify-owned explicit entries
    skipped_rings = skipped_nosp = cris_count = 0
    review = []
    rows = []           # numeric per-tuned-set data for the effective-multiplier matrix
    for sid, info in sorted(sets.items()):
        ns, setname = sid.split(":", 1)
        pl = info["placement"]; ptype = pl.get("type","")
        tier = classify(sid, info["members"], info["jar"])
        loot = bool(HAS_LOOT.get(sid, False))
        tiers[tier] += 1
        if "concentric_rings" in ptype:      # strongholds etc — leave alone
            skipped_rings += 1; review.append((sid, tier, "rings(skip)", "", "", "", loot)); continue
        sp = pl.get("spacing"); se = pl.get("separation")
        if sp is None:
            skipped_nosp += 1; review.append((sid, tier, ptype, "no-spacing", "", "", loot)); continue
        mult = set_mult(sid, tier, loot)
        cap = MASSIVE_MAX if tier in ("MASSIVE", "FLOAT") else MAX_SPACING
        nsp = scale(sp, mult, 2, cap)
        nse = scale(se, mult if se else 1, 1, cap) if se is not None else se
        if nse is not None and nsp is not None and nse >= nsp: nse = nsp - 1   # spacing > separation
        owner = "cristellib" if sid in cris_index else "structurify"
        try: van_sp = int(sp)
        except Exception: van_sp = None
        rows.append({"set": sid, "tier": tier, "loot": loot, "van_sp": van_sp,
                     "new_sp": nsp, "mult": mult, "owner": owner})
        if owner == "cristellib":
            f, key = cris_index[sid]; e = cris_parsed[f].setdefault(key, {})
            e["spacing"] = nsp
            if nse is not None: e["separation"] = nse
            if "salt" not in e and "salt" in pl: e["salt"] = pl["salt"]
            cris_dirty.add(f); cris_count += 1
        else:
            entry = {"name": sid, "is_disabled": False, "spacing": nsp,
                     "separation": nse if nse is not None else se,
                     "override_global_spacing_and_separation_modifier": True}
            if "salt" in pl: entry["salt"] = pl["salt"]
            if "frequency" in pl: entry["frequency"] = pl["frequency"]
            overrides.append(entry)
        review.append((sid, tier, f"sp{sp}/se{se}", f"x{mult}",
                       f"sp{nsp}/se{nse if nse is not None else se}", owner, loot))

    # ---- report ----
    print(f"=== {len(sets)} structure_sets classified ===")
    for t in ("LOOT","DEFAULT","TOWN","BIG","MASSIVE","FLOAT","DECO","RUIN","RUINED_DECO"):
        print(f"  {t:11} {tiers[t]:4}")
    print(f"  concentric_rings skipped: {skipped_rings}   no-spacing skipped: {skipped_nosp}")
    print(f"  OWNERSHIP -> CristelLib: {cris_count} sets in {len(cris_dirty)} files | "
          f"Structurify: {len(overrides)} explicit entries")
    print()
    print("=== sample per tier (id | tier | vanilla | mult | new | owner) ===")
    shown = collections.Counter()
    for sid, tier, van, mult, new, owner, loot in review:
        if new and shown[tier] < 5:
            print(f"  {sid:50} {tier:6} {van:11} {mult:8} {new:13} {owner}")
            shown[tier]+=1

    # ---- EFFECTIVE-MULTIPLIER MATRIX (tier x has-loot) for the user's veto ----
    print("\n=== TIER MULTIPLIER MATRIX (loot bump RETIRED; has_loot informational only) ===")
    TIER_ORDER = ["LOOT","TOWN","DEFAULT","BIG","DECO","RUIN","RUINED_DECO","MASSIVE","FLOAT"]
    by_tier = collections.defaultdict(lambda: [0,0])
    for r in rows:
        by_tier[r["tier"]][1 if r["loot"] else 0] += 1
    for t in TIER_ORDER:
        base = eff_mult(t, False)
        nl, lt = by_tier[t][0], by_tier[t][1]
        print(f"  {t:12} x{base:<5} sets:{nl+lt:4}  loot-bearing:{lt}")
    # WDA minor special line
    for sid in SPECIAL_MULT:
        rr = next((r for r in rows if r["set"] == sid), None)
        if rr:
            print(f"  SPECIAL {sid}: x{SPECIAL_MULT[sid]} (absolute); loot={rr['loot']}")

    # ---- THE EXTREME END: the rarest resulting sets (where 'why is this SO rare' lives) ----
    print("\n=== RAREST 25 RESULTING SETS (vanilla sp -> new sp | tier | loot | mult) ===")
    rk = sorted([r for r in rows if r["new_sp"] is not None], key=lambda r: -r["new_sp"])[:25]
    for r in rk:
        print(f"  sp{str(r['van_sp']):>4} -> sp{r['new_sp']:<4}  {r['tier']:11} "
              f"{'loot' if r['loot'] else '    '} x{r['mult']:<7} {r['set']}")
    # how many sets actually receive the loot bump
    bumped_n = sum(1 for r in rows if r["loot"] and r["tier"] != "LOOT")
    print(f"\n  loot bump applies to {bumped_n}/{len(rows)} tuned sets "
          f"({100*bumped_n//max(1,len(rows))}%)")

    plan = {"general": {"prevent_structure_overlap": PREVENT_OVERLAP,
                        "enable_global_spacing_and_separation_modifier": False},
            "tier_counts": dict(tiers),
            "ownership": {"cristellib": cris_count, "structurify": len(overrides)},
            "overrides": overrides,
            "review": [{"set":r[0],"tier":r[1],"vanilla":r[2],"mult":r[3],"new":r[4],
                        "owner":r[5],"loot":r[6]} for r in review]}
    with open(PLAN, "w") as f: json.dump(plan, f, indent=1)
    print(f"\nwrote review plan -> {os.path.relpath(PLAN, ROOT)}")

    if apply:
        import shutil
        # 1) Structurify: own the non-CristelLib sets, global modifier OFF
        cur = json.load(open(CFG)) if os.path.exists(CFG) else {}
        cur.setdefault("general", {})
        cur["general"]["prevent_structure_overlap"] = PREVENT_OVERLAP
        cur["general"]["enable_global_spacing_and_separation_modifier"] = False
        cur["structure_sets"] = overrides
        if os.path.exists(CFG): shutil.copy(CFG, CFG + ".prestructurify.bak")
        json.dump(cur, open(CFG, "w"), indent=2)
        print(f"APPLIED Structurify -> {os.path.relpath(CFG, ROOT)} "
              f"({len(overrides)} entries, global modifier OFF)")
        # 2) CristelLib: write tuned values into its managed placement configs (backup each once)
        for f in sorted(cris_dirty):
            bak = f + ".prestructurify.bak"
            if not os.path.exists(bak): shutil.copy(f, bak)
            json5_write(f, cris_parsed[f])
        print(f"APPLIED CristelLib -> {len(cris_dirty)} placement configs "
              f"(backups: *.prestructurify.bak)")
    else:
        print("(dry-run; re-run with --apply to write configs)")

if __name__ == "__main__":
    main()
