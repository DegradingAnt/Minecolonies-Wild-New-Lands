#!/usr/bin/env python3
"""Scout: every block in every mod jar, bucketed for decay-palette planning.
Reads zip central directories only (fast). Emits:
  - .uvrun/block_inventory.json   (full: {namespace: [paths...]})
  - console summary: counts, top mods, decay-SOURCE mods (have aged variants), base-material coverage."""
import zipfile, glob, json, os, re
from collections import defaultdict

INST = r"C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version"
MODS = INST + "/mods"

# aged / weathered / damaged variant markers -> these are DECAY TARGET candidates
AGED = re.compile(r"(mossy|cracked|cobbled|chipped|weather|broken|ruin|worn|erod|damaged|aged|crumbl|decay|rough|rotten|rotted|dilapidat|tatter|overgrown|vine|rubble)")
# base building-material markers -> these are BASE blocks structures are built from
MATERIAL = re.compile(r"(stone|brick|tile|cobble|deepslate|sandstone|granite|diorite|andesite|tuff|calcite|basalt|blackstone|prismarine|netherrack|quartz|terracotta|concrete|planks|_log$|_wood$|stripped|marble|limestone|slate|clay|mud|plaster)")
SHAPE = re.compile(r"(_slab|_stairs|_wall|_fence|_button|_pressure_plate|_door|_trapdoor|_sign|_gate)$")

inv = defaultdict(list)
for jar in glob.glob(MODS + "/*.jar"):
    try:
        with zipfile.ZipFile(jar) as z:
            for n in z.namelist():
                m = re.match(r"assets/([a-z0-9_.-]+)/blockstates/([a-z0-9_/]+)\.json$", n)
                if m:
                    inv[m.group(1)].append(m.group(2))
    except Exception as e:
        print("skip", os.path.basename(jar), e)

# drop minecraft (vanilla handled separately) for the "mod" stats but keep in json
mod_ns = {ns: ps for ns, ps in inv.items() if ns != "minecraft"}
total = sum(len(p) for p in inv.values())
print(f"=== {len(inv)} namespaces, {total} blockstate files total ({len(mod_ns)} modded ns) ===\n")

# decay-source mods: have aged-variant blocks that are ALSO building materials
src = {}
for ns, ps in inv.items():
    aged_mats = [p for p in ps if AGED.search(p) and MATERIAL.search(p)]
    if aged_mats:
        src[ns] = len(aged_mats)
print("=== TOP DECAY-SOURCE namespaces (aged building-material variants) ===")
for ns, c in sorted(src.items(), key=lambda kv: -kv[1])[:40]:
    print(f"  {ns:32} {c:5}  (of {len(inv[ns])} blocks)")

print(f"\n=== TOP namespaces by total block count ===")
for ns, ps in sorted(mod_ns.items(), key=lambda kv: -len(kv[1]))[:25]:
    print(f"  {ns:32} {len(ps):5}")

# write full inventory
with open(INST + "/.uvrun/block_inventory.json", "w", encoding="utf-8") as f:
    json.dump({ns: sorted(ps) for ns, ps in inv.items()}, f, indent=0)
print(f"\nwrote .uvrun/block_inventory.json ({total} blocks)")
print(f"decay-source mods: {len(src)} | aged-material blocks total: {sum(src.values())}")
