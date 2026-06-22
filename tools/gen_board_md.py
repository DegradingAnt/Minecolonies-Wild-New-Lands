import json, re, html, os

# GitHub-native board: a Markdown file embedding each piece as its OWN image. Markdown renders
# reliably on github.com (the giant single SVG did not), and relative SVG <img> render inline.
# For pieces without a hand-detail render we emit a standalone, CLEARLY-VISIBLE ladder SVG
# (each tier a cell-filling iso box + real W×D×H label) -- fixes the "can't see ladders" problem.
SRC = "deco_catalog_v2.json"
DEV = "C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version/_dev/wnl-pathways-src"
os.makedirs("ladder_svg", exist_ok=True)

HEROES = {"gatehouse", "harbour"}
ORDER = ["gatehouse","harbour","wayshrine","well","obelisk","plaza","rest_stop",
         "banner_stand","milestone","lamp_post","dock_shack","pier","menhir","cairn"]
KINDCOL = {
    "data":   ("#a9a39a", "#8a847b", "#736e67"),
    "nbt":    ("#b6ac97", "#94896f", "#7a705a"),
    "hybrid": ("#a6acab", "#868c8b", "#6e7473"),
}
TP, TS, TT = "#e9e9ec", "#a6a6ae", "#76767e"
CARD2, LINE = "#24262e", "#34363e"
FF = "system-ui,-apple-system,Segoe UI,Roboto,sans-serif"

def dims(fp):
    nums = [int(n) for n in re.findall(r"\d+", str(fp))]
    nums = [min(n, 42) for n in nums] or [3]
    w = nums[0]; d = nums[1] if len(nums) > 1 else nums[0]
    return max(w,1), max(d,1)

NAME_SLOT = [("great",5),("grand",5),("forum",5),("highway",4),("road",3),("path",2),("trail",1)]
def name_slot(name):
    s = (name or "").lower()
    for kw,sl in NAME_SLOT:
        if kw in s: return sl
    return None

# Detailed lower-tier renders (hand-built per tier) live at detail_svg/<pid>_<slug>.svg, where
# slug = the first alnum word of the catalog tier name, lowercased (cairn->trail/path/road/highway;
# obelisk->trail/road/highway/great; pier->ruined/fisher/stone; harbour->small/.../great). Catalog
# tiers are ascending, so the LAST is the top (already render_<pid>.py); the rest are the ladder.
# When the detailed render exists it replaces the dims-only "blob" ladder for that tier.
def slugify_tier(name):
    # tier names may be "Road -> small_quay" (the meaningful id is AFTER the arrow) or plain "Trail"
    # or "Trail — bankside perch" (first word). Take past the last arrow, then the first alnum word.
    s = str(name).lower()
    if "->" in s: s = s.rsplit("->", 1)[1]
    for w in re.split(r"[^a-z0-9]+", s.strip()):
        if w: return w
    return "tier"
def detailed_lower(pid, design):
    out = []
    for t in design.get("tiers", [])[:-1]:
        slug = slugify_tier(t.get("tier", ""))
        f = "detail_svg/%s_%s.svg" % (pid, slug)
        if os.path.exists(f):
            nm = re.split(r"[—\-]| -> |->", str(t.get("tier","")))[0].strip().title()
            out.append((f, nm))
    return out

def build_ladder(design):
    pid = design["_id"]; hero = pid in HEROES
    T = design.get("tiers", [])
    dd = [(*dims(t.get("footprint","3x3")), max(int(t.get("height",3)),1)) for t in T]
    n = len(dd); known = {}
    if hero:
        for i in range(n):
            if i == n-1: known[6] = dd[i]
            else:
                sl = name_slot(T[i].get("tier",""))
                if not sl or sl in known: sl = min(i+1,5)
                known[sl] = dd[i]
        slots = [1,2,3,4,5,6]
    elif n == 5:
        for i in range(5): known[i+1] = dd[i]
        slots = [1,2,3,4,5]
    else:
        for i in range(n):
            sl = name_slot(T[i].get("tier","")) or (i+1)
            while sl in known and sl < 5: sl += 1
            known[min(sl,5)] = dd[i]
        slots = [1,2,3,4,5]
    ks = sorted(known); out = []
    for s in slots:
        if s in known:
            w,d,h = known[s]; out.append((w,d,h,False))
        else:
            lo = [k for k in ks if k < s]; hi = [k for k in ks if k > s]
            if lo and hi:
                a = known[lo[-1]]; b = known[hi[0]]; f = (s-lo[-1])/(hi[0]-lo[-1])
                v = [max(1,round(a[j]+(b[j]-a[j])*f)) for j in range(3)]
            elif lo:
                a = known[lo[-1]]; sc = 1.0+0.24*(s-lo[-1]); v = [max(1,round(a[j]*sc)) for j in range(3)]
            elif hi:
                b = known[hi[0]]; sc = max(0.42,1.0-0.20*(hi[0]-s)); v = [max(1,round(b[j]*sc)) for j in range(3)]
            else:
                v = [3,3,3]
            out.append((v[0],v[1],v[2],True))
    lbl = ["R1","R2","R3","R4","R5","H6"]
    return [(out[i][0],out[i][1],out[i][2],out[i][3],lbl[slots[i]-1]) for i in range(len(slots))]

def iso_box(cx, base, W, D, H, U, top, sth, est):
    V = U*0.5; BH = U
    ox = cx - (W-D)*U/2.0
    oy = base - (W+D)*V
    def P(x,z,y): return (round(ox+(x-z)*U,1), round(oy+(x+z)*V-y*BH,1))
    def pts(ps): return " ".join(f"{a},{b}" for a,b in ps)
    s = []
    s.append(f'<polygon points="{pts([P(0,D,H),P(W,D,H),P(W,D,0),P(0,D,0)])}" fill="{sth}" stroke="#4a463f" stroke-width="0.6"/>')
    s.append(f'<polygon points="{pts([P(W,0,H),P(W,D,H),P(W,D,0),P(W,0,0)])}" fill="{est}" stroke="#433f39" stroke-width="0.6"/>')
    s.append(f'<polygon points="{pts([P(0,0,H),P(W,0,H),P(W,D,H),P(0,D,H)])}" fill="{top}" stroke="#5a554e" stroke-width="0.6"/>')
    for hy in range(1, int(H)):
        if H > 8 and hy % 2: continue
        a = P(0,D,hy); b = P(W,D,hy)
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#4a463f" stroke-width="0.4" opacity="0.4"/>')
    return "".join(s)

def ladder_svg(design, drop_last=False):
    """Standalone, clearly-visible ladder: each tier is a cell-filling iso box + real dims.
    drop_last omits the top rung (used for heroes: their H6 is the detail render, so the
    ladder shows R1-R5 underneath it)."""
    kind = design.get("kind","data"); top,sth,est = KINDCOL.get(kind, KINDCOL["data"])
    lad = build_ladder(design)
    if drop_last and len(lad) > 1: lad = lad[:-1]
    n = len(lad)
    W = 840; CW = W/n; DRAW_H = 168; baseY = 196; H = 250
    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="12" fill="{CARD2}"/>']
    for i,(w,d,h,interp,label) in enumerate(lad):
        cx = CW*i + CW/2
        # fit the box into its cell; clamp so tiny tiers aren't huge and big tiers stay in-cell
        U = min(CW*0.78/max(w+d,1), DRAW_H/max((w+d)*0.5+h,1))
        U = max(3.6, min(15.0, U))
        ct = ("#6f6c66","#5d5a55","#4f4c47") if interp else (top,sth,est)
        parts.append(iso_box(cx, baseY, w, d, h, U, *ct))
        lc = TT if interp else TP; pre = "~" if interp else ""
        parts.append(f'<text x="{cx:.1f}" y="222" text-anchor="middle" font-family="{FF}" font-size="16" font-weight="600" fill="{lc}">{pre}{label}</text>')
        parts.append(f'<text x="{cx:.1f}" y="240" text-anchor="middle" font-family="{FF}" font-size="12.5" fill="{TS}">{w}×{d}×{h}</text>')
        if i:  # faint divider between cells
            parts.append(f'<line x1="{CW*i:.1f}" y1="14" x2="{CW*i:.1f}" y2="{H-14}" stroke="{LINE}" stroke-width="1" opacity="0.5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{FF}"><title>{html.escape(design["_id"])} massing ladder</title>'
            + "".join(parts) + "</svg>\n")

def main():
    res = json.load(open(SRC, encoding="utf-8"))
    by = {}
    for e in res:
        d = dict(e["design"]); d["_id"] = e["id"]; by[e["id"]] = d
    lines = [
        "# wnl_pathways — deco design board",
        "",
        "Every deco/structure piece across its tiers (**R1–R5**, plus **H6** for the hero pieces). "
        "Detailed pieces show a hand-drawn 2.5D render; the rest show the **massing ladder** "
        "(footprint + height per tier, in blocks). All designs are original; modded+vanilla palettes.",
        "",
        "> Scale labels are `W×D×H` in blocks. `~` marks an interpolated (not-yet-finalised) tier. "
        "R5 cairn top still open; palettes pending modded-enrich.",
        "",
        "---",
        "",
    ]
    detailed = 0
    for pid in ORDER + [k for k in by if k not in ORDER]:
        if pid not in by: continue
        d = by[pid]; hero = pid in HEROES
        nm = pid.replace("_"," ").title()
        rid = str(d.get("registry_id", "wnl_"+pid))
        role = html.escape(str(d.get("role","")).strip())
        is_detail = os.path.exists("detail_svg/%s.svg" % pid)
        imgs = []   # (src, caption)
        low = detailed_lower(pid, d)
        if is_detail:
            detailed += 1
            top_lbl = "R5 — Great Road" if pid == "cairn" else ("H6 — hero render" if hero else "top tier")
            badge = "FINAL · " + ("HERO · H6" if hero else "R5") + (" · full ladder" if low else "")
            imgs.append(("design/detail_svg/%s.svg" % pid, top_lbl))
            if low:    # hand-detailed lower tiers -> show the real ladder, not the blob
                imgs += [("design/" + src, lbl) for src, lbl in low]
            elif hero: # fallback: heroes still get the dims-only R1-R5 ladder under the H6 render
                open("ladder_svg/%s_lower.svg" % pid, "w", encoding="utf-8").write(ladder_svg(d, drop_last=True))
                imgs.append(("design/ladder_svg/%s_lower.svg" % pid, "R1–R5 tiers (massing)"))
        else:
            open("ladder_svg/%s.svg" % pid, "w", encoding="utf-8").write(ladder_svg(d))
            badge = "HERO · H6" if hero else "R1–R5"
            imgs.append(("design/ladder_svg/%s.svg" % pid, ""))
        lines += [f"## {nm} &nbsp;·&nbsp; `{rid}` &nbsp;·&nbsp; _{badge}_", "", role, ""]
        for src, cap in imgs:
            if cap: lines.append(f"**{cap}**")
            lines += [f'<img src="{src}" width="840" alt="{nm}">', "", f"<sub>[open full image]({src})</sub>", ""]
        lines += ["---", ""]
    md = "\n".join(lines)
    open(os.path.join(DEV, "DESIGN-BOARD.md"), "w", encoding="utf-8").write(md)
    print("wrote DESIGN-BOARD.md |", detailed, "detailed +", 14-detailed, "ladders | bytes", len(md.encode()))

if __name__ == "__main__":
    main()
