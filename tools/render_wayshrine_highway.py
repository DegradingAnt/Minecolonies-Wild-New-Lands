"""Wayshrine HIGHWAY (R4) -> detail_svg/wayshrine_highway.svg.
Per deco_catalog_v2.json id 'wayshrine' tier Highway (footprint 9x9, height 11): the NON-LINEAR
leap below the Great-Road top -- the topology FLIPS from a backed wall-alcove to a free-standing
FOUR-PILLAR open LANTERN-HOUSE pavilion you walk THROUGH and AROUND, on a two-step monumental
plinth (calibrated against the structurize big-well 9x9 so it reads as a true landmark, beside the
gatehouse anchor). Four corner piers carry a SOLID polished-andesite beam ring; a central marker
stele + a dressed rear backing wall hold the 3-wide arched principal niche; a STEPPED-apex hipped
roof crowns it with a supported finial-lantern hung under an overhanging block; and -- the first
flanking-lantern payoff -- a PAIR of grounded lamp-posts light the front-stair approach.

Non-linear jump: 5x5 -> 9x9 (3.2x area), height 7 -> 11, alcove -> walk-through pavilion. Same
wnl_wayshrine data builder as render_wayshrine.py (Great Road top). ISO: the front (max-z) carries
the grand stair + flanking lamp-posts + an open inter-pier bay so the lit stele/niche reads through.
Build technique per spec: beams = SOLID block-to-block runs on the pier capitals (NEVER wall-lintels);
every hung lantern has a solid block directly above it; the apex is a stepped block-stack, not a spike.
Originality/inspiration: lantern-of-the-dead pillared lantern-tower + Roman columned roadside monument
FORM, technique only -- credited in CREDITS.md, no assets/NBT/palette copied."""
from iso_render import Iso

S = Iso(U=11, occlusion=True)

# ---- palette (literal) -- a WIDE-contrast ladder: piers + stele read LIGHT, backing wall DARK,
#      slate roof DARKEST. dark->light: ROOF < WALL < NICHE < AND < SB < PIER < CHIS < STELE < KEY.
SB     = "#8c867a"   # stone_bricks (plinth course 1, pier bases, tympanum/roof fill)
AND    = "#83868b"   # polished_andesite (inset plinth course 2 + the SOLID beam ring -- cool, separates)
WALL   = "#766f60"   # rear backing wall (DARK warm dressed stone -> the pale niche frame + piers pop)
PIER   = "#cdc7b8"   # the four corner piers + lamp-post heads (light dressed -> the hero pavilion frame)
CHIS   = "#c2bca8"   # chiseled_stone_bricks (pier shafts, capitals, arch keystone, backing-wall dressing)
KEY    = "#ece5d0"   # brightest dressed accent (keystone crown, finial block, ridge cap)
STELE  = "#bcb6a7"   # smooth_stone_slab marker-stele table (light, the focal object at centre)
NICHE  = "#46423a"   # recessed arched-niche interior (deep shadow -> the recess reads cut-IN)
ROOF   = "#585350"   # stone-brick hipped roof field (darkest mass -> strong contrast vs pale piers)
ROOFR  = "#6b655d"   # roof ridge / upper course (lighter -> the hip reads stepped)
MOSS   = "#727f57"   # moss up the piers (remote-decay note)
CRACK  = "#827a6b"   # cracked-brick scatter (remote-decay note)
LANT   = "#caa15a"   # hung-lantern body (warm metal)
SOUL   = "#5fb8c4"   # soul-lantern accent (cool teal -> the cool/warm contrast on the pier capitals)
TIMBER = "#7a5c3a"   # lamp-post standards (warm timber posts flanking the stair)
STEP   = "#a7a08e"   # broad front stair (stone_brick_stairs, 5 wide -- a monumental approach)

# =====================================================================================
# 1) TWO-STEP MONUMENTAL PLINTH (9x9): course 1 stone_bricks 9x9; course 2 polished-andesite 7x7
#    inset -> a landmark base you climb. Broad 5-wide front stair = the monumental approach.
# =====================================================================================
S.box(0, 0, 0, 9, 9, 1, SB, seam=True)               # course 1: stone_bricks 9x9
S.box(1, 1, 1, 7, 7, 1, AND)                         # course 2: polished_andesite 7x7 inset (the pavilion floor)
# broad 5-wide front stair spanning the approach (you climb it -- stone_brick_stairs[facing=south])
S.box(2, 8, 1, 5, 1, 0.5, STEP)                      # front stair tread (5 wide, proud lip)
S.box(2.5, 8.3, 1, 4, 0.7, 0.25, STEP)               # lower stair tread (the second step down to the road)

# =====================================================================================
# 2) FOUR-PILLAR OPEN LANTERN-HOUSE -- four corner piers, each a chiseled shaft 7 tall on a stone-
#    bricks base, capped by an outward stair-flare. You walk THROUGH and AROUND it (free-standing,
#    no walls between the front piers). Piers at the 7x7 floor corners (grounded vertical stacks).
# =====================================================================================
PIERX = (1.5, 6.0)   # west/east pier columns (on the andesite floor, inset from the 9x9 edge)
PIERZ = (0.8, 5.3)   # back/front pier rows (back row near z0, front row toward the viewer)
def pier(px, pz):
    S.box(px, pz, 2, 1.4, 1.4, 0.5, SB)              # stone_bricks base block (the footing)
    S.box(px+0.15, pz+0.15, 2.5, 1.1, 1.1, 6.5, CHIS, seam=True)   # chiseled shaft, 7 tall
    S.box(px-0.1, pz-0.1, 9, 1.6, 1.6, 0.6, PIER)    # capital flare (proud all 4 faces -> beams land on stone)
for px in PIERX:
    for pz in PIERZ:
        pier(px, pz)
# moss + a cracked-brick note up the shaded back-left pier (remote-decay, never to ruin near civ)
S.box(1.6, 0.9, 4, 1.0, 0.3, 1, MOSS)
S.box(6.1, 0.9, 6, 0.3, 1.0, 1, CRACK)

# =====================================================================================
# 3) CENTRAL MARKER STELE + REAR BACKING WALL -- a 3x3 raised core: a chiseled plinth topped with
#    a smooth-stone-slab table; the REAR (z0) inter-pier bay is a dressed backing wall holding the
#    3-wide arched principal niche (same arch grammar as Road: corner stairs + chiseled keystone).
# =====================================================================================
# central marker stele (3x3 core, raised, at pavilion centre -> the focal object you orient by)
S.box(3.2, 3.2, 2, 2.6, 2.6, 1.5, CHIS, seam=True)   # chiseled stele plinth (raised core)
S.box(3.0, 3.0, 3.5, 3.0, 3.0, 0.4, STELE)           # smooth-stone-slab table top (proud -> a real table)
# rear backing wall in the back inter-pier bay (z0), dressed stone_bricks + chiseled, holds the niche
S.box(2.0, 0.2, 2, 5.0, 0.8, 6, WALL, seam=True)     # rear backing wall (between the back piers)
S.box(2.0, 0.2, 2, 5.0, 0.8, 1, CHIS)                # chiseled dado course at the base (dressed read)
# the 3-wide arched principal niche in the backing wall
S.box(3.0, 0.5, 3, 3.0, 0.45, 3, NICHE)             # recessed shadow cavity (3-wide arched niche)
S.box(3.0, 0.55, 3, 3.0, 0.4, 3, CHIS)              # chiseled back panel (the flame against carved stone)
S.box(3.0, 0.45, 3, 3.0, 0.5, 0.3, STELE)          # smooth-stone-slab niche ledge (candle cluster on this)
# corbel arch over the niche: two top-half corner stairs meeting a centre keystone (supported)
S.box(2.9, 0.45, 5.5, 1.0, 0.5, 0.6, CHIS)         # left arch corner stair (on the niche jamb)
S.box(5.1, 0.45, 5.5, 1.0, 0.5, 0.6, CHIS)         # right arch corner stair
S.box(3.9, 0.45, 5.9, 1.2, 0.5, 0.6, KEY)          # chiseled KEYSTONE closing the arch crown (brightest)

# =====================================================================================
# 4) SOLID BEAM RING (carved-beam read, NOT walls) -- a continuous polished-andesite course laid
#    block-to-block capital-to-capital on all four sides (supported at the piers), bracketed
#    underneath at the capitals by stair half-blocks. The beams CONNECT + read structurally honest.
# =====================================================================================
S.box(1.4, 0.7, 9.6, 6.2, 0.9, 0.7, AND)            # back beam (z0 run, pier-cap to pier-cap)
S.box(1.4, 6.0, 9.6, 6.2, 0.9, 0.7, AND)            # front beam (the run the traveller reads)
S.box(1.4, 0.7, 9.6, 0.9, 6.2, 0.7, AND)            # left beam (x run)
S.box(6.6, 0.7, 9.6, 0.9, 6.2, 0.7, AND)            # right beam
# under-bracket stair flares at the four front-visible capitals (decorative support read)
S.box(1.4, 5.9, 9.2, 1.5, 0.5, 0.4, CHIS)           # front-left bracket
S.box(6.0, 5.9, 9.2, 1.5, 0.5, 0.4, CHIS)           # front-right bracket

# =====================================================================================
# 5) HIPPED + STEPPED ROOF (the wnl crown, not a clean pyramid) -- stone_brick_stairs climb from
#    all four eaves; the apex is STEPPED (a 3x3 then 1x1 chiseled block-stack rising 1 above the
#    field) as a SOLID finial. Eaves overhang 1 block all round + shelter the lanterns.
# =====================================================================================
S.box(0.6, -0.1, 10.3, 7.8, 7.8, 1, ROOF)           # broad eave course (1-block overhang all round)
S.box(1.6, 0.9, 11.3, 5.8, 5.8, 1, ROOFR)           # second hip course (lighter -> stepped read)
S.box(2.6, 1.9, 12.3, 3.8, 3.8, 1, ROOF)            # third hip course
S.box(3.3, 2.6, 13.3, 2.4, 2.4, 1, ROOFR)           # fourth hip course (near the apex field)
# STEPPED-apex finial: a 3x3 then 1x1 chiseled block-stack rising 1 above the roof field (SOLID)
S.box(3.3, 2.6, 14.3, 2.4, 2.4, 0.7, CHIS)          # 3x3 finial base (sits on the roof field)
S.box(4.0, 3.3, 15.0, 1.0, 1.0, 0.9, KEY)           # 1x1 finial cap (the crowning solid block)
# overhanging chiseled block at the FRONT gable peak the finial-lantern hangs UNDER (supported above)
S.box(3.6, 5.9, 12.0, 1.8, 0.6, 0.7, CHIS)          # overhang block (proud over the front eave)

# =====================================================================================
# 6) FLANKING APPROACH LAMP-POSTS -- a pair of grounded stone_brick_wall lamp-posts (3 high) one
#    each side of the front stair, each topped with a solid chiseled cap carrying a hung lantern
#    UNDER it: the FIRST flanking-lantern payoff lighting the approach. Grounded on the lower step.
# =====================================================================================
def lamp_post(lx):
    S.box(lx, 8.6, 1.25, 0.8, 0.8, 0.5, SB)         # stone footing on the front step
    S.box(lx+0.1, 8.7, 1.75, 0.6, 0.6, 2.6, PIER)   # stone_brick_wall standard (3 high, light)
    S.box(lx-0.1, 8.5, 4.35, 0.9, 0.9, 0.5, CHIS)   # solid chiseled cap (the lantern hangs UNDER it)
    S.box(lx+0.05, 8.65, 3.85, 0.7, 0.7, 0.5, LANT) # hung-lantern body under the cap (supported above)
lamp_post(1.0)                                       # west flanking lamp-post (left of the stair)
lamp_post(7.2)                                       # east flanking lamp-post (right of the stair)

# =====================================================================================
# ACCENTS -- two canopy lanterns hung from solid beam blocks + a candle cluster + a soul-lantern
#            pair on the pier capitals + the roof finial-lantern + the two flanking lamp-posts.
# =====================================================================================
# two canopy lanterns hung UNDER the front solid beam (supported above), lighting the open pavilion
S.box(3.0, 6.05, 8.9, 0.4, 0.4, 0.55, LANT)         # west canopy lantern body under the front beam
S.box(5.0, 6.05, 8.9, 0.4, 0.4, 0.55, LANT)         # east canopy lantern body
S.accent(3.2, 6.1, 8.85, "glow", "#ffd47a", r=2.2)
S.accent(5.2, 6.1, 8.85, "glow", "#ffd47a", r=2.2)
# candle cluster in the backing-wall niche (warm, on the ledge)
S.accent(4.5, 0.5, 3.6, "glow", "#ffe6a8", r=2.0)
# soul-lantern pair set ON the front pier capitals (cool counterpoint, sitting on a solid top face)
S.box(1.6, 5.4, 9.6, 0.4, 0.4, 0.45, SOUL)          # west front-pier soul-lantern (stands on the capital)
S.box(6.1, 5.4, 9.6, 0.4, 0.4, 0.45, SOUL)          # east front-pier soul-lantern
S.accent(1.8, 5.6, 9.95, "glow", SOUL, r=1.8)
S.accent(6.3, 5.6, 9.95, "glow", SOUL, r=1.8)
# roof finial-lantern hung UNDER the overhanging front-peak block (supported above, never floating)
S.box(4.3, 6.0, 11.4, 0.4, 0.4, 0.55, LANT)         # finial-lantern body under the overhang block
S.accent(4.5, 6.05, 11.4, "glow", "#eafff8", r=2.2)
# the two flanking approach lamp-post heads (the payoff lights on the stair)
S.accent(1.4, 8.7, 4.1, "glow", "#ffe6a8", r=2.4)
S.accent(7.6, 8.7, 4.1, "glow", "#ffe6a8", r=2.4)
# finial crown marker
S.accent(4.5, 3.8, 15.9, "finial")

S.label(4.5, 3.0, 15.0, "stepped-apex hipped roof + supported finial-lantern")
S.label(6.6, 0.7, 9.6, "SOLID polished-andesite beam ring (block-to-block on the piers)")
S.label(6.0, 5.3, 9.5, "four-pillar walk-through lantern-house (you pass THROUGH)")
S.label(4.5, 0.5, 5.9, "central stele + arched backing-wall niche")
S.label(7.2, 8.6, 4.3, "flanking approach lamp-posts -- first flanking-lantern payoff")
S.label(2.0, 8.0, 1.0, "two-step plinth (9x9 -> 7x7) + broad 5-wide front stair")

out = S.svg(title="Wayshrine R4 (Highway) -- four-pillar walk-through lantern-house: beam ring, stele, stepped-hip roof, flanking lamp-posts",
            size_label="9x9 foot * h11 * 2 canopy + finial + 2 flanking lanterns + soul-pair + candles (a landmark you see down the road)",
            label_w=372)
open("detail_svg/wayshrine_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/wayshrine_highway.svg | bytes", len(out.encode()))
