#!/usr/bin/env python3
"""Collapse a boot log's ERROR/WARN/exception lines into DISTINCT signatures with counts + an example.
Goal: turn thousands of lines into the handful of real distinct issues to triage."""
import re, sys, collections

path = sys.argv[1] if len(sys.argv) > 1 else "logs/latest.log"
lines = open(path, encoding="utf-8", errors="replace").read().splitlines()

# strip the leading "[25Jun2026 06:08:33.603] [thread/LEVEL] [logger/]:" prefix -> level + logger + message
PREFIX = re.compile(r"^\[(?:\d+\w+\d+ )?\d\d:\d\d:\d\d(?:\.\d+)?\]\s*\[([^\]]*)\]\s*(?:\[([^\]]*)\])?\s*:?\s*(.*)$")
# benign: mixin probing for an optional integration target that isn't installed (fail-soft by design)
BENIGN_PROBE = re.compile(r"Error loading class:|was not found |is not available|Could not (find|load) (optional|soft)")
def norm(msg):
    s = msg
    s = re.sub(r"0x[0-9a-fA-F]+", "0xHEX", s)
    s = re.sub(r"-?\b\d+\b", "N", s)                 # numbers/coords
    s = re.sub(r"[0-9a-f]{8}-[0-9a-f-]{27}", "UUID", s)
    s = re.sub(r"[A-Za-z]:[\\/][^\s'\"]+", "PATH", s) # windows paths
    s = re.sub(r"\s+", " ", s).strip()
    return s[:200]

err = collections.Counter(); errex = {}
warn = collections.Counter(); warnex = {}
exc = collections.Counter(); excex = {}
benign = collections.Counter()

for ln in lines:
    m = PREFIX.match(ln)
    if m:
        thread_level, logger, msg = m.group(1), m.group(2) or "", m.group(3)
        level = thread_level.split("/")[-1] if "/" in thread_level else thread_level
        sig = f"[{logger}] {norm(msg)}"
        if BENIGN_PROBE.search(msg):
            benign[level] += 1
            continue
        if level == "ERROR":
            err[sig] += 1; errex.setdefault(sig, ln[:300])
        elif level == "WARN":
            warn[sig] += 1; warnex.setdefault(sig, ln[:300])
    # exception class lines (anywhere, incl. inside multi-line traces) -- skip benign probe lines
    if BENIGN_PROBE.search(ln): continue
    em = re.search(r"([a-z][\w.]+\.[A-Z]\w*(?:Exception|Error|Throwable))(?::\s*(.*))?", ln)
    if em and ("Exception" in em.group(1) or "Error" in em.group(1)):
        sig = em.group(1) + ((": " + norm(em.group(2))) if em.group(2) else "")
        exc[sig[:200]] += 1; excex.setdefault(sig[:200], ln.strip()[:300])

def dump(title, counter, ex, top):
    print(f"\n{'='*70}\n{title}  ({len(counter)} distinct, {sum(counter.values())} total)\n{'='*70}")
    for sig, n in counter.most_common(top):
        print(f"\n[x{n}] {sig}")
        print(f"      e.g. {ex[sig]}")

print(f"LOG: {path}  ({len(lines)} lines)")
print(f"BENIGN mixin/optional-target probes skipped: {dict(benign)} (total {sum(benign.values())})")
dump("REAL ERROR signatures", err, errex, 80)
dump("REAL EXCEPTION classes (non-probe)", exc, excex, 50)
dump("WARN signatures (top 40, non-probe)", warn, warnex, 40)
