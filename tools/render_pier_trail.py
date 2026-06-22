"""Pier R1 (Trail = ruined_pier) -> detail_svg/pier_trail.svg.
Per deco_catalog_v2.json id 'pier' tier Trail ("ruined_pier — short half-rotted deserted jetty",
footprint ~8x3, height 4): the FLOOR of the pier ladder -- a worn pile-and-plank stub that simply
proves the road ended somewhere real. Deliberately the least-built thing: deck still carries you to
the water's edge, but barely. DESERTED + UNLIT (wear+CivLevel gate keeps it dead -> dead looks dead).

The signature here is DECAY, not build: 3-4 driven oak_log piles (one RANDOMLY broken -> its deck
cell is a structure_void GAP, water shows through, the jetty sags there), 1 rotted-through board
gap, a STEPPED seaward sag built from oak_slab[type=top] on a lower support (a dip, never a tilt),
leaning oak_fence stubs (no continuous rail), a vine draped on ONE pile face (attached to that log),
a buried coarse-dirt-over-cobble bank tie + a worn apron scatter, and a single tilted barrel. No
light, no dweller. Drawn here as the 5-pile-column / 4-driven-pile case with pile #3 broken.

Reality pass (matches render_pier.py): bed=y1, waterline=y2, deck-top=y5 -> a clear OPEN band of
piling stands above the water, so the deck reads as a real pile-and-plank staithe on its posts. The
ONE broken pile stops a course short of the deck and that cell is left OPEN (the sag/gap signature).

Credit: worn-timber pile-and-plank jetty technique + rotted-board grammar inspired by Moog's Paths
jetties + real medieval timber fishing-staithes -- studied for FORM/TECHNIQUE only, built entirely
in vanilla blocks as original WNL work (CREDITS.md). No copied build/NBT. Same wnl_pier data builder
as render_pier.py (Road top); the builder hashes decay/broken-pile/gaps/palette live per terminus.

Layout convention (matches iso_render + render_pier.py): x = right, z = depth (z=0 at BACK = the
bank/shore), y = up. The bank + apron sit at the BACK (low z); the deck marches FORWARD (rising z)
out over the water toward the viewer and ends at the sagging seaward lip.
"""
from iso_render import Iso

S = Iso(U=22)

# ---------------------------------------------------------------- palette (literal; high contrast)
# All-TIMBER tier (no stone deck): the contrast ladder is warm timber vs cool water vs earth bank,
# plus the dark wet pile-butts. Tuned so plank / log / stripped-log / slab each read as themselves.
WATER = "#3f78b4"   # open water surface (the terminus the trail walks out to)
WATERD= "#295688"   # deeper seaward water (riverbed shadow band, darker + more saturated)
BED   = "#5f5c55"   # riverbed (gravel/stone) the piles are driven into (sits under everything)
# --- timber (the whole jetty) on a clear warm luminance ladder ---
PLANK = "#a07d48"   # oak_planks deck field (worn warm timber, slightly greyed for age)
PLANKD= "#82663a"   # rotted/weathered plank (the darker boards near the gaps -> reads decayed)
LOG   = "#74522c"   # oak_log[axis=y] driven piles (dark warm timber)
LOGW  = "#4d3920"   # submerged pile butt (creosote/scour, dark wet -> reads permanent)
STRIP = "#caa063"   # stripped_oak_log seaward stringer (bright timber accent under the edge)
SLAB  = "#b89255"   # oak_slab[type=top] sagging seaward step (lighter than the deck -> reads as a step)
FENCE = "#5e472c"   # leaning oak_fence stubs (dark slim timber, no continuous rail)
# --- ground / decay accents ---
BANK  = "#566445"   # grassy/earth bank shelf (the trail arrives here)
BANKC = "#67764f"   # bank crown course (just under deck level)
DIRT  = "#5d4f3a"   # coarse_dirt bank tie + worn apron scatter (sits in the ground)
COBB  = "#8a8276"   # cobblestone buried tie under the dirt (the deck locks into the bank)
MOSSC = "#6f7d56"   # one mossy_cobblestone in the apron (age creeps in)
VINE  = "#4f7233"   # vine[south=true] draped on ONE pile face (attached to the adjacent log)
BARR  = "#9c7339"   # tilted barrel staves (the lone prop, warm)
BARRT = "#caa063"   # barrel lid / hoop (light timber top -> reads as a barrel not a cube)

# ----------------------------------------------------------------------------------------------
# VERTICAL CONVENTION (reality pass): bed top = y1, waterline = y2, deck top = y5. That leaves a
# clear y2..y4 band of OPEN piling above the waterline -> the deck is plainly CARRIED on posts
# driven to the bed, never floating. Every (sound) pile runs bed(y1) -> deck underside(y4).
BEDY, WLINE, DECKB, DECKT = 1, 2, 4, 5              # bed top / waterline / deck underside / deck top

# the single 1-wide deck runs along ONE z-row; bank is shallow so the JETTY is the hero, not the bank.
DZ = 4.0                                            # the deck/pile z-row (the 1-wide deck line)

# ============================================================ WATER + RIVERBED (the context plane)
# A shallow water slab the deck thrusts over; the bank is at the BACK (low z), water toward viewer.
S.box(0, 2, 0, 11, 5, 1, BED)                       # riverbed pan under the whole jetty reach (top=y1)
S.box(0, 3, 1, 11, 4, 1, WATERD)                    # seaward deeper water (darker, y1..y2)
S.box(0, 2, 2, 11, 5, 0.45, WATER)                  # thin bright waterline sheet (top = y2 = surface)

# ============================================================ BANK / SHORE (z 0..2, the trail arrives)
# Kept SHALLOW (2 deep) so the bank doesn't swamp the jetty -- the deck out over water is the subject.
S.box(0, 0, 0, 11, 2, 3, BANK)                      # grassy/earth bank shelf (top = y3)
S.box(0, 0, 3, 11, 2, 1, BANKC)                     # bank crown course (top = y4 = deck underside)
# bank ABUTMENT: a buried coarse-dirt-over-cobble tie locks the deck into the bank (at deck col 0/1)
S.box(0.8, 1.1, 2, 1, 1, 1, COBB)                   # buried cobblestone tie (sits in the bank)
S.box(0.8, 1.1, 3, 1, 1, 1, DIRT)                   # coarse_dirt over it (locks deck into the bank, top=y4)
# worn road-meets-shore APRON: half-buried coarse_dirt/mossy stones on the bank crown (sit IN ground)
S.box(2.2, 0.5, 3, 1, 1, 0.55, DIRT)               # apron scatter (abuts the bank crown, grounded)
S.box(3.1, 0.9, 3, 0.9, 0.9, 0.5, DIRT)            # apron scatter (chains off the first, not floating)
S.box(1.9, 1.0, 3, 0.85, 0.85, 0.45, MOSSC)        # one mossy stone in the apron (touches the dirt tie)

# ============================================================ DRIVEN PILES (grounded bed -> deck)
# 4 driven oak_log piles at deck columns 1,3,5,7 (the 5-column / 4-pile case). Each: dark wet butt
# at the waterline + lighter shaft up to the deck underside. Pile #3 (col 5) is the BROKEN one ->
# it stops one course SHORT (top omitted) so the deck cell above becomes a structure_void GAP.
PILE_X = [1.15, 3.15, 5.15, 7.15]                   # x of each driven pile (under the deck cells)
BROKEN = 2                                          # index of the randomly-broken pile (col 5; NOT fixed #2)
PW = 0.72                                            # pile width (slim -> reads as a driven post)
for i, px in enumerate(PILE_X):
    if i == BROKEN:
        # broken pile: snapped off a course below the deck -> open air above (the sag/gap signature).
        top = DECKB - 1.2                            # stops short; jagged broken top
        S.box(px, DZ, WLINE, PW, PW, top - WLINE, LOG, seam=True)        # short broken shaft (still standing)
        S.box(px - 0.06, DZ - 0.06, top - 0.05, PW + 0.12, PW + 0.12, 0.28, LOGW)  # splintered broken cap (dark)
    else:
        S.box(px, DZ, WLINE, PW, PW, DECKB - WLINE, LOG, seam=True)      # sound pile shaft, waterline->deck
    # submerged wet butt + waterline scour ring on every pile (grounded into the bed)
    S.box(px - 0.08, DZ - 0.08, BEDY, PW + 0.16, PW + 0.16, WLINE - BEDY, LOGW)   # wet butt
    S.box(px - 0.12, DZ - 0.12, WLINE - 0.05, PW + 0.24, PW + 0.24, 0.4, LOGW)    # waterline scour ring
# seaward STRINGER: one stripped_oak_log beam under the deck's seaward edge (the deck reads CARRIED).
# It runs the deck length on the FRONT (high-z) face of the piles so it's visible carrying the planks.
S.box(0.6, DZ + PW, DECKB - 0.45, 7.4, 0.32, 0.45, STRIP)   # stripped-log stringer on the pile-line front face

# ============================================================ DECK (oak_planks, 1 wide, 5 cells)
# Deck body sits ON the piles/stringer: underside y4, top y5. 1-wide. Two rot signatures live in it:
# (a) the structure_void GAP over the broken pile (col 5), (b) 1 rotted-through interior board gap.
# We lay the deck as per-cell boxes so the GAPS are true holes (omitted boxes = open air, water shows).
DECK_CELLS = [1, 2, 3, 4, 5, 6, 7]                   # deck spans cols 1..7 along the z=DZ row
GAP_CELLS  = {5, 2}                                  # col 5 = broken-pile sag gap; col 2 = rotted-through board
for cx in DECK_CELLS:
    if cx in GAP_CELLS:
        continue                                     # structure_void -> leave OPEN (water shows through)
    near_gap = (cx in (1, 3, 4, 6))                  # boards beside the gaps read weathered/darker
    S.box(cx, DZ, DECKB, 1, 1, DECKT - DECKB, PLANKD if near_gap else PLANK, seam=False)

# ---- STEPPED seaward sag: the deck DIPS over the last 2 cells (8,9) on lower supports (NOT a tilt) ----
# Each sag cell is an oak_slab[type=top] sitting one course LOWER than the last, on its own grounded
# support pile -> reads as a stepped dip toward the water, every block grid-aligned + held up.
# sag cell 8: one course down. Sits on a short log support that is itself a driven (grounded) stub pile.
S.box(8.0, DZ, BEDY, PW, PW, (DECKB - 1) - BEDY, LOG, seam=True)      # grounded sag stub-pile (bed -> support)
S.box(8.0, DZ - 0.06, BEDY, PW + 0.12, PW + 0.12, WLINE - BEDY, LOGW) # its wet butt
S.box(8.0, DZ, DECKB - 1, 1, 1, 0.5, SLAB)                           # oak_slab[type=top], one course lower (the dip)
# sag cell 9 (the very end): lower again -- a final lip slab on a stub that bottoms out near the water.
S.box(9.0, DZ + 0.05, BEDY, PW, PW, (DECKB - 1.7) - BEDY, LOG, seam=True)  # grounded stub for the end lip
S.box(9.0, DZ - 0.05, BEDY, PW + 0.12, PW + 0.12, WLINE - BEDY, LOGW)      # its wet butt
S.box(9.0, DZ + 0.05, DECKB - 1.7, 0.95, 0.9, 0.5, SLAB)                  # final lip slab (the dip bottoms out)

# ============================================================ RAIL (NO continuous rail -- decay)
# Only 2 LEANING oak_fence stubs on surviving planks (the rail is gone, not maintained). Each stub is
# grounded ON a sound deck cell + leans <=0.3 of a block (supported lean, never floating).
S.box(3.18, DZ + 0.2, DECKT, 0.34, 0.34, 1.1, FENCE, seam=True)      # fence stub on col 3 (upright-ish)
S.box(6.24, DZ + 0.05, DECKT, 0.34, 0.34, 0.85, FENCE, seam=True)    # leaning fence stub on col 6 (leans ~0.25 outward)
# VINE draped on ONE pile face: hangs on the col-7 pile's FRONT (high-z) face, attached to that log.
S.box(7.16, DZ + PW, WLINE + 0.3, PW - 0.08, 0.14, (DECKB - 0.3) - (WLINE + 0.3), VINE)  # vine curtain on the log

# ============================================================ PROP (the lone tilted barrel, on the apron)
# A single tilted barrel[facing=up] on the bank apron (no dweller, no light). Grounded on the bank
# crown (top y4), nudged so it reads tipped -- it abuts the apron scatter (a thing left behind).
S.box(3.95, 0.55, 4, 0.95, 0.95, 1.25, BARR, seam=True)             # tilted barrel staves (the one prop)
S.box(3.9, 0.5, 4 + 1.25, 1.05, 1.05, 0.16, BARRT)                  # barrel lid / top hoop (light cap)

# ============================================================ CALLOUT LABELS (the decay grammar reads)
S.label(4.5, DZ + 0.5, DECKT + 0.1, "oak-plank deck (1 wide) — worn, weathered boards")
S.label(5.15, DZ, DECKB - 0.7, "RANDOMLY-broken pile → deck cell left a structure_void GAP (sags here)")
S.label(2, DZ + 0.5, DECKT + 0.1, "rotted-through board gap (open air, water shows through)")
S.label(8.5, DZ + 0.3, DECKB - 1.3, "STEPPED seaward sag — oak_slab[type=top] dipping on lower grounded stubs")
S.label(3.2, DZ + 0.2, DECKT + 1.2, "leaning oak_fence stubs (NO continuous rail) + vine on a pile face")
S.label(0.9, 1.1, 3.5, "buried coarse-dirt-over-cobble bank tie + worn apron scatter")
S.label(4.0, 0.6, 5.3, "lone tilted barrel — NO light, NO dweller (deserted)")

out = S.svg(title="Pier R1 (Trail / ruined_pier) — short half-rotted deserted jetty: driven piles, a broken pile + rotted gaps, a stepped seaward sag, no rail, no light",
            size_label="~8x3 foot · h4 · 0 lanterns (ladder floor — a worn pile-and-plank stub that proves the trail ended somewhere real)",
            label_w=356)
open("detail_svg/pier_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/pier_trail.svg | bytes", len(out.encode()))
