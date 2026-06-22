"""Emit BUILD-GUIDE.md from deco_catalog_v2.json: per piece, per tier -> the vanilla block PALETTE
+ the course-by-course MASSING (build instructions) + footprint/height/ornament. This is the
in-game build reference (the human builds from this; the iso renders are just design preview).
Faithful catalog extraction -- no rendering, cheap."""
import json, os
import gen_board_md as M   # reuse slugify_tier so image filenames match the board renders

SRC = "deco_catalog_v2.json"
DEV = "C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version/_dev/wnl-pathways-src"
ORDER = ["cairn","milestone","menhir","lamp_post","banner_stand","wayshrine","rest_stop","well",
         "obelisk","plaza","gatehouse","dock_shack","pier","harbour"]

def palette_line(ps):
    if not isinstance(ps, dict): return ""
    parts = []
    for slot, blocks in ps.items():
        if not blocks: continue
        nice = ", ".join(b.replace("minecraft:", "") for b in blocks)
        parts.append(f"**{slot}:** {nice}")
    return "  ·  ".join(parts) if parts else "_(no light at this tier)_"

def main():
    res = json.load(open(SRC, encoding="utf-8"))
    by = {e["id"]: e["design"] for e in res}
    out = [
        "# wnl_pathways — deco BUILD GUIDE",
        "",
        "Per piece, per path tier: the vanilla **block palette** + the **course-by-course** build "
        "(y0 = ground up). Build these in-game by hand; weather/offset/palette-pick are hashed live "
        "by the data builder, so vary them as you go — these are the canonical massing + materials. "
        "All designs original; real-world/mod forms are inspiration only (see CREDITS.md).",
        "",
        "> Tiers ascend Trail → Path → Road → Highway → Great Road (some pieces rename or skip). "
        "`palette` lists the vanilla blocks per role-slot; pick within a slot per the live hash.",
        "",
        "---",
        "",
    ]
    for pid in ORDER + [k for k in by if k not in ORDER]:
        if pid not in by: continue
        d = by[pid]
        nm = pid.replace("_", " ").title()
        rid = d.get("registry_id", "wnl_" + pid)
        out += [f"## {nm} &nbsp;·&nbsp; `{rid}`", "", str(d.get("role", "")).strip(), ""]
        tiers = d.get("tiers", [])
        for i, t in enumerate(tiers):
            tier = t.get("tier", "?")
            h = t.get("height", "?")
            # image: top tier (last) = detail_svg/<pid>.svg ; lower tiers = detail_svg/<pid>_<slug>.svg
            svg = f"detail_svg/{pid}.svg" if i == len(tiers) - 1 else f"detail_svg/{pid}_{M.slugify_tier(tier)}.svg"
            out += [f"### {tier} &nbsp;·&nbsp; h{h}", ""]
            if os.path.exists(svg):
                out += [f'<img src="{svg}" width="540" alt="{nm} {tier}">', ""]
            out += [palette_line(t.get("palette_slots", {})), ""]
            massing = t.get("massing", [])
            if isinstance(massing, list) and massing:
                out += [f"- {c}" for c in massing] + [""]
            elif massing:
                out += [f"- {massing}", ""]
            # ornament kept as a one-line summary; escalation/footprint-prose dropped (the picture carries it)
        out += ["---", ""]
    md = "\n".join(out)
    open(os.path.join(DEV, "BUILD-GUIDE.md"), "w", encoding="utf-8").write(md)
    print("wrote BUILD-GUIDE.md |", len(by), "pieces | bytes", len(md.encode()))

if __name__ == "__main__":
    main()
