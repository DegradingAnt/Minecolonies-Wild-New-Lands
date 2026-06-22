"""Plaza TRAIL (R1, floor of the ladder) -> detail_svg/plaza_trail.svg.
Per deco_catalog_v2.json id 'plaza' tier Trail (footprint radial disc r=3, ~7x7 envelope, height 2):
the humblest junction HUB -- a footpath crossing that reads as 'a place', not an accident. A wider
worn radial node (scattered trail palette: coarse_dirt/dirt_path/gravel/cobblestone, podzol/rooted
accents), edges RAGGED so the disc bleeds into grass (no rim, ~35% of edge columns revert to natural
ground). One centre SLOT = a tiny trail-version cairn (2-3 stone wonky hand-stack). One arm-mouth SLOT
= a single leaning sign_post on a cobblestone block, pointing down the busiest arm. NO well, NO light.

ISO note: the disc is a flat apron of ground tiles drawn course-y=0 (each tile 1 block, dy=1 so the
worn ground reads with depth); the 3 trail ARMS keep their own width and blend at the disc edge.
The cairn + sign sit ON the apron (grounded on tile top faces). This is the Trail rung of the same
wnl_plaza whose Great Road FORUM top tier is render_plaza.py; the data builder lays the disc + scatter
+ arms + slots live per junction (radial Bresenham fill, per-arm-gap geometry, hash-deterministic).
Originality/inspiration: medieval market-cross-at-a-crossing idea, original cairn+sign arrangement,
technique only -- credited in CREDITS.md, no assets/NBT/layout copied."""
import math
from iso_render import Iso

S = Iso(U=20)

# --- palette: scattered TRAIL ground, a WIDE-CONTRAST ladder so each material reads as itself ---
COARSE = "#6f5c40"   # coarse_dirt  -- the ~40% majority (warm brown, the worn pack)
PATH   = "#8a7142"   # dirt_path    -- ~25% (lighter tan, the trodden lane look)
GRAVEL = "#9a958c"   # gravel       -- ~20% (pale grey, loose stone)
COBB   = "#857f73"   # cobblestone  -- ~10% (the first laid stone, mid grey-brown)
PODZOL = "#5a4427"   # podzol       -- ~5% accent (dark rich brown, rooted_dirt sibling)
GRASS  = "#5f7d3f"   # natural ground the ragged edge reverts to (the disc bleeds into this)
# cairn stones (trail-version, matches render_cairn_trail palette)
C_DARK = "#6f685d"   # cobbled_deepslate base stone (heavy, rooted)
C_CORE = "#8a8276"   # cobblestone middle stone
C_MOSS = "#6f7d56"   # mossy_cobblestone slab capstone
# sign-post
POST   = "#7a5c3a"   # cobblestone-block footing is COBB; the sign timber is warm oak
SIGN   = "#9a7b48"   # oak sign_post plank (warm, leaning)

C = 3.0   # junction centre on a 0..6 grid (disc radius 3 -> envelope ~7x7)
R = 3.0

# Per-tile scatter is hash-deterministic in the real builder; here a fixed seeded pick mirrors it
# so the render is stable. Weighted exactly to the catalog: coarse40/path25/gravel20/cobb10/podzol5.
def pick(ix, iz):
    h = (ix*73856093 ^ iz*19349663) & 0xffff
    r = h % 100
    if r < 40: return COARSE
    if r < 65: return PATH
    if r < 85: return GRAVEL
    if r < 95: return COBB
    return PODZOL

# 3 trail ARMS at arbitrary bearings (the prime variety source) -- here N=3 at ~90/210/330deg so the
# crossing reads as a real 3-way. Arm tiles get the dirt_path 'lane' look so the routes read through.
arm_bearings = [math.radians(b) for b in (90, 210, 330)]

def on_arm(ix, iz):
    # a tile is 'on an arm lane' if it lies within ~0.55 block of an arm ray from centre
    px, pz = ix + 0.5 - C, iz + 0.5 - C
    d = math.hypot(px, pz)
    if d < 0.6: return False
    ang = math.atan2(pz, px)
    for b in arm_bearings:
        da = abs((ang - b + math.pi) % (2*math.pi) - math.pi)
        if da * d < 0.6 and d > 0.8:   # narrow lane that widens slightly outward
            return True
    return False

# --- the radial disc apron: Bresenham-style circle fill, y0, dy=1 worn ground tiles ---
# ragged edge: columns near the rim roll 'revert to natural ground' (GRASS) ~35% so it bleeds out.
for iz in range(7):
    for ix in range(7):
        px, pz = ix + 0.5 - C, iz + 0.5 - C
        d = math.hypot(px, pz)
        if d > R + 0.55:      # outside the disc envelope entirely
            continue
        edge = d > (R - 0.85)
        h = (ix*2654435761 ^ iz*40503) & 0xff
        if edge and (h % 100) < 35:
            # reverted-to-grass ragged edge tile -- still a real ground block (grounded), just natural
            S.box(ix, iz, 0, 1, 1, 1, GRASS)
            continue
        col = PATH if on_arm(ix, iz) else pick(ix, iz)
        S.box(ix, iz, 0, 1, 1, 1, col, seam=False)

# --- 1-wide scatter ring of coarse/gravel one block out where feet pack the ground (grounded spill,
#     each abuts a disc tile face -- not floating debris) ---
for (ix, iz, col) in [(0,3,GRAVEL),(6,3,COARSE),(3,0,COARSE),(3,6,GRAVEL),(1,1,GRAVEL),(5,5,COARSE)]:
    S.box(ix, iz, 0, 1, 1, 0.5, col)    # half-height packed scatter (sunk, sits IN the ground)

# --- SLOT centre: trail-version CAIRN -- a tiny 2-3 stone wonky hand-stack on the apron (grounded) ---
# base stone half-buried into the apron top, off-centre middle stone (supported lean, inner half bears),
# opposite-offset mossy slab capstone -> the zig-zag silhouette that says 'waymarker'.
S.box(C-0.5, C-0.5, 1, 1, 1, 1, C_DARK, seam=True)          # base stone (rooted on apron top y1)
S.box(C-0.18, C-0.18, 2, 1, 1, 1, C_CORE, seam=True)        # middle, shoved off-centre (lean, supported)
S.box(C-0.45, C-0.5, 3, 0.9, 0.9, 0.5, C_MOSS)             # opposite-offset mossy slab capstone (zig-zag)

# --- SLOT arm-mouth (busiest arm, toward FRONT-east high-z so the viewer reads it): a single LEANING
#     sign_post on a cobblestone block, pointing down the arm. cobble footing grounds the lean. ---
sx, sz = 5, 5                                               # on the front-east arm mouth (high-z + high-x = visible)
S.box(sx, sz, 1, 1, 1, 1, COBB, seam=True)                 # cobblestone footing block (on apron top y1)
S.box(sx+0.35, sz+0.30, 2, 0.3, 0.3, 2, POST)             # leaning oak post (base bears on the cobble top)
S.box(sx+0.05, sz+0.55, 3.0, 1.0, 0.18, 0.7, SIGN)        # sign plank, pointing down the arm (front face)

S.label(C, C, 3.3, "centre slot: trail cairn (2-3 stone wonky hand-stack, unlit)")
S.label(sx+0.4, sz+0.5, 3.0, "arm-mouth slot: leaning sign_post on a cobble block")
S.label(0, 3, 1.0, "ragged edge -- ~35% reverts to grass, bleeds into ground (no rim)")
S.label(3.5, 0.5, 1.0, "3 arm lanes (dirt_path) keep their width, blend at the disc edge")

out = S.svg(title="Plaza R1 (Trail) -- a wider worn junction node + cairn waymarker, no rim / no light",
            size_label="~7x7 disc (r3) * h2 * 0 lanterns (ladder floor -- a footpath crossing that reads as 'a place')",
            label_w=352)
open("detail_svg/plaza_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/plaza_trail.svg | bytes", len(out.encode()))
