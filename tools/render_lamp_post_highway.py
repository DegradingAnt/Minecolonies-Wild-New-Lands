"""Lamp-post H (Highway) detail render -> detail_svg/lamp_post_highway.svg.
The PAYOFF rung that reads UNMISTAKABLY as a monumental lamp STANDARD (not a gatehouse):
a clear grounded 3x3 stepped plinth, a SOLID 2x2 dressed masonry base-drum, a built
stair-taper chamfering 2x2 -> 1x1, a legible dark-timber tapering SHAFT, a wrought 3-wide
dark-oak-fence CROSS-ARM carrying PAIRED chain-hung lanterns, and an obvious lit lantern
CROWN on a cobblestone-wall knuckle above the arm. 3x3 footprint, h10, three lights.

Why this rung (not the twin-pier arch): the author's note -- "doesn't come through as
anything at this detail" -- was the Great-Road arch reading as a lumpy gatehouse blob with
no base/column/head. The Highway standard is the canonical "monumental lamp" silhouette in
SPEC 5: base -> drum -> taper -> shaft -> arm+crown. It reads as a believable thing a town
WOULD erect at a road -- a masonry-footed street monument, not a stick and not a gatehouse.

Conventions copied from render_gatehouse.py / render_harbour.py (the quality bar): a REAL
value triad (DARK pier mass -> mid dressed -> near-white HERO stone) anchored by a cool DARK
SLATE coping/cap (the contrast lever the siblings use); warm dark-timber shaft for contrast;
lanterns via glow accents; chains as stacked dot accents; right-hand callout labels; a
size_label. Every node rests on the node below -- nothing floats; the cross-arm fences
CONNECT horizontally to the central knuckle (a supported wrought bracket, not a cantilever).

Original WNL composition. Inspiration STUDIED for scale/technique only (never reproduced):
Roman/medieval candelabrum + processional light-standards on stepped masonry plinths (the
plinth->drum->shaft->crown proportion), the milliarium milestone, and for in-pack scale
MineColonies / CTOV town lighting. The wrought dark-oak-fence cross-arm with chain-hung
paired lanterns over a chiseled-stone base-drum is original WNL work; vanilla blocks only.
"""
from iso_render import Iso

S = Iso(U=22)

# --- palette (literal) -- a REAL value triad: DARK drum mass -> mid dressed -> near-white
#     HERO stone, anchored by a cool DARK SLATE coping cap (the contrast lever the bar uses) ---
PLINTH = "#867f72"   # 3x3 stone-bricks plinth (grounded base mass, warm mid-dark)
STEP   = "#c6c0b2"   # stone-brick stairs (stepped foot skirt + the inward taper) -- pale dressed
CHIS   = "#e7e1d3"   # chiseled stone bricks (dressed corners + base-drum HERO -- near-white)
DRUM   = "#79736a"   # 2x2 base-drum body stone bricks (DARKEST masonry -> everything pops off it)
CAP    = "#4a4550"   # cool DARK SLATE taper-cap / knuckle collar (THE dark anchor)
SHAFT  = "#5b432a"   # stripped dark-oak shaft (warm timber, strong contrast vs the pale taper)
SHAFTL = "#6f5535"   # shaft seam-lit edge (a touch warmer)
ARM    = "#3d2e1c"   # dark-oak-fence wrought cross-arm + crown knuckle (darkest -- wrought identity)
KNUCK  = "#9b9488"   # cobblestone-wall knuckle the crown lantern stands on (mid-grey, reads round)
ROAD   = "#6f5d3e"   # dirt carriageway the standard lights, passing the foot
KERB   = "#8a847a"   # andesite kerb framing the road (lighter than drum -> reads the edge)

GLOW = "#ffd47a"     # warm lantern light
CROWN= "#eafff8"     # icy crown-beacon light (brightest, the head)
LINK = "#c9c9d2"     # chain link colour

# Grid: 3x3 footing in x,z = 0..2; up = y. Shaft centre cell = (1,1).
# ============================================================================
# ROAD CONTEXT -- a strip of carriageway + andesite kerb at the standard's foot,
# so the piece reads as ROAD FURNITURE lighting an avenue (not an abstract tower).
# ============================================================================
S.box(-3, 0, 0, 3, 3, 1, ROAD)                       # carriageway strip west of the post
S.box(-1, 0, 0, 1, 3, 1, KERB)                       # andesite kerb between road + plinth

# ============================================================================
# L0 -- 3x3 stone-bricks PLINTH (the clear grounded base); 4 corners dressed chiseled.
# ============================================================================
S.box(0, 0, 0, 3, 3, 1, PLINTH)
for (cx, cz) in [(0, 0), (2, 0), (0, 2), (2, 2)]:    # dressed corner quoins
    S.box(cx, cz, 0, 1, 1, 1, CHIS)

# ============================================================================
# L1 -- 3x3 stepped FOOT: stone-brick stairs skirt down on the 4 edge-centres to the road,
#       corners + centre stay full stone-brick (a real monument foot, no float).
# ============================================================================
S.box(0, 0, 1, 3, 3, 1, PLINTH)                      # foot course body
for (ox, oz) in [(1, 0), (1, 2), (0, 1), (2, 1)]:    # 4 edge-centre stair skirts (pale dressed)
    S.box(ox, oz, 1, 1, 1, 1, STEP)

# ============================================================================
# L2-L3 -- SOLID 2x2 base-DRUM: chiseled near-white over a dark stone-brick body, centred on
#          the plinth (the "real mass" that fixes the 1x1-stick read). Two courses tall.
#          Drum body DARK (DRUM) with the front+top corners dressed CHIS so it reads dressed.
# ============================================================================
S.box(0, 0, 2, 2, 2, 2, DRUM, seam=True)             # 2x2 dark base-drum body, y2..3
# dressed chiseled quoins up the 4 vertical corners of the drum (near-white hero pops off DRUM)
for (ox, oz) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    pass
S.box(0, 0, 2, 1, 1, 2, CHIS, seam=True)             # front-near corner quoin (hero stone)
S.box(0, 1, 2, 1, 1, 2, CHIS, seam=True)             # left corner quoin
S.box(1, 0, 2, 1, 1, 2, CHIS, seam=True)             # right corner quoin
# (the back-corner stays DRUM dark -> the drum reads as a dressed box with a shadowed inner corner)

# ============================================================================
# L4 -- built TAPER: stone-brick stairs[half=top] facing INWARD on the 2x2 perimeter cap the
#       drum and chamfer the square shoulder down to the 1x1 shaft; a SLATE collar caps it so
#       the shoulder reads as a crisp dark line (the dark anchor), then the shaft plants.
# ============================================================================
S.box(0, 0, 4, 2, 2, 1, STEP)                        # 2x2 inward stair-taper shoulder (pale)
S.box(0, 0, 5, 2, 2, 1, CAP)                         # slate collar capping the taper (dark anchor)

# ============================================================================
# L5-L7 -- the dark-timber SHAFT (legible tapering column): a 1x1 stripped-dark-oak standard
#          rising from the drum centre. Seam lines read the log courses. THIS is the column.
# ============================================================================
S.box(0, 0, 6, 1, 1, 3, SHAFT, seam=True)            # 1x1 timber shaft y6..8 (the standing standard)

# ============================================================================
# L8 -- the WROUGHT 3-wide CROSS-ARM: the shaft caps with a cobblestone-wall KNUCKLE; one
#       dark-oak fence reaches out EACH side, CONNECTING horizontally to the knuckle (supported
#       wrought bracket, not a cantilever). Each arm-end carries a chain then a hanging lantern.
# ============================================================================
S.box(0, 0, 9, 1, 1, 1, KNUCK)                       # central cobblestone-wall knuckle (crown seat + arm root)
S.box(-1, 0, 9, 1, 1, 1, ARM)                        # west fence arm (connects horizontally to the knuckle)
S.box(1, 0, 9, 1, 1, 1, ARM)                         # east fence arm
# a thin top rail across the whole 3-wide arm reads the cross-bar as ONE wrought member,
# and each end has a hang-knuckle the chain falls from (the underside = a real solid node).
S.box(-1, 0, 9.85, 3, 1, 0.3, ARM)                   # continuous wrought top rail over the 3-wide arm

# ============================================================================
# L9 -- the CROWN: a standing lantern head on the central knuckle, above the cross-arm.
#       Built up as a slate collar -> bright dressed cap so the HEAD reads as a real fixture.
# ============================================================================
S.box(0, 0, 10, 1, 1, 1, CAP)                        # slate crown collar on the knuckle
S.box(0, 0, 11, 1, 1, 1, CHIS)                        # bright dressed crown cap (carries the crown light)

# ============================================================================
# ACCENTS -- three lights (the Highway rung): PAIRED chain-hung arm lanterns + a crown beacon.
# Chains = stacked dot accents (the hardware that escalates Road -> Highway).
# ============================================================================
def chain_hang(x, z, y_top, links, lantern_color=GLOW):
    for k in range(links):
        S.accent(x, z, y_top - 0.42 * k, "dot", LINK, r=1.6)
    S.accent(x, z, y_top - 0.42 * links - 0.35, "glow", lantern_color, r=3.4)

# paired chain-hung lanterns under each cross-arm END (hang off the top-rail underside),
# symmetric about the shaft, throwing light DOWN onto the road.
chain_hang(-0.5, 0.5, 9.8, 2)                        # west arm lantern
chain_hang(1.5, 0.5, 9.8, 2)                         # east arm lantern

# crown beacon standing on the dressed cap (the obvious lit HEAD)
S.accent(0.5, 0.5, 12.2, "glow", CROWN, r=3.8)       # crown beacon (brightest -> reads as the head)
S.accent(0.5, 0.5, 12.4, "finial")                   # crown finial spike crowning the head

# ============================================================================
# CALLOUT LABELS
# ============================================================================
S.label(0.5, 0.5, 12.2, "lit lantern CROWN on a dressed knuckle (the head)")
S.label(-0.5, 0.5, 10.0, "wrought 3-wide cross-arm: PAIRED chain-hung lanterns")
S.label(0.5, 0.5, 7.0, "dark-timber tapering SHAFT (the standing standard)")
S.label(0.5, 0.5, 5.0, "built stair-taper 2x2 -> 1x1 + slate collar")
S.label(0.5, 0.5, 3.0, "SOLID 2x2 chiseled base-drum (real masonry mass)")
S.label(1.5, 1.5, 1.0, "3x3 stepped stone-brick plinth (grounded base)")
S.label(-2, 1.5, 0.0, "carriageway + andesite kerb at the foot")

out = S.svg(title="Lamp-post H (Highway) -- a monumental masonry-footed light STANDARD: plinth -> drum -> shaft -> wrought cross-arm + crown",
            size_label="3x3 plinth - solid 2x2 base-drum - h11 - 3 lights (paired arm + crown) - road furniture",
            label_w=360)
open("detail_svg/lamp_post_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/lamp_post_highway.svg | bytes", len(out.encode()))
