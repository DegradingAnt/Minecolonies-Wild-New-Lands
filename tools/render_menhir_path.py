"""Menhir PATH (R2) -> detail_svg/menhir_path.svg.
Per deco_catalog_v2.json id 'menhir' tier path (footprint 1x1 shaft on a loose 3-stone scatter,
height 3): a SMALL step up from trail -- the stone STANDS UP (2->3 high) and gains a loose turf
collar of exactly 3 dropped fieldstones half-buried in distinct neighbour columns (NOT a tidy ring).
Still ONE upright monolith, still raw + UNLIT (the big leaps are saved for highway/great_road).
massing: bed the shaft column in packed (top flush w/ grass) + scatter 3 half-buried rubble stones
at distinct hash directions; TWO stacked core blocks forming one continuous upright (upper offset +1
gently on the lean axis, a packed/slab wedge supporting its overhanging edge, lower rooted); ONE
crown core block pulled -1 on the OPPOSITE axis-sign so the top tapers ASYMMETRIC (never flat-topped),
overhang <=1 with the inward block below present. Remote: lower 2 courses swap to mossy variant + a
glow_lichen/vine face on the shaded side.
Originality/inspiration (FORM/technique only, credited CREDITS.md, no assets/NBT copied): neolithic
single standing stones (menhirs). Same wnl_menhir data builder as render_menhir.py (great_road top);
the builder hashes lean/taper/scatter/decay/palette live per spawn."""
from iso_render import Iso

S = Iso(U=24, occlusion=True)

# palette (literal) -- WIDE-CONTRAST ladder; still primal so only stone + earth families.
CORE   = "#8a8276"   # cobblestone core (the lower rooted course of the upright)
CORE2  = "#9b9488"   # andesite/stone lighter pick (the upper leaning course -> reads as its own block)
MOSSY  = "#6f7d56"   # mossy_cobblestone variant (remote weathering; clearly green)
RUBBLE = "#7c7468"   # accent:cobblestone scatter stones (a notch darker -> sit IN the turf)
GRAVEL = "#8f8779"   # one scatter stone is gravel (slot variety -> the 3 read as distinct picks)
PACKED = "#6b5a45"   # detail:packed_mud bed + wedge slab (warm earth -> the SET-IN ground read)
LICHEN = "#9fb86a"   # glow_lichen face strip on the shaded side (remote daylight tell, NOT a light)

# geometry: shaft column at x1,z1. Road faces FRONT (south, high z).

# --- Course 0 (y0): bed it + a loose 3-stone scatter collar (distinct neighbour columns) ---
S.box(1, 1, 0, 1, 1, 0.45, PACKED)                  # packed_mud bed under the shaft (top flush with grass)
# exactly 3 dropped fieldstones, half-buried, at DISTINCT hash directions over the 8 neighbours --
# a dropped-stone collar, NEVER a tidy ring. Each abuts the bed / a neighbour (a spill, not floating):
S.box(2.0, 1.05, 0, 1, 1, 0.42, RUBBLE)             # E scatter stone (abuts bed east face)
S.box(0.9, 2.0, 0, 1, 1, 0.38, GRAVEL)              # front (S) scatter stone -- gravel pick (abuts bed front face)
S.box(2.0, 2.0, 0, 1, 1, 0.34, RUBBLE)             # front-east corner stone (chains off the other two; sunk lowest)

# --- Courses 1-2 (y1-y2): TWO stacked core blocks = ONE continuous upright (waist-to-shoulder) ---
# lower block centred + rooted on the bed.
S.box(1, 1, 1, 1, 1, 1, CORE, seam=True)            # lower rooted course (the anchor of the upright)
# upper block offset +0.4 toward FRONT-EAST (single, gentle step -- lean axis). A packed/slab wedge
# is tucked under its overhanging (front-east) edge so the lean is SUPPORTED, inner half still bears.
S.box(1.42, 1.42, 2, 0.5, 0.5, 0.4, PACKED)         # wedge under the leaning upper edge (grounds the lean)
S.box(1.4, 1.4, 2, 1, 1, 1, CORE2, seam=True)       # upper leaning course (one continuous slab, not a pebble)

# --- Course 3 (y3, crown): ONE core block pulled -1 the OPPOSITE way -> asymmetric tapered top ---
# pulled back toward BACK-WEST (opposite the +x/+z lean) so the top tapers asymmetric, never a flat
# post. Overhang <=1 and the block below-and-inward (the y2 upper course) is present (support contract).
S.box(0.95, 0.95, 3, 0.85, 0.85, 0.9, MOSSY)        # asymmetric crown -- mossy (remote tell), pulled opposite the lean

# remote-decay tell: a glow_lichen strip on the shaded front face of the lower course (daylight read).
S.box(1.62, 1.97, 1.1, 0.34, 0.06, 0.7, LICHEN)     # glow_lichen on the lower-course front face (NOT a light)

S.label(0.9, 1.0, 3.4, "asymmetric tapered crown -- pulled the OPPOSITE way from the lean")
S.label(1.4, 1.4, 2.5, "upper leaning course (single +1 step, wedge-supported)")
S.label(2.0, 1.4, 1.4, "remote tell: 1 glow_lichen face on the shaded side (unlit)")
S.label(1.0, 1.0, 0.6, "lower rooted course -- one continuous upright (NOT a 2-pebble stack)")
S.label(2.4, 2.0, 0.3, "loose 3-stone scatter collar (half-buried, distinct dirs -- never a ring)")

out = S.svg(title="Menhir R2 (Path) -- the stone stands up (3 high) + a loose 3-stone scatter collar, raw + unlit",
            size_label="1x1 shaft + 3-stone scatter * h3 * 0 lanterns (deliberate + standing, still primal)",
            label_w=350)
open("detail_svg/menhir_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/menhir_path.svg | bytes", len(out.encode()))
