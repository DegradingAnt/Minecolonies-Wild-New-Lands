"""Gatehouse ROAD (R3) -> detail_svg/gatehouse_road.svg.
Per deco_catalog_v2.json id 'gatehouse' tier Road (footprint 9x5, opening 5 clear, height 9):
the real jump -- leaves the single-plane timber arch behind for TWO SOLID STONE PIERS carrying a
true segmental VOUSSOIR ARCH with a chiseled keystone, a recessed LIT GUARD NICHE in the left
pier, capped piers with a token crenel, and a hanging passage sign. First tier reading as
defensible infrastructure; first NBT tier. Same wnl_gatehouse family as render_gatehouse.py (top).

VAULT closing per build_technique (W=5): y5 springer stair each wall; y6 corbel 1 stair each side;
y7 flat keystone block at the crown. Symmetric, closes over the 5-clear opening.
ISO: road-facing FRONT = high-z (south) + high-x (east); niche + keystone + sign read on the front.
Inspiration: Roman/medieval stone gate-arch + voussoir technique only -- credited in CREDITS.md."""
from iso_render import Iso

S = Iso(U=17)

# ---- palette (literal) -- WIDE-CONTRAST stone ladder, each material reads as itself.
#      luminance dark->light: NICHE < SILL < PIER < CORE < ARCH < SLAB < MERL < KEY ; warm LEDGE; LANT warm.
PIER  = "#7c766a"   # stone_bricks solid piers (dark warm dressed stone -> the heavy mass)
CORE  = "#8a8276"   # cobblestone threshold sill + parapet band (mid grey)
ARCH  = "#9c9486"   # voussoir stones of the arch (lighter -> the ring reads as cut wedges)
ARCHD = "#857e72"   # alternating darker voussoir (course-to-course read of separate stones)
KEY   = "#cfc8b6"   # chiseled keystone + crenel merlon caps (brightest dressed stone)
PANEL = "#b9b3a5"   # chiseled relief panel on the outward pier faces (bright)
SLAB  = "#aaa394"   # stone_brick_slab pier caps (light mid -> reads as the capping course)
MERL  = "#b3ac9d"   # crenel merlon block (light -> the token battlement pops off the band)
NICHE = "#403c34"   # recessed guard-niche back (dark recess -> reads hollowed-in)
SILL  = "#6f685d"   # threshold doorstep + niche floor (dark, sits in the ground)
NECK  = "#9a9384"   # cobblestone_wall lantern post on the pier tops
BARREL= "#7a5c3a"   # guard-niche barrel prop (warm timber -> the manned note)
LEDGE = "#6b523a"   # niche barrel lid hoop (darker warm band)
LANT  = "#ffd47a"   # lantern glow

# =====================================================================================
# Course 0 (ground/plinth): two PIER BASES, each 2x3 (x by z), at x=0..1 and x=7..8 spanning
# z=1..3. Opening between piers = 5 clear. A CORE threshold SILL across the passage floor
# (x=2..6, z=2) as a paved doorstep -- sunk so it sits in the ground (rooted, the road runs over it).
# =====================================================================================
S.box(0, 1, 0, 2, 3, 1, PIER, seam=True)          # left pier base 2x3
S.box(7, 1, 0, 2, 3, 1, PIER, seam=True)          # right pier base 2x3
S.box(2, 2, 0, 5, 1, 0.4, SILL)                   # paved threshold doorstep (sunk -> sits in ground)

# =====================================================================================
# Courses 1-5 (piers): grow each pier up to y=5 as a solid 2x3 block. On each OUTWARD face an
# inset chiseled RELIEF PANEL at y=3. The LEFT pier's passage-facing side is hollowed into a
# GUARD NICHE (1x1x2 at y=2..3) holding a barrel + a lantern (the manned read).
# =====================================================================================
S.box(0, 1, 1, 2, 3, 7, PIER, seam=True)          # left pier shaft y1..8 (rises to the parapet -- NO floating top)
S.box(7, 1, 1, 2, 3, 7, PIER, seam=True)          # right pier shaft y1..8
# outward-face chiseled relief panels (proud, catch light) -- left=west face, right=east face
S.box(-0.12, 1.4, 3, 0.2, 1.2, 1.2, PANEL)        # left pier outward relief panel (west face)
S.box(8.92, 1.4, 3, 0.2, 1.2, 1.2, PANEL)         # right pier outward relief panel (east face)
# GUARD NICHE hollowed into the left pier's passage-facing (inner, x=2) side, y=2..3
S.box(1.0, 1.6, 2, 1.0, 1.0, 2, NICHE)            # dark recessed niche box (reads hollowed-in)
S.box(1.15, 1.7, 2, 0.8, 0.8, 0.1, SILL)          # niche floor ledge (the prop sits ON this)
S.box(1.2, 1.75, 2.1, 0.65, 0.65, 1.0, BARREL)    # guard barrel prop standing on the niche floor
S.box(1.2, 1.75, 2.45, 0.65, 0.65, 0.12, LEDGE)   # barrel lid hoop (2-tone)

# =====================================================================================
# Courses 5-7 (segmental voussoir arch, span W=5): true arch over the opening, voussoirs
# alternating ARCH/ARCHD so each wedge reads as a separate cut stone. Springers spring from the
# pier inner faces (x=2 and x=6); corbel in one each side at y6; flat chiseled keystone at y7.
# Each voussoir bears on the one below / the pier -> grounded ring, closes symmetric over W=5.
# =====================================================================================
# dark vault-back behind the opening FIRST (so it reads as a deep gateway mouth, not a hole to sky)
S.box(2, 1, 0, 5, 0.5, 8, NICHE)                  # recessed tunnel back wall (x2..7, at the back row, y0..8)
# stepped voussoir arch over the opening, FULL pier depth (z1..4) so it reads as a solid ring bridging
# the piers (not a thin floating ribbon). Springers y5, corbels y6, keystone y7.
S.box(2, 1, 5, 1, 3, 1, ARCH)                     # left springer (bears on left pier inner top)
S.box(6, 1, 5, 1, 3, 1, ARCH)                     # right springer (bears on right pier)
S.box(3, 1, 6, 1, 3, 1, ARCHD)                    # left corbel (steps in 1)
S.box(5, 1, 6, 1, 3, 1, ARCHD)                    # right corbel
S.box(4, 1, 7, 1, 3, 1, KEY)                      # chiseled KEYSTONE at the crown (closes W=5)
# spandrel fill -> solid wall above the arch ties cleanly into the parapet (no floating gap left)
S.box(2, 1, 6, 1, 3, 1, ARCH)                     # left spandrel (above springer, beside corbel)
S.box(6, 1, 6, 1, 3, 1, ARCH)                     # right spandrel
S.box(2, 1, 7, 2, 3, 1, CORE)                     # y7 wall course left of the keystone (x2..4)
S.box(5, 1, 7, 2, 3, 1, CORE)                     # y7 wall course right of the keystone (x5..7)

# =====================================================================================
# Courses 7-8 (parapet band): a continuous CORE course across BOTH piers and over the arch crown
# (y=8), tying them into one wall. Then a SLAB cap on each pier top + a token crenel (1 merlon /
# 1 gap) for a hint of battlement.
# =====================================================================================
S.box(0, 1, 8, 9, 3, 1, CORE, seam=True)          # parapet band ties piers + arch into one wall
S.box(0, 1, 9, 2, 3, 0.3, SLAB)                   # left pier slab cap
S.box(7, 1, 9, 2, 3, 0.3, SLAB)                   # right pier slab cap
# token crenel on each pier cap: 1 merlon block + 1 gap (the hint of battlement)
S.box(0.0, 2.0, 9.3, 1, 1, 1, MERL)               # left merlon (front-half block; the other half is the gap)
S.box(8.0, 2.0, 9.3, 1, 1, 1, MERL)               # right merlon

# =====================================================================================
# Courses 8-9 (lights + sign): a LANTERN on a short wall-post at each pier top (grounded on the
# parapet), and a hanging passage SIGN on the arch soffit at x=4 (held by the arch above).
# =====================================================================================
S.box(0.4, 2.0, 9.3, 0.7, 0.7, 1.0, NECK)         # left wall-post (grounded on the parapet cap)
S.box(7.9, 2.0, 9.3, 0.7, 0.7, 1.0, NECK)         # right wall-post
S.box(3.6, 2.55, 6.1, 0.8, 0.12, 0.6, BARREL)     # hanging passage sign under the arch soffit (held above)

# =====================================================================================
# LIGHTING (FIRST defensible tier keeps it functional): niche lantern + 1 per pier-top + the sign.
# =====================================================================================
S.accent(1.6, 2.7, 2.8, "glow", LANT, r=2.0)      # guard-niche lantern (the manned glow on the road face)
S.accent(0.75, 2.3, 10.5, "glow", LANT, r=2.2)    # left pier-top wall-post lantern
S.accent(8.25, 2.3, 10.5, "glow", LANT, r=2.2)    # right pier-top wall-post lantern
S.accent(4.0, 2.7, 5.7, "glow", "#ffe6a8", r=1.8) # the hanging passage sign lit under the arch

S.label(4.0, 2.0, 7.4, "true voussoir arch -- chiseled KEYSTONE at the crown (W=5 clear)")
S.label(1.6, 2.7, 3.0, "recessed LIT GUARD NICHE (barrel + lantern) in the left pier")
S.label(8.25, 2.3, 10.5, "wall-post lantern on each capped pier + token crenel")
S.label(4.0, 2.5, 5.8, "hanging passage sign under the arch soffit")
S.label(0.0, 1.0, 3.0, "two SOLID stone piers + outward relief panels")
S.label(2.0, 2.0, 0.4, "paved threshold sill -- the road passes THROUGH (5 clear)")

out = S.svg(title="Gatehouse R3 (Road) -- solid stone piers carry a keystoned voussoir arch; lit guard niche, token crenel",
            size_label="9x5 foot (5 clear) * h9 * 4 lanterns (first defensible infrastructure -- first NBT tier)",
            label_w=372)
open("detail_svg/gatehouse_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/gatehouse_road.svg | bytes", len(out.encode()))
