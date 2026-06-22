"""Robust img-based HTML design board for the 2nd monitor.
The old board INLINED 14 heavy SVGs into one 200KB+ page, which chokes the browser. This emits a
LIGHT page that references each SVG via <img src> (the same robust approach board.md uses), with
the SVGs copied next to the HTML so file:// resolves. One bad SVG can't break the whole page."""
import os, html, json, shutil, datetime
import gen_board_md as M   # reuse build_ladder / ladder_svg / dims / palettes

DEV = M.DEV
HEROES = M.HEROES
ORDER = M.ORDER

# copy current SVGs next to the HTML so <img src="detail_svg/x.svg"> resolves on file://
for sub in ("detail_svg", "ladder_svg"):
    dst = os.path.join(DEV, sub); os.makedirs(dst, exist_ok=True)
    if os.path.isdir(sub):
        for f in os.listdir(sub):
            if f.endswith(".svg"): shutil.copy2(os.path.join(sub, f), os.path.join(dst, f))

res = json.load(open(M.SRC, encoding="utf-8"))
by = {}
for e in res:
    d = dict(e["design"]); d["_id"] = e["id"]; by[e["id"]] = d

def put(rel, design=None, drop_last=False, ladder=False):
    """ensure the svg exists in .uvrun + copied to DEV; return the rel path for the <img>."""
    if ladder:
        open(rel, "w", encoding="utf-8").write(M.ladder_svg(design, drop_last=drop_last))
    shutil.copy2(rel, os.path.join(DEV, rel))
    return rel

cards = []
for pid in ORDER + [k for k in by if k not in ORDER]:
    if pid not in by: continue
    d = by[pid]; hero = pid in HEROES
    nm = pid.replace("_", " ").title()
    rid = html.escape(str(d.get("registry_id", "wnl_" + pid)))
    role = html.escape(str(d.get("role", "")).strip()[:300])
    imgs = []
    low = M.detailed_lower(pid, d)
    if os.path.exists("detail_svg/%s.svg" % pid):
        top_lbl = "R5 — Great Road" if pid == "cairn" else ("H6 — hero render" if hero else "top tier")
        badge = "FINAL · " + ("HERO · H6" if hero else "R5") + (" · full ladder" if low else "")
        imgs.append((put("detail_svg/%s.svg" % pid), top_lbl))
        if low:    # hand-detailed lower tiers -> show the real ladder, not the blob
            imgs += [(put(src), lbl) for src, lbl in low]
        elif hero:
            imgs.append((put("ladder_svg/%s_lower.svg" % pid, d, drop_last=True, ladder=True), "R1–R5 tiers (massing)"))
    else:
        badge = "HERO · H6" if hero else "R1–R5"
        imgs.append((put("ladder_svg/%s.svg" % pid, d, ladder=True), ""))
    body = ""
    for src, cap in imgs:
        if cap: body += '<div class="cap">%s</div>' % html.escape(cap)
        body += '<img class="render" src="%s" alt="%s" loading="lazy">' % (src, html.escape(nm))
    cards.append('<div class="card"><div class="chead"><h2>%s</h2><span class="id">%s</span>'
                 '<span class="pill">%s</span></div><div class="role">%s</div>%s</div>'
                 % (html.escape(nm), rid, html.escape(badge), role, body))

stamp = datetime.datetime.now().strftime("%H:%M:%S")
HEAD = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>wnl_pathways board</title><style>'
        ':root{--bg:#15161a;--card:#1e2026;--line:rgba(255,255,255,.10);--tp:#e9e9ec;--ts:#a6a6ae;--tt:#76767e}'
        '*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tp);font-family:system-ui,sans-serif;line-height:1.5}'
        'header{position:sticky;top:0;background:#101115ee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);'
        'padding:12px 24px;z-index:5;display:flex;gap:14px;align-items:center;flex-wrap:wrap}'
        'h1{font-size:17px;font-weight:500;margin:0}.sub{font-size:13px;color:var(--ts)}.live{margin-left:auto;font-size:12px;color:#5fb47e}'
        '.wrap{max-width:1100px;margin:0 auto;padding:18px 24px 60px}'
        '.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin-bottom:16px}'
        '.chead{display:flex;align-items:center;gap:10px;margin-bottom:4px}h2{font-size:16px;font-weight:500;margin:0}'
        '.id{font-family:ui-monospace,monospace;font-size:12px;color:var(--tt)}'
        '.pill{margin-left:auto;font-size:11px;color:#e0a85a;background:rgba(224,168,90,.16);padding:2px 9px;border-radius:20px}'
        '.role{font-size:13px;color:var(--ts);margin-bottom:8px}.cap{font-size:12px;color:var(--ts);margin:8px 0 2px}'
        '.render{width:100%;height:auto;display:block;background:#24262e;border:1px solid var(--line);border-radius:10px}'
        '</style></head><body><header><h1>wnl_pathways — deco board</h1>'
        '<span class="sub">14 pieces · R1–R5 (+H6 heroes) · light img build</span>'
        '<span class="live">updated ' + stamp + ' · ↻ Ctrl+R</span></header><div class="wrap">')
TAIL = ('</div><script>try{var y=sessionStorage.getItem("b");if(y)scrollTo(0,+y)}catch(e){}'
        'addEventListener("scroll",function(){try{sessionStorage.setItem("b",scrollY)}catch(e){}});'
        'setTimeout(function(){location.reload()},10000);</script></body></html>')
out = HEAD + "\n".join(cards) + TAIL
open(os.path.join(DEV, "DESIGN-BOARD.html"), "w", encoding="utf-8").write(out)
print("wrote img-based DESIGN-BOARD.html ->", DEV, "| cards", len(cards), "| bytes", len(out.encode()))
