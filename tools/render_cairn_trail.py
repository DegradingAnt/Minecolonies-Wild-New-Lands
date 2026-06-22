"""Cairn TRAIL (R1, floor of the ladder) -> detail_svg/cairn_trail.svg.
Per deco_catalog_v2.json id 'cairn' tier Trail (footprint 1x1, height 3): the smallest legible
waymarker -- a traveller's casual 2-3 stone hand-stack, raw, UNLIT, reading by silhouette in
daylight. One half-buried base stone, one shoved-off-centre stone (supported overhang, leans but
inner half bears on the stone below), one opposite-offset slab capstone that zig-zags the pile
(omitted ~40% of the time -> varies 2-3 stones; drawn here as the 3-stone case).
Originality/inspiration: universal drystone trail-cairn folk form, technique only -- credited in
CREDITS.md, no assets/NBT copied. This is the Trail rung of the same wnl_cairn whose Great Road
top tier is render_cairn.py; the data builder hashes the lean/decay/palette live per cairn."""
from iso_render import Iso

S = Iso(U=26)

CORE  = "#8a8276"   # cobblestone core stone (the common pick)
CORE2 = "#9b9488"   # andesite/stone lighter pick -> the middle stone reads as its own block
DARK  = "#6f685d"   # cobbled_deepslate darker pick (base reads heavy + rooted)
MOSS  = "#6f7d56"   # mossy_cobblestone -- moss creeps in by distance (slab capstone here)

# Course 0 (y0): base stone, FULL block, half-buried so it reads rooted (sits IN the ground).
S.box(0, 0, 0, 1, 1, 1, DARK, seam=True)

# Course 1 (y1): stone stacked + shoved off-centre toward the FRONT-EAST (visible faces), the
# inner ~2/3 still bearing on y0 -> a supported lean that reads stable, never a floating block.
S.box(0.32, 0.32, 1, 1, 1, 1, CORE, seam=True)

# Course 2 (y2): smaller capstone laid as a SLAB, offset BACK the opposite way so the pile
# zig-zags; grounded on the y1 top face (a slab needs only edge support). Moss on the cap.
S.box(0.05, 0.0, 2, 0.9, 0.9, 0.5, MOSS)

S.label(0.5, 0.5, 2.2, "opposite-offset slab capstone (zig-zag; omitted ~40% -> 2-stone pile)")
S.label(1.0, 0.9, 1.0, "off-centre stone -- supported lean (inner half bears on the base)")
S.label(0, 0, 0.4, "half-buried base stone (rooted, not dropped)")

out = S.svg(title="Cairn R1 (Trail) -- raw 2-3 stone hand-stack, unlit, reads by silhouette",
            size_label="1x1 foot * h3 * 0 lanterns (ladder floor -- a traveller's casual stone stack)",
            label_w=336)
open("detail_svg/cairn_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/cairn_trail.svg | bytes", len(out.encode()))
