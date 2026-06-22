"""Menhir ROAD (R3) -> detail_svg/menhir_road.svg.
Per deco_catalog_v2.json id 'menhir' tier road (footprint 3x3 plinth pad under a continuing single
1x1 shaft, height 6): the first sign anyone TENDED this stone -- a deliberately-irregular laid 3x3
plinth + the shaft doubles to a man-high (eye-line+) standing stone. STILL ONE monolith, STILL
UNLIT (a wild marker stays dark, SPEC 'wild stays dark' -- the big light leap waits for highway).
massing: a 3x3 packed/cobble plinth laid flush + DELIBERATELY irregular (1-2 corner blocks dropped
to slab / left as coarse_dirt, ONE pad block raised +1 at the shaft foot as a worn step); a single
TOPPLED companion stone lies FLAT on the plinth at an edge (a fallen sibling -- reinforces 'one
stone' lore, never a pile). The SHAFT = 4 stacked core blocks with an irregular S-taper: y1 centred,
y2 offset +1 (lean axis), y3 back to centred, y4 offset +1 (cross axis) -- no two faces line up,
every offset edge wedge-supported, net drift ~1 block. Crown = ONE core block pulled to a corner,
asymmetric, supported. Remote: 30-50% of shaft courses swap to mossy/cracked + a vine curtain.
Originality/inspiration (FORM/technique only, credited CREDITS.md, no assets/NBT copied): neolithic
single standing stones (menhirs) + medieval wayside way-stones for the 'tended plinth' idea. Same
wnl_menhir data builder as render_menhir.py (great_road top); hashes lean/taper/decay/palette per spawn.
ISO: road-facing FRONT = high-z (south) + high-x (east) -- the worn step + fallen stone read on that front."""
from iso_render import Iso

S = Iso(U=20)

# palette (literal) -- WIDE-CONTRAST: the LAID plinth (cool dressed greys) vs the ROUGH shaft (warm
# fieldstone) is the whole story of this tier (first human care under a still-rough stone).
PLINTH = "#9a948a"   # 3x3 laid plinth pad (cool dressed cobble -> reads as the TENDED base)
STEP   = "#7c766b"   # the worn raised step block at the shaft foot (darker -> reads as a riser)
SLABC  = "#878074"   # a corner dropped to a cobblestone_slab (irregular pad edge)
DIRT   = "#5d4f3a"   # one corner left coarse_dirt (sits IN the ground -- pad not a clean square)
CORE   = "#8a8276"   # cobblestone shaft core (the rough standing stone -- common pick)
CORE2  = "#9b9488"   # andesite/stone lighter pick (alternating courses read as their own block)
CRACK  = "#9a8f7e"   # cracked_stone_bricks weathered course (remote tell, a tended-but-worn note)
MOSSY  = "#6f7d56"   # mossy_cobblestone variant (remote weathering; clearly green)
FALLEN = "#827a6e"   # the TOPPLED companion stone lying flat (a notch off the shaft -> own stone)
PACKED = "#6b5a45"   # packed_mud / slab wedge under each lean (warm -> reads as the support wedge)
VINE   = "#5e7a3a"   # vine curtain down the shaded face (remote daylight tell, NOT a light)

# geometry: 3x3 plinth on x0-3,z0-3. Shaft column centred at x1,z1. Road faces FRONT (high z).

# --- Course 0 (y0): a DELIBERATELY-IRREGULAR laid 3x3 plinth + a worn step + a fallen companion ---
S.box(0, 0, 0, 3, 3, 1, PLINTH, seam=True)          # 3x3 laid plinth pad (the tended base the stone stands on)
S.box(0, 0, 0, 1, 1, 1, DIRT)                       # back-west corner left coarse_dirt (sits IN the ground)
S.box(2, 0, 0, 1, 1, 0.55, SLABC)                   # east-back corner dropped to a slab (irregular edge -- not a clean square)
# ONE pad block raised +1 at the shaft foot as a worn STEP (the approach lip, on the road-facing front).
S.box(1, 2, 1, 1, 1, 0.5, STEP)                     # worn raised step at the shaft foot (front-facing)
# a single TOPPLED companion stone lying FLAT on the plinth at the front-east edge -- a fallen sibling,
# rests on the pad top (y1), reads recumbent (lore: still ONE upright stone, this one fell long ago).
S.box(2.05, 2.05, 1, 0.95, 0.95, 0.45, FALLEN)      # toppled companion lying flat on the plinth front-east corner (not a pile)

# --- Courses 1-4 (y1-y4): the SHAFT -- 4 stacked core blocks, irregular S-taper, man-high ---
# y1 centred + rooted on the plinth.
S.box(1, 1, 1, 1, 1, 1, CORE, seam=True)            # y1 centred (rooted)
# y2 offset +1 toward FRONT-EAST (lean axis); wedge under the overhanging edge.
S.box(1.45, 1.45, 2, 0.55, 0.55, 0.45, PACKED)      # wedge under the y2 lean (grounds the offset)
S.box(1.4, 1.4, 2, 1, 1, 1, CORE2, seam=True)       # y2 offset +1 (lean axis)
# y3 BACK to centred -- the S returns (no two faces line up). Rests fully on the y2 top.
S.box(1.05, 1.05, 3, 1, 1, 1, CRACK, seam=True)     # y3 centred again (weathered course)
# y4 offset +1 on the CROSS axis (toward FRONT only) -- the S kinks the other way; wedge-supported.
S.box(1.0, 1.5, 4, 0.55, 0.5, 0.45, PACKED)         # wedge under the y4 cross-axis lean
S.box(1.0, 1.45, 4, 1, 1, 1, CORE, seam=True)       # y4 offset +1 (cross axis)

# --- Course 5 (y5, crown): ONE core block pulled to a corner, asymmetric, supported ---
# pulled to the FRONT-EAST corner over the y4 block (the inward block below is present -> supported).
S.box(1.35, 1.85, 5, 0.85, 0.85, 0.95, MOSSY)       # asymmetric crown pulled to a corner (mossy remote tell)

# remote-decay tell: a vine curtain down the shaded front face (daylight read, NOT a light).
S.box(1.6, 1.97, 2.2, 0.34, 0.05, 1.6, VINE)        # vine curtain on the shaft front face

S.label(1.4, 1.5, 5.5, "asymmetric crown pulled to a corner (never flat-topped)")
S.label(1.0, 1.5, 4.4, "irregular S-taper: y1 centred / y2 lean / y3 centred / y4 cross")
S.label(2.0, 1.5, 2.6, "remote tell: vine curtain on the shaded face (still UNLIT)")
S.label(1.0, 1.0, 1.4, "man-high single shaft (4 core, every lean wedge-supported)")
S.label(2.9, 2.0, 1.1, "fallen companion stone lying flat on the plinth (one stone, not a pile)")
S.label(0, 2, 0.5, "deliberately-irregular laid 3x3 plinth (the TENDED tell) + worn step")

out = S.svg(title="Menhir R3 (Road) -- a tended 3x3 plinth + a man-high S-leaning single shaft, still rough + UNLIT",
            size_label="3x3 plinth / 1x1 shaft * h6 * 0 lanterns (first human care -- the stone stays dark + rough)",
            label_w=352)
open("detail_svg/menhir_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/menhir_road.svg | bytes", len(out.encode()))
