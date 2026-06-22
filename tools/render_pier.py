"""Pier R5 (Great Road tier = Road / stone_jetty + wnl_dock_shack) detail render -> detail_svg/pier.svg.
The pier's NON-LINEAR ceiling: a railed working jetty thrust out over open water on a marching row
of DRIVEN PILE BENTS (paired posts to the riverbed + a cross-cap beam the deck rests on -- the deck
is plainly CARRIED, never floating), a stone-brick deck with a cobblestone-wall balustrade + capped
newel posts, lamp-post stations, a seaward embarkation landing with two mooring bollards + a moored
boat tied off by an iron line, AND a whole roofed shore BUILDING (the wnl_dock_shack satellite:
timber-cornered, stepped spruce-stair gable, seaward boathouse mouth, on the bank at deck level).
A 2-dweller working dock — it stops being "a walkway" and becomes "a little working dock".

Reality pass: bed=y1, waterline=y2, deck-top=y5 -> a clear open band of visible piling stands above
the water at every bent, so the deck reads as a real pile-and-plank staithe resting on its posts.

Credit: pile-and-plank jetty technique + rotted-board grammar inspired by Moog's Paths jetties and
real medieval timber fishing-staithes (the stepped-stair gable boathouse). Studied for FORM/TECHNIQUE
only; built entirely in vanilla blocks as original WNL work (see CREDITS.md). No copied build/NBT.

Layout convention (matches iso_render): x = right, z = depth (z=0 at BACK = the bank/shore),
y = up. The bank + dock-shack sit at the BACK (low z); the deck marches FORWARD (rising z) out
over the water toward the viewer and ends at the seaward embarkation landing.
"""
from iso_render import Iso

S = Iso(U=11)

# ---------------------------------------------------------------- palette (literal; high contrast)
# Rule: light dressed columns/curbs vs DARKER deck body vs CONTRASTING roof vs WARM timber.
# Tuned for SEPARATION: deck (mid grey) vs piers (BLUE-grey, cooler+darker) vs footing (dark wet)
# must each read as a distinct masonry layer at small scale -- not one grey mass.
WATER = "#3f78b4"   # open water surface (the terminus the road walks out to; pushed bluer)
WATERD= "#295688"   # deeper water (riverbed shadow band; darker, more saturated)
BED   = "#615e57"   # riverbed (gravel/stone) the piles are driven into (darker, sits under)
# --- masonry: 3 SEPARATED tones -- piers cool blue-grey, deck warm pale grey, footing dark wet ---
PIER  = "#6f7680"   # cut-stone pier shafts (COOL blue-grey -> reads vs the warmer deck)
PIERW = "#565b63"   # submerged footing course (dark cool, reads wet/permanent)
DECK  = "#9b978c"   # stone-brick deck field (warmer pale grey -> lifts off the cool piers)
MOSS  = "#6f8257"   # mossy_cobblestone accent (greener + darker -> reads as moss, not grey)
CURB  = "#e3dfd2"   # stone_brick_slab[type=top] curb + parapet caps (near-white, HIGH contrast)
PARA  = "#c4c0b3"   # cobblestone_wall parapet body (light dressed stone, stands proud)
# --- timber (warm, clearly distinct from grey stone) ---
PLANK = "#b3884f"   # oak_planks (shack walls / warm timber; brighter)
LOG   = "#6e4d29"   # oak_log corner posts (dark warm timber)
STRIP = "#caa063"   # stripped_oak_log stringer / bright timber accent
POST  = "#4f3a22"   # lamp-post fence newels (VERY dark timber -> separate from the LOG posts)
IRON  = "#3b3b40"   # lantern iron cage / chain (dark cool metal accent)
# --- roof: a CONTRASTING cool dark so the gable reads against warm walls + grey stone ---
ROOF  = "#5a4d3d"   # spruce_stairs gable roof (warm-dark, distinct from grey + from planks)
ROOFE = "#3d3428"   # roof eave / ridge shadow
RIDGE = "#7a6347"   # spruce ridge beam (lighter warm line along the peak -> sharpens silhouette)
NETS  = "#d8b878"   # spruce_trapdoor net-drying panels (light timber, on shack face)
BOLL  = "#7a766d"   # mooring bollard (DARK dressed stone -> stands out vs pale parapet/curb)
BOAT  = "#73492a"   # moored oak boat hull
BOATI = "#caa063"   # boat interior / bench planks (light timber, reads the hull is a boat)

# ----------------------------------------------------------------------------------------------
# VERTICAL CONVENTION (reality pass): the bed top = y1, waterline = y2, and the DECK TOP = y5.
# That leaves a clear y2..y4 band of OPEN PILING visible above the waterline -> the deck is
# plainly CARRIED on posts driven to the bed, never floating. Every pile runs bed(y1)->deck(y4).
BEDY, WLINE, DECKB, DECKT = 1, 2, 4, 5              # bed top / waterline / deck underside / deck top

# ============================================================ WATER + RIVERBED (the context plane)
# A shallow water slab the deck thrusts over; the bank is at the BACK (low z), water toward viewer.
# riverbed floor (piles are driven into this) -- darker, sits under the whole reach.
S.box(0, 4, 0, 17, 13, 1, BED)                      # riverbed pan under the whole jetty reach (top=y1)
# water surface: two depth bands so the deeper seaward water reads (kept THIN so piles show through)
S.box(0, 5, 1, 17, 8, 1, WATERD)                    # seaward deeper water (darker, y1..y2)
S.box(0, 4, 2, 17, 13, 0.45, WATER)                 # thin bright waterline sheet (top = y2 = surface)

# bank / shore at the BACK (z 0..4): the road arrives here, raised to meet the deck top (y5)
S.box(0, 0, 0, 17, 4, 3, "#5c6b4e")                 # grassy/earth bank shelf (top = y3)
S.box(0, 0, 3, 17, 4, 1, "#6b7a59")                 # bank crown course (top = y4, just under deck)
S.box(2, 3, 4, 12, 1, 0.7, "#8a7b55")              # approach-blend apron (road meets deck, coarse_dirt)

# ============================================================ PILE BENTS (grounded bed -> deck)
# A real timber-pile staithe: at each station a BENT = front pile + back pile (the 2 deck rows)
# joined by a cross CAP beam the deck sits on. Posts are SLIM (0.7) with open water between them
# so you read them as driven piles, not a stone wall. Each pile: dark wet butt at the waterline
# (creosote/scour) + lighter shaft up to the cap. 5 bents march out from the bank.
BENT_X = [1, 4, 7, 10, 13]                           # x of each bent (front+back pile pair)
FRONT_Z, BACK_Z = 6.15, 7.15                         # the two deck rows (seaward / landward pile lines)
PW = 0.7                                             # pile width (slim -> reads as a post)
for bx in BENT_X:
    for pz in (FRONT_Z, BACK_Z):
        S.box(bx, pz, WLINE, PW, PW, DECKB - WLINE, PIER, seam=True)   # pile shaft, waterline->deck (visible)
        S.box(bx - 0.08, pz - 0.08, BEDY, PW + 0.16, PW + 0.16, WLINE - BEDY, PIERW)  # submerged wet butt
        S.box(bx - 0.12, pz - 0.12, WLINE - 0.05, PW + 0.24, PW + 0.24, 0.4, PIERW)   # waterline scour ring
    # cross CAP beam tying the two piles of this bent (the deck timbers rest on these)
    S.box(bx - 0.1, FRONT_Z - 0.1, DECKB - 0.45, PW + 0.2, (BACK_Z - FRONT_Z) + PW + 0.2, 0.45, MOSS)
# stripped-log STRINGERS: the two longitudinal beams (one per pile line) the deck planks span
S.box(0, FRONT_Z, DECKB - 0.4, 15, PW, 0.4, STRIP)  # seaward stringer along the front pile line
S.box(0, BACK_Z,  DECKB - 0.4, 15, PW, 0.4, STRIP)  # landward stringer along the back pile line

# ============================================================ DECK (stone-brick, 2 wide, 11 long)
# Deck body sits ON the stringers/caps: underside y4, top y5. Outer rows get a pale slab CURB.
S.box(0, 6, DECKB, 15, 2, DECKT - DECKB, DECK, seam=False)   # stone-brick deck field (full run, 2 wide)
# patchy mossy/cobble accents in the field (/2-quantised, no confetti)
S.box(4, 6, DECKB, 2, 1, DECKT - DECKB, MOSS)       # mossy accent patch
S.box(9, 7, DECKB, 2, 1, DECKT - DECKB, MOSS)       # mossy accent patch (other row)
# pale curb both outer rows (stone_brick_slab[type=top]) -- frames the deck, high contrast
S.box(0, 5.65, DECKT, 15, 0.35, 0.4, CURB)          # front-row curb lip (seaward edge)
S.box(0, 8.0, DECKT, 15, 0.35, 0.4, CURB)           # back-row curb lip (landward edge)

# ---- seaward 2x2 embarkation landing (widens at the deck head, on its own bent of piles) ----
for lz in (5.15, 7.15):                              # front + back landing pile lines
    S.box(14.1, lz, WLINE, PW, PW, DECKB - WLINE, PIER, seam=True)   # landing pile (seaward)
    S.box(15.1, lz, WLINE, PW, PW, DECKB - WLINE, PIER, seam=True)   # landing pile (the wider corner)
    S.box(14.0, lz - 0.1, BEDY, PW + 0.2, PW + 0.2, WLINE - BEDY, PIERW)
    S.box(15.0, lz - 0.1, BEDY, PW + 0.2, PW + 0.2, WLINE - BEDY, PIERW)
S.box(14, 5, DECKB - 0.4, 2, 3, 0.4, MOSS)          # landing cross-cap beam (carries the landing deck)
S.box(14, 5, DECKB, 2, 3, DECKT - DECKB, DECK)      # the 2x3 embarkation landing surface
S.box(14, 4.65, DECKT, 2, 0.35, 0.4, CURB)          # landing seaward curb

# ============================================================ PARAPET + RAILINGS (the balustrade)
# A real low balustrade: a continuous cobblestone_wall rail run on BOTH outer edges, capped pale,
# with stout newel POSTS standing proud at regular bays so it reads as a built railing, not a slab.
RAILY = DECKT                                        # rail base sits on the deck top
S.box(0, 5.7, RAILY, 15, 0.45, 0.85, PARA, seam=False)  # front rail run (seaward outer edge)
S.box(0, 7.85, RAILY, 15, 0.45, 0.85, PARA, seam=False) # back rail run (landward outer edge)
S.box(0, 5.7, RAILY + 0.85, 15, 0.45, 0.3, CURB)    # pale rail cap (front)
S.box(0, 7.85, RAILY + 0.85, 15, 0.45, 0.3, CURB)   # pale rail cap (back)
# stout newel posts at regular bays (over the pile bents -> the rail is supported where it should be)
for nx in (0.2, 3.2, 6.2, 9.2, 12.2):
    S.box(nx, 5.6, RAILY, 0.7, 0.7, 1.25, BOLL, seam=True)   # front newel (proud of the rail)
    S.box(nx, 7.75, RAILY, 0.7, 0.7, 1.25, BOLL, seam=True)  # back newel
    S.box(nx - 0.06, 5.54, RAILY + 1.25, 0.82, 0.82, 0.22, CURB)  # pale newel cap (front)
    S.box(nx - 0.06, 7.69, RAILY + 1.25, 0.82, 0.82, 0.22, CURB)  # pale newel cap (back)
# rail returns around the seaward landing head (so the deck end is railed, not open)
S.box(14, 4.7, RAILY, 2, 0.45, 0.85, PARA)
S.box(14, 4.7, RAILY + 0.85, 2, 0.45, 0.3, CURB)
S.box(15.9, 4.7, RAILY, 0.45, 3.3, 0.85, PARA)      # east return down the landing side
S.box(15.9, 4.7, RAILY + 0.85, 0.45, 3.3, 0.3, CURB)

# lamp-post stations: a dark newel standard grounded on the deck over a bent -> bracket + iron
# lantern cage head. Sit them ON the rail line so they read as fixed dock lamps. (3 stations)
LAMP_STATIONS = [(1, 7.7), (7, 7.7), (15.3, 5.4)]   # (x, z): two on the landward rail + one on the landing's seaward corner
for lx, lz in LAMP_STATIONS:
    S.box(lx, lz, RAILY, 0.55, 0.55, 3, POST)       # lamp standard (deck+1..+3)
    S.box(lx - 0.32, lz + 0.05, RAILY + 2.6, 1.05, 0.35, 0.3, STRIP)  # stripped cross-arm bracket
    S.box(lx - 0.22, lz - 0.05, RAILY + 2.9, 0.85, 0.7, 0.7, IRON)    # iron lantern cage head

# ============================================================ DOCK-SHACK (wnl_dock_shack satellite)
# 5x5x5 roofed shore building on the bank (z 0..4 region), seaward (high-z) face left OPEN = boathouse mouth.
# Sits on the bank crown (top y4) so its floor is at deck level -- you step straight off the deck into it.
SX, SZ = 1, 0                                        # shack origin on the bank
# foundation course (cobblestone + stone_brick) on the bank, top = y4 (level with the deck)
S.box(SX, SZ, 3, 5, 4, 1, "#6f6c64", seam=False)    # stone foundation plinth (top = y4 = deck level)
# corner posts (oak_log) 3 tall + plank infill walls (start at y4 = on the plinth)
WALLY = 4
for (cx, cz) in [(SX, SZ), (SX+4, SZ), (SX, SZ+3), (SX+4, SZ+3)]:
    S.box(cx, cz, WALLY, 1, 1, 3, LOG, seam=True)   # oak_log corner post (3 tall)
# plank infill walls (back + two sides; seaward face stays OPEN as the boathouse mouth)
S.box(SX, SZ, WALLY, 5, 1, 3, PLANK, seam=True)     # BACK wall (landward, z=SZ) -- solid plank
S.box(SX, SZ, WALLY, 1, 4, 3, PLANK, seam=True)     # WEST side wall
S.box(SX+4, SZ, WALLY, 1, 4, 3, PLANK, seam=True)   # EAST side wall
# net-drying spruce_trapdoor panels on the open seaward face flanks (the tackle read)
S.box(SX, SZ+3.6, WALLY+0.5, 1, 0.4, 2, NETS)       # net panel W of the mouth
S.box(SX+4, SZ+3.6, WALLY+0.5, 1, 0.4, 2, NETS)     # net panel E of the mouth
# spruce_slab ceiling, then a pitched STEPPED spruce_stairs gable roof (inward one block per course)
RY = WALLY + 3                                       # roof base y = 6
S.box(SX-0.35, SZ-0.35, RY-0.25, 5.7, 4.7, 0.35, ROOFE)  # spruce_slab eave fascia (dark overhang lip)
S.box(SX-0.3, SZ-0.3, RY, 5.6, 4.6, 1, ROOF)        # roof course 0 (widest, eaves overhang)
S.box(SX+0.7, SZ+0.7, RY+1, 3.6, 2.6, 1, ROOF)      # roof course 1 (inset)
S.box(SX+1.6, SZ+1.6, RY+2, 1.8, 0.8, 0.9, RIDGE)   # ridge BEAM (lighter warm line -> sharp peak silhouette)
S.box(SX+1.9, SZ+1.55, RY+2.9, 1.2, 0.9, 0.35, ROOFE)   # ridge cap shadow over the beam

# ============================================================ QUAY DECO (props on the bank/quay)
# barrel stack + composter + cauldron clustered on the bank beside the shack (counts by hash).
# Each prop is now a distinct silhouette + a contrasting lid/band so they don't read as brown cubes.
BARR  = "#9c7339"   # barrel staves (warm)
BARRT = "#caa063"   # barrel lid / hoop (light timber top)
COMP  = "#5e7a3e"   # composter (green compost mass -> reads vs the brown barrels)
COMPW = "#7a5a32"   # composter timber frame
# props sit on the bank crown (top y4) beside the shack, clear of the deck mouth.
S.box(7, 1.0, 4, 1, 1, 1.4, BARR)                   # barrel (quay prop)
S.box(7, 1.0, 5.4, 1, 1, 0.18, BARRT)               # barrel lid (light cap)
S.box(8.25, 1.05, 4, 0.85, 0.85, 1.05, BARR)        # barrel (2nd, lower)
S.box(8.25, 1.05, 5.05, 0.85, 0.85, 0.16, BARRT)    # 2nd barrel lid
S.box(7, 2.2, 4, 1, 1, 0.9, COMPW)                  # composter frame (timber sides)
S.box(7.12, 2.32, 4.55, 0.76, 0.76, 0.45, COMP)     # composter green mass (the tackle/compost read)
S.box(8.45, 2.25, 4, 0.85, 0.85, 0.75, "#52525a")   # cauldron iron body (cool dark -> reads as metal)
S.box(8.55, 2.35, 4.65, 0.65, 0.65, 0.12, "#2f4f6e") # cauldron bait-water surface (dark blue)

# ============================================================ MOORING (bollards + moored boat)
# Two stout mooring bollards sit SOLIDLY on the landing deck (top y5), each with an iron ring;
# a line drops from the seaward bollard to the moored boat floating at the waterline (y2) alongside.
for bx, bz in ((14.3, 5.25), (15.25, 7.55)):
    S.box(bx, bz, DECKT, 0.7, 0.7, 1.0, BOLL, seam=True)        # bollard post on the landing deck
    S.box(bx - 0.1, bz - 0.1, DECKT + 1.0, 0.9, 0.9, 0.2, CURB) # pale bollard cap (high-contrast head)
    S.box(bx + 0.26, bz + 0.26, DECKT + 0.5, 0.2, 0.2, 0.35, IRON)  # iron mooring ring (faces the water)
# moored oak boat floating at the waterline (top ~ y2), alongside the landing's seaward corner.
BOX, BOZ = 15.55, 8.0                                   # boat origin (just off the landing corner)
S.box(BOX, BOZ, WLINE - 0.5, 2.3, 1.0, 0.55, BOAT)     # boat hull (sits IN the water, top ~ waterline)
S.box(BOX + 0.25, BOZ + 0.2, WLINE - 0.18, 1.8, 0.6, 0.2, BOATI)  # interior/thwart (light -> reads as a boat)
# iron mooring LINE from the seaward bollard ring down to the boat's bow (a real taut painter)
S.box(15.5, 7.85, WLINE + 0.1, 0.16, 0.16, (DECKT + 0.5) - (WLINE + 0.1), IRON)

# ============================================================ ACCENTS (lanterns / flame / finial)
# lamp-post lanterns (the warm glow sits ON each iron cage head at RAILY+2.9 ~= y7.9)
for lx, lz in LAMP_STATIONS:
    S.accent(lx + 0.15, lz + 0.25, RAILY + 3.2, "glow", "#ffe6ad", r=2.5)
# hanging lantern under the dock-shack eave (boathouse mouth glow)
S.accent(SX + 2.5, SZ + 3.4, WALLY + 2.6, "glow", "#ffe1a0", r=2.8)
# a softer glow inside the shack mouth (lit interior read)
S.accent(SX + 2.5, SZ + 1.6, WALLY + 1.6, "glow", "#ffdf9a", r=2.2)
# warm point on the quay (worked-dock life) + a ridge finial on the gable peak
S.accent(7.6, 1.4, 5.5, "dot", "#ffcf6e", r=1.8)
S.accent(SX + 2.5, SZ + 2.0, RY + 3.0, "finial")

# ============================================================ CALLOUT LABELS
S.label(7, 6.5, DECKT + 0.2, "stone-brick deck (2 wide) — pale curb both rows")
S.label(7, 6.5, 2.6, "timber pile bents — driven to the riverbed (deck rests on the caps)")
S.label(0.2, 5.6, RAILY + 1.6, "cobblestone-wall rail + newel posts + lamp stations")
S.label(SX + 2.5, SZ + 1.5, RY + 1, "wnl_dock_shack — stepped spruce-stair gable, seaward boathouse mouth")
S.label(15, 8.4, DECKT + 0.6, "embarkation landing — mooring bollards + moored boat")
S.label(8, 1.5, 5.0, "working quay — barrels / composter / cauldron")

out = S.svg(title="Pier R5 (Road / stone_jetty) — pile-and-plank working dock: railed deck on driven pile bents, lamp posts, embarkation landing + roofed dock-shack",
            size_label="~16x5 terminus · h8 · deck on driven pile bents + dock-shack (2-dweller working dock)")
open("detail_svg/pier.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/pier.svg | bytes", len(out.encode()))
