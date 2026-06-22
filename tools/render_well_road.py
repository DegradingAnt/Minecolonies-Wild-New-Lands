"""Well ROAD (R3) -> detail_svg/well_road.svg.
Per deco_catalog_v2.json id 'well' tier Road (footprint 7x7, height 7): the BIG mid-ladder jump --
the open watering point becomes a roofed FOUNTAIN-HOUSE. A 3x3 water basin sits inside a HEXAGONAL
dressed stone-brick rim (corners chamfered so the silhouette reads 6-sided); SIX oak_log posts are
locked to the 6 rim faces, each footed on a stone block, tied by oak-fence cross-braces; they carry
a course-built HIPPED oak roof (written as shrink-ring stair courses). The draw element escalates
from one spout to a TWO-STEP SPOUT-AND-BASIN CASCADE: a back gantry spout-head overflows into a
small raised channel-basin that in turn spills down a stair step into the main pool (water you watch
fall, twice). FIRST hanging lantern on a chain under the ridge + a grounded lantern on the gantry.

Massing (per catalog, graph-paper explicit):
 * y0: 3x3 water over stone_bricks floor; hex rim = stone_bricks(9)+mossy(3)+chiseled(2 front faces);
   a 3-wide stone_brick_slab apron on the road side.
 * y1: stone_brick_wall rim lip (11) + 2 chiseled piers at the front faces (carry front posts);
   inner stone_brick_slab drinking ledge around the water.
 * y2..4: SIX oak_log posts (3 tall) on the 6 hex faces, each on a stone block; oak_fence braces at y3.
 * y3: the two-step cascade (back wall gantry spout-head -> raised smooth_stone_slab channel-basin ->
   stair step -> main pool).
 * y5..6: course-built hipped roof -- y5 eave ring of oak_stairs facing out (overhang), y6 shrink to
   5x5 facing in, centre 1x3 oak_slab ridge, hip-corner oak_stairs.

Same wnl_well builder as render_well.py (Great Road top -- a colonnaded fountain-house). The roofed
fountain-house here is one step grander than the open Path basin, one step humbler than the Highway
monument. Inspiration (form/technique ONLY, credited CREDITS.md; NO assets/NBT copied): Roman
castellum-aquae + medieval town LAVOIRS / well-houses (a covered draw-point as a hub anchor);
course-built rustic hipped roofing technique studied from CTOV / Dungeons & Taverns. The carved
spout-and-cascade WATER ARCHITECTURE is deliberately NOT the chain-and-bucket cliche. Original WNL build.
ISO: road-facing FRONT = high-z (south) + high-x (east); apron, front piers, front-bay read on the front."""
from iso_render import Iso

S = Iso(U=15)

# ---- palette (literal) -- a wide-contrast ladder: cool stone-brick mass, pale dressed chiseled
#      accents, warm oak frame, dark-brown roof against the pale stone, saturated water ----
BRICK  = "#9a958a"   # minecraft:stone_bricks rim + floor (cool mid grey, the base masonry mass)
MOSSB  = "#74815a"   # minecraft:mossy_stone_bricks (controlled weathering on the rim, green-grey)
CHIS   = "#cdc7b6"   # minecraft:chiseled_stone_bricks dressed piers/accent (pale -> the dressed note)
SLAB   = "#b3ada0"   # minecraft:stone_brick_slab apron + drinking ledge (light lip -> reads as a step)
WALL   = "#a39b8c"   # minecraft:stone_brick_wall rim lip (dressed nub between brick + chiseled)
GANTRY = "#beb8aa"   # back stone_brick_wall spout gantry (pale grey, reads behind the bay)
SPOUT  = "#cfc8b6"   # stone_brick_stairs carved spout-head (bright -> the cascade spout reads)
CHAN   = "#c9cdd1"   # minecraft:smooth_stone_slab cascade channel-basin (cool pale -> a fresh tray)
FLOOR  = "#5d5a50"   # basin floor under the water (dark warm grey -> water sits clearly above)
WATER  = "#2f74b6"   # minecraft:water 3x3 pool (deep saturated blue -- unmistakable)
WATER2 = "#5aa8e2"   # flowing cascade / surface highlight water (bright cyan-blue -> moving water reads)
POSTFT = "#a89d88"   # stone-block post footing (warm band -> timber never touches ground)
POST   = "#6f5230"   # minecraft:oak_log posts (deep warm brown, strong vs cool stone)
BRACE  = "#523c22"   # minecraft:oak_fence cross-braces (darker oak -> the tied frame reads)
ROOF   = "#3a2c1f"   # minecraft:oak_stairs hipped roof (dark brown -- max contrast vs pale stone)
ROOFLT = "#54402c"   # roof alternating-course / ridge shade (stepped read)
RIDGE  = "#6a5132"   # minecraft:oak_slab ridge cap (warmer top accent)
BARREL = "#7c5a34"   # minecraft:barrel by the apron
BARLID = "#9a7647"   # barrel lid band
COMP   = "#5e7038"   # minecraft:composter (green-brown, a tended-hub note)
LANT   = "#ffd47a"   # lantern glow
CHAIN  = "#8c8c92"   # minecraft:chain (iron hanging-lantern chain)

# grid: 7x7 footprint x 0..7, z (depth) 0..7. centre 3x3 pool = x2..5 z2..5.
CHAM = BRICK   # chamfered hex corners are pulled in to the rim tone (read as the hex silhouette)

# ============================ COURSE 0 (y=0): hex stone-brick rim + 3x3 water basin + apron ============================
# the 7x7 perimeter ring, per-cell. CORNERS are chamfered (pulled to a stair/slab read) so the
# silhouette is a hexagon; the 6 'face' cells carry the posts. front 3 cells = a stone_brick_slab apron.
RING0 = {
    (1,0):MOSSB,(2,0):BRICK,(3,0):BRICK,(4,0):BRICK,(5,0):MOSSB,        # back face row (z=0)
    (0,1):BRICK,                                    (6,1):BRICK,        # back-flank faces
    (0,2):MOSSB,                                    (6,2):BRICK,
    (0,3):BRICK,                                    (6,3):BRICK,        # mid (centre 3x3 is the pool)
    (0,4):BRICK,                                    (6,4):BRICK,
    (0,5):BRICK,                                    (6,5):MOSSB,        # front-flank faces
    (1,6):CHIS,(2,6):SLAB,(3,6):SLAB,(4,6):SLAB,(5,6):CHIS,             # FRONT row: chiseled face-piers + slab apron
}
for (cx,cz),col in RING0.items():
    S.box(cx, cz, 0, 1, 1, 1, col, seam=True)
# chamfer the 4 true corners back (lower stair-read blocks) so the ring reads 6-sided not square
for (cx,cz) in [(0,0),(6,0),(0,6),(6,6)]:
    S.box(cx, cz, 0, 1, 1, 0.5, BRICK)             # corner chamfer (pulled-in low block -> hex read)
# the basin: stone_bricks floor under a recessed 3x3 water pool
S.box(2, 2, 0, 3, 3, 0.55, FLOOR)                  # basin floor tray
S.box(2, 2, 0.55, 3, 3, 0.4, WATER)                # the 3x3 WATER pool (recessed one course)
S.box(2.5,2.5,0.93, 2,2, 0.06, WATER2)             # pool surface sheen

# ============================ COURSE 1 (y=1): rim wall lip + 2 front chiseled piers + inner drinking ledge ============================
# stone_brick_wall lip on the non-apron, non-front-pier perimeter; the apron stays an open step.
LIPCELLS = [(1,0),(2,0),(3,0),(4,0),(5,0),(0,1),(6,1),(0,2),(6,2),(0,3),(6,3),(0,4),(6,4),(0,5),(6,5)]
for (cx,cz) in LIPCELLS:
    S.box(cx, cz, 1, 1, 1, 0.7, WALL, seam=True)   # rim-wall lip nub (<1 -> drinking rim, not a parapet)
# the inner stone_brick_slab drinking LEDGE on the 4 edge cells immediately around the water
for (cx,cz) in [(2,1),(4,1),(1,2),(5,4),(2,5),(4,5),(1,3),(5,3)]:
    S.box(cx, cz, 0.95, 1, 1, 0.22, SLAB)          # clean slab ledge ring around the pool (no dead annulus)

# ============================ COURSE 2..4 (y=2..4): SIX oak posts on the hex faces + fence braces ============================
# six posts locked to the 6 face cells of the hex, each FOOTED on a stone block (timber off the ground).
POSTS = [(3,0),(0,3),(6,3),(3,6),(1,1),(5,1)]      # 6 hex-face cells (back, two flanks, front, two back-diag)
PH = 3                                              # posts 3 tall (y=2..4)
for (px,pz) in POSTS:
    S.box(px, pz, 1, 1, 1, 0.6, POSTFT)            # dressed stone footing on the rim (timber never on ground)
    S.box(px, pz, 1.6, 1, 1, PH, POST, seam=True)  # the oak_log post (3 tall, warm brown)
# oak_fence cross-braces tie adjacent posts at mid-height (y=3) on the back + two flanks (front bay open)
BRY = 3
S.box(0, 3, BRY, 1, 0.3, 1, BRACE)                 # west brace stub
S.box(6, 3, BRY, 1, 0.3, 1, BRACE)                 # east brace stub
S.box(3, 0, BRY, 0.3, 1, 1, BRACE)                 # back brace stub (tie the back posts)

# ============================ COURSE 3 (y=3): TWO-STEP SPOUT + BASIN CASCADE (the escalated draw) ============================
# a back stone_brick_wall gantry holds a stair spout-head; below it a small raised smooth_stone_slab
# CHANNEL-basin catches the water and overflows down a stair STEP into the main 3x3 pool (cascade x2).
GX, GZ = 3, 0                                       # gantry on the back-centre face
S.box(GX, GZ, 1.6, 1, 1, 2.2, GANTRY, seam=True)   # the 3-tall back gantry (rises off the rim, behind the bay)
S.box(GX, GZ+0.55, 3.6, 1, 0.7, 0.55, SPOUT)       # stair spout-head leaning out over the channel-basin
# the small RAISED channel-basin (a smooth_stone_slab tray) one step down + forward of the spout
S.box(GX-0.05, GZ+1.0, 2.0, 1.1, 1.0, 0.4, CHAN)   # raised channel-basin tray (catches the spout)
S.box(GX+0.1, GZ+1.05, 2.4, 0.8, 0.85, 0.18, WATER)# water sitting in the channel-basin
# water step 1: spout -> channel-basin
S.box(GX+0.3, GZ+0.85, 2.45, 0.4, 0.4, 1.2, WATER2)# the upper trickle (spout into the channel)
# water step 2: channel-basin overflows down a stair into the main pool
S.box(GX+0.25, GZ+1.7, 1.0, 0.45, 0.5, 1.5, WATER2)# the lower cascade (channel -> main pool)

# ============================ COURSE 5..6 (y=5..6): COURSE-BUILT HIPPED OAK ROOF (shrink-rings) ============================
# rests on the 6 posts (post tops ~y=4.6). Built bottom->top as concentric SHRINK-RING courses
# (catalog technique B): each course up is a smaller solid square so the silhouette is a clean
# stepped HIP climbing to a short ridge -- NOT a flat slab. The eave (course 0) overhangs the 7x7.
RY = 5
# thin eave-trim under-course so the overhang reads as an eave (lighter slab beneath the first ring)
S.box(0, 0, RY-0.2, 7, 7, 0.2, ROOFLT)             # eave trim slab (the visible under-eave overhang)
rings = [  # (x,z,dx,dz) per ascending course -- concentric shrink, alternating shade = stepped read
    (0,0,7,7),   # y5  eave course (full 7x7, oversails the posts)
    (1,1,5,5),   # y6  shrink to 5x5
    (2,2,3,3),   # y7  shrink to 3x3
]
for i,(rx,rz,rdx,rdz) in enumerate(rings):
    col = ROOF if i % 2 == 0 else ROOFLT           # alternate course shade -> readable hip steps
    S.box(rx, rz, RY+i, rdx, rdz, 1, col)
# centre 1x3 ridge run (oak_slab) closing the hip on the long axis
S.box(3, 2, RY+len(rings), 1, 3, 0.5, RIDGE)       # the short ridge cap atop the 3x3

# ============================ DETAIL: barrel + composter at the apron ============================
S.box(5.9, 5.0, 0, 0.85, 0.85, 1.1, BARREL)        # barrel abutting the east rim (grounded)
S.box(5.9, 5.0, 1.0, 0.85, 0.85, 0.12, BARLID)     # barrel lid band
S.box(5.95, 6.0, 0, 0.85, 0.85, 0.9, COMP)         # composter beside it (chained to the barrel, grounded)

# ============================ LIGHTING: FIRST hanging lantern on chain under the ridge + gantry lantern ============================
# the chain links from the eave down to a hung lantern over the pool front (the first 'hung' light);
# hung at the FRONT-edge of the bay (z=4.5) so the roof overhang doesn't bury it -> it reads on the road side.
for cy in (RY-0.3, 4.6, 4.0):
    S.accent(3.5, 4.5, cy, "dot", CHAIN, r=0.6)    # chain links eave -> hung lantern (front of bay)
S.accent(3.5, 4.5, 3.6, "glow", LANT, r=2.3)       # the hung lantern over the pool front (on the chain)
# a grounded lantern on the spout gantry top
S.accent(GX+0.5, GZ+0.4, 3.9, "glow", LANT, r=2.0) # grounded gantry lantern over the cascade
# water glints
S.accent(3.4, 3.6, 1.0, "glow", "#bfe6ff", r=1.9)  # pool glint
S.accent(3.4, 2.0, 1.0, "glow", "#cfe6ff", r=1.4)  # splash where the cascade hits the pool

S.label(3.5, 3.5, 4.4, "FIRST hanging lantern on chain (under the ridge)")
S.label(3, 3, RY+1.2, "course-built hipped OAK roof (shrink-ring courses)")
S.label(GX, GZ+1.5, 3.4, "two-step SPOUT + channel-basin CASCADE (water falls twice)")
S.label(0, 3, 3.0, "SIX oak posts on the hex faces (footed on stone)")
S.label(3.5, 3.5, 1.0, "3x3 pool inside a chamfered HEXAGONAL stone-brick rim")
S.label(3, 6, 0.5, "stone-brick slab apron + 2 front chiseled piers (road side)")

out = S.svg(title="Well R3 (Road) -- the fountain-house arrives: hexagonal stone-brick rim, SIX oak posts, course-built hipped roof, two-step spout cascade",
            size_label="7x7 foot * h7 * 2 lanterns (open basin -> roofed running fountain-house: +roof +6 posts +cascade)",
            label_w=372)
open("detail_svg/well_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/well_road.svg | bytes", len(out.encode()))
