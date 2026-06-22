"""Banner_stand R5 (Great Road) detail render -> detail_svg/banner_stand.svg.
A monumental FOUR-mass ceremonial banner GATEWAY: a grand three-step plinth carrying two inner
3x3 banner-towers (each flying TWO 7-block white wall-banner columns split by a wall mullion) that
flank the wide avenue, two outer 2x2 lantern-pylons at the plinth ends, a deep two-course dark-oak
architrave the road passes UNDER, a low buildable PEAKED gable crown (stairs->slab ridge) with a
chiseled keystone + soul-lantern underlight, crown banners + finial lanterns up top, and a keystone
banner facing arrivals -- "you are entering a great place."

Original composition (vanilla blocks only). FORM/SCALE study, never copied (credited in CREDITS.md):
Roman triumphal/city gates (Porta Nigra, Arch of Titus) for the avenue-passes-under threshold +
stepped plinth + deep architrave; medieval town-gate banner thresholds for the pitched timber brow;
MineColonies/StyleColonies/Byzantine gatehouses + structurize wells + CTOV/Towns&Towers town gates
for the flanking-banner gesture and lantern-standard rhythm. Ours diverges HARD: an OPEN skeletal
four-post frame (no arch vault, no tunnel), cloth banner-curtains are the hero -- a banner STAND.

REFINE PASS (adversarial): palette pushed to read every surface distinctly (mullion/frame/finial
posts each get their OWN dressed tone, banner A vs B split widened, gable separated from architrave,
plinth treads/risers/skirt tiered); pylons enriched (base + banded shaft + cornice cap + corner
standards) to match the plaza detail bar; sort fixed by hanging every FRONT cloth element (banner
curtains, crown banners, keystone banner, crown finials) at z>=tower-front so they always paint
OVER the masses instead of sorting behind the architrave/beam."""
from iso_render import Iso

S = Iso(U=11)

# ---- palette (literal) -- DISTINCT tones, high contrast so every element reads --------------
# masonry family: cool greys, stepped light->dark by role so each course separates
SKIRT  = "#6f7378"   # stone-brick stair skirt (DARKEST masonry -> anchors the terrace to ground)
PLINTH = "#8e9196"   # polished-andesite plinth core (cool mid grey)
TREAD  = "#c8c5be"   # polished-andesite tread / walked surface (palest masonry -> the deck pops)
RISER  = "#7c8186"   # stair-skirt riser bevel between treads (reads the STEP, mid-dark)
CHIS   = "#d4bf90"   # chiseled stone bricks -- warm sand band, hard contrast vs cool masonry
TOWER  = "#9a948a"   # inner banner-tower stone bricks (DARK body so pale banners + light pop)
TOWDK  = "#7f7a72"   # inner-tower banded ring shadow course (darker tell, reads tower banding)
PYLON  = "#b1b7bd"   # outer lantern-pylon dressed stone (LIGHTER + cooler than towers -> separates)
PYLDK  = "#969ca2"   # pylon banded mid course (so the pylon isn't a flat stack)
WALL   = "#cfcbc3"   # generic dressed stone-brick-wall line (pilasters)
MULL   = "#e6e1d6"   # banner MULLION + frame (NEAR-WHITE, brightest dressed -> frames the cloth)
FINIAL = "#bdb6a6"   # crown finial posts (warm-grey dressed, distinct from cool pylons/mullion)
POST   = "#a9a294"   # apron / pylon corner standards (warm dressed post -> not the cool pylon body)
MOSS   = "#73855c"   # mossy stone-brick weathering course (saturated green tell, distance-gated)
TIMBER = "#5a4226"   # dark-oak architrave logs / corbels (warm mid timber)
TIMDK  = "#4a3620"   # architrave second course / corbel shadow (reads the two-course depth)
ROOF   = "#33240f"   # dark-oak gable roof (DARKEST element -> the brow caps the silhouette clean)
ROOFRDG= "#2a1d0c"   # gable ridge slab (a hair darker than the slopes -> ridge line reads)
BANNER = "#bf3b34"   # white_wall_banner recolored at placement -- heraldic claim red (column A, brighter)
BANBK  = "#7a241f"   # banner column-B / shaded depth read (MUCH darker -> the two hangings separate)
CROWN  = "#cf463d"   # crown + keystone banners (brightest red -> the highest claim reads on top)
DECK   = "#bda472"   # avenue deck / approach apron (packed warm path, NOT a masonry tone)
DECKDK = "#a68d5e"   # apron threshold edge (darker mat lip -> reads the apron as its own mass)
SOUL   = "#9fe6ff"   # soul-lantern underlight (cool blue tell)

# geometry along x (0..21 wide), depth z (0..7, z=0 back), y up
# pylonW x0-2 | towerW x2-5 | central avenue x5-16 (the grand span) | towerE x16-19 | pylonE x19-21
PYL_W = 0     # outer pylon west x-origin (2 wide)
TOW_W = 2     # inner tower west x-origin (3 wide)
SPAN_X0 = 5   # avenue span start (the grand wide avenue)
SPAN_X1 = 16  # avenue span end (11-wide avenue -> reads as the grand great-road span)
TOW_E = 16    # inner tower east x-origin (3 wide)
PYL_E = 19    # outer pylon east x-origin (2 wide)
WIDTH  = 21   # total plinth width

ZB = 2        # towers/architrave back plane (z2)
ZF = 5        # tower INNER (avenue-facing) front plane (z5) -- cloth hangs here-and-forward
ZCLOTH = 5.55 # banner curtains hang JUST proud of the tower face -> always sort OVER the body

# ============================================================================================
# MASS 0 -- the GRAND PLINTH: three contiguous stepped courses (21x7 -> 19x5 -> 17x5)
# ============================================================================================
S.box(0,0,0, WIDTH,6,1, SKIRT)               # y0 continuous 21x6 terrace (darkest stair-skirt body)
S.box(0,5,0, WIDTH,1,1, SKIRT)               # front skirt course (z5, faces the viewer)
# riser bevel reading the FIRST step-in (a proud dark lip under the y1 tread)
S.box(1,1,1, WIDTH-2,1,1, RISER)             # y1 back riser strip (reads the terrace edge)
S.box(1,4,1, WIDTH-2,1,1, RISER)             # y1 front riser strip
S.box(1,1,1, WIDTH-2,5,1, TREAD)             # y1 inset 19x5 step (pale polished-andesite tread)
S.box(2,1,2, WIDTH-4,5,1, PLINTH)            # y2 inset 17x5 step (core)
# avenue deck: warm path strip down the central span on top of the y2 step
S.box(SPAN_X0,1,3, SPAN_X1-SPAN_X0,5,1, DECK)   # the walked grand avenue (x5-16, z1-6)
# chiseled corner blocks on the top step (warm accents at the four corners)
for (cx,cz) in [(2,1),(WIDTH-3,1),(2,5),(WIDTH-3,5)]:
    S.box(cx,cz,2, 1,1,1, CHIS)

# ============================================================================================
# MASS 1/2/3 -- the FOUR masses: two INNER 3x3 banner-towers + two OUTER 2x2 lantern-pylons
# ============================================================================================
def inner_tower(x0):
    z0 = ZB                                   # towers sit toward the back, z2-5
    # body, courses y3..14 (12 tall) split so we can band rings + a moss course
    S.box(x0,z0,3, 3,3,2, TOWER, seam=True)   # y3-4
    S.box(x0,z0,5, 3,3,1, CHIS)               # y5  chiseled ring
    S.box(x0,z0,6, 3,3,1, TOWER, seam=True)   # y6
    S.box(x0,z0,7, 3,3,1, TOWDK)              # y7  shadow band (reads the banding)
    S.box(x0,z0,8, 3,3,1, MOSS)               # y8  mossy weathering course
    S.box(x0,z0,9, 3,3,1, CHIS)               # y9  chiseled ring
    S.box(x0,z0,10, 3,3,3, TOWER, seam=True)  # y10-12
    S.box(x0,z0,13, 3,3,1, CHIS)              # y13 chiseled ring
    S.box(x0,z0,14, 3,3,1, TOWDK)             # y14 head course (under the architrave, shadowed)
    # stone-brick-wall pilaster strips up the OUTWARD corner (the side away from the span)
    px = x0 if x0 < 8 else x0+2               # west tower -> left corner; east tower -> right corner
    S.box(px,z0,3, 0.55,0.55,11, WALL)        # outward front pilaster
    S.box(px,z0+2.45,3, 0.55,0.55,11, WALL)   # outward back pilaster

inner_tower(TOW_W)
inner_tower(TOW_E)

def outer_pylon(x0):
    z0 = 3                                    # 2x2 pylon, slightly forward of towers
    # a dressed lantern-standard: base course + banded shaft + cornice cap (not a flat stack)
    S.box(x0,z0,3, 2,2,1, PYLON)              # y3 base course
    S.box(x0,z0,4, 2,2,3, PYLON, seam=True)   # y4-6 lower shaft
    S.box(x0,z0,7, 2,2,1, PYLDK)              # y7 banded mid course (shadow tell)
    S.box(x0,z0,8, 2,2,3, PYLON, seam=True)   # y8-10 upper shaft
    S.box(x0-0.15,z0-0.15,11, 2.3,2.3,1, MULL)# y11 proud cornice cap (overhangs -> reads a cap)
    # four warm corner standards carrying ONE hanging lantern each = the standards
    for (dx,dz) in [(0,0),(1.4,0),(0,1.4),(1.4,1.4)]:
        S.box(x0+dx,z0+dz,12, 0.6,0.6,1.6, POST)

outer_pylon(PYL_W)
outer_pylon(PYL_E)

# banner curtains: each inner tower flies TWO 7-block white-wall-banner columns (y5..11) on its
# INWARD face (z5+, facing the viewer/avenue), split by a near-white mullion in the centre cell.
# Hung at ZCLOTH (proud of the tower face) so the cloth always paints OVER the tower body.
def banner_columns(x0):
    # mullion FIRST (slightly back of the cloth) so the bright frame sits behind/between the hangings
    S.box(x0+1.02, ZF+0.15, 5, 0.6,0.45,7, MULL)   # centre wall mullion separating the two columns
    # outer frame pilasters bracketing the curtain pair (brightest dressed line)
    S.box(x0-0.05, ZF+0.1, 5, 0.34,0.4,7, MULL)    # left frame edge
    S.box(x0+2.71, ZF+0.1, 5, 0.34,0.4,7, MULL)    # right frame edge
    # column-A (left cell, brighter red) and column-B (right cell, darker red) -- 7 banners each
    for (col, dx) in [("A", 0.32), ("B", 1.72)]:
        hue = BANNER if col == "A" else BANBK
        for y in range(5, 12):                 # y5..11 inclusive = 7 banners
            S.box(x0+dx, ZCLOTH, y, 0.78, 0.32, 1, hue)

banner_columns(TOW_W)
banner_columns(TOW_E)

# ============================================================================================
# MASS 4 -- the GREAT ARCHITRAVE: deep two-course dark-oak beam spanning the avenue (>=5 clear)
# ============================================================================================
# spans inner-tower to inner-tower across the 9-wide avenue, underside at y13 (>=5 over deck y3..)
S.box(SPAN_X0,ZB,13, SPAN_X1-SPAN_X0,3,1, TIMBER, seam=True)  # y13 architrave (dark_oak_log axis=x backed)
S.box(SPAN_X0,ZB,14, SPAN_X1-SPAN_X0,3,1, TIMDK)             # y14 second architrave course (darker -> two-course depth)
# corbel brackets dropping into the towers at each end (against the full face)
S.box(SPAN_X0-0.45,3,12, 0.55,1,1.5, TIMDK)    # west corbel
S.box(SPAN_X1-0.1,3,12, 0.55,1,1.5, TIMDK)     # east corbel

# ============================================================================================
# MASS 5 -- the PEAKED GABLE CROWN: stairs climbing to a slab ridge + chiseled keystone
# ============================================================================================
# a low buildable peaked gable over the architrave (3 stacked courses stepping to a ridge)
CTR = (SPAN_X0 + SPAN_X1) / 2.0                # avenue centre x
S.box(SPAN_X0,ZB,15, SPAN_X1-SPAN_X0,3,1, ROOF)      # y15 broad eave course (full span, climbing in)
S.box(CTR-2.5,2.4,16, 5,2.2,1, ROOF)                 # y16 second pitch course (inset both eaves)
S.box(CTR-1.5,2.7,17, 3,1.6,1, ROOFRDG)              # y17 dark-oak slab ridge cap (the gable peak)
S.box(CTR-0.5,2.0,15.05, 1,1,1, CHIS)                # chiseled keystone set proud in the gable face (front)

# ============================================================================================
# MASS 6 -- CROWN banners + finials on the two inner towers + keystone banner from the ridge
# GRAVITY: every crown cloth now hangs off a REAL beam directly above it (a banner-arm bracketed
# to the finial post) and is backed by that post -- no cloth floats past the tower head.
# ============================================================================================
# finial posts on each tower head: a tall dressed post standing ON the tower head course (y14),
# rising to carry the finial lantern. Centred over the banner so the banner has a post behind it.
def tower_crown(x0):
    cx = x0 + 1.0                                     # post x-origin (centres the 1.2-wide banner)
    # finial post -- stands on the tower head (y14 -> base at y15), tall enough to carry the lantern
    S.box(cx, ZF+0.1, 15, 0.7,0.55,2.6, FINIAL)       # finial post (rooted on the tower head course)
    # banner-ARM: a timber cross-beam bracketed off the post at the banner top (y17), reaching
    # out OVER + PROUD of the banner (to ZCLOTH) so the cloth visibly hangs FROM a beam, not air.
    S.box(x0+0.35, ZF+0.05, 16.9, 1.4,0.62,0.55, TIMBER)  # banner-arm beam (overhangs the cloth, caps it)
    S.box(cx+0.05, ZF+0.0, 15.4, 0.55,0.5,1.6, TIMDK)     # arm-to-post knee strut down the post (reads the joint)
    # crown banner -- hangs DOWN from the banner-arm (top y17 under the beam, drops to y15), post behind.
    S.box(x0+0.45, ZCLOTH+0.05, 15, 1.1,0.28,2, CROWN)    # crown banner (hung under its own arm)

tower_crown(TOW_W)
tower_crown(TOW_E)

# ONE large keystone banner hangs from the GREAT ARCHITRAVE, facing arrivals down the avenue.
# GRAVITY: a banner needs a beam over it + a wall behind it. We fix a timber PENDANT VALANCE board
# to the architrave front face (z5) as that backing, then drape the cloth against it -- so the
# banner is a true wall-banner on a real board, not a curtain floating in mid-avenue.
KB_X = CTR - 0.6                                       # keystone-banner x-origin (avenue centre)
# pendant valance: a dark-oak board hung on the architrave front face, top flush with the
# architrave underside (y13) and dropping to y11 -- this is the WALL the cloth hangs against.
S.box(KB_X-0.2, ZF-0.02, 11, 1.6,0.34,3, TIMBER)      # valance board (backs the banner, fixed to the beam)
S.box(KB_X-0.2, ZF-0.02, 13, 1.6,0.34,0.5, TIMDK)     # valance head rail against the architrave (the fixing)
# the cloth itself -- drops y11..14 PROUD of the valance board (paints over it), top tucked under
# the architrave so it reads HUNG FROM the beam, bottom hemmed at y11 (does not dangle past its board).
S.box(KB_X, ZF+0.18, 11.05, 1.2,0.3,3, CROWN)         # keystone banner cloth (on its valance board)

# ============================================================================================
# MASS 7 -- approach APRON: warm threshold mat blending the gate into the avenue (front, z6+)
# ============================================================================================
S.box(SPAN_X0,7,0, SPAN_X1-SPAN_X0,3,1, DECK)  # 9-wide apron, 3 deep out the front
S.box(SPAN_X0,9.5,0, SPAN_X1-SPAN_X0,0.5,1, DECKDK)  # apron mouth lip (darker -> reads the mat edge)
S.box(SPAN_X0+0.1,7,1, 0.6,0.6,1.6, POST)      # west apron post (carries a lantern)
S.box(SPAN_X1-0.7,7,1, 0.6,0.6,1.6, POST)      # east apron post

# ============================================================================================
# ACCENTS -- 12 lanterns (8 pylon corners + 2 finial + 2 apron) + soul-lantern gable underlight
# ============================================================================================
# eight flanking pylon-corner lanterns
for x0 in (PYL_W, PYL_E):
    for (dx,dz) in [(0.3,0.3),(1.7,0.3),(0.3,1.7),(1.7,1.7)]:
        S.accent(x0+dx, 3+dz, 13.6, "glow", r=2.2)
# two finial lanterns on the inner-tower crowns
S.accent(TOW_W+1.4, ZF+0.4, 17.4, "glow", r=2.4)
S.accent(TOW_E+1.4, ZF+0.4, 17.4, "glow", r=2.4)
# two apron-mouth lanterns
S.accent(SPAN_X0+0.4, 7.3, 2.8, "glow", r=2.2)
S.accent(SPAN_X1-0.4, 7.3, 2.8, "glow", r=2.2)
# soul-lantern underlight tucked under the gable eaves (cool blue tell)
S.accent(CTR, ZF+0.1, 14.7, "glow", SOUL, r=2.6)
# crowning finials atop the two towers
S.accent(TOW_W+1.4, ZF+0.4, 17.6, "finial")
S.accent(TOW_E+1.4, ZF+0.4, 17.6, "finial")

# ============================================================================================
# CALLOUT LABELS
# ============================================================================================
S.label(TOW_W+1.5, ZCLOTH, 8, "twin 3×3 banner-towers — 28 framing wall-banners (A/B split by a white mullion)")
S.label(PYL_E+1, 4, 7, "outer 2×2 lantern-pylons — banded shaft + cornice cap (8 flanking lights)")
S.label(CTR, ZB, 14, "deep two-course dark-oak architrave — avenue passes under (≥5 clear)")
S.label(CTR, ZB, 17, "peaked 3-course gable crown + chiseled keystone + crown banners")
S.label(2, 5, 1, "grand three-step plinth (21→19→17, tread/riser/skirt) + approach apron")

out = S.svg(title="Banner_stand R5 — monumental four-mass ceremonial banner gateway (you are entering a great place)",
            size_label="21×7 gateway precinct · h18 · 4 masses · 31 banners · 12 lanterns + soul-lantern")
open("detail_svg/banner_stand.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/banner_stand.svg | bytes", len(out.encode()))
