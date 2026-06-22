"""rest_stop PATH (R2) -> detail_svg/rest_stop_path.svg.
Per deco_catalog_v2.json id 'rest_stop' tier Path (footprint 7x7, height 3, KIND=data, no template):
a real maintained STOP, not a fire someone left. Over the Trail it adds ONE clear new idea -- the
first TRAVELLER'S POST: a 2-tall spruce standard on a path footing with a side-arm jutting at the
top, a chain, and the FIRST hanging LANTERN (the lit, vertical signature that escalates all the way
up the ladder to the Great Road's 12-tall wayshrine mast). Plus the hearth grows from a half-ring to
a small 3x3 fire RING (8 stones, hollow centre) with ONE stone swapped for a slab so a pot could sit
(the WNL 'half-built ring with a deliberate slab-gap' tell), an OPEN seating ARC of 3 flat log seats
wrapping ~1/3 round the fire on the far side (never an enclosing square), and storage -- a barrel +
upright stump side-table with a potted plant.

Still HUMBLE: pure data scatter, only the one post-lantern + a ground lantern lit (the big lit/built
leaps are saved for Road/Highway -- non-linear ladder). Same wnl_rest_stop registry/palette resolver
as the Great Road top (render_rest_stop.py); hash drives the arc rotation, which ring-stone is the
slab gap, the campfire facing + the post side.
Inspiration (FORM/technique only, never copied; CREDITS.md): roadside-camp 'middles' in CTOV /
Moog's Paths; the traveller's lantern-post a wayfarer would actually raise. Vanilla blocks only.
ISO: road is at the FRONT (high-z); the post stands on the ROAD side, the seating arc on the FAR side."""
from iso_render import Iso

S = Iso(U=20)

# ---- palette (literal) -- DISTINCT tones, WIDE luminance ladder so every element reads ----
GRASS = "#6f8a47"   # biome top block at the rim (grass shows through -- 'bare ground reads')
PACK  = "#6a5436"   # packed_mud worn middle (the trodden core -- warm earth)
PATH  = "#7c6038"   # dirt_path scatter (a touch lighter -> reads as a 2nd ground block)
COARSE= "#856a44"   # coarse_dirt rim scatter (lightest earth, thinning toward the grass)
SOIL  = "#574631"   # dug fire hollow (darkest earth)
RING  = "#8a8276"   # cobblestone fire-ring stones (mid stone -- the only masonry, so flame pops)
RING2 = "#73695d"   # darker cobble pick (a worn ring stone -> the ring isn't one flat tone)
SLAB  = "#9b9488"   # the ONE cobblestone_slab gap-stone (lighter + lower -> reads as the 'used' gap)
CAMP  = "#5a4427"   # campfire charred log bed
EMBER = "#caa24e"   # campfire ember glow band (under the flame accent)
OAK   = "#b89160"   # stripped_oak seats / bench (pale warm timber)
OAKE  = "#8f6e44"   # stripped_oak end-grain / the upright stump side-table (darker cut ring)
SPR   = "#9a7a4c"   # stripped_spruce POST shaft + side-arm (distinct mid timber -> the vertical reads)
SPRE  = "#6f5230"   # spruce post footing block + the darker base band (grounds the post)
BARR  = "#7a5c3a"   # barrel body (warm storage timber)
BARRT = "#caa24e"   # barrel hoop/top band (gold ring -> reads as a barrel, not a plain block)
CHAIN = "#54545c"   # chain under the side-arm (dark iron)
POT   = "#9c6b4a"   # terracotta flower-pot on the barrel
PLANT = "#5f8a3f"   # potted plant green
LANT  = "#ffd47a"   # lantern glow (FIRST lit tier proper -- the hung post lantern + 1 ground)

# =====================================================================================
# SUBSTRATE: cleared 7x7 patch. Grass rim shows through; a worn packed-mud middle thins to
# coarse_dirt + grass at the rim. Laid 1 thin course, sunk flush -> reads as trodden ground.
# =====================================================================================
# grass rim (one cell border all round = 'bare ground shows through')
for gx in range(7):
    S.box(gx, 0, 0, 1, 1, 0.5, GRASS)            # back rim
    S.box(gx, 6, 0, 1, 1, 0.5, GRASS)            # front rim
for gz in range(1, 6):
    S.box(0, gz, 0, 1, 1, 0.5, GRASS)            # left rim
    S.box(6, gz, 0, 1, 1, 0.5, GRASS)            # right rim
# worn trodden middle (5x5 inner): packed-mud core, dirt_path + coarse scatter, hash-mixed.
INNER = {
    (1,1):COARSE,(2,1):PATH, (3,1):PACK, (4,1):COARSE,
    (1,2):PATH,  (2,2):PACK, (3,2):PACK, (4,2):PATH,
    (1,3):PACK,  (2,3):PACK,            (4,3):PACK,
    (1,4):COARSE,(2,4):PATH, (3,4):PACK,(4,4):COARSE,
    (3,5):PATH,  (2,5):COARSE,
}
for (sx, sz), col in INNER.items():
    S.box(sx, sz, 0, 1, 1, 0.5, col)

# =====================================================================================
# HEARTH: a small 3x3 fire RING (8 stones, hollow centre) set OFF-center toward the ROAD (front),
# with ONE ring-stone replaced by a cobblestone_slab so a pot could sit -- the deliberate 'used' gap.
# Campfire in the hole. The ring stones each abut their neighbour -> a real ring, never floaty.
# =====================================================================================
HX, HZ = 2, 2                                    # ring foot, centre at (HX+1, HZ+1)
S.box(HX+1, HZ+1, 0, 1, 1, 0.5, SOIL)            # dug hollow in the ring centre (reads sunk)
# the 8 ring stones (3x3 perimeter), one is the SLAB gap (front-east -> turned to the road)
RINGCELLS = [
    (HX,   HZ,   RING2), (HX+1, HZ,   RING),  (HX+2, HZ,   RING),    # back row
    (HX,   HZ+1, RING),                        (HX+2, HZ+1, RING2),  # sides
    (HX,   HZ+2, RING),  (HX+1, HZ+2, RING2),                        # front-left + front-mid
]
for sx, sz, col in RINGCELLS:
    S.box(sx, sz, 0.5, 1, 1, 0.55, col, seam=True)
# the ONE slab gap-stone (front-east corner, lower -> a pot/pan could sit) -- turned to the road
S.box(HX+2, HZ+2, 0.5, 1, 1, 0.32, SLAB)
# campfire in the hollow (charred bed + ember band; flame is the accent)
S.box(HX+1.12, HZ+1.12, 0.5, 0.76, 0.76, 0.34, CAMP)
S.box(HX+1.18, HZ+1.18, 0.82, 0.64, 0.64, 0.18, EMBER)

# =====================================================================================
# SEATING ARC (the hub): a shallow OPEN arc of 3 flat log seats wrapping ~1/3 round the fire on the
# FAR side (the back/left, away from the road) -- never an enclosing square. One seat is a 2-block
# bench (two logs end-to-end). All grounded flat on the patch (1 course).
# =====================================================================================
S.box(HX-1.0, HZ,   0.5, 0.6, 2, 0.5, OAK)       # LEFT seat -- a 2-block bench (logs end-to-end, axis z)
S.box(HX-1.0, HZ,   0.5, 0.6, 0.55, 0.5, OAKE)   #   its near cut end-grain ring
S.box(HX-1.0, HZ+1.45,0.5,0.6, 0.55, 0.5, OAKE)  #   its far cut end-grain ring (reads 2 logs)
S.box(HX, HZ-1.0, 0.5, 2, 0.6, 0.5, OAK)         # BACK seat (single log, axis x) -- closes the arc's 2nd third
S.box(HX, HZ-1.0, 0.5, 0.55, 0.6, 0.5, OAKE)     #   its cut end-grain ring
# (front + right are OPEN -- the arc wraps only the far side, the road side stays clear)

# =====================================================================================
# STORAGE: 1 barrel (facing up) + 1 upright stump side-table by the bench, with a potted plant.
# Tucked to the back-left corner beside the seating arc. Grounded on the patch.
# =====================================================================================
S.box(HX-1.4, HZ-1.4, 0.5, 1, 1, 1, BARR, seam=True)   # barrel body (1 tall)
S.box(HX-1.4, HZ-1.4, 1.4, 1, 1, 0.18, BARRT)          # barrel top hoop band (gold ring -> reads barrel)
S.box(HX-0.4, HZ-1.4, 0.5, 0.7, 0.7, 0.85, OAKE, seam=True)  # upright stump side-table beside it
# a flower-pot on the barrel top (storage + a tended touch)
S.box(HX-1.25, HZ-1.25, 1.58, 0.5, 0.5, 0.4, POT)      # terracotta pot
S.box(HX-1.18, HZ-1.18, 1.98, 0.36, 0.36, 0.35, PLANT) # the plant tuft

# =====================================================================================
# TRAVELLER'S POST (the SIGNATURE, FIRST appearance): a 2-tall spruce standard on a path footing,
# a side-arm jutting at the top, a chain under the arm, and the FIRST hanging LANTERN. Placed on the
# ROAD side (front) so it greets the wayfarer. Fully grounded -- footing -> shaft -> arm -> chain.
# =====================================================================================
PX, PZ = 4, 5                                    # post foot on the road side (front-right of the fire)
S.box(PX, PZ, 0.5, 1, 1, 0.5, SPRE)              # path/footing block the post stands on (grounded)
S.box(PX+0.2, PZ+0.2, 1, 0.6, 0.6, 0.4, SPRE)    # darker base band (reads the step-up onto the shaft)
S.box(PX+0.25, PZ+0.25, 1.4, 0.5, 0.5, 2.0, SPR, seam=True)  # the 2-tall spruce shaft (the vertical)
# side-arm jutting toward the fire (back/left) at the top -- a 1-block log nub, axis x
S.box(PX-0.55, PZ+0.3, 3.1, 0.8, 0.4, 0.4, SPR)  # the side-arm (juts back over the path, grounded on shaft)
# chain hanging under the arm tip, then the lantern on the chain (both abut the arm -> nothing floats)
S.box(PX-0.45, PZ+0.42, 2.78, 0.16, 0.16, 0.32, CHAIN)  # chain link run under the arm tip

# =====================================================================================
# ACCENTS: the campfire flame, the hung post lantern (FIRST), and ONE ground lantern at the post
# foot (Path = the first proper lit tier, but kept to 2 lit sources -- humble, not the Road blaze).
# =====================================================================================
S.accent(HX+1.5, HZ+1.5, 1.1, "glow", "#ff9a3c", r=3.2)   # campfire flame
S.accent(PX-0.05, PZ+0.5, 2.55, "glow", LANT, r=2.2)      # the hung post lantern (under the arm)
S.accent(PX+0.5, PZ+0.5, 0.95, "glow", LANT, r=1.9)       # one ground lantern at the post foot

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(PX-0.1, PZ+0.5, 2.6, "FIRST traveller's post -- side-arm + chain + the first HUNG lantern")
S.label(HX+1.5, HZ+1.5, 1.0, "3x3 fire ring -- ONE stone swapped for a slab (a pot could sit)")
S.label(HX-1.0, HZ+1, 0.6, "open seating ARC -- 3 log seats on the FAR side (never a square)")
S.label(HX-1.4, HZ-1.4, 1.6, "barrel + stump side-table + a potted plant (storage)")
S.label(3, 6, 0.5, "7x7 patch -- packed-mud middle thins to grass at the rim")

out = S.svg(title="rest_stop R2 (Path) -- a maintained stop: fire ring, open seating arc, storage, the FIRST traveller's post + hung lantern",
            size_label="7x7 patch * h3 * 2 lanterns (a tended footpath stop -- the lit vertical post signature begins)",
            label_w=356)
open("detail_svg/rest_stop_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/rest_stop_path.svg | bytes", len(out.encode()))
