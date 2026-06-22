"""rest_stop ROAD (R3) -> detail_svg/rest_stop_road.svg.
Per deco_catalog_v2.json id 'rest_stop' tier Road (footprint 9x9, height 5, KIND=nbt TEMPLATE #1):
the jump from a camp into 'a place built for staying' -- the FIRST built SHELTER. An L-shaped
lean-to (OPEN, never a box/tent) with a real ONE-WAY SHED roof: a single course of spruce_stairs
all facing one way over the 3-wide span, the high edge on the 2-tall back wall, the low edge on the
open front -- a true pitch, not a flat lid. Plus the floor becomes a laid cobble/stone-brick COURT
(per-cell hash scatter), the hearth dresses up to a 3x3 ring with slab-capped corners + a cauldron
cook-spot, a 4-seat arc wraps the fire, and the traveller's post grows to 3 tall with TWIN side-arms
each carrying a chain + hung lantern, plus a wayfinding SIGN-POST. ~3 light sources.

This is the catalog's first NBT template (the data scatter still decorates the cleared rim around it).
The ONE clear new idea over Path = the roofed shelter (+ the post doubling its arms/lanterns). Same
wnl_rest_stop palette resolver as the Great Road top (render_rest_stop.py); hash drives the floor
scatter, arc rotation, the sub-feature (feed vs market), the shelter side + sign text.
Inspiration (FORM/technique only, never copied; CREDITS.md): MineColonies / Byzantine timber-frame
lean-tos; roadside camp 'middles' in CTOV / Moog's Paths; supplementaries:sign_post as native
wayfinding. Vanilla blocks only; original geometry. Shelter is ALWAYS open-sided (the WNL rule).
ISO: road at the FRONT (high-z); the shed's OPEN front + post + sign face the road; lean-to on the FAR side."""
from iso_render import Iso

S = Iso(U=17)

# ---- palette (literal) -- DISTINCT tones, WIDE luminance ladder so every material reads ----
# Stone court ladder (dark->light): COBBLE < BRICK < CRACK < MOSS dressed mix; warm timber kept
# distinct; the spruce shed roof goes DARK so it pops off the pale court + reads as a real roof.
KERB  = "#6d7177"   # cleared-rim earth/kerb-dark frame (darkest -> lifts the court)
GRASS = "#6f8a47"   # biome top at the rim (grass shows through)
COBB  = "#8a8276"   # cobblestone floor cell (the 55% lead -- mid stone)
BRICK = "#9d988d"   # stone_bricks floor cell (30% -- lighter dressed)
CRACK = "#857f72"   # cracked_stone_bricks floor cell (10% -- worn darker)
MOSS  = "#6f7d56"   # mossy_cobblestone floor cell (5% -- the green note)
APRON = "#6a5532"   # dirt_path apron connecting the court to the road deck (deeper earth)
RING  = "#7c7468"   # cobblestone hearth-ring stones (dark -> the flame pops)
RCAP  = "#b9b3a5"   # cobblestone_slab[top] corner caps on the ring (bright dressed -> reads dressed)
SOIL  = "#574631"   # dug fire hollow
CAMP  = "#5a4427"   # campfire charred bed
EMBER = "#caa24e"   # campfire ember glow band
CAULD = "#3f4248"   # cauldron iron (dark) on its plinth
PLINTH= "#9d988d"   # the single floor-block cook plinth under the cauldron (= BRICK tone)
OAK   = "#b89160"   # stripped_oak seats / benches (pale warm)
OAKE  = "#8f6e44"   # stripped_oak end-grain
SPR   = "#9a7a4c"   # stripped_spruce POST shaft + arms (mid timber -> the vertical reads)
SPRE  = "#6f5230"   # spruce post footing + dark base band
WLOG  = "#7a5c3a"   # stripped_spruce_log shelter WALLS (back + one side -- warm timber-frame)
WLOG2 = "#6a4f30"   # darker log pick (the log seams / the short side wall -> reads 2 wall runs)
ROOF  = "#43404a"   # spruce_stairs shed roof (DARK slate-spruce -> max contrast vs pale court)
ROOF2 = "#54505e"   # lighter roof course (the low front lip -> reads the pitch step)
HAY   = "#d4b441"   # hay_block bed corner (gold)
BARR  = "#7a5c3a"   # barrel crate body
BARRT = "#caa24e"   # barrel hoop band
SIGN  = "#9c7444"   # sign-post board (lighter warm timber -> the wayfinding board reads)
CHAIN = "#54545c"   # chain under the arms
LANT  = "#ffd47a"   # lantern glow

# =====================================================================================
# COURT (9x9): a laid floor of cobble/stone-brick cells (per-cell hash scatter), grass at the rim,
# a 3-wide dirt apron out the front to the road. Kerb-dark frame lifts the court off the ground.
# =====================================================================================
S.box(0, 0, 0, 9, 9, 0.5, KERB)                  # kerb base slab under the whole court (frames it)
# grass rim cells (corners + a thin border where the court doesn't fully reach -> 'bare ground reads')
for (gx, gz) in [(0,0),(8,0),(0,8),(8,8)]:
    S.box(gx, gz, 0.5, 1, 1, 0.4, GRASS)
# the laid floor (8x8 inner-ish), per-cell hash variant: cobble lead, brick, cracked, mossy.
FLOOR = {}
import_pat = [  # a deterministic 'hash' layout (cobble 55 / brick 30 / crack 10 / moss 5)
    "CBCBCBCB",
    "BCCBKCBC",
    "CBCMBCCB",
    "BCBCCBKC",
    "CKBCBCBC",
    "BCCBCMBC",
    "CBKCBCCB",
    "BCBCCBCB",
]
TONE = {"C":COBB, "B":BRICK, "K":CRACK, "M":MOSS}
for r, row in enumerate(import_pat):
    for c, ch in enumerate(row):
        gx, gz = c, r
        if (gx, gz) in [(0,0),(8,0),(0,8),(8,8)]:   # leave the grass corners
            continue
        if gx > 8 or gz > 8:
            continue
        S.box(gx, gz, 0.5, 1, 1, 0.4, TONE[ch])
# 3-wide dirt apron out the FRONT-centre to the road
S.box(3, 8, 0.5, 3, 1, 0.4, APRON)
S.box(3, 9, 0, 3, 1, 0.5, APRON)                 # apron tongue reaching out to the road

# =====================================================================================
# HEARTH (off-center toward the road): a dressed 3x3 ring of cobble with slab-capped corners,
# a campfire centre, and an empty cauldron one block off on a single floor-block plinth (cook spot).
# =====================================================================================
HX, HZ = 3, 4                                    # ring foot, centre (HX+1, HZ+1), nudged to road
S.box(HX+1, HZ+1, 0.9, 1, 1, 0.4, SOIL)          # dug hollow in the ring centre
RINGCELLS = [(HX,HZ),(HX+1,HZ),(HX+2,HZ),(HX,HZ+1),(HX+2,HZ+1),(HX,HZ+2),(HX+1,HZ+2),(HX+2,HZ+2)]
for (sx, sz) in RINGCELLS:
    S.box(sx, sz, 0.9, 1, 1, 0.6, RING, seam=True)
# slab caps on the 4 corner stones (dressed -> the ring reads built, not raw)
for (sx, sz) in [(HX,HZ),(HX+2,HZ),(HX,HZ+2),(HX+2,HZ+2)]:
    S.box(sx+0.1, sz+0.1, 1.5, 0.8, 0.8, 0.25, RCAP)
# campfire in the hollow
S.box(HX+1.12, HZ+1.12, 0.9, 0.76, 0.76, 0.34, CAMP)
S.box(HX+1.18, HZ+1.18, 1.22, 0.64, 0.64, 0.18, EMBER)
# cauldron cook-spot: one block off the ring (front-right), on a single floor-block plinth.
S.box(HX+3, HZ+2, 0.9, 1, 1, 0.5, PLINTH)        # the cook plinth (a floor block raised)
S.box(HX+3.12, HZ+2.12, 1.4, 0.76, 0.76, 0.7, CAULD, seam=True)  # the empty cauldron

# =====================================================================================
# LEAN-TO SHELTER (first built shelter, L-shaped, OPEN, 3x3) on the FAR side (back-left, low-z).
# WALLS y0-y1: back wall (3 logs) + ONE short side wall (2 logs); front + one side OPEN to the fire.
# ROOF: a single SHED-pitch course of spruce_stairs all facing the open front -- high edge on the
# 2-tall back wall, low edge over the open front lintel. Under it: a hay-block bed corner.
# =====================================================================================
LX, LZ = 0, 0                                    # shelter footprint x0..2, z0..2 (far back-left)
# raised floor under the shelter (its own laid cells already there); BACK WALL (low-z, z=LZ) 3 logs:
S.box(LX, LZ+0.0, 0.9, 3, 0.6, 1.3, WLOG, seam=True)   # back wall run (3 wide) -- the LOW side of the shed
# ONE short SIDE wall (left, x=LX) 2 logs deep, raked up toward the open front -> the 'L'. front + right OPEN.
S.box(LX, LZ+0.6, 0.9, 0.6, 1.4, 2.6, WLOG2, seam=True)
# front (OPEN-side) posts -- TALLER than the back wall so the roof slopes DOWN toward the back.
# A real lean-to leans its high open front toward the fire; the back wall is the LOW side.
S.box(LX+2.4, LZ+1.8, 0.9, 0.6, 0.6, 3.0, WLOG2)       # FRONT-right post (tall -> carries the high eave)
S.box(LX+0.0, LZ+1.8, 0.9, 0.6, 0.6, 3.0, WLOG2)       # front-left post (tall, the open face)
S.box(LX+0.0, LZ+1.8, 3.9, 2.4, 0.4, 0.4, WLOG)        # front lintel spanning the two tall posts (eave plate)
# SHED ROOF: spruce_stairs all facing one way; HIGH over the OPEN front (y4), each course stepping
# DOWN + BACK to the 2-tall back wall (y2.6). Big y-deltas + staggered depth so each step reads.
S.box(LX-0.3, LZ+1.6, 3.9, 3.6, 1.0, 0.5, ROOF)        # front eave (HIGH, proud over the tall open front)
S.box(LX-0.2, LZ+0.9, 3.3, 3.4, 1.0, 0.5, ROOF2)       # 2nd course steps DOWN + back (lighter -> reads pitch)
S.box(LX-0.1, LZ+0.2, 2.7, 3.2, 1.0, 0.5, ROOF)        # 3rd course steps DOWN again onto the back wall
S.box(LX-0.3, LZ-0.3, 2.2, 3.6, 0.9, 0.5, ROOF2)       # back eave (LOWEST, proud over the low back wall)
# hay-block bed corner tucked under the shelter (against the back + side walls -> grounded, not loose)
S.box(LX+0.6, LZ+0.6, 0.9, 1, 1, 0.6, HAY)

# =====================================================================================
# SEATING ARC: 4 stripped_oak seats in an arc wrapping the fire's far/left side (2 as 2-block
# benches); a 2-high crate stack (barrels) near the lean-to. Open toward the road.
# =====================================================================================
S.box(HX-1.0, HZ-0.5, 0.9, 0.6, 2.5, 0.5, OAK)         # LEFT bench (2-block, axis z)
S.box(HX-1.0, HZ-0.5, 0.9, 0.6, 0.55, 0.5, OAKE)       #   near end-grain
S.box(HX-1.0, HZ+1.45,0.9, 0.6, 0.55, 0.5, OAKE)       #   far end-grain
S.box(HX+0.2, HZ-1.0, 0.9, 2.5, 0.6, 0.5, OAK)         # BACK bench (2-block, axis x)
S.box(HX+0.2, HZ-1.0, 0.9, 0.55, 0.6, 0.5, OAKE)       #   end-grain
S.box(HX+2.2, HZ-1.0, 0.9, 0.55, 0.6, 0.5, OAKE)       #   end-grain (reads 2 logs)
# crate stack (2 barrels high) just off the OPEN front of the lean-to, grounded on the court.
# Tucked against the tall front-left post (chained to the structure, not loose/floating).
S.box(LX+0.05, LZ+2.5, 0.9, 1, 1, 1, BARR, seam=True)  # crate base (abuts the front-left post)
S.box(LX+0.05, LZ+2.5, 1.9, 1, 1, 1, BARR, seam=True)  # crate top (stacked on base -> grounded)
S.box(LX+0.05, LZ+2.5, 2.85, 1, 1, 0.16, BARRT)        # top hoop band

# =====================================================================================
# POST CLUSTER (the signature grows): a 3-tall spruce post on a floor plinth, TWO side-arms each
# with a chain + hung lantern, and a wayfinding SIGN-POST board. ONE ground lantern at the foot.
# Placed on the ROAD side (front-right) by the apron so it greets the wayfarer. Fully grounded.
# =====================================================================================
PX, PZ = 6, 6                                    # post foot on the road side
S.box(PX, PZ, 0.5, 1, 1, 0.5, PLINTH)            # floor-block plinth the post stands on
S.box(PX+0.2, PZ+0.2, 1, 0.6, 0.6, 0.4, SPRE)    # dark base band (reads the step-up)
S.box(PX+0.25, PZ+0.25, 1.4, 0.5, 0.5, 3.0, SPR, seam=True)  # the 3-tall spruce shaft (taller than Path)
# TWO side-arms at the top (axis x toward the fire, axis z toward the road) -- the doubled signature
S.box(PX-0.55, PZ+0.3, 4.0, 0.8, 0.4, 0.4, SPR)  # arm A (juts toward the fire, axis x)
S.box(PX+0.3, PZ-0.55, 4.0, 0.4, 0.8, 0.4, SPR)  # arm B (juts toward the road, axis z)
S.box(PX-0.45, PZ+0.42, 3.68, 0.16, 0.16, 0.32, CHAIN)  # chain under arm A
S.box(PX+0.42, PZ-0.45, 3.68, 0.16, 0.16, 0.32, CHAIN)  # chain under arm B
# wayfinding SIGN-POST: a board on a short post by the apron mouth (supplementaries:sign_post)
S.box(PX+1.2, PZ+1.0, 0.5, 0.5, 0.5, 2.2, SPRE)  # sign post (short, grounded by the apron)
S.box(PX+0.5, PZ+1.0, 2.0, 1.6, 0.4, 0.9, SIGN)  # the wayfinding board (turned to the road/front)

# =====================================================================================
# ACCENTS: campfire flame, TWIN hung post lanterns, ONE ground lantern at the post foot, + a soft
# fill on the sign so the wayfinding reads. ~3 lit sources (Road's first proper lighting).
# =====================================================================================
S.accent(HX+1.5, HZ+1.5, 1.5, "glow", "#ff9a3c", r=3.4)   # campfire flame
S.accent(PX-0.05, PZ+0.5, 3.45, "glow", LANT, r=2.2)      # hung lantern A (under fire-side arm)
S.accent(PX+0.5, PZ-0.05, 3.45, "glow", LANT, r=2.2)      # hung lantern B (under road-side arm)
S.accent(PX+0.5, PZ+0.5, 1.0, "glow", LANT, r=1.9)        # ground lantern at the post foot

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(LX+1.5, LZ+1, 3.0, "FIRST built shelter -- L-lean-to, real one-way SHED roof, hay bed")
S.label(PX+0.3, PZ+0.3, 4.0, "post grows to 3 tall -- TWIN arms + hung lanterns + a sign-post")
S.label(HX+1.5, HZ+1.5, 1.5, "dressed 3x3 ring (slab-capped corners) + a cauldron cook-spot")
S.label(HX-1.0, HZ+1, 0.9, "4-seat arc wrapping the fire + a 2-high crate stack")
S.label(4, 9, 0.5, "laid 9x9 court (cobble/brick scatter) + a 3-wide dirt apron to the road")

out = S.svg(title="rest_stop R3 (Road) -- a place built for staying: laid court, dressed hearth + cauldron, the FIRST shed-roof lean-to, twin-lantern post",
            size_label="9x9 court * h5 * 3 lanterns (the first NBT template -- a roofed shelter + a built hearth)",
            label_w=360)
open("detail_svg/rest_stop_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/rest_stop_road.svg | bytes", len(out.encode()))
