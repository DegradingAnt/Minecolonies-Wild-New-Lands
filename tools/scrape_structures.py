#!/usr/bin/env python3
"""
scrape_structures.py — design-inspiration palette scraper for WNL.

For every structure mod in mods/, parse the block PALETTE of each structure .nbt
template (data/<ns>/structure[s]/**.nbt) and aggregate which blocks each mod
builds with. Output a credited design-inspiration library.

This is REFERENCE MINING per design-policy-original-plus-credited-inspiration:
we read palettes to learn styles + credit sources; we do NOT copy/ship any NBT,
texture, or model. Output is palette statistics + design notes only.

Light on CPU: parses only the 'palette'/'palettes' tags and byte-SKIPS the giant
'blocks'/'entities' arrays (no object allocation), so it's safe to run while the
game is open.

Outputs:
  _dev/wnl-moogbridges-design/structure_inspo/palettes.json   (machine)
  _dev/wnl-moogbridges-design/structure_inspo/INSPIRATION.md  (human, credited)
"""
import struct, gzip, io, zipfile, os, sys, json, collections, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS = os.path.join(ROOT, "mods")
OUT  = os.path.join(ROOT, "_dev", "wnl-moogbridges-design", "structure_inspo")
os.makedirs(OUT, exist_ok=True)

NBT_RE = re.compile(r'structures?/[^?]*\.nbt$', re.I)

# ---------- minimal NBT reader: only palette, skip the rest ----------
class End(Exception): pass

def _rstr(f):
    ln = struct.unpack('>H', f.read(2))[0]
    return f.read(ln).decode('utf-8', 'replace')

def _skip(f, t):
    if   t == 1: f.seek(1, 1)
    elif t == 2: f.seek(2, 1)
    elif t == 3: f.seek(4, 1)
    elif t == 4: f.seek(8, 1)
    elif t == 5: f.seek(4, 1)
    elif t == 6: f.seek(8, 1)
    elif t == 7:
        n = struct.unpack('>i', f.read(4))[0]; f.seek(max(n,0), 1)
    elif t == 8:
        n = struct.unpack('>H', f.read(2))[0]; f.seek(n, 1)
    elif t == 9:
        it = f.read(1)[0]; n = struct.unpack('>i', f.read(4))[0]
        for _ in range(max(n,0)): _skip(f, it)
    elif t == 10:
        while True:
            b = f.read(1)
            if not b or b[0] == 0: break
            ln = struct.unpack('>H', f.read(2))[0]; f.seek(ln, 1)
            _skip(f, b[0])
    elif t == 11:
        n = struct.unpack('>i', f.read(4))[0]; f.seek(4*max(n,0), 1)
    elif t == 12:
        n = struct.unpack('>i', f.read(4))[0]; f.seek(8*max(n,0), 1)
    else:
        raise End()

def _read_palette_list(f):
    """f positioned at start of a TAG_List payload that is a list of compounds
    each having a 'Name' string. Return list of block-id strings."""
    it = f.read(1)[0]                       # element type (should be 10 compound)
    n  = struct.unpack('>i', f.read(4))[0]
    names = []
    if it != 10:
        for _ in range(max(n,0)): _skip(f, it)
        return names
    for _ in range(max(n,0)):
        nm = None
        while True:
            b = f.read(1)
            if not b or b[0] == 0: break
            t = b[0]; key = _rstr(f)
            if t == 8 and key == "Name":
                nm = _rstr(f)
            else:
                _skip(f, t)
        if nm: names.append(nm)
    return names

def palette_of(data):
    """Return a set of block ids used in this structure (union over palettes)."""
    if data[:2] == b'\x1f\x8b':
        try: data = gzip.decompress(data)
        except Exception: return None
    f = io.BytesIO(data)
    h = f.read(1)
    if not h or h[0] != 10: return None
    _rstr(f)                                # root name
    names = set()
    try:
        while True:
            b = f.read(1)
            if not b or b[0] == 0: break
            t = b[0]; key = _rstr(f)
            if t == 9 and key == "palette":
                names.update(_read_palette_list(f))
            elif t == 9 and key == "palettes":
                it = f.read(1)[0]; n = struct.unpack('>i', f.read(4))[0]
                if it == 9:                 # list of lists
                    for _ in range(max(n,0)):
                        names.update(_read_palette_list(f))
                else:
                    for _ in range(max(n,0)): _skip(f, it)
            else:
                _skip(f, t)
    except (End, struct.error, IndexError):
        pass
    return names

# ---------- block categorisation for design relevance ----------
def cat(bid):
    b = bid.split('[')[0]
    s = b.split(':')[-1]
    tags = set()
    P = ("path","coarse_dirt","rooted_dirt","podzol","dirt_path","grass_path",
         "gravel","mud","packed_mud","farmland","suspicious_","dirt")
    M = ("cobblestone","stone_brick","mossy","cracked","chiseled","andesite",
         "deepslate","polished","_bricks","brick","blackstone","tuff","calcite",
         "smooth_stone","stone_slab","stone_stair")
    W = ("_log","_wood","planks","_stairs","_slab","fence","stripped_","_fence",
         "scaffolding","ladder","trapdoor")
    D = ("lantern","campfire","torch","barrel","flower_pot","potted","composter",
         "lectern","bell","chain","banner","hay","bookshelf","candle","cauldron",
         "leaves","sapling","bush","fern","grass","flower","vine","moss")
    if any(k in s for k in P): tags.add("path")
    if any(k in s for k in M): tags.add("masonry")
    if any(k in s for k in W): tags.add("wood")
    if any(k in s for k in D): tags.add("deco")
    if "water" in s or "kelp" in s or "lily" in s or "seagrass" in s or "coral" in s:
        tags.add("water")
    return tags

def source_name(jar):
    n = re.sub(r'[-_ ]v?\d[\d.\w+\[\]() -]*$', '', jar)
    n = re.sub(r'\.jar$', '', n)
    n = re.sub(r'\[?neoforge\]?', '', n, flags=re.I).strip(" -_[]")
    return n or jar

# ---------- scan ----------
def jar_structures(path):
    out = []
    try:
        z = zipfile.ZipFile(path)
    except Exception:
        return out
    with z:
        for info in z.infolist():
            if NBT_RE.search(info.filename):
                out.append(info.filename)
    return out

def main():
    jars = sorted(glob.glob(os.path.join(MODS, "*.jar")))
    catalog = {}
    grand = collections.Counter()
    for jp in jars:
        jar = os.path.basename(jp)
        try:
            z = zipfile.ZipFile(jp)
        except Exception:
            continue
        names = [i.filename for i in z.infolist() if NBT_RE.search(i.filename)]
        if not names:
            z.close(); continue
        present = collections.Counter()    # block -> # structures containing it
        nstruct = 0
        with z:
            for fn in names:
                try:
                    data = z.read(fn)
                except Exception:
                    continue
                pal = palette_of(data)
                if pal is None:
                    continue
                nstruct += 1
                for b in pal:
                    present[b.split('[')[0]] += 1
        if nstruct == 0:
            continue
        # build categorised view
        buckets = {k: collections.Counter() for k in
                   ("path","masonry","wood","deco","water")}
        for b, c in present.items():
            for t in cat(b):
                buckets[t][b] += c
        catalog[jar] = {
            "source": source_name(jar),
            "structures_parsed": nstruct,
            "top": present.most_common(25),
            "buckets": {k: v.most_common(12) for k, v in buckets.items()},
        }
        for b, c in present.items():
            grand[b] += c
        sys.stderr.write(f"[scrape] {jar}: {nstruct} structures, "
                         f"{len(present)} block types\n")
        sys.stderr.flush()

    result = {"grand_top": grand.most_common(60), "mods": catalog}
    with open(os.path.join(OUT, "palettes.json"), "w") as f:
        json.dump(result, f, indent=1)
    write_md(result)
    sys.stderr.write(f"[scrape] DONE: {len(catalog)} structure mods scraped\n")

def fmt(pairs, ratio_of=None):
    out = []
    for b, c in pairs:
        s = b.split(':')[-1]
        ns = b.split(':')[0]
        label = s if ns in ("minecraft",) else b
        if ratio_of:
            out.append(f"{label}·{round(100*c/ratio_of)}%")
        else:
            out.append(f"{label}×{c}")
    return ", ".join(out)

def write_md(result):
    lines = []
    lines.append("# WNL Structure-Palette Inspiration Library\n")
    lines.append("_Auto-scraped block palettes from every structure mod in the pack — "
                 "REFERENCE ONLY (design-policy: mine styles + credit, never copy "
                 "assets). `%` = share of a mod's structures that use the block "
                 "(presence frequency). Generated by `.uvrun/scrape_structures.py`._\n")
    mods = result["mods"]
    # sort by richness of overworld build palette (path+masonry+wood presence)
    def relevance(v):
        b = v["buckets"]
        return sum(c for _, c in b["path"]) + sum(c for _, c in b["masonry"]) \
             + sum(c for _, c in b["wood"])
    order = sorted(mods.items(), key=lambda kv: relevance(kv[1]), reverse=True)
    lines.append("## Cross-pack signature blocks (all structures)\n")
    lines.append(fmt(result["grand_top"][:40]) + "\n")
    lines.append("## Per-mod palettes (richest builders first)\n")
    for jar, v in order:
        n = v["structures_parsed"]
        lines.append(f"### {v['source']}  \n`{jar}` — {n} structures\n")
        lines.append(f"- **top:** {fmt(v['top'][:18], n)}")
        for k, title in (("path","PATH-surface"),("masonry","MASONRY"),
                         ("wood","WOOD/timber"),("deco","DECO/foliage"),
                         ("water","WATER")):
            if v["buckets"][k]:
                lines.append(f"- **{title}:** {fmt(v['buckets'][k], n)}")
        lines.append("")
    with open(os.path.join(OUT, "INSPIRATION.md"), "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
