#!/usr/bin/env python3
"""UserPromptSubmit hook: injects a check-in reminder so Claude doesn't run long autonomous
sessions without syncing. Script-based (not inline echo) for durability across shells."""
import json, sys
msg = ("Check-in reminder (user-requested): you tend to work in long autonomous sessions and the user "
       "prefers frequent check-ins. Before launching a long multi-step build or another slow boot, briefly "
       "sync direction. If the user has sent several messages in a row, pause and address them together "
       "rather than barreling ahead heads-down.")
sys.stdout.write(json.dumps({
    "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}
}))
