"""dock_shack TRAIL (R1, floor of the ladder) -> detail_svg/dock_shack_trail.svg.
Per deco_catalog_v2.json id 'dock_shack' tier 'Trail -- bankside perch' (footprint ~3x4, height 4):
the smallest piece in this whole family by design -- a one-man fisher's LEAN-TO, open to the water.
Spec massing, course by course:
  C0  spruce sill 3x3 on the pier's bank-landing cell; the two WATER-side corners drop one block to
      short oak-log corner-posts that sit on the pier deck edge (NOT the shack's own piles -- it
      borrows the pier's ground); coarse_dirt + gravel scatter at the landward sill = trodden ground.
  C1  spruce floor 3x3; it is a LEAN-TO -> only the BACK (landward) wall + ONE side wall built 1 high;
      the water-facing front + the other side stay OPEN; the open front corner is held by one oak-fence
      post rising 2 to carry the roof eave.
  C2  back + one side wall reach course 2; inside against the back wall a barrel + a stacked barrel
      (the catch) + a composter (bait); a NON-hanging lantern sits ON the top barrel (grounded light);
      HAND-NET: two oak-fence posts on the side-wall top carry a horizontal oak-fence rail; from it
      hang 3 oak_trapdoor[open] -- each hinging on the solid rail directly above = a small drying net.
  C3  mono-pitch LEAN-TO roof: spruce_stairs in a single 3-wide x 2-deep slope falling from the high
      back wall toward the water; the high (landward) edge capped by a spruce_slab ridge; one HANGING
      lantern on a chain under the seaward eave.
ISO READ: the closed walls are put on the FAR sides (back z0 + west x0) and the OPEN mouth + the
hand-net + the catch are turned to the VISIBLE faces (the EAST x-side carries the net; the water FRONT
is the open mouth) so the viewer reads the character. Humble + warm (2 small lanterns) -- the civic
leaps are saved for Road/Highway (non-linear ladder).
Original WNL build, vanilla blocks only. FORM inspiration (studied, never copied; author knows the
devs): coastal stilt fisher lean-tos / net perches (Tidal Towns + Towns & Towers wharf vocab), scale
calibrated against MineColonies. Credited in CREDITS.md. Grid: x right, z back(0;landward)->front(water), y up.
"""
from iso_render import Iso

S = Iso(U=30)

# --- palette (literal) -- warm worn spruce hut over a cool waterline; every block reads apart -----
WATER  = "#3f7a98"   # open water just under the seaward post (cool blue -> pushes the warm hut off it)
WET    = "#2c4f4d"   # dark wet collar where the water-side post meets the waterline (the 'in water' tell)
POST   = "#5a4026"   # oak-log water-side corner-posts (dark warm timber, dropped to the pier deck edge)
SILL   = "#caa766"   # spruce-plank sill / floor platform (light warm board -> the deck reads bright)
WALL   = "#b98f51"   # spruce-plank wall (mid warm board, clearly between SILL light + ROOF dark)
WALLD  = "#9a743f"   # shaded lower wall band (a 2-tone plank read so the wall is not one flat colour)
FENCE  = "#7a5526"   # oak-fence eave post + net rail (mid warm timber, the open-corner support)
ROOF   = "#46402f"   # spruce-stair mono-pitch roof, near slope (warm dark -> a clear lean-to silhouette)
ROOFD  = "#332e22"   # shaded far roof slope (the back of the pitch reads darker)
RIDGE  = "#5d564c"   # spruce-slab ridge cap (lighter -> picks the high ridge line off the dark slope)
BARREL = "#7d5a30"   # barrel (the fisher's catch) + composter clutter
HOOP   = "#caa15a"   # barrel-lid hoop accent (the one bright ring on the catch)
NET    = "#86603a"   # hung oak-trapdoor drying net (warm brown, reads as mesh against the dark roof)
GROUND = "#6f5d3e"   # trodden landward earth (coarse_dirt) at the sill
GRAVEL = "#8a857c"   # gravel scatter mixed into the trodden ground (cool grey fleck)

# ============================================================================================
# 0) WATER 'TELL' -- a thin water plate under the seaward posts so the perch clearly sits AT the
#    water's edge (front = high z). The hut body stays on the bank; only the posts touch water.
# ============================================================================================
S.box(0, 3, 0, 3, 1, 1, WATER)                       # water plate under the seaward (front) edge

# ============================================================================================
# 1) C0 -- SILL on the bank + two dropped oak-log corner-posts on the water side (nothing floats) --
# the landward half of the 3x3 sill rests straight on the pier's bank cell; the water-side two
# corners drop one block to short oak-log posts that land on the pier deck edge.
# ============================================================================================
S.box(0, 0, 1, 3, 3, 0.5, SILL, seam=True)           # 3x3 spruce sill frame on the bank-landing cell (top at y1.5)
# trodden ground at the landward sill (coarse_dirt + a gravel fleck) -> the perch sits IN the ground
S.box(-1, 0, 0, 1, 2, 1, GROUND)                     # coarse_dirt approach abutting the sill's west face
S.box(-1, 0, 1, 1, 1, 0.3, GRAVEL)                   # gravel scatter on the trodden patch (grounded on the dirt)
# water-side corner-posts: dropped one block to sit on the pier deck edge (y0->1), carrying the sill
S.box(0, 3, 0, 1, 1, 1.5, POST, seam=True)           # west water-side oak-log post (lands on deck edge, up to floor)
S.box(2, 3, 0, 1, 1, 1.5, POST, seam=True)           # east water-side oak-log post
S.box(0, 3, 0, 1, 1, 0.4, WET)                       # wet collar at the west post waterline (the 'in water' tell)
S.box(2, 3, 0, 1, 1, 0.4, WET)                       # wet collar at the east post

# ============================================================================================
# 2) C1 -- FLOOR + the LEAN-TO walls (back + WEST side only; the EAST side + WATER front stay open)
# closed walls are on the FAR sides (back z0, west x0) so they do NOT block the read; the EAST side
# (x2, a VISIBLE face) is left open to carry the hand-net, and the WATER front (z2) is the open mouth.
# ============================================================================================
S.box(0, 0, 1.5, 3, 3, 0.5, SILL, seam=True)         # spruce floor 3x3 on the sill (top at y2)
S.box(0, 0, 2, 3, 1, 1, WALLD)                        # back (landward, z0) wall lower band
S.box(0, 1, 2, 1, 2, 1, WALLD)                        # west (x0) side wall lower band (the closed FAR side)
# open-front corner support: one oak-fence post rising 2 to carry the seaward roof eave (front-east mouth)
S.box(2, 3, 2, 0.6, 0.6, 2.2, FENCE, seam=True)      # open-corner eave post (y2..4.2) -> holds the lean-to mouth

# ============================================================================================
# 3) C2 -- wall tops + the working clutter + the HAND-NET on the EAST (visible) side -------------
# back + west walls reach course 2; the catch barrels + composter sit against the back wall (read
# through the open mouth); a non-hanging lantern rests ON the top barrel; the hand-net hangs off a
# real fence rail spanning two posts that stand on the EAST wall plate (x2 -> a viewer-visible face).
# ============================================================================================
S.box(0, 0, 3, 3, 1, 1, WALL, seam=True)             # back wall upper course (z0)
S.box(0, 1, 3, 1, 2, 1, WALL, seam=True)             # west wall upper course (x0)
# clutter inside against the back wall (all grounded on the floor / each other), set toward the open mouth
S.box(0.1, 0.1, 2, 1, 1, 1, BARREL)                  # barrel (the catch) at the back-west corner, on the floor
S.box(0.1, 0.1, 3, 1, 1, 1, BARREL)                  # stacked barrel on top of it (taller catch heap)
S.box(0.1, 0.1, 4, 1, 1, 0.18, HOOP)                 # barrel-lid hoop accent on the top barrel
S.box(1.05, 0.1, 2, 1, 1, 1, BARREL)                 # composter beside the barrels (bait/scraps)
# HAND-NET on the EAST (x2) edge -> a visible face. Two fence posts stand on the floor edge and carry
# a horizontal rail; 3 trapdoors hang off the rail (each drops straight down off the solid member).
S.box(2.45, 0.5, 2, 0.45, 0.45, 2.3, FENCE)          # net post A (rises from the floor edge, z0.5)
S.box(2.45, 2.05, 2, 0.45, 0.45, 2.3, FENCE)         # net post B (z2.05)
S.box(2.45, 0.5, 4.3, 0.45, 2.0, 0.4, FENCE)         # horizontal net RAIL spanning the two posts (solid hinge member)
# the 3 hung trapdoors -- each hinges on the rail DIRECTLY above it (drops straight down, nothing floats)
S.box(2.55, 0.6, 3.3, 0.25, 0.5, 1.0, NET)           # drying-net panel 1 (hung off the rail, top at the rail)
S.box(2.55, 1.2, 3.3, 0.25, 0.5, 1.0, NET)           # drying-net panel 2
S.box(2.55, 1.8, 3.3, 0.25, 0.5, 1.0, NET)           # drying-net panel 3

# ============================================================================================
# 4) C3 -- MONO-PITCH LEAN-TO ROOF -- a single slope falling from the high back wall to the water.
# 3 wide; high at z0 (landward), low at the seaward eave; a slab ridge caps the high edge; it
# overhangs the seaward eave just enough (<=0.35) to hang one lantern under it. The net (x2, taller
# at y4.5) deliberately stands proud of the seaward eave so the roof does NOT swallow it.
# ============================================================================================
S.box(0, 0, 4, 3, 1, 0.5, RIDGE)                     # high (landward, z0) ridge cap -- spruce slab on the back wall plate
S.box(0, 1, 3.6, 2, 0.9, 0.9, ROOFD)                 # upper slope course (z1, just below the ridge -> dark far slope)
S.box(0, 1.9, 3.0, 2, 1.1, 0.9, ROOF)                # lower slope course falling to the seaward eave (overhang ~0.3)

# ============================================================================================
# 5) ACCENTS -- 2 small warm lights (humble tier): one ON the top barrel, one hung under the eave.
# ============================================================================================
S.accent(0.6, 0.6, 4.4, "glow", "#ffe6a8", r=1.7)    # non-hanging lantern resting ON the top barrel (grounded)
S.accent(1.0, 2.9, 2.5, "glow", "#ffd47a", r=1.9)    # hanging lantern on a chain under the seaward eave (over the mouth)
S.accent(1.0, 2.95, 3.0, "dot", "#5d564c", r=0.7)    # the chain link the eave lantern hangs from (reads the hang)

# --- callout labels ---
S.label(1.5, 0.0, 4.4, "mono-pitch LEAN-TO roof -- slab ridge high (landward), eave low over the water")
S.label(2.6, 1.2, 4.5, "hand-net -- 3 trapdoors hung off a real oak-fence rail (nothing floats)")
S.label(0.6, 0.1, 3.6, "the catch -- two barrels + a composter, a lantern on the top barrel")
S.label(2.0, 3.0, 2.2, "OPEN water-face -- one fence post carries the eave; the whole character")
S.label(0.5, 3.0, 0.3, "water-side corner-posts dropped to the pier deck edge (borrows the pier)")

out = S.svg(title="dock_shack R1 (Trail) -- a one-man bankside fisher's LEAN-TO, open to the water (the smallest piece in the family)",
            size_label="~3x4 foot * h4 * 2 lanterns (ladder floor -- a perch: 'someone fishes here', nothing more)",
            label_w=352)
open("detail_svg/dock_shack_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/dock_shack_trail.svg | bytes", len(out.encode()))
