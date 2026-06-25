#!/usr/bin/env python3
"""Bucket every building block (from block_inventory.json) into MATERIAL categories, each tagged with
structural shape + decay-class, so a per-material agent can build class-locked decay families.
Writes .uvrun/decay_cand/<category>.json (one per material) + prints counts."""
import json, re, os
from collections import defaultdict

INST = r"C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version"
inv = json.load(open(INST + "/.uvrun/block_inventory.json", encoding="utf-8"))
OUT = INST + "/.uvrun/decay_cand"
os.makedirs(OUT, exist_ok=True)

# exclude obvious non-building noise even if it matched a material word
EXCLUDE = re.compile(r"(_ore$|^raw_|^deepslate_[a-z]+_ore|infested|_button$|_pressure_plate$|_door$|_trapdoor$|"
                     r"_sign$|_hanging_sign$|_fence_gate$|sapling|leaves|_log_|potted|_carpet$|banner|"
                     r"shulker|_bed$|chest|barrel|furnace|spawner|_head$|_skull$|candle|torch|lantern|"
                     r"_ladder$|rail$|piston|command|_glass|_pane$|button|_bulb$|lamp$|sponge|coral|"
                     r"machine|gear|cog|pipe|tank|pump|drill|cable|wire|conduit|portal|beacon|froglight)")

# material categories — FIRST match wins, so order specific stones BEFORE generic 'stone'
CATS = [
  ("deepslate",        re.compile(r"deepslate")),
  ("tuff_calcite",     re.compile(r"(tuff|calcite)")),
  ("sandstone",        re.compile(r"sandstone")),
  ("blackstone_basalt",re.compile(r"(blackstone|basalt)")),
  ("prismarine",       re.compile(r"prismarine")),
  ("nether",           re.compile(r"(netherrack|nether_brick|crimson|warped|magma|nylium|soul)")),
  ("quartz_end_purpur",re.compile(r"(quartz|purpur|end_stone|endstone|end_brick)")),
  ("igneous",          re.compile(r"(andesite|diorite|granite)")),
  ("marble_limestone", re.compile(r"(marble|limestone|slate(?!_)|travertine|jasper|gabbro|scoria|dripstone|veridium|asurine|crimsite|ochrum|tuffstone)")),
  ("mud_terracotta",   re.compile(r"(mud|terracotta|packed_mud|adobe|cob$|clay)")),
  ("wood_log",         re.compile(r"(_log$|_wood$|_stem$|_hyphae$|stripped_|_pillar$|bamboo_block)")),
  ("wood_planks",      re.compile(r"(planks|_plank|mosaic|_beam|_board|thatch|_shingle|_lattice)")),
  ("stone_core",       re.compile(r"(cobblestone|stone_brick|stone_tile|smooth_stone|^minecraft:stone$|_stone$|^stone|chiseled_stone|stonebrick|rubble|fieldstone|flagstone|brick)")),
]
DECAY = re.compile(r"(mossy|moss_|cracked|cobbled|chipped|weather|broken|ruin|worn|erod|crumbl|decay|rotten|rotted|dilapidat|tatter|overgrown|rough|chiseled_crack)")
KEPT  = re.compile(r"(polished|chiseled|smooth|cut_|_tiles?$|ornate|engraved|carved|gilded|encased|framed)")
def shape(p):
    for s in ("_stairs","_slab","_wall","_fence"):
        if p.endswith(s): return s[1:]
    return "full"
def klass(p):
    if DECAY.search(p): return "aged"
    if KEPT.search(p):  return "kept"
    return "base"

buckets = defaultdict(list)
for ns, paths in inv.items():
    for p in paths:
        fid = f"{ns}:{p}"
        if EXCLUDE.search(p) or EXCLUDE.search(fid): continue
        full = fid  # category match on the full id (so 'minecraft:stone' etc. resolve)
        for name, rx in CATS:
            if rx.search(p):
                buckets[name].append({"id": fid, "shape": shape(p), "class": klass(p)})
                break

print("=== material buckets (blocks | aged variants available) ===")
for name, _ in CATS:
    rows = buckets.get(name, [])
    aged = sum(1 for r in rows if r["class"] == "aged")
    with open(f"{OUT}/{name}.json", "w", encoding="utf-8") as f:
        json.dump({"material": name, "count": len(rows), "blocks": rows}, f, indent=0)
    print(f"  {name:20} {len(rows):5} blocks | {aged:4} aged | {len({r['id'].split(':')[0] for r in rows})} mods")
print(f"\nwrote {len(CATS)} category files to .uvrun/decay_cand/")
