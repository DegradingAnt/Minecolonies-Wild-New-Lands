#!/usr/bin/env python3
"""UserPromptSubmit hook: when the user's message looks like a correction / flags a miss,
inject a reminder to run /wnl-reflect automatically (standing directive 2026-06-29,
memory: reflect-automatically-on-miss). High-signal patterns only, to avoid noise."""
import sys, json, re

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = (data.get("prompt") or "")
low = prompt.lower()

# High-signal miss / correction phrases (kept tight on purpose)
PATTERNS = [
    r"\bforgot(ten)?\b", r"have you forgot", r"you (missed|keep|always|never)\b",
    r"\bre-?explain", r"told you (this|that|already)", r"\bagain\b.*(broke|stuck|wrong|fail)",
    r"\b(that'?s|thats) (wrong|not right|incorrect|not it)\b", r"\bnot (right|correct)\b",
    r"\bincorrect\b", r"\byou (broke|messed)\b", r"recurring", r"getting (really )?bad",
    r"same (mistake|issue|thing|problem)", r"didn'?t (work|fix)", r"why did you",
    r"stop (forgetting|losing)", r"\bmemory (issue|problem)",
]
hit = next((p for p in PATTERNS if re.search(p, low)), None)

if hit:
    msg = ("[auto-reflect] The user's message may signal a miss/correction "
           "(matched a correction pattern). Standing directive (memory: "
           "reflect-automatically-on-miss): if you got something wrong here, run the "
           "/wnl-reflect skill as a focused step WITHOUT being asked — capture the "
           "reasoning flaw as a trigger->action rule, then surface it. Don't merely offer.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": msg,
    }}))
sys.exit(0)
