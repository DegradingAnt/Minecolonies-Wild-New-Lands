"""Plaza HIGHWAY (R4) -> detail_svg/plaza_highway.svg.
Per deco_catalog_v2.json id 'plaza' tier Highway (footprint radial disc r=13, ~27x27 envelope, on an
engineered pad + a stepped central DAIS, height 9): the GRAND content jump below the Great Road FORUM
top -- the first tier that reads as ARCHITECTURE. Gains: an engineered FOUNDATION sub-floor (no terrain
pokes through), a 2-wide chamfered kerb (stone_brick_stairs step you ascend + a proud smooth_stone_slab
inner course, broken at each arm), strong PER-ARM-GAP wedge spokes (polished_andesite vs smooth_stone),
a stepped octagonal-on-disc central DAIS (9x9 -> 7x7 -> 5x5, stair risers + chiseled treads), a per-arm
free-standing COLONNADE PILLAR ring (stone_brick_wall x3 + chiseled cap + lantern -- the first sense of a
built room edge), a GRAND roofed well on the dais (7x7 ring, 4 stripped_oak_log posts, a pitched dark_oak
hip roof + chiseled finial + hanging eave lanterns), per-arm WEDGE market clusters (a market_stall, a
bench group, a planter), banner_stands flanking the busy arms, and a notice_board at the main arm-mouth.

ESCALATION over Road (non-linear payoff #1): the leap is VERTICAL CONTENT -- engineered foundation +
stepped DAIS + colonnade pillar ring + roofed great-well + market wedges + notice board; lighting roughly
triples (~12-16). Sized at home beside the 19x15 gatehouse anchor. One step under the Great Road FORUM
(render_plaza.py, the full peristyle + pavilions + fountain spire). Same wnl_plaza builder; inspiration
(Roman market plaza + structurize great-well scale + MineColonies stepped-plinth/colonnade technique +
CTOV/D&T market-stall IDEA -> our ORIGINAL asymmetric single-rear-spine lean-to stall) credited in
CREDITS.md -- form/scale/technique only, no assets/NBT/layout copied.
ISO: road-facing detail (notice board, well bucket, banner) turned to the FRONT high-z for the viewer."""
import math
from iso_render import Iso

S = Iso(U=9)

# --- palette: formal HIGHWAY floor (smooth_stone / stone_bricks / polished_andesite); WIDE-CONTRAST
#     ladder so the dais, kerb, spokes, colonnade + roof never blend. CONTRAST-FLOOR rule (spokes read). ---
SMTH   = "#b0ada6"   # smooth_stone      -- ~20% (pale, the formal civic field)
SBRK   = "#8d877a"   # stone_bricks      -- ~25% (mid grey-brown laid stone)
PAND   = "#5f6166"   # polished_andesite -- ~15% DARK (the hi-contrast spoke/inlay block)
ANDE   = "#9a958c"   # andesite          -- ~15%
SLAB   = "#a39d90"   # stone_brick_slab[type=top] -- ~15% (lighter)
CUCO   = "#b9744a"   # cut_copper accent -- ~5% (oxidising warm copper, the one warm floor note)
WEATH  = "#736d61"   # mossy/cracked weathering -- ~5% (light, near-civ)
FOUND  = "#6f685d"   # engineered FOUNDATION sub-floor rim (dark -> reads as the cut-and-filled pad)
GRASS  = "#5f7d3f"   # feathered bank at the rim
# kerb (2-wide chamfered)
KSTAIR = "#857f73"   # stone_brick_stairs[facing=inward] outer chamfer step (you ascend onto it)
KSLAB  = "#b3ada0"   # smooth_stone_slab[type=top] inner proud course (light -> the kerb reads)
# central DAIS (stepped 9->7->5)
DRISER = "#857f73"   # stone_brick_stairs risers (the stepped faces)
DTREAD = "#b9b3a5"   # chiseled_stone_bricks treads (light -> each step reads)
# colonnade pillar ring (per-arm)
PWALL  = "#9a9487"   # stone_brick_wall shaft (x3)
PCAP   = "#c4beb0"   # chiseled_stone_bricks cap (light -> the capital reads)
# grand roofed well on the dais
WALL   = "#9a9487"   # stone_brick well ring (7x7)
WATER  = "#3a6ea5"   # water core
WLOG   = "#5a4426"   # stripped_oak_log corner posts (4 rising 4)
WROOF  = "#46382a"   # dark_oak_stairs pitched hip roof (dark warm)
WROOF2 = "#5a4b39"   # roof mid course (a touch lighter -> stepped read)
FIN    = "#cfc8b6"   # chiseled_stone_bricks finial
WCHAIN = "#5c5c5c"   # chain
# market wedge (ORIGINAL asymmetric single-rear-spine lean-to stall) + bench + planter
SPOST  = "#7a5c3a"   # oak_fence stall posts (warm)
SCOUNT = "#9a7b48"   # oak_slab counter on barrels
SBARR  = "#7a5c3a"   # barrels under the counter
SAWN   = "#5a4b39"   # single-pitch lean-to awning (stairs[half=bottom] facing forward)
GOODS  = "#8a6a3a"   # decorated_pot / composter goods
BSEAT  = "#9a7b48"   # bench seat
BFENCE = "#7a5c3a"   # bench back
PLANT  = "#6f5536"   # oak_trapdoor planter box
PSOIL  = "#4a3a22"   # dirt in the planter
PFOL   = "#5f8d3f"   # biome foliage (sapling/flower greenery)
# banner-stand + notice board + lanterns
SFENCE = "#5a4b39"   # spruce_fence banner posts
BANNER = "#a83a31"   # banner cloth
BANNERD= "#7e2a23"   # banner shadow fold
SBASE  = "#9a9487"   # stone_brick base / notice frame
NOTICE = "#caa86a"   # supplementaries:notice_board face (warm parchment-ish)
LANT   = "#ffd47a"   # lantern glow

C = 13.0   # junction centre on a 0..26 grid (disc radius 13 -> envelope ~27x27)
R = 13.0

def pick(ix, iz):
    h = (ix*73856093 ^ iz*19349663) & 0xffff
    r = h % 100
    if r < 20: return SMTH
    if r < 45: return SBRK
    if r < 60: return ANDE   # PAND reserved for the spoke/inlay geometry (keep the field readable)
    if r < 75: return SLAB
    if r < 90: return ANDE
    if r < 95: return CUCO
    return WEATH

# N=4 arms (busy 4-way). Bearings drive kerb breaks, 4 spokes/wedges, 4 colonnade pillars, lamp count.
arm_bearings = sorted(math.radians(b) for b in (35, 125, 215, 305))
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

# --- engineered FOUNDATION sub-floor + radial apron r=13. Foundation rim feathers into banks. ---
DAIS_R = 2.6   # dais occupies the centre; floor tiles skip under it (the dais sits ON the apron)
for iz in range(27):
    for ix in range(27):
        px, pz = ix + 0.5 - C, iz + 0.5 - C
        d = math.hypot(px, pz)
        if d > R + 0.55:
            continue
        if d < DAIS_R:
            continue   # centre reserved for the dais (drawn below, grounded on the apron under it)
        h = (ix*2654435761 ^ iz*40503) & 0xff
        edge = d > (R - 1.85)        # 2-wide kerb band
        is_arm = near_bearing(ix, iz, arm_bearings, 0.55, 2.5)
        if edge and not is_arm:
            if d > (R - 0.3) and (h % 100) < 12:
                S.box(ix, iz, -1, 1, 1, 1, FOUND)            # feathered foundation bank (sub-floor, sunk)
                S.box(ix, iz, 0, 1, 1, 1, GRASS)             # grass feather over the bank rim
                continue
            if d > (R - 1.0):
                S.box(ix, iz, 0, 1, 1, 1, KSTAIR)            # outer chamfered stair step (ascend onto)
            else:
                S.box(ix, iz, 0, 1, 1, 1, KSLAB)             # inner proud smooth_stone_slab course
                S.box(ix, iz, 1, 1, 1, 0.5, KSLAB)           # proud (1 notch up)
            continue
        # per-arm SPOKES/WEDGE dividers: a strong polished_andesite vs smooth_stone radial line
        if near_bearing(ix, iz, spoke_bearings, 0.42, 3.0, R - 1.2):
            S.box(ix, iz, 0, 1, 1, 1, PAND)
            continue
        col = pick(ix, iz)
        # foundation reads under the whole disc: drop a dark sub-floor course under every apron tile
        S.box(ix, iz, -1, 1, 1, 1, FOUND)
        S.box(ix, iz, 0, 1, 1, 1, col)

# --- stepped central DAIS (9x9 -> 7x7 -> 5x5, 2 courses), grounded on the apron (y0 top = y1 base).
#     risers = stair faces (DRISER), treads = chiseled (DTREAD). A true buildable step plinth. ---
def dais_course(side, y):
    h = side/2.0
    S.box(C-h, C-h, y, side, side, 1, DRISER)               # riser body (full course, supported below)
    S.box(C-h+0.1, C-h+0.1, y+1, side-0.2, side-0.2, 0.18, DTREAD)  # chiseled tread lip (reads the step)
dais_course(9, 1)
dais_course(7, 2)
dais_course(5, 3)

# --- per-arm COLONNADE PILLAR ring: at each spoke bearing on the dais-edge ring, a free-standing
#     pillar (stone_brick_wall x3 + chiseled cap + lantern). First sense of a built room edge. ---
pillar_glows = []
PILL_R = 6.5
for b in spoke_bearings:
    lx = int(round(C + PILL_R * math.cos(b) - 0.5))
    lz = int(round(C + PILL_R * math.sin(b) - 0.5))
    S.box(lx, lz, 1, 1, 1, 3, PWALL, seam=True)             # stone_brick_wall shaft x3 (on apron top y1)
    S.box(lx-0.1, lz-0.1, 4, 1.2, 1.2, 0.5, PCAP)           # chiseled cap (proud capital)
    pillar_glows.append((lx + 0.5, lz + 0.5, 4.7))

# --- GRAND roofed WELL on the dais (7x7 ring + water + 4 stripped_oak_log posts + dark_oak hip roof
#     + chiseled finial + hanging eave lanterns). Sits ON the 5x5 dais top (y4). ~7x7x8. ---
WB = 4   # well base y (top of the dais)
for ox in range(7):
    for oz in range(7):
        if ox in (0,6) or oz in (0,6):
            S.box(C-3+ox, C-3+oz, WB, 1, 1, 1.6, WALL, seam=True)   # 7x7 stone_brick ring
S.box(C-2.5, C-2.5, WB, 5, 5, 0.6, WATER)                   # water core inside the ring
for (px, pz) in [(C-3,C-3),(C+2,C-3),(C-3,C+2),(C+2,C+2)]:
    S.box(px, pz, WB+1.4, 1, 1, 4, WLOG)                    # 4 stripped_oak_log posts rising 4 (on ring)
# dark_oak hip roof (stepped, each course supported by the one below + the 4 posts): 7x7 -> 5x5 -> finial
S.box(C-3.4, C-3.4, WB+5.4, 7.8, 7.8, 0.7, WROOF)          # eave (proud overhang on the 4 posts)
S.box(C-2.5, C-2.5, WB+6.1, 5, 5, 0.7, WROOF2)             # mid pitch (lighter -> stepped)
S.box(C-1.5, C-1.5, WB+6.8, 3, 3, 0.7, WROOF)              # upper pitch
S.box(C-0.5, C-0.5, WB+7.5, 1, 1, 0.9, FIN)               # chiseled finial
# hanging chain + eave lanterns under the roof on the front (high-z), grounded by chains
for (cx, cz) in [(C-2.0, C+2.6), (C+2.0, C+2.6)]:
    S.box(cx, cz, WB+4.6, 0.16, 0.16, 0.8, WCHAIN)         # chain from eave underside
    pillar_glows.append((cx+0.08, cz+0.08, WB+4.5))        # eave lantern (reuse the glow list)

# --- per-arm WEDGE market clusters: a market_stall (ORIGINAL asymmetric lean-to) + bench + planter.
#     Place clusters in the front wedges (high-z) so they read; grounded on the apron. ---
def market_stall(sx, sz):
    # ORIGINAL signature: 2 back corner posts + ONE offset front post (asymmetric), counter on barrels,
    # SINGLE-PITCH lean-to awning sloping toward the open front. Distinct from symmetric 4-post stalls.
    S.box(sx, sz-2, 1, 0.3, 0.3, 3, SPOST)                 # back-left post (rear spine)
    S.box(sx+2.7, sz-2, 1, 0.3, 0.3, 3, SPOST)            # back-right post (rear spine)
    S.box(sx+0.4, sz+0.7, 1, 0.3, 0.3, 2.4, SPOST)        # ONE front post offset to one side (asymmetric)
    # counter = oak_slab on a row of barrels along the front edge
    for bx in (sx, sx+1, sx+2):
        S.box(bx, sz, 1, 0.9, 0.9, 1, SBARR, seam=True)   # barrels (front counter base, grounded)
    S.box(sx, sz, 2, 3, 1, 0.3, SCOUNT)                    # oak_slab counter on the barrels
    # SINGLE-PITCH lean-to awning: a row of stairs sloping from the high back posts toward the open front
    S.box(sx-0.2, sz-2, 4, 3.4, 0.8, 0.4, SAWN)           # awning back edge (on the 2 back posts, high)
    S.box(sx-0.2, sz-1, 3.5, 3.4, 1.0, 0.4, SAWN)         # awning mid (sloping down toward front)
    S.box(sx-0.2, sz+0.0, 3.0, 3.4, 1.0, 0.4, SAWN)       # awning front lip (lowest -> single pitch)
    # goods on the counter + a wall_banner hint on the back-left post
    S.box(sx+0.6, sz+0.1, 2.3, 0.6, 0.6, 0.8, GOODS)      # decorated_pot/composter goods
    S.box(sx, sz-2, 2.0, 0.4, 0.5, 1.2, BANNER)           # wall_banner on the back-left post

def bench_group(bx, bz):
    S.box(bx, bz, 1, 2, 0.6, 0.5, BSEAT)                   # seat run
    S.box(bx, bz-0.7, 1, 2, 0.3, 1.2, BFENCE)            # fence back behind the seat (grounded)

def planter(px, pz):
    S.box(px, pz, 1, 1.4, 1.4, 0.8, PLANT)                # oak_trapdoor box (on apron top y1)
    S.box(px+0.15, pz+0.15, 1.7, 1.1, 1.1, 0.2, PSOIL)   # dirt fill
    S.box(px+0.45, pz+0.45, 1.9, 0.5, 0.5, 0.9, PFOL)    # biome foliage sprig

# front-right wedge: full market stall
market_stall(17, 20)
# front-left wedge: bench group + planter
bench_group(6, 20)
planter(9, 21)
# a planter in the right wedge too
planter(20, 16)

# --- banner_stands flanking the 2 busiest arms (front), + notice_board at the main arm-mouth (front) ---
for (gx, gz) in [(10, 22), (15, 22)]:
    S.box(gx, gz, 1, 0.4, 0.4, 3, SFENCE)                 # spruce_fence banner post (on apron)
    S.box(gx-0.05, gz+0.4, 2.2, 0.7, 0.18, 1.6, BANNER)  # banner cloth facing the avenue (front)
    S.box(gx-0.05, gz+0.55, 2.2, 0.7, 0.12, 1.6, BANNERD)# shadow fold
# notice_board on a stone_brick frame at the main arm-mouth (front-east, high-z + high-x)
nx, nz = 19, 23
S.box(nx, nz, 1, 0.5, 0.5, 2.5, SBASE)                    # left frame post
S.box(nx+1.6, nz, 1, 0.5, 0.5, 2.5, SBASE)              # right frame post
S.box(nx, nz+0.35, 2.0, 2.1, 0.2, 1.3, NOTICE)          # notice_board face (turned to the road)
S.box(nx-0.1, nz+0.25, 3.3, 2.3, 0.3, 0.3, SBASE)       # stone_brick lintel cap over the board

# --- ACCENTS: ~12-16 lanterns -- N kerb-spoke + N colonnade pillar + hanging well-eave lanterns ---
# kerb lamp-posts at each spoke bearing where it meets the kerb (component reuse)
for b in spoke_bearings:
    lx = C + (R - 1.4) * math.cos(b)
    lz = C + (R - 1.4) * math.sin(b)
    # a small grounded post + lantern at the kerb (cobblestone_wall x2 component, drawn minimal)
    ix, iz = int(round(lx-0.5)), int(round(lz-0.5))
    S.box(ix, iz, 1, 1, 1, 2, PWALL, seam=True)           # kerb lamp post (grounded on the kerb tile)
    S.accent(ix+0.5, iz+0.5, 3.25, "glow", LANT, r=2.0)   # kerb lantern
for (gx2, gz2, gy2) in pillar_glows:
    S.accent(gx2, gz2, gy2, "glow", LANT, r=2.0)          # colonnade-pillar + well-eave lanterns
S.accent(C, C, WB+5.0, "glow", "#eafff8", r=2.4)          # soft glow reading the well water/bucket

S.label(C, C, WB+7.5, "GRAND roofed well on the stepped dais (4 log posts + hip roof + finial)")
S.label(pillar_glows[1][0], pillar_glows[1][1], 4.8, "per-arm COLONNADE pillars + lanterns (a room edge)")
S.label(17, 20, 4.2, "market WEDGE -- original asymmetric single-pitch lean-to stall")
S.label(C+3, C-3, 3.2, "stepped octagonal DAIS (9->7->5, stair risers + chiseled treads)")
S.label(0.5, 13, 1.2, "engineered foundation + 2-wide chamfered kerb (ascend onto)")
S.label(nx+0.8, nz+0.4, 3.0, "notice_board at the main arm-mouth (wayfinding)")
S.label(10, 22, 2.4, "banner_stands flank the busy arms")

out = S.svg(title="Plaza R4 (Highway) -- a genuine MARKET plaza: engineered pad + stepped dais, colonnade pillar ring, roofed great-well, per-arm market wedges",
            size_label="~27x27 disc (r13) on a pad + dais * h9 * ~14 lanterns (first ARCHITECTURE -- one step under the Great Road FORUM)",
            label_w=384)
open("detail_svg/plaza_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/plaza_highway.svg | bytes", len(out.encode()))
