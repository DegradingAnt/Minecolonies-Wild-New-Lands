"""Harbour H6 (grand_port) detail render -> detail_svg/harbour.svg.
The hero TOP rung of the pier->quay->harbour ladder: a kinked dog-leg stone quay with a
RETURN ARM enclosing a sheltered 3-sided BASIN, a battered ROMAN-PHAROS LIGHTHOUSE (~22 tall,
7x7 -> 3x3, external square-spiral stair + corbelled fire-gallery), a two-storey hoist
WAREHOUSE, an A-frame raking-log GANTRY CRANE with a counterweighted cantilever jib, an
original secular SEA-CHAPEL (apsidal end + lit votive niche), a BELL-GATE at the road
threshold, mooring fingers, beacon pier-heads, and the dark-prismarine WATERLINE 'tell'.

Composition is original WNL geometry (kinked basin plan + battered pharos w/ external spiral
stair + A-frame gantry + secular oratory + dark-prismarine waterline signature).
Inspiration (FORM/SCALE/TECHNIQUE only, never copied; credited in CREDITS.md): Towns&Towers /
Tidal Towns docks; MineColonies/Byzantine civic masonry; the Roman pharos lighthouse; medieval
mariners' wayside shrines; the Roman harbour mole. All vanilla blocks.
"""
from iso_render import Iso

S = Iso(U=7)

# ---- palette (literal) -- DISTINCT tones, HIGH contrast so every surface reads apart ----
# Stone family REWORKED: pushed onto a wider value+hue spread so deck / cobble / avenue /
# plinth / parapet never blend into one grey mass (the old 7-grey ramp collided at <8 dist).
# Two hue lanes now do the work: COOL grey-blue for the worn working deck (deck/cobble),
# WARM bone for the dressed civic stone (avenue/plinth/parapet/quoins) -> the formal road,
# the Roman mole and the parapet read as a distinct dressed-stone system over the rough quay.
WATER = "#356f93"   # open sea / basin water (cooler, bluer -- pushes the stone off it)
WET   = "#14302f"   # dark_prismarine WATERLINE 'tell' (deepened -> the wet band reads near-black)
WETST = "#2b5350"   # dark_prismarine_stairs chamfer (lifted further from WET so the step reads)
DECK  = "#8f9499"   # stone_bricks quay deck -- COOL grey-blue working stone (off the warm dressed stone)
COBB  = "#6c6f72"   # cobblestone worn scatter -- DARK cool, clearly a worn patch on the deck
AVEN  = "#d8cdb0"   # chiseled_stone_bricks formal avenue -- WARM bone, telegraphs the great-road spine
PLINTH= "#c2b694"   # dressed Roman-mole plinth -- warm sand-stone, a notch under the avenue
CAP   = "#8a7d63"   # capital / base bands + counterweight heel -- warm MID-DARK (frames the dressed stone)
PARA  = "#a89a6f"   # stone_brick_wall parapet + piers -- warm dressed, darker than plinth so the wall reads
BLACK = "#322e3a"   # polished_blackstone string-course (deepened civic dark band)
LITE  = "#efe9da"   # near-white dressed stone (lighthouse banding + chapel quoins, top contrast)
TIMB  = "#86603a"   # spruce log / planks warm timber (warehouse + crane + fingers) -- richer
TIMBD = "#5a4026"   # darker spruce log corner-posts / piles (deepened -> frame reads)
ROOF  = "#3f2f1c"   # spruce_stairs roofs (darkened warm -> roofs sit DOWN, silhouette sharper)
SAND  = "#dcc585"   # cut_sandstone chapel quoins (warm pale accent, distinct from bone avenue)
GLASS = "#bfe6e2"   # lantern-room glass crown
BANNER= "#e4ddcd"   # hung white_banner (lightened -> reads as cloth, not stone)
ROAD  = "#5c4a2e"   # great-road dirt approach (darkened -> clearly earth, not the timber)

# ============================================================================
# 0) WATER FIELD (drawn first / back) -- open sea behind, sheltered basin in the crook
# ============================================================================
S.box(2, 1, 0, 34, 23, 1, WATER)                 # sea plate (hugs the port; everything sits in/over it)

# ============================================================================
# 1) MAIN QUAY ARM (runs left->right along the back) + RETURN ARM (down the right)
#    forming a kinked dog-leg that encloses a 3-sided BASIN (open toward viewer/front-left)
# ============================================================================
# -- foundation / waterline 'tell' bands (dark_prismarine wet face, 3 courses) --
def quay_foundation(x, z, dx, dz):
    S.box(x, z, 0, dx, dz, 1, WET)               # waterline tell course (Y=-1 equiv)
    S.box(x, z, 1, dx, dz, 1, WETST)             # second wet course / chamfer

# main arm along the back (z = 2..6), x = 4..34
quay_foundation(4, 2, 30, 5)
# return arm down the right side (x = 28..34, z = 6..20) enclosing the basin
quay_foundation(28, 6, 6, 14)

# -- Roman-mole dressed stepped PLINTH edge (front faces of both arms) --
S.box(4, 6, 2, 24, 1, 1, PLINTH)                 # main-arm seaward plinth step (basin side)
S.box(27, 6, 2, 1, 14, 1, PLINTH)               # return-arm inner plinth step
S.box(4, 1, 2, 30, 1, 1, PLINTH)                # main-arm OUTER (open-sea) plinth step

# -- CUTWATER PROW (spec build-technique): dark_prismarine wedge stepped seaward off the
#    return-arm head, each course narrowing to a nose facing the open swell (a buildable wedge) --
S.box(31, 18, 0, 3, 3, 1, WET)                   # wedge waterline course (widest, at the head)
S.box(31, 18, 1, 3, 3, 1, WETST)                 # second wet course
S.box(32, 19, 0, 2, 2, 1, WET)                   # step in toward the nose
S.box(32, 19, 1, 2, 2, 1, WETST)
S.box(33, 20, 0, 1, 1, 2, PLINTH)               # dressed nose cap (the prow point, stands proud)

# -- DECK course (stone_bricks + worn cobble scatter) --
S.box(4, 2, 3, 30, 4, 1, DECK)                   # main arm deck top
S.box(28, 6, 3, 6, 14, 1, DECK)                  # return arm deck top
# worn-cobble scatter patches (hash-feel, hand-placed for read; cool COBB pops off the deck now)
S.box(8, 3, 3, 3, 2, 1, COBB)
S.box(18, 2, 3, 2, 3, 1, COBB)
S.box(30, 11, 3, 3, 4, 1, COBB)
S.box(29, 16, 3, 2, 3, 1, COBB)
S.box(11, 5, 3, 2, 1, 1, COBB)                   # apron worn patch by the warehouse
S.box(24, 4, 3, 1, 2, 1, COBB)                   # worn patch mid-quay
# chiseled inlay studs flanking the avenue (small pale accents that catch the eye along the road)
S.box(7, 2, 4, 1, 1, 1, AVEN)
S.box(13, 5, 4, 1, 1, 1, AVEN)
S.box(22, 2, 4, 1, 1, 1, AVEN)

# -- formal AVENUE spine (chiseled_stone_bricks, telegraphs the great-road onto the quay) --
S.box(6, 3, 4, 22, 2, 1, AVEN)                   # 2-wide pale spine down the main arm
S.box(29, 7, 4, 2, 9, 1, AVEN)                   # avenue turns down the return arm

# -- string-course / polished_blackstone civic dressed band along the parapet base --
S.box(4, 1, 4, 30, 1, 1, BLACK)                  # outer seaward dark band
# -- cut-stone PARAPET (stone_brick_wall) with chiseled piers every 5 (outer sea edge) --
S.box(4, 1, 5, 30, 1, 1, PARA)
for px in range(5, 33, 5):
    S.box(px, 1, 6, 1, 1, 1, AVEN)               # chiseled pier caps standing proud of the wall

# ============================================================================
# 2) BELL-GATE -- great-road threshold at the landward LEFT end of the main arm
# ============================================================================
S.box(0, 3, 1, 4, 2, 1, ROAD)                    # great-road approach landing keyed into the deck
# twin stone gate posts carrying the lintel + hung banner + harbour bell
S.box(2, 2, 4, 1, 1, 4, CAP)                     # west post base band
S.box(2, 5, 4, 1, 1, 4, CAP)                     # east post base band
S.box(2, 2, 5, 1, 1, 3, PARA, seam=True)         # west post shaft
S.box(2, 5, 5, 1, 1, 3, PARA, seam=True)         # east post shaft
S.box(2, 2, 8, 1, 4, 1, BLACK)                   # gate lintel spanning the road (the bell hangs here)
S.box(3, 2, 9, 1, 4, 1, BANNER)                  # hung white_banner over the lintel

# ============================================================================
# 3) SEA-CHAPEL -- secular mariners' oratory at the gate (apsidal end + lit votive niche)
#    reserved landward pad just inside the gate (x 5..9, z 2..6)
# ============================================================================
CH_X, CH_Z = 5, 2
# thin dressed plinth lifts the oratory off the quay deck (reads as a distinct civic building)
S.box(CH_X, CH_Z, 4, 4, 3, 1, BLACK)             # dark socle course (separates chapel from cool deck)
# walls (warm dressed stone) with cut_sandstone quoins -- the first VERTICAL civic mass, off the cool quay
S.box(CH_X, CH_Z, 5, 4, 3, 4, PLINTH, seam=True) # nave body (warm dressed, pops off the cool DECK quay)
for qx, qz in [(CH_X, CH_Z), (CH_X+3, CH_Z), (CH_X, CH_Z+2), (CH_X+3, CH_Z+2)]:
    S.box(qx, qz, 5, 1, 1, 4, SAND)              # warm quoin pilasters at each corner
# round-arched doorway facing the road (west face) -- stair voussoirs + keystone read as a band
S.box(CH_X, CH_Z+1, 5, 1, 1, 2, ROOF)            # dark doorway recess
S.box(CH_X, CH_Z+1, 7, 1, 1, 1, AVEN)            # chiseled keystone over the arch
# apsidal (rounded) SEAWARD end -- stepped-back half-ring softened, faces the basin (front)
S.box(CH_X+1, CH_Z+3, 5, 2, 1, 3, PLINTH)        # apse first step (proud of the nave)
S.box(CH_X+1, CH_Z+4, 5, 2, 1, 2, SAND)          # apse second step (rounds the end)
# lit VOTIVE NICHE in the seaward wall (lantern behind iron_bars grille)
# steep spruce_stairs gable + a tiny spirelet
S.box(CH_X, CH_Z, 9, 4, 3, 1, ROOF)              # gable eave
S.box(CH_X, CH_Z+1, 10, 4, 1, 1, ROOF)           # ridge
S.box(CH_X+1, CH_Z+1, 11, 1, 1, 2, SAND)         # spirelet

# ============================================================================
# 4) TWO-STOREY WAREHOUSE -- landward pad mid-quay (x 14..20, z 2..6)
# ============================================================================
W_X, W_Z = 14, 2
S.box(W_X, W_Z, 4, 6, 4, 1, COBB)                # stone_bricks plinth course
S.box(W_X, W_Z, 5, 6, 4, 3, TIMB, seam=True)     # ground storey (spruce-frame walls)
for cx, cz in [(W_X, W_Z), (W_X+5, W_Z), (W_X, W_Z+3), (W_X+5, W_Z+3)]:
    S.box(cx, cz, 5, 1, 1, 4, TIMBD)             # darker spruce_log corner-posts (read the frame)
S.box(W_X, W_Z, 8, 6, 4, 2, TIMB)                # upper storey (set in slightly via posts)
# upper-storey window/SHUTTER band (spruce_trapdoor shutters read as dark recesses with a pale frame)
S.box(W_X+1, W_Z+4, 9, 1, 1, 1, ROOF)            # shutter recess W (front face, over the apron)
S.box(W_X+4, W_Z+4, 9, 1, 1, 1, ROOF)            # shutter recess E
S.box(W_X+1, W_Z+4, 8, 1, 1, 1, COBB)            # sill course under the shutters
S.box(W_X+4, W_Z+4, 8, 1, 1, 1, COBB)
# spruce_stairs HIP roof, courses inset + climbing
S.box(W_X, W_Z, 10, 6, 4, 1, ROOF)
S.box(W_X+1, W_Z+1, 11, 4, 2, 1, ROOF)
S.box(W_X+2, W_Z+1, 12, 2, 2, 1, ROOF)
S.box(W_X+2, W_Z+1, 13, 2, 2, 1, TIMBD)          # ridge beam capping the hip (sharpens the silhouette)
# gabled DORMER breaking the front roof slope (spruce_stairs cheeks + a lit loft window)
S.box(W_X+2, W_Z+3, 11, 2, 1, 2, ROOF)           # dormer box proud of the roof
S.box(W_X+2, W_Z+3, 13, 2, 1, 1, TIMBD)          # dormer ridge
# gable HOIST BEAM (stripped_spruce_log) cantilevering over the quay w/ chain+lantern
S.box(W_X+2, W_Z+4, 9, 2, 2, 1, TIMBD)           # hoist beam out over the loading apron
S.box(W_X+2, W_Z+5, 9, 1, 1, 1, TIMB)            # beam tip block (the chain falls from here)
# LOADING APRON goods -- barrel + hay_block stacks on the quay below the hoist (richest trade loot)
S.box(W_X+1, W_Z+4, 4, 1, 1, 2, TIMB)            # barrel stack A
S.box(W_X+3, W_Z+4, 4, 1, 1, 1, SAND)            # hay_block
S.box(W_X+4, W_Z+5, 4, 1, 1, 2, TIMBD)           # barrel stack B (taller, by the water)

# ============================================================================
# 5) A-FRAME GANTRY CRANE -- raking spruce-log legs, counterweighted cantilever jib
#    at the return-arm / dog-leg head (x 30..32, z 8..12), jib reaches out over the basin
# ============================================================================
CR_X, CR_Z = 30, 9
# two raking legs: each steps 1 block horizontally per 2 of rise (buildable lean)
S.box(CR_X, CR_Z, 4, 1, 1, 2, TIMBD)             # near leg foot
S.box(CR_X+1, CR_Z, 6, 1, 1, 2, TIMBD)           # near leg mid (stepped in)
S.box(CR_X+2, CR_Z, 8, 1, 1, 2, TIMBD)           # near leg upper
S.box(CR_X, CR_Z+2, 4, 1, 1, 2, TIMBD)           # far leg foot
S.box(CR_X+1, CR_Z+2, 6, 1, 1, 2, TIMBD)         # far leg mid
S.box(CR_X+2, CR_Z+2, 8, 1, 1, 2, TIMBD)         # far leg upper
S.box(CR_X+2, CR_Z, 10, 1, 3, 1, TIMB)           # apex block (legs meet)
S.box(CR_X+3, CR_Z+1, 9, 1, 1, 2, CAP)           # stone_bricks heel COUNTERWEIGHT cradle (carries the jib)
S.box(CR_X+3, CR_Z+1, 11, 1, 1, 1, BLACK)        # blackstone counterweight mass (dark, reads the load)
# stripped_spruce_log WINCH DRUM (a spool slung between the legs at deck level)
S.box(CR_X+1, CR_Z, 5, 1, 3, 1, TIMBD)           # drum axle spanning the legs
S.box(CR_X+1, CR_Z+1, 4, 1, 1, 2, TIMB)          # drum barrel (the rope spool)
# stripped_spruce_log JIB cantilevering out over the water (toward the viewer / basin)
S.box(CR_X-3, CR_Z+1, 10, 5, 1, 1, TIMB)         # the jib arm (back-balanced by apex+heel)
S.box(CR_X-3, CR_Z+1, 9, 1, 1, 1, TIMBD)         # jib-tip head block (DOUBLE chain falls hang here)
S.box(CR_X-3, CR_Z+1, 7, 1, 1, 1, CAP)           # the hanging hook-block / pulley (mid-air load)

# ============================================================================
# 6) THE PHAROS LIGHTHOUSE -- battered tapering tower on a pier-head at the BASIN MOUTH
#    front-most landmark (high x+z so it paints over everything), ~22 tall, 7x7 -> 3x3
# ============================================================================
LX, LZ = 20, 17     # pier-head out toward the viewer (front), at the basin mouth
# -- pier-head foundation + waterline tell under the tower --
S.box(LX-1, LZ-1, 0, 9, 9, 1, WET)               # dark_prismarine pier-head waterline
S.box(LX-1, LZ-1, 1, 9, 9, 1, WETST)
S.box(LX-1, LZ-1, 2, 9, 9, 1, PLINTH)            # dressed pier-head deck
# -- battered shaft: 7x7 -> 5x5 -> 3x3, banded LITE(white)/PLINTH(warm)/BLACK, set-backs stair-softened --
S.box(LX, LZ, 3, 7, 7, 1, WET)                   # dark base band matching the waterline
S.box(LX, LZ, 4, 7, 7, 3, LITE, seam=True)       # stage 1 (7x7) -- near-white dressed band
S.box(LX, LZ, 7, 7, 7, 1, BLACK)                 # blackstone string-course set-back band
S.box(LX+1, LZ+1, 8, 5, 5, 1, SAND)              # stage-2 stair-chamfer course (warm batter shoulder, reads dressed)
S.box(LX+1, LZ+1, 9, 5, 5, 3, PLINTH, seam=True) # stage 2 (5x5) -- WARM dressed band (contrast vs white)
S.box(LX+1, LZ+1, 12, 5, 5, 1, BLACK)            # string-course
S.box(LX+2, LZ+2, 13, 3, 3, 1, SAND)             # stage-3 stair-chamfer course (batter shoulder)
S.box(LX+2, LZ+2, 14, 3, 3, 3, LITE, seam=True)  # stage 3 (3x3) -- near-white again
# -- EXTERNAL square-spiral stair winding the shaft (clearly OUR geometry, not a cylinder) --
S.box(LX-1, LZ+2, 4, 1, 2, 1, CAP)               # tread W (low)
S.box(LX+2, LZ-1, 6, 2, 1, 1, CAP)               # tread N
S.box(LX+6, LZ+2, 8, 1, 2, 1, CAP)              # tread E
S.box(LX+2, LZ+5, 10, 2, 1, 1, CAP)             # tread S (one full turn)
# -- CORBELLED fire-GALLERY: ring stepped OUT 1 block, railed (the pharos fire-platform) --
S.box(LX+1, LZ+1, 17, 5, 5, 1, CAP)              # corbel bracket ring (steps out from the 3x3)
S.box(LX+1, LZ+1, 18, 5, 1, 1, PARA)            # gallery rail (N)
S.box(LX+1, LZ+5, 18, 5, 1, 1, PARA)            # gallery rail (S)
S.box(LX+1, LZ+1, 18, 1, 5, 1, PARA)            # gallery rail (W)
S.box(LX+5, LZ+1, 18, 1, 5, 1, PARA)            # gallery rail (E)
# -- lantern-room: sea_lantern + glass, peaked spruce_stairs cap, lightning-rod finial --
S.box(LX+2, LZ+2, 18, 3, 3, 2, GLASS)            # glazed lantern room (the pharos fire)
S.box(LX+2, LZ+2, 20, 3, 3, 1, ROOF)            # peaked cap course 1
S.box(LX+3, LZ+3, 21, 1, 1, 1, ROOF)            # peaked cap peak

# ============================================================================
# 7) BASIN-MOUTH BEACON pier-heads -- two squat dark_prismarine heads, sea_lantern beacons
# ============================================================================
S.box(12, 20, 0, 3, 3, 1, WET)                   # west beacon pier-head waterline
S.box(12, 20, 1, 3, 3, 2, WETST)                 # squat dark head
S.box(28, 20, 0, 3, 3, 1, WET)                   # east beacon pier-head (mirrors)
S.box(28, 20, 1, 3, 3, 2, WETST)

# ============================================================================
# 8) MOORING FINGERS -- timber plank decks on stilted spruce piles, reaching into the basin
# ============================================================================
def finger(fx, fz, length, bollards=True):
    for k in range(length):                      # spruce_fence/log piles down to bed (stilted)
        S.box(fx, fz+k, 1, 1, 1, 2, TIMBD)       # pile (dark log)
        if k % 2 == 0:
            S.box(fx, fz+k, 0, 1, 1, 1, WET)     # dark_prismarine pile-collar at waterline
    S.box(fx, fz, 3, 1, length, 1, TIMB)         # plank deck on top
    if bollards:                                  # stone mooring BOLLARDS standing proud along the deck
        S.box(fx, fz+1, 4, 1, 1, 1, CAP)
        S.box(fx, fz+length-2, 4, 1, 1, 1, CAP)

finger(16, 8, 8)                                 # finger 1 (reaches into the basin)
finger(23, 8, 7)                                 # finger 2
finger(26, 11, 6)                                # finger 3 (return-arm side)

# -- PASSENGER LANDING: finger 1 widened into a roofed waiting bay (spec sub-feature) --
S.box(15, 13, 3, 3, 3, 1, TIMB)                  # widened landing platform (the boarding apron)
S.box(15, 13, 4, 1, 1, 3, TIMBD)                 # waiting-bay corner posts (spruce_fence)
S.box(17, 13, 4, 1, 1, 3, TIMBD)
S.box(15, 15, 4, 1, 1, 3, TIMBD)
S.box(17, 15, 4, 1, 1, 3, TIMBD)
S.box(15, 13, 7, 3, 3, 1, ROOF)                  # spruce_stairs canopy over the waiting bay
S.box(16, 14, 8, 1, 1, 1, TIMBD)                 # canopy ridge peak (sharpens its silhouette)

# ============================================================================
# 9) ACCENTS -- ALWAYS-LIT capital port: sea_lanterns at the waterline, beacons, lighthouse
#    fire, gate lanterns, lamp-posts, crane hook, finial
# ============================================================================
# sea_lanterns flush in the waterline along the seaward edge (the wet-edge glow)
for gx in range(6, 34, 6):
    S.accent(gx, 1.5, 5.2, "glow", "#cfeede", r=2.0)
# basin-mouth BEACON pier-heads
S.accent(13.5, 21.5, 3.4, "glow", "#cfeede", r=2.8)
S.accent(29.5, 21.5, 3.4, "glow", "#cfeede", r=2.8)
# bell-gate lanterns (twin posts) + the bell read
S.accent(2.5, 2.5, 8.4, "glow", r=2.4)
S.accent(2.5, 5.5, 8.4, "glow", r=2.4)
# chapel votive niche (warm, behind the grille) + spirelet light
S.accent(7.0, 6.0, 6.0, "glow", r=2.0)           # lit votive niche (seaward wall)
# warehouse hoist lantern + interior glow
S.accent(16.0, 6.2, 9.2, "glow", r=2.2)          # hoist-beam hook lantern
S.accent(17.0, 4.0, 6.0, "glow", r=1.8)          # warehouse loading-bay glow
# crane hook-block (chain falls + hanging lantern over the basin)
S.accent(28.0, 10.5, 9.4, "glow", r=2.2)
# lamp-posts along the deck avenue (wnl_lamp_post intervals)
S.accent(10.0, 3.5, 5.4, "glow", r=1.8)
S.accent(24.0, 3.5, 5.4, "glow", r=1.8)
S.accent(30.5, 14.0, 5.4, "glow", r=1.8)
# finger-head hanging lanterns
S.accent(16.5, 15.5, 4.4, "glow", r=1.8)
S.accent(23.5, 14.5, 4.4, "glow", r=1.8)
# THE PHAROS FIRE -- bright sea-lantern crown + lightning-rod finial (distance landmark)
S.accent(LX+3.5, LZ+3.5, 22.0, "glow", "#fff6da", r=4.2)
S.accent(LX+3.5, LZ+3.5, 22.4, "finial")

# ============================================================================
# 10) CALLOUT LABELS
# ============================================================================
S.label(LX+3.5, LZ+3.5, 20, "battered Pharos lighthouse — external spiral stair + fire-gallery")
S.label(28, 10, 11, "A-frame timber gantry crane (counterweighted jib)")
S.label(W_X+3, W_Z+1, 12, "two-storey hoist warehouse")
S.label(CH_X+2, CH_Z+2, 10, "secular sea-chapel — apsidal end + votive niche")
S.label(2.5, 4, 9, "bell-gate — banner + harbour bell over the road")
S.label(20, 19, 2, "sheltered basin + beacon pier-heads + mooring fingers")
S.label(6, 1, 4, "dark-prismarine waterline 'tell' + Roman-mole esplanade")

out = S.svg(title="Harbour H6 — grand port: Pharos lighthouse over a kinked-quay basin (the pier→quay→harbour ladder top)",
            size_label="~44×30 port envelope · h24 (the Pharos reads from a great distance)")
open("detail_svg/harbour.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/harbour.svg | bytes", len(out.encode()))
