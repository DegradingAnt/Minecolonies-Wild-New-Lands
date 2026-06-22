"""Banner_stand PATH (floor of THIS piece's ladder) -> detail_svg/banner_stand_path.svg.
Per deco_catalog_v2.json id 'banner_stand' tier Path (footprint 2x2 footing, height 5): the humblest
rung -- ONE lashed wooden pole on a 2x2 cobble foot, standing BESIDE the path (it does NOT span it),
flying a SINGLE standing white banner (recolored at placement) that faces the road. The bare-minimum
'someone claims this'. Establishes the silhouette FAMILY (cobble foot + wooden post + ONE road-facing
banner) that every higher tier amplifies. UNLIT in the wild-but-claimed case (a bare chain hangs);
ONE hanging lantern appears only CivLevel-gated near a tended settlement -- drawn here as the
near-settlement LIT variant so the first-light idea is visible (Road is where light becomes standard).
Trail is INTENTIONALLY skipped for this piece (no settled territory to proclaim on a wild footpath),
so Path is the deliberate floor and Path->Road is engineered as a CLEARLY big jump.

Originality/inspiration (FORM/TECHNIQUE only, credited in CREDITS.md; no NBT/assets copied): a
roadside lashed-pole pennant standard -- universal wayside claim-marker folk form. Same wnl_banner_stand
data builder as render_banner_stand.py (Great Road top); the builder hashes dye/decay/lantern live."""
from iso_render import Iso

S = Iso(U=26)

# ---- palette (literal) -- WIDE-CONTRAST ladder so every material reads as itself ----------------
COBB   = "#8a8276"   # minecraft:cobblestone footing (the common pick, cool stone grey)
MOSS   = "#6f7d56"   # minecraft:mossy_cobblestone -- the back-left "lived-in" tell (saturated green)
KERB   = "#7c7468"   # cobblestone_slab worn kerb lip on the outward edges (darker -> reads dressed lip)
FOOT   = "#9a9384"   # cobblestone_wall masonry foot the wooden post stands on (lighter dressed grey)
RING   = "#5b5048"   # tripwire_hook iron tie-ring on the foot's outward face (dark iron note)
OAK    = "#6e5532"   # oak_fence lashed pole shaft (warm mid timber)
SPRUCE = "#4f4632"   # spruce_fence banner-mount cap (darker timber -> reads a distinct cap block)
BANNER = "#b14a3f"   # white_banner recolored at placement -- muted heraldic claim red (STANDING, pole-top)
BANPOLE= "#d8d2c4"   # the banner's pale staff/border edge (so the cloth reads as a banner, not a block)
CHAIN  = "#54504a"   # bare chain (hangs unlit when remote; carries the lantern when near settlement)
LANT   = "#ffd47a"   # lantern glow (CivLevel-gated FIRST hint of light; standard from Road up)

# geometry: 2x2 foot at x0-2,z0-2; the POST sits in the FRONT-RIGHT cell (x1,z1 -> high-x, high-z =
# the road-facing front). The path runs along the high-z FRONT; the banner faces ACROSS it (toward viewer).

# ============================================================================================
# L0 (y0) -- 2x2 cobble FOOTING set flush into the graded surface (the foot, NOT a plinth)
# ============================================================================================
S.box(0,0,0, 2,2,1, COBB, seam=True)              # 2x2 cobblestone foot
S.box(0,0,0, 1,1,1, MOSS)                          # back-left cell -> mossy_cobblestone (lived-in tell)
# worn kerb lip: cobblestone_slab on the two OUTWARD faces (back z0 + west x0) so the foot reads dressed
S.box(0,-0.28,1, 2,0.28,0.45, KERB)                # back kerb lip (worn slab, abuts + rests on the foot top)
S.box(-0.28,0,1, 0.28,2,0.45, KERB)               # west kerb lip (abuts the west face, rests on foot top)

# ============================================================================================
# L1 (y1) -- the POST BASE: ONE cobblestone_wall masonry foot in the front-right cell + iron tie-ring
# ============================================================================================
S.box(1.18,1.18,1, 0.64,0.64,1, FOOT, seam=True)  # stubby masonry foot (wall block -> slim rounded read)
# tripwire_hook tie-ring fixed to the foot's OUTWARD (front, high-z) face -> reads an iron lashing peg
S.box(1.3,1.84,1.35, 0.4,0.16,0.18, RING)         # iron tie-ring abutting the foot's front face (grounded on it)

# ============================================================================================
# L2-L3 (y2..3) -- the POLE: TWO stacked oak_fence (a lashed wooden post off the masonry foot)
# ============================================================================================
S.box(1.32,1.32,2, 0.36,0.36,2, OAK, seam=True)   # 2-tall oak_fence pole, rooted on the masonry foot

# ============================================================================================
# L4 (y4) -- BANNER MOUNT: spruce_fence cap + ONE STANDING white_banner facing the road
# (this is the ONLY tier using a STANDING banner; every higher tier uses WALL banners)
# ============================================================================================
S.box(1.32,1.32,4, 0.36,0.36,0.55, SPRUCE)        # spruce_fence cap (distinct dark timber, caps the oak pole)
# the standing pole-top banner: a thin cloth panel standing on the cap, FRONT face turned to the road
S.box(1.18,1.62,4.5, 0.66,0.12,1.5, BANNER)        # banner cloth (faces high-z front / the traveller)
S.box(1.46,1.6,4.5, 0.08,0.14,1.62, BANPOLE)       # pale banner staff edge (reads it as cloth-on-a-staff)

# ============================================================================================
# L4 (side) -- CivLevel-gated light: ONE chain off the oak_fence at y3 carrying ONE hanging lantern.
# Drawn as the LIT near-settlement variant (the wild-but-claimed case hangs the chain BARE/unlit).
# GROUNDED: the chain hangs from the pole it is lashed to; the lantern hangs directly under it.
# ============================================================================================
S.box(1.86,1.5,3.5, 0.09,0.09,0.9, CHAIN)          # chain off the pole's east face (abuts the oak_fence)
S.accent(1.9, 1.55, 3.25, "glow", LANT, r=2.3)     # hanging lantern under the chain (FIRST light, gated)

# ============================================================================================
# CALLOUT LABELS
# ============================================================================================
S.label(1.3, 1.6, 5.6, "ONE standing white_banner facing the road (only tier with a STANDING banner)")
S.label(1.5, 1.4, 3.0, "lashed oak_fence pole on a cobblestone_wall foot + iron tie-ring (tripwire_hook)")
S.label(1.95, 1.55, 3.0, "CivLevel-gated lantern on a chain (bare unlit chain when the claim is remote)")
S.label(0.0, 0.4, 1.0, "2x2 cobble footing (mossy back corner) + worn slab kerb lip -- stands BESIDE the path")

out = S.svg(title="Banner_stand R-Path -- humble beside-road claim pole: cobble foot + lashed post + ONE standing banner",
            size_label="2x2 foot * h5 * 0-1 lantern (the floor -- a single pennant standard, stands beside the path)",
            label_w=352)
open("detail_svg/banner_stand_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/banner_stand_path.svg | bytes", len(out.encode()))
