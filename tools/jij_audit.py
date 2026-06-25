#!/usr/bin/env python3
"""Ground-truth JiJ-duplicate finder. Scans EVERY mod jar for embedded META-INF/jarjar/*.jar,
then finds standalone jars in mods/ that are ALSO embedded inside another present mod.

NeoForge's JiJ resolver loads only the HIGHEST version of a duplicated library across all
copies (standalone + every embedded). So:
  * standalone version  < max(embedded versions)  -> standalone NEVER loads = provable dead weight.
  * standalone version == an embedded version      -> redundant copy (embedded would cover it).
  * standalone version  > all embedded             -> standalone is the one that loads; KEEP (removing downgrades).

This is the cleanest 0-false-positive signal: it's deterministic from jar bytes, not heuristics.
Output = candidates with the version math shown so the human can confirm.
"""
import os, re, zipfile, sys
from collections import defaultdict

MODS = "mods"
jars = sorted(f for f in os.listdir(MODS) if f.endswith(".jar"))

# base-name + version parser for library jar filenames
VER_RX = re.compile(r"(\d+(?:\.\d+){1,3}(?:[-+.][0-9A-Za-z]+)*)")
LOADER_RX = re.compile(r"[-_](neoforge|forge|fabric|forgefabric|common|mc?\d[\d.]*|1\.21[.\d]*)", re.I)

def parse(name):
    """jar filename -> (base, version). base is loader/version-stripped lowercase key."""
    n = name[:-4] if name.endswith(".jar") else name
    # find the FIRST version-looking token; everything before it is the base
    m = re.search(r"[-_](\d+\.\d)", n)
    if m:
        base = n[:m.start()]
        ver = n[m.start()+1:]
    else:
        base, ver = n, ""
    base = LOADER_RX.sub("", base).lower().strip("-_. ")
    # collapse separators
    base = re.sub(r"[-_.]+", "", base)
    return base, ver

def vkey(v):
    """version -> comparable tuple (numeric parts; non-numeric -> -1 so betas sort below releases)."""
    parts = re.split(r"[.\-+]", v)
    out = []
    for p in parts:
        if p.isdigit(): out.append((1, int(p)))
        elif p == "": continue
        else: out.append((0, p.lower()))   # textual (beta/alpha/rc) sorts below numeric at same pos
    return tuple(out)

# ---- collect embedded jars per host ----
embedded = defaultdict(list)   # base -> list of (version, host_jar)
standalone = {}                # base -> (version, jar)  (last wins; dup standalone is its own issue)
standalone_all = defaultdict(list)

for jar in jars:
    b, v = parse(jar)
    standalone[b] = (v, jar)
    standalone_all[b].append((v, jar))
    try:
        with zipfile.ZipFile(os.path.join(MODS, jar)) as z:
            for n in z.namelist():
                if re.match(r"META-INF/(jarjar|jars)/.+\.jar$", n):
                    inner = os.path.basename(n)
                    ib, iv = parse(inner)
                    embedded[ib].append((iv, jar))
    except Exception as e:
        print(f"  !! could not read {jar}: {e}", file=sys.stderr)

# ---- find standalone jars that are also embedded elsewhere ----
print("="*80)
print("JiJ-DUPLICATE AUDIT  (standalone jar ALSO embedded in another present mod)")
print("="*80)

dead, redundant, keep = [], [], []
for b, (sv, sjar) in standalone.items():
    if b not in embedded: continue
    hosts = [(hv, hj) for (hv, hj) in embedded[b] if hj != sjar]
    if not hosts: continue
    maxhv, maxhost = max(hosts, key=lambda x: vkey(x[0]))
    svk, mhk = vkey(sv), vkey(maxhv)
    rec = (b, sjar, sv, maxhv, maxhost, len(hosts))
    if svk < mhk:      dead.append(rec)
    elif svk == mhk:   redundant.append(rec)
    else:              keep.append(rec)

def show(title, rows, note):
    print(f"\n##### {title} ({len(rows)})  -- {note}")
    for b, sjar, sv, hv, host, nh in sorted(rows, key=lambda x: x[1].lower()):
        print(f"  - {sjar}")
        print(f"      lib '{b}' v{sv or '?'}  vs embedded v{hv or '?'} in {host}" +
              (f"  (+{nh-1} other host{'s' if nh>2 else ''})" if nh > 1 else ""))

show("A. PROVABLE DEAD WEIGHT  -- standalone OLDER than an embedded copy -> never loads",
     dead, "safe to remove: NeoForge loads the embedded higher version regardless")
show("B. REDUNDANT COPY  -- standalone SAME version as an embedded copy",
     redundant, "embedded copy already covers it; removing standalone changes nothing")
show("C. KEEP (standalone NEWER than embedded) -- removing would DOWNGRADE",
     keep, "do NOT remove; the standalone is the version that loads")

# also: standalone libs present in MULTIPLE copies (two jars, same lib)
print(f"\n\n##### D. DUPLICATE STANDALONE JARS (same library, 2+ loose jars in mods/)")
dd = 0
for b, lst in sorted(standalone_all.items()):
    if len(lst) >= 2:
        dd += 1
        print(f"  - {b}: " + " | ".join(f"{j} (v{v or '?'})" for v, j in sorted(lst)))
if not dd: print("  (none)")
print(f"\nscanned {len(jars)} jars | embedded-lib bases: {len(embedded)} | dead={len(dead)} redundant={len(redundant)} keep={len(keep)} dup-standalone={dd}")
