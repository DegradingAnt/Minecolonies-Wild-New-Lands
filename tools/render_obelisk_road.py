"""Obelisk ROAD (R2) -> detail_svg/obelisk_road.svg.
Per deco_catalog_v2.json id 'obelisk' tier Road (footprint 5x5 plinth / 1x1 shaft, height 11,
L0..L10 visible): the first version that reads UNMISTAKABLY as a civic obelisk. A modest-but-real
jump off Trail -- footprint 3x3->5x5, height 7->11, gains a genuine TWO-tier stepped plinth, the
FIRST flanking-lantern pair-of-pairs (4 grounded lights on stone_brick_wall posts -- the new
Road-vs-Trail distinction so the rung is not merely linear), an alternating chiseled/plain flute
shaft on a deterministic %3 map, a flared 3x3 corbel collar, and the FIRST LIT CAP (a single
lantern finial on the solid apex). Still roadside-scaled + subordinate to the Highway leap.

Same wnl_obelisk whose top tier is render_obelisk.py. MATCHED to render_cairn_road.py craft.
Inspiration (FORM/SCALE/TECHNIQUE only, credited in CREDITS.md, no assets/NBT/palette copied):
Roman milestone (miliarium) + medieval wayside-cross. Original WNL geometry, vanilla blocks only.
ISO: road-facing FRONT = high-z (south) + high-x (east)."""
from iso_render import Iso

S = Iso(U=18)

# palette (literal) -- WIDE-CONTRAST luminance ladder, every vanilla block reads as itself.
# Road steps UP from Trail's cobble foot to a dressed stone-brick plinth; smooth-stone hero faces
# are still withheld (those arrive Highway+). Ladder dark->light:
# BURIED < STAIR < PBASE < MOSS < CRACK < BRICK < CHIS ; LANT separated by hue.
BURIED = "#5a5349"   # buried L-1 stone_bricks grounding course (darkest -> sits IN terrain)
STAIR  = "#6f685d"   # stone_brick_stairs skirt / wall-posts / collar darks (shadowed stepped read)
PBASE  = "#8c8579"   # stone_bricks plinth platform mass (mid grey -- the base body)
MOSS   = "#6f7d56"   # mossy_stone_bricks dappled accent (the one green note; outer-ring age)
CRACK  = "#9a8f7e"   # cracked_stone_bricks remote-swap accent course (warm-grey worn note)
BRICK  = "#aaa493"   # stone_bricks shaft course (lighter than the plinth mass -> shaft pops)
CHIS   = "#c9c2b2"   # chiseled_stone_bricks flute / corners / collar centre / cap (lightest -> carved)
LANT   = "#ffd47a"   # lantern glow (FIRST lit tier -- warm, separated from the cool stone by hue)

# Shaft cell = the 1x1 at the centre of the 5x5 plinth (origin 0..5 -> centre cell at x=2,z=2).
CX, CZ = 2, 2

# === BURIED L-1 (5x5 grounding course) ====================================
# Sub-grade stone_bricks, outer ring dappled mossy -> grounds the whole piece. Drawn sunk.
S.box(0, 0, -0.55, 5, 5, 0.6, BURIED, seam=True)

# === L0 (5x5 plinth base: outward stair skirt that flares to the ground) ===
# Solid stone_bricks platform; the 12 outer-edge blocks carry stone_brick_stairs facing OUTWARD
# (a skirt flaring to grade); corners chiseled full blocks. Each skirt stair rests on the solid
# L0 ring and is nudged <=0.25 OUT -> grounded flare, never floating.
S.box(0, 0, 0, 5, 5, 1, PBASE, seam=True)
for (cx, cz) in [(0, 0), (4, 0), (0, 4), (4, 4)]:        # chiseled corners
    S.box(cx, cz, 0, 1, 1, 1, CHIS)
# outward skirt stairs on the four edges (low 0.5 stair body, nudged out to read as a flare)
for ex in (1, 2, 3):
    S.box(ex, -0.22, 0, 1, 0.7, 0.5, STAIR)             # NORTH (back) skirt
    S.box(ex, 4.52, 0, 1, 0.7, 0.5, STAIR)              # SOUTH (front) skirt
for ez in (1, 2, 3):
    S.box(-0.22, ez, 0, 0.7, 1, 0.5, STAIR)            # WEST skirt
    S.box(4.52, ez, 0, 0.7, 1, 0.5, STAIR)             # EAST skirt
# one outer mossy dapple (age) tucked on the front skirt -- abuts the front edge, grounded
S.box(3, 4.55, 0, 1, 0.45, 0.4, MOSS)

# === L1 (5x5 ring + four cardinal WALL-POST necks carrying the first lanterns) ===
# stone_bricks ring; the four cardinal mid-edges carry short stone_brick_wall posts, each crowned
# at L2 height by a lantern -- the FIRST flanking lights (4 grounded), the Road-vs-Trail distinction.
S.box(0, 0, 1, 5, 5, 1, PBASE, seam=True)
S.box(1, 1, 1, 3, 3, 1, PBASE)                          # solid centre 3x3 (the shaft seat below)
# four wall-post necks on the cardinal mid-edges (rise from the solid L1 ring -> grounded)
wall_posts = [(2, 0), (2, 4), (0, 2), (4, 2)]           # N, S(front), W, E mid-edges
for (px, pz) in wall_posts:
    S.box(px + 0.25, pz + 0.25, 1, 0.5, 0.5, 1.4, STAIR)  # slender wall-post neck (1.4 tall)

# === L2 (3x3 second step: INWARD stairs lift to the shaft) =================
# stone_bricks ring with the four cardinal mid-edges as stone_brick_stairs facing INWARD (stepping
# up to the shaft); chiseled centre. A genuine two-tier stepped plinth. The 4 lanterns sit here,
# flanking the shaft foot (seated on the L1 wall-post tops -> grounded lights).
S.box(1, 1, 2, 3, 3, 1, PBASE, seam=True)
for (cx, cz) in [(1, 1), (3, 1), (1, 3), (3, 3)]:       # chiseled step corners
    S.box(cx, cz, 2, 1, 1, 1, CHIS)
# inward cardinal stairs stepping up toward the shaft (back/solid side to centre, nudged <=0.25 in)
S.box(2, 1.2, 2, 1, 0.8, 0.5, STAIR)                    # N inward
S.box(2, 2.0, 2, 1, 0.8, 0.5, STAIR)                    # S(front) inward
S.box(1.2, 2, 2, 0.8, 1, 0.5, STAIR)                    # W inward
S.box(2.0, 2, 2, 0.8, 1, 0.5, STAIR)                    # E inward
S.box(CX, CZ, 2, 1, 1, 1, CHIS)                         # chiseled shaft foot at centre

# === L3..L8 (1x1 shaft, 6 courses, deterministic %3 flute map) ============
# flute courses (chiseled) fall where course_index %3 == 0; else plain stone_bricks. One remote
# course shown cracked per the decay-hash note. Light shaft brick pops off the darker plinth.
# course_index 0 at L3: L3 chiseled, L4 brick, L5 brick, L6 chiseled(%3==0 -> idx3), L7 brick, L8 brick.
shaft_map = {3: CHIS, 4: BRICK, 5: BRICK, 6: CHIS, 7: CRACK, 8: BRICK}  # L7 = the remote cracked course
for ly, col in shaft_map.items():
    S.box(CX, CZ, ly, 1, 1, 1, col, seam=True)

# === L9 (1x1 -> 3x3 COLLAR: flared corbel crown) ==========================
# Grounded crown collar -- chiseled centre, four stone_brick_stairs facing OUTWARD on the cardinal
# mid-edges (a flared corbel reaching over the shaft), stone_brick_slab corners. >=3x3 support.
S.box(CX, CZ, 9, 1, 1, 1, CHIS)                         # collar centre (solid -> the cap seats here)
for (cx, cz) in [(1, 1), (3, 1), (1, 3), (3, 3)]:       # slab corners (bottom slabs, 0.5 tall)
    S.box(cx, cz, 9, 1, 1, 0.5, PBASE)
# outward corbel stairs, low, nudged <=0.25 OUT, back/solid side bearing on the collar centre
S.box(2, 0.95, 9, 1, 0.8, 0.5, STAIR)                   # N outward corbel
S.box(2, 3.25, 9, 1, 0.8, 0.5, STAIR)                   # S(front) outward corbel
S.box(0.95, 2, 9, 0.8, 1, 0.5, STAIR)                  # W outward corbel
S.box(3.25, 2, 9, 0.8, 1, 0.5, STAIR)                  # E outward corbel

# === L10 (cap apex: ONE chiseled block + a single lantern finial) =========
# The FIRST lit cap on the ladder: one chiseled_stone_bricks block carrying a single lantern seated
# on its top face -- a modest finial light, resting on solid masonry, never floating.
S.box(CX, CZ, 10, 1, 1, 1, CHIS, seam=True)

# ============================ ACCENTS (lights) ============================
# four flanking lanterns on the L1 wall-post tops (y ~2.4, flanking the shaft foot)
for (px, pz) in wall_posts:
    S.accent(px + 0.5, pz + 0.5, 2.5, "glow", LANT, r=2.0)
# the single cap finial lantern, seated on the L10 apex top face
S.accent(CX + 0.5, CZ + 0.5, 11.15, "glow", LANT, r=2.2)

S.label(CX + 0.5, CZ + 0.5, 11.2, "FIRST lit cap -- single lantern finial on the solid apex")
S.label(CX + 0.5, CZ + 0.5, 9.6, "flared 3x3 corbel collar -- supports the pyramidion cap")
S.label(CX + 0.5, CZ + 0.5, 6.0, "1x1 flute shaft -- chiseled / plain on a %3 map (one cracked course)")
S.label(4, 2, 2.5, "FIRST flanking lanterns -- 4 on stone-brick wall posts (the Road distinction)")
S.label(2, 4, 2.4, "two-tier stepped plinth -- inward stairs lift to the shaft")
S.label(0, 4, 0.5, "5x5 plinth base -- outward stair skirt flares to the ground")

out = S.svg(title="Obelisk R2 (Road) -- first true civic obelisk: 2-tier plinth, 4 flanking lanterns, flute shaft, lit pyramidion cap",
            size_label="5x5 plinth / 1x1 shaft * h11 * 5 lanterns (the road's first proper civic obelisk)",
            label_w=372)
open("detail_svg/obelisk_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/obelisk_road.svg | bytes", len(out.encode()))
