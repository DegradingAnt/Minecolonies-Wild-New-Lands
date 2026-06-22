"""Cairn PATH (R2) -> detail_svg/cairn_path.svg.
Per deco_catalog_v2.json id 'cairn' tier Path (footprint 1x1 stack on a loose 2-radius scatter
skirt, height 4): a small jump from Trail -- +1 course, +a ground SKIRT of fallen stones, +an
intentional cap (slab or wall-nub) so it reads as a MADE marker someone TENDS, not a chance pile.
Still humble + UNLIT (the big leaps are saved for Road/Highway -- non-linear ladder curve).
Same wnl_cairn data builder as render_cairn.py (Great Road top); inspiration credited in CREDITS.md."""
from iso_render import Iso

S = Iso(U=24)

CORE  = "#8a8276"   # cobblestone core
CORE2 = "#9b9488"   # andesite/stone lighter pick
DARK  = "#6f685d"   # cobbled_deepslate base
MOSS  = "#6f7d56"   # mossy_cobblestone accent (wear)
CRACK = "#9a8f7e"   # cracked_stone_bricks accent (a tended-but-worn note)
SKIRT = "#7c7468"   # half-buried fallen skirt stones (sunk, slightly darker -> sit in terrain)

# Course 0 (y0): ground SKIRT -- 3 loose stones + 1 slab scattered half-buried in neighbour
# columns (NOT a tidy ring): "stones that rolled off the pile". Each sunk (dy<1) -> sits in ground.
S.box(-0.85, 0.05, 0, 1, 1, 0.6, SKIRT)           # west boulder -- OVERLAPS the base west face (grounded spill, not floating)
S.box( 0.95, 0.3,  0, 1, 1, 0.55, SKIRT)          # east boulder -- abuts the base east face
S.box( 0.15, 0.95, 0, 1, 1, 0.5, SKIRT)           # front boulder -- abuts the base front face
S.box(-0.55,-0.55, 0, 0.9, 0.9, 0.45, MOSS)       # back-corner stone -- touches the west boulder (chained, not isolated)

# Course 1 (y1): base stone, full block, sunk 1 into the centre column (rooted, the anchor).
S.box(0, 0, 0, 1, 1, 1, DARK, seam=True)

# Course 2 (y2): stone offset ~0.3 (supported lean -- inner 2/3 still bears on y1, reads stable not floaty).
S.box(0.3, 0.12, 1, 1, 1, 1, CORE, seam=True)

# Course 3 (y3): stone offset back the other way (~0.3); the worn accent course (cracked/mossy).
S.box(0.02, 0.34, 2, 1, 1, 1, CRACK, seam=True)

# Course 4 (y4): capstone -- a core slab cap here (the alt is a single cobblestone_wall nub);
# the first hint someone TENDS this marker.
S.box(0.1, 0.15, 3, 0.85, 0.85, 0.5, CORE2)

S.label(0.5, 0.5, 3.3, "intentional slab cap (or wall-nub) -- first sign it is TENDED")
S.label(0.0, 0.9, 2.3, "worn accent course (cracked / mossy stone)")
S.label(1.4, -0.2, 0.4, "loose ground scatter skirt (2-4 fallen half-buried stones)")

out = S.svg(title="Cairn R2 (Path) -- tended hand-stack: +scatter skirt, +intentional cap, still unlit",
            size_label="1x1 stack + scatter skirt * h4 * 0 lanterns (a worn footpath marker someone keeps)",
            label_w=320)
open("detail_svg/cairn_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/cairn_path.svg | bytes", len(out.encode()))
