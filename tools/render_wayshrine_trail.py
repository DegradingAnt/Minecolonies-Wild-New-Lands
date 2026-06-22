"""Wayshrine TRAIL (R1, floor of the ladder) -> detail_svg/wayshrine_trail.svg.
Per deco_catalog_v2.json id 'wayshrine' tier Trail (footprint 3x3, 1-deep usable niche, height 4):
the smallest legible wayside shrine -- a hand-stacked mossy-cobblestone back wall with a single
recessed lit NICHE under a tiny stone gable hood, bracketed by two waist-high cobblestone-wall
posts. Deliberately HUMBLE: raw cobble, flat-topped nook (no arch claim yet), one lit flame, one
optional vine. The ornament IS the light + the moss + the little peak. Sits IN the path (front-
centre cell left as the bare dirt path so the traveller stands flush).

This is the FLOOR of the same wnl_wayshrine whose Great-Road top tier is render_wayshrine.py;
the data builder hashes flame-type (candle 2/3 vs standing lantern 1/3), moss%, and the vine
(present iff distance_decay>0.4) live per shrine. Drawn here as the candle + light-vine case.

ISO: visible faces are FRONT (max-z) + east (max-x) + top, so the niche opens on the FRONT (z) face
toward the viewer -- the traveller reads the lit nook head-on.
Originality/inspiration: the European wayside aedicula / lantern-of-the-dead niche-house FORM,
technique only -- credited in CREDITS.md, no assets/NBT/palette copied."""
from iso_render import Iso

S = Iso(U=26)

# ---- palette (literal) -- a clear luminance ladder so every raw-cobble block reads as itself.
#      dark->light: PATH < MOSS < COBB < MSB < LEDGE < FLAME-glow (accent).
COBB  = "#8a8276"   # cobblestone (the common hand-stacked field block)
MOSS  = "#6f7d56"   # mossy_cobblestone (the dominant body -- moss reads green-grey)
MSB   = "#9b9488"   # mossy_stone_bricks (the one dressed scatter block, a touch lighter)
WALLP = "#7e776b"   # cobblestone_wall posts (waist-high, slightly darker raw cobble)
LEDGE = "#b8b2a4"   # stone_brick_slab offering ledge (lightest dressed stone -> the flame sits proud)
NICHE = "#4a463d"   # recessed nook interior (deep shadow so the cavity reads cut-IN, not painted-on)
PATH  = "#6b5836"   # dirt_path the traveller stands on (clearly earth, front-centre cell)
COBBS = "#807868"   # cobblestone scatter under the niche (ground course, a touch warm)
VINE  = "#5a6e3c"   # vine off the solid back-wall side face (high distance_decay only)

# =====================================================================================
# 1) GROUND COURSE (3x3, y0): packed earth + cobble scatter; front-centre cell = bare path.
#    Sits IN the path -- earthworks-free, the traveller stands flush on the road.
# =====================================================================================
S.box(0, 0, 0, 3, 3, 1, COBBS, seam=True)            # cobble scatter pad under the niche (back two rows + sides)
S.box(1, 2, 0, 1, 1, 1, PATH)                        # front-centre cell = bare dirt_path (stand flush on the road)

# =====================================================================================
# 2) BACK WALL (3 wide x 3 tall, y1..3): mossy_cobblestone field, 1 cobblestone + 1 mossy_stone_
#    bricks hash-scattered so it reads HAND-STACKED, not modelled. Back row at z=0 (BACK).
# =====================================================================================
S.box(0, 0, 1, 3, 1, 3, MOSS, seam=True)             # mossy_cobblestone back-wall field, full 3-tall
S.box(0, 0, 1, 1, 1, 1, COBB)                        # 1 plain-cobble scatter (lower-left, hand-stacked read)
S.box(2, 0, 2, 1, 1, 1, MSB)                         # 1 mossy_stone_bricks scatter (upper-right dressed note)

# =====================================================================================
# 3) THE NICHE -- centre back-wall block at y1..2 recessed 1 deep -> a flat-topped lit nook
#    (NO arch claim at this tier). Opens on the FRONT (z, viewer) face. Floor = a slab ledge.
# =====================================================================================
# side jambs + lintel framing the cavity (solid mossy cobble around the recess)
S.box(0, 0, 1, 1, 1, 2, MOSS, seam=True)             # left jamb (x0)
S.box(2, 0, 1, 1, 1, 2, MOSS, seam=True)             # right jamb (x2)
S.box(0, 0, 3, 3, 1, 1, MOSS)                        # lintel course over the nook (top of the recess)
# recessed nook interior -- pushed BACK to z0.6 so it reads cut-IN behind the front wall plane
S.box(1, 0.6, 1, 1, 0.4, 2, NICHE)                   # deep shadow back panel of the cavity
S.box(1, 0.55, 1, 1, 0.45, 0.3, LEDGE)               # stone_brick_slab offering ledge (the flame stands on this)

# =====================================================================================
# 4) SIDE FRAMING -- two waist-high cobblestone_wall posts flanking the nook so it is BRACKETED,
#    not a flat hole. Posts rise off the wall top (grounded, vertical stack).
# =====================================================================================
S.box(0.15, 0.1, 4, 0.7, 0.7, 1, WALLP)             # left cobblestone_wall post (waist-high, on the wall top)
S.box(2.15, 0.1, 4, 0.7, 0.7, 1, WALLP)             # right cobblestone_wall post

# =====================================================================================
# 5) GABLE CAP (y4): a tiny peaked hood over the nook -- two cobblestone_stairs meeting at a
#    1-block mossy_stone_bricks ridge centre. Each stair rests on the lintel course beneath it.
# =====================================================================================
S.box(0.1, 0.1, 4, 0.85, 0.85, 0.5, COBB)           # left stair half (rises toward centre, grounded on lintel)
S.box(2.05, 0.1, 4, 0.85, 0.85, 0.5, COBB)          # right stair half (mirrored)
S.box(1, 0.1, 4.5, 1, 0.85, 0.5, MSB)               # mossy_stone_bricks ridge keystone (the little peak)

# =====================================================================================
# 6) VINE -- one vine on the SIDE FACE of the solid back-wall block beside the nook (a full
#    vertical face = valid attachment). Present only at high distance_decay; drawn here.
# =====================================================================================
S.box(2.98, 0.2, 1.2, 0.06, 0.5, 1.6, VINE)         # vine hanging on the east-wall full face (grounded read)

# =====================================================================================
# ACCENTS -- the single lit flame in the niche (candle 2/3 of spawns; standing lantern 1/3).
#            One light: the lit mossy niche reads as a PLACE even at the smallest tier.
# =====================================================================================
S.accent(1.5, 0.6, 1.5, "glow", "#ffd47a", r=2.6)    # lit candle in the recessed nook (the flame-in-a-niche focal)

S.label(1.5, 0.1, 4.6, "tiny cobblestone-stairs gable hood + mossy ridge")
S.label(2.2, 0.1, 4.2, "waist-high cobblestone-wall posts bracket the nook")
S.label(1.5, 0.55, 1.6, "recessed lit niche -- one candle on a slab ledge (the only light)")
S.label(0, 0, 2.0, "mossy_cobblestone field, hand-stacked (1 cobble + 1 mossy-brick scatter)")
S.label(1.5, 2, 0.4, "front-centre cell left as bare dirt path -- sits IN the road")

out = S.svg(title="Wayshrine R1 (Trail) -- mossy lantern-niche under a tiny stone gable, one lit flame, unlit-baseline",
            size_label="3x3 foot * h4 * 1 candle (ladder floor -- a hand-stacked wayside niche the size of a doorway)",
            label_w=352)
open("detail_svg/wayshrine_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/wayshrine_trail.svg | bytes", len(out.encode()))
