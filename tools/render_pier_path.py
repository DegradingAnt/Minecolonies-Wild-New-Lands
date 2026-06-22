"""Pier R2 (Path = fisher_jetty) -> detail_svg/pier_path.svg.
Per deco_catalog_v2.json id 'pier' tier Path ("fisher_jetty — tidy little working jetty, lone
fisherman", footprint ~11x3, height 5): a MODEST, near-linear step up from the Trail -- same timber
materials, but built PROPERLY, LIT, and INHABITED instead of rotting. The big non-linear jump is
reserved for Road (this piece's ceiling); here the headline upgrade is simply LIGHT + LIFE.

What's new over the Trail (ruined_pier): (1) the deck is CLEAN + SOLID -- no broken pile, no
structure_void gaps, no sag; (2) a full grounded pile-and-stringer STRUCTURE -- 4-5 bents, each pile
with a cobblestone footing course at the waterline, an oak_log BENT-CAP at deckY-1, and a
stripped_oak_log STRINGER the full length (the deck plainly reads CARRIED); (3) a CONTINUOUS oak_fence
handrail along most of the run with ONE gap near the seaward end for the moored boat; (4) a
spruce_trapdoor net-drying RACK on a deck cell (the tackle read); (5) WORKING PROPS on the bank
landing -- a barrel + a composter (+ optional cauldron); (6) the FIRST LIGHT -- one lantern on a
grounded oak_fence post at the deck head (+ an optional hanging lantern off a fence arm); (7) a moored
oak boat + a lone tended fisherman (both via the §4.2 deferred populate pass, NOT baked into NBT --
drawn here for the read). Wear-gated TENDED -> lit + populated.

Reality pass (matches render_pier.py): bed=y1, waterline=y2, deck-top=y5 -> a clear OPEN band of
piling stands above the water at every bent, so the deck reads as a real pile-and-plank staithe.

Credit: worn-timber pile-and-plank jetty technique inspired by Moog's Paths jetties + real medieval
timber fishing-staithes (driven log piles + plank deck + net-drying racks + a single shore presence)
-- studied for FORM/TECHNIQUE only, built entirely in vanilla blocks as original WNL work (CREDITS.md).
No copied build/NBT. Same wnl_pier data builder as render_pier.py (Road top); the builder hashes
pile count / deck length / accent boards / prop+lamp counts / palette live per terminus.

Layout convention (matches iso_render + render_pier.py): x = right, z = depth (z=0 at BACK = the
bank/shore), y = up. The bank landing sits at the BACK (low z); the deck marches FORWARD (rising z)
out over the water toward the viewer and ends at the seaward step-down landing + moored boat.
"""
from iso_render import Iso

S = Iso(U=20)

# ---------------------------------------------------------------- palette (literal; high contrast)
# Still ALL-TIMBER like the Trail (escalation is build+life, NOT a new material class -- that leap is
# saved for Road's stone). Ladder: plank deck vs darker log piles vs bright stripped stringer vs the
# cobblestone footing (the one cool stone note) vs spruce step + spruce net-rack (cooler timber).
WATER = "#3f78b4"   # open water surface (the terminus the path walks out to)
WATERD= "#295688"   # deeper seaward water (riverbed shadow band, darker + more saturated)
BED   = "#5f5c55"   # riverbed the piles are driven into (sits under everything)
# --- timber (the jetty) on a clear warm luminance ladder ---
PLANK = "#a9854e"   # oak_planks deck field (TIDY warm timber -> brighter+cleaner than the Trail's worn deck)
PLANKA= "#caa063"   # stripped_oak_log accent boards (patchy, low-freq -> the tidy accent grain)
LOG   = "#74522c"   # oak_log[axis=y] driven piles + bent-caps (dark warm timber)
LOGW  = "#4d3920"   # submerged pile shaft (dark wet -> reads permanent)
STRIP = "#caa063"   # stripped_oak_log full-length stringer (bright timber beam under the deck edge)
FOOT  = "#7c8a93"   # cobblestone footing course at the waterline (cool stone -> reads wet+permanent)
FENCE = "#5e472c"   # oak_fence handrail + lantern post (dark slim timber)
SPSLAB= "#6e5a40"   # spruce_slab[type=top] seaward step-down (cooler timber -> reads as the step)
NETS  = "#7a6747"   # spruce_trapdoor[open] net-drying rack panel (cool timber lattice)
# --- ground / props ---
BANK  = "#566445"   # grassy/earth bank shelf (the path arrives here)
BANKC = "#67764f"   # bank crown course (just under deck level)
LAND  = "#8a8276"   # bank LANDING -- cobblestone approach-blend patch (the road's own surface palette)
DIRT  = "#5d4f3a"   # coarse_dirt scatter in the landing (approach-blend §3)
BARR  = "#9c7339"   # barrel staves (working prop, warm)
BARRT = "#caa063"   # barrel lid / hoop (light timber top)
COMP  = "#5e7a3e"   # composter green compost mass (the net/tackle read -> reads vs the brown barrel)
COMPW = "#7a5a32"   # composter timber frame
CAULD = "#52525a"   # cauldron iron body (cool dark -> reads as metal, the bait-water prop)
CAULW = "#2f4f6e"   # cauldron bait-water surface (dark blue)
IRON  = "#3b3b40"   # lantern iron cage / hanger
BOAT  = "#73492a"   # moored oak boat hull (deferred-populate, drawn for the read)
BOATI = "#caa063"   # boat interior / thwart (light timber -> reads as a boat)
FISH  = "#6b5132"   # lone fisherman stand-in mass (deferred-populate; a humble seated figure block)
FISHT = "#9a8a6a"   # fisherman tunic/highlight (so the figure reads, not a brown cube)

# ----------------------------------------------------------------------------------------------
# VERTICAL CONVENTION (reality pass): bed top = y1, waterline = y2, deck top = y5. A clear y2..y4
# band of OPEN piling stands above the waterline at every bent -> the deck is plainly CARRIED on
# posts driven to the bed, never floating. Every pile runs bed(y1) -> bent-cap (deckY-1 = y4).
BEDY, WLINE, DECKB, DECKT = 1, 2, 4, 5             # bed top / waterline / deck underside / deck top
DZ = 4.0                                           # the 1-wide deck/pile z-row

# ============================================================ WATER + RIVERBED (the context plane)
S.box(0, 2, 0, 12, 5, 1, BED)                       # riverbed pan under the whole jetty reach (top=y1)
S.box(0, 3, 1, 12, 4, 1, WATERD)                    # seaward deeper water (darker, y1..y2)
S.box(0, 2, 2, 12, 5, 0.45, WATER)                  # thin bright waterline sheet (top = y2 = surface)

# ============================================================ BANK + LANDING (z 0..2, the path arrives)
# Kept SHALLOW so the jetty stays the hero. A 3x2 LANDING of the road's own surface (cobble +
# coarse_dirt scatter, approach-blend §3) ties the jetty to where the path meets the shore.
S.box(0, 0, 0, 12, 2, 3, BANK)                      # grassy/earth bank shelf (top = y3)
S.box(0, 0, 3, 12, 2, 1, BANKC)                     # bank crown course (top = y4 = deck underside)
S.box(0.5, 0.4, 4, 3, 1.6, 0.4, LAND)              # 3x2 cobblestone landing patch (the road's surface, top y4.4)
S.box(2.4, 0.5, 4, 0.9, 0.9, 0.45, DIRT)           # coarse_dirt scatter in the landing (approach-blend, grounded)
S.box(1.1, 1.2, 4, 0.85, 0.7, 0.42, DIRT)          # 2nd coarse_dirt scatter (abuts the landing patch)

# ============================================================ PILE BENTS (grounded bed -> bent-cap)
# 5 bents at deck cols 1,3,5,7,9. Each pile: cobblestone FOOTING course at the waterline (wet/permanent)
# + an oak_log shaft up to the bent-cap. An oak_log BENT-CAP sits at deckY-1 over each pile, and a
# full-length stripped_oak_log STRINGER runs the front edge -> the deck reads CARRIED, never floating.
PILE_X = [1.15, 3.15, 5.15, 7.15, 9.15]            # 5 bents (cols 1,3,5,7,9)
PW = 0.72                                           # pile width (slim -> a driven post)
for px in PILE_X:
    S.box(px, DZ, WLINE + 0.5, PW, PW, DECKB - (WLINE + 0.5), LOG, seam=True)   # oak_log shaft (footing -> cap)
    S.box(px - 0.05, DZ - 0.05, WLINE - 0.1, PW + 0.1, PW + 0.1, 0.6, FOOT)     # cobblestone FOOTING at waterline
    S.box(px - 0.08, DZ - 0.08, BEDY, PW + 0.16, PW + 0.16, WLINE - BEDY, LOGW) # submerged shaft into the bed
    # oak_log BENT-CAP at deckY-1 over the pile (the cross beam the deck timbers rest on)
    S.box(px - 0.18, DZ - 0.05, DECKB - 0.4, PW + 0.36, PW + 0.1, 0.4, LOG)
# full-length stripped_oak_log STRINGER on the FRONT (high-z) face of the pile line (visible, carrying)
S.box(0.6, DZ + PW, DECKB - 0.45, 9.4, 0.32, 0.45, STRIP)

# ============================================================ DECK (oak_planks, 1 wide, 8 long, SOLID)
# Deck body sits ON the bent-caps + stringer: underside y4, top y5. 1-wide, 8 cells, FULLY SOLID
# (it is tended -- no gaps, unlike the Trail). Low-frequency stripped_oak_log accent boards, patchy
# (/2-quantised per the no-confetti rule -> only a couple of cells, never a stripe).
DECK_CELLS = list(range(1, 9))                       # cols 1..8 -> 8-long deck (all solid)
ACCENT = {3, 6}                                      # the 2 stripped-log accent boards (patchy, /2-quantised)
for cx in DECK_CELLS:
    S.box(cx, DZ, DECKB, 1, 1, DECKT - DECKB, PLANKA if cx in ACCENT else PLANK, seam=False)

# ---- seaward step-down LANDING: the last cell is a spruce_slab[type=top] on a deckY-1 support ----
# A tidy step toward the water (NOT a sag) -- grounded on its own bent, every block held up.
S.box(9.0, DZ, WLINE + 0.5, PW, PW, (DECKB - 1) - (WLINE + 0.5), LOG, seam=True)   # support pile for the step
S.box(9.0, DZ - 0.05, WLINE - 0.1, PW + 0.1, PW + 0.1, 0.6, FOOT)                  # its cobble footing
S.box(9.0, DZ - 0.08, BEDY, PW + 0.16, PW + 0.16, WLINE - BEDY, LOGW)              # submerged into bed
S.box(9.0, DZ, DECKB - 1, 1, 1, 0.5, SPSLAB)                                       # spruce_slab[type=top] step-down

# ============================================================ RAIL (continuous handrail, ONE gap)
# A CONTINUOUS oak_fence handrail at deckY+1 along the FRONT (seaward, high-z) deck edge, on the solid
# deck cells -- except ONE hash-positioned GAP near the seaward end (cols 7-8) for the moored boat.
RAILY = DECKT
RAIL_CELLS = [1, 2, 3, 4, 5, 6]                      # handrail cols 1..6; gap left at cols 7-8 (the mooring gap)
for cx in RAIL_CELLS:
    S.box(cx + 0.32, DZ + 0.72, RAILY, 0.36, 0.18, 1.0, FENCE)        # fence post run on the seaward deck edge
S.box(1.32, DZ + 0.7, RAILY + 0.6, 5.36, 0.2, 0.22, FENCE)           # top rail connecting the posts (a real handrail)
# spruce_trapdoor net-drying RACK on a deck cell -- a panel kicked UP-and-OUT over the seaward edge
# (facing outward, never into a wall), reading as drying nets/tackle.
S.box(4.32, DZ + 0.88, RAILY + 0.15, 0.9, 0.16, 1.0, NETS)           # net-drying spruce_trapdoor panel (the tackle read)

# ============================================================ LIGHT (the FIRST lantern -- the headline)
# One lantern[hanging=false] sits on a single GROUNDED oak_fence post at the deck head (landward end),
# the post grounded straight onto the first bent. Plus an optional 2nd hanging lantern off a fence arm.
LPX, LPZ = 1.25, DZ + 0.15                                            # lantern-post foot (on the deck head, over bent #1)
S.box(LPX, LPZ, RAILY, 0.36, 0.36, 2.2, FENCE, seam=True)            # grounded lantern post (deckY+1..+2)
S.box(LPX - 0.12, LPZ - 0.12, RAILY + 2.2, 0.6, 0.6, 0.55, IRON)     # standing lantern[hanging=false] cage on the post top
# optional 2nd lantern: a short fence ARM out the seaward side + a hanging lantern[hanging=true] below it
S.box(LPX + 0.18, LPZ + 0.36, RAILY + 1.85, 0.7, 0.2, 0.18, FENCE)   # fence cross-arm reaching seaward (clear of the cage)
S.box(LPX + 0.74, LPZ + 0.42, RAILY + 1.35, 0.14, 0.14, 0.5, IRON)   # short chain from the arm tip
S.box(LPX + 0.64, LPZ + 0.32, RAILY + 0.95, 0.42, 0.42, 0.42, IRON)  # hanging lantern[hanging=true] cage (hangs clear)

# ============================================================ PROPS (working dock life, on the landing)
# A barrel + a composter (the net/tackle read) + a cauldron (bait-water) clustered on the bank landing.
S.box(5.6, 0.45, 4, 0.95, 0.95, 1.25, BARR, seam=True)              # barrel on the landing
S.box(5.55, 0.4, 4 + 1.25, 1.05, 1.05, 0.16, BARRT)                # barrel lid (light cap)
S.box(6.9, 0.5, 4, 0.95, 0.95, 0.95, COMPW)                        # composter frame (timber sides)
S.box(7.02, 0.62, 4.5, 0.71, 0.71, 0.5, COMP)                      # composter green mass (the tackle/compost read)
S.box(6.95, 1.25, 4, 0.85, 0.85, 0.8, CAULD)                       # cauldron iron body (the bait-water prop)
S.box(7.05, 1.35, 4.65, 0.65, 0.65, 0.14, CAULW)                   # cauldron bait-water surface (dark blue)

# ============================================================ MOORED BOAT + FISHERMAN (deferred populate)
# Both spawn via the §4.2 deferred one-shot populate pass (NOT baked into NBT) -- drawn here for the
# read. The boat floats at the waterline (top ~ y2) seaward of the rail GAP (cols 7-8). The lone
# fisherman sits on the deck head near the lantern (a humble seated figure block, tended + lit).
BOX, BOZ = 7.4, DZ + 1.05                            # boat origin (just off the rail-gap seaward edge)
S.box(BOX, BOZ, WLINE - 0.5, 2.1, 0.95, 0.55, BOAT)               # boat hull (sits IN the water, top ~ waterline)
S.box(BOX + 0.22, BOZ + 0.18, WLINE - 0.18, 1.65, 0.58, 0.2, BOATI)  # interior/thwart (light -> reads as a boat)
# lone fisherman -- a small standing figure mid-deck by the rail (facing the water); body + lighter tunic.
S.box(3.3, DZ + 0.18, DECKT, 0.5, 0.5, 0.95, FISH)              # fisherman lower body (standing on the deck)
S.box(3.3, DZ + 0.18, DECKT + 0.95, 0.5, 0.5, 0.45, FISHT)     # head/tunic highlight (so the figure reads)

# ============================================================ ACCENTS (the lantern GLOWS -- first light)
S.accent(LPX + 0.18, LPZ + 0.18, RAILY + 2.75, "glow", "#ffe6ad", r=2.6)   # standing lantern glow at the deck head
S.accent(LPX + 0.85, LPZ + 0.5, RAILY + 1.1, "glow", "#ffdf9a", r=1.9)     # hanging lantern glow off the fence arm
S.accent(6.0, 0.7, 5.4, "dot", "#ffcf6e", r=1.6)                            # warm point on the quay (worked-dock life)

# ============================================================ CALLOUT LABELS
S.label(5, DZ + 0.5, DECKT + 0.1, "oak-plank deck (1 wide) — CLEAN + SOLID, patchy stripped-log accents")
S.label(5.15, DZ, DECKB - 0.6, "5 grounded pile bents — cobble footing + oak bent-cap + stripped stringer")
S.label(3.5, DZ + 0.9, RAILY + 1.2, "continuous oak_fence handrail (one mooring gap) + net-drying rack")
S.label(LPX, LPZ, RAILY + 3.0, "FIRST LIGHT — lantern on a grounded post (+ a hanging lantern)")
S.label(9.0, DZ, DECKB - 0.5, "tidy spruce-slab step-down landing (grounded, not a sag)")
S.label(7.0, 0.8, 5.0, "working props — barrel / composter / cauldron")
S.label(7.4, DZ + 1.2, WLINE, "moored boat + lone fisherman (deferred populate — life)")

out = S.svg(title="Pier R2 (Path / fisher_jetty) — tidy little working jetty: clean grounded pile-and-stringer deck, handrail, net rack, FIRST light + a lone fisherman",
            size_label="~11x3 foot · h5 · 1–2 lanterns (modest step up — same timber, but built, lit + lived-in)",
            label_w=360)
open("detail_svg/pier_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/pier_path.svg | bytes", len(out.encode()))
