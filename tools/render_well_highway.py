"""Well HIGHWAY (R4) -> detail_svg/well_highway.svg.
Per deco_catalog_v2.json id 'well' tier Highway (footprint 13x13, height 14): the genuinely GRAND
leap below the Great Road top -- a MONUMENT, not a fixture. A stepped stone DAIS lifts the whole
fountain-house one course above the road; on it an OCTAGONAL dressed stone-brick rim encloses a 5x5
water pool; EIGHT stripped-oak posts (locked to the 8 octagon faces, each on a chiseled pier) carry
a course-built HIPPED dark-oak roof crowned by a lantern-CUPOLA beacon + an end-rod FINIAL. The draw
element peaks below the top: a central CHISELED AQUEDUCT-HEAD pier throws FOUR visible water streams
out across the pool (a true multi-spout standing fountain, not a bucket). Twin flanking TROUGHS
(water channels with end-lanterns) run the two side flanks; civic banners + a bell on the front posts.
13x13x14 deliberately EXCEEDS the structurize big-well (9x9x13) -- it's a landmark.

Massing (per catalog, summarised; graph-paper rim is explicit below):
 * y-1 dais: 13x13 stepped plinth, stone_brick_stairs tread skirt, polished_andesite + stone_brick fill.
 * y0: 5x5 water pool over stone_bricks; OCTAGONAL rim (stone_bricks/chiseled faces/mossy weather) +
   stone_brick_slab drinking lip; twin 7-long flank TROUGHS outboard.
 * y1: stone_brick_wall parapet + chiseled PIER blocks at the 8 faces (carry posts).
 * y2..6: EIGHT stripped_oak_log posts (5 tall) on the piers; oak_fence + trapdoor knee-braces; oak-plank ring-beam.
 * y3..5: the CENTRE -- a chiseled aqueduct PIER to y5 with a 4-way stair spout-head ring throwing 4 streams.
 * y7..10: course-built hipped DARK-OAK roof (13->9->5->ridge shrink-rings) + slab eave trim.
 * y11..12: a chiseled lantern-CUPOLA (iron-bars walls + lantern) capped by a stair pyramidlet.
 * y13: an end_rod FINIAL spike (a DH-visible civic beacon).

Same wnl_well builder as render_well.py (the Great Road top -- which ADDS a flanking colonnade, a
two-step dais, an open belfry-cupola + a continuous Roman cascade: this Highway is one clear step
humbler). Inspiration (form/technique ONLY, credited CREDITS.md; NO assets/NBT copied): Roman
castellum-aquae multi-spout street fountains + medieval town well-houses; course-built rustic hip
roofing from CTOV / Dungeons & Taverns. The multi-stream aqueduct-head WATER ARCHITECTURE is
deliberately NOT a chain-and-bucket. Entirely original WNL vanilla-block build.
ISO: road-facing FRONT = high-z (south) + high-x (east); apron steps, front piers, banners + bell
on the front; the cupola-beacon crowns the centre."""
from iso_render import Iso

S = Iso(U=12)

# ---- palette (literal) -- a wide-contrast ladder across FOUR families kept far apart:
#   cool stone-brick mass / pale dressed chiseled accents / warm stripped-oak frame /
#   near-black dark-oak roof / saturated water; pale cupola crown above the dark roof ----
DAIS_L = "#9aa0a7"   # minecraft:polished_andesite dais top (cool mid blue-grey, the base mass)
DAIS_D = "#727880"   # lower dais step / chiseled fill (distinctly DARKER cool grey)
TREAD  = "#c2c6cb"   # stone_brick_stairs dais tread skirt (LIGHT lip -> the walk-up steps pop)
BRICK  = "#9a958a"   # minecraft:stone_bricks rim + pool floor (warm-neutral grey masonry)
MOSSB  = "#74815a"   # minecraft:mossy_stone_bricks weathering (green-grey, controlled)
CHIS   = "#cdc7b6"   # minecraft:chiseled_stone_bricks faces/piers/aqueduct (pale dressed hero stone)
SLAB   = "#b3ada0"   # minecraft:stone_brick_slab drinking lip + trough surround (light step lip)
WALL   = "#a39b8c"   # minecraft:stone_brick_wall parapet (dressed nub between brick + chiseled)
FLOOR  = "#5d5a50"   # pool/trough floor under the water (dark warm grey -> water sits clearly above)
WATER  = "#2f74b6"   # minecraft:water 5x5 pool + troughs (deep saturated blue -- unmistakable)
WATER2 = "#5aa8e2"   # flowing aqueduct streams / surface highlight (bright cyan-blue -> moving water)
PIER   = "#a89d88"   # chiseled pier post-footing band (warm -> timber never touches stone bare)
POST   = "#7a5c36"   # minecraft:stripped_oak_log posts (warm tan-brown, strong vs cool stone)
POSTLT = "#9a7647"   # post capital / oak-plank ring-beam (brighter amber -> the tied frame reads)
BRACE  = "#5c4326"   # minecraft:oak_fence + trapdoor knee-braces (darker oak)
ROOF   = "#2f251c"   # minecraft:dark_oak_stairs hipped roof (near-black brown -- max contrast)
ROOFLT = "#4a3a2c"   # dark_oak alternating-course / eave-trim shade (stepped read)
RIDGE  = "#5a4632"   # dark_oak_planks ridge cap (warmer crown of the hip)
CUPOLA = "#dcd6c8"   # chiseled_stone_bricks lantern-cupola (pale -> the crown reads above the dark roof)
IRON   = "#6f7178"   # minecraft:iron_bars cupola walls (cool grey, open beacon-house)
BANNER = "#e6e3da"   # minecraft:white_banner civic cloth on the front posts
BELL   = "#caa24a"   # minecraft:bell brass (civic call)
LANT   = "#ffd47a"   # lantern glow
CHAIN  = "#8c8c92"   # minecraft:chain (hung-lantern chains)

# grid: 13x13 footprint x 0..13, z (depth) 0..13. centre 5x5 pool = x4..9 z4..9. centre pier = (6,6).
CX, CZ = 6.5, 6.5

# ============================ COURSE -1 (y=-1): STEPPED 13x13 CIVIC DAIS (the monument lift) ============================
# a solid plinth one course tall; an outward stone_brick_stairs tread skirt = the step you walk up.
S.box(0, 0, -1, 13, 13, 1, DAIS_D)                 # full 13x13 dais body (the base mass)
S.box(1, 1, -1, 11, 11, 1, DAIS_L)                 # inset polished-andesite dais top (lighter, the deck)
# tread skirt (light) on all four approaches -- the walk-up step (front + east read strongest)
S.box(0, 12, -1, 13, 1, 1, TREAD)                  # FRONT tread (z=12, road side)
S.box(12, 0, -1, 1, 13, 1, TREAD)                  # east tread
S.box(0, 0, -1, 1, 13, 1, TREAD)                   # west tread
S.box(0, 0, -1, 13, 1, 1, TREAD)                   # back tread

# ============================ COURSE 0 (y=0): octagonal rim + 5x5 water pool + twin flank troughs ============================
# the 11x11 inner deck holds the rim. rim perimeter = ring x2..10 z2..10; corners chamfered = octagon.
# face cells (the 8 octagon faces -> the 8 posts) get chiseled_stone_bricks; mossy a few; brick rest.
RIMX0, RIMZ0, RIMX1, RIMZ1 = 2, 2, 10, 10          # rim ring bounds (9x9 ring on the deck)
def rim_perimeter():
    cells=[]
    for x in range(RIMX0, RIMX1+1):
        cells.append((x,RIMZ0)); cells.append((x,RIMZ1))
    for z in range(RIMZ0+1, RIMZ1):
        cells.append((RIMX0,z)); cells.append((RIMX1,z))
    return sorted(set(cells))
FACE_CELLS = [(6,2),(6,10),(2,6),(10,6),(3,3),(9,3),(3,9),(9,9)]   # 8 octagon faces (edge mids + chamfer corners)
TRUE_CORNERS = [(2,2),(10,2),(2,10),(10,10)]
for (cx,cz) in rim_perimeter():
    if (cx,cz) in TRUE_CORNERS:
        S.box(cx, cz, 0, 1, 1, 0.5, BRICK)          # chamfer the square corners DOWN -> octagon read
    elif (cx,cz) in FACE_CELLS:
        S.box(cx, cz, 0, 1, 1, 1, CHIS, seam=True)  # chiseled face cell (carries a post)
    else:
        col = MOSSB if (cx+cz) % 5 == 0 else BRICK  # a little controlled moss in the ring
        S.box(cx, cz, 0, 1, 1, 1, col, seam=True)
# the 5x5 pool: stone_bricks floor under a recessed water body (one course down inside the rim)
S.box(4, 4, 0, 5, 5, 0.55, FLOOR)                  # pool floor tray
S.box(4, 4, 0.55, 5, 5, 0.4, WATER)                # the 5x5 WATER pool (recessed)
S.box(4.5,4.5,0.93, 4,4, 0.06, WATER2)             # pool surface sheen
# inner stone_brick_slab drinking lip on the 16 cells bordering the pool (resolves the annulus)
for x in range(3,10):
    for z in range(3,10):
        if (x in (3,9) or z in (3,9)) and not (4<=x<=8 and 4<=z<=8):
            S.box(x, z, 0.95, 1, 1, 0.2, SLAB)      # clean slab drinking ledge ring
# twin flanking TROUGHS on the two side flanks (outboard of the rim, on the deck): 5-long water channels
for tx in (0, 11):                                  # west flank (x0..1) + east flank (x11..12)
    S.box(tx, 4, 0, 2, 5, 0.5, SLAB)               # trough surround tray (stone_brick_slab read)
    S.box(tx+0.3, 4.3, 0.3, 1.4, 4.4, 0.25, WATER) # the trough water channel (recessed, real water)

# ============================ COURSE 1 (y=1): parapet rim wall + 8 chiseled PIERS (carry the posts) ============================
PIERS = FACE_CELLS                                 # 8 piers locked to the 8 octagon faces
for (cx,cz) in rim_perimeter():
    if (cx,cz) in PIERS:
        S.box(cx, cz, 1, 1, 1, 1, CHIS, seam=True) # chiseled pier block (full -> carries the post)
    elif (cx,cz) in TRUE_CORNERS:
        continue                                    # chamfered corners stay low (octagon read)
    else:
        S.box(cx, cz, 1, 1, 1, 0.7, WALL, seam=True)# stone_brick_wall parapet nub (the drinking rim)

# ============================ COURSE 2..6 (y=2..6): EIGHT stripped-oak POSTS + braces + ring-beam ============================
PH = 5                                              # posts 5 tall (y=2..6)
for (px,pz) in PIERS:
    S.box(px, pz, 2, 1, 1, 0.5, PIER)              # pier capital footing (timber off bare stone)
    S.box(px, pz, 2.5, 1, 1, PH, POST, seam=True)  # the stripped_oak_log post (5 tall)
    S.box(px, pz, 2.5+PH, 1, 1, 0.4, POSTLT)       # post capital band
# oak_fence + trapdoor knee-braces between adjacent posts at mid-height (back + flanks; front bay open)
KB = 3
S.box(2, 6, KB, 1, 0.3, 1, BRACE); S.box(10, 6, KB, 1, 0.3, 1, BRACE)   # west / east knee-braces
S.box(3, 2, KB, 0.3, 1, 1, BRACE); S.box(9, 2, KB, 0.3, 1, 1, BRACE)    # back knee-braces
# oak-plank RING-BEAM tying all 8 posts at the top (the roof sits squarely on this)
RB = 2 + PH                                         # ring-beam height (y=7)
S.box(2, 2, RB, 9, 0.6, 0.5, POSTLT); S.box(2, 9.4, RB, 9, 0.6, 0.5, POSTLT)  # back + front beams
S.box(2, 2, RB, 0.6, 9, 0.5, POSTLT); S.box(9.4, 2, RB, 0.6, 9, 0.5, POSTLT)  # west + east beams

# ============================ COURSE 3..5 (y=3..5): CENTRE AQUEDUCT-HEAD PIER -> FOUR water streams ============================
# a chiseled pier rises from the pool floor to y=5; at the top a 4-way stair spout-head ring throws
# four streams that visibly cascade down the pier + out across the 5x5 pool. The standing fountain.
S.box(6, 6, 0.55, 1, 1, 4.4, CHIS, seam=True)      # the central aqueduct PIER (from the pool, to y=5)
S.box(5.7, 5.7, 4.9, 1.6, 1.6, 0.6, CHIS)          # the 4-way spout-head ring (the carved head)
# four visible streams falling off the 4 spout faces down into the pool (grounded in the water)
S.box(6.35, 5.55, 1.0, 0.3, 0.3, 4.0, WATER2)      # north stream
S.box(6.35, 6.85, 1.0, 0.3, 0.3, 4.0, WATER2)      # south stream (front-facing)
S.box(5.55, 6.35, 1.0, 0.3, 0.3, 4.0, WATER2)      # west stream
S.box(6.85, 6.35, 1.0, 0.3, 0.3, 4.0, WATER2)      # east stream

# ============================ COURSE 7..10 (y=7..10): COURSE-BUILT HIPPED DARK-OAK ROOF (shrink-rings) ============================
RY = RB + 0.5
S.box(1, 1, RY-0.2, 11, 11, 0.2, ROOFLT)           # eave trim slab (the overhang under-course)
rings = [  # concentric shrink-rings 11->9->7->5->3 climbing to the ridge (clean tall hip)
    (1,1,11,11),
    (2,2, 9, 9),
    (3,3, 7, 7),
    (4,4, 5, 5),
    (5,5, 3, 3),
]
for i,(rx,rz,rdx,rdz) in enumerate(rings):
    col = ROOF if i % 2 == 0 else ROOFLT           # alternate shade -> readable hip steps
    S.box(rx, rz, RY+i, rdx, rdz, 1, col)
RIDGE_Y = RY + len(rings)
S.box(6, 5, RIDGE_Y, 1, 3, 0.5, RIDGE)             # short ridge cap closing the hip

# ============================ COURSE 11..12 (y=11..12): LANTERN-CUPOLA BEACON (iron-bars + lantern + pyramidlet) ============================
CUP_Y = RIDGE_Y + 0.5
for (dx,dz) in [(0,0),(1,0),(0,1),(1,1)]:
    S.box(6+dx, 6+dz, CUP_Y, 1, 1, 1.6, CUPOLA)    # 4 corner pillars (iron-bars open walls between)
S.box(6, 6, CUP_Y+1.6, 2, 2, 0.5, CUPOLA)          # cupola roof slab (rests on the 4 pillars)
# stair pyramidlet cap (a small 4-way pyramid closing the cupola)
S.box(6.4, 6.4, CUP_Y+2.1, 1.2, 1.2, 0.6, CUPOLA)  # pyramidlet cap

# ============================ COURSE 13 (y=13): END-ROD FINIAL (DH-visible civic beacon) ============================
S.box(6.85, 6.85, CUP_Y+2.7, 0.3, 0.3, 0.5, CHIS)  # finial base block (the end_rod sits on it)

# ============================ DETAIL: barrels + composters at the dais steps ============================
S.box(11.0, 10.0, -1, 0.85, 0.85, 1.1, POST)       # barrel by the SE dais step (warm, grounded)
S.box(11.0, 10.0, 0.1, 0.85, 0.85, 0.12, POSTLT)   # barrel lid band
S.box(11.0, 11.0, -1, 0.85, 0.85, 0.9, MOSSB)      # composter beside it (chained, grounded)

# ============================ ACCENTS: 4 hung eave lanterns + cupola beacon + trough end-lanterns + banners + bell + finial ============================
# 4 hung lanterns on chain under the eaves (one toward each visible corner of the roof)
for (lx,lz) in [(2.5,2.5),(9.5,2.5),(2.5,9.5),(9.5,9.5)]:
    for cy in (RY-0.3, RY-0.9):
        S.accent(lx, lz, cy, "dot", CHAIN, r=0.5)  # chain link
    S.accent(lx, lz, RY-1.3, "glow", LANT, r=1.9)  # hung eave lantern
# cupola BEACON lantern (the big crown light) + the finial spike
S.accent(CX, CZ, CUP_Y+0.9, "glow", "#ffe8b0", r=2.8)  # cupola beacon lantern (DH-visible)
S.accent(CX, CZ, CUP_Y+3.2, "finial")                  # end_rod finial spike
# trough END-lanterns (grounded on the trough surrounds, one per visible flank end)
S.accent(0.9, 8.6, 0.7, "glow", LANT, r=1.7)       # west trough end-lantern (front end)
S.accent(12.1, 8.6, 0.7, "glow", LANT, r=1.7)      # east trough end-lantern (front end)
# civic banners on the two FRONT posts (cloth facing the avenue) + a bell on the front-east post
S.accent(3.4, 9.0, RB-1.4, "dot", BANNER, r=2.0)   # front-west banner
S.accent(9.6, 9.0, RB-1.4, "dot", BANNER, r=2.0)   # front-east banner
S.accent(9.5, 9.5, RB-0.3, "glow", BELL, r=1.6)    # civic bell on the front-east post
# four-stream fountain glints on the pool surface
S.accent(5.5, 7.5, 1.0, "glow", "#bfe6ff", r=1.8)  # pool glint front-left
S.accent(7.5, 6.5, 1.0, "glow", "#cfe6ff", r=1.6)  # pool glint front-right

S.label(CX, CZ, CUP_Y+3.4, "lantern-CUPOLA beacon + end-rod finial (DH-visible)")
S.label(5, 5, RIDGE_Y+0.5, "course-built hipped DARK-OAK roof (13->9->5 shrink-rings)")
S.label(6, 6, 5.4, "central AQUEDUCT-HEAD pier -> FOUR visible water streams")
S.label(10, 6, 4.0, "EIGHT stripped-oak posts on the octagon faces (ring-beam tied)")
S.label(9.5, 9.5, RB-0.2, "civic banners + a bell on the front posts")
S.label(12, 6, 0.5, "twin flank TROUGHS (water channels + end-lanterns)")
S.label(6.5, 6.5, 1.0, "5x5 pool inside an OCTAGONAL dressed rim")
S.label(0, 12, -0.5, "stepped 13x13 civic DAIS (lifts it above the road)")

out = S.svg(title="Well R4 (Highway) -- monumental fountain-house: stepped dais, octagonal rim, 5x5 pool, EIGHT posts, four-stream aqueduct-head, hipped dark-oak roof + lantern-cupola beacon",
            size_label="13x13 foot * h14 * ~9 lanterns + bell (a landmark -- exceeds the 9x9x13 big-well; one step under the Great Road)",
            label_w=392)
open("detail_svg/well_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/well_highway.svg | bytes", len(out.encode()))
