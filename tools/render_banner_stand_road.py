"""Banner_stand ROAD -> detail_svg/banner_stand_road.svg.
Per deco_catalog_v2.json id 'banner_stand' tier Road (footprint 7x3, height 9): the first tier that
SPANS the road -- TWIN 2-wide dressed-stone PIERS the ~5-wide road passes BETWEEN, each pier flying a
3-block inward white-wall-banner column (6 banners, paired claim-curtains facing each other across the
threshold), tied together by a REAL timber LINTEL (dark_oak_log header on dark_oak_fence drop-brackets)
with a dark-oak slab brow and ONE hung lantern at the threshold centre. The silhouette FLIPS from
beside-the-road (Path) to ACROSS-the-road -- the first true 'entering somewhere' gate.

NON-LINEAR ESCALATION over Path (engineered big since Trail is skipped): one beside-road pole -> two
flanking 2-wide stone PIERS; oak fence -> cut stone_bricks masonry; +4 height (5->9); a single standing
banner -> six stacked WALL banners; the Path's gated chain -> a STRUCTURAL timber lintel the road clears
(>=4 air under it). Still well below the Highway leap -- the curve keeps accelerating.

ISO: road-facing detail (dressed chiseled front, banner-curtains) on the HIGH-z FRONT + HIGH-x sides so
the viewer reads it. Both piers + the banners + the lintel face the avenue between them (toward viewer).

Originality/inspiration (FORM/TECHNIQUE only, credited CREDITS.md; no NBT/assets copied): medieval
town-gate threshold + Roman flanking gateposts -- the road-passes-between-dressed-piers civic gesture.
Same wnl_banner_stand builder as render_banner_stand.py (Great Road top); dye/decay/lantern hashed live."""
from iso_render import Iso

S = Iso(U=17)

# ---- palette (literal) -- WIDE-CONTRAST ladder; each masonry role steps light->dark so it reads ----
SBRICK = "#8e8a80"   # minecraft:stone_bricks pier core (cool dressed grey -- the body)
CHIS   = "#c7b487"   # minecraft:chiseled_stone_bricks -- dressed front face + banded ring (warm sand, hard contrast)
MOSS   = "#6f7d56"   # minecraft:mossy_stone_bricks weathering swap (saturated green, distance-lerped)
KERB   = "#6f6b62"   # stone_brick_slab outer kerb lip (darker -> reads the stepped dressed lip)
CAP    = "#a7a297"   # stone_brick_slab[type=top] pier cap (lighter -> the cap pops off the body)
TIMBER = "#5a4226"   # dark_oak_log lintel header (warm mid timber, axis=x)
TIMDK  = "#46341e"   # dark_oak_fence drop-bracket + brow shadow (darker timber -> reads the bracket joint)
BROW   = "#33240f"   # dark_oak_slab brow over the lintel (DARKEST -> caps the silhouette clean)
BANNER = "#b14a3f"   # white_wall_banner recolored at placement -- muted heraldic claim red (column, inward)
BANEDGE= "#d8d2c4"   # pale banner border/staff edge so each hanging reads as cloth
CHAIN  = "#54504a"   # chain carrying the threshold lantern (or bare unlit when remote)
LANT   = "#ffd47a"   # lantern glow (standard light from Road up)

# geometry: 7 wide (x0..7), 3 deep (z0..3, z0=back/z3=front). Two 2-wide piers: WEST x0-2, EAST x5-7.
# The ~3-wide threshold/road runs BETWEEN them (x2..5) -- the road passes through the gap (>= road width).
WP = 0      # west pier x-origin (2 wide)
EP = 5      # east pier x-origin (2 wide)
ZB = 0      # pier back plane
ZF = 2      # pier front depth (piers are 2 deep, z0..2); cloth hangs proud at z>=2
ZCLOTH = 2.05  # inward banner-curtains hang JUST proud of the pier front face -> always paint OVER the body

# ============================================================================================
# THE GROUND -- a faint road strip running through the threshold (reads the road passing BETWEEN)
# ============================================================================================
S.box(2,0,0, 3,3,0.18, "#9b8a63")   # warm packed road strip in the gap (flush, low -> the avenue floor)

# ============================================================================================
# TWIN 2x2 PIER FOOTINGS (L0) -- stone_bricks, chiseled dressed front-inner block, slab kerb + moss
# ============================================================================================
def pier_footing(x0, inner_x):
    # 2x2 footing (2 along road x 2 deep)
    S.box(x0,0,0, 2,2,1, SBRICK, seam=True)
    # front-INNER block dressed in chiseled (the face the traveller meets first, high-z front)
    S.box(inner_x,2-1,0, 1,1,1, CHIS)              # front-inner cell (z1 row, the inner column)
    # one mossy weathering block (distance-lerped tell)
    S.box(x0,0,0, 1,1,1, MOSS)                      # back-outer cell mossy
    # outer kerb lip: stone_brick_slab wraps the OUTWARD side
    outer = x0 if inner_x != x0 else x0+1
    S.box(outer,-0.26,1, 1,0.26,0.4, KERB)          # outer kerb (back face here reads as the stepped lip)

pier_footing(WP, WP+1)   # west pier: inner column is its EAST cell (x1)
pier_footing(EP, EP)     # east pier: inner column is its WEST cell (x5)

# ============================================================================================
# THE TWO PIERS (L1-L5) -- SOLID 2-wide x 1-deep masonry, banded chiseled ring at y3
# (2-wide base = real piers, not fence posts). Front depth z1..2 so the inner face shows.
# ============================================================================================
def pier_body(x0):
    z0 = 1                                          # piers sit forward (z1..2) so inner face reads
    S.box(x0,z0,1, 2,1,2, SBRICK, seam=True)        # y1-2 core
    S.box(x0,z0,3, 2,1,1, CHIS)                      # y3 banded chiseled ring (dressed)
    S.box(x0,z0,4, 2,1,2, SBRICK, seam=True)        # y4-5 upper core
    # cap (L8 caps at y8, but pier core needs to reach the lintel at y6) -> carry core to y7
    S.box(x0,z0,6, 2,1,1, SBRICK, seam=True)        # y6 head course (lintel ties in here)
    S.box(x0,z0,7, 2,1,1, SBRICK, seam=True)        # y7 (under cap)
    S.box(x0-0.1,z0-0.1,8, 2.2,1.2,0.45, CAP)       # y8 proud slab cap (overhangs -> reads a cap)

pier_body(WP)
pier_body(EP)

# ============================================================================================
# BANNER-CURTAINS -- each pier flies a 3-block white_wall_banner column on its INNER face (y4,5,6),
# both facing INWARD toward the threshold (toward each other / the viewer). 3 per side = 6 total.
# Hung proud of the inner face so the cloth always paints OVER the pier body.
# ============================================================================================
def banner_column(inner_x):
    for y in (4,5,6):                               # 3 stacked 1-block wall banners
        S.box(inner_x+0.12, ZCLOTH, y, 0.76, 0.3, 1, BANNER)
    S.box(inner_x+0.06, ZCLOTH+0.02, 4, 0.1, 0.26, 3, BANEDGE)  # pale staff edge down the column

banner_column(WP+1)     # west pier inner face = its east column (x1)
banner_column(EP)       # east pier inner face = its west column (x5)

# ============================================================================================
# THE LINTEL (L6-L7) -- a REAL timber header crossing pier-to-pier across the threshold at y7,
# with dark_oak_fence drop-brackets tying into the pier tops at y6. Underside >=4 over the road deck.
# ============================================================================================
# drop-brackets first (at each pier top inner corner, y6), then the header beam across
S.box(WP+1.7,1.1,6, 0.3,0.8,1, TIMDK)               # west drop-bracket (dark_oak_fence into pier top)
S.box(EP+0.0,1.1,6, 0.3,0.8,1, TIMDK)               # east drop-bracket
S.box(WP+1.5,1.0,7, (EP+0.5)-(WP+1.5), 0.9,1, TIMBER, seam=True)  # dark_oak_log header spans the threshold

# ============================================================================================
# THE BROW (L8) -- a thin dark_oak_slab capping course over the lintel as a shelter brow
# ============================================================================================
S.box(WP+1.4,0.9,8, (EP+0.6)-(WP+1.4), 1.1,0.45, BROW)  # dark-oak slab brow (caps the silhouette)

# ============================================================================================
# LIGHT (L8) -- ONE lantern hangs on a chain from the lintel centre at the threshold (CivLevel-gated;
# bare unlit chain when remote). GROUNDED: chain abuts the lintel underside; lantern hangs under it.
# ============================================================================================
CTR = (WP+2 + EP) / 2.0                              # threshold centre x
S.box(CTR-0.05,1.3,6.0, 0.1,0.1,1.0, CHAIN)          # chain from the lintel underside (abuts the header)
S.accent(CTR, 1.4, 5.7, "glow", LANT, r=2.5)         # threshold lantern under the chain

# ============================================================================================
# CALLOUT LABELS
# ============================================================================================
S.label(CTR, 1.4, 7.6, "REAL dark_oak_log LINTEL on fence drop-brackets + dark-oak slab brow (>=4 clear)")
S.label(WP+1.1, ZCLOTH, 5.4, "paired 3-block inward banner-curtains (6 white_wall_banners facing the threshold)")
S.label(CTR, 1.4, 5.5, "ONE threshold lantern slung at the lintel centre (standard light from Road up)")
S.label(EP+1, 1, 1.0, "twin 2-wide dressed stone_brick PIERS -- the road passes BETWEEN them")
S.label(WP, 0.4, 0.5, "stone_brick footings: chiseled dressed front, mossy weather block, slab kerb lip")

out = S.svg(title="Banner_stand R-Road -- twin-pier gate the road passes BETWEEN: 6 banner-curtains + real timber lintel + first standard light",
            size_label="7x3 (twin 2-wide piers) * h9 * 1 lantern (first tier that SPANS the road -- a true 'entering somewhere' gate)",
            label_w=358)
open("detail_svg/banner_stand_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/banner_stand_road.svg | bytes", len(out.encode()))
