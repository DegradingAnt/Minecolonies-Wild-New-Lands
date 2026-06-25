#!/usr/bin/env python3
"""Rebuild the wood decay families species-preservingly. The sweep's wood agent collapsed ~all woods to a
generic rotten_log (homogenizing + skipping the natural weathering step). Fix: log -> stripped_log (same
species, the real mid-decay) -> rotten (rare, deep-wild only). Also registers rotten/weathered/stripped in
condition.json's aged_patterns so they actually rise with the ruin dial. Logs are MEMBERS (one variant per
post via the member-anchor), so a coherent stripped/rotten post reads correctly."""
import json, re
from collections import OrderedDict

INST = r"C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version"
CFG  = INST + "/config/wnl_pathways/condition.json"
inv  = json.load(open(INST + "/.uvrun/block_inventory.json", encoding="utf-8"))
EXIST = {f"{ns}:{p}" for ns, ps in inv.items() for p in ps}

ROT_LOG  = [i for i in ["spawn:rotten_log", "betterarcheology:rotten_log"] if i in EXIST]
ROT_WOOD = [i for i in ["spawn:rotten_wood"] if i in EXIST]
WOOD_RE  = re.compile(r"(_log|_stem|_hyphae|_wood)$|^bamboo_block$|^stripped_bamboo_block$")
NETHER   = re.compile(r"(crimson|warped)")   # fungus stems: no wood-rot mapping (+ nether is dim-gated anyway)

def woodfam(base):
    ns, p = base.split(":", 1)
    if NETHER.search(p):
        return None                                   # leave crimson/warped uniform
    is_wood = p.endswith("_wood")
    rot = ROT_WOOD if is_wood else ROT_LOG
    if p.startswith("stripped_"):                     # already stripped -> can only rot further (deep wild)
        out = [(base, 70)] + list(zip(rot, [16, 12]))
    else:
        strp = f"{ns}:stripped_{p}"
        if strp in EXIST:                             # species-preserving mid-decay + rare rot
            out = [(base, 64), (strp, 24)] + list(zip(rot, [8, 6]))
        else:                                         # no stripped variant -> rot is the only aged path
            out = [(base, 70)] + list(zip(rot, [18, 12]))
    out = [(i, w) for i, w in out if i == base or i in EXIST]
    return out if len(out) >= 2 else None             # need >=1 real aged variant, else skip (clean wood is fine)

data = json.load(open(CFG, encoding="utf-8"), object_pairs_hook=OrderedDict)

# 1) register the wood-aging patterns so rotten/weathered/stripped scale with condition
aged = data["aging"]["aged_patterns"]
for pat in ["rotten", "rotted", "weathered", "stripped"]:
    if pat not in aged: aged.append(pat)

# 2) drop every existing wood-shaped family, then rebuild from the full inventory
fams = data["families"]
for k in [k for k in fams if ":" in k and WOOD_RE.search(k.split(":", 1)[1])]:
    del fams[k]
wood_bases = sorted(b for b in EXIST if WOOD_RE.search(b.split(":", 1)[1]))
built = 0
for b in wood_bases:
    fam = woodfam(b)
    if fam:
        fams[b] = [[i, w] for i, w in fam]
        built += 1

# 3) compact write (families one-per-line)
def fam_line(k, v):
    if isinstance(v, str): return json.dumps(k) + ": " + json.dumps(v)
    return json.dumps(k) + ": [" + ", ".join("[" + json.dumps(p[0]) + ", " + str(p[1]) + "]" for p in v) + "]"
items = list(data.items()); out = "{\n"
for i, (k, v) in enumerate(items):
    comma = "," if i < len(items) - 1 else ""
    if k == "families":
        out += '  "families": {\n'
        fi = list(v.items())
        for j, (fk, fv) in enumerate(fi):
            out += "    " + fam_line(fk, fv) + ("," if j < len(fi) - 1 else "") + "\n"
        out += "  }" + comma + "\n"
    else:
        s = json.dumps({k: v}, indent=2, ensure_ascii=False)
        out += s[s.index("\n") + 1: s.rindex("\n")] + comma + "\n"
out += "}\n"
json.loads(out)
open(CFG, "w", encoding="utf-8").write(out)
print(f"wood families rebuilt: {built} | rotten pool log={ROT_LOG} wood={ROT_WOOD}")
print(f"total families now: {len(fams)} | aged_patterns: {aged}")
print("sample:")
for b in ["minecraft:oak_log","minecraft:spruce_log","valhelsia_structures:bundled_stripped_oak_posts"]:
    if b in fams: print(f"  {b} -> {fams[b]}")
for b in list(wood_bases):
    if b in fams and 'pale_oak_log' in b:
        print(f"  {b} -> {fams[b]}"); break
