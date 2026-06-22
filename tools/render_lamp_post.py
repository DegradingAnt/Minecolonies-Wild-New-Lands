"""Lamp-post GREAT ROAD (R5, the grandest tier) -> detail_svg/lamp_post.svg.
Per deco_catalog_v2.json id 'lamp_post' tier Great Road (footprint 7x5 plinth, twin 3x3 piers
flanking the carriageway, an overhead lintel-arch the road passes UNDER, height 14): the biggest
non-linear leap and the answer to "monumental" -- NOT a wider doormat but a GATEWAY. Two SOLID 3x3
chiseled-stone PIERS with corner pilasters and built stair-tapers flank the road; a corbelled flat
STAIR-ARCH steps up+in from each pier to a centre chiseled KEYSTONE over the carriageway, carrying
CHAIN-hung lanterns that light the road FROM ABOVE as you pass beneath; the arch is decked with a
stone-brick-slab parapet carrying a central beacon; each pier is crowned by a lantern on a
cobblestone-wall finial AND a flat biome-tinted civic BANNER mounted FLAT on the outer pier face.
Six-to-eight lights. 14 tall, 7 wide -- a landmark you read from a distance.

NOTE: this is the catalog's LAST tier. render_lamp_post.py renders the HIGHWAY rung (h10, 3x3 single
base-drum + wrought cross-arm). This Great-Road rung is the rung ABOVE that -- the twin-pier gateway.

Escalation over Highway: 3x3 SINGLE base -> TWIN 3x3 SOLID piers + an overhead lintel-arch over the
carriageway; height 10 -> 14; 3 lights -> 6-8 (now lighting the road FROM ABOVE); a wholly new
arch-and-keystone form; flat pier-mounted civic banners. A gateway, not a marker.

ISO STRATEGY (learned from the sibling render_gatehouse.py, the gateway gold standard): the
carriageway runs in the DEPTH (z) direction so the mouth OPENS toward the viewer (high-z front);
the two 3x3 piers flank along X with a GENUINELY EMPTY gap between them (the road); the corbelled
arch is rendered as a FRONT RIB (at the front z-band) springing from each pier to a centre keystone;
a DARK recess mass closes the tunnel back so the mouth reads as a shadowed opening. Road-facing
detail (banners, keystone, under-arch lanterns) reads on the HIGH-z front.

Build technique (catalog C/D/E): (C) corbelled flat arch -- from each pier inner top edge, stairs
step one block IN and one UP toward centre, each resting on the one below (cantilever within 1 block
= always supported), meeting at a single chiseled KEYSTONE; clearance under the keystone >=3 tall so
the road truly passes beneath; the arch top is decked with slab so it reads as a walkable lintel.
(D) corner pilasters = stone_brick_wall on pier corners, grounded on the drum, purely vertical.
(E) chain hangs off the arch underside, lantern off the chain; banners are wall_banner mounted FLAT
on a solid pier face (no free-standing flagpole).

Originality/inspiration: Roman monumental roadside ARCH/janus the road physically passed beneath +
the stepped jack flat-arch corbel technique + medieval market-cross civic banners -- studied for
form/scale/technique ONLY, never reproduced; credited in CREDITS.md, vanilla blocks only. The
corbelled keystone arch carrying CHAIN-hung UNDER-arch road lighting + flat pier-mounted banners is
an arrangement none of those sources use -- original WNL geometry. Same wnl_lamp_post identity; the
top two rungs ship as one NBT template per tier, palette-swapped per biome (silhouette constant)."""
from iso_render import Iso

S = Iso(U=15, occlusion=True)

# --- palette (literal) -- a REAL value triad anchored by a cool DARK SLATE: DARK pier drum mass
#     -> mid dressed stone -> near-white HERO chiseled stone (keystone/quoins), warm dark-timber
#     finial shafts, a slate coping as the contrast lever. Each material reads as itself. ---
PLINTH = "#867f72"   # 7x5 stone_bricks plinth spanning both sides (warm mid-dark base mass)
STEP   = "#c6c0b2"   # stone_brick_stairs stepped foot skirt (pale dressed -> reads the step down)
DRUM   = "#79736a"   # SOLID 3x3 pier drum body, stone_bricks (DARKEST masonry -> everything pops off it)
CHIS   = "#e7e1d3"   # chiseled_stone_bricks (HERO near-white: pier drum front face, quoins)
BAND   = "#9b9488"   # mossy/dressed mid band breaking the pale pier mass (mid-grey)
PILA   = "#b0a99b"   # stone_brick_wall corner pilasters (paler dressed -> the vertical reads)
TAPER  = "#c6c0b2"   # inward stair-taper shoulder capping each drum (pale dressed)
CAP    = "#4a4550"   # cool DARK SLATE coping / taper collar (THE dark anchor / contrast lever)
SHAFT  = "#5b432a"   # stripped_dark_oak_log pier finial shaft (warm timber vs the pale stone)
SHAFTL = "#6f5535"   # finial-shaft seam-lit edge (a touch warmer)
ARCH   = "#cfc9bb"   # stone_brick_stairs corbelled arch courses (dressed -> reads the jack arch)
ARCHD  = "#b6b0a2"   # alt corbel course (a touch darker -> each stepped voussoir reads distinct)
KEY    = "#efe9da"   # chiseled_stone_bricks KEYSTONE (brightest hero -> the arch centre reads)
DECK   = "#b3ada0"   # stone_brick_slab arch-deck parapet course (the walkable lintel top)
RECESS = "#33303a"   # DARK tunnel-back mass closing the mouth (deep shadow -> reads as an opening)
NECK   = "#9b9488"   # cobblestone_wall pier-crown finials + beacon neck (mid-grey, reads round)
BANNER = "#b8772e"   # white_wall_banner mounted FLAT on the outer pier face (biome-tinted orange here)
BANRIM = "#7a4d18"   # banner dark border / mount bar (reads it as hung cloth, flat on stone)
ROAD   = "#6f5d3e"   # dirt carriageway running UNDER the arch (through the pier gap)
KERB   = "#8a847a"   # andesite kerb framing the carriageway edges

GLOW   = "#ffd47a"   # warm lantern light
CROWN  = "#eafff8"   # icy beacon light (brightest -- the parapet beacon head)
LINK   = "#c9c9d2"   # chain link colour

# ============================================================================
# LAYOUT (gatehouse-proven): the carriageway runs along DEPTH (z), through the gap between two
#   3x3 piers that flank along X. The mouth OPENS toward the viewer at high-z (front).
#     West pier x=0..3 ; ROAD GAP x=3..4 (kept genuinely EMPTY) ; East pier x=4..7  (7 wide).
#   Piers are 3 deep (z=1..4), the road tunnel runs z=0..5 through the gap. Up = y.
#   The gap between the 3x3 piers is 1 wide of clear sky here at render scale; the road floor +
#   dark recess + arch rib all sit IN that gap so "the road passes under the arch" reads.
# ============================================================================

# ---- ROAD: the carriageway floor running THROUGH the gap, front to back (the whole point) ----
S.box(3, -1.0, 0, 1, 7, 0.4, ROAD)                   # dirt carriageway floor through the gap (extends front+back)
S.box(2.7, -1.0, 0, 0.3, 7, 0.4, KERB)              # west kerb lining the road
S.box(4.0, -1.0, 0, 0.3, 7, 0.4, KERB)              # east kerb lining the road

# ============================================================================
# L0 -- 7x5 stone_bricks PLINTH under BOTH piers; the road gap is left open (no plinth in x=3..4
#       so the carriageway is a true gap). Outer corners chiseled.
# ============================================================================
S.box(0, 0, 0, 3, 5, 1, PLINTH)                      # west pier plinth
S.box(4, 0, 0, 3, 5, 1, PLINTH)                      # east pier plinth
for (cx, cz) in [(0, 0), (6, 0), (0, 4), (6, 4)]:    # outer dressed corner quoins (chiseled)
    S.box(cx, cz, 0, 1, 1, 1, CHIS)

# ---- stepped stair FOOT skirting down around each pier (monument foot, avenue scale) ----
for px in (0, 4):
    S.box(px, 4, 1, 3, 1, 0.5, STEP)                 # FRONT (road-facing) stair foot
    S.box(px, 0, 1, 3, 1, 0.5, STEP)                 # back stair foot
    ox = px if px == 0 else px+2                      # outer-x edge of each pier
    S.box(ox, 1, 1, 1, 3, 0.5, STEP)                 # outer-x stair foot

# ============================================================================
# PIER BUILDER -- each pier: SOLID 3x3 drum (3 courses) with chiseled front face + corner
# pilasters + a mid band, an inward stair-taper to a 1x1 dark-oak finial shaft, a slate collar,
# and a cobblestone-wall crown finial + a flat outer-face banner. Every block rests on the one below.
# ============================================================================
def pier(px):
    pz = 1                                            # piers sit z=1..4 (3 deep, behind the front road)
    # L1-L3: SOLID 3x3 drum, 3 courses tall (the real tower-base mass)
    S.box(px, pz, 1, 3, 3, 1, DRUM, seam=True)        # drum course 1 (dark body)
    S.box(px, pz, 2, 3, 3, 1, BAND, seam=True)        # drum course 2 (mid band breaks the mass)
    S.box(px, pz, 3, 3, 3, 1, DRUM, seam=True)        # drum course 3 (dark body)
    # chiseled HERO front face on the road-facing (high-z) side, all 3 courses (near-white pops)
    S.box(px, pz+2.55, 1, 3, 0.45, 3, CHIS, seam=True)  # dressed chiseled front facing the road
    # corner pilasters: stone_brick_wall on the 4 drum corners, grounded, purely vertical
    for (ox, oz) in [(0, 0), (2, 0), (0, 2), (2, 2)]:
        S.box(px+ox, pz+oz, 1, 1, 1, 3, PILA, seam=True)  # corner pilaster rising the full drum
    # L4 taper: inward stair shoulder on the 3x3 perimeter chamfering down to a centred 1x1;
    # centre cell a full chiseled block carrying the finial shaft (solid load path under cladding).
    S.box(px, pz, 4, 3, 3, 0.6, TAPER)                # 3x3 inward stair-taper shoulder (pale)
    S.box(px+1, pz+1, 4, 1, 1, 0.6, CHIS)             # centre load block (carries the shaft)
    S.box(px, pz, 4.6, 3, 3, 0.4, CAP)                # slate coping collar capping the taper (dark anchor)
    # L5-L6: 1x1 stripped_dark_oak finial SHAFT rising from the centre cell
    S.box(px+1, pz+1, 5, 1, 1, 2, SHAFT, seam=True)   # dark-timber finial shaft
    S.box(px+1, pz+1.95, 5, 1, 0.05, 2, SHAFTL)       # lit front edge reads the log courses
    # pier crown: cobblestone_wall finial on the shaft cap (the crown lantern stands on it)
    S.box(px+1, pz+1, 7, 1, 1, 0.8, NECK, seam=True)  # cobblestone_wall crown finial
    # flat civic BANNER mounted FLAT on the OUTER pier face (not a free flagpole) -- TRUE cloth
    # proportion (~1 wide, hung high), centred on the outer-x face, reading as part of the pier mass.
    # Only the EAST pier's outer face (high-x) is viewer-visible in iso; the west banner sits on the
    # hidden west face (rendered for completeness, mostly occluded -- the silhouette stays clean).
    bx = px if px == 0 else px+3                       # outer-x face plane of each pier
    bxoff = bx - 0.16 if px == 0 else bx               # banner stands just proud of the outer face
    S.box(bxoff, pz+1.0, 2.4, 0.16, 1.0, 2.1, BANNER) # flat banner cloth (1 wide, centred, hung high)
    S.box(bxoff, pz+1.0, 4.5, 0.16, 1.0, 0.22, BANRIM)# banner mount bar (top border, reads it hung)

pier(0)                                               # WEST pier (x=0..3)
pier(4)                                               # EAST pier (x=4..7)

# ============================================================================
# DARK RECESS closing the tunnel back BEHIND the road gap, so the mouth reads as a shadowed
# opening you pass into (the gatehouse spandrel/deep-mouth technique).
# ============================================================================
S.box(3, 1, 1, 1, 3, 4, RECESS)                       # dark tunnel-back mass in the gap (behind the arch rib)

# ============================================================================
# THE CORBELLED FLAT STAIR-ARCH (catalog C) as a FRONT RIB spanning the two pier tops OVER the
# road. From each pier inner top edge, stone_brick_stairs step one block IN (toward x=3.5) and one
# UP toward centre, each course resting on the one below (cantilever within 1 block = supported),
# meeting at a single chiseled KEYSTONE. Clearance under the keystone is sized to the carriageway
# (the road passes beneath, >=3 tall). Rendered at the FRONT depth band (z~3.5) so it reads.
# ============================================================================
AZ = 3.4   # arch rib front depth (just in front of the pier front faces so it reads as the rib)
# West corbels: spring from the west pier inner-top (x=3 edge), step in toward x=3.5 + up.
S.box(2.3, AZ, 4.6, 0.9, 1.1, 0.55, ARCH)             # west springer (on the west pier inner shoulder)
S.box(2.7, AZ, 5.15, 0.9, 1.1, 0.55, ARCHD)           # west corbel course 1 (in + up, rests on springer)
S.box(3.0, AZ, 5.7, 0.8, 1.1, 0.55, ARCH)             # west corbel course 2 (in + up, rests on c1)
# East corbels: spring from the east pier inner-top (x=4 edge), step in toward x=3.5 + up.
S.box(3.8, AZ, 4.6, 0.9, 1.1, 0.55, ARCH)             # east springer
S.box(3.4, AZ, 5.15, 0.9, 1.1, 0.55, ARCHD)           # east corbel course 1 (in + up, rests on springer)
S.box(3.2, AZ, 5.7, 0.8, 1.1, 0.55, ARCH)             # east corbel course 2 (in + up, rests on c1)
# KEYSTONE: a single chiseled_stone_bricks block where the two corbelled sides meet (the centre).
S.box(2.9, AZ-0.1, 6.2, 1.2, 1.25, 0.95, KEY)         # chiseled keystone (brightest hero -> arch centre)

# ============================================================================
# L9 -- ARCH DECK / CROWN ROW: the arch top decked with a stone_brick_slab parapet so it reads as a
# WALKABLE LINTEL (not a thin rib); above the keystone a SHORT THICK MAST -> central beacon (no
# spindly stack). The deck bridges keystone-to-pier-tops, reading the lintel as one member.
# ============================================================================
S.box(2.6, AZ-0.15, 7.1, 1.8, 1.35, 0.4, DECK)        # stone_brick_slab parapet deck on the arch top
S.box(3.1, AZ-0.05, 7.5, 0.8, 0.9, 0.9, CHIS, seam=True)  # short thick chiseled beacon mast (no spindle)
S.box(3.1, AZ-0.05, 8.4, 0.8, 0.9, 0.4, CAP)          # slate beacon collar (the dark anchor under the beacon)

# ============================================================================
# ACCENTS -- 6-to-8 lights (the Great-Road rung): under-arch road lighting + 2 pier crowns + beacon.
# Chains = stacked dot accents (hardware present on Highway+; here under the arch over the road).
# ============================================================================
def chain_hang(x, z, y_top, links, lantern_color=GLOW, r=2.4):
    for k in range(links):
        S.accent(x, z, y_top - 0.42 * k, "dot", LINK, r=1.3)
    S.accent(x, z, y_top - 0.42 * links - 0.3, "glow", lantern_color, r=r)

# 4 CHAIN-hung lanterns under the arch (catalog: 2-or-4; drawn as the 4 case) lighting the road
# FROM ABOVE -- hung off the corbel/keystone underside down INTO the mouth, across the carriageway.
chain_hang(3.5, 3.7, 5.5, 2)                          # centre under-keystone lantern (front of the mouth)
chain_hang(3.5, 2.6, 5.5, 2)                          # centre under-keystone lantern (deeper in the mouth)
chain_hang(3.05, 4.0, 5.0, 2, r=2.2)                  # west-of-keystone under-arch lantern
chain_hang(3.95, 4.0, 5.0, 2, r=2.2)                  # east-of-keystone under-arch lantern

# 2 pier-crown lanterns standing on the cobblestone-wall finials
S.accent(1.5, 2.5, 8.0, "glow", GLOW, r=2.6)          # west pier crown lantern
S.accent(5.5, 2.5, 8.0, "glow", GLOW, r=2.6)          # east pier crown lantern

# central parapet BEACON standing on the mast (brightest -> the head of the gateway)
S.accent(3.5, 3.4, 9.0, "glow", CROWN, r=3.2)         # central parapet beacon
S.accent(3.5, 3.4, 9.2, "finial")                     # beacon finial spike crowning the gateway

# ============================================================================
# CALLOUT LABELS
# ============================================================================
S.label(3.5, 3.4, 9.1, "central parapet BEACON on a short thick mast (the gateway head)")
S.label(3.5, 3.4, 6.4, "chiseled KEYSTONE -- chain-hung lanterns light the road FROM ABOVE (2-4)")
S.label(2.6, 3.4, 5.0, "corbelled flat STAIR-arch: stairs step in+up to the keystone")
S.label(1.5, 2.5, 8.0, "pier crown lantern on a cobblestone-wall finial (x2)")
S.label(0.0, 2.5, 3.8, "flat civic BANNER mounted FLAT on the outer pier face (biome-tinted)")
S.label(5.0, 4.0, 2.5, "SOLID 3x3 chiseled pier drum + corner pilasters (twin tower-bases)")
S.label(0, 4, 0.5, "7x5 plinth, stepped pier feet (road gap left open)")
S.label(3.5, 5.0, 0.2, "the road passes THROUGH the gap, UNDER the arch")

out = S.svg(title="Lamp-post R5 (Great Road) -- a monumental TWIN-PIER LIGHT-ARCH the avenue passes beneath: solid 3x3 piers, corbelled keystone arch lighting the road from above, parapet beacon + flat civic banners",
            size_label="7x5 plinth - twin 3x3 piers - h14 - 6-8 lights (4 under-arch + 2 crowns + beacon) - a GATEWAY",
            label_w=430)
open("detail_svg/lamp_post.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/lamp_post.svg | bytes", len(out.encode()))
