"""dock_shack detail render -> detail_svg/dock_shack.svg.

REALITY PASS (author: "needs a reality pass"). Re-scoped back to what the spec actually
asks for: a TINY fisher's shack that sits at the LAND end of a pier -- the lived-in plank hut,
NOT a hall, NOT a stone tower, NOT a chapel, NOT a cargo gantry (those belong to wnl_harbour /
wnl_pier). See deco_catalog_v2.json id "dock_shack": "a SATELLITE deco piece placed ON/beside
the wnl_pier deck... barrels, hung drying-net, a personal hand-winch, a fisher's saint-niche."

What a fisher would actually build here, and what this render now shows:
  * a grounded STONE-and-PLANK footing on the bank, with driven LOG PILINGS carrying the
    water-side half of the hut down to the riverbed (nothing floats),
  * sensible 1-block-thick PLANK walls on a timber frame (corner posts proud),
  * a real DOOR facing the road approach + a shuttered WINDOW on the side,
  * a real pitched GABLE roof (spruce stairs, ridge beam, eaves overhang),
  * the signature PERSONAL hand-winch (a small mast + short boom + drum, hung net) -- one-fisher
    scale, braced back to the gable, NOT a harbour crane,
  * a hung drying-NET on a real fence rail, barrels + a composter, a small wall saint-NICHE,
  * a grounded lantern + a smoking chimney = a tended, lived-in shack.

PERSPECTIVE: clean single iso massing read left-to-right -- bank footing + door, then the hut
block, then the water-side stilts + winch over the water. Nothing reads as a muddled blob.

Original WNL composition, vanilla blocks only. FORM inspiration (studied, never copied; author
knows the devs): coastal stilt fisher-huts / net-lofts (Tidal Towns, Towns & Towers wharf vocab),
scale calibrated against MineColonies. Credited in CREDITS.md.
Grid: x right, z back(0; landward)->front(water), y up.
"""
from iso_render import Iso

S = Iso(U=20)

# --- palette (literal) -- warm worn timber hut over cool water; everything reads apart --------
WATER  = "#3f7a98"   # open water under the stilts (cool blue, pushes the warm hut off it)
WET    = "#2c4f4d"   # dark wet pile-collar at the waterline (the 'tell' the build sits in water)
PILE   = "#5a4026"   # driven oak-log pilings under the water-side floor (dark warm timber)
STONE  = "#8d8880"   # stone-brick bank footing (cool grey, grounds the landward half)
STONED = "#6f6b63"   # darker stone plinth course (the footing reads as built stone, not a slab)
SILL   = "#caa766"   # spruce-plank floor / sill platform (light warm board)
FRAME  = "#4a371d"   # stripped-dark-oak corner posts + bressumer (dark warm timber, stands proud)
WALL   = "#b98f51"   # spruce-plank wall infill (mid warm board, contrasts FRAME + STONE)
WALLD  = "#9a743f"   # shaded plank course / lower wall band (a 2-tone wall read)
DOOR   = "#3a2c1b"   # dark recessed doorway (near-black, punches a real opening)
WIN    = "#2b3138"   # shuttered window reveal (dark recess)
GLASS  = "#67aab8"   # a little glass in the window (cool jewel)
SHUT   = "#7a5526"   # window shutter / sill timber (mid warm)
ROOF   = "#3c352c"   # spruce-stair pitched roof (dark, strong silhouette)
ROOFD  = "#2c2720"   # shaded roof slope (the far pitch reads darker)
RIDGE  = "#5d564c"   # ridge beam course (lighter, picks the ridge line off the dark pitch)
MAST   = "#e0c489"   # stripped-oak winch mast + boom (palest timber -> the winch pops)
DRUM   = "#9c7338"   # winch drum / stay (darker amber, the brace reads)
NET    = "#7a5526"   # hung oak-trapdoor drying net (warm brown)
BARREL = "#7d5a30"   # barrel / composter clutter
HOOP   = "#caa15a"   # barrel hoop / saint-niche bell accent
NICHE  = "#a8946a"   # small fisher's saint-niche dressed stone (warm, set in the gable)
CHIM   = "#79746c"   # small cobble chimney flue
GROUND = "#6f5d3e"   # trodden landward earth at the door

# ============================================================================================
# 0) WATER + WET 'TELL' -- the hut meets the water on its front half; a thin water plate reads
#    under the stilts so the build clearly sits AT the water's edge (front = high z).
# ============================================================================================
S.box(-1, 5, 0, 7, 4, 1, WATER)                      # water plate under the water-side stilts

# ============================================================================================
# 1) GROUNDING -- landward STONE footing + water-side LOG PILINGS (nothing floats) ------------
# the bank (z0..4) gets a low stone-brick footing built up from the ground; the water side
# (z5..8) is carried on four driven log pilings down to the riverbed, collared at the waterline.
# ============================================================================================
# landward stone footing (two courses so it reads as built stone, grounded on the bank)
S.box(0, 0, 0, 5, 5, 1, STONED, seam=True)           # plinth course on the bank
S.box(0, 0, 1, 5, 5, 1, STONE, seam=True)            # footing top course (the floor seats on this)
S.box(-1, 1, 0, 1, 3, 1, GROUND)                     # trodden earth at the landward door approach
# water-side driven LOG PILINGS: six posts (two rows) from the riverbed up to floor level so the
# whole water-side deck (z5..8) is carried -> grounded, nothing floats.
for (px, pz) in [(0, 5), (4, 5), (0, 8), (4, 8)]:
    S.box(px, pz, 0, 1, 1, 2, PILE, seam=True)        # corner piling shaft up to under the deck (y0->2)
    S.box(px, pz, 0, 1, 1, 1, WET)                    # dark wet collar at the waterline
S.box(2, 8, 0, 1, 1, 2, PILE, seam=True)             # mid seaward piling under the deck front edge
S.box(2, 8, 0, 1, 1, 1, WET)                         # its wet collar
# cap-beams between the pilings (a real stilt frame, not single sticks) carrying the deck
S.box(0, 8, 1, 5, 1, 1, PILE)                         # seaward pile cap-beam carrying the deck front edge
S.box(0, 5, 1, 1, 4, 1, PILE)                         # west pile cap-beam (z5..8)
S.box(4, 5, 1, 1, 4, 1, PILE)                         # east pile cap-beam (z5..8)

# ============================================================================================
# 2) FLOOR / SILL PLATFORM -- a 5x9 plank deck spanning bank footing -> water-side pilings ----
# ============================================================================================
S.box(0, 0, 2, 5, 9, 1, SILL, seam=True)             # spruce-plank floor, lands on stone + pilings
S.box(0, 4, 2, 5, 1, 1, FRAME)                        # bressumer sill-beam at the bank/water joint

# ============================================================================================
# 3) THE HUT -- a 5x5 fully-enclosed plank cabin on the landward half (z0..4), timber-framed.
# walls are 1 thick on a frame: dark corner posts stand proud, light plank infill between. The
# cabin is CLOSED on all four sides (a cosy hut); the working gear lives OUT on the open water
# deck in FRONT of it (z5..8) where it reads cleanly against the water -- not in a dark cavity.
# The DOOR + WINDOW sit on the VISIBLE east (x4) + water (z4) faces so the camera reads them.
# ============================================================================================
HY = 3                                               # wall foot course
# corner posts (proud dark timber), full wall height (y3..6 = 3 high walls)
for (cx, cz) in [(0, 0), (4, 0), (0, 4), (4, 4)]:
    S.box(cx, cz, HY, 1, 1, 3, FRAME, seam=True)      # corner posts y3..6
# plank walls between the posts (all four sides closed); a darker lower band = 2-tone plank read
S.box(1, 0, HY, 3, 1, 1, WALLD)                       # back (landward) wall lower band (z0)
S.box(1, 0, HY + 1, 3, 1, 2, WALL, seam=True)         # back wall upper
S.box(0, 1, HY, 1, 3, 1, WALLD)                       # west (far) wall lower band
S.box(0, 1, HY + 1, 1, 3, 2, WALL, seam=True)         # west wall upper
S.box(4, 1, HY, 1, 3, 1, WALLD)                       # east (near, visible) wall lower band
S.box(4, 1, HY + 1, 1, 3, 2, WALL, seam=True)         # east wall upper
S.box(1, 4, HY, 3, 1, 1, WALLD)                       # water (near, visible) wall lower band (z4)
S.box(1, 4, HY + 1, 3, 1, 2, WALL, seam=True)         # water wall upper
# bressumer / wall-plate capping the walls (the eave line the roof sits on)
S.box(0, 0, HY + 3, 5, 5, 1, FRAME)                   # top plate ring at y6 (the roof seats here)

# DOOR -- a real plank door in the WATER (z4) wall, facing the deck + the pier approach.
# It is on a viewer-visible face, framed by a timber surround, with a stone doorstep.
S.box(2, 4, HY, 1, 1, 2, DOOR)                        # dark recessed doorway opening (y3..4)
S.box(2, 4.15, HY, 1, 0.3, 2, SHUT)                   # door leaf (proud, reads as a hung door)
S.box(1, 4, HY + 2, 3, 1, 1, FRAME)                   # door lintel beam over the opening
S.box(2, 5, 2, 1, 1, 1, STONED)                       # stone doorstep on the deck below the door

# WINDOW -- a shuttered glazed window in the EAST (x4) side wall (a viewer-visible face)
S.box(4, 2, HY + 1, 1, 1, 1, WIN)                     # window reveal (dark recess)
S.box(4.15, 2, HY + 1, 0.3, 1, 1, GLASS)             # a little glass in the reveal (proud)
S.box(4.15, 1.6, HY + 1, 0.3, 0.4, 1, SHUT)          # north shutter leaf (open, reads as a shutter)
S.box(4.15, 3.0, HY + 1, 0.3, 0.4, 1, SHUT)          # south shutter leaf
S.box(4, 1.8, HY, 1, 1.4, 1, SHUT)                    # window sill timber under the reveal

# small fisher's saint-NICHE set into the WATER (z4) wall beside the door (visible sub-feature)
S.box(3.4, 4, HY + 1, 0.6, 0.3, 1, NICHE)            # dressed-stone niche surround (proud of plank)

# ============================================================================================
# 4) ROOF -- a real PITCHED GABLE roof over the 5x5 hut. RIDGE RUNS ALONG Z (front->back) so a
#    clean gable TRIANGLE faces the viewer; pitches fall to the x-eaves. Overhang only on the
#    eave (x) sides + a small barge over the gable ends -> the walls stay readable below.
# the near (east) slope reads light(ROOF), the far (west) slope darker(ROOFD) for a clean gable.
# ============================================================================================
# eave course: a SHALLOW overhang. The near (viewer-facing) eaves -- the east x-side and the
# water z-end -- are pulled BACK flush to the wall so they do NOT shadow the door/window below;
# the far/back eaves keep a 1-block overhang. This keeps the front faces readable.
S.box(-1, -1, HY + 4, 6.4, 6.4, 1, ROOF)             # eave course y7 (overhang on far sides only)
# climbing pitches toward the ridge -- x narrows, z stays full so the slopes read as long planes
S.box(0, -1, HY + 5, 4.6, 6.4, 1, ROOFD)             # course y8 (far slope shading)
S.box(1, -1, HY + 6, 3, 6.4, 1, ROOF)                # course y9 (near slope, lighter)
S.box(2, -1, HY + 7, 1, 6.4, 1, RIDGE)               # ridge beam y10 (runs front->back over the gable)
# gable barge-boards close the triangle at the two ends (back z0 landward + water z4 ends),
# stepping in with the pitch so each gable reads as a real filled triangle (not open sky)
S.box(0, -0.4, HY + 4, 5, 0.4, 1, FRAME)             # back gable barge eave (z0 end)
S.box(1, -0.3, HY + 5, 3, 0.3, 1, WALL)              # back gable infill course 1
S.box(2, -0.3, HY + 6, 1, 0.3, 1, WALL)              # back gable apex infill
S.box(0, 5.0, HY + 4, 5, 0.4, 1, FRAME)              # water gable barge eave (z4 end)
S.box(1, 5.0, HY + 5, 3, 0.3, 1, WALL)              # water gable infill course 1
S.box(2, 5.0, HY + 6, 1, 0.3, 1, WALL)              # water gable apex infill
# small cobble CHIMNEY breaking the FAR (west) slope near the landward gable (smoking hearth).
# it springs from the wall plate and rises just proud of the ridge = grounded, not floating.
S.box(0, 0.5, HY + 3, 1, 1, 4, CHIM, seam=True)      # chimney flue up the west slope (y6->9)
S.box(0, 0.5, HY + 7, 1, 1, 1, STONE)                # flue head cap (campfire smoke escapes here)

# ============================================================================================
# 5) PERSONAL HAND-WINCH -- one-fisher net-hoist on the EAST half of the open deck (clean, alone)
# a TALL slim mast rises off the deck clear of all clutter; a slim boom cantilevers seaward; a
# drum sits at the foot; a stay ties the boom-tip back+down to the mast; a net hangs on the boom.
# everything stands on the deck (y3, carried by the pilings) -> grounded, nothing floats.
# ============================================================================================
MX = 4                                               # winch on the east deck edge (x4)
# TALL mast (slim 0.7-wide so it reads as a pole, not a wall block), rising clear above the clutter
S.box(MX + 0.15, 6, 3, 0.7, 0.7, 5, MAST, seam=True) # winch MAST y3..7 (taller than the deck gear)
S.box(MX + 0.1, 5.9, 4, 0.8, 0.8, 1, DRUM)           # winch DRUM (chain-spool) low on the mast
# slim BOOM cantilevering seaward from the mast head (z6 -> z8), thin so it reads as an arm
S.box(MX + 0.15, 6.5, 7, 0.7, 2.5, 0.7, MAST)        # the boom arm projecting out over the water
# diagonal STAY: boom-tip -> back+down to the mast foot (two stepped blocks = a real brace)
S.box(MX + 0.2, 7.5, 6, 0.5, 0.5, 1, DRUM)           # stay upper (under the boom tip)
S.box(MX + 0.2, 6.5, 5, 0.5, 0.5, 1, DRUM)           # stay lower (down to the mast foot)
# hung drying NET on a chain from the boom tip (hangs straight down -> not floating)
S.box(MX + 0.25, 8.3, 4.5, 0.2, 0.2, 2.5, FRAME)     # the hoist chain dropping from the boom tip
S.box(MX - 0.5, 8, 3, 2, 1, 1.5, NET)                # the drying net hung below the boom tip

# ============================================================================================
# 6) CLUTTER -- barrels (the catch) + composter on the WEST half of the deck, all on y3 ---------
#    kept on the opposite side from the winch so neither blob obscures the other.
# ============================================================================================
S.box(0, 6, 3, 1, 1, 1, BARREL)                      # barrel (catch) on the deck
S.box(0, 6, 4, 1, 1, 1, BARREL)                      # stacked barrel (taller heap read)
S.box(0, 6, 5, 1, 1, 0.15, HOOP)                     # barrel-lid hoop accent on top
S.box(1, 6, 3, 1, 1, 1, BARREL)                      # composter beside it (bait/scraps)
S.box(0, 7, 3, 1, 1, 1, NET)                         # a coiled net / crab-pot heap on the deck edge

# ============================================================================================
# 7) ACCENTS -- a grounded lantern over the deck, the chimney smoke-glow, the niche candle ------
# ============================================================================================
S.accent(4.5, 8.5, 7.4, "glow", r=2.0)               # lantern hung at the winch boom tip over the water
S.accent(3.5, 4.7, 6.2, "glow", "#ffe6a8", r=1.6)    # lantern by the door (over the deck, grounded read)
S.accent(0.4, 1.0, 11.0, "glow", "#ff9d57", r=2.0)   # chimney fire-glow (warm smoke)
S.accent(3.7, 4.7, 7.2, "glow", "#ffd27a", r=1.4)    # fisher's saint-niche candle (warm devotion)
S.accent(4.5, 8.5, 2.8, "dot", "#7a5526", r=1.4)     # crab-pot / net-float read below the hung net

# --- callout labels ---
S.label(2.0, 0.0, 11, "pitched spruce-stair gable roof — ridge beam + smoking chimney")
S.label(3.0, 4.0, 5, "plank-framed hut — door to the deck + shuttered window + saint-niche")
S.label(4.5, 8.0, 7, "personal hand-winch — short boom + drum + hung drying-net")
S.label(0.0, 0.0, 1, "stone bank footing — landward half grounded")
S.label(2.5, 8.0, 1, "driven log pilings carry the water-side deck (nothing floats)")

out = S.svg(title="dock_shack — a fisher's stilt shack at the pier head (grounded footing + pilings, plank walls, pitched roof, personal hand-winch)",
            size_label="~5x9 hut over the water's edge · ridge h10 · the lived-in pier hut (barrels, drying-net, saint-niche)")
open("detail_svg/dock_shack.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/dock_shack.svg | bytes", len(out.encode()))
