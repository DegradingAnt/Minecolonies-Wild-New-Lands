"""Harbour rung 2 (harbour, the Highway tier) -> detail_svg/harbour_harbour.svg.
Per deco_catalog_v2.json id 'harbour' tier 'Highway -> harbour' (22x11 KINKED main quay with a
~30deg dog-leg ~2/3 along + 2-3 mooring fingers + a 5x4 warehouse + a 7-tall A-frame timber
GANTRY CRANE + a stepped cutwater prow + a slipway; envelope ~26x16; height 11).

THE NON-LINEAR JUMP from small_quay: one finger + a shack becomes a multi-finger ENGINEERED quay
with a 7-tall CRANE LANDMARK (the harbour's recognisable original mass), a real warehouse, a
stepped CUTWATER prow and a slipway -- roughly 3-4x the block volume, the first rung you'd read
from offshore. NEW IDEA this rung (per escalation_note): the A-frame gantry crane + warehouse +
kinked cutwater quay. The FIRST sea_lanterns appear recessed flush in the dark-prismarine waterline.

Massing translated course-by-course from the catalog:
  - WATERLINE (Y=-1..-2): dark_prismarine wet-face 2 courses on seaward + dog-leg faces; the
    dog-leg corner chamfered with dark_prismarine_stairs (reads engineered, not a raw box).
  - FOUNDATION (clamped 6 + stilt fallback): cobble + mossy fill on the kinked plan; the dog-leg
    corner reinforced as a stepped CUTWATER prow (dark_prismarine stepped inward 1/layer, softened
    with stairs facing the swell -- the buildable 'curve').
  - DECK (Y=0): stone_bricks scatter + polished_andesite banding as a 2-wide walkway SPINE down
    the centre (telegraphs the road onto the quay); cobblestone_wall parapet + chiseled pier-caps.
  - WAREHOUSE (5x4x6): spruce-frame + spruce_log posts, stone_bricks plinth, low spruce_stairs
    gable, twin spruce_trapdoor shutters, a wide loading bay, barrel + hay_block crates inside.
  - GANTRY CRANE (~7 tall A-frame at the DOG-LEG HEAD): two raking spruce_log legs (step 1 across
    per 2 of rise), an apex, a stripped_spruce_log JIB cantilevering 4 out over the water,
    back-counterweighted by the apex + a stone_bricks heel, a chain falls + hook-lantern.
  - FINGERS (x2-3, out 6-8): plank decks on spruce piles, dark_prismarine collars, lantern + bollards.
  - HARBOUR GATE + SIGN: a lantern-topped spruce_fence post PAIR at the road->quay threshold + a
    way_sign (oak-sign fallback). NO banner here (banner reserved for great_harbour+).
  - SLIPWAY: a 3-wide stone_brick_stairs ramp descending into the water (each stair on a riser).

Original WNL geometry. Inspiration (FORM/SCALE/TECHNIQUE only, credited in CREDITS.md): Towns&Towers
/ Tidal Towns docks (stone quay + timber fingers + waterline course); the A-frame raking-log gantry
crane with a counterweighted cantilever jib is WNL's own original mass; the kinked dog-leg/cutwater
plan is a distinct footprint unlike the straight wharves of the source mods. Same wnl_harbour data
builder as render_harbour.py (the grand_port top rung); placer hashes dog-leg angle / finger count /
jib length / warehouse decay / slipway side live.
ISO: viewer-visible faces are SOUTH (max-z FRONT) + EAST (max-x) + TOP -> the cutwater prow, the
fingers, the crane jib and the gate all turned to the high-z FRONT so they read.
"""
from iso_render import Iso

S = Iso(U=11)

# ---- palette (literal hex ~ vanilla blocks) -- WIDE-CONTRAST ladder, each material reads apart ----
WATER = "#356f93"   # sea / inlet water (cool blue -- pushes the stone off it)
WET   = "#14302f"   # dark_prismarine WATERLINE 'tell' (near-black wet band -- the signature)
WETST = "#27514e"   # dark_prismarine_stairs chamfer (lifted off WET so the chamfered step reads)
DECK  = "#8f9499"   # stone_bricks deck -- cool grey-blue working stone
COBB  = "#6c6f72"   # cobblestone worn scatter -- darker cool, a worn patch
ANDE  = "#bdc0c2"   # polished_andesite SPINE band (pale cool -> telegraphs the road onto the quay)
CHIS  = "#d6cdb3"   # chiseled_stone_bricks pier-caps (warm bone -> the dressed caps pop)
FOUND = "#5a5d60"   # cobblestone foundation mass (darkest stone -> reads heavy + rooted)
MOSS  = "#5f7050"   # mossy_cobblestone foundation fleck
KERB  = "#9a948a"   # cobblestone_wall parapet / bollard caps (warm pale -> the low parapet reads)
BOLL  = "#7c756a"   # cobblestone bollard column (warm mid)
DIRT  = "#5d4f3a"   # coarse_dirt landward keying (the quay roots to land)
TIMB  = "#86603a"   # spruce_planks (warehouse + finger decks) -- warm timber
TIMBD = "#5a4026"   # spruce_log posts / spruce_fence piles (darker -> the frame reads)
STRIP = "#a98455"   # stripped_spruce_log crane jib (lighter timber -> the jib reads off the legs)
ROOF  = "#3f2f1c"   # spruce_stairs warehouse roof (dark warm -> roof sits DOWN, silhouette sharp)
SHUT  = "#2c2114"   # spruce_trapdoor shutters (darkest timber -> recessed window read)
HAY   = "#caa83e"   # hay_block cargo (warm gold -> the trade goods pop)
BARR  = "#7a5c3a"   # barrel cargo
HEEL  = "#7d7468"   # stone_bricks crane heel counterweight (the cantilever's anchor)
LANT  = "#ffd47a"   # lantern glow (hook + fingers + gate)
SEAL  = "#cfeede"   # sea_lantern glow (FIRST appears this rung, flush in the waterline)

# ============================================================================
# 0) WATER FIELD (drawn first / back)
# ============================================================================
S.box(0, 0, 0, 30, 18, 1, WATER)                 # sea / inlet plate

# ============================================================================
# 1) KINKED MAIN QUAY -- a dog-leg plan that hugs an inlet (NOT a straight wharf)
#    main arm along the back (x 3..19, z 3..9), kink ~2/3 along stepping the front edge OUT,
#    so the seaward face jogs forward at the dog-leg (x 16..25, z 6..12).
# ============================================================================
# -- waterline 'tell': 2 dark_prismarine courses on the seaward + dog-leg faces --
def wet2(x, z, dx, dz):
    S.box(x, z, 0, dx, dz, 1, WET)               # wet course 1 (Y=-1)
    S.box(x, z, 1, dx, dz, 1, WET)               # wet course 2 (Y=-2)
wet2(3, 9, 16, 1)                                # main-arm seaward wet face
wet2(16, 11, 9, 1)                               # dog-leg seaward wet face (jogged forward)
wet2(3, 3, 1, 6)                                 # west end wet face
wet2(24, 6, 1, 6)                                # dog-leg east end wet face
# dog-leg corner CHAMFER (dark_prismarine_stairs) -- the engineered jog, not a raw box
S.box(16, 9, 0, 1, 2, 1, WETST)
S.box(16, 9, 1, 1, 2, 1, WETST)

# -- foundation mass (cobble + mossy fleck, clamped) following the kinked plan --
S.box(3, 3, 1, 16, 6, 1, FOUND)                  # main-arm foundation
S.box(16, 6, 1, 9, 6, 1, FOUND)                  # dog-leg foundation
S.box(6, 9, 1, 2, 1, 1, MOSS)                    # mossy fleck at the waterline
S.box(20, 11, 1, 2, 1, 1, MOSS)
# landward keying (coarse_dirt back-west)
S.box(1, 3, 1, 2, 4, 1, DIRT)

# -- STEPPED CUTWATER PROW at the dog-leg corner: dark_prismarine stepped inward 1/layer into a
#    trapezoid, each step's nose capped + softened with a stairs course facing the open swell --
S.box(24, 11, 0, 3, 3, 1, WET)                   # widest wet course at the prow head
S.box(24, 11, 1, 3, 3, 1, WETST)                 # 2nd course (chamfered nose)
S.box(25, 12, 0, 2, 2, 1, WET)                   # step in toward the nose
S.box(25, 12, 1, 2, 2, 1, WETST)
S.box(26, 13, 0, 1, 1, 2, KERB)                  # dressed nose cap (stands proud, breaks the swell)

# ============================================================================
# 2) DECK COURSE (Y=0) -- worn stone scatter + a polished_andesite SPINE + parapet
# ============================================================================
S.box(3, 3, 2, 16, 6, 1, DECK)                   # main-arm deck
S.box(16, 6, 2, 9, 6, 1, DECK)                   # dog-leg deck
# worn cobble scatter
S.box(5, 4, 2, 3, 2, 1, COBB)
S.box(11, 6, 2, 2, 2, 1, COBB)
S.box(19, 8, 2, 3, 2, 1, COBB)
S.box(21, 6, 2, 2, 2, 1, COBB)
# -- polished_andesite SPINE: a 2-wide walkway down the quay centre (telegraphs the road) --
S.box(4, 5, 3, 14, 2, 1, ANDE)                   # main-arm spine
S.box(18, 7, 3, 6, 2, 1, ANDE)                   # spine turns down the dog-leg
# -- cobblestone_wall PARAPET on the seaward + dog-leg edges, chiseled pier-caps at fingerheads --
S.box(3, 9, 3, 13, 1, 1, KERB)                   # main-arm parapet (gap at x16 for the dog-leg)
S.box(16, 11, 3, 9, 1, 1, KERB)                  # dog-leg parapet
S.box(8, 9, 4, 1, 1, 1, CHIS)                    # chiseled pier-cap at finger 1 head
S.box(13, 9, 4, 1, 1, 1, CHIS)                   # pier-cap at finger 2 head
S.box(23, 11, 4, 1, 1, 1, CHIS)                  # pier-cap at the dog-leg finger head

# ============================================================================
# 3) BOLLARD ROW -- cobble column + wall cap, every ~3 along the seaward kerb
# ============================================================================
def bollard(bx, bz):
    S.box(bx, bz, 3, 1, 1, 1, BOLL)
    S.box(bx, bz, 4, 1, 1, 1, KERB)
bollard(5, 9); bollard(11, 9); bollard(18, 11); bollard(23, 11)

# ============================================================================
# 4) SLIPWAY -- a 3-wide stone_brick_stairs ramp descending into the water (each tread on a riser)
#    on the main arm's seaward face (west of finger 1), grounded course-by-course.
# ============================================================================
S.box(3, 9, 2, 2, 1, 1, COBB)                    # top of the ramp at deck level
S.box(3, 10, 1, 2, 1, 1, DECK)                   # mid ramp (steps down + out over the wet face)
S.box(3, 11, 0, 2, 1, 1, WET)                    # foot of the ramp at the waterline

# ============================================================================
# 5) WAREHOUSE (5x4x6) -- landward pad on the main arm (x 5..10, z 3..7), back-kerb flush
# ============================================================================
W_X, W_Z = 5, 3
S.box(W_X, W_Z, 2, 5, 4, 1, COBB)                # stone_bricks plinth course
S.box(W_X, W_Z, 3, 5, 4, 3, TIMB, seam=True)     # spruce-frame walls (the pale read)
for cx, cz in [(W_X, W_Z), (W_X+4, W_Z), (W_X, W_Z+3), (W_X+4, W_Z+3)]:
    S.box(cx, cz, 3, 0.7, 0.7, 3, TIMBD)         # spruce_log corner-posts (frame, not a dark box)
# twin spruce_trapdoor shutters on the high-z FRONT (over the loading bay) + a wide loading bay
S.box(W_X+1, W_Z+3, 5, 1, 1, 1, SHUT)            # shutter W (front face)
S.box(W_X+3, W_Z+3, 5, 1, 1, 1, SHUT)            # shutter E
S.box(W_X+1, W_Z+3, 3, 3, 1, 1, ROOF)           # wide loading-bay opening (dark, at deck level)
# low-pitch spruce_stairs gable roof: proud eave -> ridge
S.box(W_X-0.3, W_Z-0.3, 6, 5.6, 4.6, 1, ROOF)    # proud eave (overhang -> shadow line)
S.box(W_X+1, W_Z+1, 7, 3, 2, 1, ROOF)            # ridge course
# barrel + hay_block crates on the loading apron out front (abut the warehouse -- grounded)
S.box(W_X+1, W_Z+4, 2, 1, 1, 1, HAY)             # hay_block crate
S.box(W_X+3, W_Z+4, 2, 1, 1, 2, BARR)            # barrel stack (taller, by the apron)

# ============================================================================
# 6) A-FRAME GANTRY CRANE (~7 tall) at the DOG-LEG HEAD -- the recognisable original mass.
#    Stood ISOLATED at the front-right of the dog-leg deck so only open water sits behind it.
#    The two raking spruce_log legs are separated across X (3 apart) so the A reads in iso: the
#    WEST leg (low x) rakes UP + EAST, the EAST leg (high x) rakes UP + WEST, stepping 1 block
#    toward centre per 2 of rise, meeting at an apex over the deck. The stripped_spruce_log JIB
#    cantilevers FORWARD over the basin (toward the viewer, +z), back-balanced by the apex mass +
#    a stone_bricks heel block on the landward side -> structurally carried, never floating.
# ============================================================================
CR_X, CR_Z = 18, 7                               # crane base on the dog-leg deck (front-right, isolated)
# -- WEST leg: foot at (CR_X, z), rakes UP + EAST toward centre (x+1 per 2 of rise), 3 courses --
S.box(CR_X, CR_Z, 2, 1, 1, 2, TIMBD)             # west leg foot
S.box(CR_X+1, CR_Z, 4, 1, 1, 2, TIMBD)           # west leg mid (steps EAST 1 per 2 of rise)
S.box(CR_X+2, CR_Z, 6, 1, 1, 2, TIMBD)           # west leg upper (reaches the apex height)
# -- EAST leg: foot 5 east, rakes UP + WEST toward centre, 3 courses (a TALL, wide A) --
S.box(CR_X+5, CR_Z, 2, 1, 1, 2, TIMBD)           # east leg foot
S.box(CR_X+4, CR_Z, 4, 1, 1, 2, TIMBD)           # east leg mid (steps WEST 1 per 2 of rise)
S.box(CR_X+3, CR_Z, 6, 1, 1, 2, TIMBD)           # east leg upper (converges over the centre)
# -- APEX where the legs converge ~7-8 up (lighter STRIP timber so the A-frame crown reads) --
S.box(CR_X+2, CR_Z, 8, 2, 1, 1, STRIP)           # apex beam (the two legs meet; jib pivots here)
# -- heel COUNTERWEIGHT on the landward side of the apex (back-balances the cantilever) --
S.box(CR_X+1, CR_Z, 8, 1, 1, 1, HEEL)            # stone_bricks heel block (the back-balance anchor)
# -- stripped_spruce_log JIB cantilevering FORWARD over the basin (toward the viewer, +z) --
S.box(CR_X+2, CR_Z+1, 8, 1, 4, 1, STRIP)         # jib arm reaching out over the water (4 long, +z)
S.box(CR_X+2, CR_Z+5, 8, 1, 1, 1, TIMBD)         # jib-tip head block (the chain falls hang here)
S.box(CR_X+2, CR_Z+5, 5, 1, 1, 1, HEEL)          # hanging hook-block (mid-air load, on the chain falls)
# winch drum slung between the legs at deck level (a stripped-log spool)
S.box(CR_X+2, CR_Z, 2, 2, 1, 1, STRIP)           # winch drum + base guard

# ============================================================================
# 7) MOORING FINGERS (x3, out 6-8) -- plank decks on stilted piles + dark_prismarine collars
# ============================================================================
def finger(fx, fz0, length):
    for k in range(length):
        fz = fz0 + k
        S.box(fx, fz, 0, 1, 1, 1, TIMBD)         # spruce pile (grounded down to bed)
    # dark_prismarine collars at every-other pile waterline (abut the piles)
    for k in range(0, length, 2):
        S.box(fx, fz0 + k, 0, 1, 1, 1, WET)
    S.box(fx, fz0, 1, 1, length, 1, TIMB)        # plank deck spanning the piles
    S.box(fx, fz0 + length - 1, 2, 1, 1, 1, TIMBD)  # tip post (carries the hanging lantern)
    S.box(fx, fz0 + 1, 2, 1, 1, 1, BOLL)         # a bollard along the finger

finger(8, 10, 6)                                 # finger 1 (off the main arm)
finger(13, 10, 7)                                # finger 2
finger(23, 12, 6)                                # finger 3 (off the dog-leg, east of the crane)

# ============================================================================
# 8) HARBOUR GATE + SIGN -- lantern-topped spruce_fence post PAIR at the road->quay threshold
#    (the landward LEFT end) + a way_sign (oak-sign fallback). NO banner this rung.
# ============================================================================
S.box(1, 4, 2, 1, 1, 1, DIRT)                    # road approach landing keyed into the deck
S.box(2, 3, 3, 1, 1, 3, TIMBD)                   # west gate post
S.box(2, 6, 3, 1, 1, 3, TIMBD)                   # east gate post
S.box(2, 4, 5, 1, 2, 1, STRIP)                   # the lintel / sign-board spanning the posts (way_sign)

# ============================================================================
# 9) ACCENTS -- the FIRST sea_lanterns flush in the waterline + finger / hook / gate lanterns
# ============================================================================
# sea_lanterns recessed flush in the dark-prismarine waterline (the wet-edge glow begins this rung)
S.accent(7, 9.5, 1.4, "glow", SEAL, r=1.9)
S.accent(14, 9.5, 1.4, "glow", SEAL, r=1.9)
S.accent(22, 11.5, 1.4, "glow", SEAL, r=1.9)
# finger-tip hanging lanterns
S.accent(8.5, 15.5, 3.2, "glow", LANT, r=1.9)
S.accent(13.5, 16.5, 3.2, "glow", LANT, r=1.9)
S.accent(20.5, 17.5, 3.2, "glow", LANT, r=1.9)
# crane hook-block lantern (the chain falls forward over the basin)
S.accent(CR_X + 2.5, 12.5, 5.4, "glow", LANT, r=2.1)
# gate-post lanterns (twin posts)
S.accent(2.5, 3.5, 6.3, "glow", LANT, r=1.9)
S.accent(2.5, 6.5, 6.3, "glow", LANT, r=1.9)

# ============================================================================
# 10) CALLOUT LABELS
# ============================================================================
S.label(CR_X + 2.5, CR_Z, 8.5, "A-frame timber GANTRY crane (counterweighted cantilever jib) -- the offshore landmark")
S.label(W_X + 2, W_Z + 1, 7, "5x4 warehouse -- spruce frame, loading bay, barrel + hay_block cargo")
S.label(26, 13, 2.5, "stepped CUTWATER prow at the dog-leg (breaks the swell)")
S.label(14, 10, 1.5, "2-3 mooring fingers + a slipway, lantern per fingerhead")
S.label(7, 9.5, 1.4, "FIRST sea_lanterns flush in the dark-prismarine waterline")
S.label(2.5, 5, 6.3, "lantern-topped HARBOUR GATE + named way_sign (no banner yet)")
S.label(4, 5, 3, "polished-andesite SPINE telegraphs the road onto the kinked quay")

out = S.svg(title="Harbour R2 (harbour) -- the engineered jump: kinked cutwater quay + A-frame gantry crane + warehouse + slipway, first sea-lanterns",
            size_label="22x11 kinked quay + 3 fingers * h11 * ~9 lanterns (the first rung you read from offshore)",
            label_w=372)
open("detail_svg/harbour_harbour.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/harbour_harbour.svg | bytes", len(out.encode()))
