#!/usr/bin/env python3
"""Un-suppressed log audit.
Reads logs/latest.log (booted with logbegone blanked) + the suppression catalog
from config/logbegone.json.uvbak, and splits problem lines into:
  NEW       - ERROR/WARN/FATAL/Exception lines NOT matched by any catalog phrase/regex
  CATALOG   - per-phrase hit counts (active vs stale=0) so we can re-vet/trim the catalog
Usage: python .uvrun/log_audit.py [logfile]
"""
import json, re, sys, collections

ROOT = r"C:\Users\linde\curseforge\minecraft\Instances\Ultimate vibes distant horizons version"
LOG = sys.argv[1] if len(sys.argv) > 1 else ROOT + r"\logs\latest.log"
CAT = ROOT + r"\config\logbegone.json.uvbak"

cat = json.load(open(CAT, encoding="utf-8"))["logbegone"]
phrases = cat.get("phrases", [])
regexes = [re.compile(r) for r in cat.get("regex", [])]

SEV = re.compile(r"\]\s*\[[^\]]*/(ERROR|WARN|FATAL)\]")
EXC = re.compile(r"(Exception|Caused by:|java\.lang\.|NullPointer|ClassCast|NoSuchMethod|NoClassDefFound|Error parsing|Couldn't parse|Failed to)")

def is_problem(line):
    if SEV.search(line):
        return True
    if EXC.search(line) and "\tat " not in line:
        return True
    return False

def matches_catalog(line):
    for p in phrases:
        if p in line:
            return p
    for rx in regexes:
        if rx.search(line):
            return rx.pattern
    return None

def signature(line):
    # message after the last "]: "
    m = re.split(r"\]:\s*", line, maxsplit=1)
    msg = m[1] if len(m) > 1 else line
    msg = msg.strip()
    # strip volatile bits
    msg = re.sub(r"\d+", "#", msg)
    msg = re.sub(r"0x[0-9a-fA-F#]+", "0x#", msg)
    msg = re.sub(r"[A-Za-z]:\\[^\s,'\"]+", "<path>", msg)
    return msg[:160]

new_sigs = collections.Counter()
new_samples = {}
cat_hits = collections.Counter()
total_problem = 0

for raw in open(LOG, encoding="utf-8", errors="replace"):
    line = raw.rstrip("\n")
    if not is_problem(line):
        continue
    total_problem += 1
    hit = matches_catalog(line)
    if hit is not None:
        cat_hits[hit] += 1
    else:
        sig = signature(line)
        new_sigs[sig] += 1
        if sig not in new_samples:
            new_samples[sig] = line[:300]

print(f"=== UN-SUPPRESSED LOG AUDIT — {LOG}")
print(f"problem lines (ERROR/WARN/FATAL/Exception): {total_problem}")
print(f"  matched catalog (vetted-noise): {sum(cat_hits.values())}")
print(f"  NEW / uncatalogued:             {sum(new_sigs.values())}  ({len(new_sigs)} distinct)\n")

print("================ NEW / UNCATALOGUED (investigate) ================")
for sig, n in new_sigs.most_common(60):
    print(f"[{n:>4}]  {new_samples[sig]}")

print("\n================ CATALOG ACTIVITY (re-vet / trim) ================")
print("-- ACTIVE phrases (still firing — re-confirm benign): --")
for p, n in cat_hits.most_common():
    print(f"[{n:>4}]  {p!r}")
stale = [p for p in phrases if cat_hits.get(p, 0) == 0]
print(f"\n-- STALE phrases (0 hits this boot — candidates to trim): {len(stale)}/{len(phrases)} --")
for p in stale:
    print(f"        {p!r}")
