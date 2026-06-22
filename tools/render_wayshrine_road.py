"""Wayshrine ROAD (R3) -> detail_svg/wayshrine_road.svg.
Per deco_catalog_v2.json id 'wayshrine' tier Road (footprint 5x5, height 7): the BIG identity jump
of the ladder -- the flat niche becomes ARCHITECTURE. A two-course stepped plinth lifts a real
3-SIDED ALCOVE (a room you stand inside out of the rain); the niche WIDENS to 3-wide x 3-tall with
an explicit corbel ARCH + chiseled keystone; a free-standing front PILLAR PAIR frames the open
front; a chain lantern hangs from a SOLID chiseled crossbeam set block-to-block between the pillar
tops (supported at both ends, NOT a wall lintel); a 3-candle ledge + a soul-lantern give cool/warm
contrast; and -- the headline -- the FIRST ROOFED tier: a peaked gable over the 5x5 with a filled
stone-bricks tympanum, eaves overhanging the pillars.

Non-linear ladder: footprint near-doubles (4x4 -> 5x5), gains a roof + a true third dimension.
Same wnl_wayshrine data builder as render_wayshrine.py (Great Road top). ISO: the open front +
arched niche face the viewer on the FRONT (max-z). Build technique per spec: arch = two top-half
corner stairs meeting a centre keystone resting on the wall course above; beam = a SOLID block run.
Originality/inspiration: wayside aedicula + lantern-house FORM, technique only -- credited CREDITS.md."""
from iso_render import Iso

S = Iso(U=15)

# ---- palette (literal) -- a WIDE-contrast ladder so the alcove WALL reads dark, the pillars +
#      arch frame read light, and the slate roof reads darkest. dark->light:
#      ROOF < WALL < NICHE < AND < SB < PILLAR < CHIS < LEDGE < KEY.  (+ green moss, warm lights.)
SB     = "#8c867a"   # stone_bricks (the dressed field / pad / tympanum)
WALL   = "#766f60"   # alcove side+back walls (DARKER warm stone -> the pale pillars + arch pop off it)
AND    = "#83868b"   # polished_andesite inset plinth course (cool -> separates the two base courses)
MOSS   = "#727f57"   # mossy_cobblestone / mossy scatter (moss up the shaded wall)
CRACK  = "#827a6b"   # cracked_stone_bricks (occasional weathering scatter)
PILLAR = "#cdc7b8"   # free-standing front pillars + pillar shafts (light dressed stone, the frame)
CHIS   = "#c2bca8"   # chiseled_stone_bricks (arch keystone, pillar caps, crossbeam, back panel)
KEY    = "#ece5d0"   # brightest dressed accent (keystone crown, ridge cap)
LEDGE  = "#b8b2a4"   # smooth_stone_slab offering ledge (light walkable stone)
NICHE  = "#46423a"   # recessed arched-niche interior (deep shadow -> the recess reads cut-IN)
ROOF   = "#5a5550"   # stone-brick gable roof field (darkest mass -> strong contrast vs pale pillars)
ROOFR  = "#6d675f"   # roof ridge / upper course (lighter -> the pitch reads stepped)
LANT   = "#caa15a"   # hung-lantern body (warm metal)
SOUL   = "#5fb8c4"   # soul-lantern accent (cool teal -> the cool/warm contrast the spec calls for)
STEP   = "#a7a08e"   # front ascending step (stone_brick_stairs notch)
VINE   = "#5a6e3c"   # vine off an eave-end solid face (distance_decay note)

# =====================================================================================
# 1) STEPPED PLINTH (5x5, y0..1): two courses -- outer stone_bricks ring (5x5) + inset polished-
#    andesite top course (3x3) -> the shrine stands ON something. Front-centre ascending step.
# =====================================================================================
S.box(0, 0, 0, 5, 5, 1, SB, seam=True)               # course 1: stone_bricks 5x5 outer ring
S.box(1, 1, 1, 3, 3, 1, AND)                         # course 2: polished_andesite 3x3 inset (the floor the alcove sits on)
S.box(2, 4, 1, 1, 1, 0.5, STEP)                      # front-centre stone_brick_stairs ascending step (notch, you climb)

# =====================================================================================
# 2) 3-SIDED ALCOVE (y2..5): back wall (z0) + two SIDE walls (x0, x4) = a real room you stand in
#    out of the rain. Dark dressed stone with mossy + cracked scatter. Open on the FRONT (viewer).
# =====================================================================================
S.box(1, 0, 2, 3, 1, 4, WALL, seam=True)             # back wall (3 wide x 4 tall, z=0 BACK)
S.box(1, 0, 2, 1, 3, 4, WALL, seam=True)             # left side wall (x1, runs z0..3 toward the front)
S.box(3, 0, 2, 1, 3, 4, WALL, seam=True)             # right side wall (x3)
S.box(1, 0, 2, 1, 1, 1, MOSS)                        # moss up the shaded back-left corner
S.box(3, 0, 4, 1, 1, 1, CRACK)                       # a cracked-brick weathering note (upper-right back)

# =====================================================================================
# 3) THE PRINCIPAL NICHE -- now 3 WIDE x 3 TALL so the ARCH reads. Recess in the back wall with a
#    chiseled back panel, a smooth-stone-slab ledge, and a corbel arch at the top: two top-half
#    corner stairs meeting a centre chiseled KEYSTONE (resting on the wall course above -- supported).
# =====================================================================================
S.box(1.5, 0.55, 2.5, 2, 0.45, 2, NICHE)            # recessed shadow cavity (3-wide read, cut into the back wall)
S.box(1.5, 0.6, 2.5, 2, 0.4, 2, CHIS)               # chiseled_stone_bricks back panel (the flame sits against carved stone)
S.box(1.4, 0.5, 2.5, 2.2, 0.5, 0.3, LEDGE)          # smooth_stone_slab offering ledge (candles + soul-lantern on this)
# corbel arch: left + right top-half corner stairs stepping inward to a bright centre keystone
S.box(1.4, 0.5, 4.5, 0.7, 0.5, 0.6, CHIS)           # left arch corner stair (rests on the niche jamb)
S.box(2.9, 0.5, 4.5, 0.7, 0.5, 0.6, CHIS)           # right arch corner stair
S.box(2.1, 0.5, 4.9, 0.8, 0.5, 0.6, KEY)            # chiseled KEYSTONE closing the arch crown (brightest, supported above)

# =====================================================================================
# 4) FREE-STANDING FRONT PILLAR PAIR -- two 1x1 columns at the front corners, 4 tall, capped with
#    chiseled brick. The OPEN front the silhouette keeps scaling. Grounded vertical stacks on the plinth.
# =====================================================================================
def pillar(px):
    S.box(px, 3.3, 2, 0.8, 0.8, 0.4, CHIS)          # moulded base block (proud footing)
    S.box(px+0.05, 3.35, 2.4, 0.7, 0.7, 3.4, PILLAR, seam=True)   # light dressed shaft (4 tall total)
    S.box(px-0.1, 3.2, 5.8, 0.95, 0.95, 0.5, CHIS)  # chiseled capital cap (proud -> the crossbeam lands on stone)
pillar(1.1)                                          # west front pillar (front-left corner)
pillar(3.1)                                          # east front pillar (front-right corner)

# =====================================================================================
# 5) SOLID CROSSBEAM between the pillar tops -- a chiseled_stone_bricks block run laid block-to-
#    block from capital to capital (supported at BOTH ends). The chain lantern hangs UNDER it.
#    (Per build_technique: a SOLID beam, NEVER a stone_brick_wall used as a horizontal lintel.)
# =====================================================================================
S.box(1.1, 3.25, 6.3, 2.9, 0.9, 0.6, CHIS)          # solid chiseled crossbeam (pillar-cap to pillar-cap)

# =====================================================================================
# 6) GABLE ROOF (first roofed tier, the payoff) -- a peaked gable over the 5x5: stone_brick_stairs
#    climb from both long eaves to a single ridge run; eaves overhang the pillars half a block;
#    gable ends filled with a stone_bricks tympanum. Each course sits on the solid course beneath.
#    Roof base lifted to y7 (on the crossbeam course) so the open-front pillars + lantern breathe.
# =====================================================================================
S.box(0.5, -0.3, 7, 4, 4.0, 1, ROOF)                # eave course (proud overhang all round -> shadow line over the pillars)
S.box(1, 0.2, 8, 3, 3.4, 1, ROOFR)                  # second pitch course (lighter -> stepped read)
S.box(1.4, 0.6, 9, 2.2, 2.6, 1, ROOF)              # third pitch course
S.box(1.7, 0.9, 10, 1.6, 2.0, 0.6, KEY)            # ridge run (chiseled-cap ridge, the crest line)
# gable tympanum filling the FRONT triangle (stone_bricks, so the roof reads closed, not floating)
S.box(1.5, 3.0, 7, 2, 0.45, 1.3, SB)               # front gable tympanum field (fills under the front pitch)
S.box(1.5, 3.0, 8.3, 2, 0.45, 0.8, ROOFR)          # upper tympanum block (closes to the ridge)

# vine off the east eave-end solid face (distance_decay note; valid full-face attachment)
S.box(3.62, 0.4, 7.3, 0.06, 0.5, 1.4, VINE)

# =====================================================================================
# ACCENTS -- a chain lantern hung from the SOLID crossbeam + 3 candles + a soul-lantern (cool/warm).
# =====================================================================================
# chain lantern body, hung UNDER the solid crossbeam (supported above -> never floating)
S.box(2.3, 3.45, 5.6, 0.4, 0.4, 0.6, LANT)          # hanging chain-lantern fixture under the crossbeam
S.accent(2.5, 3.5, 5.55, "glow", "#ffd47a", r=2.4)  # chain-lantern glow (warm, in the open front)
S.accent(2.0, 0.55, 3.0, "glow", "#ffe6a8", r=1.7)  # 3-candle row glow on the niche ledge (warm)
# soul-lantern accent -- the cool counterpoint, set on the ledge at the niche side
S.box(2.85, 0.55, 3.1, 0.32, 0.32, 0.42, SOUL)      # soul-lantern body on the ledge
S.accent(3.0, 0.55, 3.4, "glow", SOUL, r=1.7)       # soul-lantern cool glow

S.label(2.0, 0.9, 10, "FIRST ROOF: peaked gable + filled tympanum")
S.label(3.1, 3.3, 6.3, "solid chiseled crossbeam -> chain lantern hangs under it")
S.label(3.1, 3.3, 4.5, "free-standing front pillar pair (capped)")
S.label(2.5, 0.5, 4.9, "3-wide ARCHED niche + chiseled keystone")
S.label(2.5, 0.55, 3.0, "3-candle ledge + soul-lantern (cool/warm)")
S.label(1.0, 0.0, 3.5, "real 3-sided alcove -- a room out of the rain")
S.label(0, 0, 1.2, "two-course stepped plinth (5x5 -> 3x3 andesite)")

out = S.svg(title="Wayshrine R3 (Road) -- the architecture jump: roofed 3-sided alcove, pillar pair, arched niche, first roof",
            size_label="5x5 foot * h7 * 1 chain-lantern + soul-lantern + 3 candles (an enclosed roadside shrine)",
            label_w=352)
open("detail_svg/wayshrine_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/wayshrine_road.svg | bytes", len(out.encode()))
