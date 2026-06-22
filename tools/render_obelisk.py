"""Obelisk R5 (Great Road) detail render -> detail_svg/obelisk.svg.
A capital civic monument-column whose HERO is a single soaring TAPERING MONOLITH:
a clean stepped plinth carries a battered (visibly narrowing) chiseled shaft that rises far
above the base and terminates in a true 4-sided PYRAMIDION (a stepped pointed pyramid cap),
end-rod spark at the very tip. The base is deliberately SLIM + simplified and the surrounding
clutter cut right back so the soaring needle unmistakably dominates the silhouette.

Author note (2026-06-21): the prior build "read as a monument but not OBELISK enough" — the
needle was too short/stubby on a wide 15x15 four-tier plinth crowded with attendant mini-obelisks
and banners. FIX: the central needle now DOMINATES — much TALLER, more SLENDER, clearly battered
(tapering) up to a pronounced 4-sided pyramidion; the plinth is slimmed to a clean 3-step base and
the attendants + most banners are cut so the lone monolith is the hero. Egyptian/Roman obelisk
proportions: a tall thin shaft on a clean stepped base.

Models the deco_catalog_v2 'obelisk' Great Road tier as a box list. Conventions copied from
render_gatehouse.py / render_plaza.py / render_harbour.py: named literal palette; LIGHT dressed
shaft stands PROUD vs a darker plinth so the column reads; lanterns via accents; callout labels;
size_label. Inspiration (FORM/SCALE/TECHNIQUE only, never copied; credited in CREDITS.md):
the Egyptian/Roman civic obelisk (battered shaft + pointed pyramidion), the honorific column +
medieval wayside-cross tradition. All geometry is original WNL work, vanilla blocks only.
"""
from iso_render import Iso

S = Iso(U=10)

# palette (literal) -- engineered for CONTRAST on a clear luminance ladder so no two adjacent
# faces blend. The hero shaft is the LIGHTEST dressed stone so it reads tall against a darker,
# cooler plinth; the pyramidion cap brightens once more at the apex; one warm banner accent.
# Ladder (dark->light): ANDE < PLINTH < CORBEL < SPINE < BRICK < COLLAR < CHIS < SHAFT < CAPLT.
PLINTH = "#7c7669"   # smooth-stone ceremonial step mass (warm-grey, anchors the base dark)
ANDE   = "#65696f"   # polished andesite platform band (coolest/darkest masonry -> reads as a band)
CHIS   = "#c9c2b2"   # chiseled-stone-brick rings / borders / corners (clean light band)
SHAFT  = "#ece7da"   # shaft body / smooth-stone faces (near-white dressed stone -> reads tall)
SPINE  = "#c4bba4"   # flute-spine chiseled centre column (carved read, distinct from SHAFT + CHIS)
BRICK  = "#a8a293"   # stone-brick courses (mid band on the shaft, clearly below CHIS)
CORBEL = "#8f897b"   # flared corbel shoulder + crown-collar stairs -- DARK so the flares read
                     # as a shadowed element stepping out of the pale shaft above/below
COLLAR = "#b3ac97"   # chiseled ring under each corbel flare (mid, separates flare from shaft)
CAPLT  = "#f4efe2"   # bright dressed pyramidion stone (brightest -> the lit apex pops)
WALLP  = "#928c7f"   # stone-brick wall posts (corner beacon posts)
SLATE  = "#3c3843"   # hooded slab caps over the corner beacons (deep cool, max lantern contrast)
BANNER = "#d4b25f"   # approach banner cloth (saturated warm gold -- the one warm accent)
POST   = "#6f5535"   # banner timber pole
LANT   = "#a7eee6"   # sea-lantern beacon-core block (vivid cyan -> separates from warm shaft by hue)

# ---------------------------------------------------------------------------
# Centre column = the 1-wide cell at (x=6, z=6). The whole monument is built much
# slimmer than before: a clean 3-step plinth (11 -> 7 -> 5) so the SHAFT dominates.
# Approach/front face = the high-z (south) side.
CX, CZ = 6, 6          # shaft centre cell origin (1x1)

# === SLIM THREE-STEP CEREMONIAL PLINTH (L0..L2) ============================
# Cut from the old four-tier 15x15 mass: a clean, low stepped base whose only job is to
# seat the soaring shaft. Each step is a full ring resting on the solid course below.
# L0 11x11 grand step -- the broad ground pediment the great road clears past
S.box(1,1,0, 11,11,1, PLINTH)
S.box(1,1,0, 11,1,1, CHIS); S.box(1,11,0, 11,1,1, CHIS)   # chiseled outward-stair skirt (N/S edges)
S.box(1,1,0, 1,11,1, CHIS); S.box(11,1,0, 1,11,1, CHIS)   # E/W edges
# L1 7x7 step -- polished andesite platform, chiseled border
S.box(3,3,1, 7,7,1, ANDE)
S.box(3,3,1, 7,1,1, CHIS); S.box(3,9,1, 7,1,1, CHIS)
S.box(3,3,1, 1,7,1, CHIS); S.box(9,3,1, 1,7,1, CHIS)
# L2 5x5 top step -- smooth-stone platform, chiseled border (the shaft springs from here)
S.box(4,4,2, 5,5,1, CHIS)
S.box(5,5,2, 3,3,1, SHAFT)

# === BATTERED 3x3 SHAFT BASE + LOWER SHAFT (L3..L7) ========================
# A short, heavy battered foot so the tall needle reads load-bearing -- but kept LOW
# (5 courses, not the old sprawling block) so it is clearly a plinth-for-a-needle, not
# a tower in its own right. Light SHAFT faces, darker flute-SPINE centre, brick corners.
# L3 battered buttress base -- corners lean IN (BRICK quoins), cardinal cross chiseled
S.box(5,5,3, 3,3,1, BRICK)
S.box(6,5,3, 1,3,1, CHIS); S.box(5,6,3, 3,1,1, CHIS)      # lit chiseled cardinal cross
# L4-L7 thick 3x3 lower shaft (4 courses) -- flute-spine centre running continuously up
for ly in (4,5,6,7):
    S.box(5,5,ly, 3,3,1, SHAFT, seam=True)     # full 3x3 face mass (light)
    S.box(6,5,ly, 1,3,1, SPINE)                # flute-spine column (N-S faces centre)
    S.box(5,6,ly, 3,1,1, SPINE)                # flute-spine column (E-W faces centre)
    S.box(5,5,ly, 1,1,1, BRICK); S.box(7,5,ly, 1,1,1, BRICK)   # brick corners
    S.box(5,7,ly, 1,1,1, BRICK); S.box(7,7,ly, 1,1,1, BRICK)

# === CORBEL SHOULDER (L8) -> shaft "shoulders" then steps IN to the needle =====
# A darker CORBEL apron (steps OUT past the 3x3 shaft) over a lighter COLLAR ring, so the
# shoulder reads as a shadowed overhang -- the springing line of the tall needle above.
S.box(4,4,8, 5,5,1, CORBEL)             # flared 5x5 corbel apron (dark -> shadowed step-out)
S.box(5,5,8, 3,3,1, COLLAR, seam=True)  # lit chiseled collar ring beneath the flare
S.box(6,6,8, 1,1,1, CHIS)               # bright keyed centre block the needle springs from

# === SOARING BATTERED NEEDLE (L9..L30, 22 courses) =========================
# THE HERO. The shaft now rises ~22 courses (was 13) and visibly TAPERS: it starts a hair
# under 1 block and battered-narrows toward the tip, drawn by shrinking each course's width
# and re-centring it on the shaft axis. The %3 flute map keys the eye to height as it climbs;
# a single COLLAR girdle string-course at mid-height breaks the long run. The taper +
# the great height are what make it OBELISK -- a thin monolith, not a stubby spike.
NEEDLE_BASE = 9
NEEDLE_TOP  = 30                      # last shaft course before the pyramidion
NC = NEEDLE_TOP - NEEDLE_BASE + 1     # 22 courses
NEEDLE_BAND = NEEDLE_BASE + NC // 2   # mid-needle girdle string-course
cap_w = None
for k in range(NC):
    ly = NEEDLE_BASE + k
    t = k / (NC - 1)                  # 0 at foot -> 1 at top
    # battered taper: width eases from ~0.98 at the foot to ~0.50 at the tip; re-centre on axis.
    # a mild ease (t**1.15) keeps the foot near-full then narrows more visibly up high, so the
    # batter reads as a true entasis-less obelisk taper rather than a uniform cone.
    w = 0.98 - 0.48 * (t ** 1.15)
    off = (1.0 - w) / 2.0
    bx, bz = CX + off, CZ + off
    cap_w = w                         # remember the topmost shaft width for the pyramidion base
    if ly == NEEDLE_BAND:
        # carved girdle string-course (a touch proud + darker -> a shadow line keying the height)
        S.box(bx - 0.08, bz - 0.08, ly, w + 0.16, w + 0.16, 1, COLLAR, seam=True)
        continue
    if   k % 3 == 0: col = SPINE      # flute course
    elif k % 3 == 1: col = SHAFT
    else:            col = BRICK
    S.box(bx, bz, ly, w, w, 1, col)

# === FOUR-SIDED PYRAMIDION CAP (L31..L34) ==================================
# A REAL pointed pyramid, not a lantern box: four stepped chiseled courses, each smaller and
# re-centred over the one below, tapering to a single bright apex block. Grounded on the
# topmost shaft course. This pointed pyramidion is the unmistakable OBELISK signature.
top = NEEDLE_TOP + 1
pyr_w0 = cap_w + 0.16                 # pyramidion base just over the shaft tip (a real, crisp cap)
pyr_steps = [pyr_w0, pyr_w0*0.72, pyr_w0*0.46, pyr_w0*0.22]
for i, pw in enumerate(pyr_steps):
    po = (1.0 - pw) / 2.0
    col = CAPLT if i >= len(pyr_steps) - 2 else SHAFT   # brighten toward the apex
    S.box(CX + po, CZ + po, top + i, pw, pw, 1, col)
APEX_Y = top + len(pyr_steps)         # y of the very tip (for the finial accent)

# === FOUR CORNER SEA-LANTERN BEACONS (on L1, hooded) -- the ONLY satellites ==
# Kept (the spec's four corner beacons) but that's ALL: the attendant mini-obelisks are cut
# and the banners trimmed to a single discreet pair, so nothing competes with the needle.
beacon_posts = [(3,3),(9,3),(3,9),(9,9)]
for (bx,bz) in beacon_posts:
    S.box(bx,bz,2, 1,1,2, WALLP)         # stone-brick wall post rising off the L1 platform
    S.box(bx,bz,4, 1,1,1, LANT)          # sea-lantern beacon
    S.box(bx,bz,5, 1,1,1, SLATE)         # hooded dark slab cap (flush -> sorts ON TOP of lantern)
    S.box(bx+0.15,bz+0.15,5, 1,1,0.5, SLATE)  # front eave lip (overhang read)

# === A DISCREET APPROACH-BANNER PAIR (front face, on L1 posts) =============
# One low pair only -- a whisper of ceremony at the foot, never tall enough to crowd the shaft.
for bx in (4,8):
    S.box(bx,9,2, 1,1,2, WALLP)      # short wall post on the approach (front, high-z) edge
    S.box(bx,9.05,2, 1,1,2, BANNER)  # short banner cloth (warm gold)
    S.box(bx,9,4, 1,1,1, POST)       # banner pole crown

# ============================ ACCENTS (lights / finial) ====================
# pyramidion apex spark -- a single end-rod finial at the very tip (grounded on the cap apex).
S.accent(CX+0.5, CZ+0.5, APEX_Y, "finial")
# four corner beacons (glow sits between lantern y4 and hood y5)
for (bx,bz) in beacon_posts:
    S.accent(bx+0.5, bz+0.5, 4.5, "glow", "#dff6ef", r=2.6)
# warm banner dots (cloth highlight)
for bx in (4,8):
    S.accent(bx+0.5, 9.5, 3.4, "dot", BANNER, r=1.8)

# ============================ CALLOUT LABELS ===============================
S.label(CX+0.5, CZ+0.5, APEX_Y-1, "four-sided pyramidion cap + end-rod finial (real pointed tip)")
S.label(CX+0.5, CZ+0.5, 20, "soaring BATTERED needle — visibly tapers as it climbs (the hero)")
S.label(7.5, 6, 8.5, "flared 5x5 corbel shoulder — the needle springs from here")
S.label(7.5, 6, 5.5, "low battered 3x3 buttressed foot + flute-spine")
S.label(9, 9, 4.6, "four corner sea-lantern beacons (hooded)")
S.label(8, 9, 3, "discreet approach banners")
S.label(2, 9, 0, "slim 3-step ceremonial plinth (11→7→5)")

out = S.svg(title="Obelisk R5 (Great Road) — soaring tapering monolith: slim stepped plinth, battered flute needle + four-sided pyramidion cap",
            size_label="11×11 plinth · h35 — a tall thin monolith that reads OBELISK from kilometres out",
            label_w=344)
open("detail_svg/obelisk.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/obelisk.svg | bytes", len(out.encode()))
