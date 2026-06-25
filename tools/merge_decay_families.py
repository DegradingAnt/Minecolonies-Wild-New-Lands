#!/usr/bin/env python3
"""Merge the decay-palette-sweep agent output (.uvrun/decay_cand/out_*.json) into
config/wnl_pathways/condition.json. Re-validates EVERY id against the real jar inventory
(block_inventory.json) and enforces CLASS-LOCK (base shape == variant shape) as a safety net —
agents can't smuggle in a hallucinated id or a slab-in-a-full-family. UNION merge: never drops an
existing/Stoneworks variant. Backs up first; reports added/upgraded/dropped + every rejected id."""
import json, glob, re, shutil
from collections import OrderedDict

INST = r"C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version"
CFG  = INST + "/config/wnl_pathways/condition.json"
INVF = INST + "/.uvrun/block_inventory.json"

inv = json.load(open(INVF, encoding="utf-8"))
EXIST = {f"{ns}:{p}" for ns, ps in inv.items() for p in ps}            # every real block id in the pack
DECAY = re.compile(r"(mossy|moss_|cracked|cobbled|chipped|weather|broken|ruin|worn|erod|crumbl|decay|rotten|rotted|dilapidat|tatter|overgrown|rough)")
def shp(fid):
    p = fid.split(":")[-1]
    for s in ("_stairs","_slab","_wall","_fence"):
        if p.endswith(s): return s
    return "full"

# material-token safety net: base + variant must share the same stone/wood token (catches andesite->diorite,
# oak->spruce within a category that passed the shape check). LONGEST first so dark_oak beats oak, etc.
TOKENS = ["dark_prismarine","prismarine","red_sandstone","sandstone","deepslate","blackstone","end_stone",
          "andesite","diorite","granite","calcite","basalt","tuff","quartz","purpur","netherrack","nether_brick",
          "terracotta","limestone","marble","travertine","mud","cobblestone","stone",
          "dark_oak","mangrove","crimson","warped","spruce","birch","jungle","acacia","cherry","bamboo","oak",
          "mushroom","willow","maple","redwood","fir","ash","palm","walnut","pine","poplar","hazel"]
def tok(fid):
    p = fid.split(":")[-1]
    for t in TOKENS:
        if t in p: return t
    return None
def same_material(base, var):
    tb, tv = tok(base), tok(var)
    return tb is None or tv is None or tb == tv   # unknown token -> can't judge -> allow (trust agent)

with open(CFG, encoding="utf-8") as f:
    data = json.load(f, object_pairs_hook=OrderedDict)
fams = data["families"]

rejected, dropped_class, dropped_missing, dropped_material = [], [], [], []
added, upgraded = [], []

for fp in sorted(glob.glob(INST + "/.uvrun/decay_cand/out_*.json")):
    try:
        blob = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        print("skip", fp, e); continue
    for fam in blob.get("families", []):
        base = fam.get("base", "")
        if base not in EXIST:                                         # base must be a real block
            rejected.append(("base-missing", base)); continue
        bshape = shp(base)
        # collect valid variants (real id + class-lock); base always anchors first
        keep = OrderedDict()
        for v in fam.get("variants", []):
            vid, w = v.get("id", ""), v.get("weight", 0)
            if vid not in EXIST:
                dropped_missing.append(vid); continue
            if shp(vid) != bshape:
                dropped_class.append(f"{vid} (in {base})"); continue
            if vid != base and not same_material(base, vid):
                dropped_material.append(f"{vid} (in {base})"); continue
            keep[vid] = int(round(w))
        # union with any existing family for this base (never lose a variant we already had)
        prev = {vid: w for vid, w in (fams.get(base) or [])}
        merged = OrderedDict()
        bw = keep.get(base, prev.get(base, 52))
        merged[base] = bw                                            # anchor first
        for vid, w in list(prev.items()) + list(keep.items()):
            if vid == base: continue
            if vid not in merged: merged[vid] = w
        # require >=1 real aged variant, else the family does nothing -> skip
        if not any(DECAY.search(vid) for vid in merged if vid != base):
            if base not in fams: rejected.append(("no-aged", base))
            continue
        out = [[vid, w] for vid, w in merged.items()]
        (upgraded if base in fams else added).append(base)
        fams[base] = out

# ---- compact serializer (families one-per-line; everything else json-indented) ----
def fam_line(k, v):
    if isinstance(v, str): return json.dumps(k) + ": " + json.dumps(v)
    inner = ", ".join("[" + json.dumps(p[0]) + ", " + str(p[1]) + "]" for p in v)
    return json.dumps(k) + ": [" + inner + "]"
items = list(data.items()); out = "{\n"
for i, (k, v) in enumerate(items):
    comma = "," if i < len(items) - 1 else ""
    if k == "families":
        out += '  "families": {\n'
        fitems = list(v.items())
        for j, (fk, fv) in enumerate(fitems):
            out += "    " + fam_line(fk, fv) + ("," if j < len(fitems) - 1 else "") + "\n"
        out += "  }" + comma + "\n"
    else:
        s = json.dumps({k: v}, indent=2, ensure_ascii=False)
        out += s[s.index("\n") + 1: s.rindex("\n")] + comma + "\n"
out += "}\n"
json.loads(out)
shutil.copy(CFG, CFG + ".presweep.bak")
open(CFG, "w", encoding="utf-8").write(out)

print(f"families now {len(fams)}  (added {len(set(added))}, upgraded {len(set(upgraded))})")
print(f"rejected bases: {len(rejected)} | class-lock drops: {len(dropped_class)} | "
      f"cross-material drops: {len(dropped_material)} | missing-id drops: {len(set(dropped_missing))}")
if rejected[:20]:          print("  rejected:", rejected[:20])
if dropped_class[:15]:     print("  class-lock drops:", dropped_class[:15])
if dropped_material[:20]:  print("  cross-material drops:", dropped_material[:20])
if set(dropped_missing):   print("  missing-id drops (sample):", sorted(set(dropped_missing))[:15])
