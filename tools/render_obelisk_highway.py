"""Obelisk HIGHWAY (R3) -> detail_svg/obelisk_highway.svg.
Per deco_catalog_v2.json id 'obelisk' tier Highway (footprint 9x9 plinth / 1x1 shaft thickening to
3x3 at base, height 19, L0..L18 visible): the BIG non-linear jump -- this is where it leaps to
GRAND. Footprint 5x5->9x9, height 11->19 (+8); a THREE-tier walkable stepped plinth; the single
shaft becomes a thick 3x3 BUTTRESSED base (battered corner stairs leaning in) that SHOULDERS in to
a 1x1 needle via a flared 5x5 corbel ring; a continuous flute-spine up the 3x3 lower shaft; a
deterministic %3 flute on the upper needle; a 3x3 crown collar; and a SEA-LANTERN BEACON-CORE cap
that glows through a slab seam, tipped with an end-rod finial spark. A genuine landmark.

Same wnl_obelisk whose top tier is render_obelisk.py (the soaring needle + pyramidion). MATCHED to
render_cairn_highway.py craft -- the rung directly under the capital monument. Inspiration
(FORM/SCALE/TECHNIQUE only, credited in CREDITS.md, no assets/NBT/palette copied): Roman honorific
column + stepped-plinth/corbel-collar masonry (CTOV / D&T tower-obelisks) + the pyramidion-on-
tapering-shaft archetype. Original WNL geometry, vanilla blocks only.
ISO: road-facing FRONT = high-z (south) + high-x (east)."""
from iso_render import Iso

S = Iso(U=13)

# palette (literal) -- WIDE-CONTRAST luminance ladder; every vanilla block reads as itself.
# Highway introduces the LIGHT smooth-stone hero faces (the shaft pops near-white above the plinth)
# + polished_andesite as the cool walkable platform band, exactly as the spec's palette_slots.
# Ladder dark->light: BURIED < STAIR < ANDE < PBASE < BAND < BRICK < SMOOTH < CHIS ; lights by hue.
BURIED = "#544e45"   # buried L-1 stone_bricks course (darkest -> sits IN terrain)
STAIR  = "#665f55"   # stone_brick_stairs skirts / buttresses / collar darks (shadowed stepped read)
ANDE   = "#6f7177"   # polished_andesite walkable platform top (cool grey band -> reads distinct)
PBASE  = "#8c8579"   # stone_bricks plinth/ring mass (warm mid grey)
BAND   = "#a09a8a"   # mossy/mid band note breaking the pale mass (between PBASE and BRICK)
BRICK  = "#b4ae9d"   # stone_bricks shaft course (mid-light)
SMOOTH = "#dcd7ca"   # smooth_stone shaft faces (near-white hero -> the needle reads tall + lit)
CHIS   = "#c9c2b2"   # chiseled_stone_bricks flute-spine / corners / collar / cap (carved light read)
SEAL   = "#bfeee4"   # sea_lantern beacon-core block (cyan-white -> the glowing cap, by hue)
LANT   = "#ffd47a"   # lantern glow (the 4 flanking plinth lights -- warm)
SLATE  = "#3c3843"   # stone_brick_slab seam-cap over the beacon core (deep cool -> max light contrast)

# Shaft centre = the 3x3 block centred at x=3,z=3 on the 9x9 plinth (origin 0..9 -> centre cell 4,4).
CX, CZ = 4, 4   # the 1x1 needle cell; the 3x3 lower shaft spans 3..6

# === BURIED L-1 (9x9 grounding course) ====================================
S.box(0, 0, -0.5, 9, 9, 0.55, BURIED, seam=True)

# === L0 (9x9 plinth step 1: broad walkable ground skirt) ==================
# polished_andesite walkable top; full perimeter stone_brick_stairs OUTWARD; chiseled corners.
S.box(0, 0, 0, 9, 9, 1, ANDE, seam=True)
for (cx, cz) in [(0, 0), (8, 0), (0, 8), (8, 8)]:        # chiseled corners
    S.box(cx, cz, 0, 1, 1, 1, CHIS)
for e in (1, 2, 3, 4, 5, 6, 7):                          # outward perimeter skirt stairs (grounded flare)
    S.box(e, -0.22, 0, 1, 0.7, 0.5, STAIR)               # N skirt
    S.box(e, 8.52, 0, 1, 0.7, 0.5, STAIR)                # S(front) skirt
    S.box(-0.22, e, 0, 0.7, 1, 0.5, STAIR)              # W skirt
    S.box(8.52, e, 0, 0.7, 1, 0.5, STAIR)               # E skirt

# === L1 (7x7 plinth step 2: ring + four WALL-POST lanterns) ===============
# stone_bricks platform, chiseled edge ring; the four cardinal mid-edges carry stone_brick_wall
# posts crowned with lanterns (4 grounded flanking lights). Inward stairs lift toward step 3.
S.box(1, 1, 1, 7, 7, 1, PBASE, seam=True)
for (cx, cz) in [(1, 1), (7, 1), (1, 7), (7, 7)]:        # chiseled edge-ring corners
    S.box(cx, cz, 1, 1, 1, 1, CHIS)
wall_posts = [(4, 1), (4, 7), (1, 4), (7, 4)]            # N, S(front), W, E cardinal mid-edges
for (px, pz) in wall_posts:
    S.box(px + 0.25, pz + 0.25, 2, 0.5, 0.5, 1.4, STAIR)  # wall-post neck rising off the L1 ring

# === L2 (5x5 plinth step 3: chiseled ring + inward stairs to the shaft) ===
# chiseled ring, solid stone_bricks centre; cardinal mid-edges inward stairs -> three-tier plinth,
# the non-linear payoff begins.
S.box(2, 2, 2, 5, 5, 1, PBASE, seam=True)
for (cx, cz) in [(2, 2), (6, 2), (2, 6), (6, 6)]:        # chiseled ring corners
    S.box(cx, cz, 2, 1, 1, 1, CHIS)
S.box(4, 2.2, 2, 1, 0.8, 0.5, STAIR)                     # N inward
S.box(4, 3.0, 2, 1, 0.8, 0.5, STAIR)                     # S(front) inward
S.box(2.2, 4, 2, 0.8, 1, 0.5, STAIR)                     # W inward
S.box(3.0, 4, 2, 0.8, 1, 0.5, STAIR)                     # E inward

# === L3 (3x3 shaft base / battered buttress) ==============================
# A 3x3 mass: four corners as stone_brick_stairs battered IN toward the shaft (stair-back to centre,
# step facing out), the four cardinal faces + centre chiseled. Thickens the foot so the tall shaft
# reads load-bearing. The buttress stairs rest on the L2 step (grounded) + lean <=0.3 toward centre.
S.box(3, 3, 3, 3, 3, 1, CHIS, seam=True)                 # solid 3x3 chiseled base mass
for (bx, bz) in [(3, 3), (5, 3), (3, 5), (5, 5)]:        # four battered corner buttresses (lean IN)
    lean_x = 0.28 if bx == 3 else -0.28
    lean_z = 0.28 if bz == 3 else -0.28
    S.box(bx + lean_x, bz + lean_z, 3, 1, 1, 0.85, STAIR)  # battered buttress block, leaning toward shaft

# === L4..L5 (3x3 shaft lower, 2 courses, continuous FLUTE-SPINE) ==========
# Outer shell = smooth_stone faces; the centre column of each face is the flute-spine (chiseled)
# running continuously up; corners stone_bricks; core stone_bricks. Light smooth-stone hero faces.
for ly in (4, 5):
    S.box(3, 3, ly, 3, 3, 1, SMOOTH, seam=True)          # 3x3 smooth-stone face mass
    S.box(4, 3, ly, 1, 3, 1, CHIS)                       # flute-spine centre column (N-S faces)
    S.box(3, 4, ly, 3, 1, 1, CHIS)                       # flute-spine centre column (E-W faces)
    for (cx, cz) in [(3, 3), (5, 3), (3, 5), (5, 5)]:    # stone-brick corners
        S.box(cx, cz, ly, 1, 1, 1, BRICK)

# === L6 (5x5 corbel SHOULDER: shaft shoulders, then steps IN to 1x1) ======
# A flared stone_brick_stairs corbel ring (OUTWARD) over a chiseled 5x5 ring -- the shaft 'shoulders'
# -- then the needle above occupies just the 1x1 centre. The ring rests on the 3x3 lower shaft +
# the L2 step corners below it (grounded), stairs nudged <=0.25 out.
S.box(2, 2, 6, 5, 5, 1, CHIS, seam=True)                 # chiseled 5x5 shoulder ring
for e in (2, 3, 4, 5, 6):                                # outward corbel stairs round the shoulder edge
    S.box(e, 1.78, 6, 1, 0.7, 0.5, STAIR)                # N corbel
    S.box(e, 6.52, 6, 1, 0.7, 0.5, STAIR)                # S(front) corbel
    S.box(1.78, e, 6, 0.7, 1, 0.5, STAIR)               # W corbel
    S.box(6.52, e, 6, 0.7, 1, 0.5, STAIR)               # E corbel

# === L7..L15 (1x1 upper needle, 9 courses, deterministic %3 flute map) ====
# the soaring needle. k counted 0 at L7: k%3==0 -> chiseled (flute at L7,L10,L13); k%3==1 -> one
# smooth_stone tonal course; else stone_bricks. One remote non-flute course swapped cracked.
for k in range(9):
    ly = 7 + k
    if k % 3 == 0:
        col = CHIS               # flute course
    elif k % 3 == 1:
        col = SMOOTH             # smooth-stone tonal course
    else:
        col = BRICK
    if ly == 14:                 # the one remote cracked course (decay-hash note)
        col = BAND
    S.box(CX, CZ, ly, 1, 1, 1, col, seam=True)

# === L16 (1x1 -> 3x3 CROWN COLLAR) ========================================
# grounded corbel crown -- chiseled centre, four stone_brick_stairs OUTWARD on cardinal mid-edges,
# stone_brick_slab corners. The >=3x3 support for the beacon cap.
S.box(CX, CZ, 16, 1, 1, 1, CHIS)                         # collar centre (solid -> the beacon core seats here)
for (cx, cz) in [(3, 3), (5, 3), (3, 5), (5, 5)]:        # slab corners (bottom slabs)
    S.box(cx, cz, 16, 1, 1, 0.5, PBASE)
S.box(4, 2.95, 16, 1, 0.8, 0.5, STAIR)                   # N outward corbel
S.box(4, 5.25, 16, 1, 0.8, 0.5, STAIR)                   # S(front) outward corbel
S.box(2.95, 4, 16, 0.8, 1, 0.5, STAIR)                  # W outward corbel
S.box(5.25, 4, 16, 0.8, 1, 0.5, STAIR)                  # E outward corbel

# === L17 (beacon-core: sea_lantern wrapped by slab seam) ==================
# ONE sea_lantern on the solid L16 centre block (grounded), wrapped at this course by four
# stone_brick_slab[type=top] sitting on the L16 collar's cardinal stair-tops, so light bleeds
# through the seam between slab and lantern.
S.box(CX, CZ, 17, 1, 1, 1, SEAL)                         # sea-lantern beacon core
# four seam slabs on the collar stair-tops, abutting the lantern's four sides (top-slabs, raised 0.5)
S.box(4, 3.05, 17.5, 1, 0.7, 0.5, PBASE)                 # N seam slab
S.box(4, 5.25, 17.5, 1, 0.7, 0.5, PBASE)                 # S seam slab
S.box(3.05, 4, 17.5, 0.7, 1, 0.5, PBASE)                # W seam slab
S.box(5.25, 4, 17.5, 0.7, 1, 0.5, PBASE)                # E seam slab

# === L18 (cap apex: chiseled block capping the lantern + end-rod finial) ===
S.box(CX, CZ, 18, 1, 1, 1, SLATE, seam=True)             # dark chiseled cap (slate read -> the spark pops)

# ============================ ACCENTS (lights / finial) ===================
# four flanking lanterns on the L1 wall-post tops (y ~3.4)
for (px, pz) in wall_posts:
    S.accent(px + 0.5, pz + 0.5, 3.5, "glow", LANT, r=2.0)
# beacon-core glow bleeding through the L17 slab seam
S.accent(CX + 0.5, CZ + 0.5, 17.5, "glow", "#dff6ef", r=3.0)
# end-rod finial spark at the very tip, grounded on the L18 cap
S.accent(CX + 0.5, CZ + 0.5, 19, "finial")

S.label(CX + 0.5, CZ + 0.5, 19, "sea-lantern beacon cap (glows through a slab seam) + end-rod finial")
S.label(CX + 0.5, CZ + 0.5, 16.4, "3x3 crown collar -- grounds the beacon core (no floating cap)")
S.label(CX + 0.5, CZ + 0.5, 11.0, "soaring 1x1 needle -- deterministic %3 flute (smooth + chiseled)")
S.label(6.6, 4, 6.4, "flared 5x5 corbel shoulder -- the shaft steps IN to the needle")
S.label(6.6, 4, 4.4, "thick 3x3 flute-spine lower shaft on battered corner buttresses")
S.label(7, 4, 3.4, "4 flanking lanterns on wall posts (plinth step 2)")
S.label(2, 6, 2.4, "THREE-tier walkable stepped plinth (9->7->5)")
S.label(0, 8, 0.5, "broad 9x9 ground skirt -- polished-andesite walkable top")

out = S.svg(title="Obelisk R3 (Highway) -- GRAND landmark: 3-tier plinth, buttressed 3x3 shaft shouldering to a flute needle, sea-lantern beacon cap",
            size_label="9x9 plinth -> 3x3 base -> 1x1 needle * h19 * 5 lanterns (one step under the capital monument)",
            label_w=388)
open("detail_svg/obelisk_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/obelisk_highway.svg | bytes", len(out.encode()))
