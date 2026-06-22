"""Menhir TRAIL (R1, floor of the ladder) -> detail_svg/menhir_trail.svg.
Per deco_catalog_v2.json id 'menhir' tier trail (footprint 1x1, height 2): the smallest legible
STANDING STONE -- ONE crooked upright fieldstone slab half-sunk in the turf, with a SINGLE buried
companion stone half-sunk in a diagonal neighbour column. UNLIT, reads by silhouette in daylight.
The identity vs the cairn is the geometry: ONE leaning upright block (never a 2-3 stone hand-stack).
massing: bed the shaft column in detail:packed (top flush w/ grass), one buried rubble stone in a
hash-chosen diagonal neighbour (only its top shows), then ONE knee-high core block offset +1 on the
lean axis with a detail:packed slab WEDGE under the leaning edge (the lean is supported, never
floating). Remote: core picks its mossy variant + one glow_lichen face on the shaded lean side.
Originality/inspiration (FORM/technique only, credited CREDITS.md, no assets/NBT copied): neolithic
single standing stones (menhirs) for the one-stone leaning silhouette. This is the trail rung of the
same wnl_menhir whose great_road top tier is render_menhir.py; the data builder hashes the
lean/decay/palette live per spawn."""
from iso_render import Iso

S = Iso(U=26, occlusion=True)

# palette (literal) -- WIDE-CONTRAST ladder so every material reads as itself after the
# renderer's 0.84/0.70 face-shading. Only 3 stone families at the floor of the ladder:
CORE   = "#8a8276"   # cobblestone core stone (the one upright standing slab -- the common pick)
MOSSY  = "#6f7d56"   # mossy_cobblestone variant smear (remote weathering, clearly green not just dark)
RUBBLE = "#7c7468"   # accent:cobblestone buried companion stone (slightly darker -> sits IN the earth)
PACKED = "#6b5a45"   # detail:packed_mud bed + wedge slab (warm earth -> reads as the SET-IN ground, not stone)
LICHEN = "#9fb86a"   # glow_lichen face smear on the shaded lean side (remote tell, NOT a light)

# geometry: the shaft column is at x1,z1. Road faces FRONT (south, high z). The buried companion
# stone sits in the FRONT-EAST diagonal neighbour (x2,z2) so the camera reads it as a real spill.

# --- Course 0 (y0): BED the stone + the single buried companion ---
# packed_mud bed under the shaft column, sunk so its top sits flush with grade (the stone rises
# straight from set-in earth -- "set INTO the land, not dropped").
S.box(1, 1, 0, 1, 1, 0.45, PACKED)                  # detail:packed bed (top flush with grass)
# ONE buried companion fieldstone, half-sunk in the FRONT-EAST diagonal neighbour -- only its top
# face shows (dy<0.5) and it ABUTS the bed (shares the x2/z2 edge with the shaft column) -> a real
# half-sunk neighbour stone, never a floating second stack. This is the WHOLE rest of the footprint.
S.box(2, 2, 0, 1, 1, 0.4, RUBBLE)                   # accent:rubble half-buried companion (top face only)

# --- Course 1 (y1): ONE leaning core block -- the crooked single upright (the identity) ---
# the monolith LEANS: offset +0.45 toward FRONT-EAST (the visible faces) on the hash lean axis.
# The inner ~half still bears on the bed below, and a packed_mud WEDGE slab is tucked under the
# overhanging (front-east) edge so the lean is SUPPORTED -- never a floating offset.
S.box(1.45, 1.45, 1, 0.5, 0.5, 0.45, PACKED)        # detail:packed WEDGE under the leaning edge (grounds the lean)
S.box(1.0, 1.0, 1, 1, 1, 1, CORE, seam=True)        # the one knee-to-thigh-high leaning standing block
# remote-decay tell: a single mossy smear on the shaded lean face + a glow_lichen strip (NOT a light,
# reads in daylight). Both abut the core front/east face (no floating decoration).
S.box(1.0, 1.95, 1.05, 0.55, 0.06, 0.85, MOSSY)     # mossy_cobblestone smear on the shaded (left) front face
S.box(1.62, 1.95, 1.15, 0.34, 0.06, 0.5, LICHEN)    # glow_lichen strip on the same front face (a daylight tell, NOT a light)

S.label(1.5, 1.5, 2.0, "ONE leaning upright core block -- the crooked standing stone (NOT a stack)")
S.label(1.9, 1.5, 1.2, "packed_mud wedge under the lean (supported, never floating)")
S.label(1.0, 1.9, 1.4, "remote tell: mossy smear + 1 glow_lichen face (unlit)")
S.label(2.5, 2.0, 0.4, "single buried companion stone (half-sunk in a diagonal neighbour)")
S.label(1.0, 1.0, 0.2, "shaft column BEDDED in packed_mud (set into the earth, not dropped)")

out = S.svg(title="Menhir R1 (Trail) -- one crooked leaning standing stone + a buried companion, unlit, reads by silhouette",
            size_label="1x1 foot * h2 * 0 lanterns (ladder floor -- a lone leaning stone you'd nearly walk past)",
            label_w=348)
open("detail_svg/menhir_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/menhir_trail.svg | bytes", len(out.encode()))
