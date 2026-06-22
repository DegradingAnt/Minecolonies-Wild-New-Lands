"""Milestone PATH (R2) -> detail_svg/milestone_path.svg.
Per deco_catalog_v2.json id 'milestone' tier Path (footprint 1x1 base plinth + 3x3 trodden skirt,
height 4): a small-but-real jump from Trail. The board no longer stabs into dirt -- it stands ON a
made cobblestone base block, hosted on a squared-up cobblestone_wall stone post (2 tall, y1-y2),
with the way_sign attaching at y2. A modest 3x3 trodden cobble/gravel skirt appears at the foot.
First hint of masonry; still tiny + UNLIT (the big leaps are saved for Highway / Great Road).

ONE new idea over Trail: the found wood fence becomes a BUILT stone footing -- a made base block +
a stone host-post + a modest stone foot. Unmistakably built, not found. Light is still none (the
non-linear ladder keeps Trail/Path humble).

Same wnl_milestone data builder + same way_sign functional heart as render_milestone.py (Great Road
top). Grid: x right, z back->front (z=0 back), y up. Road-facing FRONT = high-z (south) + high-x.
Inspiration (studied only, NOTHING copied): the wayside post-on-a-footing folk form; Supplementaries
way_sign integration is the credit. All geometry/arrangement original WNL. Vanilla-buildable, grounded.
"""
from iso_render import Iso

S = Iso(U=25)

# --- palette (literal) : WIDE-CONTRAST ladder so every material reads as itself --------------
# The base + host-post are dressed cobble (the new masonry note), stepped DARK base -> mid post so
# the made footing reads as a climbing stack; the way_sign board stays the saturated warm oak (the
# constant heart, popping off the stone); the skirt steps mid cobble / pale gravel / green moss so
# the trodden foot reads by color. Path surface is a flat dim earth band, like Trail.
BASEB  = "#6f685d"   # cobblestone BASE block, set flush into the surface (dark dressed stone -> the made footing reads heavy)
WALL   = "#8a8276"   # cobblestone_wall host post (mid grey -> a clear step lighter than the base, the post pops)
WALLD  = "#6f685d"   # the wall post's shaded notch band (post reads turned/round, not a plain prism)
MOSS   = "#6f7d56"   # mossy_cobblestone weathered note (on the base + a skirt stone)
BOARD  = "#a9712f"   # supplementaries way_sign board (saturated warm oak -> the constant heart, pops off stone)
BOARDH = "#c08a44"   # way_sign board sunlit face (lighter timber, catches the eye)
POST   = "#4f3518"   # board batten / sign-nail edge (dark timber line)
PATH   = "#7a7066"   # the trodden path shoulder band the base is set into (dim packed earth)
SKIRT  = "#837b6f"   # trodden cobble skirt stones (a touch lighter than base -> the foot reads as loose, walked cobble)
GRAVEL = "#9a948a"   # gravel skirt cells (pale loose stone, clearly not the dressed base)

# =====================================================================
# PATH SURFACE -- a thin dim band of trodden ground (the base block sits flush INTO it, the skirt
# half-sunk into it -> everything sits in real walked ground, not on void). y -0.25..0.
# =====================================================================
S.box(-1.5, -1.1, -0.25, 4.2, 4.2, 0.25, PATH)        # the trodden path shoulder (flush ground band)

# =====================================================================
# GROUND SCATTER / 3x3 TRODDEN SKIRT (y0) -- a modest 3x3 foot of loose cobble + gravel + a moss
# note half-sunk into the path band, irregular with a couple of cells left bare ground. Each stone
# ABUTS the base block or chains to a neighbour (a trodden foot, never floating). (catalog GROUND SCATTER)
# =====================================================================
S.box(-0.95, 0.05, 0, 1, 1, 0.42, SKIRT)              # west cobble -- OVERLAPS the base west face (grounded)
S.box( 0.05, 1.0,  0, 1, 1, 0.4,  GRAVEL)             # front gravel -- abuts the base front face
S.box( 0.98, 0.5,  0, 0.95, 0.95, 0.38, SKIRT)        # east cobble -- abuts the base east face
S.box(-0.7, 1.0,   0, 0.85, 0.85, 0.34, MOSS)         # front-west moss note -- touches the west cobble AND the front gravel (chained)
S.box( 0.5, -0.85, 0, 0.9, 0.9, 0.36, GRAVEL)         # back gravel -- abuts the base back face (one back cell filled; corners left bare)

# =====================================================================
# COURSE 0 (y0) -- the made BASE block: a single cobblestone set FLUSH into the surface. The post
# now stands ON something built, not stabbed in dirt. Foot sunk slightly into the path band (rooted).
# =====================================================================
S.box(0, 0, -0.15, 1, 1, 1.0, BASEB, seam=True)       # cobblestone base block, set into the ground (the made footing)
S.box(0.0, 0.62, 0.78, 1, 0.0, 0.001, MOSS)           # a touch of moss in the front joint of the base (weathered read; flush, no mass)

# =====================================================================
# COURSE 1-2 (y1-y2) -- the HOST POST: a cobblestone_wall squared up on the base, 2 tall, reading as
# a little stone footing-post. The way_sign attaches at y2. A wall is slimmer than a full block ->
# drawn as a 0.55 column centred on the base. (catalog COURSE 1 + COURSE 2)
# =====================================================================
S.box(0.22, 0.22, 0.85, 0.56, 0.56, 2.0, WALL, seam=True)   # cobblestone_wall host post (2 tall), squared on the base
S.box(0.22, 0.22, 1.55, 0.56, 0.56, 0.12, WALLD)            # shaded notch band mid-post (the wall reads turned, not a plain prism)

# =====================================================================
# WAY_SIGN BOARD (y2) -- the Supplementaries way_sign attaches UPRIGHT to the wall post at y2, turned
# to the road FRONT (high-z) with one down-road arrow. Inner edge flush to the post -> never floating.
# FALLBACK = oak_sign on an oak_fence top segment swapped for the upper wall block (still post-hosted).
# =====================================================================
S.box(0.04, 0.5, 2.18, 0.92, 0.14, 0.66, BOARD)       # the way_sign board, inner edge flush to the post (faces front/down-road)
S.box(0.04, 0.5, 2.18, 0.92, 0.05, 0.66, BOARDH)      # sunlit batten strip on the board front (catches the eye)
S.box(0.04, 0.5, 2.10, 0.92, 0.14, 0.07, POST)        # board lower batten (dark timber edge so the plaque reads)
S.box(0.42, 0.5, 2.18, 0.14, 0.14, 0.66, POST)        # the nail/host strut joining board to the wall post (no gap)

S.label(0.5, 0.5, 2.5,  "Supplementaries way_sign — one down-road arrow (now lifted on a stone post)")
S.label(0.5, 0.5, 1.6,  "cobblestone_wall host post (2 tall) — a squared stone footing-post")
S.label(0.5, 0.5, 0.45, "made cobblestone BASE block, set flush into the surface (not dirt-jabbed)")
S.label(1.5, 0.5, 0.3,  "3×3 trodden cobble + gravel + moss skirt — a modest worn foot")

out = S.svg(title="Milestone R2 (Path) — board on a made stone footing + host-post + trodden cobble skirt, still unlit",
            size_label="1×1 base + 3×3 skirt · h4 · 0 lanterns (a worn footpath marker — built, not found)",
            label_w=356)
open("detail_svg/milestone_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/milestone_path.svg | bytes", len(out.encode()))
