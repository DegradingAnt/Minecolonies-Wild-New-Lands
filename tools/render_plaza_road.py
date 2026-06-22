"""Plaza ROAD (R3) -> detail_svg/plaza_road.svg.
Per deco_catalog_v2.json id 'plaza' tier Road (footprint radial disc r=7, ~17x17 envelope w/ a defined
kerb ring + radial banding, height 6): the BIG content jump from Path. The floor gains DESIGNED GEOMETRY
-- a stone-brick laid scatter, a real PROUD kerb ring (stone_brick_slab one notch up, BROKEN at each of
the N arms), an inlaid contrast BAND 2 in from the kerb (polished_andesite vs stone_bricks), and PER-ARM
SPOKES (one polished_andesite spoke bisects each gap between consecutive arm bearings). Lighting goes from
1 lantern to a lit RING of N cobblestone_wall LAMP POSTS at the spoke bearings. The centre well grows a
ROOF (an original draw-well: 5x5 stone-brick ring, water, 4 oak_log corner posts, a pitched spruce_stairs
cap, chain + cauldron bucket). Arm-gaps carry a rest_stop (campfire + barrels + stumps) + a bench cluster;
the busiest arm-mouth gets a banner_stand (twin spruce_fence + a banner pair on a stone_brick base).

ESCALATION over Path: first DESIGNED floor geometry (banded disc + per-arm spokes + a real proud kerb),
the well grows a ROOF + first vertical structure, lighting 1 -> a lit ring of N posts, 3 reused components
populate it. The 'proper road' payoff rung -- first true civic reading. The leaps above (Highway/Great
Road) are vertical CONTENT (dais, colonnade, market quarter), not width. Same wnl_plaza builder as
render_plaza.py (Great Road FORUM); inspiration (Roman roadside + market-cross + structurize draw-well
technique) credited in CREDITS.md -- form/technique only, no assets/NBT/layout copied.
ISO: road-facing detail (banner-stand, well bucket) turned to the FRONT high-z so the viewer reads it."""
import math
from iso_render import Iso

S = Iso(U=12)

# --- palette: stone-brick laid ROAD floor; WIDE-CONTRAST ladder so banding + spokes always read ---
SBRK   = "#8d877a"   # stone_bricks      -- ~25% majority (the laid civic floor)
COBB   = "#7c766a"   # cobblestone       -- ~20% (mid grey-brown)
ANDE   = "#9a958c"   # andesite          -- ~15% (pale grey)
SLAB   = "#a39d90"   # cobblestone_slab[type=top] worn-flat -- ~15% (lighter)
GRAVEL = "#8f8a80"   # gravel            -- ~10%
MOSSB  = "#6f7d56"   # mossy_stone_bricks-- ~10% (green character)
CRACK  = "#736d61"   # cracked_stone_bricks -- ~5% (darker character)
GRASS  = "#5f7d3f"   # ragged-edge revert (now only a touch, the disc is mostly defined)
# floor GEOMETRY (the signature begins): proud kerb + contrast band + spokes
KERB   = "#b3ada0"   # stone_brick_slab kerb ring, set 1 notch PROUD (light -> the kerb reads strong)
PAND   = "#5f6166"   # polished_andesite inlay (DARK -> hi-contrast vs the pale floor: band + spokes)
# ROOFED draw-well component
WALL   = "#9a9487"   # stone_brick ring of the well (the kerb of the well)
WATER  = "#3a6ea5"   # water core
WLOG   = "#6f5536"   # oak_log corner posts (warm timber, 4 rising)
WROOF  = "#5a4b39"   # spruce_stairs pitched cap (dark warm roof, the first ROOF)
WCHAIN = "#5c5c5c"   # chain
WBUCK  = "#8a8a8a"   # cauldron bucket (iron grey)
FIN    = "#b9b3a5"   # chiseled finial-ish cap stone
# lamp posts (N), rest_stop, bench, banner-stand
LPOST  = "#7c766a"   # cobblestone_wall lamp post (x2)
LANT   = "#ffd47a"   # lantern glow
CFIRE  = "#d8772f"   # campfire embers (warm)
BARREL = "#7a5c3a"   # barrels
STUMP  = "#6f5536"   # oak_log stump
BSEAT  = "#9a7b48"   # oak_stairs/oak_slab bench seat
BFENCE = "#7a5c3a"   # oak_fence back
SFENCE = "#5a4b39"   # spruce_fence banner posts (darker)
BANNER = "#a83a31"   # banner cloth (the one saturated accent)
BANNERD= "#7e2a23"   # banner shadow fold
SBASE  = "#9a9487"   # stone_brick banner base

C = 7.0   # junction centre on a 0..14 grid (disc radius 7 -> envelope ~15x15)
R = 7.0

def pick(ix, iz):
    h = (ix*73856093 ^ iz*19349663) & 0xffff
    r = h % 100
    if r < 25: return SBRK
    if r < 45: return COBB
    if r < 60: return ANDE
    if r < 75: return SLAB
    if r < 85: return GRAVEL
    if r < 95: return MOSSB
    return CRACK

# N=3 arms (busy 3-way). Bearings drive: kerb breaks (at arms), spokes (gap-bisectors), lamp posts
# (at spoke bearings), rest_stop/bench (arm-gaps), banner (busiest arm = first bearing).
arm_bearings = sorted(math.radians(b) for b in (70, 195, 315))
# spoke bearings = bisector of each consecutive arm-gap (wraps around)
spoke_bearings = []
for i in range(len(arm_bearings)):
    a0 = arm_bearings[i]; a1 = arm_bearings[(i+1) % len(arm_bearings)]
    if a1 < a0: a1 += 2*math.pi
    spoke_bearings.append(((a0 + a1) / 2) % (2*math.pi))

def near_bearing(ix, iz, bearings, tol_arc, dmin, dmax=99):
    px, pz = ix + 0.5 - C, iz + 0.5 - C
    d = math.hypot(px, pz)
    if d < dmin or d > dmax: return False
    ang = math.atan2(pz, px)
    for b in bearings:
        da = abs((ang - b + math.pi) % (2*math.pi) - math.pi)
        if da * d < tol_arc:
            return True
    return False

# --- radial disc apron r=7, y0 dy=1; arms break the floor pattern; mostly defined (little ragged) ---
for iz in range(15):
    for ix in range(15):
        px, pz = ix + 0.5 - C, iz + 0.5 - C
        d = math.hypot(px, pz)
        if d > R + 0.55:
            continue
        h = (ix*2654435761 ^ iz*40503) & 0xff
        edge = d > (R - 0.85)
        is_arm = near_bearing(ix, iz, arm_bearings, 0.6, 1.5)
        if edge and not is_arm:
            if (h % 100) < 15:
                S.box(ix, iz, 0, 1, 1, 1, GRASS)             # slight ragged revert
                continue
            S.box(ix, iz, 0, 1, 1, 1, KERB)                  # base under the proud kerb slab (full block)
            S.box(ix, iz, 1, 1, 1, 0.5, KERB)                # PROUD kerb slab (1 notch up -> reads as a kerb)
            continue
        # contrast BAND ring 2 blocks in from the kerb (alternating polished_andesite / stone_bricks)
        if (R - 2.6) < d <= (R - 1.4) and not is_arm:
            col = PAND if ((ix + iz) % 2 == 0) else SBRK
            S.box(ix, iz, 0, 1, 1, 1, col)
            continue
        # per-arm SPOKES (polished_andesite line from centre to kerb, one per arm-gap bisector)
        if near_bearing(ix, iz, spoke_bearings, 0.5, 2.2, R - 0.6):
            S.box(ix, iz, 0, 1, 1, 1, PAND)
            continue
        S.box(ix, iz, 0, 1, 1, 1, pick(ix, iz))

# --- SLOT centre: ROOFED draw-well (5x5 stone_brick ring + water + 4 oak_log posts + pitched cap) ---
# ring (hollow 5x5 perimeter), grounded on apron top y1
for ox in range(5):
    for oz in range(5):
        if ox in (0,4) or oz in (0,4):
            S.box(C-2+ox, C-2+oz, 1, 1, 1, 1.4, WALL, seam=True)
S.box(C-1.5, C-1.5, 1, 3, 3, 0.6, WATER)                     # water core inside the ring
# 4 oak_log corner posts rising 3 from the ring corners (grounded on the ring tops)
for (px, pz) in [(C-2,C-2),(C+1,C-2),(C-2,C+1),(C+1,C+1)]:
    S.box(px, pz, 2.4, 1, 1, 3, WLOG)
# --- pitched spruce_stairs cap (well-cap technique: stepped, each course supported by the one below
#     + the 4 log posts) -- eave 5x5 -> 3x3 ridge band -> 1x1 finial. NO floats. ---
S.box(C-2.3, C-2.3, 5.4, 5.6, 5.6, 0.6, WROOF)               # eave course (proud overhang on the 4 posts)
S.box(C-1.5, C-1.5, 6.0, 3, 3, 0.6, WROOF)                   # mid pitch (3x3 ridge band)
S.box(C-0.5, C-0.5, 6.6, 1, 1, 0.8, FIN)                     # chiseled_stone_bricks finial
# chain + cauldron bucket hung UNDER the eave on the front (road-facing high-z), grounded by the chain
S.box(C+0.0, C+1.4, 4.4, 0.18, 0.18, 1.0, WCHAIN)            # chain from the eave underside
S.box(C-0.15, C+1.25, 4.1, 0.5, 0.5, 0.4, WBUCK)            # cauldron bucket on the chain (over the water)

# --- SLOT lamp anchors: N cobblestone_wall LAMP POSTS at the spoke bearings where they meet the kerb.
#     each post = 2x cobblestone_wall + a lantern on top (grounded ring). ---
lamp_glows = []
for b in spoke_bearings:
    lx = int(round(C + (R - 1.2) * math.cos(b) - 0.5))
    lz = int(round(C + (R - 1.2) * math.sin(b) - 0.5))
    S.box(lx, lz, 1, 1, 1, 1, LPOST, seam=True)              # post lower (on apron top y1)
    S.box(lx, lz, 2, 1, 1, 1, LPOST, seam=True)              # post upper (2x wall)
    lamp_glows.append((lx + 0.5, lz + 0.5, 3.25))

# --- SLOT per-arm-gap: a REST_STOP (campfire + 2 barrels + a stump) + a bench cluster, in the
#     gaps not carrying the busy milestone. Placed toward the FRONT (high-z) so they read. ---
# rest_stop (front-left gap)
rx, rz = 4, 11
S.box(rx, rz, 1, 1, 1, 0.4, STUMP)                           # campfire log base (on apron top y1)
S.box(rx+1.1, rz-0.1, 1, 1, 1, 1, BARREL, seam=True)         # barrel 1 (abuts the campfire)
S.box(rx+1.1, rz+0.95, 1, 1, 1, 1, BARREL, seam=True)        # barrel 2 (chained to barrel 1)
S.box(rx-0.9, rz+0.2, 1, 0.9, 0.9, 1, STUMP)                # oak_log stump (abuts the campfire west)
# bench cluster (front-right gap): oak_stairs seat + oak_slab + oak_fence back
bx, bz = 10, 11
S.box(bx, bz, 1, 2, 0.6, 0.5, BSEAT)                         # seat run (stairs+slab), on apron top
S.box(bx, bz-0.7, 1, 2, 0.3, 1.2, BFENCE)                   # oak_fence back (grounded behind the seat)

# --- SLOT busiest arm-mouth: BANNER_STAND -- twin spruce_fence posts + a banner pair on a stone_brick
#     base. On the front-east arm mouth (high-z + high-x so the heraldry faces the viewer). ---
gx, gz = 11, 12
S.box(gx, gz, 1, 2, 1, 0.5, SBASE)                           # stone_brick base (on apron top y1)
S.box(gx, gz, 1.5, 0.4, 0.4, 3, SFENCE)                     # left spruce_fence post (on the base)
S.box(gx+1.6, gz, 1.5, 0.4, 0.4, 3, SFENCE)                # right spruce_fence post
# banner pair hung between the posts, facing the avenue (front, high-z); 2-tone drape
S.box(gx+0.1, gz+0.35, 2.6, 0.7, 0.18, 1.7, BANNER)         # left banner cloth (front face)
S.box(gx+0.1, gz+0.5, 2.6, 0.7, 0.12, 1.7, BANNERD)        # shadow fold
S.box(gx+1.0, gz+0.35, 2.6, 0.7, 0.18, 1.7, BANNER)        # right banner cloth
S.box(gx+1.0, gz+0.5, 2.6, 0.7, 0.12, 1.7, BANNERD)

# --- ACCENTS: the lit RING (N lamp posts) + well + rest-stop campfire glow (~N+2 lights) ---
for (gx2, gz2, gy2) in lamp_glows:
    S.accent(gx2, gz2, gy2, "glow", LANT, r=2.2)            # lamp-post lanterns (the lit ring)
S.accent(C+0.0, C+1.4, 4.5, "glow", "#eafff8", r=2.0)       # soft glow reading the well bucket/water
S.accent(rx+0.5, rz+0.5, 1.6, "glow", CFIRE, r=2.4)         # rest_stop campfire (warm embers)

S.label(C, C, 6.6, "centre: ROOFED draw-well (ring + 4 log posts + pitched cap + chain bucket)")
S.label(lamp_glows[0][0], lamp_glows[0][1], 3.3, "lit RING -- N cobblestone_wall lamp posts at spoke bearings")
S.label(0.5, 7, 1.5, "PROUD kerb ring (stone_brick_slab, broken at each arm)")
S.label(11, 4, 0.5, "contrast band + per-arm polished_andesite SPOKES (floor geometry)")
S.label(rx, rz, 1.6, "rest_stop (campfire + barrels + stump) in an arm-gap")
S.label(gx+0.8, gz+0.4, 2.8, "banner_stand at the busiest arm-mouth")

out = S.svg(title="Plaza R3 (Road) -- a proper laid plaza: banded radial floor + kerb + per-arm spokes, ROOFED draw-well, lit ring of N posts",
            size_label="~15x15 disc (r7) * h6 * 5 lanterns (DESIGNED floor geometry + first roof + first lit ring -- the road payoff)",
            label_w=372)
open("detail_svg/plaza_road.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/plaza_road.svg | bytes", len(out.encode()))
