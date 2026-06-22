"""Well PATH (R2) -> detail_svg/well_path.svg.
Per deco_catalog_v2.json id 'well' tier Path (footprint 5x5, height 4): a modest jump from the
Trail spring -- the water becomes a REAL 3x3 basin (not a 1x1 hole) inside a dressed cobble rim,
and the piece gains its FIRST SPOUT: a back stone-brick pillar topped by a carved stair spout-head
that visibly trickles flowing water down into the pool. Still open-topped + small (no posts, no
roof yet -- the big leaps are saved for Road/Highway, a non-linear ladder).

Massing (per catalog, graph-paper explicit):
 * y0: centre 3x3 = minecraft:water over a cobble floor (a true square pool); outer 16-cell ring =
   cobblestone + 4 mossy_cobblestone corners + 1 cobble approach apron where the road meets it.
 * y1: rim wall on the 12 non-apron perimeter cells (cobblestone_wall) + 2 chiseled_stone_bricks
   PIER blocks at the two front corners (the first 'dressed' note); apron stays an open kneeling step.
 * y2: the SPOUT -- a stone_brick_wall pillar 2 tall on the back face, topped by a stone_brick_stairs
   spout-head leaning out over the pool; a water source in the stair-notch trickles into the basin.
 * y3: a grounded lantern on the spout pillar top; a barrel beside the apron; light decay moss.

Same wnl_well builder as render_well.py (the Great Road fountain-house top tier). Inspiration
(form/technique ONLY, credited CREDITS.md; NO assets/NBT copied): Roman castellum-aquae street
fountains + medieval village watering points -- the dressed-rim basin + carved spout as the first
'tended watering point'. The signature draw is WATER ARCHITECTURE (a visible trickling spout),
deliberately NOT a chain-and-bucket. Entirely original WNL vanilla-block build.
ISO: road-facing FRONT = high-z (south) + high-x (east); apron + front piers + spout face the front."""
from iso_render import Iso

S = Iso(U=20)

# ---- palette (literal) -- wide-contrast ladder: cool ring stone, warm mossy corners, pale dressed
#      piers, dark basin floor under saturated water, warm timber for the lone barrel ----
COBB   = "#8a8276"   # minecraft:cobblestone ring + basin floor (cool mid grey, the base mass)
MOSS   = "#6f7d56"   # minecraft:mossy_cobblestone corners (green-grey, controlled weathering)
APRON  = "#9b9488"   # cobblestone approach apron (a touch lighter -> the open kneeling step reads)
WALL   = "#a39b8c"   # minecraft:cobblestone_wall rim lip (dressed-ish nub, lighter than the ring)
PIER   = "#cdc7b6"   # minecraft:chiseled_stone_bricks front piers (pale dressed -> first 'dressed' note)
SBW    = "#b3ada0"   # minecraft:stone_brick_wall spout pillar (pale grey, the back gantry)
SPOUT  = "#c4beb0"   # minecraft:stone_brick_stairs carved spout-head (bright -> the spout reads)
FLOOR  = "#5d5a50"   # basin floor stone under the water (dark warm grey -> water sits clearly above)
WATER  = "#2f74b6"   # minecraft:water 3x3 basin pool (deep saturated blue -- unmistakable)
WATER2 = "#5aa8e2"   # flowing-spout / surface highlight water (bright cyan-blue -> the trickle reads)
BARREL = "#7c5a34"   # minecraft:barrel beside the apron (warm oak)
BARLID = "#9a7647"   # barrel rim/lid band (brighter amber -> reads as a barrel not a cube)
MOSSBK = "#586f3a"   # minecraft:moss_block decay creep on a back corner (greener)
LANT   = "#ffd47a"   # lantern glow (one grounded light on the spout pillar)

# grid: 5x5 footprint x 0..5, z (depth) 0..5. centre 3x3 pool = x1..4 z1..4. apron on the FRONT (z=4).
# ============================ COURSE 0 (y=0): dressed cobble ring + REAL 3x3 water basin ============================
# outer 16-cell perimeter ring, built per-cell: corners mossy, edges cobble, ONE front edge = apron.
RING0 = {
    (0,0):MOSS,(1,0):COBB,(2,0):COBB,(3,0):COBB,(4,0):MOSS,            # back row (z=0, far)
    (0,1):COBB,                              (4,1):COBB,               # mid rows -- flanks only
    (0,2):COBB,                              (4,2):COBB,               #   (centre 3x3 is the pool)
    (0,3):COBB,                              (4,3):COBB,
    (0,4):MOSS,(1,4):COBB,(2,4):APRON,(3,4):COBB,(4,4):MOSS,           # front row (z=4) -- (2,4)=apron
}
for (cx,cz),col in RING0.items():
    S.box(cx, cz, 0, 1, 1, 1, col, seam=True)
# the basin: a cobble floor under a recessed 3x3 water pool (water one course down inside the rim).
S.box(1, 1, 0, 3, 3, 0.55, FLOOR)              # basin floor (recessed tray under the water)
S.box(1, 1, 0.55, 3, 3, 0.4, WATER)            # the 3x3 WATER pool, sitting one course recessed
S.box(1.5,1.5,0.93, 2, 2, 0.06, WATER2)        # bright surface sheen on the pool (reads as wet)

# ============================ COURSE 1 (y=1): rim wall on 12 cells + 2 front chiseled PIERS ============================
# cobblestone_wall lip on the 12 non-apron perimeter cells (the drinking rim); the apron cell at
# (2,4) stays OPEN as a low kneeling step so the viewer sees into the basin from the front.
WALLCELLS = [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(4,1),(0,2),(4,2),(0,3),(4,3),(0,4),(4,4)]
for (cx,cz) in WALLCELLS:
    S.box(cx, cz, 1, 1, 1, 0.7, WALL, seam=True)   # rim-wall nub (<1 tall -> a lip, not a parapet)
# the two FRONT-CORNER cells become dressed chiseled_stone_bricks PIERS (the first dressed note),
# full-height blocks so they read as little dressed posts framing the road-facing approach.
S.box(1, 4, 1, 1, 1, 1, PIER, seam=True)       # front-west pier (flanks the apron, road side)
S.box(3, 4, 1, 1, 1, 1, PIER, seam=True)       # front-east pier
# (apron cell (2,4) is left OPEN at y1 -> the kneeling step the viewer reads into the water through)

# ============================ COURSE 2 (y=2): the FIRST SPOUT -- back pillar + carved stair spout-head ============================
# a stone_brick_wall pillar 2 tall rises on the BACK face (behind the water, so it never occludes
# the pool from the road side); a stone_brick_stairs spout-head leans FORWARD over the basin and a
# water source in the notch trickles visibly down into the 3x3 pool. The signature WATER draw.
SPX, SPZ = 2, 0                                 # spout pillar on the back-centre rim cell (z=0)
S.box(SPX, SPZ, 1, 1, 1, 1, SBW, seam=True)    # pillar course 1 (rises off the back rim, y=1..2)
S.box(SPX, SPZ, 2, 1, 1, 1, SBW, seam=True)    # pillar course 2 (the 2-tall stone_brick_wall gantry)
# carved spout-head: a stair block leaning out toward the pool (south, +z), notch facing the basin.
S.box(SPX, SPZ+0.55, 3, 1, 0.7, 0.55, SPOUT)   # stone_brick_stairs spout-head, oversailing the basin
# the visible flowing water: a thin column from the spout-notch down into the front of the pool
S.box(SPX+0.3, SPZ+0.85, 1.0, 0.4, 0.4, 2.0, WATER2)  # the trickling spout stream (grounded in the pool)

# ============================ COURSE 3 (y=3): lantern on the spout pillar + a barrel + decay moss ============================
# one grounded lantern rests on the spout-pillar top (the only light -- this rung is barely lit).
S.accent(SPX+0.5, SPZ+0.4, 3.2, "glow", LANT, r=2.3)   # grounded lantern over the spout / water
# a single barrel set on the dais beside the front apron (a tended note -- someone draws water here).
S.box(3.95, 3.1, 0, 0.85, 0.85, 1.1, BARREL)   # barrel ABUTTING the east rim (grounded, not floating)
S.box(3.95, 3.1, 1.0, 0.85, 0.85, 0.12, BARLID)# barrel lid band (reads as a barrel)
# light decay: a moss_block creeping onto the back-west corner ring cell (far-from-civ weathering).
S.box(0, 0, 1, 1, 1, 0.22, MOSSBK)             # moss creep on the back-west corner top (grounded)

# water glint accents -- the wet read carries in daylight
S.accent(2.5, 2.5, 1.0, "glow", "#bfe6ff", r=2.0)      # central pool glint
S.accent(2.4, 1.2, 1.0, "glow", "#cfe6ff", r=1.5)      # spout splash where the stream hits the pool

S.label(SPX+0.5, SPZ+0.4, 3.3, "grounded lantern on the spout pillar (the one light)")
S.label(SPX, SPZ+1, 3.2, "FIRST spout -- carved stair-head trickling water into the pool")
S.label(3, 4, 1.4, "two front chiseled-brick PIERS (first 'dressed' note)")
S.label(2.5, 2.5, 1.0, "REAL 3x3 water basin (no more a single hole)")
S.label(2.0, 4.0, 0.5, "open apron kneeling step (the road-facing drinking side)")
S.label(0, 0, 0.5, "dressed cobble rim -- cobblestone + mossy corners")

out = S.svg(title="Well R2 (Path) -- tended village watering point: dressed cobble rim, REAL 3x3 basin, FIRST carved spout trickling water, open-topped",
            size_label="5x5 foot * h4 * 1 lantern (gains a real basin + a dressed rim + the first running spout)",
            label_w=360)
open("detail_svg/well_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/well_path.svg | bytes", len(out.encode()))
