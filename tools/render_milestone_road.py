"""Milestone ROAD (R3) -> detail_svg/milestone_road.svg.
Per deco_catalog_v2.json id 'milestone' tier Road (footprint 3x3 stepped base + a separate lantern
post beside it ~3x4, height 5): the real jump. The board gets its first FOOTPRINT -- a low stepped
3x3 plinth you can climb (cobblestone centre, stone_brick_stairs facing out on the 4 edges, cobble
corners), a chiseled_stone_bricks pedestal (y1, the carved marker-stone), a stone_brick_wall host
(y2) lifting the way_sign with TWO arrow boards (toward settlement + back-the-way), corner wall-post
stubs, AND -- the headline -- the FIRST LIGHT: a dedicated GROUNDED lantern post one cell off the
pad toward the road (cobblestone footing, 2-tall cobblestone_wall, a hanging lantern under a
stone_brick_slab soffit). Plus one randomized roadside satellite prop (here: a campfire on a slab).

ONE big new idea over Path: a real laid FOOTPRINT + its OWN dedicated LIGHT + a second arrow board
(two-way wayfinding). First lit rung of the ladder.

Same wnl_milestone data builder + way_sign heart as render_milestone.py (Great Road top). Grid: x
right, z back->front (z=0 back), y up. Road-facing FRONT = high-z (south) + high-x (east); the
plaque + lantern post turned to that front so the viewer reads them. Inspiration (studied only,
NOTHING copied): Roman milestone-on-a-stepped-base + wayside-shrine lantern read; Supplementaries
way_sign integration is the credit. Geometry/arrangement original WNL. Vanilla-buildable, grounded.
"""
from iso_render import Iso

S = Iso(U=21)

# --- palette (literal) : WIDE-CONTRAST ladder so every material reads as itself --------------
# The pad steps DARK stair skirt -> mid cobble field so each step casts its own shadow band; the
# chiseled pedestal is the BRIGHTEST stone (the carved marker-stone reads proud); the host wall is a
# mid dressed grey; the board stays saturated warm oak (the constant heart). The lantern post is a
# cooler cobble so it frames-and-recedes; its lantern is the one warm glow (first lit tier). Moss +
# cracked accents are a green / pale-warm note for weathering. Path surface a flat dim earth band.
PADF   = "#8a8276"   # 3x3 cobblestone pad field (mid grey, the walked surface)
STAIR  = "#6f685d"   # stone_brick_stairs skirt on the 4 pad edges (DARK -> each step casts a shadow band)
PADCOR = "#9b9488"   # cobblestone pad corners (a touch lighter -> crisp corner read)
MOSS   = "#6f7d56"   # mossy_cobblestone weathered note (one pad cell + a skirt stone)
PED    = "#c2bcae"   # chiseled_stone_bricks PEDESTAL (the carved marker-stone, BRIGHTEST stone -> reads proud)
PEDF   = "#3f3b33"   # the recessed carved face on the pedestal, turned to the road (dark recess)
WALL   = "#9a9384"   # stone_brick_wall host post (mid dressed grey)
WALLD  = "#7e7869"   # the host wall's shaded notch band (reads turned)
BOARD  = "#a9712f"   # supplementaries way_sign board (saturated warm oak -> the constant heart, pops off stone)
BOARDH = "#c08a44"   # way_sign board sunlit face (lighter timber, catches the eye)
POST   = "#4f3518"   # board batten / sign-nail + corner-stub cap edge (dark timber/stone line)
LPOST  = "#7c756a"   # the dedicated lantern POST -- cobblestone_wall, COOLER -> frames + recedes vs the marker
LFOOT  = "#6f685d"   # the lantern post's cobblestone footing block (dark, grounded)
SOFF   = "#5c574e"   # stone_brick_slab soffit the lantern hangs beneath (dark -> the hung lantern reads)
LANT   = "#ffd47a"   # lantern glow (FIRST lit tier)
CAMP   = "#b8552a"   # campfire ember (the randomized satellite prop -- a warm roadside note)
CAMPL  = "#8a8276"   # the stone slab the campfire sits on (grounded)
PATH   = "#7a7066"   # the trodden path shoulder band (dim packed earth)

# =====================================================================
# PATH SURFACE -- a thin dim band of trodden ground under everything, so the pad + lantern post +
# satellite all sit IN real walked ground (the corners of the pad sink slightly into it). y -0.25..0.
# =====================================================================
S.box(-2.4, -1.0, -0.25, 6.6, 5.2, 0.25, PATH)        # the trodden path shoulder (flush ground band)

# =====================================================================
# COURSE 0 (y0) -- the stepped 3x3 PAD: cobblestone centre, stone_brick_stairs facing OUT on the 4
# edge cells (a low pad you can climb), cobblestone corners. The DARK stair skirt under the bright
# field = each step casts its own shadow band so the climbable pad reads. One cell weathered moss.
# Foot of the pad sunk slightly into the path band (rooted). (catalog COURSE 0)
# =====================================================================
S.box(0, 0, -0.1, 3, 3, 0.9, STAIR, seam=True)        # the full 3x3 riser block (the step's vertical face, dark)
S.box(0.5, 0.5, 0.78, 2, 2, 0.16, PADF)               # the inset cobble tread/field on top (the walked surface, brighter)
for (cx, cz) in [(0,0),(2,0),(0,2),(2,2)]:            # 4 cobblestone CORNERS standing proud of the stair skirt
    S.box(cx, cz, -0.1, 1, 1, 1.05, PADCOR)
    S.box(cx, cz, 0.95, 1, 1, 0.1, PADF)              # crisp cap on each corner
S.box(2, 0, -0.1, 1, 1, 1.05, MOSS)                   # ONE corner weathered to mossy_cobblestone (distance_decay)

# =====================================================================
# COURSE 1 (y1) -- the chiseled_stone_bricks PEDESTAL, single centre block on the pad: the carved
# marker-stone, the first decorative masonry. BRIGHTEST stone so it reads proud; the carved face is
# recessed and turned to the road FRONT (high-z). (catalog COURSE 1)
# =====================================================================
S.box(1, 1, 0.9, 1, 1, 1.0, PED, seam=True)           # chiseled pedestal block (the carved marker-stone)
S.box(1.08, 1.92, 1.18, 0.84, 0.1, 0.55, PEDF)        # the recessed carved face turned to the road (dark recess on the FRONT)

# =====================================================================
# COURSE 2 (y2) -- the HOST: a stone_brick_wall on the pedestal lifting the way_sign above the pad,
# with TWO arrow boards now (toward settlement = front/down-road, + back-the-way). The wall is slim
# (0.55) centred on the pedestal. (catalog COURSE 2)
# =====================================================================
S.box(1.22, 1.22, 1.9, 0.56, 0.56, 1.0, WALL, seam=True)  # stone_brick_wall host post on the pedestal
S.box(1.22, 1.22, 2.55, 0.56, 0.56, 0.1, WALLD)           # shaded notch band (the wall reads turned)
# board A -- toward-settlement arrow, faces the road FRONT (high-z), inner edge flush to the post
S.box(1.04, 1.5, 2.18, 0.92, 0.14, 0.62, BOARD)
S.box(1.04, 1.5, 2.18, 0.92, 0.05, 0.62, BOARDH)         # sunlit batten strip (catches the eye)
S.box(1.04, 1.5, 2.10, 0.92, 0.14, 0.07, POST)           # lower batten (dark timber edge)
# board B -- back-the-way arrow on the side face (high-x / east), perpendicular to board A
S.box(1.5, 1.04, 2.18, 0.14, 0.92, 0.62, BOARD)
S.box(1.5, 1.04, 2.10, 0.14, 0.92, 0.07, POST)           # its lower batten
S.box(1.42, 1.42, 2.18, 0.16, 0.16, 0.62, POST)          # the shared nail/host strut at the post (no gap, both boards hosted)

# =====================================================================
# CORNER WALL-POST STUBS -- 1-tall cobblestone_wall stubs at two pad corners (front-facing), reading
# as little corner posts framing the pedestal. Grounded on the pad corners. (catalog DETAIL)
# =====================================================================
S.box(0.28, 2.28, 0.95, 0.44, 0.44, 0.7, LPOST)          # front-west corner stub
S.box(0.28, 2.28, 1.62, 0.44, 0.44, 0.08, POST)          # its dark cap
# (front-east corner is occupied by the lantern-post approach side; one stub keeps it asymmetric)

# =====================================================================
# ADJACENT LANTERN POST (separate column, 1 cell off the pad toward the road FRONT) -- the FIRST
# LIGHT. y0 cobblestone footing, y1-y2 cobblestone_wall (2 tall), y3 a hanging lantern UNDER a
# stone_brick_slab[type=top] soffit keyed onto the wall top (grounded -- the slab is what the lantern
# hangs from, never floating). Placed front-east so it lights the carved face. (catalog ADJACENT LANTERN POST)
# =====================================================================
LX, LZ = 4.0, 2.0
S.box(LX, LZ, -0.1, 1, 1, 1.0, LFOOT, seam=True)         # cobblestone footing block (grounded in the path)
S.box(LX+0.22, LZ+0.22, 0.9, 0.56, 0.56, 2.0, LPOST, seam=True)  # cobblestone_wall, 2 tall (the lantern column)
S.box(LX+0.22, LZ+0.22, 1.6, 0.56, 0.56, 0.1, WALLD)     # shaded notch band on the lantern post
S.box(LX+0.1, LZ+0.1, 2.9, 0.8, 0.8, 0.28, SOFF)         # stone_brick_slab[type=top] soffit on the wall top (the lantern hangs from THIS)

# =====================================================================
# RANDOMIZED SATELLITE PROP -- here the {campfire on a stone slab} pick (alt: a boundary stone, or a
# 2-block mini-cairn). Set 1-2 cells out on the OTHER side of the pad, grounded on a slab. (catalog DETAIL)
# =====================================================================
S.box(-1.6, 1.5, -0.1, 1, 1, 0.32, CAMPL)               # the stone slab base (grounded in the path)
S.box(-1.45, 1.65, 0.22, 0.7, 0.7, 0.28, CAMP)          # the lit campfire on the slab (a warm roadside note)

# =====================================================================
# ACCENTS -- the single lantern (first lit tier) + the campfire ember glow.
# =====================================================================
S.accent(LX+0.5, LZ+0.5, 2.75, "glow", LANT, r=2.4)     # the dedicated-post lantern (FIRST light)
S.accent(-1.1, 2.0, 0.45, "glow", "#ffb060", r=1.6)     # the campfire ember glow (soft warm satellite note)

S.label(LX+0.5, LZ+0.5, 2.9, "FIRST lantern — dedicated grounded post (slab soffit), lights the face")
S.label(1.5, 1.5, 2.5,  "TWO arrow boards now (toward settlement + back-the-way) — two-way wayfinding")
S.label(1.5, 1.5, 1.5,  "chiseled_stone_bricks pedestal — the carved marker-stone, face to the road")
S.label(1.5, 1.5, 0.4,  "stepped 3×3 plinth you can climb (stair skirt + cobble corners)")
S.label(-1.1, 2.0, 0.4, "1 randomized satellite (campfire on a slab / boundary stone / mini-cairn)")

out = S.svg(title="Milestone R3 (Road) — first FOOTPRINT + first LIGHT: stepped 3×3 pad, chiseled pedestal, two-way sign, lantern post",
            size_label="3×3 pad + lantern post · h5 · 1 lantern (the road's first laid, lit, two-way marker)",
            label_w=372)
open("detail_svg/milestone_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/milestone_road.svg | bytes", len(out.encode()))
