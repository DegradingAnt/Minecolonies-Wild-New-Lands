"""Plaza PATH (R2) -> detail_svg/plaza_path.svg.
Per deco_catalog_v2.json id 'plaza' tier Path (footprint radial disc r=5, ~11x11 envelope, height 3):
a modest step from Trail (+2 radius). The node becomes a REAL defined place: scatter shifts up-material
(cobblestone-led, worn-flat cobble slabs), a SOFTLY defined 1-wide cobblestone RIM (only ~25% reverts to
natural, less ragged than Trail), embedded flush flagstones (cobble slabs) + a couple of moss_carpet
overgrowth patches. Centre SLOT (hash 50/50): a small UNROOFED well (5x5 cobblestone_wall ring + water
core + 2 oak_fence posts + a quarter oak_slab lid -- the FIRST reused 'real' component) -- drawn here.
Per-arm-gap SLOT (2 widest gaps): a bench hint (oak_stairs seat + an oak_fence lean-post behind).
Arm-mouth SLOT (busiest arm): milestone -- a stone post (2x cobblestone) + sign_post + the FIRST LIGHT
(one lantern on top).

ESCALATION over Trail: first laid stone RIM, first single LANTERN, first reused 'real' component
(the small unroofed well). Still humble light construction -- the big leaps are saved for Road/Highway
(non-linear ladder). Same wnl_plaza data builder as render_plaza.py (Great Road FORUM top tier);
inspiration (medieval market-cross-at-a-crossing, original well+sign arrangement) credited in CREDITS.md."""
import math
from iso_render import Iso

S = Iso(U=15)

# --- palette: up-material PATH ground (cobble-led), WIDE-CONTRAST ladder so each block reads ---
COBB   = "#857f73"   # cobblestone   -- the ~30% majority now (laid stone, mid grey-brown)
PATH   = "#8a7142"   # dirt_path     -- ~20% (warm tan lane)
GRAVEL = "#9a958c"   # gravel        -- ~20% (pale loose stone)
SLAB   = "#9b9487"   # cobblestone_slab[type=top] worn-flat -- ~10% (lighter, the polished-by-feet look)
COARSE = "#6f5c40"   # coarse_dirt   -- ~15% (warm brown, the bare patch)
MOSS   = "#6f7d56"   # mossy_cobblestone / moss_carpet accent -- ~5% (green overgrowth)
RIM    = "#736d61"   # cobblestone RIM ring (darker -> the soft kerb reads as a defined edge)
GRASS  = "#5f7d3f"   # natural ground the (now softer) ragged edge reverts to
# well component (path/small, UNROOFED)
WALL   = "#7c766a"   # cobblestone_wall ring (the well kerb)
WATER  = "#3a6ea5"   # water core (the one cool note -- reads as the well)
WPOST  = "#7a5c3a"   # oak_fence posts (warm timber)
LID    = "#9a7b48"   # oak_slab[type=top] quarter-lid
# bench hint + milestone
BSEAT  = "#9a7b48"   # oak_stairs seat
BBACK  = "#7a5c3a"   # oak_fence lean-post behind
MPOST  = "#857f73"   # milestone cobblestone post (2x)
SIGN   = "#9a7b48"   # sign_post plank
LANT   = "#ffd47a"   # lantern glow (FIRST light)

C = 5.0   # junction centre on a 0..10 grid (disc radius 5 -> envelope ~11x11)
R = 5.0

def pick(ix, iz):
    h = (ix*73856093 ^ iz*19349663) & 0xffff
    r = h % 100
    if r < 30: return COBB
    if r < 50: return PATH
    if r < 70: return GRAVEL
    if r < 80: return SLAB
    if r < 95: return COARSE
    return MOSS

# N=3 arms (busy 3-way), bearings drive the 2-widest-gap bench slots + the busiest arm milestone
arm_bearings = [math.radians(b) for b in (75, 200, 320)]
def on_arm(ix, iz):
    px, pz = ix + 0.5 - C, iz + 0.5 - C
    d = math.hypot(px, pz)
    if d < 1.0: return False
    ang = math.atan2(pz, px)
    for b in arm_bearings:
        da = abs((ang - b + math.pi) % (2*math.pi) - math.pi)
        if da * d < 0.7 and d > 1.2:
            return True
    return False

# --- radial disc apron r=5, y0 dy=1; softer ragged edge (only ~25% revert), arm lanes read through ---
for iz in range(11):
    for ix in range(11):
        px, pz = ix + 0.5 - C, iz + 0.5 - C
        d = math.hypot(px, pz)
        if d > R + 0.55:
            continue
        h = (ix*2654435761 ^ iz*40503) & 0xff
        edge = d > (R - 0.85)
        if edge:
            if (h % 100) < 25:
                S.box(ix, iz, 0, 1, 1, 1, GRASS)          # softer ragged revert (grounded grass tile)
                continue
            S.box(ix, iz, 0, 1, 1, 1, RIM)                # 1-wide cobblestone RIM ring (the soft kerb)
            continue
        col = PATH if on_arm(ix, iz) else pick(ix, iz)
        S.box(ix, iz, 0, 1, 1, 1, col)

# --- embedded flush FLAGSTONES (cobble slabs part-laid) + moss_carpet overgrowth near rim ---
# each is a thin slab seated flush ON a disc tile top (grounded, part of the floor, not raised debris).
for (ix, iz) in [(3,4),(6,3),(4,7),(7,6),(2,6),(6,8)]:
    S.box(ix, iz, 1, 0.9, 0.9, 0.18, SLAB)               # flush flagstone (sits flat on the apron)
for (ix, iz) in [(1,4),(8,7),(4,1)]:
    S.box(ix, iz, 1, 0.8, 0.8, 0.1, MOSS)                # moss_carpet patch near the rim (overgrowth)

# --- SLOT centre: small UNROOFED WELL -- 5x5 cobblestone_wall ring + water core + 2 fence posts +
#     a quarter oak_slab lid. ~5x5x4. Sits ON the apron (ring base bears on tile tops y1). ---
# wall ring (hollow 5x5: place the 16 perimeter columns, leave the centre open for water)
for ox in range(5):
    for oz in range(5):
        if ox in (0,4) or oz in (0,4):
            S.box(C-2+ox, C-2+oz, 1, 1, 1, 1.6, WALL, seam=True)   # cobblestone_wall ring (1.6 tall kerb)
S.box(C-1.5, C-1.5, 1, 3, 3, 0.7, WATER)                 # water core (recessed inside the ring)
# 2 oak_fence posts at the back two corners rising over the ring (the winch frame hint, unroofed)
S.box(C-2, C-2, 2.6, 1, 1, 2, WPOST)                     # back-west post
S.box(C+1, C-2, 2.6, 1, 1, 2, WPOST)                     # back-east post
S.box(C-2, C-2, 4.6, 3, 0.5, 0.4, LID)                   # a quarter oak_slab lid spanning the two posts (rests on both)

# --- SLOT per-arm-gap (2 widest gaps): a BENCH HINT -- oak_stairs seat + oak_fence lean-post behind.
#     Placed toward FRONT-east (high-z, visible) and one to the left, grounded on the apron. ---
for (bx, bz, face) in [(7, 8, 'front'), (2, 7, 'left')]:
    S.box(bx, bz, 1, 1, 0.6, 0.5, BSEAT)                 # oak_stairs seat (low, sits on apron top)
    S.box(bx, bz-0.7, 1, 1, 0.3, 1.3, BBACK)            # oak_fence lean-post BEHIND the seat (grounded)

# --- SLOT busiest arm-mouth: MILESTONE -- 2x cobblestone post + sign_post + the FIRST LANTERN on top.
#     On the front-east arm mouth (high-z + high-x so the viewer reads it). ---
mx, mz = 8, 8
S.box(mx, mz, 1, 1, 1, 1, MPOST, seam=True)              # cobblestone post lower (on apron top y1)
S.box(mx, mz, 2, 1, 1, 1, MPOST, seam=True)              # cobblestone post upper (2x stone post)
S.box(mx+0.05, mz+0.55, 3.0, 1.0, 0.18, 0.7, SIGN)       # sign_post plank pointing down the arm (front)
# lantern seated ON the post top (grounded on the y3 top face)
S.accent(mx+0.5, mz+0.5, 3.25, "glow", LANT, r=2.4)

S.label(C, C, 4.8, "centre slot: small UNROOFED well (wall ring + water + posts + lid)")
S.label(mx+0.5, mz+0.5, 3.3, "milestone arm-mouth: post + sign + FIRST lantern")
S.label(7, 8, 1.6, "bench hints in the 2 widest arm-gaps (stairs seat + fence back)")
S.label(0.5, 5, 1.0, "soft cobblestone RIM (only ~25% reverts -> a defined edge now)")
S.label(3, 4, 1.2, "embedded flush flagstones + moss_carpet overgrowth")

out = S.svg(title="Plaza R2 (Path) -- a defined node: soft rim, flagstones, small unroofed well, bench hints, FIRST light",
            size_label="~11x11 disc (r5) * h3 * 1 lantern (first laid rim + first single light + first reused well)",
            label_w=360)
open("detail_svg/plaza_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/plaza_path.svg | bytes", len(out.encode()))
