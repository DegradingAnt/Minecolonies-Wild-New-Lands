#!/usr/bin/env python3
"""Deterministic dependency-graph audit for Ultimate Vibes -> unnecessary-mod candidates.
Goal: 0 false positives. We emit CANDIDATES with full evidence; the human confirms each.

Three analyses:
  A. ORPHAN LIBRARIES  -- library-class mods that NOTHING depends on (required|optional)
                          AND are not embedded(JiJ) anywhere. Dead weight IF truly a lib.
  B. JiJ DUPLICATES    -- a standalone modId that is ALSO JiJ'd inside another present mod
                          (the embedded copy would load it anyway -> standalone may be redundant).
  C. CONTENT LEAVES    -- (informational) content mods with 0 dependents are NORMAL; we count
                          them so we don't mistake 'no dependents' for 'unnecessary'.

False-positive guards baked in:
  * optional deps COUNT as a dependent (mod uses it if present).
  * runtime-service libs (rendering/mixin/asm/config frameworks) are NEVER flagged as orphan
    even with 0 declared dependents -- they're loaded reflectively. Hard allowlist below.
  * we report evidence, never auto-remove.
"""
import json, ast, re, sys

d = json.load(open(r".uvrun/modmeta.json"))
entries = d if isinstance(d, list) else d.get("mods", list(d.values()))

def aslist(v):
    if isinstance(v, list): return v
    if isinstance(v, str):
        try: return ast.literal_eval(v)
        except Exception: return []
    return v or []

# ---- build per-modId record + the graph ----
byid = {}            # modId -> record
file_of = {}         # modId -> jar file
jij_provides = {}    # file -> set(embedded modIds)  (from each jar's jij list)
embedded_ids = {}    # embedded modId -> set(host files)  (reverse JiJ)

for e in entries:
    f = e.get("file", "?")
    mlist = aslist(e.get("mods"))
    jij = aslist(e.get("jij"))
    # jij entries may be dicts {modId/file} or bare strings
    emb = set()
    for j in jij:
        if isinstance(j, dict):
            mid = j.get("modId") or j.get("id") or j.get("file")
        else:
            mid = j
        if mid: emb.add(str(mid).lower())
    jij_provides[f] = emb
    for mid in emb:
        embedded_ids.setdefault(mid, set()).add(f)
    for m in mlist:
        mid = (m.get("modId") or "?").lower()
        byid[mid] = {
            "id": mid, "name": m.get("name") or mid, "desc": (m.get("desc") or "").replace("\n", " "),
            "file": f, "classes": int(e.get("classes", 0) or 0), "recipes": int(e.get("recipes", 0) or 0),
            "models": int(e.get("models", 0) or 0), "size": float(e.get("sizeMB", 0) or 0),
        }
        file_of[mid] = f

# ---- dependency edges: dependents[X] = who declares a dep ON X ----
dependents = {mid: [] for mid in byid}
PLATFORM = {"neoforge", "forge", "fabric", "minecraft", "java", "fabricloader", "*"}
for e in entries:
    for dep in aslist(e.get("deps")):
        frm = (dep.get("from") or "").lower()
        on  = (dep.get("on")  or "").lower()
        typ = (dep.get("type") or "").lower()
        if on in PLATFORM or not on: continue
        if typ in ("incompatible", "discouraged"): continue   # not a 'needs it' edge
        dependents.setdefault(on, []).append((frm, typ))

# ---- library / runtime-service classification ----
LIB_RX = re.compile(r"\b(librar|api|\blib\b|framework|\bcore\b|codec|registr|\bsdk\b|"
                    r"datagen|mixin|coremod|asm|bytecode|reflection|annotation|"
                    r"util(it|s)|helper|common\b|backend|runtime|loader|provider|"
                    r"compat layer|integration api|modding kit|\btoolkit\b)", re.I)
# runtime/service-loaded libs that legitimately have 0 declared dependents -> NEVER orphan-flag
SERVICE_ALLOW = re.compile(r"mixin|mixinextras|asm|kotlin|kotlinforforge|architectury|"
                           r"cloth.?config|yacl|forgeconfig|night.?config|"
                           r"fabric.?api|connector|sinytra|embeddium|sodium|iris|oculus|"
                           r"flywheel|ferritecore|modernfix|memoryleakfix|spark|"
                           r"mixinsquared|manifold|geckolib|azurelib|playeranim|"
                           r"resourcefullib|resourceful.?config|prism|terrablender|"
                           r"jade|jei|emi|rei|patchouli|moonlight|supplementaries.?core|"
                           r"balm|bookshelf|puzzleslib|framework|forgified|collective|"
                           r"caelus|curios|trinkets|accessories|cardinal|continuity|"
                           r"athena|fusion|veil|sodiumextra|reeses|entityculling|"
                           r"creativecore|team.?reborn|cofh.?core|placebo|spectrelib|"
                           r"obscure_api|blueprint|prickle|kremlin|searchables|"
                           r"konkrete|fabric.?language.?kotlin|catalogue|configured", re.I)

def is_library(r):
    # KEYWORD-ONLY (no structural fallback): structure/worldgen/entity mods have 0 recipes+models
    # but are CONTENT, not libraries. Only flag mods whose own name/desc/id calls them a library.
    blob = f"{r['id']} {r['name']} {r['desc']}"
    return bool(LIB_RX.search(blob))

def is_service(r):
    return bool(SERVICE_ALLOW.search(f"{r['id']} {r['name']} {r['file']}"))

# ---- ground-truth embedded-lib bases (so we don't flag a lib that's also JiJ'd = used by host) ----
import os, zipfile
def basekey(name):
    n = name[:-4] if name.endswith(".jar") else name
    m = re.search(r"[-_](\d+\.\d)", n)
    n = n[:m.start()] if m else n
    n = re.sub(r"[-_](neoforge|forge|fabric|common|mc?\d[\d.]*)", "", n, flags=re.I)
    return re.sub(r"[-_.]+", "", n).lower()
EMB_BASES = set()
for f in os.listdir("mods"):
    if not f.endswith(".jar"): continue
    try:
        with zipfile.ZipFile(os.path.join("mods", f)) as z:
            for n in z.namelist():
                if re.match(r"META-INF/(jarjar|jars)/.+\.jar$", n):
                    EMB_BASES.add(basekey(os.path.basename(n)))
    except Exception: pass

# ---- A. ORPHAN LIBRARIES ----
orphans = []
for mid, r in byid.items():
    deps_on = dependents.get(mid, [])
    if deps_on: continue                 # something needs it (required OR optional)
    if not is_library(r): continue       # content leaf w/ 0 dependents = normal, skip
    if is_service(r): continue           # runtime/service lib -> not an orphan even at 0 deps
    fbase = basekey(r["file"])           # is this lib ALSO embedded somewhere (= used by a host)?
    if fbase in EMB_BASES or basekey(mid) in EMB_BASES: continue
    orphans.append((mid, r, set()))

# ---- B. JiJ DUPLICATES (standalone present AND embedded elsewhere) ----
dupes = []
for mid, hosts in embedded_ids.items():
    if mid in byid:                      # standalone jar exists for an embedded modId
        # exclude self-host
        ext = {h for h in hosts if h != byid[mid]["file"]}
        if ext:
            dupes.append((mid, byid[mid], ext, dependents.get(mid, [])))

# ---- output ----
print("="*78)
print(f"DEPENDENCY-GRAPH AUDIT  | {len(byid)} mod ids | game-closed deterministic scan")
print("="*78)

print(f"\n##### A. ORPHAN-LIBRARY CANDIDATES ({len(orphans)})  -- lib-class, 0 dependents, not JiJ host, not a service-lib")
print("    (each still needs a manual runtime-use check before flagging -- 0-FP rule)\n")
for mid, r, _ in sorted(orphans, key=lambda x: -x[1]["size"]):
    print(f"  - {r['name'][:30]:30s} [{mid[:26]:26s}] cls={r['classes']:<4} rec={r['recipes']:<3} mdl={r['models']:<4} {r['size']}MB")
    print(f"      {r['desc'][:108]}")
    print(f"      file: {r['file']}")

print(f"\n\n##### B. JiJ-DUPLICATE CANDIDATES ({len(dupes)})  -- standalone jar AND embedded in another present mod")
print("    (standalone may be redundant; CHECK versions -- removing a NEWER standalone downgrades)\n")
for mid, r, hosts, deps_on in sorted(dupes, key=lambda x: x[0]):
    dn = f"{len(deps_on)} dependents" if deps_on else "0 dependents"
    print(f"  - {mid[:28]:28s} standalone={r['file'][:40]}")
    print(f"      embedded in: {', '.join(sorted(h[:38] for h in hosts))[:120]}  | {dn}")

# ---- counts for sanity ----
libs = [m for m in byid.values() if is_library(m)]
content_leaves = [mid for mid,r in byid.items() if not dependents.get(mid) and not is_library(r)]
print(f"\n\n##### SANITY COUNTS")
print(f"  total mod ids:           {len(byid)}")
print(f"  classified as library:   {len(libs)}")
print(f"  content leaves (0 deps, NOT flagged -- normal player content): {len(content_leaves)}")
print(f"  orphan-lib candidates:   {len(orphans)}")
print(f"  jij-duplicate candidates:{len(dupes)}")
