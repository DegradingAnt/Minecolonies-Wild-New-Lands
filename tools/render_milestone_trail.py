"""Milestone TRAIL (R1, floor of the ladder) -> detail_svg/milestone_trail.svg.
Per deco_catalog_v2.json id 'milestone' tier Trail (footprint 1x1 post + 2-4 scattered ground
blocks, height 3): the humblest rung -- a single oak_fence post (biome wood) jabbed straight into
the trodden path at the road shoulder, with the Supplementaries way_sign board cantilevered off the
post at y1 (one down-road arrow, fallback = oak_sign on the same fence). The only "structure" is a
little disturbed ground: 2-4 loose blocks (coarse_dirt + a cobble + a moss note) dropped at random
adjacent cells. UNLIT, reads by silhouette in daylight. The constant heart -- the post-hosted board
-- is here at its barest; every higher tier re-frames THIS.

The way_sign is the fixed functional heart at every tier; this is it with no masonry around it.
Inspiration (studied only, NOTHING copied): the universal lone wayside post-with-a-board folk form;
the Supplementaries way_sign INTEGRATION is itself the credit. Geometry/arrangement original WNL.
Vanilla-buildable, fully grounded -- the fence is rooted in the path, the board hosted on the post,
every scatter stone abuts the post column or chains to a neighbour (a spill, never floating debris).

Same wnl_milestone data builder as render_milestone.py (Great Road top). Grid: x right, z back->front
(z=0 back), y up. The road-facing FRONT = high-z (south) + high-x (east); the board faces that front.
"""
from iso_render import Iso

S = Iso(U=26)

# --- palette (literal) : a WIDE-CONTRAST ladder so every material reads as itself -----------
# The post is warm timber (the one wood note); the board is a brighter saturated oak so the carved
# sign pops off the post; the ground scatter steps DARK earth -> mid cobble -> green moss so the
# disturbed-ground read carries by color, not just shape. Path surface is a flat dim band.
FENCE  = "#6e4a25"   # oak_fence host post (biome wood; warm mid timber)
FENCED = "#5a3c1e"   # the fence's shaded notches / lower lashing (a touch darker -> post reads turned)
BOARD  = "#a9712f"   # supplementaries way_sign board (saturated warm oak -> reads off the post)
BOARDH = "#c08a44"   # way_sign board sunlit face (lighter timber so the board catches the eye)
POST   = "#4f3518"   # board batten / sign-nail edge (dark timber line)
PATH   = "#7a7066"   # the trodden path surface the post is jabbed into (dim packed earth band)
DIRT   = "#5d4f3a"   # coarse_dirt scatter (disturbed earth -- the darkest ground note)
COBB   = "#8a8276"   # cobblestone scatter stone (mid grey, clearly a stone not earth)
MOSS   = "#6f7d56"   # moss_block / mossy_cobblestone scatter (the green weathered note)

# =====================================================================
# PATH SURFACE -- a thin dim band of trodden ground the post is jabbed INTO (so the fence reads
# rooted in a real walked path, not standing on void). Sits at y -0.25..0 under everything.
# =====================================================================
S.box(-1.4, -1.0, -0.25, 4.0, 4.0, 0.25, PATH)        # the trodden path shoulder (flush ground band)

# =====================================================================
# GROUND SCATTER (decoration, NOT a base) -- 2-4 loose blocks dropped at random adjacent y0 cells,
# half-sunk into the path band so they sit IN the land. Each ABUTS the post column or chains to a
# neighbour (a spill of disturbed ground, never isolated floating debris). Drawn here as the 4-block
# case (scatter count hashes 2-4). (catalog GROUND SCATTER)
# =====================================================================
S.box(-0.9, 0.1, 0,  1, 1, 0.55, DIRT)                # west coarse_dirt -- OVERLAPS the post west face (grounded spill)
S.box( 0.05, 1.0, 0, 1, 1, 0.5,  COBB)                # front cobblestone -- abuts the post front face
S.box( 0.95, 0.45, 0, 0.9, 0.9, 0.45, DIRT)           # east coarse_dirt -- abuts the post east face
S.box(-0.7, 1.0, 0,  0.85, 0.85, 0.4, MOSS)           # front-west moss note -- touches BOTH the dirt + cobble (chained, not isolated)

# =====================================================================
# HOST POST (y0-y1) -- a single oak_fence jabbed STRAIGHT into the path (a fence can't lean; the
# "shoved-aside" read comes from the scatter, per the catalog). Rooted: its foot sits inside the
# path band. The fence is a slim 0.45 column centred in its cell (a real fence is thin). (catalog GROUND + HOST)
# =====================================================================
S.box(0.28, 0.28, -0.2, 0.44, 0.44, 2.2, FENCE, seam=True)   # the oak_fence post, foot sunk into the path (rooted)
S.box(0.28, 0.28, 0.55, 0.44, 0.44, 0.12, FENCED)            # a shaded lashing band low on the post (post reads round/turned)

# =====================================================================
# WAY_SIGN BOARD (y1) -- the Supplementaries way_sign overlay cantilevers off the post at y1, a warm
# timber plaque turned to the road FRONT (high-z) with a single down-road arrow. The board hangs on
# the post's central element (verified buildable), its inner edge flush to the post -> never floating.
# FALLBACK (Supplementaries absent) = an oak_sign standing on this same fence -- still post-hosted.
# (catalog HOST+BOARD)
# =====================================================================
S.box(0.06, 0.5, 1.35, 0.9, 0.14, 0.62, BOARD)        # the way_sign board, inner edge flush to the post (faces front/down-road)
S.box(0.06, 0.5, 1.35, 0.9, 0.05, 0.62, BOARDH)       # sunlit batten strip on the board front (catches the eye)
S.box(0.06, 0.5, 1.28, 0.9, 0.14, 0.07, POST)         # board lower batten (a dark timber edge so the plaque reads)
S.box(0.43, 0.5, 1.35, 0.12, 0.14, 0.62, POST)        # the nail/host strut joining the board to the post (no gap)

S.label(0.5, 0.5, 1.65, "Supplementaries way_sign — one down-road arrow board (post-hosted, never free)")
S.label(0.5, 0.5, 1.0,  "single oak_fence host post (biome wood), jabbed into the trodden path")
S.label(1.4, 0.45, 0.4, "2–4 loose ground scatter (coarse_dirt + cobble + a moss note) — disturbed land")

out = S.svg(title="Milestone R1 (Trail) — lone post + nailed board in disturbed dirt, unlit, reads by silhouette",
            size_label="1×1 post + scatter · h3 · 0 lanterns (ladder floor — a hand-cut waymark, found not built)",
            label_w=352)
open("detail_svg/milestone_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/milestone_trail.svg | bytes", len(out.encode()))
