"""Obelisk GREAT ROAD (R4) -> detail_svg/obelisk_great.svg.
Per deco_catalog_v2.json id 'obelisk' tier Great Road (footprint 15x15 main plinth + two grounded
3x3 attendant pads flanking the approach, 3x3 shaft shouldering to 1x1, height 27, L0..L26 visible):
the grandest STANDARD leap below the Forum-Pillar capstone -- a capital monument. Footprint
9x9->15x15 (+two grounded attendant mini-obelisks), height 19->27 (+8), a FOUR-tier walkable
ceremonial plinth, four corner SEA-LANTERN beacons hooded by slabs, a pair of approach BANNERS, a
battered 3x3 buttressed shaft base, a continuous flute-spine lower shaft, a flared 5x5 corbel
shoulder, a soaring tapered needle on a deterministic %3 flute, a double-flared crown collar, and a
taller 1x2 SEA-LANTERN beacon-core cap tipped with an end-rod. From landmark to capital monument.

Same wnl_obelisk whose top tier (the Forum Pillar / soaring needle) is render_obelisk.py. MATCHED
to the cairn lower-tier template + render_cairn_highway.py craft. Inspiration (FORM/SCALE/TECHNIQUE
only, credited in CREDITS.md, no assets/NBT/palette copied): the Roman civic-obelisk / honorific-
column + forum-platform massing + the attendant-column arrangement; stepped-plinth/corner-beacon/
corbel-collar masonry (CTOV / D&T tower-obelisks). Original WNL geometry, vanilla blocks only.
ISO: road-facing FRONT/approach = high-z (south); attendants + banners read on that front."""
from iso_render import Iso

S = Iso(U=10)

# palette (literal) -- WIDE-CONTRAST luminance ladder; every vanilla block reads as itself.
# Same family as Highway but grander: smooth-stone hero needle, polished-andesite cool platform
# bands, the one warm BANNER accent, sea-lantern beacon cores. Ladder dark->light:
# BURIED < STAIR < ANDE < PBASE < BAND < BRICK < SMOOTH < CHIS ; lights + banner by hue.
BURIED = "#544e45"   # buried L-1 stone_bricks course (darkest -> sits IN terrain)
STAIR  = "#665f55"   # stone_brick_stairs skirts / buttresses / collar / wall-posts (shadowed steps)
ANDE   = "#6f7177"   # polished_andesite walkable platform bands (cool grey -> reads distinct)
PBASE  = "#8c8579"   # stone_bricks ring / platform mass (warm mid grey)
BAND   = "#a09a8a"   # mid tonal band note (between PBASE and BRICK)
BRICK  = "#b4ae9d"   # stone_bricks shaft course (mid-light)
SMOOTH = "#dcd7ca"   # smooth_stone shaft faces (near-white hero -> the needle reads tall + lit)
CHIS   = "#c9c2b2"   # chiseled_stone_bricks flute-spine / corners / collars / cap (carved light)
SEAL   = "#bfeee4"   # sea_lantern beacon-core / corner-beacon blocks (cyan-white glow, by hue)
LANT   = "#ffd47a"   # lantern glow (attendant-stone finial lights -- warm)
SLATE  = "#3c3843"   # stone_brick_slab hoods over the corner beacons + apex cap (deep cool)
BANNER = "#d4b25f"   # white_banner cloth, palette-tinted (the one saturated warm accent)
POST   = "#6f5535"   # banner timber pole crown

# Shaft centre: the 3x3 lower shaft is centred at x=6,z=6 on the 15x15 plinth (origin 0..15);
# the 1x1 needle occupies the centre cell (7,7).
CX, CZ = 7, 7

# === BURIED L-1 (15x15 grounding course) ==================================
S.box(0, 0, -0.5, 15, 15, 0.55, BURIED, seam=True)

# === L0 (15x15 grand step 1: broad walkable ceremonial pediment) ==========
# smooth_stone walkable top; full perimeter stone_brick_stairs OUTWARD; chiseled corners.
S.box(0, 0, 0, 15, 15, 1, ANDE, seam=True)
for (cx, cz) in [(0, 0), (14, 0), (0, 14), (14, 14)]:    # chiseled corners
    S.box(cx, cz, 0, 1, 1, 1, CHIS)
for e in range(1, 14):                                   # outward perimeter skirt (grounded flare)
    S.box(e, -0.2, 0, 1, 0.6, 0.5, STAIR)                # N skirt
    S.box(e, 14.55, 0, 1, 0.6, 0.5, STAIR)               # S(front) skirt
    S.box(-0.2, e, 0, 0.6, 1, 0.5, STAIR)               # W skirt
    S.box(14.55, e, 0, 0.6, 1, 0.5, STAIR)              # E skirt

# === L1 (11x11 step 2: andesite platform + four corner SEA-LANTERN beacons) ===
# polished_andesite platform edged chiseled; four corner stone_brick_wall posts each crowned with a
# sea_lantern hooded by a stone_brick_slab above (four grand corner beacons). Inward stairs lift up.
S.box(2, 2, 1, 11, 11, 1, ANDE, seam=True)
for (cx, cz) in [(2, 2), (12, 2), (2, 12), (12, 12)]:    # chiseled edge ring corners
    S.box(cx, cz, 1, 1, 1, 1, CHIS)
# four corner beacons: wall-post neck -> sea_lantern -> hooded slab cap (grounded on the L1 corners)
corner_beacons = [(2, 2), (12, 2), (2, 12), (12, 12)]
for (bx, bz) in corner_beacons:
    S.box(bx + 0.2, bz + 0.2, 2, 0.6, 0.6, 1.4, STAIR)   # wall-post neck
    S.box(bx, bz, 3.4, 1, 1, 1, SEAL)                    # sea-lantern beacon
    S.box(bx, bz, 4.4, 1, 1, 0.5, SLATE)                 # hooded dark slab cap (flush -> sorts on top)
    S.box(bx + 0.15, bz + 0.15, 4.4, 1, 1, 0.4, SLATE)   # front eave lip (overhang read)

# === L2 (9x9 step 3: chiseled ring + two approach BANNERS) ================
# chiseled ring, smooth_stone centre; two stone_brick_wall posts on the approach (front) face each
# fly a banner (palette-tinted). Inward stairs lift again.
S.box(3, 3, 2, 9, 9, 1, PBASE, seam=True)
for (cx, cz) in [(3, 3), (11, 3), (3, 11), (11, 11)]:    # chiseled ring corners
    S.box(cx, cz, 2, 1, 1, 1, CHIS)
# inward cardinal stairs lifting to step 4
S.box(7, 3.2, 2, 1, 0.7, 0.5, STAIR)                     # N inward
S.box(7, 11.5, 2, 1, 0.7, 0.5, STAIR)                    # S(front) inward
S.box(3.2, 7, 2, 0.7, 1, 0.5, STAIR)                    # W inward
S.box(11.5, 7, 2, 0.7, 1, 0.5, STAIR)                   # E inward
# two approach banners on wall-posts, on the front (high-z) face of step 3, cloth facing the avenue
for bx in (5, 9):
    S.box(bx + 0.25, 11.25, 3, 0.5, 0.5, 1.6, POST)      # banner wall-post (front face)
    S.box(bx, 11.55, 3.4, 1, 0.35, 1.8, BANNER)          # banner cloth facing the approach

# === L3 (7x7 step 4: smooth-stone platform, chiseled border -> FOUR-tier plinth) ===
S.box(4, 4, 3, 7, 7, 1, PBASE, seam=True)
for (cx, cz) in [(4, 4), (10, 4), (4, 10), (10, 10)]:    # chiseled border corners
    S.box(cx, cz, 3, 1, 1, 1, CHIS)

# === L4 (3x3 shaft base / battered buttress) ==============================
# Battered buttress mass: four corners stone_brick_stairs leaning IN, four cardinal faces + centre
# chiseled. The buttress stairs rest on the L3 step (grounded) + lean <=0.3 toward the shaft.
S.box(6, 6, 4, 3, 3, 1, CHIS, seam=True)
for (bx, bz) in [(6, 6), (8, 6), (6, 8), (8, 8)]:
    lean_x = 0.28 if bx == 6 else -0.28
    lean_z = 0.28 if bz == 6 else -0.28
    S.box(bx + lean_x, bz + lean_z, 4, 1, 1, 0.85, STAIR)

# === L5..L8 (3x3 shaft lower, 4 courses, continuous FLUTE-SPINE) ==========
# thick lower shaft for viaduct-tower heft -- smooth_stone faces alternating with stone_bricks,
# the centre column of each face a continuous chiseled flute-spine, stone-brick corners.
for i, ly in enumerate((5, 6, 7, 8)):
    face = SMOOTH if i % 2 == 0 else BRICK               # L5/L7 smooth, L6/L8 brick
    S.box(6, 6, ly, 3, 3, 1, face, seam=True)            # 3x3 face mass
    S.box(7, 6, ly, 1, 3, 1, CHIS)                       # flute-spine column (N-S faces)
    S.box(6, 7, ly, 3, 1, 1, CHIS)                       # flute-spine column (E-W faces)
    for (cx, cz) in [(6, 6), (8, 6), (6, 8), (8, 8)]:    # stone-brick corners
        S.box(cx, cz, ly, 1, 1, 1, BAND)

# === L9 (5x5 corbel SHOULDER: shaft shoulders, then steps IN to 1x1) ======
S.box(5, 5, 9, 5, 5, 1, CHIS, seam=True)                 # chiseled 5x5 shoulder ring
for e in (5, 6, 7, 8, 9):
    S.box(e, 4.78, 9, 1, 0.7, 0.5, STAIR)                # N corbel
    S.box(e, 9.52, 9, 1, 0.7, 0.5, STAIR)                # S(front) corbel
    S.box(4.78, e, 9, 0.7, 1, 0.5, STAIR)               # W corbel
    S.box(9.52, e, 9, 0.7, 1, 0.5, STAIR)               # E corbel

# === L10..L22 (1x1 upper needle, 13 courses, deterministic %3 flute) ======
# clean tier -- NO cracked courses (great-road stays polished). k=0 at L10:
# k%3==0 -> chiseled flute (L10,13,16,19,22); k%3==1 -> smooth_stone; k%3==2 -> stone_bricks.
for k in range(13):
    ly = 10 + k
    if k % 3 == 0:
        col = CHIS
    elif k % 3 == 1:
        col = SMOOTH
    else:
        col = BRICK
    S.box(CX, CZ, ly, 1, 1, 1, col, seam=True)

# === L23 (1x1 -> 3x3 CROWN COLLAR, double-flared) =========================
# grandest collar -- chiseled centre, four stone_brick_stairs OUTWARD on the cardinal mid-edges,
# stone_brick_slab[type=top] corners reading as a double flare. >=3x3 support for the cap.
S.box(CX, CZ, 23, 1, 1, 1, CHIS)                         # collar centre (solid -> beacon core seats here)
for (cx, cz) in [(6, 6), (8, 6), (6, 8), (8, 8)]:        # top-slab corners (raised 0.5 -> double-flare read)
    S.box(cx, cz, 23.5, 1, 1, 0.5, PBASE)
S.box(7, 5.95, 23, 1, 0.8, 0.5, STAIR)                   # N outward corbel
S.box(7, 8.25, 23, 1, 0.8, 0.5, STAIR)                   # S(front) outward corbel
S.box(5.95, 7, 23, 0.8, 1, 0.5, STAIR)                  # W outward corbel
S.box(8.25, 7, 23, 0.8, 1, 0.5, STAIR)                  # E outward corbel

# === L24 (beacon-core lower: sea_lantern wrapped by slab seam) =============
S.box(CX, CZ, 24, 1, 1, 1, SEAL)                         # sea-lantern core 1
S.box(7, 6.05, 24.5, 1, 0.7, 0.5, PBASE)                 # N seam slab on the collar stair-top
S.box(7, 8.25, 24.5, 1, 0.7, 0.5, PBASE)                 # S seam slab
S.box(6.05, 7, 24.5, 0.7, 1, 0.5, PBASE)                # W seam slab
S.box(8.25, 7, 24.5, 0.7, 1, 0.5, PBASE)                # E seam slab

# === L25 (beacon-core upper: SECOND sea_lantern ringed by wall posts) ======
# a SECOND sea_lantern stacked on L24, ringed by four stone_brick_wall posts on the L23 collar
# corners that rise to here -- a 1x2 glowing core sheathed in masonry (glows through the seam).
S.box(CX, CZ, 25, 1, 1, 1, SEAL)                         # sea-lantern core 2 (taller 1x2 beacon stack)
for (cx, cz) in [(6, 6), (8, 6), (6, 8), (8, 8)]:        # wall posts ringing the upper core
    S.box(cx + 0.25, cz + 0.25, 25, 0.5, 0.5, 1, STAIR)

# === L26 (cap apex: chiseled block capping the core + end-rod finial) ======
S.box(CX, CZ, 26, 1, 1, 1, SLATE, seam=True)             # dark cap -> the spark + glow pop

# ============================ ATTENDANT MINI-OBELISKS ======================
# two 3x3 mini-obelisks on their OWN grounded sub-grade pads, flanking the approach (front) face,
# centred 6 out from main centre, pads just beyond the 15x15 plinth's front edge. Each echoes the
# central form in miniature (footing / chiseled foot / 1x1 shaft / 3x3 collar / capped tip + lantern).
attendant_origins = [(0.5, 15.5), (11.5, 15.5)]          # x-origin of each 3x3 pad, just past the front edge
for (ax, az) in attendant_origins:
    acx, acz = ax + 1, az + 1                            # the attendant's 1x1 shaft cell
    S.box(ax, az, -0.4, 3, 3, 0.45, BURIED)              # buried grounding pad
    S.box(ax, az, 0, 3, 3, 1, PBASE, seam=True)          # L0 3x3 footing
    for (dx, dz) in [(0, 0), (2, 0), (0, 2), (2, 2)]:    # outward stair skirt corners read
        S.box(ax + dx, az + dz, 0, 1, 1, 0.6, STAIR)
    S.box(acx, acz, 1, 1, 1, 1, CHIS)                    # L1 chiseled foot
    S.box(acx, acz, 2, 1, 1, 1, BRICK, seam=True)        # L2 shaft
    S.box(acx, acz, 3, 1, 1, 1, SMOOTH)                  # L3 shaft
    S.box(acx, acz, 4, 1, 1, 1, CHIS)                    # L4 shaft (flute)
    # L5 3x3 collar of outward stairs over a chiseled centre
    S.box(acx, acz, 5, 1, 1, 1, CHIS)
    S.box(acx, acz - 0.6, 5, 1, 0.7, 0.5, STAIR)         # N outward corbel
    S.box(acx, acz + 0.9, 5, 1, 0.7, 0.5, STAIR)         # S outward corbel
    S.box(acx - 0.6, acz, 5, 0.7, 1, 0.5, STAIR)        # W outward corbel
    S.box(acx + 0.9, acz, 5, 0.7, 1, 0.5, STAIR)        # E outward corbel
    S.box(acx, acz, 6, 1, 1, 1, CHIS, seam=True)         # L6 capped tip (carries a lantern)

# ============================ ACCENTS (lights / finials) ===================
# four corner sea-lantern beacons (glow between the lantern y3.4 and hood y4.4)
for (bx, bz) in corner_beacons:
    S.accent(bx + 0.5, bz + 0.5, 4.0, "glow", "#dff6ef", r=2.4)
# two warm banner-cloth highlights
for bx in (5, 9):
    S.accent(bx + 0.5, 11.6, 4.2, "dot", BANNER, r=1.6)
# the 1x2 beacon-core glow bleeding through the seam (between L24 and L25)
S.accent(CX + 0.5, CZ + 0.5, 25.0, "glow", "#dff6ef", r=3.2)
# end-rod finial spark at the very tip
S.accent(CX + 0.5, CZ + 0.5, 27, "finial")
# attendant lanterns + finials on each mini-obelisk tip
for (ax, az) in attendant_origins:
    S.accent(ax + 1.5, az + 1.5, 7.15, "glow", LANT, r=2.0)
    S.accent(ax + 1.5, az + 1.5, 7.0, "finial")

# ============================ CALLOUT LABELS ===============================
S.label(CX + 0.5, CZ + 0.5, 27, "1x2 sea-lantern beacon-core cap + end-rod apex spark")
S.label(CX + 0.5, CZ + 0.5, 23.4, "double-flared crown collar -- grounds the 1x2 beacon core")
S.label(CX + 0.5, CZ + 0.5, 15.0, "soaring tapered needle -- clean %3 flute (NO cracked courses)")
S.label(9.5, 7, 9.4, "flared 5x5 corbel shoulder over the 3x3 flute-spine lower shaft")
S.label(13, 12, 4.0, "four corner sea-lantern beacons (hooded by slabs)")
S.label(9, 11.5, 4.4, "approach banner pair (palette-tinted)")
S.label(13.5, 15.5, 6.2, "two GROUNDED attendant mini-obelisks (own pads, each lit)")
S.label(0, 14, 0.5, "FOUR-tier walkable ceremonial plinth (15->11->9->7)")

out = S.svg(title="Obelisk R4 (Great Road) -- capital monument: 4-tier ceremonial plinth, attendant mini-obelisks, corner beacons, banners, tapered needle, 1x2 beacon cap",
            size_label="15x15 plinth (+2 attendants) -> 3x3 base -> 1x1 needle * h27 * 9 lanterns (the capital-road monument, one step under the Forum Pillar)",
            label_w=392)
open("detail_svg/obelisk_great.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/obelisk_great.svg | bytes", len(out.encode()))
