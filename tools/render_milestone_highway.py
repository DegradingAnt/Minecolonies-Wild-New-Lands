"""Milestone HIGHWAY (R4) -> detail_svg/milestone_highway.svg.
Per deco_catalog_v2.json id 'milestone' tier Highway (footprint 5x5 two-tier stepped plinth, ~5x7
with the flanking lantern pair + a boundary stone, height 8): the BIG non-linear jump -- the first
payoff rung, directly under the Great Road monument (render_milestone.py, h14 / 4-lantern crown +
banner masts). Footprint roughly quadruples (3x3 -> 5x5) and goes TWO-TIER: a wedding-cake plinth
you climb on every side (stone_bricks fill + stone_brick_stairs skirts, chiseled corners), a
collared, slab-capped chiseled marker PEDESTAL (y2) growing a dressed multi-course BODY (y3), a
stone_brick_wall host (y4) lifting the way_sign with two arrow boards, and -- the headline -- a
SYMMETRICAL FLANKING LANTERN PAIR: two 4-tall stone_brick_wall posts at the road-facing perimeter,
each capped with an inward-leaning stone_brick_stairs[half=top] bracket with a lantern hung beneath,
framing the sign from both sides. A small civic monument.

ONE big new idea over Road: the footprint QUADRUPLES + goes two-tier (a wedding-cake you climb), the
marker grows a dressed multi-course body, and lighting goes from ONE post to a matched FLANKING PAIR.
It stops being roadside furniture and becomes a small civic monument (a real medieval market-cross base).

Same wnl_milestone data builder + way_sign heart as render_milestone.py. Grid: x right, z back->front
(z=0 back), y up. Road-facing FRONT = high-z (south) + high-x (east); the lantern pair flanks ALONG
the road on the front so the viewer reads the framed board between them. Inspiration (studied only,
NOTHING copied): Roman milliarium stepped base + medieval market-cross flanking-bracket lighting;
Supplementaries way_sign integration is the credit. Geometry/arrangement original WNL. Grounded.
"""
from iso_render import Iso

S = Iso(U=17)

# --- palette (literal) : WIDE-CONTRAST ladder so every cut-stone element reads as itself ------
# The two plinth tiers step DARK stair skirt -> mid stone_bricks field, each tier's skirt darker so
# every step casts its own shadow band (the wedding-cake reads); chiseled corners + the marker
# pedestal/body are the BRIGHTER dressed stone so the marker pops above the plinth; the collar is a
# mid band; the host wall a mid grey; the board the constant saturated warm oak. The flanking lantern
# posts are a COOLER slate so the pair frames-and-recedes; their lanterns are the two warm glows
# (escalated from Road's single). Moss + cracked accents weather it. Path surface a dim earth band.
PBASE  = "#7a746a"   # 5x5 plinth base field (stone_bricks, dressed mid grey)
STAIR1 = "#5f5a51"   # tier-1 stone_brick_stairs skirt (DARKEST -> the lowest step's shadow band)
PSTEP  = "#867f74"   # 3x3 tier-2 plinth field (a clear step brighter than the base)
STAIR2 = "#6b665c"   # tier-2 stone_brick_stairs skirt (dark, but lighter than tier-1 -> the climb reads)
TRIM   = "#b3ada0"   # smooth stone_brick_slab step-tread / trim lip (the bright nosing the climb reads off)
CORNER = "#8f7f63"   # chiseled_stone_bricks plinth corners (warm dressed accent -> crisp corners)
PED    = "#c6c0b2"   # chiseled_stone_bricks marker PEDESTAL + BODY (BRIGHTEST dressed stone -> the marker pops)
PEDF   = "#3f3b33"   # the recessed carved face on the marker body, turned to the road (dark recess)
COLLAR = "#9a9384"   # stone_brick_wall collar ring around the pedestal (mid band)
COLCAP = "#b3ada0"   # stone_brick_slab cap on the collar (bright, reads the slab cap)
WALL   = "#9a9384"   # stone_brick_wall host post (mid dressed grey)
WALLD  = "#7e7869"   # host wall shaded notch band (reads turned)
BOARD  = "#a9712f"   # supplementaries way_sign board (saturated warm oak -> the constant heart)
BOARDH = "#c08a44"   # way_sign board sunlit face (lighter timber, catches the eye)
POST   = "#4f3518"   # board batten / sign-nail edge (dark timber line)
MAST   = "#878d95"   # the flanking lantern POSTS -- stone_brick_wall, COOLER slate -> the pair frames + recedes
MASTD  = "#6f747b"   # the lantern post shaded notch band (reads turned)
BRACK  = "#a7a299"   # the inward stone_brick_stairs[half=top] bracket the lantern hangs from (lighter -> the bracket reads proud)
LANT   = "#ffd47a"   # lantern glow (now a PAIR)
MOSS   = "#6f7d56"   # mossy_stone_bricks weathered note (a couple of plinth cells)
CRACK  = "#9a9078"   # cracked_stone_bricks weathered note (distance_decay)
BSTONE = "#8f7f63"   # chiseled_stone_bricks boundary stone (the randomized satellite, 1-2 cells out)
PATH   = "#7a7066"   # the trodden path shoulder band (dim packed earth)

def plinth_tier(x0, z0, side, y, field, skirt, h=1.0):
    """A stepped plinth tier: a DARK stair-skirt riser ring at y carrying an inset brighter FIELD on
    top, so each wedding-cake step casts its own shadow band + a bright TRIM nosing reads the climb."""
    S.box(x0, z0, y, side, side, h, skirt)                          # the dark riser ring (the step's vertical face)
    S.box(x0+0.5, z0+0.5, y+h-0.12, side-1.0, side-1.0, 0.12, TRIM) # bright slab-tread nosing lip (reads the climb)
    S.box(x0+0.5, z0+0.5, y+h, side-1.0, side-1.0, 0.16, field)     # the inset field/tread surface on top

# =====================================================================
# PATH SURFACE -- a dim band of trodden ground under everything (plinth, lantern pair, boundary
# stone all sit IN real walked ground; the plinth foot sinks slightly into it). y -0.25..0.
# =====================================================================
S.box(-2.2, -1.4, -0.25, 9.4, 8.0, 0.25, PATH)        # the trodden path shoulder (flush ground band)

# =====================================================================
# COURSE 0 (y0) -- the 5x5 base: stone_bricks fill, stone_brick_stairs skirt facing OUT on all 16
# perimeter cells (a full climbable step on every side), chiseled corners. Foot sunk into the path
# band (rooted). (catalog COURSE 0)
# =====================================================================
plinth_tier(0, 0, 5, -0.1, PBASE, STAIR1)
for (cx, cz) in [(0,0),(4,0),(0,4),(4,4)]:            # chiseled_stone_bricks CORNERS standing proud of the skirt
    S.box(cx, cz, -0.1, 1, 1, 1.05, CORNER, seam=True)
    S.box(cx, cz, 0.95, 1, 1, 0.08, TRIM)             # crisp bright cap on each corner
S.box(4, 0, -0.1, 1, 1, 1.05, MOSS)                   # ONE corner weathered mossy (distance_decay)
S.box(0, 3, 0.78, 1, 1, 0.18, CRACK)                  # a cracked-brick weathered tread cell (side, distance_decay)

# =====================================================================
# COURSE 1 (y1) -- the 3x3 inset, second step of the wedding-cake: stone_bricks field + stairs skirt
# facing out, centre cell open for the pedestal. (catalog COURSE 1)
# =====================================================================
plinth_tier(1, 1, 3, 0.9, PSTEP, STAIR2)

# =====================================================================
# COURSE 2 (y2) -- the marker PEDESTAL: a chiseled_stone_bricks 1x1 with a stone_brick_wall collar on
# the 4 cells around it + a stone_brick_slab cap on the collar. (catalog COURSE 2)
# =====================================================================
S.box(2, 2, 2.06, 1, 1, 1.0, PED, seam=True)          # chiseled pedestal core
for (cx, cz) in [(1,2),(3,2),(2,1),(2,3)]:            # stone_brick_wall collar ring (slim, on the 4 sides)
    S.box(cx+0.22, cz+0.22, 2.06, 0.56, 0.56, 0.85, COLLAR)
    S.box(cx+0.1, cz+0.1, 2.91, 0.8, 0.8, 0.16, COLCAP)   # stone_brick_slab cap on each collar block (the slab cap reads)

# =====================================================================
# COURSE 3 (y3) -- the marker BODY tapers up: a chiseled_stone_bricks dressed course (the carved-face
# read), recessed face turned to the road FRONT (high-z). (catalog COURSE 3)
# =====================================================================
S.box(2, 2, 3.06, 1, 1, 1.0, PED, seam=True)          # the dressed marker body course (carved-face read)
S.box(2.08, 2.92, 3.32, 0.84, 0.1, 0.55, PEDF)        # the recessed carved face turned to the road (dark recess on the FRONT)

# =====================================================================
# COURSE 4 (y4) -- the HOST: a stone_brick_wall on the marker body, framed + lifted, carrying the
# way_sign with two arrow boards (settlement + back-the-way). (catalog COURSE 4)
# =====================================================================
S.box(2.22, 2.22, 4.06, 0.56, 0.56, 1.0, WALL, seam=True)  # stone_brick_wall host post
S.box(2.22, 2.22, 4.7, 0.56, 0.56, 0.1, WALLD)             # shaded notch band (reads turned)
# board A -- toward-settlement arrow, faces the road FRONT (high-z), inner edge flush to the post
S.box(2.04, 2.5, 4.34, 0.92, 0.14, 0.62, BOARD)
S.box(2.04, 2.5, 4.34, 0.92, 0.05, 0.62, BOARDH)          # sunlit batten strip (catches the eye)
S.box(2.04, 2.5, 4.26, 0.92, 0.14, 0.07, POST)            # lower batten (dark timber edge)
# board B -- back-the-way arrow on the side face (high-x / east), perpendicular to board A
S.box(2.5, 2.04, 4.34, 0.14, 0.92, 0.62, BOARD)
S.box(2.5, 2.04, 4.26, 0.14, 0.92, 0.07, POST)            # its lower batten
S.box(2.42, 2.42, 4.34, 0.16, 0.16, 0.62, POST)           # shared nail/host strut at the post (no gap)

# =====================================================================
# FLANKING LANTERN PAIR -- two matching 4-tall stone_brick_wall posts on OPPOSITE tier-1 corners that
# face ALONG the road, placed at the screen-LEFT and screen-RIGHT extremes (same depth) so they FRAME
# the marker symmetrically WITHOUT occluding the carved board between them (same technique the Great
# Road masts use). Each is capped with an inward-leaning stone_brick_stairs[half=top] bracket toward
# the marker, with a lantern hung BENEATH the bracket: grounded on the tier-1 step, the bracket back
# flush to the post -> supported, never floating. Two lights framing the sign from both road-facing
# sides (escalated from Road's single post). (catalog FLANKING LANTERN PAIR)
# Left post (1,4)->screenX -3 ; right post (4,1)->screenX +3 ; both (x+z)=5 -> symmetric, no occlude.
# =====================================================================
LPOS = [(1.0, 3.7, +1), (3.7, 1.0, -1)]               # (x, z, inward-bracket x-direction); opposite corners, screen extremes
for (mx, mz, bdir) in LPOS:
    S.box(mx, mz, 0.9, 0.7, 0.7, 4.0, MAST, seam=True)        # 4-tall stone_brick_wall post (grounded on tier-1)
    S.box(mx, mz, 2.6, 0.7, 0.7, 0.12, MASTD)                 # a shaded mid notch band (post reads turned)
    # inward stair bracket (half=top) reaching toward the marker centre, back flush against the post top
    bx = mx + (0.7 if bdir > 0 else -0.4)                     # bracket reaches inward (toward the marker)
    S.box(bx, mz+0.1, 4.62, 0.5, 0.5, 0.26, BRACK)           # the inward stair bracket soffit (the lantern hangs from THIS)

# =====================================================================
# RANDOMIZED SATELLITE -- a single chiseled_stone_bricks boundary stone set 1-2 cells out from the
# plinth (here on the back-west side), grounded in the path. (catalog DETAIL)
# =====================================================================
S.box(-1.6, 1.0, -0.1, 1, 1, 1.2, BSTONE, seam=True)  # chiseled boundary stone (1-2 cells out)
S.box(-1.6, 1.0, 1.1, 1, 1, 0.16, TRIM)               # its bright slab cap

# =====================================================================
# ACCENTS -- the flanking lantern PAIR (escalated from Road's one) + a soft fill reading the front
# carved face.
# =====================================================================
S.accent(1.85, 4.05, 4.55, "glow", LANT, r=2.3)       # screen-left flanking lantern (under its inward bracket)
S.accent(3.65, 1.85, 4.55, "glow", LANT, r=2.3)       # screen-right flanking lantern (under its inward bracket)
S.accent(2.5, 3.0, 3.55, "glow", "#cfe8e2", r=1.7)    # soft fill reading the front carved face

S.label(3.65, 1.85, 4.8, "SYMMETRICAL flanking lantern PAIR — inward stair brackets frame the sign")
S.label(2.5, 2.5, 4.6,  "stone_brick_wall host — two arrow boards (settlement + back-the-way)")
S.label(2.5, 2.5, 3.4,  "collared, slab-capped chiseled marker body — carved face to the road")
S.label(0.5, 1.0, 1.8,  "two-tier stepped 5×5 → 3×3 wedding-cake plinth (climb on every side)")
S.label(-1.6, 1.0, 1.4, "1 randomized boundary stone, set 1–2 cells out (+ optional rope-line)")

out = S.svg(title="Milestone R4 (Highway) — small civic monument: two-tier 5×5 wedding-cake plinth, collared marker body, flanking lantern PAIR",
            size_label="5×5 two-tier plinth · h8 · 2 lanterns (one step under the Great Road monument)",
            label_w=378)
open("detail_svg/milestone_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/milestone_highway.svg | bytes", len(out.encode()))
