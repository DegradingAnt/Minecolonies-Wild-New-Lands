"""Menhir HIGHWAY (R4) -> detail_svg/menhir_highway.svg.
Per deco_catalog_v2.json id 'menhir' tier highway (footprint 5x5 dressed apron under a single
dressed-but-rough shaft, foot girth 2x2 tapering to 1x1, height 11): the BIG non-linear LEAP below
the great_road monument. trail->road crept up; highway nearly doubles (6->11), gains a 25-block
dressed flagstone apron with kerb posts, a broad 2x2 rough HEFT-FOOT, a DRESSED-but-rough shaft,
AND its first carving + first LIGHT (one lantern recessed 1 block DEEP behind a carved socket).
From 'old stone' to 'worked monument' -- still ONE leaning monolith (no second object).
massing: a 5x5 flagstone apron (mix of full blocks + slab + cobble, rim sunk + feathered) with 4
kerb corner posts; a 2x2 rough heft-foot (y1-y2) so the tall stone has weight; 6 dressed core
courses (y3 still rough-skinned, y4-y8 clean dressed) pulling 2x2 -> 1x1 via slab/stair shoulder
wedges with a faint ~1-block lean; THE FACE (y4-y6 road side) = a carved channel-and-socket --
a chiseled socket at y5 centre with a chiseled groove block directly above (y6) + below (y4), the
ONE lantern set 1 block DEEP behind the socket (glow leaks, the block face still reads); 2 core head
courses (y9-y10) narrowing to a weathered crown pulled to a corner. STRICTLY abstract incised
geometry (channel + socket), never a literal cross/face/rune/glyph. Remote: cracked/mossy swap +
a structure_void chip knocked out of a hash face + heavier vine.
Originality/inspiration (FORM/technique only, credited CREDITS.md, no assets/NBT copied): neolithic
single standing stones (menhirs) + medieval wayside boundary/way-stones for the tooled channel-and-
socket face + the dressed forecourt. Same wnl_menhir data builder as render_menhir.py (great_road
top, h16/3 lanterns) -- one step less grand; hashes lean/taper/decay/palette/chip per spawn.
ISO: road-facing FRONT = high-z (south) + high-x (east) -- the carved socket + lantern read on that front."""
from iso_render import Iso

S = Iso(U=17, occlusion=True)

# palette (literal) -- WIDE-CONTRAST 3-zone ladder (cf. render_menhir top):
#   ZONE A (the APRON) = cool dressed greys, grounded + receding.
#   ZONE B (the SHAFT) = warmer DRESSED near-white stone-brick (the worked standing stone, brightest).
#   ZONE C (the carved MARK + lantern) = saturated warm chiseled stone + a near-black socket throat.
APRON  = "#8e8378"   # 5x5 flagstone apron field (cool dressed grey -> the forecourt, receding base)
FLAG2  = "#a39b8d"   # apron scatter-mix lighter flagstone (full-block/slab variety so it reads laid, not poured)
RIM    = "#6f685d"   # rim sunk + feathered to grade (darkest cool -> the apron settles INTO the ground)
PACKED = "#6b5a45"   # 1-2 rim blocks left packed_mud (ages into the earth)
KERB   = "#b3ada0"   # 4 kerb corner posts (stone_brick_wall -- bright dressed, marks the apron edge)
FOOT   = "#6e6358"   # 2x2 rough heft-foot (DARK warm fieldstone -> maximum weight under the bright shaft)
ROUGH  = "#9b9488"   # the y3 rough-skinned dressed course (the join between rough foot + dressed shaft)
SHAFT  = "#ddd8cb"   # the DRESSED shaft body (near-white stone_bricks -> the worked standing stone, brightest)
SHADE  = "#b3ac9d"   # shoulder wedge / mid band (clearly darker dressed -> the taper + lean read hard)
MOSSY  = "#7d8a5a"   # mossy_stone_bricks course (remote weathering swap; green-grey)
CARVE  = "#a87b4f"   # chiseled channel surround (saturated warm tooled-stone -> the MARK leaps off the pale shaft)
GROOVE = "#6e4d31"   # the incised groove block above/below the socket (deep warm brown -> reads as shadow)
SOCKET = "#473524"   # the recessed socket throat behind the lantern (near-black warm -> the depth read)
PACKW  = "#7a6a52"   # slab/stair shoulder wedges on the shaft (warm -> reads as the taper corbel)
VINE   = "#5e7a3a"   # vine down the shaded face (remote daylight tell)
LANT   = "#ffd47a"   # lantern glow (the FIRST lit tier -- a single recessed socket lantern)

# geometry: 5x5 apron on x0-5,z0-5. Shaft centred (2x2 foot at x2,z2). Road faces FRONT (high z).

# ----------------------------------------------------------------------------
# COURSE 0 (y0) -- 5x5 dressed flagstone APRON: laid scatter-mix + sunk feathered rim + kerb posts
# ----------------------------------------------------------------------------
S.box(0, 0, 0, 5, 5, 1, APRON, seam=True)           # 5x5 flagstone apron the stone stands before
# scatter-MIX: a few lighter full-block/slab flagstones so the apron reads LAID (a proper forecourt),
# not one poured slab. Each sits flush in the apron field.
S.box(1, 1, 1, 1, 1, 0.25, FLAG2)                   # lighter flagstone inlay
S.box(3, 1, 1, 1, 1, 0.25, FLAG2)                   # lighter flagstone inlay
S.box(2, 3, 1, 1, 1, 0.25, FLAG2)                   # lighter flagstone inlay (front area)
# rim sunk 1 + feathered to grade on the camera-facing edges (front + east) -> apron settles into ground.
S.box(0, 4, 0, 5, 1, 0.7, RIM)                      # front rim, sunk (feathered to grade)
S.box(4, 0, 0, 1, 5, 0.7, RIM)                      # east rim, sunk
S.box(0, 4, 0, 1, 1, 0.6, PACKED)                   # 1 front-west rim block left packed_mud (ages in)
# 4 kerb corner posts marking the apron edge (proud 1 course).
for (kx, kz) in [(0,0),(4,0),(0,4),(4,4)]:
    S.box(kx, kz, 1, 1, 1, 1, KERB, seam=True)      # stone_brick_wall kerb post

# ----------------------------------------------------------------------------
# COURSES 1-2 (y1-y2) -- 2x2 rough HEFT-FOOT (gives the 11-high stone weight at the ground)
# ----------------------------------------------------------------------------
S.box(2, 2, 1, 2, 2, 1, FOOT, seam=True)            # heft-foot lower course (broad rough base)
S.box(2, 2, 2, 2, 2, 1, FOOT, seam=True)            # heft-foot upper course

# ----------------------------------------------------------------------------
# COURSES 3-8 (y3-y8) -- the DRESSED SHAFT: 6 courses, 2x2 -> 1x1, faint lean, slab-shoulder taper
# ----------------------------------------------------------------------------
# y3 still rough-skinned (the join between the rough foot and the dressed shaft).
S.box(2, 2, 3, 2, 2, 1, ROUGH, seam=True)           # y3 rough-skinned dressed course (the join)
# y4-y6: clean dressed 2x2 core, drifting +1 x over the run (the faint lean), wedge-supported.
S.box(2, 2, 4, 2, 2, 1, SHAFT, seam=True)           # y4 dressed
S.box(2, 2, 5, 2, 2, 1, SHAFT, seam=True)           # y5 dressed (carries the carved socket on its front face)
S.box(2.3, 2, 6, 2, 2, 1, SHADE, seam=True)         # y6 shoulder wedge band, drifted +0.3 x (lean) before the 1x1 pull-in
S.box(2.0, 2.3, 6, 0.5, 0.5, 0.4, PACKW)            # slab shoulder wedge grounding the y6 drift (taper corbel)
# y7-y8: pull in to 1x1, drifted +1 x again (final lean) toward the head.
S.box(3, 3, 7, 1, 1, 1, SHAFT, seam=True)           # y7 1x1 dressed (pulled in, leaned)
S.box(3, 3, 8, 1, 1, 1, SHAFT, seam=True)           # y8 1x1 dressed

# --- THE CARVED FACE (y4-y6, road/front face of the 2x2 shaft): channel-and-socket way-mark ---
# IMPORTANT (perspective, cf. render_menhir top): the carved mark is a pure BLOCK-SWAP INTO the
# shaft's own front (south) face. The 2x2 shaft's front row is z=3 (cells z3..4 span z3->4), so the
# carved blocks are placed AT z=3 (replacing the shaft's front cells) -> they sit flush IN the face
# and depth-sort ON TOP of the shaft (higher x+z paints later) = a real tooled niche, not a stuck-on box.
# Layout, single column on the front face (x3, the road-facing-east cell of the 2x2):
#   y4 = lower groove (chiseled), y5 = the deep SOCKET throat (the lantern embers here), y6 = upper groove.
S.box(3, 3, 4, 1, 1, 1, GROOVE)                     # lower incised groove (y4)
S.box(3, 3, 5, 1, 1, 1, SOCKET)                     # the deep socket throat (y5) -- the lantern is 1-deep behind this
S.box(3, 3, 6, 1, 1, 1, CARVE)                      # upper channel surround / groove (y6 -- the warm tooled MARK)

# ----------------------------------------------------------------------------
# COURSES 9-10 (y9-y10) -- the HEAD: 2 core blocks narrowing, crown pulled to a corner
# ----------------------------------------------------------------------------
S.box(3, 3, 9, 1, 1, 1, SHADE)                      # y9 neck narrows (shoulder band)
# y10 crown pulled to the FRONT-EAST corner, asymmetric (never a flat cap), supported by y9 below-inward.
S.box(3.3, 3.3, 10, 0.85, 0.85, 0.95, MOSSY)        # weathered crown pulled to a corner (mossy remote tell)

# remote-decay tell: a vine curtain down the shaded front face + a structure_void CHIP knocked out of
# the y7 east face (battle damage). Both read in daylight (vine = no light).
S.box(3.62, 3.97, 4.2, 0.34, 0.05, 1.6, VINE)       # vine curtain on the shaft front face (remote)
S.box(3.97, 3.18, 7.15, 0.05, 0.45, 0.55, RIM)      # structure_void chip shadow on the y7 east face (knocked-out corner)

# ----------------------------------------------------------------------------
# ACCENT -- the FIRST light: one lantern recessed 1 block DEEP behind the carved socket (y5)
# ----------------------------------------------------------------------------
# the lantern embers on the SOCKET throat front face (cell x3,z3 -> front face at z=4), y5 cell.
S.accent(3.5, 4.0, 5.5, "glow", LANT, r=2.5)        # the recessed socket lantern -- the abstract mark embers at night

S.label(3.3, 3.3, 10.5, "weathered crown pulled to a corner (never a flat cap)")
S.label(3.0, 3.0, 8.2, "dressed-but-rough shaft (2x2 -> 1x1, slab-shoulder taper, faint lean)")
S.label(3.5, 4.0, 5.5, "FIRST light: ONE lantern recessed 1 block behind the carved SOCKET")
S.label(3.0, 3.0, 4.4, "carved channel-and-socket WAY-MARK (strictly abstract incised geometry)")
S.label(2.0, 2.0, 2.2, "2x2 rough heft-foot (gives the tall stone weight at the ground)")
S.label(0, 4, 1.1, "5x5 dressed flagstone apron + 4 kerb corner posts (rim sunk to grade)")

out = S.svg(title="Menhir R4 (Highway) -- the LEAP: 5x5 dressed apron, 2x2 heft-foot, 11-high dressed-but-rough shaft, carved socket way-mark + FIRST lantern",
            size_label="5x5 apron / 2x2->1x1 shaft * h11 * 1 lantern (worked monument -- the carved mark embers at night)",
            label_w=360)
open("detail_svg/menhir_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/menhir_highway.svg | bytes", len(out.encode()))
