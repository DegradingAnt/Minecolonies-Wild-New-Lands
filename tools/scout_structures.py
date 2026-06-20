#!/usr/bin/env python3
"""
scout_structures.py — gather HARD FACTS per structure_set so each can be tier-evaluated
correctly (not keyword-guessed). Emits:
  .uvrun/structure_eval_data.json  — rich per-set facts (for reference / categorizer)
  .uvrun/structure_audit.jsonl     — line-addressable audit input for the eval/audit workflow

Per set: placement (spacing/sep), member structure ids + each member's definition
(type, jigsaw size, max_distance_from_center, start_height + project_start_to_heightmap =
floating signal, terrain_adaptation, step, biomes), a floating flag, a CristelLib-managed flag,
and an OBJECTIVE loot signal (`has_loot`): does the structure actually place lootable
containers? Detected by gzip-decompressing each referenced .nbt template and byte-searching for
the `LootTable` tag (a literal TAG_String name in the NBT stream) — no full NBT parser needed.
Pieces are mapped to a structure via its start-pool element locations + their longest common
prefix (captures the whole piece family incl. deep jigsaw pieces in the same folder), which is
robust to jigsaw chaining (that lives in NBT, not JSON) without over-broad namespace scans.

The loot signal is OBJECTIVE ground-truth for chest/barrel loot; the audit agents combine it
with semantic judgement (vault/spawner/mob-drop loot that isn't a LootTable-tagged container).
"""
import zipfile, glob, os, re, json, gzip, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS = os.path.join(ROOT, "mods")
CRIS = os.path.join(ROOT, "config", "cristellib")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "structure_eval_data.json")
AUD  = os.path.join(HERE, "structure_audit.jsonl")
TIERS_F = os.path.join(HERE, "structure_tiers.json")

# vanilla/hardcoded non-jigsaw structure types that always carry loot (modded loot structures
# are almost all jigsaw, handled by the nbt scan; this just covers the few hardcoded types)
LOOT_TYPES = {"mineshaft", "ocean_ruin", "shipwreck", "buried_treasure", "ruined_portal",
              "nether_fortress", "bastion_remnant", "stronghold", "jungle_temple",
              "desert_pyramid", "igloo", "swamp_hut", "end_city", "woodland_mansion",
              "ocean_monument", "fortress", "trail_ruins"}

def heightmap_floats(d):
    if not isinstance(d, dict): return False
    hm = d.get("project_start_to_heightmap")
    sh = d.get("start_height")
    absh = sh.get("absolute") if isinstance(sh, dict) else None
    return hm in (None, "") and isinstance(absh, (int, float)) and absh >= 70

def lcp(strs):
    if not strs: return ""
    lo, hi = min(strs), max(strs); i = 0
    while i < len(lo) and i < len(hi) and lo[i] == hi[i]: i += 1
    return lo[:i]

def main():
    structs, sets, pools = {}, {}, {}
    nbt_index = {}            # "ns:relpath" -> (jar_path, inner_path)
    jarz = {}                 # jar_path -> open ZipFile (lazy reuse for nbt reads)

    for jp in sorted(glob.glob(os.path.join(MODS, "*.jar"))):
        try: z = zipfile.ZipFile(jp)
        except Exception: continue
        keep = False
        for n in z.namelist():
            ms = re.match(r"data/([^/]+)/worldgen/structure/(.+)\.json$", n)
            if ms:
                sid = f"{ms.group(1)}:{ms.group(2)}"
                if sid not in structs:
                    try: structs[sid] = json.loads(z.read(n))
                    except Exception: pass
                continue
            mss = re.match(r"data/([^/]+)/worldgen/structure_set/(.+)\.json$", n)
            if mss:
                sid = f"{mss.group(1)}:{mss.group(2)}"
                if sid not in sets:
                    try: sets[sid] = json.loads(z.read(n))
                    except Exception: pass
                continue
            mp = re.match(r"data/([^/]+)/worldgen/template_pool/(.+)\.json$", n)
            if mp:
                pid = f"{mp.group(1)}:{mp.group(2)}"
                if pid not in pools:
                    try: pools[pid] = json.loads(z.read(n))
                    except Exception: pass
                continue
            mn = re.match(r"data/([^/]+)/structure/(.+)\.nbt$", n)
            if mn:
                loc = f"{mn.group(1)}:{mn.group(2)}"
                nbt_index.setdefault(loc, (jp, n)); keep = True
        if keep: jarz[jp] = z      # keep handle open for nbt reads; close at end
        else: z.close()

    loot_cache = {}              # loc -> bool (contains a LootTable container)
    def nbt_has_loot(loc):
        if loc in loot_cache: return loot_cache[loc]
        ref = nbt_index.get(loc); res = False
        if ref:
            jp, inner = ref
            try:
                raw = jarz[jp].read(inner)
                try: data = gzip.decompress(raw)
                except Exception: data = raw           # some .nbt are stored uncompressed
                res = b"LootTable" in data
            except Exception: res = False
        loot_cache[loc] = res; return res

    def pool_locations(pid):
        p = pools.get(pid); locs = []
        if not isinstance(p, dict): return locs
        for el in p.get("elements", []):
            e = el.get("element", {}) if isinstance(el, dict) else {}
            for key in ("location", "start_pool"):     # single_pool_element / nested
                v = e.get(key)
                if isinstance(v, str): locs.append(v)
        return locs

    ns_struct_count = collections.Counter(k.split(":")[0] for k in structs)
    def struct_has_loot(struct_id):
        sd = structs.get(struct_id)
        if not isinstance(sd, dict): return False
        t = sd.get("type", "").split(":")[-1]
        if t in LOOT_TYPES: return True            # hardcoded vanilla-ish loot types
        sp = sd.get("start_pool")
        sp = sp if isinstance(sp, str) else (sp.get("name") if isinstance(sp, dict) else None)
        direct = pool_locations(sp) if sp else []
        for loc in direct:                          # cheapest, most precise
            if nbt_has_loot(loc): return True
        # OR a set of family prefixes (recall: jigsaw loot rooms often sit in a sibling folder):
        #   start-pool LCP (tight) | start-pool id | the structure's OWN folder (ns:name/...)
        #   | whole namespace for small dedicated dungeon/temple mods (<=3 structures)
        prefixes = set()
        if direct:
            p = lcp(direct)
            if ":" in p: prefixes.add(p)
        if sp and ":" in sp: prefixes.add(sp)
        prefixes.add(struct_id)
        if ns_struct_count.get(struct_id.split(":")[0], 99) <= 3:
            prefixes.add(struct_id.split(":")[0] + ":")
        prefixes = tuple(prefixes)
        for loc in nbt_index:
            if loc.startswith(prefixes) and nbt_has_loot(loc): return True
        return False

    cur_tiers = json.load(open(TIERS_F)) if os.path.exists(TIERS_F) else {}

    # CristelLib-managed set ids
    cris = set()
    for f in glob.glob(os.path.join(CRIS, "*", "structure_placement_config.json5")):
        ns = os.path.basename(os.path.dirname(f))
        txt = open(f, encoding="utf-8").read()
        txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S); txt = re.sub(r"//[^\n]*", "", txt)
        txt = re.sub(r",(\s*[}\]])", r"\1", txt)
        try:
            for k in json.loads(txt): cris.add(f"{ns}:{k}")
        except Exception: pass

    out, audit = [], []
    for i, (sid, d) in enumerate(sorted(sets.items())):
        pl = d.get("placement", {})
        members = [s.get("structure","") for s in d.get("structures",[]) if isinstance(s,dict)]
        mdefs, any_float, any_loot, max_sz = [], False, False, 0
        for m in members:
            if struct_has_loot(m): any_loot = True
        for m in members[:8]:                      # cap detail for huge sets
            sd = structs.get(m, {})
            sh = sd.get("start_height")
            absh = sh.get("absolute") if isinstance(sh, dict) else None
            fl = heightmap_floats(sd); any_float = any_float or fl
            sz = sd.get("size")
            if isinstance(sz, int): max_sz = max(max_sz, sz)
            b = sd.get("biomes")
            biome = (b if isinstance(b, str) else (f"list[{len(b)}]" if isinstance(b, list) else "?"))
            mdefs.append({"id": m.split(":")[-1], "type": sd.get("type","?").split(":")[-1],
                          "size": sz, "maxdist": sd.get("max_distance_from_center"),
                          "start_abs": absh, "heightmap": sd.get("project_start_to_heightmap"),
                          "terrain": sd.get("terrain_adaptation"), "step": sd.get("step"),
                          "floats": fl, "biome": biome})
        out.append({"set": sid, "namespace": sid.split(":")[0],
                    "placement_type": pl.get("type","?").split(":")[-1],
                    "spacing": pl.get("spacing"), "separation": pl.get("separation"),
                    "member_count": len(members), "members": [m.split(":")[-1] for m in members[:16]],
                    "member_defs": mdefs, "any_member_floats": any_float,
                    "has_loot": any_loot, "cristellib_managed": sid in cris,
                    "current_tier": cur_tiers.get(sid)})
        audit.append({"i": i, "set": sid, "ns": sid.split(":")[0],
                      "tier": cur_tiers.get(sid), "loot": any_loot,
                      "n": len(members), "sz": max_sz, "float": any_float,
                      "sp": pl.get("spacing"),
                      "mem": [m.split(":")[-1] for m in members[:12]]})

    json.dump({"count": len(out), "sets": out}, open(OUT, "w"), indent=1)
    with open(AUD, "w") as f:
        for a in audit: f.write(json.dumps(a) + "\n")
    for z in jarz.values():
        try: z.close()
        except Exception: pass

    n_loot = sum(1 for s in out if s["has_loot"])
    print(f"scouted {len(out)} structure_sets -> {os.path.relpath(OUT, ROOT)}")
    print(f"  audit jsonl -> {os.path.relpath(AUD, ROOT)} ({len(audit)} lines)")
    print(f"  floating-signal sets: {sum(1 for s in out if s['any_member_floats'])}")
    print(f"  cristellib-managed:   {sum(1 for s in out if s['cristellib_managed'])}")
    print(f"  HAS-LOOT (nbt LootTable): {n_loot}/{len(out)}  ({100*n_loot//max(1,len(out))}%)")
    # sanity: loot rate by current tier
    by = collections.defaultdict(lambda: [0,0])
    for s in out:
        t = s.get("current_tier") or "?"
        by[t][0] += 1; by[t][1] += 1 if s["has_loot"] else 0
    print("  loot-rate by current tier:")
    for t in sorted(by, key=lambda k: -by[k][0]):
        tot, lt = by[t]; print(f"    {t:12} {lt:4}/{tot:<4}  {100*lt//max(1,tot):3}%")

if __name__ == "__main__":
    main()
