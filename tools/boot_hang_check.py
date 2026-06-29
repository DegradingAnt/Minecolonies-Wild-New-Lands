#!/usr/bin/env python3
"""Boot hang-check GUARD (memory: boot-test-discipline). A quiet log is NOT a hang on its own —
twice on 2026-06-29 a busy-but-quiet boot got mis-called a hang. This guard takes a thread dump and
refuses the "HUNG" verdict unless the work threads are genuinely PARKED (waiting), not RUNNABLE/busy.

Usage:  boot_hang_check.py <pid> [jcmd_path]
Prints one of: BUSY (working — NOT a hang) | HUNG (genuinely parked) | DEAD (no such pid)
plus the deciding Server/main thread frame. A boot waiter must require HUNG (not just a frozen log)
before declaring a hang."""
import sys, subprocess, re

JCMD_DEFAULT = r"C:/Program Files/Eclipse Adoptium/jdk-25.0.3.9-hotspot/bin/jcmd.exe"

def main():
    if len(sys.argv) < 2:
        print("usage: boot_hang_check.py <pid> [jcmd]"); return 2
    pid = sys.argv[1]
    jcmd = sys.argv[2] if len(sys.argv) > 2 else JCMD_DEFAULT
    try:
        out = subprocess.run([jcmd, pid, "Thread.print"], capture_output=True, text=True, timeout=30).stdout
    except Exception as e:
        print(f"DEAD (jcmd failed: {e})"); return 1
    if not out or "Thread.print" not in out and '"' not in out:
        print("DEAD (no dump)"); return 1

    # Pull the state + first app frame of the most gen-relevant threads.
    blocks = re.split(r'\n(?=")', out)
    verdict_threads = {}
    for b in blocks:
        m = re.match(r'"([^"]+)"', b)
        if not m: continue
        name = m.group(1)
        if name not in ("Server thread", "main", "Render thread"):
            continue
        st = re.search(r'java\.lang\.Thread\.State:\s*(\S+)', b)
        state = st.group(1) if st else "?"
        frame = ""
        for line in b.splitlines():
            line = line.strip()
            if line.startswith("at ") and not re.search(r'\bat (java|jdk|sun)\.', line):
                frame = line[3:]; break
        verdict_threads[name] = (state, frame)

    server = verdict_threads.get("Server thread") or verdict_threads.get("main")
    if not server:
        print("BUSY (no Server/main thread parked — likely still working)"); return 0
    state, frame = server
    # RUNNABLE = on-CPU = working (this is the exact mis-call to prevent).
    if state == "RUNNABLE":
        print(f"BUSY (Server/main is RUNNABLE = working, NOT hung) :: {frame}"); return 0
    # PARKED/WAITING on the chunk-load path = genuine hang candidate.
    parked_for_chunk = any(k in frame for k in ("managedBlock", "getOverworldRespawnPos", "waitForTasks", "getChunk")) \
                       or "managedBlock" in server[1]
    if state in ("WAITING", "TIMED_WAITING") and parked_for_chunk:
        print(f"HUNG (Server/main PARKED on chunk-load: {state}) :: {frame}"); return 0
    print(f"BUSY (Server/main {state}, not parked on chunk-load) :: {frame}"); return 0

if __name__ == "__main__":
    sys.exit(main())
