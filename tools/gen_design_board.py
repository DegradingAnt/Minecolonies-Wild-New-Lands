import json, re, html, os, datetime

SRC = "deco_catalog_v2.json"
OUT = "C:/Users/linde/curseforge/minecraft/Instances/Ultimate vibes distant horizons version/_dev/wnl-pathways-src/DESIGN-BOARD.html"
HEROES = {"gatehouse", "harbour"}
KINDCOL = {
    "data":   ("#a9a39a", "#8a847b", "#736e67"),
    "nbt":    ("#b6ac97", "#94896f", "#7a705a"),
    "hybrid": ("#a6acab", "#868c8b", "#6e7473"),
}
ORDER = ["gatehouse","harbour","wayshrine","well","obelisk","plaza","rest_stop",
         "banner_stand","milestone","lamp_post","dock_shack","pier","menhir","cairn"]

def dims(fp):
    nums = [int(n) for n in re.findall(r"\d+", str(fp))]
    nums = [min(n, 42) for n in nums] or [3]
    w = nums[0]
    d = nums[1] if len(nums) > 1 else nums[0]
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
    # course seams on the south face (a few horizontal block lines)
    for hy in range(1, int(H)):
        if H > 6 and hy % 2: continue
        a = P(0,D,hy); b = P(W,D,hy)
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#5f5b54" stroke-width="0.4" opacity="0.35"/>')
    return "".join(s)

def strip_svg(design, drop_last=False):
    kind = design.get("kind","data")
    top,sth,est = KINDCOL.get(kind, KINDCOL["data"])
    lad = build_ladder(design)
    if drop_last and len(lad) > 1: lad = lad[:-1]
    SW, SH = 108.0, 116.0
    def usc(w,d,h): return min(SW/max(w+d,1), SH/max((w+d)/2.0+h,1))
    U = max(2.2, min(8.0, min(usc(w,d,h) for w,d,h,_,_ in lad)))
    n = len(lad); colw = min(116.0, 636.0/n); startx = 46 + colw/2.0; base = 150.0
    parts = []
    for i,(w,d,h,interp,label) in enumerate(lad):
        cx = startx + i*colw
        ct = ("#6f6c66","#5d5a55","#4f4c47") if interp else (top,sth,est)
        parts.append(iso_box(cx, base, w, d, h, U, *ct))
        lc = "#76767e" if interp else "var(--color-text-primary)"
        pre = "~" if interp else ""
        parts.append(f'<text x="{round(cx,1)}" y="167" text-anchor="middle" font-family="var(--font-sans)" font-size="12" font-weight="500" fill="{lc}">{pre}{label}</text>')
        parts.append(f'<text x="{round(cx,1)}" y="180" text-anchor="middle" font-family="var(--font-sans)" font-size="11" fill="var(--color-text-secondary)">{w}×{d}×{h}</text>')
    return f'<svg width="100%" viewBox="0 0 700 192" role="img"><title>{html.escape(design["_id"])} ladder</title>' + "".join(parts) + "</svg>"

def main():
    res = json.load(open(SRC, encoding="utf-8"))
    by = {}
    for e in res:
        d = dict(e["design"]); d["_id"] = e["id"]; by[e["id"]] = d
    cards = []
    for pid in ORDER + [k for k in by if k not in ORDER]:
        if pid not in by: continue
        d = by[pid]
        hero = pid in HEROES
        badge = '<span class="pill p-hero">HERO · H6</span>' if hero else '<span class="pill p-norm">R1–R5</span>'
        role = html.escape(str(d.get("role",""))[:240])
        rid = html.escape(str(d.get("registry_id", "wnl_"+pid)))
        nm = pid.replace("_"," ").title()
        dp = "detail_svg/%s.svg" % pid
        if os.path.exists(dp):
            svg = open(dp, encoding="utf-8").read()
            badge = '<span class="pill p-final">FINAL · detailed</span>' + badge
            if hero:   # heroes also show the R1-R5 ladder under their H6 render
                svg += ('<div style="margin-top:6px;padding-top:6px;border-top:1px solid var(--line);'
                        'font-size:12px;color:var(--color-text-secondary)">R1–R5 tiers</div>'
                        + strip_svg(d, drop_last=True))
        else:
            svg = strip_svg(d)
        cards.append(f'''<div class="card">
  <div class="chead"><h2>{nm}</h2><span class="id">{rid}</span>{badge}</div>
  <div class="role">{role}</div>
  <div class="svgbox">{svg}</div>
</div>''')
    body = "\n".join(cards)
    stamp = "updated " + datetime.datetime.now().strftime("%H:%M:%S") + " · ↻ Ctrl+R to force"
    page = HTML_HEAD.replace("auto-refreshing", stamp) + body + HTML_TAIL
    open(OUT, "w", encoding="utf-8").write(page)
    print("wrote board:", len(cards), "pieces ->", OUT)

HTML_HEAD = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>wnl_pathways — design board (2.5D)</title>
<style>
:root{--bg:#15161a;--card:#1e2026;--card2:#24262e;--line:rgba(255,255,255,.10);
--color-text-primary:#e9e9ec;--color-text-secondary:#a6a6ae;--color-text-tertiary:#76767e;
--font-sans:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--color-text-primary);font-family:var(--font-sans);line-height:1.5}
header{position:sticky;top:0;background:#101115ee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:13px 26px;z-index:5;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
header h1{font-size:18px;font-weight:500;margin:0}.sub{font-size:13px;color:var(--color-text-secondary)}
.live{font-size:12px;color:#5fb47e;margin-left:auto}
.wrap{max-width:1180px;margin:0 auto;padding:20px 26px 60px}
.note{background:var(--card2);border-left:2px solid #e0a85a;border-radius:0 6px 6px 0;padding:9px 13px;font-size:13px;color:var(--color-text-secondary);margin-bottom:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px 12px;margin-bottom:18px}
.chead{display:flex;align-items:center;gap:10px;margin-bottom:3px}.chead h2{font-size:16px;font-weight:500;margin:0}
.id{font-family:ui-monospace,monospace;font-size:12px;color:var(--color-text-tertiary)}
.pill{font-size:11px;font-weight:500;padding:2px 9px;border-radius:20px;margin-left:auto}
.p-hero{background:rgba(224,168,90,.18);color:#e0a85a}.p-norm{background:rgba(95,151,200,.16);color:#5f97c8}
.role{font-size:13px;color:var(--color-text-secondary);margin-bottom:6px}
.svgbox{background:var(--card2);border:1px solid var(--line);border-radius:10px;padding:4px}
</style></head><body>
<header><h1>wnl_pathways — deco design board · 2.5D</h1>
<span class="sub">14 pieces · R1–R5 tiers (+H6 heroes) · generated from v2 · scale in blocks (W×D×H)</span>
<span class="live">auto-refreshing</span></header>
<div class="wrap">
<div class="note">2.5D massing pass over every piece (top-down, heroes first). Boxes show footprint + height per tier — hand-detailed crowns/arches/plaques come next, top-down. <b>R5 cairn top still open.</b> Palettes pending modded-enrich (v2 came back vanilla-only).</div>
'''
HTML_TAIL = '''</div>
<script>try{var y=sessionStorage.getItem('b');if(y)scrollTo(0,+y)}catch(e){}
addEventListener('scroll',function(){try{sessionStorage.setItem('b',scrollY)}catch(e){}});
setTimeout(function(){location.reload()},8000);</script>
</body></html>'''

main()
