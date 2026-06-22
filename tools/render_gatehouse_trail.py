"""Gatehouse TRAIL (R1, floor of the ladder) -> detail_svg/gatehouse_trail.svg.
Per deco_catalog_v2.json id 'gatehouse' tier Trail (footprint 5x3, opening 3 clear, height 4):
the smallest the family gets -- a bare timber goalpost way-arch on two stone footing pads, with
ONE hanging lantern slung under the beam. Reads 'someone marked the way', not 'someone built a
gate'. Pure data-driven, no NBT. Optional weathering (hash, far from civ): a lean-rail between the
posts + a vine on the beam -- drawn here as the weathered case so the rung has character.

ISO: road-facing FRONT = high-z (south, z=2 face) + high-x (east). The trail passes THROUGH the
3-clear opening front-to-back. Same wnl_gatehouse family as render_gatehouse.py (Great Road top);
the data builder hashes lean/decay/palette/weathering live per gate. Inspiration: universal timber
way-arch / lych-gate folk form -- technique only, credited in CREDITS.md, no assets/NBT copied."""
from iso_render import Iso

S = Iso(U=22)

# ---- palette (literal) -- a WIDE-CONTRAST ladder so each material reads as itself.
#      luminance dark->light: FOOT < BEAM < POST < RAIL  ; LANT/FLAME warm; VINE the one green.
FOOT  = "#6f685d"   # cobblestone / mossy_cobblestone footing pad (dark grey -> reads heavy + rooted)
POST  = "#8a6a3f"   # oak/spruce LOG upright post (warm mid timber -- the structural pair)
BEAM  = "#7a5c3a"   # stripped-log lintel beam (slightly DARKER timber -> spans read distinct from posts)
RAIL  = "#a07c4a"   # oak_fence lean-rail between posts (lighter timber -> reads as the thin add-on)
VINE  = "#5f7544"   # weathering vine creeping the beam (the one green note, far-from-civ)

# =====================================================================================
# Course 0 (ground): two dressed stone FOOTING PADS only, at x=0 and x=4 (z=1), flush with
# the worn path. Everything between is OPEN so the trail passes through -> opening = 3 clear.
# =====================================================================================
S.box(0, 1, 0, 1, 1, 1, FOOT, seam=True)          # left footing pad (rooted, half the post-foot)
S.box(4, 1, 0, 1, 1, 1, FOOT, seam=True)          # right footing pad

# =====================================================================================
# Courses 1-3 (posts): two upright LOG posts, each a 1x1 column rising 3 tall, seated SQUARELY
# on the footing pads (grounded -- inner face bears fully on the pad below, no overhang).
# =====================================================================================
S.box(0, 1, 1, 1, 1, 3, POST, seam=True)          # left post y1..3
S.box(4, 1, 1, 1, 1, 3, POST, seam=True)          # right post y1..3

# =====================================================================================
# Course 4 (lintel): a single horizontal BEAM spanning x=0..4 across the post tops (axis=x).
# Rests directly on both posts (full bearing each end) -> the goalpost reads carpentered.
# =====================================================================================
S.box(0, 1, 4, 5, 1, 1, BEAM, seam=True)          # lintel beam x0..4 across the post tops

# =====================================================================================
# WEATHERING (far-from-civ case): a fence 'lean-rail' between the posts (one rail, NOT a wall)
# planted on the ground between the footings + leaning to one post, and a vine off the beam.
# Both grounded: the rail rises from the floor + abuts the right post; the vine hangs FROM the
# beam (held above), never a floating strand.
# =====================================================================================
S.box(2.6, 1.25, 0, 0.3, 0.5, 2, RAIL)            # lean-rail post nub rising from the ground (grounded)
S.box(2.0, 1.3, 1.7, 1.9, 0.35, 0.3, RAIL)        # the rail itself, leaning up to abut the right post (<0.35 rise)
S.box(2.9, 1.2, 3.3, 0.3, 0.4, 0.7, VINE)         # vine hanging FROM the beam soffit (held above, not floating)

# =====================================================================================
# LIGHTING: ONE hanging lantern slung under the beam soffit at x=2 (centred), held by the beam
# directly above -> grounded by suspension, not floating in space.
# =====================================================================================
S.accent(2.5, 1.5, 3.75, "glow", "#ffd47a", r=2.6)  # single hanging lantern under the beam centre

S.label(2.5, 1.5, 3.8, "ONE hanging lantern slung under the beam (held above)")
S.label(0.0, 1.0, 4.0, "stripped-log lintel beam (axis=x) across the post tops")
S.label(4.0, 1.0, 2.0, "two upright LOG posts -- a bare timber goalpost arch")
S.label(2.6, 1.0, 1.5, "weathering: a lean-rail + a vine (far-from-civ hash)")
S.label(0.0, 1.0, 0.4, "two dressed stone footing pads (3 clear between -- trail passes through)")

out = S.svg(title="Gatehouse R1 (Trail) -- bare timber way-arch on two stone footings, one hanging lantern",
            size_label="5x3 foot (3 clear) * h4 * 1 lantern (ladder floor -- 'someone marked the way')",
            label_w=372)
open("detail_svg/gatehouse_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/gatehouse_trail.svg | bytes", len(out.encode()))
