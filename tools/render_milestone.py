"""Milestone R5 (Great Road) detail render -> detail_svg/milestone.svg.
The monumental rung of wnl_milestone: a three-tier stepped 9x9 dressed-stone wedding-cake
plinth (every tier ringed with an explicit STAIR skirt so the steps actually read) carrying a
tapered chiseled milliarium-COLUMN that lifts the Supplementaries way_sign board to read-from-
distance height, crowned by a grounded FOUR-LANTERN ring on full-block collars, and framed by a
flanking BANNER-MAST PAIR. A sacred-civic landmark you navigate by.

Models the deco_catalog_v2 'milestone' Great-Road massing as an iso box list. Grid: x right,
z back->front (z=0 at back), y up. Footprint centred on a 0..9 grid.

Inspiration (studied only, NOTHING copied): Roman milliarium (tapered shaft on a stepped base),
medieval market-cross / wayside-shrine (tiered lantern-crowned civic marker w/ banner masts),
MineColonies/structurize cut-stone plinth TECHNIQUE. The way_sign integration is the credit.
All geometry, proportions, taper + crown grounding original WNL. Vanilla-buildable, fully grounded.
"""
from iso_render import Iso

S = Iso(U=18)

# --- palette (literal) : DISTINCT tones, high contrast so every element reads ---------------
# Strategy (learned from render_cairn.py's contrast bar): the plinth goes COOL mid-grey with a
# DARKER stair skirt ring beneath each tread (so every step casts its own shadow band and the
# wedding-cake reads); the trim ring is the BRIGHTEST stone; the chequer + andesite accents are a
# COOL BLUE-grey (clearly not beige); and the central milliarium COLUMN is a genuinely
# DARK WARM stone -- the single darkest mass on the piece -- so it is the unmistakable focal. The
# banner masts are a COOLER slate so they frame-and-recede instead of out-shouting the column.
# the three plinth treads step DARK->LIGHT bottom-to-top so the wedding-cake reads as 3 climbing
# steps (each higher tread is brighter, like real sunlit stair nosings rising out of shadow).
# SNOW-FIX (author note "is it snowy?"): the old near-white TRIM (#e6e1d4) read as SNOW on every
# step nosing + the trim ring. Re-toned to a warm DRESSED-STONE cream/grey -- still the brightest
# element on the piece (it caps the climbing treads + the top ring), but unmistakably cut stone:
# a sandy bone with enough grey + saturation that it can never be mistaken for snow. The nosing
# lines also got a touch DARKER + thicker so they read as a chiseled stone edge, not a frost rime.
TREAD1 = "#b1ada4"   # tier-1 tread (lowest, dimmest dressed stone)
TREAD2 = "#c6c2b9"   # tier-2 tread (a clear step brighter)
TREAD3 = "#d4cfc2"   # tier-3 tread (brightest tread, nudged toward warm stone, NOT near-white)
SKIRT  = "#83807a"   # stair-skirt RISER ring under each tread (DARK -> every step casts a shadow band)
FILL_A = "#aeb0b4"   # dressed platform field (cool neutral grey, clearly cooler than the warm column)
FILL_B = "#737d88"   # polished-andesite chequer tiles (cool blue-grey, eased off saturation -> reads as STONE)
COLUMN = "#5b5750"   # chiseled milliarium COLUMN body (DARKEST warm stone = the focal, pops vs all)
COLCAP = "#6e6a61"   # column collar/cap band (a step lighter than the body so the shaft articulates)
COLHEAD= "#8b8478"   # the chiseled cap STONE at the shaft head (lighter dressed stone -> the column head reads proud above the crown collar, not lost in the dark cluster)
TRIM   = "#d8cdaf"   # stone-brick-slab trim ring + step nosings -- WARM DRESSED CREAM (brightest stone, clearly NOT snow)
NOSE   = "#c2b693"   # the chiseled nosing edge-line on each tread (a touch DARKER than TRIM -> a stone edge, not frost)
ANDB   = "#5d6772"   # polished-andesite accent band on tier-2 mid-edges (deep cool, distinct device)
MAST   = "#878d95"   # stone-brick-wall banner masts (COOL slate -> framing pair recedes vs column)
BOARD  = "#a9712f"   # supplementaries way_sign board (saturated warm oak timber -> reads off the stone)
BOARDH = "#c08a44"   # way_sign board sunlit face (lighter timber so the board catches the eye)
POST   = "#5e3f20"   # sign host nub / board battens (dark timber edge)
BANNER = "#5b6f8a"   # banner cloth (cool civic indigo-grey, original geometric device, no real arms)
BANRED = "#a8443a"   # banner chevron accent (biome-tinted dye, ORIGINAL device, no real heraldry)
SOFF   = "#7c7a74"   # stair soffits under the crown lanterns (dark -> the hung lantern reads beneath)

def step_tier(x0, z0, side, y, tread, skirt):
    """A stepped plinth tier: a DARK skirt-riser ring at y, an inset TREAD cap on top, so the
    wedding-cake step casts its own shadow band (the 'grand stair skirt on every side')."""
    # dark riser ring = the full tier block (the step's vertical face)
    S.box(x0, z0, y, side, side, 1, skirt)
    # tread cap inset 0.5 all round, sitting on the riser -> the walked nosing reads. The thin band
    # at the lip is the chiseled stone NOSING (NOSE = a notch darker than TRIM so it reads as a cut
    # stone edge, never a frost rime); the tread surface above it is the warm dressed-stone walk.
    S.box(x0+0.5, z0+0.5, y+0.92, side-1.0, side-1.0, 0.1, NOSE)     # chiseled stone nosing edge-line
    S.box(x0+0.5, z0+0.5, y+1.0, side-1.0, side-1.0, 0.18, tread)    # the tread surface (dressed stone)

# =====================================================================
# TIER 1 -- 9x9 base platform (y0). Dark stair-skirt riser + bright tread, inner andesite chequer
# field, chiseled corners. (catalog COURSE 0)
# =====================================================================
step_tier(0,0,9,0, TREAD1, SKIRT)
# inner 7x7 chequer field flush on the tread (the dressed platform reads, cool blue tiles pop)
S.box(1,1,1.2, 7,7,0.001, FILL_A)                # base field tone
for cx in range(1,8):
    for cz in range(1,8):
        if (cx+cz) % 2 == 0:
            S.box(cx,cz,1.2, 1,1,0.18, FILL_B)   # polished-andesite chequer tiles (saturated cool)
# crisp chiseled DARK corner blocks standing proud of the base skirt (anchor the silhouette)
for (cx,cz) in [(0,0),(8,0),(0,8),(8,8)]:
    S.box(cx,cz,0, 1,1,1.35, COLUMN)             # chiseled corner posts (dark -> sharp corners read)
    S.box(cx,cz,1.35, 1,1,0.18, TRIM)            # bright cap on each corner post

# =====================================================================
# TIER 2 -- 7x7 inset (y1). Stair skirt out + polished-andesite-stair accent BAND on the 4
# mid-edge cells (catalog COURSE 1).
# =====================================================================
step_tier(1,1,7,1.4, TREAD2, SKIRT)
# deep cool andesite accent band on the 4 mid-edge cells of this tier (proud so the band reads)
for (ax,az) in [(4,1),(4,7),(1,4),(7,4)]:
    S.box(ax,az,1.4, 1,1,1.0, ANDB)

# =====================================================================
# TIER 3 -- 5x5 inset (y2). Stair skirt out, bright stone-brick-slab trim RING on top.
# Three-step wedding-cake complete. (catalog COURSE 2)
# =====================================================================
step_tier(2,2,5,2.8, TREAD3, SKIRT)
S.box(2,2,3.98, 5,5,0.22, TRIM)                  # full bright slab trim ring capping the top tier

# =====================================================================
# CENTRAL TAPERED MILLIARIUM COLUMN (y4-y7) -- the focal, DARKEST warm stone.
# y4: 3x3 base ring + 4 inward corner stair-wedges faking the 3x3->1x1 taper (build_technique).
# y5: chiseled body. y6: collar band around chiseled core. y7: chiseled cap. (catalog COURSE 3-6)
# =====================================================================
S.box(3,3,4.2, 3,3,1, COLUMN, seam=True)         # y4 3x3 base ring of the column (dark)
# 4 inward corner stair-wedges keying 3x3 -> 1x1 (the dressed taper; small boxes climbing inward)
for (sx,sz) in [(3,3),(5,3),(3,5),(5,5)]:
    S.box(sx,sz,5.2, 1,1,0.55, COLCAP)           # corner taper wedge (lighter band -> the taper reads)
S.box(4,4,5.2, 1,1,1, COLUMN)                    # y5 dressed shaft (chiseled, dark)
S.box(3.82,3.82,6.2, 1.36,1.36,0.95, COLCAP)     # y6 collar band (proud, lighter -> a dressed band)
S.box(4,4,6.2, 1,1,1, COLUMN)                    # chiseled core inside the collar
# y7 chiseled cap = head of the shaft. Lighter dressed stone + a thin bright nosing so the column
# HEAD reads proud and clear ABOVE the dark crown-collar cluster (the focal milliarium tip, lit).
S.box(4,4,7.15, 1,1,0.9, COLHEAD)               # y7 dressed chiseled cap (catches light, reads as the column head)
S.box(4.05,4.05,8.04, 0.9,0.9,0.08, TRIM)       # bright chiseled nosing on the cap (a crisp dressed top edge)

# =====================================================================
# LANTERN CROWN (y6 collar + soffits) -- four full-block collar blocks ringing the column head
# (the grounded load path), each with a stair soffit + a hanging lantern beneath. (catalog COURSE 6)
# =====================================================================
for (cx,cz) in [(3,4),(5,4),(4,3),(4,5)]:        # 4 collar blocks flush on the 4 sides of the head
    S.box(cx,cz,6.2, 1,1,1, COLCAP)              # full-block collar (grounded support, mid tone)
    S.box(cx+0.18,cz+0.18,7.2, 0.64,0.64,0.22, SOFF)  # dark stair soffit -> the hung lantern reads

# =====================================================================
# HOST + WAY_SIGN (y8) -- stone-brick-wall host on the column cap carrying the Supplementaries
# way_sign board. Two arrow boards (toward settlement + back-the-way). (catalog COURSE 7)
# =====================================================================
S.box(4.3,4.3,8.1, 0.4,0.4,1.05, POST)           # slim host post on the cap (dark timber neck)
# the carved way_sign board cantilevers off the post -> a warm timber plaque w/ a sunlit face
S.box(3.85,4.74,8.5, 1.3,0.2,0.7, BOARD)         # main arrow board (faces front/down-road)
S.box(3.85,4.74,8.5, 1.3,0.06,0.7, BOARDH)       # sunlit batten strip on the board front (catches eye)
S.box(3.85,4.74,8.42, 1.3,0.2,0.08, POST)        # board lower batten (timber edge read)
S.box(3.78,3.85,8.5, 0.2,1.0,0.7, BOARD)         # second board (back-the-way arrow)
S.box(3.78,3.85,8.42, 0.2,1.0,0.08, POST)        # its lower batten

# =====================================================================
# BANNER MAST PAIR -- two stone-brick-wall masts on OPPOSITE y2-tier corners (the screen-left and
# screen-right extremes) so they FRAME the column symmetrically without occluding the crown. Each
# is topped with an original-device banner hung on the OUTWARD face. (catalog BANNER/TORCH MASTS)
# Left mast at (2,5.5)->screenX -3.5 ; right mast at (5.5,2)->screenX +3.5. Both at the 5x5 tier.
# =====================================================================
MAST_POS = [(2.0,5.5, 0,+1), (5.5,2.0, +1,0)]    # (x,z, banner dx-offset dir, banner dz-offset dir)
for (mx,mz,bdx,bdz) in MAST_POS:
    S.box(mx,mz,3.0, 0.7,0.7,4.6, MAST, seam=True)   # slim stone-brick-wall mast (cool slate, grounded on tier 3)
    S.box(mx-0.1,mz-0.1,7.6, 0.9,0.9,0.32, COLCAP)   # a dressed cap stone on the mast head
    # banner cloth hangs off the OUTWARD face (toward the road / screen edge), chevron-notch device
    bx = mx + (0.7 if bdx>0 else 0.02) ; bz = mz + (0.7 if bdz>0 else 0.02)
    bw = 0.12 if bdx>0 else 0.6 ; bd = 0.12 if bdz>0 else 0.6   # thin in the hang direction
    S.box(bx,bz,7.0, bw,bd,1.9, BANNER)              # banner cloth body
    S.box(bx,bz,7.55, bw,bd,0.65, BANRED)            # original chevron device band (no real arms)

# =====================================================================
# SATELLITE PROPS -- a boundary stone + a low hitching-post pair at the step foot (variation).
# =====================================================================
S.box(-2,7,0, 1,1,1.3, COLUMN)                   # chiseled boundary stone (1-2 cells out, dark)
S.box(-2,7,1.3, 1,1,0.3, TRIM)                   # its bright slab cap
S.box(10,2,0, 0.85,0.85,0.9, MAST)               # hitching post stub at the step foot (right)
S.box(10,4,0, 0.85,0.85,0.9, MAST)               # hitching post stub (right, second)

# =====================================================================
# ACCENTS -- the four-lantern crown, banner-mast finials, the daylit way_sign sky-glow.
# =====================================================================
S.accent(3.5,4.5,7.5, "glow", r=2.5)             # crown lantern - left
S.accent(5.5,4.5,7.5, "glow", r=2.5)             # crown lantern - right
S.accent(4.5,3.5,7.5, "glow", r=2.5)             # crown lantern - back
S.accent(4.5,5.5,7.5, "glow", r=2.5)             # crown lantern - front
S.accent(2.35,5.85,3.2, "glow", r=2.0)           # base-lamp at the left banner-mast foot
S.accent(2.35,5.85,11.9, "finial")               # left banner-mast finial
S.accent(5.85,2.35,11.9, "finial")               # right banner-mast finial
S.accent(4.3,4.5,9.6,  "glow", "#eafff8", r=2.3) # the lifted way_sign reads in daylight (sky glow)

# =====================================================================
# CALLOUT LABELS
# =====================================================================
S.label(4.3,4.7,9.2, "Supplementaries way_sign — two-way arrow board")
S.label(4.5,4.5,7.2, "grounded four-lantern crown (full-block collar)")
S.label(4.5,4.5,5.5, "tapered chiseled milliarium column (focal)")
S.label(5.85,2.35,10.5, "flanking banner masts — original chevron device")
S.label(8,8,0, "three-tier 9×9 stepped wedding-cake plinth (stair skirts)")

out = S.svg(title="Milestone R5 (Great Road) — tiered milliarium-column marker, lantern crown + banner masts",
            size_label="9×9 monument precinct · h14 (a landmark you navigate by from down the avenue)")
open("detail_svg/milestone.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/milestone.svg | bytes", len(out.encode()))
