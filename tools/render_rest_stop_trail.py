"""rest_stop TRAIL (R1, floor of the ladder) -> detail_svg/rest_stop_trail.svg.
Per deco_catalog_v2.json id 'rest_stop' tier Trail (footprint 5x5, height 2, KIND=data, no template):
the most humble rung -- a traveller's casual FIRE someone stopped at, not a built thing. A cleared
5x5 patch of bare ground showing the biome top block, a loose hash-scatter of dirt_path/coarse_dirt
densest around the fire and thinning to untouched grass at the rim, ONE campfire on a cobblestone
base with a single ring-stone tucked against ONE side only (the asymmetric HALF-ring -- never a closed
circle, the WNL 'half-built fire ring' signature in its embryonic form), one sit-log laid flat on the
side AWAY from the road, and one upright stump a block off as a side-table. UNLIT (rendered as the
remote/worn trail case so 'dead reads dead' -- the catalog omits the lantern far from civ; the big
lit leaps are saved for Road/Highway -- non-linear ladder curve).

This establishes the asymmetric HEARTH-AND-HUB geometry every higher tier inherits: off-center fire,
open seat on one side, half-ring on another. Same wnl_rest_stop registry/palette resolver as the
Great Road top (render_rest_stop.py); the data builder hashes the campfire facing, seat side, scatter
count + which ring-stone live per stop.
Inspiration (FORM/technique only, never copied; CREDITS.md): the universal roadside campfire a traveller
leaves; CTOV / Moog's Paths roadside-camp 'middles'. Vanilla blocks only; original geometry.
ISO: road is at the FRONT (high-z); the fire sits off-center TOWARD the road, the seat on the far side."""
from iso_render import Iso

S = Iso(U=24)

# ---- palette (literal) -- DISTINCT tones on a clear luminance ladder so every material reads ----
# Ground ladder kept LOW + earthy (this is bare trodden ground); the cobble + logs are the only
# 'placed' tones and they sit only a touch brighter so nothing competes with the future tiers' stone.
GRASS = "#6f8a47"   # biome top block showing through at the rim (grass_block -- 'bare ground reads')
PATH  = "#6a5436"   # dirt_path scatter -- the trodden core (warm earth, the densest middle)
COARSE= "#7a5f3c"   # coarse_dirt scatter -- lighter earth pick, reads as a 2nd scatter block
SOIL  = "#5c4a30"   # dug/worn cell under the densest tread (darkest earth -> the fire's bare hollow)
RING  = "#8a8276"   # cobblestone hearth base + the one half-ring stone (mid stone, the only masonry)
RING2 = "#73695d"   # darker cobble pick on the base lip (reads the laid base, not one flat tile)
CAMP  = "#5a4427"   # campfire log bed (dark charred timber under the flame)
EMBER = "#caa24e"   # campfire's lit log glow band (warm, sits under the flame accent)
LOG   = "#b89160"   # stripped_oak sit-log (pale warm timber -> pops off the dark earth)
LOGE  = "#8f6e44"   # stripped_oak end-grain / the upright stump (darker ring -> reads the cut face)

# =====================================================================================
# SUBSTRATE: a cleared 5x5 patch. The biome top block (grass) shows at the RIM; the trodden
# earth scatter fills the middle. Laid 1 course thick, sunk flush so it reads as ground, not a slab.
# (Render the patch as a thin ground plane: y0 cells, dy<1 so they sit IN the terrain.)
# =====================================================================================
# rim ring = untouched grass showing through (the 'bare ground' read), one cell border all round
for gx in range(5):
    S.box(gx, 0, 0, 1, 1, 0.5, GRASS)            # back rim
    S.box(gx, 4, 0, 1, 1, 0.5, GRASS)            # front rim
for gz in range(1, 4):
    S.box(0, gz, 0, 1, 1, 0.5, GRASS)            # left rim
    S.box(4, gz, 0, 1, 1, 0.5, GRASS)            # right rim
# trodden EARTH scatter over the inner 3x3 -- hash-placed, densest at the fire, mixed path/coarse.
# (each cell abuts its neighbour -> one continuous trodden patch, never floating cells.)
SCATTER = [
    (1, 1, COARSE), (2, 1, PATH),  (3, 1, COARSE),
    (1, 2, PATH),                  (3, 2, PATH),
    (1, 3, COARSE), (2, 3, PATH),  (3, 3, COARSE),
]
for sx, sz, col in SCATTER:
    S.box(sx, sz, 0, 1, 1, 0.5, col)
# a couple of stray trodden cells creeping toward the rim (thinning scatter, still abutting inner)
S.box(2, 0, 0, 1, 1, 0.42, COARSE)               # one tread reaching the back rim (chains to (2,1))
S.box(3, 4, 0, 1, 1, 0.42, PATH)                 # one tread reaching the front (road) rim

# =====================================================================================
# HEARTH (off-center ~1 toward the ROAD/front): a cobblestone fire-base + a campfire, with ONE
# ring-stone tucked against a SINGLE side only -- the asymmetric HALF-ring (never a closed circle).
# Centre cell of the inner patch is the dug hollow the fire sits in.
# =====================================================================================
HX, HZ = 2, 2                                    # fire on the centre cell, nudged toward front below
S.box(HX, HZ, 0, 1, 1, 0.5, SOIL)                # dug hollow the fire sits in (darkest -> reads sunk)
S.box(HX, HZ, 0.5, 1, 1, 0.4, RING)              # cobblestone fire-base proud of the scatter (laid)
S.box(HX, HZ, 0.5, 0.45, 1, 0.42, RING2)         # darker cobble lip on the base west edge (laid read)
# the campfire itself: a charred log bed + an ember band; the flame is an accent above it.
S.box(HX+0.12, HZ+0.12, 0.9, 0.76, 0.76, 0.32, CAMP)   # charred log bed
S.box(HX+0.18, HZ+0.18, 1.18, 0.64, 0.64, 0.18, EMBER) # lit ember band under the flame
# the ONE half-ring stone -- a single cobble tucked against the FRONT (road-facing) side only.
# Abuts the fire-base front face; this is the embryo of the half-built ring the higher tiers grow.
S.box(HX+0.05, HZ+0.95, 0.5, 0.9, 0.55, 0.55, RING)

# =====================================================================================
# SEAT: one stripped_oak sit-log laid FLAT on the side AWAY from the road (the BACK, low-z), plus
# one upright stump a block off as a side-table. Both grounded flat on the trodden patch.
# =====================================================================================
S.box(HX-0.5, HZ-1.0, 0.5, 2, 0.55, 0.5, LOG)    # sit-log laid flat behind the fire (axis along x)
S.box(HX-0.5, HZ-1.0, 0.5, 0.3, 0.55, 0.5, LOGE) # its cut end-grain ring (reads the log end)
# upright stump 1 block to the side of the log (a side-stump table), grounded on the patch.
S.box(HX-1.4, HZ-0.95, 0.5, 0.7, 0.7, 0.95, LOGE, seam=True)

# =====================================================================================
# ACCENT: the campfire flame -- the ONLY warmth on a Trail (UNLIT otherwise: no lantern far from
# civ, so 'dead reads dead'). One soft flame proud of the ember band.
# =====================================================================================
S.accent(HX+0.5, HZ+0.5, 1.5, "glow", "#ff9a3c", r=3.4)

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(HX+0.5, HZ+0.5, 1.4, "one campfire on a cobble base -- the only warmth (UNLIT trail)")
S.label(HX+0.5, HZ+1.4, 1.0, "ONE ring-stone, one side only -- the half-ring (never a circle)")
S.label(HX-0.5, HZ-1.0, 0.9, "sit-log laid flat on the side AWAY from the road + a side-stump")
S.label(3, 4, 0.5, "loose dirt-path scatter -- densest at the fire, grass shows at the rim")

out = S.svg(title="rest_stop R1 (Trail) -- a traveller's casual campfire: half-ring hearth, one sit-log, bare ground, unlit",
            size_label="5x5 cleared patch * h2 * 0 lanterns (ladder floor -- a fire someone stopped at, not a built stop)",
            label_w=352)
open("detail_svg/rest_stop_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/rest_stop_trail.svg | bytes", len(out.encode()))
