"""Cairn ROAD (R3) -> detail_svg/cairn_road.svg.
Per deco_catalog_v2.json id 'cairn' tier Road (footprint 2x2 body on a 3x3 base-pad, height 6):
the real jump -- doubles to a 2x2 body on a stair-dressed 3x3 pad, gains a chiseled-brick PLAQUE
face turned to the road, a wall-post neck, and the FIRST LIGHT (single lantern) + offering ledge.
Becomes a tended civic marker. One pad corner left as coarse_dirt so it sits IN the ground (the
pad is not a perfect square). Same wnl_cairn data builder as render_cairn.py; inspiration in CREDITS.md.
ISO: road-facing FRONT = high-z (south) + high-x (east); plaque turned to that front."""
from iso_render import Iso

S = Iso(U=21)

PAD   = "#8a8276"   # 3x3 cobble base pad
STAIR = "#6f685d"   # stair-dressed pad edge (darker -> reads as the stepped skirt)
DIRT  = "#5d4f3a"   # one corner left coarse_dirt (sits in the ground -- pad not a perfect square)
BODY  = "#9b9488"   # 2x2 stacked body (core mix, lighter -> pops off the pad)
BODY2 = "#857d70"   # the wonked body block (a dropped/shifted stone for asymmetry)
MOSS  = "#6f7d56"   # mossy/cracked accent course (wear)
PLAQ  = "#b9b3a5"   # chiseled_stone_bricks PLAQUE block (bright -> the carved face reads)
NECK  = "#9a9384"   # cobblestone_wall post neck
LEDGE = "#7a5c3a"   # warm offering-ledge slab beside the neck (one warm note)
LANT  = "#ffd47a"   # lantern glow (FIRST lit tier)

# Course 0 (y0): 3x3 base PAD, stair-dressed on 2 visible sides (asymmetry), 1 corner coarse_dirt.
S.box(0,0,0, 3,3,1, PAD, seam=True)
S.box(0,2,0, 3,1,1, STAIR)                 # front (high-z) stair-dressed edge -- the read edge
S.box(2,0,0, 1,3,1, STAIR)                 # east stair-dressed edge
S.box(0,0,0, 1,1,1, DIRT)                  # back-west corner left as coarse_dirt (sits in ground)

# Course 1 (y1): 2x2 stacked body, one of the 4 dropped to a slab / shifted for wonk.
S.box(0.5,0.5,1, 2,2,1, BODY, seam=True)
S.box(1.6,1.55,1, 1,1,0.6, BODY2)          # ONE block dropped to a slab + nudged (hand-stacked wonk)

# Course 2 (y2): 2x2 body continues, a DIFFERENT block wonked; ~accent for wear.
S.box(0.5,0.5,2, 2,2,1, MOSS, seam=True)
S.box(0.4,1.1,2, 1,1,1, BODY2)             # rotated-asymmetry wonk block

# Course 3 (y3): tapers to 1x1 chiseled PLAQUE block, carved face to the road (front, high-z).
S.box(0.9,1.0,3, 1,1,1, PLAQ, seam=True)
S.box(0.95,1.95,3.25,0.9,0.12,0.55, "#403c34")  # the recessed carved face turned to the road

# Course 4 (y4): cobblestone_wall post -- the NECK (stays a real block).
S.box(1.1,1.2,4, 0.8,0.8,1, NECK, seam=True)
# offering ledge slab tucked beside the neck
S.box(1.95,1.2,4, 0.5,0.8,0.4, LEDGE)

# Course 5 (y5): LANTERN in the column directly above the wall post (rests on its top face).
S.accent(1.5, 1.6, 5.15, "glow", LANT, r=2.4)

S.label(1.5, 1.6, 5.2, "FIRST lantern (above the wall-post neck) + offering ledge slab")
S.label(1.4, 1.0, 3.5, "chiseled-brick PLAQUE block -- carved face turned to the road")
S.label(0.5, 2, 2.0, "2x2 hand-wonked body (one block dropped/shifted per course)")
S.label(0, 2, 0.5, "3x3 stair-dressed pad (1 corner coarse_dirt -- sits in the ground)")

out = S.svg(title="Cairn R3 (Road) -- tended civic marker: 3x3 pad, 2x2 body, plaque face, FIRST light",
            size_label="3x3 pad / 2x2 body * h6 * 1 lantern (the road's first proper laid-surface marker)",
            label_w=336)
open("detail_svg/cairn_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/cairn_road.svg | bytes", len(out.encode()))
