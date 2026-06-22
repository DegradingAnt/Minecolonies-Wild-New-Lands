"""Lamp-post ROAD (R3) -> detail_svg/lamp_post_road.svg.
Per deco_catalog_v2.json id 'lamp_post' tier Road (footprint 1x1, side-arm reaches one block into
the adjacent column at the top, height 6): a THREE-log squared standard on a DRESSED stone-brick
plinth, with the FIRST outward-casting SIDE-ARM hanging lantern (NO chain at this tier -- chains
are reserved for Highway+ so the hardware itself escalates) plus a crown lantern. Two lights -- road
furniture casting light onto the carriageway, an engineered read.

Escalation: third distinct step -- taller THREE-log shaft (heavier than Path's two) on dressed
STONE-BRICK (a step up from cobblestone_wall), and the first OUTWARD side-arm appears. The chain is
deliberately WITHHELD until Highway so the hardware escalates Road -> Highway -> Great-Road. Trail/
Path/Road now read as three distinct silhouettes: leaning stub -> upright standard -> engineered
side-arm standard.

Build technique (E): the side-arm is one oak_fence reaching one block out, CONNECTING horizontally
to the full-block log shaft (logs are full blocks, the fence connects = a supported bracket); the
lantern hangs DIRECTLY off that fence underside (no chain) -- a supported hang, never a cantilever.

Originality/inspiration: medieval/early-modern street bracket-lamp, technique only; credited in
CREDITS.md, no assets/NBT copied. Same wnl_lamp_post identity whose Great-Road top is the twin-pier
light-arch; the data builder hashes decay/light/palette live per post."""
from iso_render import Iso

S = Iso(U=28)

# --- palette (literal) -- WIDE-CONTRAST ladder: dressed stone-brick foot -> warm squared timber
#     shaft -> wrought fence side-arm -> warm light. Each material reads as itself. Comment each ---
PAD    = "#8a8276"   # cobblestone footing pad (flush ground course)
BRICK  = "#9d978a"   # stone_brick_wall dressed base (paler dressed masonry -> the step up from cobble-wall)
BRICKD = "#7f7a6e"   # stone_brick_wall shadowed inner cheek -> reads the dressed wall waist
LOG    = "#b08a4f"   # stripped_oak_log SQUARED shaft (warm timber, THREE logs -> heavier than Path)
LOGL   = "#c49a5b"   # stripped_oak_log seam-lit edge -> reads the log courses
LOGE   = "#8a6c3c"   # stripped_oak_log end-grain ring at the cap (the cut top)
FENCE  = "#a9874f"   # oak_fence finial cap (the crown neck -- thinner than the log)
ARM    = "#8f6f3a"   # oak_fence SIDE-ARM (a touch darker -> the wrought bracket reads as its own member)
GROUND = "#5d5447"   # the road surface the pad sits flush in (darker -> reads grounded)

GLOW   = "#ffd47a"   # warm lantern light (two lights this rung -- crown + side-arm)

# Grid: 1x1 centre column; side-arm reaches one block out toward FRONT-EAST (the visible road side).
# ============================================================================
# ROAD CONTEXT -- a flush carriageway patch the footing sits IN, extending toward the lit side.
# ============================================================================
S.box(-0.3, -0.3, 0, 1.6, 2.4, 0.25, GROUND)         # carriageway patch (longer toward the front/lit side)

# ============================================================================
# L0 -- cobblestone footing PAD, flush; the ground course the dressed plinth plants on.
# ============================================================================
S.box(0, 0, 0.25, 1, 1, 0.75, PAD, seam=True)        # footing pad set flush into the road

# ============================================================================
# L1 -- DRESSED stone_brick_wall PLINTH (the step up from Path's cobblestone_wall -- crisper,
#       paler dressed stone): inset so it reads as a turned dressed post on the pad.
# ============================================================================
S.box(0.18, 0.18, 1.0, 0.64, 0.64, 1.0, BRICK, seam=True)   # stone_brick_wall dressed plinth post
S.box(0.18, 0.18, 1.0, 0.2, 0.64, 1.0, BRICKD)              # shadowed west cheek -> reads the wall waist

# ============================================================================
# L2-L4 -- the THREE-log squared stripped-oak SHAFT (heavier read than Path's two logs -- THIS is
#          the step up): a 3-log upright standard on the dressed plinth. Seams read the courses.
# ============================================================================
S.box(0.28, 0.28, 2.0, 0.44, 0.44, 3.0, LOG, seam=True)     # 3-log squared shaft y2..5
S.box(0.28, 0.72, 2.0, 0.44, 0.0, 3.0, LOGL)               # lit front edge reads the log courses
S.box(0.28, 0.28, 4.92, 0.44, 0.44, 0.08, LOGE)            # cut-top end-grain ring (dressed cap)

# ============================================================================
# L5 -- the CAP + SIDE-ARM: an oak_fence finial caps the shaft (crown neck); ONE oak_fence side-arm
#       reaches one block out toward the road (FRONT-EAST), CONNECTING horizontally to the full-block
#       log shaft (a supported bracket). A lantern hangs DIRECTLY off the arm underside -- NO CHAIN.
# ============================================================================
S.box(0.36, 0.36, 5.0, 0.28, 0.28, 0.7, FENCE, seam=True)  # oak_fence finial neck (crown seat)
# side-arm: spans from the shaft face out one block toward the front; thin wrought member, abuts shaft.
S.box(0.5, 0.72, 5.15, 0.18, 1.0, 0.18, ARM)               # oak_fence side-arm reaching to the road (connects to shaft)
S.box(0.45, 0.72, 5.0, 0.28, 0.18, 0.5, ARM)               # the arm-root collar on the shaft face (the connect node)

# ============================================================================
# ACCENTS -- TWO lights (the Road rung): a hanging lantern DIRECTLY off the side-arm underside
# (NO chain -- hardware withheld until Highway) throwing light onto the road, + a crown lantern.
# ============================================================================
S.accent(0.59, 1.6, 5.0, "glow", GLOW, r=3.2)             # side-arm hanging lantern (no chain) over the road
S.accent(0.5, 0.5, 5.95, "glow", GLOW, r=3.4)             # crown lantern standing on the fence finial

# ============================================================================
# CALLOUT LABELS
# ============================================================================
S.label(0.5, 0.5, 6.0, "crown lantern standing on the fence finial")
S.label(0.59, 1.6, 5.1, "FIRST side-arm: lantern hangs DIRECTLY off the fence (NO chain yet -- saved for Highway)")
S.label(0.5, 0.5, 3.4, "THREE-log squared shaft (heavier than Path's two)")
S.label(0.5, 0.5, 1.5, "DRESSED stone_brick_wall plinth (step up from cobble-wall)")
S.label(-0.3, 0.5, 0.3, "cobblestone footing pad, flush in the road (grounded)")

out = S.svg(title="Lamp-post R3 (Road) -- a three-log standard on a dressed stone-brick plinth, FIRST side-arm hanging lantern (no chain) + crown",
            size_label="1x1 foot * h6 * 2 lanterns (crown + side-arm) -- road furniture, NO chain (hardware withheld)",
            label_w=404)
open("detail_svg/lamp_post_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/lamp_post_road.svg | bytes", len(out.encode()))
