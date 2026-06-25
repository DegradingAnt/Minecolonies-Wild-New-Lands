#!/usr/bin/env python3
"""PostToolUse hook (Write|Edit): append every WNL-relevant file touch to _dev/.change-trail.log.

Backstop trail for the `wnl-changelog` skill — guarantees that even an un-logged change leaves a
footprint, so "I don't know what changed" can't happen again. Records WHAT + WHEN; the human-written
CHANGELOG.md still carries the WHY. Never raises; exits 0 always so it can't disrupt the tool flow.
"""
import sys, json, datetime

TRAIL = (r"C:\Users\linde\curseforge\minecraft\Instances"
         r"\Ultimate vibes distant horizons version\_dev\.change-trail.log")
# only record files under the pack / the WNL dev repos / the AR fork
MARKERS = ("Ultimate vibes distant horizons version",
           "curseforge\\WNL-", "curseforge/WNL-", "AR-fork")

try:
    data = json.load(sys.stdin)
    ti = data.get("tool_input") or {}
    tr = data.get("tool_response") or {}
    path = (ti.get("file_path") or ti.get("notebook_path")
            or (tr.get("filePath") if isinstance(tr, dict) else None))
    if path and any(m in path for m in MARKERS) and ".change-trail.log" not in path:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(TRAIL, "a", encoding="utf-8") as fh:
            fh.write(f"{ts}\t{data.get('tool_name', '?')}\t{path}\n")
except Exception:
    pass
sys.exit(0)
