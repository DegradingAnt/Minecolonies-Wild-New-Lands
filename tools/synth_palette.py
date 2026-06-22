"""Synthesize the modded-deco-palette workflow result into the deco palette data:
  modded_palette.json  — theme -> role -> [class-locked blocks] (the IN-GAME palette)
  render_proxy.json    — modded block id -> nearest VANILLA id (the board's representative preview)
  palette_credits.txt  — deduped credit lines (-> CREDITS.md)
Reads the workflow output file (arg 1) WITHOUT dumping it into the main context."""
import json, re, sys

raw = open(sys.argv[1], encoding="utf-8").read()
try:
    data = json.loads(raw)
except Exception:
    m = re.search(r'\{"themes"\s*:\s*\[.*\]\s*\}', raw, re.S)
    data = json.loads(m.group(0))
themes = data.get("themes") or data.get("result", {}).get("themes")

palette, proxy, credits, seen = {}, {}, [], set()
for t in themes:
    palette[t["theme"]] = {"roles": t["roles"]}
    proxy.update(t.get("render_proxy", {}))
    for c in t.get("credits", []):
        key = re.split(r"[—(]", c)[0].strip().lower()
        if key not in seen:
            seen.add(key); credits.append(c)

json.dump(palette, open("modded_palette.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(proxy, open("render_proxy.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open("palette_credits.txt", "w", encoding="utf-8").write("\n".join("- " + c for c in credits) + "\n")

modded = sorted({b for th in palette.values() for r in th["roles"].values() for b in r if ":" in b and not b.startswith("minecraft:")})
mods = sorted({b.split(":")[0] for b in modded})
print("themes=%d  modded_blocks=%d  proxies=%d  mods=%d  credit_lines=%d" % (
    len(palette), len(modded), len(proxy), len(mods), len(credits)))
print("mods featured:", ", ".join(mods))
# integrity: any modded block missing a proxy?
noproxy = [b for b in modded if b not in proxy]
print("modded blocks missing a render_proxy:", len(noproxy), noproxy[:8])
