"""Build WNL-MegaPack.zip — port + merge ALL resourcepacks/ into ONE pack_format-34 pack for 1.21.1.
Strategy (megapack-plan.md): use the latest art, port every pack down to 1.21.1 by (a) normalizing
pack_format to 34, (b) keeping all assets (textures always apply; 1.21.4+ items/ defs stay inert/harmless;
unknown model fields fall back). Overlay packs LOW->HIGH precedence so the highest pack with an asset wins
and lower packs fill gaps. Stay True is the base + wins shared vanilla textures; Fresh/Musgo/VanillaExp sit
BELOW it (gap-fill); FA ecosystem wins entities; the 3 non-fa mob dupes are dropped; WNL-TextureFixes on top.
PRIVATE/personal only (bundles third-party art). Run: python .uvrun/build_megapack.py"""
import os, io, json, zipfile, re

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
RP = os.path.join(ROOT, "resourcepacks")          # OUTPUT lives here (the merged megapack)
# SOURCE packs live in resourcepacks/ alongside the output, so CurseForge surfaces their updates
# (the user wants to SEE when a source pack updates). excluded() drops the megapack + dupes from the merge.
# Dev override: set WNL_MEGAPACK_SRC to build from an external sources folder instead.
SRC = os.environ.get("WNL_MEGAPACK_SRC", RP)
OUT = os.path.join(RP, "WNL-MegaPack.zip")

# --- packs to EXCLUDE: the 3 non-fa mob dupes (FA variants win) + our own output if it exists ---
EXCLUDE_SUBSTR = ["creepers-refreshed-v", "golems-refreshed-v", "mobs-refreshed-v", "wnl-megapack"]
DROP_NAMES = ["visual titles"]   # unconditional drops — Visual Traveler's Titles (its mod was removed)
def excluded(f):
    fl = f.lower()
    if any(d in fl for d in DROP_NAMES):
        return True
    # keep the -fa ones; drop only the plain non-fa (…-refreshed-vN, no "fa")
    for s in EXCLUDE_SUBSTR:
        if s in fl and "fa" not in fl.replace("-refreshed", ""):
            # guard: "creepers-refreshed-fa-v1.0" contains "creepers-refreshed-v"? no (has -fa- between). safe.
            if "refreshed-fa" in fl:
                return False
            return True
    return False

# --- precedence tiers (LOW number = applied first = LOWER priority; HIGH overwrites) ---
def tier(f):
    fl = f.lower()
    def has(*ks): return any(k in fl for k in ks)
    # base vanilla overhauls — BELOW Stay True so Stay True wins shared vanilla, these fill gaps
    if "fresh textures" in fl and "+fa" not in fl: return 10
    if fl.startswith("musgo"): return 10
    if "vanilla experience" in fl: return 11
    # connected-texture packs (Jacosvaldo + Fusion + snow) — below Stay True; fill CTM gaps
    if has("connected-", "connected_", "fusion", "geo - ", "snow side"): return 13
    # Stay True base — wins vanilla textures + its own CTM
    if fl.startswith("stay true"): return 15
    # the Stay True modded addon (Compats Reforged: Create/Quark/FD) — Stay-True-style modded blocks
    if fl.startswith("staytrue26") or "stay true compat" in fl: return 42
    # block/deco vanilla overrides
    if has("better-leaves", "fluffy carpet", "ladders", "torches", "fancy crops", "simple grass"): return 30
    # --- FreshAnimations ecosystem: EXPLICIT sub-tiers (higher wins) ---
    # FA base + official extensions OWN the 29 vanilla core mobs; every other FA-adjacent pack sits
    # BELOW them so it only fills modded/variant mobs FA doesn't define. This fixes the old flat-sort
    # clobber (mobs-refreshed-fa / FreshTextures+FA were winning spider/husk/illager/piglin over FA →
    # broken animations). User intent: "FreshAnimations+FA+All_Extensions own core mobs." See pack_rules.
    FA_TIERS = [   # (filename substring, tier) — most-specific first
        ("fa+all_extensions", 56), ("fa+player", 56),     # 56: official extensions — above base (FA docs)
        ("freshanimations", 55),                          # 55: BASE — wins all 29 core mobs
        # 52: FA mod-compat patches (modded mobs animate w/ FA; lose vanilla-core to base above them)
        ("fresh patch", 52), ("freshly modded", 52), ("abnormally fresh", 52), ("fa illager", 52),
        ("armored illager", 52), ("eating animations", 52), ("quarkfacompat", 52), ("morepiglins", 52),
        ("assorted allays", 52), ("wandering traders", 52), ("mca_resourcepack", 52), ("semos", 52),
        # 51: alt-style "refreshed" mob retextures + movement anims (lose vanilla-core to FA)
        ("refreshed-fa", 51), ("refreshed-v", 51), ("boss-refreshed", 51), ("fresh moves", 51),
        # 50: FA texture-compat layers (non-FA-animated looks; lose to FA models)
        ("freshtextures+fa", 50), ("th + fresh", 50),
    ]
    for sub, t in FA_TIERS:
        if sub in fl:
            return t
    # GUI / icons / lang / font — top-ish, minimal conflict
    if has("icons", "descriptions", "biomesnames", "healthbars", "armor trim", "journeymap"): return 60
    # our fix layer — very top
    if "texturefixes" in fl: return 70
    # everything else: mod-specific item/block packs — mid, above base
    return 40

# --- collect + order ---
packs = [f for f in os.listdir(SRC) if f.endswith(".zip") and not excluded(f)]
dropped = [f for f in os.listdir(SRC) if f.endswith(".zip") and excluded(f)]
packs.sort(key=lambda f: (tier(f), f.lower()))

# --- merge: overlay low->high into a path->bytes map (later wins) ---
SKIP = ("pack.mcmeta", "pack.png")
files = {}      # internal path -> bytes
provenance = {} # internal path -> winning pack (for stats)
per_pack_added = {}
for f in packs:
    try:
        z = zipfile.ZipFile(os.path.join(SRC, f))
    except Exception as e:
        print("  SKIP (bad zip):", f, e); continue
    added = 0
    for n in z.namelist():
        if n.endswith("/") or n in SKIP:
            continue
        if not n.startswith("assets/"):
            continue
        nl = n.lower()
        if nl.endswith("desktop.ini") or nl.endswith(".ds_store") or nl.endswith("thumbs.db"):
            continue   # strip Windows/macOS folder cruft that rode in from source packs
        try:
            files[n] = z.read(n)
        except Exception:
            continue
        provenance[n] = f
        added += 1
    per_pack_added[f] = added

# --- write our own pack.mcmeta (format 34) + CREDITS.txt ---
mcmeta = {"pack": {"pack_format": 34,
    "description": "§6WNL Mega-Pack§r — Stay True base, merged collection (ported to 1.21.1).\nPrivate/personal use. All credit to original pack authors — see CREDITS.txt."}}
credits = ["WNL Mega-Pack — merged personal resource collection (PRIVATE / personal use only).",
           "All textures belong to their original authors. This is a local merge of packs the user owns,",
           "ported to MC 1.21.1 (pack_format 34) and layered Stay-True-first. NOT for redistribution.",
           "", "Source packs (low->high precedence):"]
for f in packs:
    credits.append("  [tier %2d] %s  (+%d assets won)" % (tier(f), f, sum(1 for p,w in provenance.items() if w == f)))
if dropped:
    credits.append("");  credits.append("Dropped (non-FA mob dupes, superseded by FA variants):")
    for f in dropped: credits.append("  %s" % f)

# --- emit zip ---
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    z.writestr("pack.mcmeta", json.dumps(mcmeta, indent=2))
    z.writestr("CREDITS.txt", "\n".join(credits))
    for n, data in files.items():
        z.writestr(n, data)

sz = os.path.getsize(OUT) / (1024 * 1024)
print("=== WNL-MegaPack.zip built ===")
print("  %d packs merged, %d dropped, %d unique asset files, %.1f MB" % (len(packs), len(dropped), len(files), sz))
print("\n=== precedence order (low->high = base->override) ===")
last = None
for f in packs:
    t = tier(f)
    if t != last:
        print("  --- tier %d ---" % t); last = t
    print("    %-46s (+%d)" % (f[:46], per_pack_added.get(f, 0)))
if dropped:
    print("\n  DROPPED (non-fa dupes):", ", ".join(dropped))
print("\n  vanilla textures resolved from:")
for ns_pref in ("assets/minecraft/textures/block/stone.png", "assets/minecraft/textures/block/grass_block_top.png",
                "assets/minecraft/textures/block/oak_planks.png"):
    print("    %-50s <- %s" % (ns_pref.split("block/")[1], provenance.get(ns_pref, "(vanilla default)")))
