"""dock_shack HIGHWAY (R4) -> detail_svg/dock_shack_highway.svg.
Per deco_catalog_v2.json id 'dock_shack' tier 'Highway -- two-storey fish-house' (footprint 7x8 +
a 1-block stone plinth skirt, height 12): the BIG non-linear leap below the Great-Road hall (Road
7x7x8 -> 7x8x12) -- the whole ground floor becomes MASONRY, it gains a genuine JETTIED (overhanging)
timber second storey on stair corbels (a vertical silhouette break), a full-height gable-integrated
HAND-WINCH, a main gable + CROSS-GABLE roof with a smoking STONE CHIMNEY + dormer, a banner + sign,
and a hash-gated medieval fisher's SAINT-NICHE. A building that out-masses the big-well by reading as
a tall two-storey house. This is the rung directly under the Great-Road fisher's hall (render_dock_shack.py).
Spec massing, course by course:
  C0   a 7x8 single-course STONE-BRICK plinth lifting the house one block (civic damp-proof base, NOT
       a quay); two landward corners on cobblestone footings.
  C1   masonry ground-floor walls (stone_bricks + chiseled-brick QUOINS at the corners); a wide water-
       side LOADING opening framed by stone-brick-stairs as a flat-arch head; a spruce door landward +
       two iron-bars windows.
  C2-3 masonry to course 3, a stone-brick-slab STRING-COURSE capping the stone storey (the floor-line
       separating stone below / timber above); the working ground room (smokers, barrels, chest).
  C4   the JETTIED upper floor OVERHANGS the stone ground floor by 1 on the water side, carried on
       spruce-stairs[half=top] CORBELS jutting from the string-course + a stripped-dark-oak bressumer
       beam across the corbel tops. This jetty reads as a proper two-storey house from a distance.
  C5-6 timber upper storey (stripped-dark-oak posts + spruce-plank infill); a wide shuttered hoist-
       opening on the water gable; the net-loft inside.
  C7   the HAND-WINCH, full-height + gable-integrated: a stripped-oak-log MAST rises from the string-
       course up the gable face to the ridge; a stripped-oak-log BOOM projects 4 over the water near
       the ridge (inboard end pinned into the gable -> the winch IS the gable). Chain over boom ->
       iron-block counterweight (1x1x3) inboard + a 3x2 hoisted net (oak_trapdoor on a fence drop-
       lattice) outboard; winch drum at the boom foot.
  C8-9 ROOF -- main gable (stair pitches over the 7-span to a slab ridge at course 9) + a CROSS-GABLE
       over the water-side loading bay (a perpendicular gablet meeting the main ridge in a slab valley).
       CHIMNEY: a stone-brick 1x1 flue rising from a ground-floor smoker straight up through the land-
       ward pitch, topping at course 11 with a lit campfire flue-head = visible smoke.
  C10-11 a spruce-trapdoor DORMER shutter on the water pitch; lanterns under every eave + on the winch
       boom + on the loft-rail; a hanging-sign gantry over the loading bay; one muted (faded-blue) banner
       on the landward gable.
  SUB-FEATURE (~45%): a fisher's SAINT-NICHE in the landward gable base -- a 1-wide stone-brick-stairs
       arched recess holding 3 lit candles on a slab altar shelf + a flower-pot + a tiny chain above.
ISO READ: the JETTY overhang + the loading-bay flat-arch + the winch + cross-gable + saint-niche all
turn to the VISIBLE water FRONT (high z) + east; the chimney + banner break the landward roofline.
NON-LINEAR: a true second storey, masonry ground floor, a smoking chimney + the saint-niche all arrive
here -- a clearly bigger leap than Path->Road, one step under the monumental hall.
Original WNL build, vanilla blocks only. FORM inspiration (studied, never copied; author knows the
devs): medieval timber JETTY-HOUSES / wharf fish-houses (masonry ground floor + jettied timber upper
storey on corbels, the string-course floor-line) + medieval coastal fisher's wayside SAINT-NICHES for
safe return; Roman/medieval corbelled/stepped ARCH technique; Tidal Towns + Towns & Towers wharf vocab;
scale vs MineColonies/structurize. Credited in CREDITS.md.
Grid: x right, z back(0;landward)->front(water), y up.
"""
from iso_render import Iso

S = Iso(U=15)

# --- palette (literal) -- masonry ground floor (cool stone) + warm timber jetty above; wide ladder -
WATER  = "#3f7a98"   # open water under the jetty + winch (cool blue -> the warm hut pops off it)
WET    = "#2c4f4d"   # dark wet line at the plinth/water meeting (the 'sits at the water' tell)
PLINTH = "#6f6b63"   # stone-brick plinth course (cool grey base, grounds the whole house)
STONE  = "#8d8880"   # stone-brick ground-floor walls (cool dressed stone -> reads clearly as masonry)
STONED = "#75716a"   # shaded lower stone course (a 2-tone masonry read)
QUOIN  = "#b3ada0"   # chiseled-stone-brick QUOINS at the corners (bright dressed stone -> corners read)
STRING = "#a59f93"   # stone-brick-slab STRING-COURSE (the stone/timber floor-line, light stone band)
COBBLE = "#7c776e"   # cobblestone damp-proof footings (cool grey)
ARCH   = "#9a948a"   # stone-brick-stairs flat-arch head over the loading bay (mid stone)
DOOR   = "#3a2c1b"   # dark recessed doorway / loading-bay reveal (near-black opening)
BARS   = "#3a4048"   # iron-bars windows (dark cool metal grid)
CORBEL = "#b3ada0"   # spruce-stairs[half=top] jetty corbels (light -> the cantilever bracket reads)
BRESS  = "#3a2c1b"   # stripped-dark-oak bressumer beam across the corbels (darkest timber)
TFPOST = "#5a4026"   # stripped-dark-oak timber-frame corner posts (dark warm, the upper frame)
WALL   = "#b98f51"   # spruce-plank upper-storey infill (mid warm board -> warm timber above cool stone)
WALLD  = "#9a743f"   # shaded plank band (2-tone read)
SHUT   = "#7a5526"   # spruce-trapdoor shutters (hoist-opening + dormer)
MAST   = "#e0c489"   # stripped-oak-log winch MAST + boom + drum (palest -> the full-height winch pops)
IRON   = "#b9c0c9"   # iron-block counterweight (cool bright metal -> the honest smith weight)
CHAIN  = "#46433d"   # winch chain / tackle (dark line)
NET    = "#86603a"   # hung oak-trapdoor net (warm brown mesh)
FENCE  = "#7a5526"   # oak-fence loft-rail + net drop-lattice
ROOF   = "#46402f"   # spruce-stair roof, near pitch (warm dark -> strong silhouette)
ROOFD  = "#332e22"   # shaded far pitch / cross-gable far slope (darker)
RIDGE  = "#5d564c"   # spruce-slab ridge + valley (lighter -> ridge/valley lines read)
CHIM   = "#79746c"   # stone-brick chimney flue (cool grey stone, rises through the landward pitch)
CHIMG  = "#ff9d57"   # lit-campfire chimney flue-head glow accent
NICHE  = "#a8946a"   # saint-niche dressed-stone surround / altar shelf (warm dressed stone)
CANDLE = "#ffe6a8"   # saint-niche candle glow
POT    = "#7d5a30"   # saint-niche flower-pot
BANNER = "#5d7da8"   # faded-blue fisher's-guild wall-banner (muted blue cloth, the one cool accent)
BANNERD= "#465f80"   # banner shadow fold (darker blue -> 2-tone drape)
SIGN   = "#8a6a38"   # hanging-sign board
SIGNP  = "#4a371d"   # sign gantry timber
SMOKE  = "#5a5550"   # smoker body (ground-floor trade)
SMOKEL = "#ff9d57"   # lit smoker glow
BARREL = "#7d5a30"   # barrel clutter

# ============================================================================================
# 0) WATER 'TELL' -- a water plate under the jetty overhang + winch (front = high z) -------------
# ============================================================================================
S.box(0, 8, 0, 7, 2, 1, WATER)                       # water plate off the water side (z8..10 front)

# ============================================================================================
# 1) C0 -- 7x8 STONE-BRICK PLINTH (the house's damp-proof base, NOT a quay) ----------------------
# ============================================================================================
S.box(0, 0, 0, 7, 8, 1, PLINTH, seam=True)           # 7x8 stone-brick plinth lifting the house one block
S.box(0, 0, 0, 1, 1, 1, COBBLE)                       # back-west cobblestone footing
S.box(6, 0, 0, 1, 1, 1, COBBLE)                       # back-east cobblestone footing
S.box(0, 7.6, 0, 7, 0.4, 1, WET)                      # wet line along the water edge of the plinth (the 'at water' tell)
S.box(-1, 1, 0, 1, 4, 1, "#6f5d3e")                  # trodden landward earth at the door approach (abuts the plinth)

# ============================================================================================
# 2) C1-3 -- MASONRY GROUND FLOOR (stone walls + chiseled QUOINS + a flat-arch loading bay) ------
# the entire ground floor is stone_bricks, 3 high (y1..4); bright chiseled-brick quoins at the four
# corners; a wide water-side loading opening with a stone-brick-stair flat-arch head; landward door
# + two iron-bars windows; a stone-brick-slab string-course caps the masonry at course 3.
# ============================================================================================
# chiseled-brick QUOINS at the corners (full 3-high), then plank... no -> stone walls between them
for (cx, cz) in [(0, 0), (6, 0), (0, 7), (6, 7)]:
    S.box(cx, cz, 1, 1, 1, 3, QUOIN, seam=True)       # corner quoin pier y1..4 (bright dressed stone)
# stone-brick wall infill between the quoins (back + west + east closed; water front = loading bay)
S.box(1, 0, 1, 5, 1, 1, STONED)                       # back (z0) wall lower course
S.box(1, 0, 2, 5, 1, 2, STONE, seam=True)             # back wall upper
S.box(0, 1, 1, 1, 6, 1, STONED)                       # west wall lower course
S.box(0, 1, 2, 1, 6, 2, STONE, seam=True)             # west wall upper
S.box(6, 1, 1, 1, 6, 1, STONED)                       # east wall lower
S.box(6, 1, 2, 1, 6, 2, STONE, seam=True)             # east wall upper
# water-side (z7) wall flanks the loading bay (the bay is the central 3-wide opening x2..5)
S.box(1, 7, 1, 1, 1, 3, STONE, seam=True)             # water wall west flank of the bay
S.box(5, 7, 1, 1, 1, 3, STONE, seam=True)             # water wall east flank of the bay
# wide LOADING OPENING (flat-arch): two stone-brick-stairs lean in over the 3-wide gap to a slab key
S.box(2, 7, 1, 3, 1, 2, DOOR)                         # the dark loading-bay reveal (y1..3, x2..5)
S.box(2, 6.85, 3, 1, 0.3, 0.6, ARCH)                  # flat-arch stair leaning in from the west jamb (faces east)
S.box(4, 6.85, 3, 1, 0.3, 0.6, ARCH)                  # flat-arch stair leaning in from the east jamb (faces west)
S.box(3, 6.85, 3.0, 1, 0.3, 0.5, STRING)              # the slab keystone-fill closing the flat arch
# landward DOOR (back-west of centre, a readable spot) + two iron-bars windows
S.box(2, 0, 1, 1, 1, 2, DOOR)                         # recessed spruce doorway (y1..3)
S.box(2, 0, 3, 1, 1, 0.4, BRESS)                      # door lintel
S.box(3.1, 0, 2, 0.9, 0.3, 1, BARS)                   # back iron-bars window (east of the door)
S.box(6, 2.5, 2.2, 1, 1, 1, BARS)                     # east-wall iron-bars window (visible face)
# STRING-COURSE -- a stone-brick-slab band capping the masonry storey at course 3 (the floor-line)
S.box(-0.3, -0.3, 4, 7.6, 8.6, 0.4, STRING)          # string-course slab band (proud all round -> the stone/timber line)

# ============================================================================================
# 3) C4 -- the JETTIED upper floor OVERHANGING the water side on stair CORBELS + a bressumer ------
# spruce-stairs[half=top] corbels jut 1 from the string-course on the water side; a stripped-dark-oak
# bressumer beam lies across the corbel tops; the upper wall is built ON the beam (a real medieval
# jetty -- every overhanging block carried by the corbel + beam below it, nothing cantilevers free).
# ============================================================================================
for cx in (0.5, 2.5, 4.5, 6.0):                       # jetty corbel brackets along the water side
    S.box(cx, 8.0, 4.0, 0.8, 0.6, 0.5, CORBEL)        # spruce-stair[half=top] corbel jutting 1 over the water (z8)
S.box(0, 8.0, 4.5, 7, 0.7, 0.5, BRESS)               # stripped-dark-oak bressumer beam across the corbel tops
S.box(0, 8.0, 5, 7, 1, 0.5, WALLD)                    # the jettied upper-wall sill seats on the bressumer (overhangs 1)

# ============================================================================================
# 4) C5-6 -- timber UPPER STOREY (dark-oak frame + plank infill) + a wide shuttered hoist-opening --
# ============================================================================================
# stripped-dark-oak timber-frame corner posts (the upper frame), y5..7
for (cx, cz) in [(0, 0), (6, 0), (0, 8), (6, 8)]:
    S.box(cx, cz, 5, 1, 1, 2, TFPOST, seam=True)      # upper-storey corner post
# plank infill between the posts (back + sides closed; water gable = hoist-opening)
S.box(1, 0, 5, 5, 1, 2, WALL, seam=True)             # back upper wall
S.box(0, 1, 5, 1, 7, 2, WALL, seam=True)             # west upper wall (overhangs the jetty on the water end)
S.box(6, 1, 5, 1, 7, 2, WALLD, seam=True)            # east upper wall
S.box(1, 8, 5, 1, 1, 2, WALL)                         # water gable west flank
S.box(5, 8, 5, 1, 1, 2, WALL)                         # water gable east flank
# wide shuttered HOIST-OPENING on the water gable (3-wide, x2..5) -- spruce-trapdoor shutters
S.box(2, 8, 5, 3, 1, 1.6, DOOR)                       # the dark hoist-opening reveal (upper, over the loading bay)
S.box(2, 8.85, 5, 1, 0.2, 1.5, SHUT)                  # shutter leaf 1
S.box(4, 8.85, 5, 1, 0.2, 1.5, SHUT)                  # shutter leaf 2
# top wall-plate ring the roof seats on
S.box(0, 0, 7, 7, 9, 0.5, BRESS)                      # upper top-plate at y7
# loft-rail inside the hoist-opening (oak-fence) + a hint of stored net
S.box(2, 7.6, 7, 3, 0.3, 0.7, FENCE)                 # loft-rail at the hoist-opening lip
S.box(2.3, 8.0, 7, 1.5, 0.8, 0.5, NET)               # coiled net in the loft (read through the opening)

# ============================================================================================
# 5) C7 -- the FULL-HEIGHT gable-integrated HAND-WINCH ------------------------------------------
# a stripped-oak-log MAST rises from the string-course (y4) up the water gable face to the ridge;
# a stripped-oak-log BOOM projects 4 over the water near the ridge (inboard pinned into the gable);
# chain over boom -> iron-block counterweight (1x1x3) inboard + a 3x2 hung net outboard; drum at foot.
# placed on the EAST half of the water gable so the whole hoist reads against the open water.
# ============================================================================================
WX = 5.0                                              # winch on the EAST edge of the water gable -> reads against open water
# full-height MAST up the gable face (string-course y4 -> ridge ~y9), the gable IS the hoist-head.
S.box(WX, 8.05, 4, 0.8, 0.8, 5.2, MAST, seam=True)    # full-height MAST (y4..9.2), pinned through the gable
S.box(WX - 0.05, 7.85, 4.2, 0.95, 0.95, 0.8, MAST)    # winch DRUM at the mast foot (chain-wrapped stripped-log)
# the BOOM projects 4 over the water from HIGH on the mast (y8.4), kept on the east edge + clear of the
# roof so it reads as a clean arm against the open water; the hung net + counterweight hang in FRONT.
S.box(WX + 0.05, 8.4, 8.4, 0.65, 4.2, 0.55, MAST)     # boom arm cantilevering 4 seaward over the water (z8.4->12.6)
# CHAIN over the boom tip dropping to the hung net (outboard) + a short chain to the counterweight (inboard)
S.box(WX + 0.45, 12.3, 5.6, 0.16, 0.16, 3.4, CHAIN)   # tackle chain from the boom TIP down to the net
S.box(WX + 0.2, 9.0, 6.0, 0.16, 0.16, 2.6, CHAIN)     # short chain inboard holding the iron counterweight
# HONEST iron-block COUNTERWEIGHT (1x1x3) hanging clear of the water, just inboard of the boom
for cy in (5.0, 6.0, 7.0):
    S.box(WX + 0.1, 9.2, cy, 0.6, 0.6, 0.9, IRON)     # counterweight block (1x1x3 smith weight, chained to the boom)
# 3x2 hung NET off a fence drop-lattice from the boom tip (each panel a solid hinge above -> nothing floats)
for nz in (12.0, 12.6):                               # two lattice drops across the net width
    S.box(WX + 0.12, nz, 5.6, 0.3, 0.3, 1.9, FENCE)   # net drop-lattice descending from the boom tip
for (nz, ny) in [(12.0,6.3),(12.55,6.3),(12.0,5.6),(12.55,5.6),(12.0,4.9),(12.55,4.9)]:
    S.box(WX + 0.42, nz, ny, 0.22, 0.45, 0.65, NET)   # net panel (3 tall x 2 wide, hinged on lattice/boom)

# ============================================================================================
# 6) C8-9 -- ROOF: main gable (over the 7-span, ridge at course 9) + CROSS-GABLE over the bay -----
# ridge runs along Z (front->back) so a clean gable faces the viewer; far-side overhang only.
# a cross-gable (perpendicular gablet) projects from the water pitch over the loading bay, meeting
# the main ridge in a slab VALLEY. A stone CHIMNEY pierces the landward pitch.
# ============================================================================================
S.box(-0.5, -0.5, 7.5, 8, 9.5, 0.9, ROOFD)           # main eave course (far overhang) -- far slope shading
S.box(0, -0.5, 8.4, 7, 9.5, 0.9, ROOF)               # near main pitch (lighter)
S.box(1.5, -0.5, 9.3, 4, 9.5, 0.9, ROOFD)            # upper far pitch
S.box(2.5, -0.5, 10.2, 2, 9.5, 0.6, RIDGE)           # main slab ridge (runs front->back), ridge top ~y10.8
# back (landward) gable triangle: plank infill up to the climbing ridge
S.box(0.5, -0.3, 7.5, 6, 0.3, 1, WALL)               # back gable infill course 1
S.box(1.5, -0.3, 8.5, 4, 0.3, 1, WALL)               # back gable infill course 2
S.box(2.5, -0.3, 9.5, 2, 0.3, 0.9, WALL)             # back gable apex
# CROSS-GABLE over the water-side loading bay (a perpendicular gablet projecting from the water pitch)
S.box(2, 8.0, 8.4, 3, 1.6, 0.8, ROOF)                # cross-gable eave (projects over the bay, x2..5)
S.box(2.4, 8.0, 9.2, 2.2, 1.2, 0.8, ROOFD)           # cross-gable upper pitch
S.box(2.8, 8.0, 10.0, 1.4, 0.8, 0.5, RIDGE)          # cross-gable ridgelet
S.box(2, 7.0, 10.2, 3, 0.5, 0.4, RIDGE)              # the slab VALLEY where the cross-gable meets the main ridge
# STONE CHIMNEY: a 1x1 stone-brick flue from a ground-floor smoker straight up through the landward
# pitch, piercing the roof and topping with a lit campfire flue-head. It rises from the SMOKER (y1)
# all the way up -> grounded the whole height, NOT starting mid-air. Behind the back wall plane (z1)
# so it reads as built into the landward wall.
S.box(0.5, 1.0, 2, 1, 1, 8.5, CHIM, seam=True)        # chimney flue from the smoker up through the landward pitch (y2..10.5)
S.box(0.5, 1.0, 10.5, 1, 1, 0.7, STRING)             # flue-head cap (campfire sits in here, smoke escapes)

# ============================================================================================
# 7) C10-11 -- a DORMER on the water pitch + a faded banner on the landward gable + a sign gantry --
# ============================================================================================
S.box(1.0, 6.0, 9.0, 0.7, 0.5, 0.9, SHUT)            # spruce-trapdoor DORMER shutter on the main water pitch
# faded-blue fisher's-guild BANNER on the landward (back) gable
S.box(4.5, -0.1, 7.5, 0.2, 0.4, 2.2, BANNER)         # banner cloth on the back gable (faded blue)
S.box(4.7, -0.1, 7.5, 0.15, 0.3, 2.2, BANNERD)       # banner shadow fold (2-tone drape)
# hanging-SIGN gantry over the loading bay (wayfinding)
S.box(5.6, 8.6, 4.0, 0.3, 0.3, 0.8, SIGNP)           # sign gantry post off the water side
S.box(5.2, 8.6, 3.1, 1.0, 0.2, 0.8, SIGN)            # the hanging-sign board (under the gantry, on chains)
S.box(5.3, 8.6, 4.0, 0.8, 0.15, 0.15, SIGNP)         # the gantry arm the board hangs from

# ============================================================================================
# 8) SAINT-NICHE (hash-gated ~45%) -- a 1-wide arched recess in the LANDWARD gable base ----------
# a stone-brick-stairs arched recess holding 3 lit candles on a slab altar shelf + a flower-pot +
# a tiny chain above. Built into the back (z0) wall at a readable east spot, grounded on the plinth.
# ============================================================================================
S.box(4.5, 0, 1, 1, 0.4, 2, NICHE)                   # the dressed-stone niche surround (proud of the back wall)
S.box(4.6, 0, 1.2, 0.8, 0.25, 1.4, DOOR)             # the dark arched recess inside the surround
S.box(4.6, 0, 1.2, 0.8, 0.25, 0.3, NICHE)            # the slab altar SHELF in the recess
S.box(4.65, 0, 1.5, 0.25, 0.2, 0.4, POT)             # flower-pot on the altar shelf
S.box(4.6, -0.05, 2.7, 0.8, 0.2, 0.5, ARCH)          # stone-brick-stair arch head over the niche (stepped)

# ============================================================================================
# 9) ground-floor SMOKERS + barrels (the trade, read through the loading bay) -------------------
# ============================================================================================
S.box(0.6, 1.0, 1, 1, 1, 1, SMOKE)                   # back-west smoker (the chimney rises off this)
S.box(1.7, 1.0, 1, 1, 1, 1, SMOKE)                   # a second smoker beside it
S.box(2.8, 6.0, 1, 1, 1, 1, BARREL)                  # barrel in the loading bay (read through the arch)
S.box(3.9, 6.0, 1, 1, 1, 1, BARREL)                  # stacked barrels by the bay

# ============================================================================================
# 10) ACCENTS -- a fully-lit two-storey house: eave run + winch boom + loft + chimney + niche -----
# ============================================================================================
S.accent(0.0, 4.0, 7.6, "glow", "#ffd47a", r=2.0)    # hanging lantern under the WEST main eave
S.accent(7.0, 4.0, 7.6, "glow", "#ffd47a", r=2.0)    # hanging lantern under the EAST main eave
S.accent(WX + 0.3, 12.7, 8.5, "glow", "#ffe6a8", r=2.2) # lantern on the winch BOOM TIP (over the water)
S.accent(3.5, 8.3, 7.2, "glow", "#ffe6a8", r=1.8)    # lantern on the loft-rail at the hoist-opening
S.accent(1.0, 1.5, 1.6, "glow", SMOKEL, r=1.7)       # the lit ground-floor smoker glow (through the bay)
S.accent(1.0, 1.5, 10.9, "glow", CHIMG, r=1.9)       # the lit-campfire chimney flue-head (smoke escaping)
S.accent(5.0, 0.2, 1.7, "glow", CANDLE, r=1.6)       # the saint-niche candle glow (3 candles, warm devotion)

# --- callout labels ---
S.label(2.5, -0.5, 10.2, "main GABLE + CROSS-GABLE roof + a smoking stone CHIMNEY + dormer")
S.label(WX + 0.3, 12.6, 8.6, "FULL-HEIGHT gable-integrated hand-winch (mast+boom+drum+IRON counterweight)")
S.label(3.0, 8.0, 5.0, "JETTIED timber upper storey -- overhangs on stair corbels + a bressumer beam")
S.label(3.0, 7.0, 2.5, "MASONRY ground floor -- chiseled quoins + a flat-arch loading bay + string-course")
S.label(5.0, 0.0, 2.0, "hash-gated fisher's SAINT-NICHE -- arched recess, 3 candles, altar shelf")
S.label(4.5, -0.1, 8.0, "faded fisher's-guild banner on the landward gable + loading-bay sign")
S.label(0.0, 7.0, 0.5, "7x8 stone-brick plinth (the house's damp-proof base, NOT a quay)")

out = S.svg(title="dock_shack R4 (Highway) -- a two-storey fish-house: masonry ground floor + JETTIED timber loft, full-height hand-winch, cross-gable + smoking chimney + saint-niche",
            size_label="7x8 foot * h12 * 4 lanterns + smoker + chimney + niche (the BIG leap -> a tall two-storey house, one step under the hall)",
            label_w=372)
open("detail_svg/dock_shack_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/dock_shack_highway.svg | bytes", len(out.encode()))
