"""Menhir R5 (Great Road) detail render -> detail_svg/menhir.svg.
ONE monumental leaning standing stone (never a building, never a circle): a 7x7 stepped
dressed plinth, a 5x5 inset step carrying a FLANKING PAIR of small sentinel stones at the
front corners, a broad 3x3 heft-foot, then a single 16-high shaft that tapers 3x3 -> 2x2 -> 1x1
with a deliberate lean, a tall carved abstract channel + a deep 2-lantern recessed socket on the
road face, and a flared chiseled capstone crown haloed by a recessed lantern over a weather-broken tip.
Silhouette stays a single leaning monolith at every tier (the sentinels are a framing pair, not a ring).

Inspiration (FORM/scale study ONLY, never copied; CREDITS.md-style): neolithic single standing
stones (menhirs) for the one-stone leaning silhouette; medieval wayside boundary/way-stones for the
tooled abstract channel-and-socket face + tended plinth; betterarcheology desert_obelisk nodded only
for how a tall single-stone marker carries scale. Original geometry, all vanilla blocks, nothing copied.
"""
from iso_render import Iso

S = Iso(U=15)

# palette (literal) -- HIGH CONTRAST so every element reads as a DISTINCT material.
# Strategy: split the build into 3 value-zones that never touch in tone so adjacent
# surfaces never blend after the renderer's 0.84/0.70 face-shading:
#   ZONE A (the PLINTH/FOOT base) = COOL mid-to-dark greys (grounded, heavy).
#   ZONE B (the SHAFT) = WARM near-white dressed stone (the one bright standing stone).
#   ZONE C (the carved MARK + crown) = saturated warm-brown + dark slate (the worked gestures).
# Every neighbouring pair is separated by >= ~0.18 in value so no two faces mush together.
PLINTH = "#9ea7ad"   # 7x7 plinth field (COOL grey -- clearly below/behind the warm shaft)
STEP   = "#737d84"   # 5x5 inset step riser (much darker cool grey -- the step now reads as a shadow course)
TREAD  = "#d6dde0"   # stair/slab tread lips (bright cool -- the worked edge catches the light, pops off the riser)
CHIS   = "#586d77"   # chiseled corner / cap blocks (deep slate-teal -- coolest accent, anchors corners)
FOOT   = "#6e6358"   # broad 3x3 rough heft-foot (DARK warm fieldstone -- maximum weight under the bright shaft)
SHAFT  = "#e7e2d6"   # the dressed shaft body (near-white warm tuff -- the bright standing stone, brightest in the build)
SHADE  = "#a59c8c"   # taper shoulder wedges / shaft mid-band (clearly darker warm -- the lean + each pull-in read hard)
CARVE  = "#a87b4f"   # the carved channel surround (saturated warm tooled-stone -- the abstract MARK leaps off the pale shaft)
GROOVE = "#6e4d31"   # flanking incised grooves (deep warm brown -- the twin side cuts read as true shadow)
SOCKET = "#4a3826"   # the recessed socket throat behind the lanterns (near-black warm -- depth read)
CAP    = "#4c5a61"   # flared chiseled capstone (dark slate -- the one 'finished' gesture, crowns it)
MOSS   = "#6f8a3f"   # remote-decay moss smear (more saturated green -- clearly weathering, not just dark stone)
SENT   = "#cfcabd"   # sentinel stones (dressed but a notch off the shaft white -- the pair reads as its own stone)
SENTB  = "#5e5346"   # sentinel base stub (darkest rough -- the stub grips the step, the stone springs off it)

# geometry anchors: 7x7 plinth on x0-7,z0-7. The road faces FRONT (south, high z). Shaft centred.
CX, CZ = 3, 3        # back-left corner of the 1x1 crown column / shaft-centre reference

# ----------------------------------------------------------------------------
# COURSE 0 (y0) -- 7x7 stepped dressed plinth: pale cut-stone field + a tread wrap lip
# ----------------------------------------------------------------------------
S.box(0,0,0, 7,7,1, PLINTH)                 # 7x7 polished plinth the stone STANDS ON (not a plaza)
# stepped foot: a bright tread lip wrapping all four edges (stone_brick_stairs facing outward).
# The front + right edges are the camera-facing ones, so they read the worked step hardest.
S.box(0,0,0, 7,1,1, TREAD)                  # back edge tread
S.box(0,0,0, 1,7,1, TREAD)                  # left edge tread
S.box(6,0,0, 1,7,1, TREAD)                  # right edge tread (camera side -- catches light)
S.box(0,6,0, 7,1,1, TREAD)                  # front edge tread (road side -- catches light)
# masonry seams across the plinth field so the big flat course reads as cut blocks, not a slab
S.box(0,3,0, 7,1,1, STEP)                   # a darker jointing course bisecting the plinth field
# chiseled corners on the plinth -- coolest accent, proud 1 course, anchors the footprint corners
for (cxx,czz) in [(0,0),(6,0),(0,6),(6,6)]:
    S.box(cxx,czz,1, 1,1,1, CHIS)           # corner chiseled blocks, proud 1 course

# ----------------------------------------------------------------------------
# COURSE 1 (y1) -- 5x5 inset step (the riser) with a tread lip
# ----------------------------------------------------------------------------
S.box(1,1,1, 5,5,1, STEP)                   # 5x5 dressed step inset 1 all round (dark riser -- reads as shadow)
S.box(1,1,2, 5,1,1, TREAD)                  # step tread lip (slab) -- bright top band, reads the step
S.box(1,1,2, 1,5,1, TREAD)
S.box(5,1,2, 1,5,1, TREAD)                  # right step tread (camera side)
S.box(1,5,2, 5,1,1, TREAD)                  # front step tread (road side -- the approach lip)

# --- SENTINEL PAIR: 2 small leaning mini-menhirs at the FRONT CORNERS of the 5x5 step ---
# Each sits GROUNDED on the step tread (the step top is y2) at z=5 (the step's own front row),
# on a DARK rough stub (SENTB) so the pale leaning stone visibly springs off it. Mirrored
# left (x=1) / right (x=5) of the approach -- a framing pair (gatehouse twin-tower echo), never a ring.
# left sentinel (h=3, UPRIGHT -- near-capital clean read). Lean is +x, fully supported:
#   the y5 course at x=2 rests on the wedge stub at x=2,y4 (no float) beside the x=1 stack.
S.box(1,5,2, 1,1,1, SENTB)                  # dark stub-root, grounded on the step tread (y2)
S.box(1,5,3, 1,1,1, SENT)                   # leaning shaft course 1 (x=1)
S.box(1,5,4, 1,1,1, SENT)                   # course 2 (x=1)
S.box(2,5,4, 1,1,1, SENTB)                  # lean-support wedge stub beneath the offset top (grounds the lean)
S.box(2,5,5, 1,1,1, SENT)                   # crown course, offset +1 x = the lean, now SUPPORTED (no float)
# right sentinel (TOPPLED -- the ~40% remote fallen-one variation), MIRRORS the upright footprint
# at x=5, z=5. Its stone has FALLEN: it lies RECUMBENT, fully grounded flat on the step tread (y2),
# a pale 2-long shaft snapped off its dark stub-root which still stands beside it. No cantilever --
# the whole recumbent stone rests on the step course below; reads as a fallen mirror of the standing one.
S.box(5,5,2, 1,1,1, SENTB)                  # the snapped-off dark stub-root, still standing
S.box(4,5,2, 1,1,1, SENT)                   # recumbent fallen stone (rests flat on the step, y2)
S.box(3,5,2, 1,1,1, SENT)                   # recumbent fallen stone, 2nd course -- lies pointing away from the stub

# ----------------------------------------------------------------------------
# COURSES 2-3 (y2-y3) -- broad 3x3 rough HEFT-FOOT (gives the 16-high giant real weight)
# ----------------------------------------------------------------------------
S.box(2,2,2, 3,3,1, FOOT, seam=True)
S.box(2,2,3, 3,3,1, FOOT, seam=True)
S.box(2,2,3, 3,1,1, MOSS)                   # a single wild-edge moss smear band on the foot back

# ----------------------------------------------------------------------------
# COURSES 4-12 (y4-y12) -- the SHAFT: dressed core, 3x3 -> 2x2 -> 1x1, deliberate LEAN.
# Lean axis = +x (this spawn). Each shoulder is softened with a darker wedge course so the
# stepped taper + the lean both read. Every overhang is slab/stair-supported (build_technique).
# ----------------------------------------------------------------------------
# 3x3 segment (y4-y6) -- base of the shaft, leans by drifting the footprint +1 x over the run
S.box(2,2,4, 3,3,1, SHAFT, seam=True)
S.box(2,2,5, 3,3,1, SHAFT, seam=True)
S.box(2,2,6, 3,3,1, SHADE, seam=True)       # shoulder wedge band before the 2x2 pull-in
# 2x2 segment (y7-y10) -- inset to 2x2, drifted +1 x (the lean) so it overhangs the foot's lean side
S.box(3,2,7, 2,2,1, SHAFT, seam=True)
S.box(3,2,8, 2,2,1, SHAFT, seam=True)
S.box(3,2,9, 2,2,1, SHAFT, seam=True)
S.box(3,2,10, 2,2,1, SHADE, seam=True)      # shoulder wedge band before the 1x1 pull-in
# 1x1 segment (y11-y12) -- the neck, drifted +1 x again (final lean) toward the crown
S.box(4,3,11, 1,1,1, SHAFT)
S.box(4,3,12, 1,1,1, SHAFT)

# --- THE CARVED FACE (y6-y9, road/front face): abstract channel + deep socket ---
# IMPORTANT (perspective fix): the carved mark is a pure BLOCK-SWAP *into the shaft's own
# front (south) face -- the FRONT ROW of the 2x2 shaft is z=3 (cells z3..4), so the carved
# blocks are placed AT z=3 (replacing the shaft's front cells), NOT proud at z=4. Placed at
# z=4 they used to read as a separate brown box stuck onto the side; at z=3 they sit flush IN
# the face and depth-sort ON TOP of the shaft (higher x+z paints later) -> a real tooled niche.
# Layout on the 2-wide front face: LEFT column (x3) = the carved channel (CARVE surround framing
# a near-black SOCKET throat where the 2 lanterns ember); RIGHT column (x4) = the flanking GROOVE
# incision. Surround / dark throat / side-cut = the recess reads as carved, not a flat patch.
# The mark lives ENTIRELY on the 2x2 shaft (y7-y10), whose front row IS z=3 -- so every carved
# block sits flush in one coherent front face (no block stranded back inside the wider 3x3 below).
# channel surround (top + bottom of the column) frames the deep socket throat between them:
S.box(3,3,7, 1,1,1, CARVE)                  # lower channel surround (y7)
S.box(3,3,10,1,1,1, CARVE)                  # upper channel surround (y10)
S.box(3,3,8, 1,1,1, SOCKET)                 # socket throat (deep recess, y8) -- a lantern embers here
S.box(3,3,9, 1,1,1, SOCKET)                 # socket throat (deep recess, y9)
# the single flanking GROOVE incision, full height of the mark, on the right front column (x4):
S.box(4,3,7, 1,1,1, GROOVE)
S.box(4,3,8, 1,1,1, GROOVE)
S.box(4,3,9, 1,1,1, GROOVE)
S.box(4,3,10,1,1,1, GROOVE)
# (the 2 stacked socket lanterns ember on the SOCKET throat front face at y8/y9 -- accents below)

# ----------------------------------------------------------------------------
# COURSES 13-15 (y13-y15) -- the CROWN: 1x1 neck -> chiseled cap -> flared chiseled capstone
# ----------------------------------------------------------------------------
S.box(4,3,13, 1,1,1, SHADE)                 # neck narrows (y13)
S.box(4,3,14, 1,1,1, CHIS)                  # chiseled cap block (y14) -- the 'finished' gesture
# FLARED capstone (y15): corbels back out +1 on the lean (+x) side. The overhanging x=5 cell
# is GROUNDED by a chiseled corbel wedge tucked under it at y14 (build_technique C: the cantilever
# is supported, never floating) so the flare reads as a real corbelled capstone, not a ledge.
S.box(5,3,14, 1,1,1, CHIS)                  # corbel wedge under the flare's overhanging cell (grounds y15 x5)
S.box(4,3,15, 2,1,1, CAP)                   # FLARED capstone spanning x4..5 (now fully supported below)
S.box(4,2,15, 1,2,1, CAP)                   # capstone flare also wraps 1 in z (broad crown read)

# ----------------------------------------------------------------------------
# COURSE 16 (y16) -- the TIP: 1 asymmetric weather-broken core block, pulled to a hash corner
# ----------------------------------------------------------------------------
S.box(5,3,16, 1,1,1, CHIS)                  # crown tip on the flare's x5 cell (supported), pulled to the +x lean corner

# ----------------------------------------------------------------------------
# ACCENTS -- recessed lights (haloed crown + the deep socket pair) + sentinel finial
# ----------------------------------------------------------------------------
# socket lanterns ember on the SOCKET throat front face (cell x3,z3 -> front face at z=4), y8/y9 cells:
S.accent(3.5,4.0,8.5, "glow", r=2.3)        # deep carved-socket lantern (lower of the stacked pair)
S.accent(3.5,4.0,9.5, "glow", r=2.3)        # deep carved-socket lantern (upper) -- the embered MARK
S.accent(4.5,3.5,14.6, "glow", "#eafff8", r=2.8)  # recessed crown-lantern under the flared capstone halo
S.accent(2.5,5.5,6.0, "finial")             # upright left sentinel cap (the standing one of the pair)

# ----------------------------------------------------------------------------
# CALLOUT LABELS
# ----------------------------------------------------------------------------
S.label(5,3,16, "weather-broken tip — pulled to a hash corner")
S.label(5,3,15, "flared chiseled capstone + recessed crown-lantern halo")
S.label(4,3,9, "carved abstract channel + deep 2-lantern socket")
S.label(4,2,5, "single leaning shaft — 3×3 → 2×2 → 1×1 taper")
S.label(4,2,3, "broad 3×3 rough heft-foot (gives the giant weight)")
S.label(1,5,4, "flanking sentinel PAIR (one upright, one toppled)")
S.label(0,3,1, "7×7 stepped dressed plinth (never a plaza)")

out = S.svg(title="Menhir R5 — single monumental leaning standing stone (carved mark, sentinel pair)",
            size_label="7×7 plinth · h16 (over-tops the big-well; reads from afar)",
            label_w=360)
open("detail_svg/menhir.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/menhir.svg | bytes", len(out.encode()))
