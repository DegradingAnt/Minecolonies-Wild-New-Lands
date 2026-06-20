#!/usr/bin/env python3
"""
cooccur_palettes.py — derive distinct WNL palettes from block CO-OCCURRENCE.

Scans every structure mod's .nbt templates and asks: which blocks actually appear
TOGETHER in the same structure? Uses Jaccard association (|A&B| / |A|B|) so it
surfaces blocks that *specifically* belong together — including RARER accent blocks —
instead of just re-listing dirt/cobblestone (which co-occur with everything).

Then greedily clusters the association graph into themed palettes.

REFERENCE ONLY (design-policy): we mine which styles the pack already uses + credit;
we build our own vanilla-block placement. Output:
  _dev/wnl-moogbridges-design/structure_inspo/PALETTES_COMBINED.md
  _dev/wnl-moogbridges-design/structure_inspo/cooccur.json
"""
import sys, os, glob, zipfile, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scrape_structures import palette_of, NBT_RE, source_name

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS = os.path.join(ROOT, "mods")
OUT  = os.path.join(ROOT, "_dev", "wnl-moogbridges-design", "structure_inspo")

# blocks that are environment / structural noise, not build palette
JUNK = {"air","cave_air","void_air","jigsaw","structure_void","barrier","light",
        "moving_piston","piston_head","water","lava","bubble_column","kelp",
        "kelp_plant","seagrass","tall_seagrass","grass_block","dirt","short_grass",
        "tall_grass","snow","powder_snow","fire","soul_fire"}

def base(bid):
    return bid.split('[')[0]

def is_junk(bid):
    s = base(bid).split(':')[-1]
    return s in JUNK

# building materials only — exclude ores/plants/environment so palettes are buildable
BUILD_INC = ("planks","_log","_wood","_stem","hyphae","stairs","slab","_wall","fence",
    "_gate","door","trapdoor","brick","tile","cobble","deepslate","granite","andesite",
    "diorite","sandstone","terracotta","concrete","glazed","glass","copper","prismarine",
    "blackstone","basalt","tuff","calcite","quartz","purpur","end_stone","nether_brick",
    "_mud","mud_","clay","pillar","chiseled","polished","smooth","cut_","lantern","chain",
    "_bars","lamp","bookshelf","barrel","composter","scaffolding","shingle","bamboo",
    "mosaic","ladder","wool","carpet","gravel","podzol","coarse_dirt","rooted_dirt",
    "dripstone_block","mossy","cracked","_path")
BUILD_EXC = ("ore","coral","sapling","propagule","leaves","mushroom","fungus","nylium",
    "roots","sprouts","wart","crop","kelp","seagrass","vine","lichen","bee_nest","honey",
    "spawner","command","infested","budding","amethyst","sulfur","cinnabar","potent",
    "spike","froglight","sculk","spore","seeds","azalea","_stem_")
def is_build(bid):
    s = base(bid).split(':')[-1]
    if any(x in s for x in BUILD_EXC): return False
    return any(x in s for x in BUILD_INC)

def main():
    # ---- pass 1 (cached): per-structure palettes ----
    CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cooc_cache.json")
    structures = []          # list of (list(blocks), modsource)
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            structures = json.load(f)
        sys.stderr.write(f"[cooc] loaded {len(structures)} structures from cache\n")
    else:
        for jp in sorted(glob.glob(os.path.join(MODS, "*.jar"))):
            jar = os.path.basename(jp); src = source_name(jar)
            try: z = zipfile.ZipFile(jp)
            except Exception: continue
            names = [i.filename for i in z.infolist() if NBT_RE.search(i.filename)]
            if not names: z.close(); continue
            with z:
                for fn in names:
                    try: pal = palette_of(z.read(fn))
                    except Exception: pal = None
                    if not pal: continue
                    blocks = sorted(set(base(b) for b in pal if not is_junk(b)))
                    if len(blocks) < 2: continue
                    structures.append([blocks, src])
            sys.stderr.write(f"[cooc] {jar}\n"); sys.stderr.flush()
        with open(CACHE, "w") as f:
            json.dump(structures, f)
        sys.stderr.write(f"[cooc] cached {len(structures)} structures\n")

    freq = collections.Counter()
    block_mods = collections.defaultdict(collections.Counter)
    for blocks, src in structures:
        for b in blocks:
            freq[b] += 1
            block_mods[b][src] += 1
    total = len(structures)
    # ---- vocab: drop ultra-common (in >55% of structures) + ultra-rare (<6) ----
    hi = 0.55 * total
    # vanilla BUILD blocks only (modded = inspiration, approximated later)
    vocab = {b for b, c in freq.items()
             if 6 <= c <= hi and b.startswith("minecraft:") and is_build(b)}
    sys.stderr.write(f"[cooc] {total} structures, {len(freq)} blocks, "
                     f"{len(vocab)} in vocab\n")

    # ---- pass 2: co-occurrence within vocab ----
    cooc = collections.Counter()
    for blocks, _ in structures:
        v = sorted(b for b in blocks if b in vocab)
        for i in range(len(v)):
            for j in range(i+1, len(v)):
                cooc[(v[i], v[j])] += 1

    def jac(a, b):
        key = (a, b) if a < b else (b, a)
        c = cooc.get(key, 0)
        if not c: return 0.0
        return c / (freq[a] + freq[b] - c)

    # adjacency of strong associations
    MIN_C, MIN_J = 8, 0.16
    adj = collections.defaultdict(dict)
    for (a, b), c in cooc.items():
        if c < MIN_C: continue
        j = c / (freq[a] + freq[b] - c)
        if j >= MIN_J:
            adj[a][b] = j; adj[b][a] = j

    # ---- greedy themed clustering ----
    # anchor on distinctive-but-solid materials (mid-frequency, common-first), then
    # grow the palette outward by association — surfaces rarer accents around an anchor.
    used = set()
    seeds = sorted((b for b in adj if 0.012*total <= freq[b] <= 0.35*total),
                   key=lambda b: -freq[b])
    palettes = []
    for seed in seeds:
        if seed in used: continue
        nbrs = [b for b, _ in sorted(adj[seed].items(), key=lambda kv: -kv[1])
                if b not in used]
        members = [seed] + nbrs[:11]
        # keep members linked to >=2 others in the group (cohesion)
        keep = [m for m in members
                if m == seed or sum(1 for o in members if o != m and o in adj[m]) >= 2]
        if len(keep) < 4: continue
        for m in keep: used.add(m)
        # credit: top mods across members
        mc = collections.Counter()
        for m in keep:
            for mod, c in block_mods[m].items(): mc[mod] += c
        palettes.append({
            "seed": seed,
            "blocks": sorted(keep, key=lambda b: -freq[b]),
            "size": len(keep),
            "avg_freq": round(sum(freq[m] for m in keep)/len(keep)),
            "mods": [m for m, _ in mc.most_common(4)],
        })
        if len(palettes) >= 16: break

    result = {"total_structures": total, "palettes": palettes}
    with open(os.path.join(OUT, "cooccur.json"), "w") as f:
        json.dump({"freq": dict(freq.most_common(400)),
                   "palettes": palettes}, f, indent=1)
    write_md(result, freq, total)
    sys.stderr.write(f"[cooc] DONE: {len(palettes)} palettes\n")

def fam(blocks):
    """name a palette by its most characteristic material family"""
    s = set(b.split(':')[-1] for b in blocks)
    def has(k): return any(k in x for x in s)
    if has("spruce") and (has("stone_brick") or "stone_bricks" in s):
        return "Rustic town (spruce + stone-brick + lantern)"
    if has("purpur") or has("end_stone"):    return "End-stone / purpur"
    if has("blackstone") or "polished_basalt" in s: return "Blackstone / nether keep"
    if has("deepslate"):                     return "Deepslate / dark fortress"
    if has("nether_brick"):                  return "Nether brick"
    if has("mud_brick") or has("packed_mud"):return "Mud-brick / wattle village"
    if has("red_sandstone"):                 return "Red sandstone / mesa"
    if has("sandstone"):                     return "Sandstone / desert"
    if has("prismarine"):                    return "Prismarine / ocean"
    if has("terracotta"):                    return "Terracotta / adobe"
    if has("tuff") or has("waxed_") or has("copper"): return "Tuff + copper / engineered"
    if has("quartz"):                        return "Quartz / refined"
    if "bricks" in s:                        return "Clay brick"
    if has("mossy") or has("cracked"):       return "Mossy / cracked ruin"
    if has("andesite"):                      return "Andesite"
    if has("diorite"):                       return "Diorite / pale"
    for w, label in [("dark_oak","Dark-oak timber"),("spruce","Spruce timber"),
        ("jungle","Jungle timber"),("birch","Birch timber"),("acacia","Acacia / savanna"),
        ("cherry","Cherry grove"),("mangrove","Mangrove"),("bamboo","Bamboo"),("oak","Oak timber")]:
        if has(w): return label
    if has("stone_brick") or has("cobble"):  return "Stone-brick / cobble masonry"
    return sorted(s)[0].replace('_',' ').title()

def disp(b):
    ns, s = b.split(':') if ':' in b else ("minecraft", b)
    return s if ns == "minecraft" else b

def write_md(result, freq, total):
    L = ["# WNL Combined-Block Palettes (co-occurrence derived)\n",
         f"_Blocks that actually appear TOGETHER across {total} structure templates "
         "pack-wide, grouped by Jaccard association so rarer accent blocks surface. "
         "REFERENCE ONLY — mine the style, build vanilla, credit the source "
         "([[design-policy-original-plus-credited-inspiration]]). "
         "Generated by `.uvrun/cooccur_palettes.py`._\n",
         "Use these as ready-made palettes for `wnl_pathbridges` bridge tiers, path "
         "edging, deco middles, and biome variants — pick a base + an accent family.\n"]
    for i, p in enumerate(result["palettes"], 1):
        name = fam(p["blocks"])
        cred = ", ".join(p["mods"])
        L.append(f"## {i}. {name}")
        L.append(f"*seen together in {p['mods'] and 'mods: '+cred or 'various'}*  ")
        L.append("`" + "  ".join(disp(b) for b in p["blocks"]) + "`\n")
    with open(os.path.join(OUT, "PALETTES_COMBINED.md"), "w") as f:
        f.write("\n".join(L))

if __name__ == "__main__":
    main()
