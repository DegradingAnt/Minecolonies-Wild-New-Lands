import json, re, html, os

# Combined-SVG design board: one tall .svg that GitHub renders NATIVELY in the
# file view (no Pages, no tunnel, private repo OK). Reuses the HTML board's
# ladder/iso logic but bakes literal colors (GitHub's SVG sanitizer drops
# <style>/CSS-vars and <script>, so this is a static snapshot, regenerated on push).
SRC = "deco_catalog_v2.json"
OUT = "C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version/_dev/wnl-pathways-src/DESIGN-BOARD.svg"
HEROES = {"gatehouse", "harbour"}
ORDER = ["gatehouse","harbour","wayshrine","well","obelisk","plaza","rest_stop",
         "banner_stand","milestone","lamp_post","dock_shack","pier","menhir","cairn"]

# theme (literal, mirrors the HTML board)
BG="#15161a"; CARD="#1e2026"; CARD2="#24262e"; LINE="#34363e"
TP="#e9e9ec"; TS="#a6a6ae"; TT="#76767e"
HERO="#e0a85a"; NORM="#5f97c8"; FINAL="#5fb47e"
KINDCOL = {
    "data":   ("#a9a39a", "#8a847b", "#736e67"),
    "nbt":    ("#b6ac97", "#94896f", "#7a705a"),
    "hybrid": ("#a6acab", "#868c8b", "#6e7473"),
}
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
    s.append(f'<polygon points="{pts([P(0,D,H),P(W,D,H),P(W,D,0),P(0,D,0)])}" fill="{sth}" stroke="#5f5b54" stroke-width="0.5"/>')
    s.append(f'<polygon points="{pts([P(W,0,H),P(W,D,H),P(W,D,0),P(W,0,0)])}" fill="{est}" stroke="#544f49" stroke-width="0.5"/>')
    s.append(f'<polygon points="{pts([P(0,0,H),P(W,0,H),P(W,D,H),P(0,D,H)])}" fill="{top}" stroke="#6f6a63" stroke-width="0.5"/>')
    for hy in range(1, int(H)):
        if H > 6 and hy % 2: continue
        a = P(0,D,hy); b = P(W,D,hy)
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#5f5b54" stroke-width="0.4" opacity="0.35"/>')
    return "".join(s)

def strip_inner(design):
    """Interpolated ladder, literal colors. Returns (inner_svg, vbW, vbH)."""
    kind = design.get("kind","data")
    top,sth,est = KINDCOL.get(kind, KINDCOL["data"])
    lad = build_ladder(design)
    SW, SH = 108.0, 116.0
    def usc(w,d,h): return min(SW/max(w+d,1), SH/max((w+d)/2.0+h,1))
    U = max(2.2, min(8.0, min(usc(w,d,h) for w,d,h,_,_ in lad)))
    n = len(lad); colw = min(116.0, 636.0/n); startx = 46 + colw/2.0; base = 150.0
    parts = []
    for i,(w,d,h,interp,label) in enumerate(lad):
        cx = startx + i*colw
        ct = ("#6f6c66","#5d5a55","#4f4c47") if interp else (top,sth,est)
        parts.append(iso_box(cx, base, w, d, h, U, *ct))
        lc = TT if interp else TP
        pre = "~" if interp else ""
        parts.append(f'<text x="{round(cx,1)}" y="167" text-anchor="middle" font-family="{FF}" font-size="12" font-weight="500" fill="{lc}">{pre}{label}</text>')
        parts.append(f'<text x="{round(cx,1)}" y="180" text-anchor="middle" font-family="{FF}" font-size="11" fill="{TS}">{w}×{d}×{h}</text>')
    return "".join(parts), 700.0, 192.0

def detail_inner(pid):
    txt = open("detail_svg/%s.svg" % pid, encoding="utf-8").read()
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', txt, re.S)
    vb = m.group(1).split()
    return m.group(2), float(vb[2]), float(vb[3])

def wrap(text, maxc, maxlines):
    words = text.split(); lines = []; cur = ""
    for w in words:
        if len(cur)+len(w)+1 <= maxc: cur = (cur+" "+w).strip()
        else:
            lines.append(cur); cur = w
            if len(lines) == maxlines: break
    if cur and len(lines) < maxlines: lines.append(cur)
    used = sum(len(x) for x in lines) + max(0,len(lines)-1)
    if len(lines) == maxlines and used < len(text.strip()):
        lines[-1] = lines[-1][:maxc-1].rstrip() + "…"
    return lines

def main():
    res = json.load(open(SRC, encoding="utf-8"))
    by = {}
    for e in res:
        d = dict(e["design"]); d["_id"] = e["id"]; by[e["id"]] = d

    WIDTH = 860; M = 18; PAD = 14
    cardw = WIDTH - 2*M
    slotw = cardw - 2*PAD
    y = 64
    body = []
    for pid in ORDER + [k for k in by if k not in ORDER]:
        if pid not in by: continue
        d = by[pid]; hero = pid in HEROES
        nm = pid.replace("_"," ").title()
        rid = html.escape(str(d.get("registry_id", "wnl_"+pid)))
        role = html.escape(str(d.get("role","")))
        detail = os.path.exists("detail_svg/%s.svg" % pid)
        inner, vbW, vbH = detail_inner(pid) if detail else strip_inner(d)
        scale = slotw / vbW
        renderh = vbH * scale
        rlines = wrap(role, 104, 2)
        headerh = 26; roleh = 4 + len(rlines)*16; slotpad = 8
        cardh = 12 + headerh + roleh + slotpad + renderh + slotpad + 10
        cx0 = M; cy0 = y
        body.append(f'<rect x="{cx0}" y="{cy0}" width="{cardw}" height="{round(cardh,1)}" rx="14" fill="{CARD}" stroke="{LINE}" stroke-width="1"/>')
        tx = cx0 + PAD; ty = cy0 + 12
        body.append(f'<text x="{tx}" y="{ty+16}" font-family="{FF}" font-size="16" font-weight="600" fill="{TP}">{html.escape(nm)}</text>')
        badge = ("HERO · H6" if hero else "R1–R5")
        if detail: badge = "FINAL · " + badge
        bcol = FINAL if detail else (HERO if hero else NORM)
        bw = 12 + len(badge)*6.6
        bx = cx0 + cardw - PAD - bw
        body.append(f'<rect x="{round(bx,1)}" y="{ty+2}" width="{round(bw,1)}" height="18" rx="9" fill="{bcol}" fill-opacity="0.16" stroke="{bcol}" stroke-width="0.8"/>')
        body.append(f'<text x="{round(bx+bw/2,1)}" y="{ty+15}" text-anchor="middle" font-family="{FF}" font-size="11" font-weight="500" fill="{bcol}">{html.escape(badge)}</text>')
        body.append(f'<text x="{round(bx-10,1)}" y="{ty+16}" text-anchor="end" font-family="ui-monospace,monospace" font-size="12" fill="{TT}">{rid}</text>')
        ry = cy0 + 12 + headerh
        for li,ln in enumerate(rlines):
            body.append(f'<text x="{tx}" y="{round(ry+li*16+12,1)}" font-family="{FF}" font-size="13" fill="{TS}">{ln}</text>')
        sy = ry + roleh
        body.append(f'<rect x="{tx}" y="{round(sy,1)}" width="{slotw}" height="{round(renderh+2*slotpad,1)}" rx="10" fill="{CARD2}" stroke="{LINE}" stroke-width="1"/>')
        body.append(f'<g transform="translate({round(tx,2)},{round(sy+slotpad,2)}) scale({round(scale,4)})">{inner}</g>')
        y = cy0 + cardh + 16

    total_h = round(y + 10, 1)
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{total_h}" '
            f'viewBox="0 0 {WIDTH} {total_h}" font-family="{FF}">\n'
            f'<rect x="0" y="0" width="{WIDTH}" height="{total_h}" fill="{BG}"/>\n'
            f'<text x="{M}" y="30" font-family="{FF}" font-size="18" font-weight="600" fill="{TP}">wnl_pathways — deco design board · 2.5D</text>\n'
            f'<text x="{M}" y="50" font-family="{FF}" font-size="12" fill="{TS}">14 pieces · R1–R5 tiers (+H6 heroes) · scale in blocks (W×D×H) · renders natively on GitHub</text>\n')
    svg = head + "\n".join(body) + "\n</svg>\n"
    open(OUT, "w", encoding="utf-8").write(svg)
    print("wrote SVG board:", OUT, "| height", total_h, "| bytes", len(svg.encode("utf-8")))

main()
