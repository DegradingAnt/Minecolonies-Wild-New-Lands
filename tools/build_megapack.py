"""Build WNL-MegaPack.zip — merge ALL resourcepacks/ into ONE pack_format-34 pack for 1.21.1.

CURATION ENGINE (2026-06-26, Phase 1) — data-driven from _dev/megapack-curation-rules.md (95 rules).
Two base anchors: Stay True = block/texture base; FreshAnimations = mob base. Everything else overlays
by TIER (low->high = base->override). Plus: per-pack ASSET EXCLUDES, mine-only concept DROPS, a
persistent WNL-Custom authoring layer applied LAST (top precedence). Overlay resolution + sanitizer
from the foundation fix are preserved.

DEFERRED to Phase 2 (flagged [investigate] in the spec, too risky to do blind):
  - variant AGGREGATION (#59): variety packs currently last-wins by tier (one variant shows), same as
    before — NOT regressed; true ETF random-variant merge is Phase 2.
  - SPLITS (#5 Armored Illager armor-vs-model, #27 Ender Eyes anim-vs-texture): need path inspection.
  - custom authoring (#19/#35/#60/#61/#63/#69-port/#71/#92) -> live in WNL-Custom, authored separately.
PRIVATE/personal only (bundles third-party art, credited). Run: python .uvrun/build_megapack.py"""
import os, io, json, zipfile, re

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
RP = os.path.join(ROOT, "resourcepacks")              # source zips + OUTPUT live here
SRC = os.environ.get("WNL_MEGAPACK_SRC", RP)
OUT = os.path.join(RP, "WNL-MegaPack.zip")
CUSTOM_DIR = os.path.join(ROOT, "resourcepacks-src", "WNL-Custom")  # hand-authored layer (#62), applied LAST

# === DROPS: never merged (own output, removed-mod packs, + MINE-ONLY concept packs) ===
# mine-only = "port the IDEA, do NOT use textures" (design policy) -> source stays in resourcepacks/
# for reference, but its art never ships in the megapack. (#69 Display/Fresh Armor, #71 FA Variated
# Villagers, #72 Blue's Better Monsters, batch-2 Better Zombies.)
DROP_SUBSTR = [
    "wnl-megapack",                # our own output
    "visual titles",               # removed mod
    "display armor",               # #69 Fresh/Display Armor -> author 3D armor originally in WNL-Custom
    "blues_better_monsters",       # #72 mine-only
    "better zombies",              # batch-2 mine-only (Blue's Better Zombies)
    "fresh variated villagers",    # #71 mine-only (port the idea -> our own random-variant villagers)
]
def dropped_pack(f):
    fl = f.lower()
    return any(d in fl for d in DROP_SUBSTR)

# === PER-PACK ASSET EXCLUDES: skip matching paths from a specific pack during merge ===
# (substr -> predicate(internal_path)->True to SKIP). Source packs stay pristine.
def _excl_fresh_textures(p):   # #28/#66 Fresh Textures = MISC only; it wrongly won mob textures
    return "/textures/entity/" in p
def _excl_freshtextures_fa(p): # #3 FreshTextures+FA = mob-support, NOT the player (Fresh Moves drives player)
    return "/textures/entity/player/" in p or "/player/" in p and p.endswith(".jem") or "/cem/player" in p
PACK_EXCLUDES = [
    ("fresh textures", _excl_fresh_textures),     # matches "Fresh Textures 1.4.4" (NOT "freshtextures+fa")
    ("freshtextures+fa", _excl_freshtextures_fa),
]
def exclude_pred(packname):
    fl = packname.lower()
    for sub, pred in PACK_EXCLUDES:
        if sub == "fresh textures":
            if "fresh textures" in fl and "+fa" not in fl:
                return pred
        elif sub in fl:
            return pred
    return None

# === TIER TABLE (low number = applied first = LOWER priority; high overwrites) ===
# ordered, first-match wins. substrings are the REAL lowercased source-zip filenames.
TIER_RULES = [
    # -- FLOOR: last-line-of-defence + demoted ruining source --
    ("rcp", 1),                       # #95 The RCP: wins only what nothing else covers
    ("musgo", 1),                     # #36 Musgo: ruining source, NOT a global override -> never wins base
    # -- base-plus / below Stay True (gap-fill) --
    ("vanilla experience", 11),       # #37 base + variety (specific drivers win shared)
    ("freshtextures+fa", 14),         # #3/#25 base-plus, mob-only (player excluded), below all FA addons
    ("fresh textures", 10),           # #28 MISC base (entity excluded); keep below Stay True
    # -- CTM backups (below Stay True; fill connected-texture gaps only) --
    ("connected-", 13),               # #31/#33/#34 Connected Paths/Rocks/Bricks
    ("connected_copper_grate", 13),   # #50
    ("fusion connected blocks", 13),  # #51
    ("snow side", 13),                # #54 snowy-side overlay (custom patches pending)
    ("geo - ", 13),                   # GEO Fusion CTM
    # -- Stay True = THE block/vanilla-texture base anchor (#28) --
    ("stay true 1.21", 15),
    # -- low bases that must lose shared features to specific drivers --
    ("armor trim compat", 25),        # #23 trim-compat base
    ("emissive lanterns", 30),        # #32 emissive-ONLY base (its _e textures are unique paths)
    ("better-leaves", 30),            # #45 leaves base
    # -- Stay-True-style modded support --
    ("staytrue26", 42), ("stay true compat", 42),  # #44
    # -- FreshAnimations ecosystem (explicit sub-tiers; #25 hierarchy) --
    ("fa+all_extensions", 56), ("fa+player", 56),   # 56: extensions = FA base layer (own vanilla mobs)
    ("freshanimations", 55),                        # 55: FA base
    ("th + fresh", 50),                             # 50: FA texture-compat looks (lose models to FA)
    # 52: FA specific-mob compat addons (modded mobs animate w/ FA; overlay ON the base)
    ("fa illager", 52), ("armored illager", 52), ("morepiglins", 52), ("rotten creatures", 52),
    ("variants and ventures", 52), ("abnormally fresh", 52), ("assorted allays", 52),
    ("wandering traders", 52), ("mca_resourcepack", 52), ("quarkfacompat", 52),
    ("eating animations", 52), ("freshly modded", 52), ("endereyes", 52),
    ("semos", 48),                                  # #6 lib: load but don't win finished mobs [investigate]
    # 51: variety packs (refreshed family + Drodi's + Al's series + turtles) -> STACK (#38-41/#59/#67)
    ("refreshed-fa", 51), ("refreshed-v", 51), ("refreshed-v2", 51), ("boss-refreshed", 51),
    ("drodi", 51), ("freshturtle", 51), ("fresh moves", 51), ("fresh patch", 52),
    # -- category drivers (win their category over Stay True; #1/#2/#16/#17/#21/#18/#29/#55/#56/#58...) --
    ("armory", 45),                   # #1 armor (split from models = Phase 2)
    ("modded omelet", 45),            # #2 spawn eggs
    ("medieval_style_lootr", 45),     # #16 lootr (format 10 but wins lootr)
    ("fancy crops", 45),              # #17 crops
    ("fluffy carpet", 45),            # #21 wool/carpet
    ("modded swords", 46),            # #18 first-person item assets (high)
    ("better enchanting", 45), ("enchanting table", 45),  # #29
    ("lily pads", 45),                # #30 variety
    ("3d", 45),                       # #47 Nico's 3D Ladders (filename has 3d + ladders)
    ("torches", 45),                  # Torches Reimagined
    ("fancy", 45),
    ("cubic-sun-moon", 45),           # #35 sun/moon (shader patch pending)
    ("simple grass", 45),             # #19 grass flowers (bake pending)
    ("shivaklans", 45), ("animated textures", 45),  # #49 animated+emissive variety
    ("fusion stacking items", 45),    # #52 inventory item models
    ("cataclysm reimagined", 45),     # #55
    ("xali's potion", 40),            # #56 potions base (others can override)
    ("waystones", 45),                # #58
    ("muskets_overhaul", 45),         # kept musket pack (#40 Flintl0cks pulled)
    # -- GUI / icons / lang (top-ish, minimal conflict) --
    ("enhanced boss bars", 60),       # #46
    ("rpg_series_icons", 60), ("attribute icons", 60),  # #15 RPG icons base
    ("journeymap icons", 60),         # #57
    ("biomesnames", 60), ("terralithbiomesnames", 60),  # #43 name fixes
    ("descriptions", 60),             # enchantment descriptions
    ("rename compat", 60),            # The Rename Compat Project (lang/rename)
    # -- our fix layer (very top, below WNL-Custom) --
    ("texturefixes", 70),
]
def tier(f):
    fl = f.lower()
    for sub, t in TIER_RULES:
        # guard: "fresh textures" must NOT swallow "freshtextures+fa"
        if sub == "fresh textures" and "+fa" in fl:
            continue
        if sub in fl:
            return t
    return 40   # default: mod-specific item/block packs, above base, below category drivers

# === collect + order ===
packs = [f for f in os.listdir(SRC) if f.endswith(".zip") and not dropped_pack(f)]
dropped = [f for f in os.listdir(SRC) if f.endswith(".zip") and dropped_pack(f)]
packs.sort(key=lambda f: (tier(f), f.lower()))

# === per-file SANITIZER (preserved from the foundation fix) ===
ABSENT_NS = ("regions_unexplored:", "biomesoplenty:")
SANITIZE_LOG = []
def sanitize(n, data):
    nl = n.lower()
    if nl.endswith("/drowned3.jem"):
        SANITIZE_LOG.append("drop drowned3.jem (EMF player_rot_y)"); return None
    if nl.endswith("/cem/frog.properties"):
        SANITIZE_LOG.append("drop frog.properties (ETF no-rules)"); return None
    if "ghastling_explosion" in nl or ("accessibility" in nl and nl.endswith(".mcmeta")):
        SANITIZE_LOG.append("drop dead animatica anim " + n.split("/")[-1]); return None
    if "optifine/ctm/" in nl and nl.endswith(".properties"):
        try:
            kept = []
            for line in data.decode("utf-8", "replace").splitlines():
                s = line.strip()
                if s.startswith("tintIndex") and "=" in s and not s.split("=", 1)[1].strip().lstrip("-").isdigit():
                    SANITIZE_LOG.append("strip bad tintIndex " + n.split("/")[-1]); continue
                if s.startswith("tintBlock") and "=" in s and any(a in s for a in ABSENT_NS):
                    SANITIZE_LOG.append("strip absent tintBlock " + n.split("/")[-1]); continue
                kept.append(line)
            return ("\n".join(kept)).encode("utf-8")
        except Exception:
            return data
    return data

# === overlay resolution (preserved) ===
TARGET_FMT = 34
SKIP = ("pack.mcmeta", "pack.png")
JUNK = ("desktop.ini", ".ds_store", "thumbs.db")
def applicable_overlays(z):
    out = []
    try:
        meta = json.loads(z.read("pack.mcmeta").decode("utf-8", "replace"))
    except Exception:
        return out
    for ov in (meta.get("overlays") or {}).get("entries", []) or []:
        if not isinstance(ov, dict):
            continue
        fmts = ov.get("formats")
        if isinstance(fmts, dict):
            mn, mx = fmts.get("min_inclusive", 0), fmts.get("max_inclusive", 9999)
        elif isinstance(fmts, list) and len(fmts) >= 2:
            mn, mx = fmts[0], fmts[1]
        elif isinstance(fmts, int):
            mn, mx = fmts, fmts
        else:
            mn, mx = ov.get("min_format", 0), ov.get("max_format", 9999)
        try:
            if int(mn) <= TARGET_FMT <= int(mx) and ov.get("directory"):
                out.append(ov["directory"].rstrip("/") + "/assets/")
        except Exception:
            continue
    return out

def extract(zpath, packname):
    """Return {internal_path: clean_bytes} for one pack: base assets/ + applicable overlays,
    sanitized, with per-pack excludes applied. Used by the merge AND (future) category overrides."""
    out, ov_used = {}, []
    try:
        z = zipfile.ZipFile(zpath)
    except Exception as e:
        print("  SKIP (bad zip):", packname, e); return out, ov_used
    skip_pred = exclude_pred(packname)
    # ARCHITECTURE GUARD: the mob/variety/FA band (tier >= 50) is the MOB base (#59); it must NOT win
    # vanilla BLOCK textures (Stay True owns those, #28). Mixed packs like Drodi's Assortments ship
    # stray block textures (planks/crafting table) that would clobber the block base — scope them out.
    mob_band = tier(packname) >= 50
    ovs = applicable_overlays(z)
    if ovs:
        ov_used = [o[:-8] for o in ovs]
    for prefix in ["assets/"] + ovs:
        for n in z.namelist():
            if n.endswith("/") or n in SKIP or not n.startswith(prefix):
                continue
            internal = "assets/" + n[len(prefix):]
            il = internal.lower()
            if il.endswith(JUNK):
                continue
            if skip_pred and skip_pred(il):
                continue
            if mob_band and "/textures/block/" in il:
                continue   # mob/variety pack — block textures stay with the block base
            try:
                raw = z.read(n)
            except Exception:
                continue
            clean = sanitize(internal, raw)
            if clean is None:
                continue
            out[internal] = clean
    z.close()
    return out, ov_used

# === merge low->high ===
files = {}
provenance = {}
per_pack_added = {}
overlay_log = []
for f in packs:
    assets, ov_used = extract(os.path.join(SRC, f), f)
    if ov_used:
        overlay_log.append("%-46s + overlays %s" % (f[:46], ov_used))
    for internal, data in assets.items():
        files[internal] = data
        provenance[internal] = f
    per_pack_added[f] = len(assets)

# === WNL-Custom authoring layer (#62) — folder, applied LAST = TOP precedence ===
custom_added = 0
if os.path.isdir(CUSTOM_DIR):
    base = os.path.join(CUSTOM_DIR, "assets")
    if os.path.isdir(base):
        for dp, _, fns in os.walk(base):
            for fn in fns:
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, CUSTOM_DIR).replace(os.sep, "/")
                if rel.lower().endswith(JUNK):
                    continue
                try:
                    with open(full, "rb") as fh:
                        files[rel] = fh.read()
                    provenance[rel] = "WNL-Custom"
                    custom_added += 1
                except Exception:
                    continue

# === pack.mcmeta (format 34) + CREDITS ===
mcmeta = {"pack": {"pack_format": 34,
    "description": "§6WNL Mega-Pack§r — curated merge (Stay True + FreshAnimations anchors), ported to 1.21.1.\nPrivate/personal use. Credit to all original authors — see CREDITS.txt."}}
credits = ["WNL Mega-Pack — curated personal resource collection (PRIVATE / personal use only).",
           "All textures belong to their original authors. Local merge of packs the user owns,",
           "ported to MC 1.21.1 (format 34), curated per _dev/megapack-curation-rules.md. NOT for redistribution.",
           "", "Source packs (low->high precedence):"]
for f in packs:
    credits.append("  [tier %2d] %s  (+%d assets won)" % (tier(f), f, sum(1 for w in provenance.values() if w == f)))
if custom_added:
    credits.append(""); credits.append("WNL-Custom authoring layer: +%d assets (top precedence)" % custom_added)
if dropped:
    credits.append(""); credits.append("Dropped (mine-only concept packs + removed mods — art not shipped):")
    for f in dropped:
        credits.append("  %s" % f)

# === emit ===
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    z.writestr("pack.mcmeta", json.dumps(mcmeta, indent=2))
    z.writestr("CREDITS.txt", "\n".join(credits))
    for n, data in files.items():
        z.writestr(n, data)

sz = os.path.getsize(OUT) / (1024 * 1024)

# === emit human-readable CURATED LIST (_dev/megapack-curated-list.md) for user review/editing ===
import collections as _c
def _cat(p):
    parts = p.split("/"); ns = parts[1] if len(parts) > 1 else "?"; rest = "/".join(parts[2:])
    if ns == "minecraft":
        seg = rest.split("/")
        if rest.startswith("textures/entity/"): return ("1 MOB (entity textures)", seg[2] if len(seg) > 2 else "_")
        if rest.startswith("optifine/cem"):     return ("2 MOB (CEM .jem models)", seg[-1])
        if rest.startswith("optifine/random"):  return ("3 MOB (ETF random variants)", seg[-1])
        if rest.startswith("optifine/ctm"):     return ("8 CTM", seg[2] if len(seg) > 2 else "_")
        if rest.startswith("textures/block/"):  return ("4 BLOCK", seg[-1])
        if rest.startswith("textures/item/"):   return ("5 ITEM", seg[-1])
        if rest.startswith("textures/gui") or "/gui/" in rest: return ("6 GUI", seg[-1])
        if rest.startswith("textures/painting"):return ("7 PAINTING", seg[-1])
        if rest.startswith("models/"):          return ("9 MODEL (block/item)", seg[-1])
        if "font" in rest:                       return ("A FONT", seg[-1])
        return ("B MISC minecraft", rest)
    return ("Z MODDED: " + ns, "")
cats = _c.defaultdict(lambda: _c.defaultdict(set))  # category -> key -> set(winners)
foot = _c.Counter()
for path, win in provenance.items():
    c, key = _cat(path); cats[c][key].add(win); foot[win] += 1
ml = ["# WNL Mega-Pack — CURATED LIST (auto-generated by build_megapack.py — edit the RULES, not this file)",
      "", "Every asset CATEGORY -> which source pack WON it. Review for wrong winners; fix in",
      "`_dev/megapack-curation-rules.md` + the tier table, then rebuild. ⚠ = split (>1 pack wins one",
      "mob's files = texture/model mismatch risk). Generated %d assets across %d packs + WNL-Custom." % (len(provenance), len(packs)),
      "", "## Pack footprint (assets won)"]
for pk, n in foot.most_common():
    ml.append("- %5d  %s" % (n, pk))
for c in sorted(cats):
    keys = cats[c]
    ml.append(""); ml.append("## %s  (%d entries)" % (c[2:] if c[1] == " " else c, len(keys)))
    if c.startswith("Z"):   # modded: summarize winners (too many to list per-asset)
        wc = _c.Counter()
        for ws in keys.values():
            for w in ws: wc[w] += 1
        for w, n in wc.most_common():
            ml.append("  %s  (%d)" % (w, n))
        continue
    for key in sorted(keys):
        wins = sorted(keys[key])
        flag = " ⚠SPLIT" if (c.startswith("1") or c.startswith("2") or c.startswith("3")) and len(wins) > 1 else ""
        ml.append("- **%s** ← %s%s" % (key, ", ".join(wins), flag))
try:
    with open(os.path.join(ROOT, "_dev", "megapack-curated-list.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(ml))
    _listed = len(provenance)
except Exception as _e:
    _listed = 0; print("  (curated list write failed:", _e, ")")

print("=== WNL-MegaPack.zip built (curation engine Phase 1) ===")
print("  %d packs merged, %d dropped, %d unique assets, +%d WNL-Custom, %.1f MB"
      % (len(packs), len(dropped), len(files), custom_added, sz))
print("  OVERLAYS resolved for format %d in %d packs" % (TARGET_FMT, len(overlay_log)))
print("  SANITIZER applied %d fix/drop ops" % len(SANITIZE_LOG))
for s in sorted(set(SANITIZE_LOG)):
    print("    - " + s)
print("\n=== precedence order (low->high = base->override) ===")
last = None
for f in packs:
    t = tier(f)
    if t != last:
        print("  --- tier %d ---" % t); last = t
    print("    %-48s (+%d)" % (f[:48], per_pack_added.get(f, 0)))
if dropped:
    print("\n  DROPPED (mine-only/removed):", ", ".join(dropped))
print("\n  vanilla textures resolved from:")
for ns_pref in ("assets/minecraft/textures/block/stone.png", "assets/minecraft/textures/block/grass_block_top.png",
                "assets/minecraft/textures/block/oak_planks.png"):
    print("    %-44s <- %s" % (ns_pref.split("block/")[1], provenance.get(ns_pref, "(vanilla default)")))
