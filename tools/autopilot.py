#!/usr/bin/env python
"""WNL autopilot — the never-stop / auto-resume engine.

Fixes two distinct failures that both made the grind halt:
  1. "you needed a prompt to start again" — after a /compact (manual OR auto) the
     session waited for a human message. Now a SessionStart hook injects an
     `initialUserMessage` that AUTO-STARTS the next turn (no human prompt).
  2. "you stop working after ~an hour" — when Claude finished a turn it idle-stopped.
     Now a Stop hook BLOCKS the stop and pushes Claude to the next build-queue item.

Both behaviors are gated on the autopilot SENTINEL file (.uvrun/.autopilot) so the
author has a hard on/off switch, and a per-context-window continue counter (CAP) is a
runaway backstop. A real human message resets the counter (fresh continue budget).

Two roles, one file (disambiguated by argv[1]):
  * HOOK MODE  (argv[1]=="hook", reads hook JSON on stdin): dispatch on hook_event_name.
  * CLI  MODE  (argv[1] in on|off|status|handback): engage / disengage / inspect / seed.
Must NEVER throw in hook mode — a failing hook must not break the session.
"""
import sys, os, json, glob

ROOT = r"C:\Users\linde\curseforge\minecraft\Instances\Ultimate vibes distant horizons version"
UVRUN = os.path.join(ROOT, ".uvrun")
SENTINEL = os.path.join(UVRUN, ".autopilot")        # present == autopilot engaged
CTR = os.path.join(UVRUN, ".autopilot_turns")       # consecutive auto-continues this window
CAP = 1000                                          # backstop: allow a natural stop after this many

def anchor_ptr():
    """Newest _dev/RESTART-*.md = the read-first resume anchor."""
    try:
        cands = glob.glob(os.path.join(ROOT, "_dev", "RESTART-*.md"))
        if cands:
            return "_dev/" + os.path.basename(max(cands, key=os.path.getmtime))
    except Exception:
        pass
    return "_dev/RESTART-2026-07-01-QUESTIONNAIRE-COMPLETE.md"

def read_ctr():
    try:
        return int(open(CTR).read().strip() or "0")
    except Exception:
        return 0

def write_ctr(n):
    try:
        open(CTR, "w").write(str(n))
        return True
    except Exception:
        return False

# ----------------------------------------------------------------------------- hooks
def hook_mode():
    data = {}
    try:
        data = json.load(sys.stdin) or {}
    except Exception:
        pass
    ev = data.get("hook_event_name") or data.get("hookEventName") or "?"
    engaged = os.path.exists(SENTINEL)

    # A real human turn -> fresh continue budget (so the author is never rate-limited
    # out of their own conversation by a stale counter). ALSO: a bare stop-word typed from
    # ANY remote (phone / native remote control) is a HARD KILL — disengage autopilot right
    # here in the hook, so it never relies on the model noticing. Exact-match only, so
    # "stop the render bug" (a work request) does NOT trip it.
    if ev == "UserPromptSubmit":
        write_ctr(0)
        p = (data.get("prompt") or "").strip().lower().rstrip(".!")
        STOPWORDS = {"stop", "pause", "halt", "kill", "disengage", "stop autopilot",
                     "pause autopilot", "autopilot off", "stop grinding", "stop grind", "stand down"}
        if p in STOPWORDS and engaged:
            try:
                if os.path.exists(SENTINEL):
                    os.remove(SENTINEL)   # hard kill from any remote (phone / native remote)
            except Exception:
                pass
            return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                    "additionalContext": "[autopilot] DISENGAGED by a remote stop command. Do NOT continue the "
                    "grind — acknowledge that autopilot is now off and wait for the author."}}
        return {}

    # After a compaction/resume/startup, AUTO-START the next turn (the core fix).
    if ev == "SessionStart":
        ptr = anchor_ptr()
        out = {"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "★ RESUME: read `" + ptr + "` FIRST, then "
                                 "`git -C C:/Users/linde/curseforge/WNL-Dev log -1` for the last banked increment."}}
        if engaged and data.get("source") in ("compact", "resume", "startup"):
            write_ctr(0)
            out["hookSpecificOutput"]["initialUserMessage"] = (
                "[autopilot auto-resume — source=" + str(data.get("source")) + "] "
                "Continue the autonomous main-dev grind with NO further human prompt. "
                "1) Read `" + ptr + "` (POST-RESUME TASK LIST + §4 queue). "
                "2) Confirm you resumed cleanly in ONE line. "
                "3) Pick the next queue item and BUILD it (wnl-autopilot loop). "
                "Keep going until the backlog is empty or the author stops you — the author is away, "
                "so do not wait for input on anything you own.")
        return out

    # Don't idle-stop while engaged: block the stop and push to the next item.
    if ev in ("Stop", "SubagentStop"):
        if not engaged:
            return {}                                   # off -> normal stop
        n = read_ctr()
        if n >= CAP:                                    # backstop -> natural check-in
            write_ctr(0)
            return {"systemMessage": "[autopilot] natural check-in after %d continuous turns — "
                    "say 'continue' to resume, or `python .uvrun/autopilot.py off` to disengage." % CAP}
        if not write_ctr(n + 1):                        # counter unwritable -> fail SAFE (allow stop)
            return {"systemMessage": "[autopilot] continue-counter unwritable; allowing a stop (fail-safe)."}
        return {"decision": "block", "reason": (
            "[autopilot] Do NOT stop — you are main dev on an autonomous grind. Pick the next build-queue item "
            "(`" + anchor_ptr() + "` §4 / CIV-ENGINE-VISION.md §6 / the open task list) and BUILD it now: "
            "build atomically → verify (compile / offline-test / audit) → bank (`bash .uvrun/bank_fast.sh \"...\"`, async) "
            "→ refresh the RESTART savestate → report a tight chunk → immediately continue. "
            "Only stop if the backlog is genuinely empty or a task truly needs the author (queue it, jump to other work). "
            "Hold the hard rules: perf-check-before-ship, graphics-floor-no-lower, the prelaunch gate.")}
    return {}

# ------------------------------------------------------------------------------- cli
def cli_mode(cmd):
    if cmd == "on":
        try:
            open(SENTINEL, "w").write("engaged\n")
        except Exception as e:
            print("failed to engage:", e); return
        write_ctr(0)
        print("autopilot ENGAGED — no idle-stop, auto-resume after compaction. "
              "Off: python .uvrun/autopilot.py off  (or delete .uvrun/.autopilot)")
    elif cmd == "off":
        try:
            if os.path.exists(SENTINEL):
                os.remove(SENTINEL)
        except Exception as e:
            print("failed to disengage:", e); return
        print("autopilot DISENGAGED — normal interactive behavior (stops when done; waits for a prompt).")
    elif cmd == "handback":
        # Seed the counter to CAP so the VERY NEXT stop is allowed (a clean hand-back to
        # the author, e.g. right after engaging, without steam-rolling a live conversation).
        write_ctr(CAP)
        print("seeded one clean hand-back (next stop allowed; autopilot stays engaged after).")
    else:  # status
        print("autopilot:", "ENGAGED" if os.path.exists(SENTINEL) else "OFF",
              "| turns:", read_ctr(), "| cap:", CAP)

# ------------------------------------------------------------------------------ main
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "status"
    if mode == "hook":
        try:
            out = hook_mode()
        except Exception:
            out = {}
        try:
            if out:
                print(json.dumps(out))
        except Exception:
            pass
    elif mode in ("on", "off", "status", "handback"):
        cli_mode(mode)
    else:
        cli_mode("status")
    sys.exit(0)
