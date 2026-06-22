"""dock_shack ROAD (R3) -> detail_svg/dock_shack_road.svg.
Per deco_catalog_v2.json id 'dock_shack' tier 'Road -- net-loft' (footprint ~7x9 w/ porch, height 8):
the FIRST BIG JUMP of the lower ladder (Path 4x4x5 -> Road 7x7x8): footprint nearly doubles, it gains
a covered PORCH over the pier head, a genuine SECOND MASS (a half-loft net-hall), a working LIT smoke-
rack, the signature PERSONAL HAND-WINCH integrated INTO the gable wall (boom + drum + iron counter-
weight), and wayfinding signage. A real little net-loft fishery, clearly a larger leap than Trail->Path.
Spec massing, course by course:
  C0  a 5x5 ground room on the pier's bank head; a 2-wide PORCH extends over the first two pier-deck
      cells on FOUR oak-log corner-posts (each cross-braced to the deck corner by one diagonal oak-
      fence); cobblestone footings under the two landward room corners (damp-proofing).
  C1  spruce floor across the 5x5 room + 2x5 porch; porch open edge gets an oak-fence rail with a
      mooring gap. Ground room corner: a LIT smoker (the trade), 1 barrel + 1 chest, 1 composter.
  C2-3 spruce-plank infill between STRIPPED-oak-log corner posts standing proud (timber-frame look);
      back wall = a spruce door + two iron-bars windows; side wall toward water = a wide shuttered
      opening (two spruce-trapdoor shutters on a 2-wide gap) so the loft can hoist nets in.
  C4  the SECOND MASS: a half-LOFT -- spruce-slab floor across the landward 5x3, leaving the seaward
      5x2 open to the porch below (double-height net hall); the loft front gets an oak-fence loft-rail.
  C5  the HAND-WINCH, integrated into the seaward GABLE WALL: the gable rises one block proud as a
      hoist-head; from its top plate a stripped-oak-log boom projects 3 over the porch/water (inboard
      end embedded in the gable = structural). A chain runs over the boom; inboard it wraps a WINCH
      DRUM (a stripped-oak-log mounted in the gable); outboard the chain drops to an HONEST iron-block
      counterweight (1x1x2) hanging clear of the water + a second short chain holds a 2x2 hoisted net
      (oak_trapdoor on an oak-fence drop-lattice). Honest parts: weight is iron, tackle is chain.
  C6-7 a full spruce GABLE roof over the 5x5+loft (3-deep stair pitches to a slab ridge); the water
      gable triangle is the proud hoist-head (boom through it); a spruce-trapdoor smoke-louvre on the
      ridge above the smoker. Lanterns: one under each main eave + one on the winch boom tip + one
      non-hanging on the porch rail post.
  SIGN: one hanging sign on the porch eave (wayfinding).
ISO READ: the porch + winch + boom turn to the VISIBLE water FRONT (high z); the door + windows on
the back/east; the loft + smoke-louvre break the roofline so the second mass + the winch read clearly.
This is the first LIT civic rung -> several lanterns + a glowing smoker (non-linear ladder: the leap is here).
Original WNL build, vanilla blocks only. FORM inspiration (studied, never copied; author knows the
devs): medieval coastal net-lofts + timber-frame fishery huts (Tidal Towns + Towns & Towers wharf
vocab, CTOV/D&T rustic spruce); scale calibrated against MineColonies. Credited in CREDITS.md.
Grid: x right, z back(0;landward)->front(water), y up.
"""
from iso_render import Iso

S = Iso(U=20)

# --- palette (literal) -- warm worn timber-frame fishery over cool water; wide-contrast ladder ----
WATER  = "#3f7a98"   # open water under the porch posts (cool blue -> pushes the warm timber off it)
WET    = "#2c4f4d"   # dark wet collar at the porch-post waterline (the 'sits in water' tell)
POST   = "#5a4026"   # oak-log porch corner-posts (dark warm timber, land on the pier deck)
FRAME  = "#4a371d"   # stripped-DARK lintels / bressumer / door-frame (darkest warm timber, punches openings)
TFPOST = "#e0c489"   # stripped-oak-log timber-frame CORNER POSTS standing proud (palest -> the frame reads)
SILL   = "#caa766"   # spruce-plank floor / porch deck (light warm board)
WALL   = "#b98f51"   # spruce-plank wall infill between the proud posts (mid warm board)
WALLD  = "#9a743f"   # shaded lower wall band (2-tone plank read)
FENCE  = "#7a5526"   # oak-fence rails (porch + loft) + net drop-lattice (mid warm timber)
COBBLE = "#7c776e"   # cobblestone damp-proof footings under the landward corners (cool grey)
DOOR   = "#3a2c1b"   # dark recessed spruce doorway
BARS   = "#3a4048"   # iron-bars window (dark cool metal grid)
SHUT   = "#7a5526"   # spruce-trapdoor shutters on the loft hoist-opening
ROOF   = "#46402f"   # spruce-stair gable roof, near pitch (warm dark)
ROOFD  = "#332e22"   # shaded far gable pitch (darker)
RIDGE  = "#5d564c"   # spruce-slab ridge (lighter -> the ridge line reads)
LOUVRE = "#8a6a38"   # spruce-trapdoor smoke-louvre on the ridge (warm, over the smoker)
LOFT   = "#b08646"   # spruce-slab half-loft floor (the SECOND MASS reads as its own plane)
BOOM   = "#e0c489"   # stripped-oak-log winch BOOM + drum (palest timber -> the winch pops)
IRON   = "#b9c0c9"   # iron-block counterweight (cool bright metal -> reads as the honest smith weight)
CHAIN  = "#46433d"   # winch chain / tackle (dark line)
NET    = "#86603a"   # hung oak-trapdoor net (warm brown mesh)
SMOKE  = "#5a5550"   # smoker body (cool grey-brown stone block)
SMOKEL = "#ff9d57"   # lit smoker mouth glow accent
BARREL = "#7d5a30"   # barrel / chest clutter
CHEST  = "#9a6f33"   # chest (a touch warmer/brighter than the barrel)
SIGN   = "#8a6a38"   # hanging-sign board (warm wayfinding plank)
SIGNP  = "#4a371d"   # sign gantry timber

# ============================================================================================
# 0) WATER 'TELL' -- a water plate under the porch (the seaward 2 cells, front = high z) ----------
# ============================================================================================
S.box(0, 5, 0, 5, 2, 1, WATER)                       # water plate under the porch (z5..7 front)

# ============================================================================================
# 1) C0 -- 5x5 ground room on the bank + a 2-wide PORCH on four oak-log posts over the pier deck --
# landward room corners on cobblestone footings; the seaward porch is carried on 4 oak-log posts that
# land on the pier deck (NOT the shack's piles), each cross-braced to the deck corner by a fence.
# ============================================================================================
S.box(0, 0, 1, 5, 5, 0.5, SILL, seam=True)           # 5x5 ground-room sill on the bank head (top y1.5)
S.box(0, 0, 0, 1, 1, 1, COBBLE)                       # back-west cobblestone damp-proof footing
S.box(4, 0, 0, 1, 1, 1, COBBLE)                       # back-east cobblestone footing
S.box(-1, 1, 0, 1, 3, 1, "#6f5d3e")                  # trodden landward earth at the door approach (abuts the sill)
# porch posts: 4 oak-logs landing on the pier deck (y0->floor), cross-braced by a diagonal fence
for (px, pz) in [(0, 5), (4, 5), (0, 7), (4, 7)]:
    S.box(px, pz, 0, 1, 1, 1.5, POST, seam=True)      # porch corner-post up to the porch floor
    S.box(px, pz, 0, 1, 1, 0.4, WET)                  # wet collar at the waterline
S.box(0.4, 5.4, 0.6, 0.4, 0.4, 1.0, FENCE)           # cross-brace (diagonal fence) at the west porch joint
S.box(4.0, 5.4, 0.6, 0.4, 0.4, 1.0, FENCE)           # cross-brace at the east porch joint

# ============================================================================================
# 2) C1 -- FLOOR across room + porch; porch rail (with a mooring gap); the working corner ---------
# ============================================================================================
S.box(0, 0, 1.5, 5, 5, 0.5, SILL, seam=True)         # ground-room floor (top y2)
S.box(0, 5, 1.5, 5, 2, 0.5, SILL, seam=True)         # 2x5 porch deck over the water (top y2)
# porch oak-fence rail along the open front (z7) with ONE mooring gap (x2..3)
S.box(0, 7, 2, 2, 0.4, 0.8, FENCE)                   # porch rail west of the gap
S.box(3, 7, 2, 2, 0.4, 0.8, FENCE)                   # porch rail east of the gap
# the WORKING corner (back-east, inside the room): a LIT smoker (the trade) + barrel + chest + composter
S.box(3.05, 0.1, 2, 1, 1, 1, SMOKE)                  # smoker body (the fish-smoking trade)
S.box(3.05, 1.05, 2, 0.9, 0.9, 0.9, SMOKE)           # a second smoker block beside it (the rack reads bigger)
S.box(4.05, 0.1, 2, 0.9, 0.9, 0.9, BARREL)           # barrel (the catch)
S.box(4.05, 1.05, 2, 0.9, 0.9, 0.9, CHEST)           # chest (fisher loot)
S.box(2.05, 0.1, 2, 0.9, 0.9, 0.9, BARREL)           # composter (bait/scraps, barrel-toned)

# ============================================================================================
# 3) C2-3 -- timber-frame walls 2 high (proud stripped-log corner posts + plank infill) ----------
# corner posts stand PROUD; plank infill between. Back wall: door + two iron-bars windows. Side wall
# toward the water (east, visible): a wide 2-wide shuttered hoist-opening (two spruce-trapdoor shutters).
# ============================================================================================
# proud stripped-log timber-frame CORNER POSTS (the frame read), full wall height y2..4
for (cx, cz) in [(0, 0), (4, 0), (0, 4), (4, 4)]:
    S.box(cx, cz, 2, 1, 1, 2, TFPOST, seam=True)      # corner post y2..4 (palest -> the frame pops)
# plank wall infill between posts (back + west closed; east + front carry openings)
S.box(1, 0, 2, 3, 1, 1, WALLD)                        # back wall lower band (z0)
S.box(1, 0, 3, 3, 1, 1, WALL, seam=True)             # back wall upper
S.box(0, 1, 2, 1, 3, 1, WALLD)                        # west wall lower band
S.box(0, 1, 3, 1, 3, 1, WALL, seam=True)             # west wall upper
S.box(4, 1, 2, 1, 3, 2, WALLD)                        # east wall lower (carries the shuttered opening above)
S.box(0, 4, 2, 1, 1, 2, WALLD)                        # short return at the seaward-west corner (frame to the porch)
# top wall-plate ring (the eave line the roof + the loft seat on)
S.box(0, 0, 4, 5, 5, 0.5, FRAME)                      # top plate at y4
# DOOR in the back wall (back-east, a visible corner): dark recess + frame
S.box(2, 0, 2, 1, 1, 2, DOOR)                        # recessed spruce doorway (y2..4)
S.box(2, 0, 4, 1, 1, 0.4, FRAME)                     # door lintel beam
# two IRON-BARS windows flanking the door on the back wall
S.box(1, 0, 3, 0.9, 0.3, 0.9, BARS)                  # back window 1 (west of the door)
S.box(3.1, 0, 3, 0.9, 0.3, 0.9, BARS)                # back window 2 (east of the door)
# wide SHUTTERED hoist-opening on the EAST wall (toward the water) -- 2 spruce-trapdoor shutters
S.box(4, 2, 3, 1, 2, 1.4, DOOR)                       # the dark 2-wide hoist-opening reveal (east wall)
S.box(4.85, 2.0, 3, 0.2, 0.9, 1.3, SHUT)             # spruce-trapdoor shutter leaf 1 (proud)
S.box(4.85, 3.0, 3, 0.2, 0.9, 1.3, SHUT)             # shutter leaf 2

# ============================================================================================
# 4) C4 -- the SECOND MASS: a half-LOFT (spruce-slab floor on the landward 5x3) ------------------
# the loft floor spans the landward 5x3; the seaward 5x2 stays open to the porch below (double-height
# net hall); the loft front gets an oak-fence loft-rail. This is what makes Road read as two-storey.
# ============================================================================================
S.box(0, 0, 4.5, 5, 3, 0.4, LOFT, seam=True)         # half-loft slab floor (landward 5x3) -- the SECOND MASS
S.box(0, 3, 5, 5, 0.4, 0.8, FENCE)                   # oak-fence loft-rail at the loft front (z3, over the open hall)
# a hint of net stored in the loft (read through the open seaward bay)
S.box(0.3, 0.3, 5, 1.2, 1, 0.5, NET)                 # a coiled net heap on the loft floor

# ============================================================================================
# 5) C5 -- the SIGNATURE HAND-WINCH, integrated INTO the seaward gable wall ----------------------
# the seaward gable rises one block proud as a hoist-head; a stripped-log BOOM projects 3 over the
# porch/water (inboard end embedded in the gable = structural). Chain over the boom: inboard wraps a
# DRUM (stripped-log in the gable), outboard drops to an iron-block COUNTERWEIGHT + a 2x2 hung net.
# the gable + winch sit on the EAST half so they read against the open water, clear of the roof mass.
# ============================================================================================
GX = 4.0                                              # winch on the EAST edge of the seaward gable -> the boom reads over open water
# gable hoist-head: the gable wall rises proud one block; the boom + drum root INTO it (structural).
S.box(GX, 4.0, 4, 1, 1, 2.2, WALL, seam=True)        # gable hoist-head rising proud above the wall plate (y4..6.2)
S.box(GX + 0.05, 4.0, 4.6, 0.9, 0.9, 0.7, BOOM)      # winch DRUM (stripped-log mounted in the gable, chain coiled on it)
# the BOOM cantilevers 3 over the porch/water from the hoist-head; kept HIGH (y5.7) + on the east
# edge (x4.1) so it reads as a clean arm against the open water, clear of the porch + roof below it.
S.box(GX + 0.1, 4.6, 5.7, 0.65, 3.2, 0.55, BOOM)     # the boom arm projecting seaward over the water (z4.6->7.8)
# CHAIN over the boom tip, dropping to the iron counterweight (inboard) + the hung net (outboard)
S.box(GX + 0.55, 7.3, 4.0, 0.16, 0.16, 2.3, CHAIN)   # tackle chain dropping from the boom TIP to the net
S.box(GX + 0.15, 5.2, 3.2, 0.16, 0.16, 1.5, CHAIN)   # short chain inboard holding the iron counterweight
# HONEST iron-block COUNTERWEIGHT (1x1x2) hanging just clear of the water, inboard of the boom
S.box(GX + 0.1, 5.0, 2.4, 0.6, 0.6, 0.8, IRON)       # counterweight lower block (clear of the water)
S.box(GX + 0.1, 5.0, 3.2, 0.6, 0.6, 0.8, IRON)       # counterweight upper block (the 1x1x2 smith weight)
# a 2x2 hung NET off a short oak-fence drop-lattice from the boom TIP (each panel a solid hinge above)
S.box(GX + 0.15, 7.0, 3.2, 0.35, 0.35, 1.4, FENCE)   # net drop-lattice A (descends from the boom tip)
S.box(GX + 0.15, 7.6, 3.2, 0.35, 0.35, 1.4, FENCE)   # net drop-lattice B
S.box(GX + 0.5, 7.0, 3.6, 0.25, 0.5, 0.9, NET)       # net panel top 1 (hinges on the boom/lattice)
S.box(GX + 0.5, 7.6, 3.6, 0.25, 0.5, 0.9, NET)       # net panel top 2
S.box(GX + 0.5, 7.0, 2.6, 0.25, 0.5, 0.9, NET)       # net panel bottom 1 (hinges on the lattice)
S.box(GX + 0.5, 7.6, 2.6, 0.25, 0.5, 0.9, NET)       # net panel bottom 2

# ============================================================================================
# 6) C6-7 -- full spruce GABLE roof over the 5x5+loft + a smoke-louvre on the ridge --------------
# ridge runs along Z (front->back) so a clean gable faces the viewer; 3-deep stair pitches to a slab
# ridge on a plank course; the water gable triangle is the proud hoist-head (the boom passes through).
# overhang on the far sides only so the front faces stay readable.
# ============================================================================================
S.box(-0.5, -0.5, 5, 6, 6, 0.9, ROOFD)               # eave course (far overhang) -- far slope shading
S.box(0, -0.5, 5.9, 5, 6, 0.9, ROOF)                 # near pitch course (lighter)
S.box(1, -0.5, 6.8, 3, 6, 0.9, ROOFD)                # upper far pitch
S.box(1.5, -0.5, 7.7, 2, 6, 0.6, RIDGE)              # slab ridge (runs front->back over the gable)
# back gable triangle: plank infill up to the climbing ridge (the landward gable, fully filled)
S.box(0.5, -0.3, 5, 4, 0.3, 1, WALL)                 # back gable infill course 1
S.box(1, -0.3, 6, 3, 0.3, 1, WALL)                   # back gable infill course 2
S.box(1.5, -0.3, 7, 2, 0.3, 0.8, WALL)               # back gable apex
# smoke-LOUVRE on the ridge above the smoker (back-east) -- vents the smoking trade
S.box(3.4, 0.3, 7.6, 0.7, 0.7, 0.7, LOUVRE)          # spruce-trapdoor smoke-louvre (proud of the ridge, over the smoker)

# ============================================================================================
# 7) SIGN -- one hanging sign on the porch eave (wayfinding) -------------------------------------
# ============================================================================================
S.box(1.0, 7.0, 4.4, 0.3, 0.3, 0.6, SIGNP)           # sign gantry post off the porch eave
S.box(0.6, 7.0, 3.5, 1.1, 0.2, 0.9, SIGN)            # the hanging-sign board (under the gantry, on chains)
S.box(0.7, 7.0, 4.4, 0.9, 0.15, 0.15, SIGNP)         # the gantry arm the board hangs from

# ============================================================================================
# 8) ACCENTS -- the first properly LIT rung: eave lanterns + boom + porch + the glowing smoker -----
# ============================================================================================
S.accent(0.0, 2.3, 5.3, "glow", "#ffd47a", r=2.1)    # hanging lantern under the WEST main eave
S.accent(5.0, 2.3, 5.3, "glow", "#ffd47a", r=2.1)    # hanging lantern under the EAST main eave
S.accent(GX + 0.4, 7.9, 5.6, "glow", "#ffe6a8", r=2.0) # lantern on the winch BOOM TIP (over the water)
S.accent(4.5, 7.0, 2.9, "glow", "#ffe6a8", r=1.7)    # non-hanging lantern on the porch rail post
S.accent(3.5, 0.5, 2.5, "glow", SMOKEL, r=1.9)       # the LIT smoker mouth glow (the trade burning)
S.accent(3.7, 0.5, 8.0, "glow", "#ff9d57", r=1.5)    # smoke-louvre glow on the ridge (smoke escaping)

# --- callout labels ---
S.label(2.0, -0.5, 7.7, "full spruce GABLE roof + ridge smoke-LOUVRE over the lit smoker")
S.label(GX + 0.4, 7.8, 5.7, "SIGNATURE hand-winch -- gable-integrated boom + drum + IRON counterweight + hung net")
S.label(0.5, 3.0, 4.9, "the SECOND MASS -- a half-LOFT net-hall (reads two-storey, not a taller hut)")
S.label(3.5, 0.5, 2.5, "lit SMOKER (the trade) + barrel + chest + composter working corner")
S.label(2.0, 0.0, 3.2, "timber-frame walls: proud stripped-log posts, door + iron-bars windows")
S.label(0.7, 7.0, 3.5, "covered PORCH over the pier head + hanging wayfinding sign")
S.label(0.0, 6.0, 1.0, "porch on 4 oak-log posts on the pier deck (cross-braced; nothing floats)")

out = S.svg(title="dock_shack R3 (Road) -- a net-loft fishery: porch + half-loft second mass + the gable-integrated PERSONAL hand-winch + lit smoker (the first big jump)",
            size_label="~7x9 w/ porch * h8 * 4 lanterns + lit smoker (the BIG lower-ladder leap: second mass + porch + hand-winch + signage)",
            label_w=360)
open("detail_svg/dock_shack_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/dock_shack_road.svg | bytes", len(out.encode()))
