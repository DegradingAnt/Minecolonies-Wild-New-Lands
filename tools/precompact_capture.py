#!/usr/bin/env python
"""PreCompact hook — mechanical savestate safety net.

Fires automatically when Claude Code is about to compact (manual or auto). Appends a timestamped
snapshot of the pack's mechanical state to _dev/SAVESTATE-auto.md so context is NEVER fully lost,
even if the rich `wnl-savestate` skill wasn't run. Also runs a "verification gate" (per the
context-amnesia 4-step protocol): if the rich SAVESTATE.md is older than recent file changes, it
warns that the narrative savestate is stale. Must NEVER throw — a failing hook must not block compaction.
"""
import sys, os, json, glob

ROOT = r"C:\Users\linde\curseforge\minecraft\Instances\Ultimate vibes distant horizons version"
AUTO = os.path.join(ROOT, "_dev", "SAVESTATE-auto.md")
RICH = os.path.join(ROOT, "_dev", "wnl-pathways-src", "SAVESTATE.md")
TRAIL = os.path.join(ROOT, "_dev", ".change-trail.log")
CL = os.path.join(ROOT, "_dev", "CHANGELOG.md")

def safe(fn, default=""):
    try: return fn()
    except Exception as e: return f"{default}(err:{e})"

def main():
    import datetime
    trigger = "?"
    try: trigger = (json.load(sys.stdin) or {}).get("trigger", "?")
    except Exception: pass
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    L = ["", f"## auto-capture {ts} (PreCompact, trigger={trigger})"]

    wnl = safe(lambda: sorted(os.path.basename(j) for j in
               glob.glob(os.path.join(ROOT, "mods", "WNL-*.jar")) +
               glob.glob(os.path.join(ROOT, "mods", "wnl_*.jar"))), [])
    L.append("- WNL jars: " + (", ".join(wnl) if isinstance(wnl, list) else str(wnl)))

    crashes = safe(lambda: sorted(glob.glob(os.path.join(ROOT, "crash-reports", "*.txt")),
                   key=os.path.getmtime, reverse=True), [])
    L.append("- latest crash: " + (os.path.basename(crashes[0]) if crashes else "none"))

    if os.path.exists(TRAIL):
        tail = safe(lambda: open(TRAIL, encoding="utf-8", errors="replace").read().splitlines()[-8:], [])
        if isinstance(tail, list):
            L.append("- recent file touches:")
            L += ["  " + t for t in tail]

    if os.path.exists(CL):
        top = safe(lambda: [l for l in open(CL, encoding="utf-8", errors="replace").read().splitlines()
                            if l.startswith("## ")][:3], [])
        if isinstance(top, list):
            L.append("- CHANGELOG top: " + " | ".join(top))

    warn = ""
    if os.path.exists(RICH) and os.path.exists(TRAIL):
        try:
            if os.path.getmtime(TRAIL) > os.path.getmtime(RICH) + 300:
                warn = "rich SAVESTATE.md is OLDER than recent changes — run /wnl-savestate; it may be stale."
                L.append("- WARNING: " + warn)
        except Exception:
            pass

    try:
        with open(AUTO, "a", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
    except Exception:
        pass

    msg = "[precompact] mechanical state captured to _dev/SAVESTATE-auto.md."
    if warn: msg += " WARNING: " + warn
    try: print(json.dumps({"systemMessage": msg}))
    except Exception: pass

try:
    main()
except Exception:
    pass  # never block compaction
sys.exit(0)
