"""Well TRAIL (R1, floor of the ladder) -> detail_svg/well_trail.svg.
Per deco_catalog_v2.json id 'well' tier Trail (footprint 3x3, height 2): the humblest readable
form of the fountain-house family -- a raw stone-ringed SPRING you can see water in. Centre 1x1
shaft sunk 3 deep with a minecraft:water source at the bottom; the 8 surrounding cells are a rough
horseshoe of mossy_cobblestone + cobblestone with ONE cell left as a worn dirt_path drinking lip
(the open side the trail meets). A LOW lip (cobblestone_wall + one mossy variant) rises on only the
three rim cells opposite the path lip; ONE grounded lantern rests on the centre rim wall. No spout,
no posts, no roof -- just a place to drink. Reads by silhouette + visible water in daylight.

This is the Trail rung of the same wnl_well whose Great Road top tier is render_well.py (a
colonnaded fountain-house). The data builder hashes palette/decay/rotation live per spawn.
Inspiration (form/technique ONLY, credited in CREDITS.md; NO assets/NBT copied): Roman castellum-
aquae street springs + medieval village watering points -- the bare stone-ringed spring as the
humblest ancestor of the civic fountain-house. Entirely original WNL vanilla-block build.
ISO: road-facing FRONT = high-z (south) + high-x (east); the open dirt-path drinking lip is on the
FRONT so the viewer reads straight into the water from the avenue side."""
from iso_render import Iso

S = Iso(U=24)

# ---- palette (literal) -- a wide-contrast ladder so every material reads as itself ----
COBB   = "#8a8276"   # minecraft:cobblestone ring stone (the common pick, cool mid grey)
MOSS   = "#6f7d56"   # minecraft:mossy_cobblestone -- moss creeps into the horseshoe (green-grey)
WALL   = "#9a9384"   # minecraft:cobblestone_wall low lip (lighter dressed-ish nub -> reads as a wall)
MWALL  = "#7c8a60"   # minecraft:mossy_cobblestone_wall (one mossy lip nub, greener than COBB wall)
PATH   = "#6e5d3e"   # minecraft:dirt_path worn drinking lip (warm brown -> the open approach side)
SHAFT  = "#4b463c"   # dark sunk shaft wall (cobble in shadow, the spring throat reads as a hole)
FLOOR  = "#5d5a50"   # spring-shaft floor stone just under the water (dark warm grey)
WATER  = "#2f74b6"   # minecraft:water spring source (deep saturated blue -- unmistakable)
WATER2 = "#5aa8e2"   # water surface glint (bright cyan-blue -> the water reads as wet + alive)
VINE   = "#586f3a"   # minecraft:vine (sparse decay note on one ring cell, far-from-civ)
LANT   = "#ffd47a"   # lantern glow (ONE grounded light, on the centre rim wall)

# grid: 3x3 footprint x 0..3, z (depth) 0..3. centre cell = (1,1).
# Course 0 (y=0): the ground ring -- a rough HORSESHOE of mossy_cobble + cobble around the shaft,
# ONE front-centre cell left as a worn dirt_path drinking lip (the open side the trail meets).
# Each ring cell is a full block sunk flush with the ground so the spring reads rooted, not perched.
RING = {  # per-cell block: graph-paper grid (deco_catalog massing is explicit per cell)
    (0,0): MOSS, (1,0): COBB, (2,0): MOSS,     # back row (z=0, far)
    (0,1): COBB,             (2,1): COBB,      # mid row flanks (centre is the shaft)
    (0,2): MOSS, (1,2): PATH, (2,2): COBB,     # front row (z=2, near) -- (1,2) is the dirt-path lip
}
for (cx,cz),col in RING.items():
    S.box(cx, cz, 0, 1, 1, 1, col, seam=True)

# Course 0 sunk SHAFT: the centre 1x1 dug down -- dark throat walls + a water source at the bottom.
# Drawn as a short recessed stack (a hole you see INTO): dark wall course, floor, then the spring.
S.box(1, 1, -0.9, 1, 1, 0.9, SHAFT)            # sunk shaft throat (below the ring top -> reads as a hole)
S.box(1, 1, -0.05, 1, 1, 0.18, FLOOR)          # shaft floor stone just under the water line
S.box(1, 1, 0.13, 1, 1, 0.62, WATER)           # the spring WATER source, recessed in the shaft mouth
S.box(1.18,1.18,0.74, 0.6,0.6,0.06, WATER2)    # bright surface glint -> the water reads as wet

# Course 1 (y=1): a LOW lip on only the THREE rim cells OPPOSITE the path lip (the back + back-flanks),
# so the rim reads from the road side without hiding the water. cobblestone_wall x2 + one mossy wall;
# the path side + the two front-flanking cells stay flush (worn down, walkable). Walls are <1 tall nubs.
S.box(0, 0, 1, 1, 1, 0.7, WALL,  seam=True)    # back-west lip nub (cobblestone_wall)
S.box(1, 0, 1, 1, 1, 0.7, MWALL, seam=True)    # back-CENTRE lip nub (mossy_cobblestone_wall -> lantern seat)
S.box(2, 0, 1, 1, 1, 0.7, WALL,  seam=True)    # back-east lip nub (cobblestone_wall)

# Detail (sparse, decay-gated): a single vine trailing off the back-east ring cell, ABUTTING it
# (grounded spill down the block face, never floating) -- far-from-civ weathering only.
S.box(2.05, 0.0, 0.55, 0.12, 0.5, 0.45, VINE)  # vine clinging to the east face of the back-east wall

# ONE grounded lantern: rests directly on top of the centre back rim wall (the MWALL nub at (1,0)).
S.accent(1.5, 0.5, 1.85, "glow", LANT, r=2.3)  # the single Trail lantern, seated on the rim wall

# water glint accent on the open spring mouth so the wet read carries even small
S.accent(1.5, 1.5, 0.8, "glow", "#bfe6ff", r=1.9)

S.label(1.5, 0.5, 1.95, "ONE grounded lantern (rests on the centre rim wall)")
S.label(1.0, 0.0, 1.0, "low lip on 3 back cells (cobblestone_wall + 1 mossy)")
S.label(1.5, 1.5, 0.8, "1x1 spring shaft sunk 3 deep -- minecraft:water you can see")
S.label(1.0, 2.0, 0.5, "worn dirt_path drinking lip (the open side the trail meets)")
S.label(0.0, 0.0, 0.5, "rough horseshoe ring -- mossy_cobblestone + cobblestone")

out = S.svg(title="Well R1 (Trail) -- raw stone-ringed spring: horseshoe rim, sunk 1x1 water shaft, one lantern, unlit-by-day",
            size_label="3x3 foot * h2 * 1 lantern (ladder floor -- a place to drink, no spout/posts/roof yet)",
            label_w=352)
open("detail_svg/well_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/well_trail.svg | bytes", len(out.encode()))
