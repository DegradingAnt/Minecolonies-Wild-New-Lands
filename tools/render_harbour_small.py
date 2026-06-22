"""Harbour rung 1 (small_quay, the Road tier / floor of the pier->quay->harbour ladder)
   -> detail_svg/harbour_small.svg.
Per deco_catalog_v2.json id 'harbour' tier 'Road -> small_quay' (footprint 14x7 stone quay + ONE
timber mooring finger out 5; envelope ~16x12; height 6). The first STONE rung of the ladder: a
working fisher quay, NOT yet a port. Reads as 'roughly one pier's worth of structure on a real
stone platform with the dark-prismarine waterline'. Deliberately modest -- the big leaps (crane,
warehouse, chapel, lighthouse) are saved for the rungs above. ONE hanging lantern only.

Massing translated course-by-course from the catalog:
  - WATERLINE 'tell' (Y=-1): single dark_prismarine wet-face course on seaward + end faces.
  - FOUNDATION (Y=-1 down): cobblestone + ~20% mossy fill, clamped; landward edge keys into bank.
  - DECK (Y=0): stone_bricks(~55%) + cobblestone(~30%) + cracked_stone_bricks(~15%) worn scatter,
    1-wide cobblestone_wall kerb on the seaward edge broken by a stairs gap.
  - BOLLARD ROW (Y=+1..+2): cobble column + wall cap + side-hung chain loop, every 3-4 blocks.
  - MOORING FINGER (1 wide x5 out): spruce_planks deck on spruce_fence piles + dark_prismarine
    collars, ONE hanging lantern on the tip post.
  - DOCK-SHACK (3x3x4): spruce hut, spruce_stairs roof, barrel + composter out front, net-line.
  - STAIRS-TO-WATER: a 1-wide stone_brick_stairs flight at the kerb gap (quay reads boardable).

Original WNL geometry. Inspiration (FORM/SCALE/TECHNIQUE only, never copied; credited in CREDITS.md):
Towns&Towers / Tidal Towns docks (stone quay + timber mooring fingers + a waterline course); Moog's
Paths timber-jetty + hanging-lantern-post pier vocabulary. The dark-prismarine waterline 'tell' is
the WNL signature wrapping every tier. Same wnl_harbour data builder as render_harbour.py (the
grand_port top rung); the placer hashes wear / bollard count / finger length / shack decay live.
ISO: viewer-visible faces are SOUTH (max-z, FRONT) + EAST (max-x) + TOP -> dock-shack door + the
finger + the stairs-to-water all turned to the high-z FRONT so they read.
"""
from iso_render import Iso

S = Iso(U=15)

# ---- palette (literal hex ~ vanilla blocks) -- WIDE-CONTRAST ladder so each material reads ----
WATER = "#356f93"   # sea plate (cool blue -- pushes the stone off it)
WET   = "#14302f"   # dark_prismarine WATERLINE 'tell' (near-black wet band -- the signature)
DECK  = "#8f9499"   # stone_bricks deck (~55%) -- cool grey-blue working stone
COBB  = "#6c6f72"   # cobblestone worn scatter (~30%) -- darker cool, a worn patch on the deck
CRACK = "#7e7d78"   # cracked_stone_bricks (~15%) -- warm-grey worn note (distinct from cobble)
MOSS  = "#5f7050"   # mossy_cobblestone foundation fleck (creeps in at the waterline)
FOUND = "#5a5d60"   # cobblestone foundation mass (darkest stone -> reads heavy + rooted)
KERB  = "#9a948a"   # cobblestone_wall kerb / bollard caps (warm pale -> the low parapet reads)
BOLL  = "#7c756a"   # cobblestone bollard column (warm mid)
DIRT  = "#5d4f3a"   # coarse_dirt landward keying (sits IN the bank -- the quay roots to land)
TIMB  = "#86603a"   # spruce_planks finger deck + shack walls (warm timber)
TIMBD = "#5a4026"   # spruce_fence piles / spruce_log posts (darker -> the frame reads)
ROOF  = "#3f2f1c"   # spruce_stairs shack roof (dark warm -> roof sits DOWN, silhouette sharp)
BARR  = "#7a5c3a"   # barrel / composter props (warm)
LANT  = "#ffd47a"   # hanging lantern glow (the ONE light this rung gets)

# ============================================================================
# 0) WATER FIELD (drawn first / back) -- the quay sits in it
# ============================================================================
S.box(0, 0, 0, 18, 12, 1, WATER)                 # sea plate (everything sits in/over it)

# ============================================================================
# 1) STONE QUAY -- 14 long (x 2..16) x 7 deep (z 2..9), the real platform
#    waterline 'tell' on the SEAWARD (high-z FRONT) + the two end faces.
# ============================================================================
# -- waterline 'tell' course (Y=-1 equiv): dark_prismarine wet face, seaward + ends --
S.box(2, 8, 0, 14, 1, 1, WET)                    # seaward (FRONT) wet face
S.box(2, 2, 0, 1, 7, 1, WET)                     # west end wet face
S.box(15, 2, 0, 1, 7, 1, WET)                    # east end wet face
# -- foundation course just under the deck (cobblestone + mossy fleck, clamped) --
S.box(2, 2, 1, 14, 7, 1, FOUND)                  # foundation mass
S.box(5, 8, 1, 2, 1, 1, MOSS)                    # mossy fleck at the seaward waterline
S.box(11, 8, 1, 2, 1, 1, MOSS)                   # mossy fleck
S.box(2, 8, 1, 1, 1, 1, MOSS)                    # mossy west corner at the water
# -- landward keying: coarse_dirt where the quay meets the bank (back-west, low-z) --
S.box(0, 2, 1, 2, 3, 1, DIRT)                    # coarse_dirt bank key (roots the quay to land)
S.box(1, 5, 1, 1, 3, 1, DIRT)

# ============================================================================
# 2) DECK COURSE (Y=0) -- worn stone scatter + a 1-wide seaward kerb
# ============================================================================
S.box(2, 2, 2, 14, 7, 1, DECK)                   # stone_bricks deck base (the ~55% pick)
# worn cobble scatter (~30%) -- hand-placed patches, cool COBB pops off the deck
S.box(4, 3, 2, 3, 2, 1, COBB)
S.box(9, 2, 2, 2, 3, 1, COBB)
S.box(12, 5, 2, 2, 2, 1, COBB)
S.box(6, 6, 2, 2, 1, 1, COBB)
# cracked_stone_bricks worn note (~15%)
S.box(8, 5, 2, 1, 1, 1, CRACK)
S.box(13, 3, 2, 1, 1, 1, CRACK)
S.box(3, 7, 2, 1, 1, 1, CRACK)
# -- 1-wide cobblestone_wall KERB along the seaward (high-z FRONT) edge, broken by a stairs gap --
S.box(2, 8, 3, 5, 1, 1, KERB)                    # kerb run W of the gap
S.box(9, 8, 3, 7, 1, 1, KERB)                    # kerb run E of the gap (gap at x7..9 for stairs)

# ============================================================================
# 3) BOLLARD ROW (Y=+1..+2) -- cobble column + wall cap + side-hung chain loop
#    one every ~3-4 blocks along the seaward kerb (3 here -- the modest count)
# ============================================================================
def bollard(bx):
    S.box(bx, 8, 3, 1, 1, 1, BOLL)               # cobblestone column (Y=+1)
    S.box(bx, 8, 4, 1, 1, 1, KERB)               # cobblestone_wall cap (Y=+2)
bollard(3)
bollard(11)
bollard(14)

# ============================================================================
# 4) STAIRS-TO-WATER -- 1-wide stone_brick_stairs flight in the kerb gap (boardable)
#    descends the seaward face from deck (Y=0) to the waterline; each tread on a riser.
# ============================================================================
S.box(7, 8, 2, 1, 1, 1, COBB)                    # top tread at deck level (in the kerb gap)
S.box(7, 9, 1, 1, 1, 1, DECK)                    # mid tread (steps down + out over the wet face)
S.box(7, 9, 0, 1, 1, 1, WET)                     # foot tread at the waterline (on the wet course)

# ============================================================================
# 5) DOCK-SHACK (3x3x4) -- tiny fisher hut on the landward back-kerb, door to the road
#    (re-uses the dock_shack catalog piece; seats on a reserved flat 3x3 pad)
# ============================================================================
SH_X, SH_Z = 3, 2
S.box(SH_X, SH_Z, 2, 3, 3, 1, COBB)              # stone_bricks plinth course under the hut
S.box(SH_X, SH_Z, 3, 3, 3, 2, TIMB, seam=True)   # spruce_planks walls (2 tall, the pale read)
for cx, cz in [(SH_X, SH_Z), (SH_X+2, SH_Z), (SH_X, SH_Z+2), (SH_X+2, SH_Z+2)]:
    S.box(cx, cz, 3, 0.6, 0.6, 2, TIMBD)         # slim spruce_log corner-posts (frame, not a dark box)
# doorway recess facing the road approach (high-z FRONT face so the viewer reads it)
S.box(SH_X+1, SH_Z+2, 3, 1, 1, 2, ROOF)          # dark doorway recess (front wall, toward the road)
# spruce_stairs gable roof: proud eave -> stepped-in ridge so it reads as a PITCH, not a block
S.box(SH_X-0.3, SH_Z-0.3, 5, 3.6, 3.6, 1, ROOF)  # proud eave course (overhang -> shadow line)
S.box(SH_X, SH_Z+1, 6, 3, 1, 1, ROOF)            # ridge beam (sits down the centre -> a peak)
# props out front (on the deck, abutting the hut -- grounded, never floating)
S.box(SH_X+3, SH_Z+1, 2, 1, 1, 1, BARR)          # barrel out front (abuts the east wall)
S.box(SH_X+3, SH_Z+2, 2, 1, 1, 1, MOSS)          # composter beside the barrel (chained to it)

# ============================================================================
# 6) MOORING FINGER -- 1 wide x 5 out into the water (high-z FRONT), planks on stilted piles
#    spruce_fence piles scan down to bed; dark_prismarine collar at each waterline; ONE lantern.
# ============================================================================
FG_X = 12
for k in range(5):
    fz = 9 + k
    S.box(FG_X, fz, 0, 1, 1, 1, TIMBD)           # spruce_fence pile (down to bed; grounded)
# dark_prismarine pile-collars at the waterline (every other pile) -- abut the piles
S.box(FG_X, 9, 0, 1, 1, 1, WET)                  # collar at base of pile 1 (the wet 'tell' on the finger)
S.box(FG_X, 11, 0, 1, 1, 1, WET)                 # collar at pile 3
S.box(FG_X, 13, 0, 1, 1, 1, WET)                 # collar at pile 5 (the tip)
# spruce_planks deck spanning the piles (one block up, resting on the pile tops)
S.box(FG_X, 9, 1, 1, 5, 1, TIMB)                 # the plank finger deck
# tip post carrying the single hanging lantern (spruce_fence post on the last deck block)
S.box(FG_X, 13, 2, 1, 1, 1, TIMBD)               # lantern post at the finger tip

# ============================================================================
# 7) ACCENTS -- the ONE hanging lantern (this rung is otherwise UNLIT; the dark-prismarine
#    waterline + the quay silhouette carry the read in daylight)
# ============================================================================
S.accent(FG_X + 0.5, 13.5, 3.2, "glow", LANT, r=2.2)   # hanging lantern on the finger-tip post

# ============================================================================
# 8) CALLOUT LABELS
# ============================================================================
S.label(FG_X + 0.5, 13.5, 3.0, "ONE hanging lantern on the finger-tip post (the rung's only light)")
S.label(FG_X, 11, 1.5, "timber mooring finger -- planks on stilted piles + dark-prismarine collars")
S.label(SH_X + 1.5, SH_Z + 1, 6, "dock-shack (3x3x4) -- spruce hut, barrel + composter out front")
S.label(13, 8, 4, "chain-loop bollard row (cobble column + wall cap, every 3-4)")
S.label(7, 9, 1, "stairs-to-water in the kerb gap -- the quay reads boardable")
S.label(2, 8, 1, "dark-prismarine waterline 'tell' (the WNL signature) on a real stone quay")

out = S.svg(title="Harbour R1 (small_quay) -- a working fisher quay: stone platform + one finger + a dock-shack, dark-prismarine waterline, 1 lantern",
            size_label="14x7 quay + 1 finger * h6 * 1 lantern (the ladder's first STONE rung -- modest, a quay not yet a port)",
            label_w=352)
open("detail_svg/harbour_small.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/harbour_small.svg | bytes", len(out.encode()))
