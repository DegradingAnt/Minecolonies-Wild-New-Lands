"""dock_shack PATH (R2) -> detail_svg/dock_shack_path.svg.
Per deco_catalog_v2.json id 'dock_shack' tier 'Path -- stilt-edge hut' (footprint ~4x5, height 5):
a small, CONTROLLED step up from the Trail lean-to (+1 footprint / +1 height / +one new idea), kept
deliberately modest so the ladder ACCELERATES below it (the big jumps are saved for Road+).
Spec massing, course by course:
  C0  the hut sits at the pier's bank head but its TWO water-side corners now OVERHANG the first
      pier-deck cell, carried on two oak-log short posts that land on the pier's own deck; each
      water-side post gets one STRIPPED-oak-log collar where it meets the floor (a visible joint).
      Landward corners on a spruce sill as Trail.
  C1  spruce floor 4x4; the open water edge gets a LOW oak-fence rail with ONE gap (still opens to
      the water); inside corner a 2-high barrel stack.
  C2  spruce walls on BACK + both SIDES, 1 high; the front stays a wide opening. Landward back wall
      holds a spruce DOOR + a 1x1 glass-pane WINDOW.
  C3  walls reach 2 high. SIGNATURE NET-ARM: one stripped-oak-log juts 2 blocks out over the water
      from the side-wall top plate (inboard end embedded in the plate = cantilevered 2 only). Hung
      from the arm: a 2-wide x 2-tall trapdoor net -- the TOP row hinges on the arm log, the BOTTOM
      row hinges on an oak-fence drop-lattice dropping from each top trapdoor (explicit frame, nothing
      floats). A chain drops from the arm tip to a half-submerged barrel on an oak_slab at water level
      (a crab-pot float, grounded on the slab).
  C4  small spruce GABLE roof -- two opposing 2-deep stair pitches meeting at a 1-block slab ridge on
      a plank course; gable triangles filled with planks + a propped spruce_trapdoor vent shutter. One
      hanging lantern under EACH eave (2 total).
ISO READ: closed walls on the FAR sides; the DOOR + WINDOW turned to a visible face; the NET-ARM
cantilevers toward the viewer over the water (front) so it reads; +crab-pot float grounded on a slab.
First door, first window, first cantilevered net-arm + first proper framed hung net -> a one-room HUT,
not a perch -- but still humble + only just lit (non-linear ladder).
Original WNL build, vanilla blocks only. FORM inspiration (studied, never copied; author knows the
devs): medieval coastal net-lofts / stilt fisher-huts (Tidal Towns + Towns & Towers wharf vocab),
scale calibrated against MineColonies. Credited in CREDITS.md.
Grid: x right, z back(0;landward)->front(water), y up.
"""
from iso_render import Iso

S = Iso(U=27, occlusion=True)

# --- palette (literal) -- warm worn spruce hut over a cool waterline; a wide-contrast ladder -----
WATER  = "#3f7a98"   # open water under the overhanging water-side corners (cool blue, pushes the hut off it)
WET    = "#2c4f4d"   # dark wet collar at the water-side post waterline (the 'sits in water' tell)
POST   = "#5a4026"   # oak-log water-side corner-posts (dark warm timber, land on the pier deck)
COLLAR = "#caa15a"   # stripped-oak-log collar where the post meets the floor (bright joint -> reads as built)
SILL   = "#caa766"   # spruce-plank sill / floor (light warm board, the deck reads bright)
WALL   = "#b98f51"   # spruce-plank wall (mid warm board, between SILL light + ROOF dark)
WALLD  = "#9a743f"   # shaded lower wall band (2-tone plank read)
FRAME  = "#4a371d"   # dark plank/timber lintel + sill-beam accents (dark warm -> punches openings)
FENCE  = "#7a5526"   # oak-fence water rail + net drop-lattice (mid warm timber)
ARM    = "#e0c489"   # stripped-oak-log NET-ARM (palest timber -> the cantilevered arm pops)
DOOR   = "#3a2c1b"   # dark recessed spruce doorway (near-black, a real opening)
WIN    = "#2b3138"   # dark window reveal
GLASS  = "#67aab8"   # glass-pane window (cool jewel, reads as glazing)
ROOF   = "#46402f"   # spruce-stair gable roof, near pitch (warm dark)
ROOFD  = "#332e22"   # shaded far gable pitch (darker)
RIDGE  = "#5d564c"   # spruce-slab ridge (lighter -> the ridge line reads off the dark pitches)
VENT   = "#7a5526"   # propped spruce-trapdoor gable vent shutter
BARREL = "#7d5a30"   # barrel / crab-pot float clutter
HOOP   = "#caa15a"   # barrel-lid hoop accent
NET    = "#86603a"   # hung oak-trapdoor drying net (warm brown, reads as mesh)
SLAB   = "#9a743f"   # oak_slab the crab-pot float rests on at water level (grounded)
GROUND = "#6f5d3e"   # trodden landward earth

# ============================================================================================
# 0) WATER 'TELL' -- a thin water plate under the overhanging water-side corners (front = high z)
# ============================================================================================
S.box(0, 4, 0, 4, 1, 1, WATER)                       # water plate under the seaward (front) overhang

# ============================================================================================
# 1) C0 -- sill on the bank + two water-side oak-log posts (collared) carrying the overhang -------
# landward corners rest on a spruce sill; the two water-side corners overhang the first pier-deck
# cell on two oak-log posts that land on the pier deck (NOT the shack's piles), collared at the floor.
# ============================================================================================
S.box(0, 0, 1, 4, 4, 0.5, SILL, seam=True)           # 4x4 spruce sill on the bank head (top at y1.5)
S.box(-1, 0, 0, 1, 2, 1, GROUND)                     # trodden coarse_dirt at the landward sill (abuts the sill west face)
# water-side oak-log posts (overhang corners), dropped to the pier deck, collared where they meet the floor
S.box(0, 4, 0, 1, 1, 1.5, POST, seam=True)           # west water-side post (y0->floor)
S.box(3, 4, 0, 1, 1, 1.5, POST, seam=True)           # east water-side post
S.box(0, 4, 1.4, 1, 1, 0.3, COLLAR)                  # stripped-log collar at the west post-floor joint (bright)
S.box(3, 4, 1.4, 1, 1, 0.3, COLLAR)                  # collar at the east post-floor joint
S.box(0, 4, 0, 1, 1, 0.4, WET)                       # wet collar at the west post waterline
S.box(3, 4, 0, 1, 1, 0.4, WET)                       # wet collar at the east post

# ============================================================================================
# 2) C1 -- FLOOR + low water-rail (with one gap) ------------------------------------------------
# ============================================================================================
S.box(0, 0, 1.5, 4, 4, 0.5, SILL, seam=True)         # spruce floor 4x4 (top at y2)
# low oak-fence water rail along the open front (z4), with ONE gap (still opens to the water)
S.box(0, 4, 2, 1, 0.4, 0.8, FENCE)                   # rail post + run, west of the gap
S.box(2, 4, 2, 2, 0.4, 0.8, FENCE)                   # rail run east of the gap (the gap is x1..2 -> the mooring step)

# ============================================================================================
# 3) C2 -- walls on BACK + both SIDES (1 high); front stays a wide opening; DOOR + WINDOW ---------
# closed walls go on the FAR back + far west; the EAST side wall (a visible face) carries the window;
# the DOOR sits in the back wall but is turned partly toward the viewer corner so it reads.
# ============================================================================================
S.box(0, 0, 2, 4, 1, 1, WALLD)                       # back (z0) wall lower band
S.box(0, 1, 2, 1, 3, 1, WALLD)                       # west (x0) side wall lower band
S.box(3, 1, 2, 1, 3, 1, WALLD)                       # east (x3) side wall lower band (visible face -> carries window)

# ============================================================================================
# 4) C3 -- walls reach 2 high + the SIGNATURE NET-ARM cantilevering over the water --------------
# ============================================================================================
S.box(0, 0, 3, 4, 1, 1, WALL, seam=True)             # back wall upper course (z0)
S.box(0, 1, 3, 1, 3, 1, WALL, seam=True)             # west wall upper course
S.box(3, 1, 3, 1, 3, 1, WALL, seam=True)             # east wall upper course
# DOOR in the back wall, at the visible back-east corner so the camera reads it (dark recess + leaf)
S.box(2, 0, 2, 1, 1, 2, DOOR)                        # recessed spruce doorway (y2..4)
S.box(2, 0.85, 2, 1, 0.15, 2, FRAME)                 # door leaf (proud, reads as a hung door on the back face)
S.box(2, 0, 4, 1, 1, 0.4, FRAME)                     # door lintel beam over the opening
# WINDOW on the EAST side wall (x3, visible face): dark reveal + a glass pane + sill
S.box(3, 1.8, 3.2, 1, 1, 0.8, WIN)                   # window reveal (dark recess)
S.box(3.85, 1.8, 3.2, 0.2, 1, 0.8, GLASS)            # glass pane proud of the reveal
S.box(3, 1.7, 3.0, 1, 1.3, 0.2, FRAME)               # window sill timber under the reveal
# SIGNATURE NET-ARM: a stripped-oak-log juts 2 over the water from the EAST side-wall top plate.
ARMX = 3.2                                            # net-arm sits on the east wall plate -> cantilevers toward the viewer
S.box(ARMX, 3.0, 4, 0.7, 0.7, 0.7, ARM)              # arm inboard root, embedded in the east wall plate (supported)
S.box(ARMX, 4.0, 4, 0.7, 2.0, 0.7, ARM)              # the arm cantilevering 2 over the water (z4->6)
# 2-wide x 2-tall hung net: TOP row hinges on the arm log; BOTTOM row hinges on an oak-fence drop-lattice
S.box(ARMX + 0.15, 4.2, 3.9, 0.45, 0.45, 1.0, FENCE) # drop-lattice A (descends from the arm -> hinge for lower row)
S.box(ARMX + 0.15, 5.0, 3.9, 0.45, 0.45, 1.0, FENCE) # drop-lattice B
# net panels: top row hung on the arm, bottom row hung on the lattice (each has a solid hinge above)
S.box(ARMX + 0.55, 4.2, 4.0, 0.2, 0.6, 0.85, NET)    # net top-row panel 1 (hinges on the arm)
S.box(ARMX + 0.55, 5.0, 4.0, 0.2, 0.6, 0.85, NET)    # net top-row panel 2
S.box(ARMX + 0.55, 4.2, 3.1, 0.2, 0.6, 0.85, NET)    # net bottom-row panel 1 (hinges on the lattice)
S.box(ARMX + 0.55, 5.0, 3.1, 0.2, 0.6, 0.85, NET)    # net bottom-row panel 2
# chain from the arm tip down to a half-submerged crab-pot float on an oak_slab at water level (grounded)
S.box(ARMX + 0.25, 5.9, 1.2, 0.18, 0.18, 2.6, FENCE) # the hoist chain dropping from the arm tip
S.box(ARMX - 0.3, 5.6, 1, 1, 1, 0.3, SLAB)           # oak_slab at water level (the float rests on this)
S.box(ARMX - 0.2, 5.7, 1.3, 0.8, 0.8, 0.7, BARREL)   # half-submerged barrel = crab-pot float (grounded on the slab)

# ============================================================================================
# 5) clutter -- a 2-high barrel stack in the inside corner (read through the open front) ----------
# ============================================================================================
S.box(0.1, 0.1, 2, 1, 1, 1, BARREL)                  # barrel at the back-west inside corner
S.box(0.1, 0.1, 3, 1, 1, 1, BARREL)                  # stacked barrel (2-high catch)
S.box(0.1, 0.1, 4, 1, 1, 0.18, HOOP)                 # barrel-lid hoop accent

# ============================================================================================
# 6) C4 -- small spruce GABLE roof (two opposing 2-deep pitches to a slab ridge) ----------------
# ridge runs along Z (front->back) so a clean gable triangle faces the viewer; pitches fall to the
# x-eaves. Gable triangle filled with planks + a propped vent shutter. Overhang only on the far sides.
# ============================================================================================
S.box(-0.4, -0.4, 4, 4.8, 4.8, 0.9, ROOFD)           # eave course (far-side overhang) -- far pitch shading
S.box(0, -0.4, 4.9, 4, 4.8, 0.9, ROOF)               # near pitch course (lighter)
S.box(1, -0.4, 5.8, 2, 4.8, 0.9, ROOFD)              # upper far pitch
S.box(1.5, -0.4, 6.7, 1, 4.8, 0.6, RIDGE)            # slab ridge (runs front->back over the gable)
# back gable triangle: planks filling up to the climbing ridge + a propped trapdoor vent
S.box(0.5, -0.2, 4, 3, 0.3, 1, WALL)                 # back gable infill course 1
S.box(1, -0.2, 5, 2, 0.3, 1, WALL)                   # back gable infill course 2
S.box(1.5, -0.2, 6, 1, 0.3, 0.7, WALL)               # back gable apex
S.box(1.3, -0.35, 5.0, 0.2, 0.5, 0.9, VENT)          # propped spruce-trapdoor vent shutter on the back gable

# ============================================================================================
# 7) ACCENTS -- one hanging lantern under EACH eave (2 total, the modest step in light) ----------
# ============================================================================================
S.accent(0.0, 1.8, 4.3, "glow", "#ffd47a", r=2.0)    # hanging lantern under the WEST eave
S.accent(4.0, 1.8, 4.3, "glow", "#ffd47a", r=2.0)    # hanging lantern under the EAST eave
S.accent(0.05, 1.8, 4.7, "dot", "#5d564c", r=0.6)    # west eave chain link (reads the hang)
S.accent(4.05, 1.8, 4.7, "dot", "#5d564c", r=0.6)    # east eave chain link

# --- callout labels ---
S.label(2.0, -0.4, 6.7, "small spruce GABLE roof -- slab ridge, gable-vent shutter, lantern each eave")
S.label(3.4, 5.2, 5.0, "SIGNATURE net-arm -- stripped-log cantilever (2) + framed 2x2 hung net")
S.label(2.0, 0.0, 4.0, "first DOOR + glass WINDOW -- a real one-room enclosure")
S.label(1.0, 4.0, 2.4, "low water-rail with ONE gap (still opens to the water) + crab-pot float")
S.label(0.0, 4.0, 1.4, "water-side corners OVERHANG the pier deck on collared oak posts")

out = S.svg(title="dock_shack R2 (Path) -- a stilt-edge fisher's HUT: first door + window + the cantilevered net-arm (a controlled step up)",
            size_label="~4x5 foot * h5 * 2 lanterns (a one-room hut -- the ladder accelerates below; big jumps saved for Road)",
            label_w=352)
open("detail_svg/dock_shack_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/dock_shack_path.svg | bytes", len(out.encode()))
