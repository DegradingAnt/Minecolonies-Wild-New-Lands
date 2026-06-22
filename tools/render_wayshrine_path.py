"""Wayshrine PATH (R2) -> detail_svg/wayshrine_path.svg.
Per deco_catalog_v2.json id 'wayshrine' tier Path (footprint 4x4 = niche + 1-block forecourt
threshold, height 5): a MODEST jump from Trail -- raw cobble becomes DRESSED stone_bricks, the niche
deepens to a 1-wide x 2-tall flat recess against a chiseled_stone_bricks centre stripe, a true
PILASTER pair (stone_brick_wall posts capped with chiseled brick) brackets it, a hung lantern over
a 2-candle ledge replaces the bare candle, and a continuous peaked GABLE CORNICE caps the front.
It now has a THRESHOLD you step onto. Still single-wall, no enclosed room -- the architecture proper
begins at Road (non-linear ladder: Trail/Path humble, the big leaps saved for Road/Highway).

Same wnl_wayshrine data builder as render_wayshrine.py (Great Road top); cracked-brick + moss are
distance_decay-gated weathering picks. ISO: niche opens on the FRONT (max-z) face toward the viewer.
Originality/inspiration: the European wayside aedicula FORM, technique only -- credited in CREDITS.md."""
from iso_render import Iso

S = Iso(U=22, occlusion=True)

# ---- palette (literal) -- a clear luminance ladder so dressed stone reads distinct from cobble-tier.
#      dark->light: NICHE < STEP < SB < MSB < WALLP < CHIS < LEDGE.
SB    = "#8f897c"   # stone_bricks (the dressed field block -- the whole shift up from cobble)
MSB   = "#79805e"   # mossy_stone_bricks scatter (light moss, distance_decay note)
CRACK = "#857d6e"   # cracked_stone_bricks (the odd weathering brick for character)
CHIS  = "#c2bca8"   # chiseled_stone_bricks (light dressed accent: centre stripe, pilaster caps, keystone)
WALLP = "#a7a08e"   # stone_brick_wall pilaster posts (proto-pillars, a touch proud + light)
LEDGE = "#b8b2a4"   # stone_brick_slab ledge + threshold step (lightest walkable dressed stone)
NICHE = "#46423a"   # recessed nook interior (deep shadow -> the 1x2 recess reads cut-IN)
STEP  = "#7d7768"   # forecourt threshold slab row (a touch darker -> the step reads as entered)
LANT  = "#caa15a"   # hung-lantern body (warm metal, sits under the solid nook ceiling)

# =====================================================================================
# 1) BASE (4x4, y0): stone_bricks pad + mossy scatter; FRONT row = slab threshold step so the
#    shrine reads as ENTERED, not passed. The forecourt cell the traveller stands on.
# =====================================================================================
S.box(0, 0, 0, 4, 4, 1, SB, seam=True)               # stone_bricks pad 4x4
S.box(1, 1, 0, 1, 1, 1, MSB)                         # mossy_stone_bricks scatter (hand-laid read)
S.box(0, 3, 1, 4, 1, 0.3, LEDGE)                     # FRONT-row stone_brick_slab threshold step (proud, you step onto it)
S.box(1, 2.0, 1, 2, 1, 0.15, STEP)                   # worn forecourt cell behind the threshold (the place you stand)

# =====================================================================================
# 2) BACK WALL (3 wide x 4 tall, y1..4) DRESSED: stone_bricks field with a vertical chiseled
#    centre STRIPE behind the niche (the first sign of craft). Back row at z=0 (BACK).
# =====================================================================================
S.box(0, 0, 1, 3, 1, 4, SB, seam=True)               # stone_bricks back-wall field (4 tall)
S.box(1, 0, 1, 1, 1, 4, CHIS)                        # chiseled_stone_bricks vertical centre stripe (full height)
S.box(0, 0, 3, 1, 1, 1, CRACK)                       # 1 cracked-brick character note (lower-left)
S.box(2, 0, 4, 1, 1, 1, MSB)                         # light mossy scatter (upper-right)

# =====================================================================================
# 3) THE NICHE -- 1-wide x 2-tall flat-topped recess (deeper than Trail, still NOT arched);
#    floor = slab ledge; nook back = the chiseled stripe so the flame sits against carved stone.
# =====================================================================================
S.box(1, 0.55, 1, 1, 0.45, 2, NICHE)                 # recessed shadow cavity (1x2, cut into the chiseled stripe)
S.box(1, 0.5, 1, 1, 0.5, 0.3, LEDGE)                 # stone_brick_slab offering ledge (candles stand on this)
S.box(1, 0.5, 3, 1, 0.5, 0.25, SB)                   # solid nook-ceiling block (the lantern hangs UNDER this -- supported)

# =====================================================================================
# 4) FLANKING PILASTERS -- the two columns either side of the nook step OUT half a block as
#    stone_brick_wall posts, each capped with a chiseled_stone_bricks block: a proto-pillar pair.
#    Grounded vertical stacks rising off the base, proud of the wall plane (z forward to ~ -0.4).
# =====================================================================================
def pilaster(px):
    S.box(px, -0.35, 1, 0.7, 0.7, 3, WALLP, seam=True)   # stone_brick_wall shaft (proud of the wall, 3 tall)
    S.box(px-0.1, -0.45, 4, 0.9, 0.9, 0.6, CHIS)         # chiseled_stone_bricks cap (proud -> reads as a capital)
pilaster(0.15)                                            # left pilaster (x0 column)
pilaster(2.15)                                            # right pilaster (x2 column)

# =====================================================================================
# 5) GABLE CORNICE (y5): a continuous peaked hood across the 3-wide front -- stone_brick_stairs
#    left + mirrored right rising to a centre chiseled keystone-RIDGE. Each stair rests on the
#    wall/pilaster-cap course beneath it (grounded). A touch of moss in the cornice.
# =====================================================================================
S.box(0, -0.1, 4.6, 1, 1.0, 0.5, SB)                 # left stair half (rises toward centre, on the wall top)
S.box(2, -0.1, 4.6, 1, 1.0, 0.5, SB)                 # right stair half (mirrored)
S.box(1, -0.1, 5.1, 1, 1.0, 0.5, CHIS)              # chiseled keystone-ridge (the centre peak, brightest)
S.box(0.4, -0.1, 4.6, 0.3, 1.0, 0.4, MSB)           # a mossy cornice block for character (grounded on the eave)

# =====================================================================================
# ACCENTS -- a real fixture now: a HUNG lantern off the solid nook ceiling + 2 candles on the ledge.
# =====================================================================================
# the hung lantern body, modelled as a small box under the solid ceiling block (supported above)
S.box(1.3, 0.62, 2.3, 0.4, 0.35, 0.55, LANT)         # hanging-lantern fixture (hangs UNDER the nook ceiling)
S.accent(1.5, 0.6, 2.55, "glow", "#ffd47a", r=2.0)   # lantern glow (the hung fixture lit)
S.accent(1.5, 0.55, 1.45, "glow", "#ffe6a8", r=1.6)  # 2-candle row glow on the ledge (warm, lower)

S.label(1.5, 0.0, 5.2, "peaked gable cornice + chiseled keystone-ridge")
S.label(2.2, -0.45, 4.3, "true pilaster pair: stone_brick_wall + chiseled cap")
S.label(1.5, 0.6, 2.5, "hung lantern over a 2-candle ledge (a real fixture)")
S.label(1.0, 0.0, 1.6, "chiseled centre stripe -- first sign of craft")
S.label(0, 3, 1.3, "stone_brick_slab threshold step -- you step ONTO it")

out = S.svg(title="Wayshrine R2 (Path) -- dressed-stone niche: chiseled stripe, pilaster pair, hung lantern, gable cornice",
            size_label="4x4 foot * h5 * 1 lantern + 2 candles (a tended footpath shrine you step onto)",
            label_w=336)
open("detail_svg/wayshrine_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/wayshrine_path.svg | bytes", len(out.encode()))
