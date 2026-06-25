#!/usr/bin/env python3
"""Merge Stoneworks aged-stone variants into config/wnl_pathways/condition.json decay families.
Every stoneworks: id is validated against the jar's actual blockstate list (a typo -> abort, never a
silent fallback). CLASS-LOCKED: solid->solid, brick->brick, stair->stair, slab->slab, wall->wall.
The 'mossy_'/'cracked_'/'cobbled_' substrings already classify as AGED in condition.json's aging block,
so these rise with the condition dial automatically; 'polished_'/'cut_' are KEPT (fall with ruin)."""
import json, zipfile, shutil, sys

INST = r"C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version"
CFG  = INST + "/config/wnl_pathways/condition.json"
JAR  = INST + "/mods/Stoneworks-v21.1.0-1.21.1-NeoForge.jar"

# --- read the jar's real block set (namespace-qualified) ---
sw = set()
with zipfile.ZipFile(JAR) as z:
    for n in z.namelist():
        if n.startswith("assets/stoneworks/blockstates/") and n.endswith(".json"):
            sw.add("stoneworks:" + n.split("/")[-1][:-5])

def S(p): return "stoneworks:" + p
def M(p): return "minecraft:" + p

# base id -> [(variant_id, base_weight), ...]   (1st entry = base = anchor; aging dial re-weights the rest)
NEW = {
  # ---- vanilla solid stones that had NO decay path -> Stoneworks cobbled + mossy_cobbled ----
  M("andesite"):        [(M("andesite"),52),(M("polished_andesite"),12),(S("cobbled_andesite"),18),(S("mossy_cobbled_andesite"),18)],
  M("diorite"):         [(M("diorite"),54),(M("polished_diorite"),12),(S("cobbled_diorite"),17),(S("mossy_cobbled_diorite"),17)],
  M("granite"):         [(M("granite"),54),(M("polished_granite"),12),(S("cobbled_granite"),17),(S("mossy_cobbled_granite"),17)],
  M("blackstone"):      [(M("blackstone"),54),(S("cobbled_blackstone"),24),(S("mossy_cobbled_blackstone"),22)],
  M("tuff"):            [(M("tuff"),56),(S("cobbled_tuff"),22),(S("mossy_cobbled_tuff"),22)],
  M("calcite"):         [(M("calcite"),60),(S("cobbled_calcite"),20),(S("mossy_cobbled_calcite"),20)],
  M("sandstone"):       [(M("sandstone"),54),(M("cut_sandstone"),10),(S("cobbled_sandstone"),18),(S("mossy_cobbled_sandstone"),18)],
  M("red_sandstone"):   [(M("red_sandstone"),54),(M("cut_red_sandstone"),10),(S("cobbled_red_sandstone"),18),(S("mossy_cobbled_red_sandstone"),18)],
  M("prismarine"):      [(M("prismarine"),58),(S("cobbled_prismarine"),21),(S("mossy_cobbled_prismarine"),21)],
  M("dark_prismarine"): [(M("dark_prismarine"),60),(S("cobbled_dark_prismarine"),20),(S("mossy_cobbled_dark_prismarine"),20)],
  # ---- brick families -> Stoneworks cracked + mossy bricks ----
  M("prismarine_bricks"): [(M("prismarine_bricks"),58),(S("cracked_prismarine_bricks"),21),(S("mossy_prismarine_bricks"),21)],
  M("tuff_bricks"):       [(M("tuff_bricks"),56),(S("cracked_tuff_bricks"),22),(S("mossy_tuff_bricks"),22)],
  # ---- UPGRADE existing deepslate families: add mossy_cobbled / mossy bricks (vanilla has none) ----
  M("deepslate"):         [(M("deepslate"),46),(M("cobbled_deepslate"),28),(S("mossy_cobbled_deepslate"),26)],
  M("cobbled_deepslate"): [(M("cobbled_deepslate"),52),(M("deepslate"),22),(S("mossy_cobbled_deepslate"),26)],
  M("deepslate_bricks"):  [(M("deepslate_bricks"),50),(M("cracked_deepslate_bricks"),24),(M("deepslate_tiles"),14),(S("mossy_deepslate_bricks"),12)],
  # ---- pure-vanilla stair/slab/wall moss (high-frequency roof/parapet surfaces; no mod dep) ----
  M("stone_brick_stairs"):  [(M("stone_brick_stairs"),58),(M("mossy_stone_brick_stairs"),42)],
  M("stone_brick_slab"):    [(M("stone_brick_slab"),58),(M("mossy_stone_brick_slab"),42)],
  M("stone_brick_wall"):    [(M("stone_brick_wall"),58),(M("mossy_stone_brick_wall"),42)],
  M("cobblestone_stairs"):  [(M("cobblestone_stairs"),56),(M("mossy_cobblestone_stairs"),44)],
  M("cobblestone_slab"):    [(M("cobblestone_slab"),56),(M("mossy_cobblestone_slab"),44)],
  M("cobblestone_wall"):    [(M("cobblestone_wall"),56),(M("mossy_cobblestone_wall"),44)],
}

# --- validate every stoneworks id actually exists in the jar ---
bad = sorted({v for vs in NEW.values() for v,_ in vs if v.startswith("stoneworks:") and v not in sw})
if bad:
    print("ABORT — stoneworks ids not in jar:", bad); sys.exit(1)

# --- merge into families, preserving file structure ---
with open(CFG, encoding="utf-8") as f:
    data = json.load(f)
fams = data["families"]
added = [k for k in NEW if k not in fams]
upgraded = [k for k in NEW if k in fams]
for base, vs in NEW.items():
    fams[base] = [[v, w] for v, w in vs]

# --- compact serializer (families one-per-line; everything else via json indent) ---
def fam_line(k, v):
    if isinstance(v, str):
        return json.dumps(k) + ": " + json.dumps(v)
    inner = ", ".join("[" + json.dumps(p[0]) + ", " + str(p[1]) + "]" for p in v)
    return json.dumps(k) + ": [" + inner + "]"

items = list(data.items())
out = "{\n"
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

json.loads(out)  # parse-validate before writing
shutil.copy(CFG, CFG + ".prestoneworks.bak")
with open(CFG, "w", encoding="utf-8") as f:
    f.write(out)
print(f"OK. families now {len(fams)} (added {len(added)}, upgraded {len(upgraded)}).")
print("added:", ", ".join(sorted(added)))
print("upgraded:", ", ".join(sorted(upgraded)))
