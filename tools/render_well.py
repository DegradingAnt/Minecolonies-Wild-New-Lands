"""Well R5 (Great Road) detail render -> detail_svg/well.svg.
A roofed civic DRAW-WELL / fountain-house: a two-step stone dais carries a clean octagonal
dressed rim around ONE clear central water basin + well shaft; FOUR stout timber posts (on the
four octagon corners) visibly carry a tied ring-beam and a solid course-built hipped roof; over
the shaft a WINDLASS (a turned beam on two short uprights) lowers a bucket on a chain into the
visible water -- the unmistakable "this is a well" read. Grounded belfry-cupola crowns the roof.
Built per deco_catalog_v2 'well' Great Road tier (octagon rim + course-built hip + visible water).

REWRITE (author feedback: the old render was "a mess, nothing is clear ... needs fixing
perspective wise" -- ~8 crisscrossing posts, scattered water, a floaty open roof). Fixes:
 * 4 CLEAN posts instead of an 8-post thicket -> the frame reads at a glance and clearly
   SUPPORTS the roof (each post grounded on a dressed pier, tied by a ring-beam the roof sits on);
 * ONE central basin + well shaft with a clear WINDLASS + bucket + chain draw mechanism (plus a
   single thin spout of visible water) -- de-cluttered from the old pier/troughs/3-basin cascade;
 * a SOLID grounded hipped roof (shrink-ring courses) that visibly rests on the 4 posts, not floating.

Conventions copied from render_gatehouse/render_harbour/render_plaza: named literal palette;
posts/timber are WARM and stand against LIGHT dressed stone with base+capital bands that read;
lanterns via accents; right-hand callout labels; a size_label. Everything is GROUNDED.

Credit (form/scale/technique ONLY, never copied -- S8 no-copy): studied Roman castellum-aquae
street fountains + medieval town lavoirs / market-cross well-houses for the roofed civic draw-point,
structurize big-well + MineColonies wells for the civic-well ROLE, and CTOV / Dungeons & Taverns
rustic roofing for the course-built hip. Entirely original WNL vanilla-block build."""
from iso_render import Iso

S = Iso(U=11, occlusion=True)

# ---- palette (literal) -- a clear luminance ladder so NO two adjacent faces blend ----
# THREE families kept far apart: (a) cool blue-grey dais (darkest stone, the base mass),
# (b) near-white dressed rim/curb (the LIGHT hero ring that pops), (c) warm mid stone for
# the pier bases/curb-banding between them. Water saturated; timber warm; roof near-black brown.
DAIS_L = "#9aa0a7"   # polished-andesite dais top  (cool mid blue-grey)
DAIS_D = "#727880"   # lower dais step / chiseled fill (distinctly DARKER, cool)
TREAD  = "#c2c6cb"   # stone-brick approach treads (LIGHT lip -> steps pop off the dais)
RIM    = "#e6e2d6"   # octagonal pool rim -- pale dressed stone (near-white, reads as the ring)
CURB   = "#cdc7b6"   # raised drinking-curb course (a touch under the rim so the lip reads)
BAND   = "#a89d88"   # pier base + shaft-head banding (warm mid -- dark band under the light caps)
FLOOR  = "#7f7a6d"   # basin floor under the water (dark warm grey -> water sits clearly above it)
WATER  = "#2f74b6"   # real well water (deep saturated blue -- unmistakable)
WATER2 = "#5aa8e2"   # spout / surface highlight water (bright cyan-blue -> the moving water reads)
POST   = "#6f5230"   # stripped-oak timber posts (deep warm brown, strong vs cool stone)
POSTLT = "#9a7647"   # post capital / ring-beam / windlass timber (brighter amber -> reads)
POSTDK = "#523c22"   # darker post foot / brace (frames the timber)
ROOF   = "#2f251c"   # dark-oak hipped roof (near-black brown -- max contrast vs pale stone)
ROOFLT = "#4a3a2c"   # roof eave / alternating course shade (stepped read)
CUPOLA = "#dcd6c8"   # belfry cupola dressed stone (pale, above the dark roof = crown reads)
BUCKET = "#7c5a34"   # oak draw-bucket
BANNER = "#e6e3da"   # light-gray civic banner cloth
CHAIN  = "#8c8c92"   # iron windlass chain / fittings

# grid: square footprint x 0..15, z (depth) 0..15.  core ring centred ~ (7.5, 7.5).
CX, CZ = 7.5, 7.5

# ============================ TWO-STEP CIVIC DAIS (grounded base) ============================
# y=0 lower step 15x15 ; y=1 upper step 11x11 (raised so the avenue clears it -> a monument).
S.box(0,0,0, 15,15,1, DAIS_D)                 # lower dais 15x15
S.box(2,2,1, 11,11,1, DAIS_L)                 # upper dais 11x11 (the ring + posts seat on this)
# approach treads (lighter lip) on the front + two flanks -- the steps you walk up
S.box(2,13,0, 11,1,1, TREAD)                  # front step lip (z=13)
S.box(0,2,0, 2,11,1, TREAD)                   # west step lip
S.box(13,2,0, 2,11,1, TREAD)                  # east step lip

# ============================ OCTAGONAL DRESSED RIM + ONE CLEAN BASIN + WATER ============================
Y0 = 2   # everything civic sits on the upper dais top (y=2)
# the rim is a 9x9 ring of pale dressed stone on x3..12 z3..12, corners CHAMFERED back -> octagon.
# inside it: a recessed 3x3 basin holding real water (one course down so the water stays put).
S.box(3,3,Y0, 9,9,1, RIM)                     # full rim slab (we carve the basin + chamfers out of it)
# chamfer the 4 corners back to the dais tone so the silhouette reads 8-sided (octagon)
for (cxr,czr) in [(3,3),(11,3),(3,11),(11,11)]:
    S.box(cxr,czr,Y0, 1,1,1, DAIS_L)          # corner cut -> octagon
# basin floor + recessed water (3x3 centred on x6..8 z6..8)
S.box(6,6,Y0, 3,3,1, FLOOR)                   # basin floor (under the water)
S.box(6,6,Y0+1, 3,3,1, WATER)                 # the 3x3 water body, one course proud of the floor
# raised drinking-curb you stand at -- ONLY on the back + sides (the FRONT is left open/low so the
# viewer sees straight into the water basin from the avenue side; nothing hides the central water).
S.box(4,4,Y0+1, 7,1,1, CURB)                  # back curb (z=4, far side -- reads behind the basin)
S.box(4,4,Y0+1, 1,6,1, CURB)                  # west curb
S.box(10,4,Y0+1, 1,6,1, CURB)                 # east curb

# ============================ FOUR STOUT POSTS (one per octagon CORNER) -> the legible frame ============================
# locked to the four chamfered corners; each footed on a dressed pier so timber never touches water.
# dressed pier base (warm band) -> tall warm-brown shaft -> light capital band = reads as a column.
POSTS = [(3,3),(11,3),(3,11),(11,11)]
PH = 7   # shaft 7 tall (opens the bay so the well + windlass read clearly under the roof)
for (px,pz) in POSTS:
    S.box(px,pz,Y0+1, 1,1,1, BAND)            # dressed pier base (warm band on the dais)
    S.box(px,pz,Y0+2, 1,1,PH, POST, seam=True)# tall timber shaft (warm brown)
    S.box(px,pz,Y0+2+PH, 1,1,1, POSTLT)       # capital band
# brace rails ONLY on the back + two sides (the FRONT bay is left OPEN so the well + windlass +
# water read clearly through it -- de-cluttered: no rail crossing the front of the central object).
BRY = Y0+2+3
S.box(3,3,BRY, 9,1,1, POSTDK)                                   # back brace (z=3)
S.box(3,3,BRY, 1,9,1, POSTDK); S.box(11,3,BRY, 1,9,1, POSTDK)   # west / east braces
# ring-beam tying all four posts at the top -- the roof sits squarely on THIS
RB = Y0+2+PH
S.box(3,3,RB, 9,1,1, POSTLT); S.box(3,11,RB, 9,1,1, POSTLT)
S.box(3,3,RB, 1,9,1, POSTLT); S.box(11,3,RB, 1,9,1, POSTLT)

# ============================ CENTRAL WELL SHAFT + WINDLASS + BUCKET + CHAIN (the draw read) ============================
# a raised dressed WELLHEAD column rises out of the basin water (so it clears the curb and reads
# in the lit bay under the roof); two stout winder uprights carry a turned windlass BEAM across it;
# an oak BUCKET hangs on an iron chain dangling over the visible water. THIS is the "it's a well" read.
# LEGIBILITY LAYOUT (the key fix): keep the basin water OPEN at the front; foot the two windlass
# uprights on the BACK curb (behind the water, so they never occlude it); reach the turned beam
# FORWARD over the basin; hang the bucket + chain in the CLEAR FRONT water cell where nothing hides
# it. A low pale wellhead collar rings the shaft -- it does NOT rise into a column blocking the view.
WX, WZ = 7, 7   # basin centre (water on x6..8 z6..8)
# low dressed wellhead collar around the shaft mouth (one course proud of the water, reads the rim)
S.box(WX,WZ,Y0+1, 1,1,1, RIM)                 # pale wellhead collar at the back of the basin
# --- windlass A-frame: two uprights on the BACK curb (z=5, behind the water) carrying the beam ---
WUZ = 5                                        # uprights stand on the back curb course
WUH = 4                                        # upright height
S.box(WX-1,WUZ,Y0+2, 1,1,WUH, POSTLT)         # west winder upright (on back curb -> behind the water)
S.box(WX+1,WUZ,Y0+2, 1,1,WUH, POSTLT)         # east winder upright
WBY = Y0+2+WUH-1                               # beam top height
# the turned windlass BARREL-beam, spanning the two uprights and reaching FORWARD one cell over water
S.box(WX-1,WUZ,WBY, 3,2,1, POST)              # the windlass barrel (spans uprights, extends 1 over the basin)
S.box(WX-1,WUZ,WBY, 1,1,1, POSTDK); S.box(WX+1,WUZ,WBY, 1,1,1, POSTDK)  # darker turned-end discs / crank
# the draw-BUCKET hung on a chain over the OPEN basin centre, in full view above the blue water.
# a dark iron hoop band under the oak body so it unmistakably reads as a bucket (not just a cube).
BKY = Y0+3                                      # bucket height -- hung above the water, in full view
S.box(WX,WZ,BKY, 1,1,1, BUCKET)               # the hanging oak draw-bucket (front water, unoccluded)
S.box(WX,WZ,BKY, 1,1,0.3, POSTDK)             # dark iron base-hoop on the bucket (reads as a bucket)
# a single thin SPOUT of visible moving water on the basin surface (the WNL flowing-water signature)
S.box(WX+1,WZ+1,Y0+1, 1,1,1, WATER2)          # water trickle highlight on the front-right water cell

# ============================ SOLID COURSE-BUILT HIPPED ROOF (shrink-rings on the 4-post frame) ============================
# rests directly on the ring-beam; concentric shrink-ring courses climb to a short ridge. SOLID.
RY = RB+1
rings = [  # (x,z,dx,dz) per ascending course -- concentric shrink, eave overhangs the posts
    (2,2,11,11),
    (3,3, 9, 9),
    (4,4, 7, 7),
    (5,5, 5, 5),
    (6,6, 3, 3),
]
for i,(rx,rz,rdx,rdz) in enumerate(rings):
    col = ROOF if i % 2 == 0 else ROOFLT      # alternate course shade = readable steps
    S.box(rx,rz,RY+i, rdx,rdz,1, col)
RIDGE_Y = RY+len(rings)
S.box(7,7,RIDGE_Y, 1,1,1, ROOFLT)             # short ridge cap closing the hip

# ============================ GROUNDED BELFRY-CUPOLA (sits on the ridge, bell + finial) ============================
# small solid-cornered open box capped by a stair-pyramidlet -> grounded crown (not floating).
CUP_Y = RIDGE_Y+1
for (cdx,cdz) in [(0,0),(1,0),(0,1),(1,1)]:
    S.box(6+cdx,6+cdz,CUP_Y, 1,1,2, CUPOLA)   # 4 corner pillars (2 tall, iron-bar open walls)
S.box(6,6,CUP_Y+2, 2,2,1, CUPOLA)             # cupola roof slab (rests on the 4 pillars)
S.box(7,7,CUP_Y+3, 1,1,1, RIM)                # finial block (the end-rod spike rises off it)

# ============================ ACCENTS : lanterns, bell, banners, finial (all grounded reads) ============================
# eave ring of hung lanterns under the roof (one per side, on the ring-beam corners)
for (lx,lz) in [(3,3),(12,3),(3,12),(12,12)]:
    S.accent(lx+0.0, lz+0.0, RY-0.4, "glow", r=2.4)
# the iron CHAIN draping from the windlass barrel (front edge, z=WZ) straight down to the bucket
# in the front water cell -- chain + bucket line up vertically as one obvious draw-rig
for cy in (WBY-0.4, WBY-1.2, WBY-2.0, BKY+0.9):
    S.accent(WX+0.5, WZ+0.5, cy, "dot", CHAIN, r=0.7)           # chain links barrel -> bucket
# windlass crank-handle lantern (grounded on the east upright head, behind the water)
S.accent(WX+1.5, WUZ+0.5, WBY+0.4, "glow", "#ffe6a8", r=1.7)
# belfry bell (brass dot) + lantern cluster (grounded in the cupola box)
S.accent(CX, CZ, CUP_Y+1.0, "glow", "#ffe8b0", r=2.6)            # belfry lantern
S.accent(7.4, 7.4, CUP_Y+1.0, "glow", "#caa24a", r=1.6)         # bell
# water glint on the OPEN basin surface (front-left water cell, not under the wellhead)
S.accent(6.4, 7.6, Y0+2.0, "glow", "#bfe6ff", r=2.0)
# civic banner pair on the two FRONT posts (cloth facing the avenue)
S.accent(3.5,11.0,RB-1.2,"dot", BANNER, r=2.0)
S.accent(11.5,11.0,RB-1.2,"dot", BANNER, r=2.0)
# crowning finial spike (end-rod off the finial block)
S.accent(CX, CZ, CUP_Y+4.0, "finial")

# ============================ CALLOUT LABELS ============================
S.label(WX, WZ, WBY, "windlass + bucket + chain over the well shaft")
S.label(CX, CZ, Y0+2.0, "octagonal dressed rim · clear 3×3 water basin")
S.label(11, 11, RB-1, "four stout posts carry the frame (octagon corners)")
S.label(7.5, 7.0, RIDGE_Y+1, "solid course-built hipped roof + belfry-cupola")
S.label(2, 13, 0, "two-step civic dais (15×15 → 11×11)")

out = S.svg(title="Well R5 — roofed civic draw-well (octagonal rim, central well shaft + windlass, course-built hipped roof + belfry)",
            size_label="15×15 well-house · h~17 (belfry beacon reads at DH range)")
open("detail_svg/well.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/well.svg | bytes", len(out.encode()))
