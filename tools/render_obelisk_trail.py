"""Obelisk TRAIL (R1, floor of the obelisk ladder) -> detail_svg/obelisk_trail.svg.
Per deco_catalog_v2.json id 'obelisk' tier Trail (footprint 3x3 footing / 1x1 shaft, height 7,
L0..L6 visible): barely an obelisk -- a rough wayside menhir/boundary-stone cousin. One buried
grounding course, a shallow 3x3 cobble footing ring (0-4 mossy corners for age), a tiny single
INWARD-stair plinth ring, a 1x1 chiseled/brick/cracked shaft (3 courses), a real 3x3 OUTWARD-stair
COLLAR so the cap rests on >=3x3 (the critic's floating-stairs fix), and ONE blunt single-block
pyramidion tip. UNLIT -- the only dark tier; reads by silhouette in daylight alone.

This is the Trail rung of the same wnl_obelisk whose top tier is render_obelisk.py (the soaring
needle + four-sided pyramidion). MATCHED to the cairn lower-tier template (render_cairn_trail.py).
Inspiration (FORM/SCALE/TECHNIQUE only, credited in CREDITS.md, no assets/NBT/palette copied):
the medieval wayside-cross / boundary-menhir + Roman milestone (miliarium) tradition. Original WNL
geometry, vanilla blocks only.
ISO: road-facing FRONT = high-z (south) + high-x (east); the inward stairs read on that front."""
from iso_render import Iso

S = Iso(U=22)

# palette (literal) -- a WIDE-CONTRAST luminance ladder so every vanilla block reads as itself.
# This is the HUMBLE end of the obelisk family: cobblestone foot, plain/chiseled/cracked brick
# shaft, NO smooth-stone hero faces yet (those arrive at Highway+). Ladder dark->light:
# BURIED < FOOT < STAIR < MOSS < BRICK < CRACK < CHIS.
BURIED = "#5a5349"   # buried L-1 cobblestone grounding course (darkest -> sits IN the terrain)
FOOT   = "#8a8276"   # 3x3 cobblestone footing ring (the common grey foot mass)
STAIR  = "#6f685d"   # cobblestone_stairs plinth / collar darks (darker -> stepped read, shadowed)
MOSS   = "#6f7d56"   # mossy_cobblestone aged corners (the one green note; decay-hash picks 0-4)
BRICK  = "#a8a293"   # stone_bricks shaft course (mid)
CRACK  = "#9a8f7e"   # cracked_stone_bricks worn mid-shaft course (a touch warmer/greyer than BRICK)
CHIS   = "#c7c0b0"   # chiseled_stone_bricks shaft foot / flute / collar centre / cap (lightest -> carved read)

CX, CZ = 1, 1   # the 1x1 shaft cell sits in the centre of the 3x3 footing (origin 0..3)

# === BURIED L-1 (3x3 grounding course) ====================================
# One sub-grade cobblestone course, centre flush with terrain -- the only below-grade course;
# drawn sunk (sits half into the ground) so nothing the piece carries ever floats.
S.box(0, 0, -0.55, 3, 3, 0.6, BURIED, seam=True)

# === L0 (ground, 3x3 cobblestone footing ring) ============================
# Shallow footing ring; four corners swapped to mossy_cobblestone for age (decay-hash 0-4 mossy;
# drawn here as 3 mossy corners). Centre = chiseled shaft foot, flush with the ring.
S.box(0, 0, 0, 3, 3, 1, FOOT, seam=True)
for (cx, cz) in [(0, 0), (2, 0), (0, 2)]:          # 3 aged mossy corners (the 4th left clean)
    S.box(cx, cz, 0, 1, 1, 1, MOSS)
S.box(CX, CZ, 0, 1, 1, 1, CHIS)                    # chiseled centre = the shaft foot

# === L1 (3x3 plinth: tiny INWARD-stair foot) ==============================
# Four cobblestone_stairs facing INWARD on the cardinal mid-edges (each rests on the solid L0 ring
# below -- a real stepped foot, never floating); the four corners are full cobblestone blocks;
# centre is the chiseled shaft. This single inward-stair ring is the ONLY plinth a trail obelisk gets.
for (cx, cz) in [(0, 0), (2, 0), (0, 2), (2, 2)]:  # full-block corners
    S.box(cx, cz, 1, 1, 1, 1, FOOT)
# inward cardinal stairs: short, low, leaning toward the centre shaft (back/solid side to centre).
# modelled as a 0.55-tall stair body nudged <=0.25 toward the shaft -> grounded supported step.
S.box(1, 0.2, 1, 1, 0.8, 0.5, STAIR)               # NORTH (back) inward stair
S.box(1, 2.0, 1, 1, 0.8, 0.5, STAIR)               # SOUTH (front, road-facing) inward stair
S.box(0.2, 1, 1, 0.8, 1, 0.5, STAIR)               # WEST inward stair
S.box(2.0, 1, 1, 0.8, 1, 0.5, STAIR)               # EAST inward stair
S.box(CX, CZ, 1, 1, 1, 1, CHIS)                    # chiseled shaft rising through the ring

# === L2..L4 (1x1 shaft, 3 courses) ========================================
# A worn standing pillar: flute foot (chiseled), a plain brick course, a cracked worn mid-course.
S.box(CX, CZ, 2, 1, 1, 1, CHIS,  seam=True)        # L2 flute course (chiseled all 4 faces)
S.box(CX, CZ, 3, 1, 1, 1, BRICK, seam=True)        # L3 stone_bricks
S.box(CX, CZ, 4, 1, 1, 1, CRACK, seam=True)        # L4 cracked (worn mid-shaft; decay-hash note)

# === L5 (1x1 -> 3x3 COLLAR) ===============================================
# The required >=3x3 support beneath the apex (fixes the floating-stair cap). A grounded collar:
# chiseled centre, four stone_brick_stairs facing OUTWARD on the cardinal mid-edges (a tiny flared
# corbel resting on the L4 shaft + reaching out over the L1 ring corners below), cobblestone corners.
S.box(CX, CZ, 5, 1, 1, 1, CHIS)                    # collar centre (solid -> the cap seats on this)
for (cx, cz) in [(0, 0), (2, 0), (0, 2), (2, 2)]:  # cobblestone collar corners
    S.box(cx, cz, 5, 1, 1, 0.7, FOOT)
# outward cardinal corbel stairs: low, nudged <=0.25 OUT, back/solid side bearing on the collar centre.
S.box(1, -0.05, 5, 1, 0.8, 0.5, STAIR)             # NORTH outward corbel
S.box(1, 2.25, 5, 1, 0.8, 0.5, STAIR)              # SOUTH (front) outward corbel
S.box(-0.05, 1, 5, 0.8, 1, 0.5, STAIR)            # WEST outward corbel
S.box(2.25, 1, 5, 0.8, 1, 0.5, STAIR)             # EAST outward corbel

# === L6 (cap apex: ONE blunt pyramidion block over the collar centre) =====
# A single chiseled_stone_bricks block as a blunt pyramidion tip -- NO four-stairs-over-thin-air.
# Reads as a capped standing stone. No light (deliberately the only dark tier).
S.box(CX, CZ, 6, 1, 1, 1, CHIS, seam=True)

S.label(CX + 0.5, CZ + 0.5, 7.1, "blunt single-block pyramidion tip (no floating stairs) -- UNLIT")
S.label(2.3, CZ + 0.5, 5.6, "real 3x3 collar -- outward corbel stairs support the cap")
S.label(CX + 0.5, CZ + 0.5, 3.6, "1x1 worn shaft (chiseled / brick / cracked courses)")
S.label(2.3, 1, 1.4, "tiny inward-stair plinth foot (the only plinth a trail gets)")
S.label(0, 2, 0.4, "3x3 cobble footing ring -- 0-4 mossy corners for age")
S.label(2.3, 2.6, -0.3, "buried grounding course (centre flush -> never floats)")

out = S.svg(title="Obelisk R1 (Trail) -- rough wayside menhir/boundary-stone: 3x3 cobble foot, 1x1 worn shaft, blunt capped tip, UNLIT",
            size_label="3x3 foot / 1x1 shaft * h7 * 0 lanterns (ladder floor -- a boundary-stone cousin, reads by silhouette)",
            label_w=352)
open("detail_svg/obelisk_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/obelisk_trail.svg | bytes", len(out.encode()))
