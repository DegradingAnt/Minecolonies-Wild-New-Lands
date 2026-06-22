"""Banner_stand HIGHWAY -> detail_svg/banner_stand_highway.svg.
Per deco_catalog_v2.json id 'banner_stand' tier Highway (footprint 11x5, height 13): the BIG
non-linear jump below the Great Road top -- TWIN 3x3 dressed PYLON-TOWERS on a CONTINUOUS two-step
plinth that bridges UNDER the ~7-wide road (one monument, not two footings). Each tower flies a
4-block inward white-wall-banner column (8 banners framing the crossing), course-banded with chiseled +
mossy rings and stone_brick_wall corner pilasters. A real timber LINTEL ties tower-to-tower (>=4 clear)
under a dark-oak slab BROW with a chiseled KEYSTONE and a keystone banner facing arrivals. Four flanking
corner lanterns + one lintel lantern = the payoff lights (5). An engineered town threshold read from a
distance, not a marker.

NON-LINEAR ESCALATION over Road: 2-wide piers -> 3x3 masonry TOWERS; modest lintel -> a deep tower-tied
beam with KEYSTONE + brow; height 9->13; banners 6->9 (8 curtain + 1 keystone); lanterns 1->5; a
CONTINUOUS two-step plinth unifies it into ONE monument. The rung directly under the Great Road
four-mass gateway (render_banner_stand.py, h18 / 31 banners / 12 lanterns) -- same identity, one step less grand.

ISO: road-facing detail (recessed banner-curtains, keystone banner, dressed fronts) on the HIGH-z FRONT
+ HIGH-x sides so the viewer reads it. The road crosses the plinth centre, passing under the lintel.

Originality/inspiration (FORM/SCALE/TECHNIQUE only, credited CREDITS.md; no NBT/assets copied): Roman
city-gate twin-tower threshold + stepped plinth + deep architrave; medieval town-gate banner brow;
MineColonies/StyleColonies/Byzantine gatehouse twin-mass massing (height calibrated to live beside their
19x15 gatehouse). Ours diverges: an OPEN skeletal post-and-lintel frame, banner-curtains the hero, no
arch/vault/tunnel/chamber. Same wnl_banner_stand builder as the Great Road top; dye/decay/lantern hashed live."""
from iso_render import Iso

S = Iso(U=14)

# ---- palette (literal) -- WIDE-CONTRAST ladder; each masonry role steps so every surface reads -----
PBASE  = "#858177"   # minecraft:stone_bricks continuous plinth course 1 (cool dressed grey -- the bed)
CRACK  = "#9a8f7e"   # minecraft:cracked_stone_bricks character scatter (~1-in-6, warm worn tell)
MOSS   = "#6f7d56"   # minecraft:mossy_stone_bricks weathering swap (saturated green, distance-lerped)
STAIR  = "#6c685f"   # stone_brick_stairs outward skirt (darkest -> the corbel/step shadow, reads the plinth bevel)
ANDE   = "#9c9a93"   # minecraft:polished_andesite inset step 2 tread (cooler/paler -> the two-step rise reads)
CHIS   = "#c7b487"   # minecraft:chiseled_stone_bricks -- banding rings, corners, keystone (warm sand, hard contrast)
TOWER  = "#8e8a80"   # 3x3 pylon-tower core stone_bricks (dressed body)
PIL    = "#b7b2a6"   # stone_brick_wall pilaster strips up the outward corners (lighter -> vertical relief reads)
CAP    = "#a7a297"   # stone_brick_slab[type=top] tower cap (lighter -> the cap pops)
POST   = "#9a9384"   # stone_brick_wall corner posts carrying the lanterns
TIMBER = "#5a4226"   # dark_oak_log lintel header (warm mid timber, axis=x)
TIMDK  = "#46341e"   # dark_oak_fence drop-bracket + corbel shadow (darker timber -> reads the joint)
BROW   = "#33240f"   # dark_oak_slab brow over the lintel (DARKEST element -> caps the silhouette clean)
NICHE  = "#3c3830"   # darkened recess behind the banner column (reads the cloth hung in a slight recess)
BANNER = "#b14a3f"   # white_wall_banner recolored at placement -- muted heraldic claim red (curtain, inward)
BANEDGE= "#d8d2c4"   # pale banner border/staff edge so each hanging reads as cloth
KEYBAN = "#c4504a"   # keystone banner (a hair brighter -> the highest claim on this tier reads on top)
CHAIN  = "#54504a"   # chain carrying the lintel lantern
LANT   = "#ffd47a"   # lantern glow (4 corner + 1 lintel = the payoff lights)

# geometry: 11 wide (x0..11), 5 deep (z0..5, z0=back/z5=front). Twin 3x3 towers: WEST x0-3, EAST x8-11.
# The ~5-wide road crosses the plinth centre (x3..8) under the lintel. Towers face inward (cloth at high-z front).
WT = 0      # west tower x-origin (3 wide)
ET = 8      # east tower x-origin (3 wide)
ZB = 0      # tower back plane
ZF = 3      # tower front depth (towers are 3 deep z0..3 toward back; cloth hangs proud at the FRONT z3)
ZCLOTH = 3.05  # inward banner-curtains hang JUST proud of the tower front face -> always paint OVER the body

# ============================================================================================
# L0 -- CONTINUOUS 11x5 PLINTH course 1, bridging UNDER the road (ONE monument), stair skirt + corners
# ============================================================================================
S.box(0,0,0, 11,5,1, PBASE, seam=True)              # continuous base bridging shoulder-to-shoulder
# character scatter: a few cracked + mossy cells (mid-tier wear, distance-lerped)
S.box(4,1,0, 1,1,1, CRACK); S.box(7,3,0, 1,1,1, MOSS); S.box(1,4,0, 1,1,1, MOSS)
# outward stair skirt all four edges (stepped dressed plinth) -- abuts + rests against the base
S.box(0,-0.34,0, 11,0.34,0.5, STAIR)                # back skirt
S.box(0,5,0.0, 11,0.34,0.5, STAIR)                  # front skirt (faces viewer)
S.box(-0.34,0,0, 0.34,5,0.5, STAIR)                 # west skirt
S.box(11,0,0, 0.34,5,0.5, STAIR)                    # east skirt
for (cx,cz) in [(0,0),(10,0),(0,4),(10,4)]:         # chiseled corners
    S.box(cx,cz,0, 1,1,1, CHIS)

# ============================================================================================
# L1 -- inset 9x3 PLINTH course 2 (polished_andesite) = the two-step rise; chiseled outward corners.
# The road deck sits on this step's centre strip (x3..8).
# ============================================================================================
S.box(1,1,1, 9,3,1, ANDE, seam=True)                # inset andesite step (paler -> two-step rise reads)
for (cx,cz) in [(1,1),(8,1),(1,3),(8,3)]:
    S.box(cx,cz,1, 1,1,1, CHIS)                      # chiseled step corners
# faint road deck strip crossing the plinth centre (reads the road passing under)
S.box(3,1,2, 5,3,0.15, "#9b8a63")

# ============================================================================================
# L2-L9 -- the two 3x3 PYLON-TOWERS, banded (chiseled ring y4, mossy ring y7), wall pilasters up corners
# Towers sit on the andesite step; their FRONT is z1..3 (high-z) so the inner banner face reads.
# ============================================================================================
def tower(x0, outer_x):
    z0 = 1                                           # tower depth z1..3 (3 deep), front face at z3 (high-z)
    S.box(x0,z0,2, 3,3,2, TOWER, seam=True)          # y2-3 base courses
    S.box(x0,z0,4, 3,3,1, CHIS)                      # y4 chiseled banding ring
    S.box(x0,z0,5, 3,3,2, TOWER, seam=True)          # y5-6
    S.box(x0,z0,7, 3,3,1, MOSS)                      # y7 mossy weathering ring (distance-lerped)
    S.box(x0,z0,8, 3,3,2, TOWER, seam=True)          # y8-9 head courses
    # stone_brick_wall pilaster strips up the TWO OUTWARD corners (front + back) for vertical relief
    S.box(outer_x,z0,2, 0.5,0.5,8, PIL)              # outward FRONT-corner pilaster
    S.box(outer_x,z0+2.5,2, 0.5,0.5,8, PIL)          # outward BACK-corner pilaster
    # L10 cap: 3x3 slab cap, proud
    S.box(x0-0.1,z0-0.1,10, 3.2,3.2,0.45, CAP)       # y10 tower cap (overhangs -> reads a cap)
    # corner posts on the cap carrying the lanterns (the two OUTER corners shown lit)
    S.box(outer_x,z0,10.45, 0.6,0.6,1, POST)         # outward-front corner post
    S.box(outer_x,z0+2.4,10.45, 0.6,0.6,1, POST)     # outward-back corner post

tower(WT, WT)        # west tower: outward corner is its WEST edge (x0)
tower(ET, ET+2.5)    # east tower: outward corner is its EAST edge (x10.5)

# ============================================================================================
# BANNER-CURTAINS -- each tower flies a 4-block white_wall_banner column on its INNER face (y4,5,6,7),
# facing INWARD toward the crossing. 4 per side = 8. Slight recess behind so the cloth reads hung-in.
# Hung proud of the inner face so it always paints OVER the tower body.
# ============================================================================================
def banner_column(inner_cell_x):
    S.box(inner_cell_x+0.05, ZF-0.02, 4, 0.9, 0.28, 4, NICHE)   # darkened recess behind the column
    for y in (4,5,6,7):                              # 4 stacked 1-block wall banners
        S.box(inner_cell_x+0.12, ZCLOTH, y, 0.78, 0.3, 1, BANNER)
    S.box(inner_cell_x+0.06, ZCLOTH+0.02, 4, 0.1, 0.26, 4, BANEDGE)  # pale staff edge

banner_column(WT+2)    # west tower inner face = its east column (x2)
banner_column(ET)      # east tower inner face = its west column (x8)

# ============================================================================================
# THE LINTEL (L10-L11) -- a real spanning beam tower-to-tower at y10, backed by stone_bricks, with
# dark_oak_fence drop-brackets into the towers. Underside >=4 over the road deck. ONE lintel lantern.
# ============================================================================================
S.box(WT+2.7,1.2,10, 0.3,1,1, TIMDK)                 # west drop-bracket into the tower
S.box(ET+0.0,1.2,10, 0.3,1,1, TIMDK)                 # east drop-bracket
S.box(WT+2.5,1.0,11, (ET+0.5)-(WT+2.5), 1.0,1, TIMBER, seam=True)  # dark_oak_log header (backed by brick)
S.box(WT+2.5,1.0,10, (ET+0.5)-(WT+2.5), 1.0,1, TOWER)              # stone_bricks backing course under the log

# ============================================================================================
# THE BROW + KEYSTONE (L12) -- dark_oak_slab brow over the lintel; a chiseled keystone in the beam
# face; ONE keystone banner hanging from the brow front facing arrivals.
# ============================================================================================
CTR = (WT+3 + ET) / 2.0                              # crossing centre x
S.box(WT+2.4,0.9,12, (ET+0.6)-(WT+2.4), 1.2,0.45, BROW)  # dark-oak slab brow (caps the silhouette)
S.box(CTR-0.5,0.95,11, 1,0.3,1, CHIS)                # chiseled keystone set in the beam face (front)
# keystone banner hangs from the brow front, facing arrivals (high-z front)
S.box(CTR-0.6,2.0,9.5, 1.2,0.3,2.4, KEYBAN)          # keystone banner cloth (hung under the brow, proud)
S.box(CTR-0.55,1.95,11.4, 1.1,0.34,0.5, TIMDK)       # valance head-rail fixing it to the brow (no float)

# ============================================================================================
# ACCENTS -- 5 lanterns: 4 tower-corner (outer corners of each tower) + 1 lintel-centre.
# GROUNDED: corner lanterns hang off the posts on the caps; lintel lantern on a chain under the beam.
# ============================================================================================
# four corner lanterns (two per tower, on the outer corner posts)
S.accent(WT+0.3, 1.3, 10.7, "glow", LANT, r=2.1)      # west tower front-outer corner
S.accent(WT+0.3, 3.3, 10.7, "glow", LANT, r=2.1)      # west tower back-outer corner
S.accent(ET+2.8, 1.3, 10.7, "glow", LANT, r=2.1)      # east tower front-outer corner
S.accent(ET+2.8, 3.3, 10.7, "glow", LANT, r=2.1)      # east tower back-outer corner
# lintel-centre lantern on a chain
S.box(CTR-0.05,1.4,10.0, 0.1,0.1,1.0, CHAIN)          # chain under the beam (abuts the lintel)
S.accent(CTR, 1.5, 9.7, "glow", LANT, r=2.5)          # threshold lantern

# ============================================================================================
# CALLOUT LABELS
# ============================================================================================
S.label(CTR, 1.2, 12.4, "dark_oak_log LINTEL + slab brow + chiseled KEYSTONE + keystone banner facing arrivals")
S.label(WT+2.1, ZCLOTH, 6.6, "paired 4-block inward banner-curtains (8 white_wall_banners frame the crossing)")
S.label(ET+2.8, 3.3, 11.0, "four flanking corner lanterns + one lintel lantern = 5 payoff lights")
S.label(ET+1.5, 1, 6.0, "twin 3x3 PYLON-TOWERS: chiseled + mossy banding rings, wall-post pilasters")
S.label(0, 4.5, 1.0, "continuous 11x5 two-step plinth bridges UNDER the road -- ONE monument, not two footings")

out = S.svg(title="Banner_stand R-Highway -- twin 3x3 pylon-tower town threshold: 8 banner-curtains + keystone banner + 5 lanterns on a two-step plinth",
            size_label="11x5 (twin 3x3 towers) * h13 * 5 lanterns (the BIG jump -- an engineered town threshold read from a distance)",
            label_w=362)
open("detail_svg/banner_stand_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/banner_stand_highway.svg | bytes", len(out.encode()))
