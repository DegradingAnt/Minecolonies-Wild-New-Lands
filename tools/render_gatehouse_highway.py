"""Gatehouse HIGHWAY (R4) -> detail_svg/gatehouse_highway.svg.
Per deco_catalog_v2.json id 'gatehouse' tier Highway (footprint 19x11, opening=max(7,road_width),
height 15): the BIG non-linear leap -- from a one-plane arch (Road) to a genuine fortified
TWIN-TOWER city-gate with an interior, a chamber-over-the-gate, and battlements. Battered chamfered
tower bases, a barrel-vaulted deep carriageway (default W=7 over the 9-wide opening), arrow-slits,
a glass-windowed LIT CHAMBER-OVER-THE-GATE bridging the towers, cantilevered machicolation,
crenellated parapets, a banner + lantern per tower, a finialed chamber cap. The rung directly under
the Great Road monument (render_gatehouse.py, h21/full row of soffit lanterns) -- same wnl_gatehouse
identity, one step less grand (square-ish single-chamfer towers, barrel [not pointed] vault, single
storey, a flat chamber cap [not peaked tower roofs], no plinth/pilasters/flanking lamp-posts).

VAULT closing per build_technique (W=7): y5 springer stair each wall; y6 corbel 2 each side; y7
3-block keystone row at the crown. Symmetric over the 9-wide opening, towers at x0..4 / x14..18.
SOFFIT lanterns >= 1 per 3 blocks of the 11-deep tunnel (4 here) so it never goes dark.
ISO: road-facing FRONT = high-z (south, z=10 face) + high-x (east). Inspiration: Roman/medieval
twin-tower city-gates + machicolation -- form/technique only, credited in CREDITS.md, no NBT copied."""
from iso_render import Iso

S = Iso(U=11)

# ---- palette (literal) -- WIDE-CONTRAST ladder, NO two adjacent faces blend.
#      dark->light: SLATE < WALL < BASE < CHAMF < BAND < TOWER < KEY ; GLASS/GLASSL teal glazing;
#      ARCH band mid; TIMBER/BANNER warm+red accents; LANT warm.
BASE  = "#6b655b"   # battered tower base block (dark warm stone -> the planted heavy foot)
CHAMF = "#b3ac9d"   # stair chamfer capping the stepped base edge (light -> softens the offset)
WALL  = "#736d61"   # carriageway + chamber walls (DARK warm dressed stone -> towers pop off it)
TOWER = "#ddd8cb"   # tower shafts (near-white dressed stone -- the LIGHT hero mass)
BAND  = "#bcae90"   # cracked/mossy_stone_brick mid string-course (warm -> breaks the pale shaft)
ARCH  = "#9c9486"   # carriageway voussoir stones (mid -> the vault ring reads as cut wedges)
ARCHD = "#857e72"   # alternating darker voussoir (course-to-course separate-stone read)
KEY   = "#cfc8b6"   # chiseled keystone row + chamber-cap finial + merlon caps (brightest stone)
GLASS = "#5fa6bd"   # chamber glass-pane window band (deep teal -> glazing, not pale stone)
GLASSL= "#bfe9f2"   # lit glass panes + arrow-slit glow (icy night-glow read)
SLATE = "#3c3744"   # machicolation corbel shadow + tunnel-back + chamber-cap roof (darkest)
PMOULD= "#9a9488"   # machicolation proud slab band + parapet ring (mid stone)
TIMBER= "#7a5c3a"   # banner-post + barrel + hanging sign (warm timber)
BANNER= "#7d8088"   # gray_banner cloth (the Highway banner is muted grey, not the red of the top)
BANNERD="#5e6068"   # banner shadow fold (2-tone drape)
SILL  = "#aaa394"   # chamber floor slab + window sills (mid-light)
NECK  = "#9a9384"   # wall-post lantern necks
LANT  = "#ffd47a"   # lantern glow

# geometry anchors
TL = 0      # left tower x0..4 (5 wide)
TR = 14     # right tower x14..18 (5 wide)

# =====================================================================================
# Course 0 (footing/plinth): one continuous CORE plinth pad 19x11, top flush at y=0 -- the road
# runs across it. (Sunk 0.4 so it reads seated in the ground, rooted, not a raised slab.)
# =====================================================================================
S.box(0, 0, 0, 19, 11, 0.5, WALL)                 # continuous footing pad (road crosses it)

# =====================================================================================
# 1) TWIN GATE-TOWERS (x0..4 and x14..18, depth z0..10 = 11 deep). Battered base: bottom course
#    a solid 5x11 block, stepped IN 1 at y=1 with a stair chamfer capping the exposed edge so the
#    foot reads splayed + planted (heavier than a plain box). Single-chamfer (the top tier doubles).
# =====================================================================================
def tower(tx, east_face=False):
    # battered base: full 5x11 block, then step in 1 with a chamfer cap
    S.box(tx, 0, 0.5, 5, 11, 1, BASE, seam=True)          # base course (full 5x11, planted)
    S.box(tx-0.3, -0.3, 1.4, 5.6, 11.6, 0.4, CHAMF)       # stair chamfer cap (proud lip -> splayed foot)
    # tower shaft (TOWER shell), seam courses for masonry, rises tall y=2..11 (taller than the
    # carriageway so the towers FLANK the chamber-over-the-gate and stay the hero mass).
    S.box(tx, 0, 2, 5, 11, 9, TOWER, seam=True)           # shaft y2..10 (the pale hero mass)
    # mid string-course belt breaks the tall flat face (warm -> reads as a shadow line)
    S.box(tx-0.25, -0.25, 6, 5.5, 11.5, 0.4, BAND)        # proud belt course at y6
    # ARROW-SLIT windows on the OUTWARD face (2 per face, framed) at y=3.5 and y=8 -- towers glow.
    of = tx-0.12 if not east_face else tx+4.92            # left tower=west face (x=tx), right=east face
    for wy in (3.5, 8):
        S.box(of, 4.3, wy, 0.2, 1.2, 1.8, WALL)           # dark slit reveal (recessed read)
        S.box(of+(0.02 if not east_face else 0.0), 4.55, wy+0.25, 0.18, 0.7, 1.2, GLASS)  # glazed slit
    # also slit the NEAR (south, z=10) face so the front of each tower glows (viewer-facing)
    for wx in (tx+1.2, tx+3.0):
        for wy2 in (3.5, 7.5):
            S.box(wx, 9.92, wy2, 0.7, 0.2, 1.8, WALL)          # near-face slit reveal
            S.box(wx+0.05, 9.78, wy2+0.3, 0.6, 0.2, 1.2, GLASS)  # glazed near-face slit
    # cornice oversail before the crown (1 proud all round -> a capping shadow line) at y=11
    S.box(tx-0.3, -0.3, 11, 5.6, 11.6, 0.5, BAND)         # cyma moulding under the cornice
    S.box(tx, 0, 11.5, 5, 11, 0.5, CHAMF)                 # cornice oversail

tower(TL)
tower(TR, east_face=True)

# =====================================================================================
# 2) CARRIAGEWAY WALLS + BARREL VAULT (opening x5..13 = 9 clear; default vault span W=7 over it).
#    Inner side-walls are the DARK wall the towers pop against, full tunnel depth z0..10. The FRONT
#    (z=10) is left OPEN so the viewer reads INTO the dark vaulted mouth; the front rib frames it.
# =====================================================================================
S.box(4, 0, 0.5, 1, 11, 8.5, WALL, seam=True)     # left tunnel wall (carries the vault springer)
S.box(13, 0, 0.5, 1, 11, 8.5, WALL, seam=True)    # right tunnel wall
# dark tunnel interior backing, pulled BACK to z0..8.5 and held BELOW the arch crown so the
# voussoir rib (in front, z9..10) reads as an arched mouth, not a flat-topped hole.
S.box(5, 0, 0.5, 8, 8.5, 7.5, SLATE)              # tunnel interior shadow mass (deep-mouth read)
# DETAIL relief panel midway down each carriageway wall (front-readable, proud of the inner wall)
S.box(4.6, 7.0, 3.5, 0.5, 1.6, 1.8, CHAMF)        # left wall chiseled relief panel (light, proud)
S.box(12.9, 7.0, 3.5, 0.5, 1.6, 1.8, CHAMF)       # right wall relief panel
# FRONT voussoir arch ring over the 9-wide opening, voussoirs alternating ARCH/ARCHD so each wedge
# reads as a separate cut stone. Placed at the FRONT plane (z=9..11) so it is the frontmost
# geometry of the mouth -> a true arched opening. W=7 closing: y6 springer each wall; y7 corbel 2
# each side; y8 3-block keystone row. Each voussoir bears on the one below -> grounded, closes.
S.box(5, 9, 6, 1, 2, 1, ARCH); S.box(13, 9, 6, 1, 2, 1, ARCH)     # springers (off the tunnel walls)
S.box(6, 9, 7, 1, 2, 1, ARCHD); S.box(7, 9, 7, 1, 2, 1, ARCHD)    # left corbel x2
S.box(11, 9, 7, 1, 2, 1, ARCHD); S.box(12, 9, 7, 1, 2, 1, ARCHD)  # right corbel x2
S.box(8, 9, 8, 3, 2, 1, KEY)                      # 3-block chiseled KEYSTONE row at the crown
# arch jambs framing the mouth sides at the front plane (so the opening reads cased, not a gap)
S.box(5, 9, 0.5, 1, 1, 5.5, ARCHD, seam=True)     # left jamb (front face of the left tunnel wall)
S.box(13, 9, 0.5, 1, 1, 5.5, ARCHD, seam=True)    # right jamb
# spandrel fill above the vault back so the chamber floor above has a solid bearing (closes plane)
S.box(5, 0, 8, 9, 2, 1, WALL)

# =====================================================================================
# 3) GLASS-WINDOWED LIT CHAMBER-OVER-THE-GATE (bridges the towers, y9..12 OVER the carriageway,
#    sitting ON the closed vault crown). 9x5 walled chamber set back to z3..8: CORE walls, a glass-
#    pane window band on the ROAD (front, z=8) face, a slab floor, lantern inside. The 'manned'
#    room glowing over the gate -- now ABOVE the vault, FLANKED by the taller towers.
# =====================================================================================
S.box(5, 3, 9, 9, 5, 0.5, SILL)                   # chamber slab floor (spans tower-to-tower, on the vault)
S.box(5, 3, 9.5, 9, 5, 2.5, WALL, seam=True)      # chamber walls y9..11 (the room mass)
# continuous sill + lintel framing the glazed band on the front (road-facing, z=8) face
S.box(5.3, 7.6, 9.6, 8.4, 0.5, 0.4, SILL)         # window sill ledge under the glazing
S.box(5.3, 7.6, 11.5, 8.4, 0.5, 0.4, SILL)        # window lintel over the glazing
# glass-pane window band on the FRONT face (z=8): alternate deep-teal with bright LIT panes.
lit = True
for bx in (5.5, 6.5, 7.9, 8.9, 10.3, 11.3, 12.5):
    S.box(bx, 7.65, 10.0, 0.8, 0.4, 1.5, GLASSL if lit else GLASS)   # glazed bay on the front face
    lit = not lit
# slender stone mullions breaking the glass band (colonnade read, proud of the glass)
for mx in (5.4, 6.4, 7.8, 9.6, 11.0, 12.4, 13.4):
    S.box(mx, 7.55, 9.6, 0.3, 0.45, 2.0, CHAMF)   # mullion pier (light, proud)

# =====================================================================================
# 4) TOWER CROWNS: cantilevered MACHICOLATION ring -> crenellated parapet (single-chamfer, square
#    towers; NO peaked roofs -- that leap is saved for the Great Road top).
# =====================================================================================
def crown(tx):
    # machicolation: a dark corbel shadow course UNDER a proud light slab band -> true cantilever,
    # sitting ON the cornice (y12) so it crowns the tower ABOVE the chamber, not buried in it.
    S.box(tx-0.2, -0.2, 12, 5.4, 11.4, 0.4, SLATE)    # corbel shadow course (dark, recessed)
    S.box(tx-0.5, -0.5, 12.4, 6, 12, 0.6, PMOULD)     # proud machicolation slab band (cantilevered)
    # crenellated parapet: a darker ring + light merlons that pop (1 block / 1 gap rhythm).
    S.box(tx, 0, 13, 5, 11, 0.6, PMOULD)              # parapet base ring (mid -> merlons read against it)
    for mx in range(0, 5, 2):                          # near (z=10) + far (z=0) merlons
        S.box(tx+mx, 10, 13.6, 1, 1, 1, TOWER)        # near (viewer-facing) merlon
        S.box(tx+mx, 0, 13.6, 1, 1, 1, TOWER)         # far merlon
    for mz in (0, 2, 4, 6, 8, 10):                    # side merlons (west + east edges of the tower)
        S.box(tx, mz, 13.6, 1, 1, 1, TOWER)
        S.box(tx+4, mz, 13.6, 1, 1, 1, TOWER)

crown(TL)
crown(TR)

# =====================================================================================
# 5) CHAMBER ROOF: a flat ACCENT-slab roof on the chamber walls (y12) + a low stair-pyramid cap
#    with a centred chiseled finial. Kept BELOW the tower merlons (y13.6+) so the towers stay the
#    hero mass; the PEAKED tower roofs are the Great Road leap, not here.
# =====================================================================================
S.box(4.7, 2.7, 12, 9.6, 5.6, 0.5, SLATE)         # chamber eaves slab (proud overhang -> shadow line)
S.box(6, 4, 12.5, 7, 3, 0.5, PMOULD)              # low pyramid cap course (steps inward)
S.box(8, 5, 13.0, 3, 1, 0.5, KEY)                 # chiseled finial ridge (centred, low -- under the merlons)

# =====================================================================================
# 6) BANNERS: a gray banner on a 2-tall wall-post at each tower's NEAR (viewer-facing, z=10) front
#    merlon, cloth draped toward the avenue (heraldry faces out). Two-tone for a real drape.
#    Grounded: post rises from the near merlon (y14.6), cloth hangs off it.
# =====================================================================================
for tx in (TL, TR):
    S.box(tx+2, 10, 14.6, 0.8, 0.8, 2, TIMBER)        # banner-post on the near merlon (grounded on it)
    S.box(tx+2, 10.7, 15, 0.8, 0.4, 1.8, BANNER)      # banner cloth facing the avenue (near face)
    S.box(tx+2, 11.0, 15, 0.8, 0.2, 1.8, BANNERD)     # shadowed trailing fold (2-tone drape)

# =====================================================================================
# LIGHTING: soffit lanterns >=1 per 3 blocks of the 11-deep tunnel (4 here), chamber glow through
# the glass band, a lantern at each front merlon. Arrow-slit + near-face glows.
# =====================================================================================
for lz in (1.5, 4.5, 7.5, 9.5):
    S.accent(9, lz, 5.2, "glow", LANT, r=1.9)         # soffit lanterns down the carriageway (never dark)
S.accent(9, 7.8, 10.6, "glow", "#eafff8", r=3.2)      # chamber window-band glow (the manned room at night)
# arrow-slit + near-face tower glows (the towers reading lit at night)
for tx in (TL, TR):
    for wx in (tx+1.5, tx+3.3):
        S.accent(wx, 9.9, 4.4, "glow", GLASSL, r=1.2)
        S.accent(wx, 9.9, 8.4, "glow", GLASSL, r=1.2)
# lantern at each front (near, z=10) merlon corner of each tower
S.accent(0.5, 10.0, 14.2, "glow", LANT, r=2.0)
S.accent(4.5, 10.0, 14.2, "glow", LANT, r=2.0)
S.accent(14.5, 10.0, 14.2, "glow", LANT, r=2.0)
S.accent(18.5, 10.0, 14.2, "glow", LANT, r=2.0)
# chamber-cap finial crowned
S.accent(9.5, 5.5, 13.4, "finial")

S.label(2.0, 10.0, 14.6, "twin gate-towers -- battered chamfered base, single-chamfer (top tier doubles)")
S.label(9.0, 9.0, 8.6, "barrel-vaulted carriageway -- 3-block keystone row (W=7 over 9 clear)")
S.label(9.0, 7.6, 11.4, "glass-windowed LIT chamber-over-the-gate (manned room glows)")
S.label(16.0, 10.0, 13.6, "cantilevered machicolation + crenellated parapet + banner")
S.label(9.0, 4.5, 5.2, "soffit lanterns -- >=1 per 3 blocks of the 11-deep tunnel")
S.label(9.5, 5.0, 13.0, "flat chamber cap + low finial (peaked tower roofs saved for Great Road)")
S.label(0.5, 5.0, 8.4, "arrow-slits on outward + near faces -- the towers glow")

out = S.svg(title="Gatehouse R4 (Highway) -- fortified twin-tower gate: barrel-vaulted carriageway, lit chamber-over-the-gate, machicolation",
            size_label="19x11 foot (9 clear) * h15 * ~12 lanterns (the big leap -- a genuine fortified gate, one step under the monument)",
            label_w=420)
open("detail_svg/gatehouse_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/gatehouse_highway.svg | bytes", len(out.encode()))
