"""rest_stop HIGHWAY (R4) -> detail_svg/rest_stop_highway.svg.
Per deco_catalog_v2.json id 'rest_stop' tier Highway (footprint 13x11, height 7, KIND=nbt TEMPLATE #2):
the first GRAND payoff -- a genuine civic WAYSTATION, not a camp. The non-linear leaps over Road:
(1) the lean-to becomes a real timber-framed GABLED shed (ridge runs the long axis: two opposed eave
stair-courses at y3, inset 1 at y4, a slab ridge run at y5, gable triangles filled flush -- a true
two-pitch roof, every stair on the plate or the course below); (2) the single post becomes a 4-tall
TWIN-POST banner-GATE flanking the road apron (two posts, a cross-lintel, chain+lantern each side,
ONE palette-tinted banner on the taller post, a sign cluster at the base); (3) a BELL on a post +
a 2-board BOUNTY/notice board appear. Plus a raised kerbed STONE-BRICK court, a raised hearth with a
SMOKER + cauldron (a real cook-fire), and a 5-6 seat arc. ~5-6 light sources.

Second of 3 NBT templates (the data scatter still decorates the cleared rim). Same wnl_rest_stop
palette resolver as the Great Road top (render_rest_stop.py); hash drives floor scatter, arc rotation,
the banner tint, the shed side + the sub-feature (extra bell vs extra crate).
Inspiration (FORM/technique only, never copied; CREDITS.md): Roman MANSIO/mutatio road-stations
(the kerbed civic court, monument-flanked entrance, changing-of-mounts function); MineColonies /
Byzantine timber-frame GABLED sheds; CTOV / Moog's Paths roadside 'middles'; Bountiful-style notice
boards; supplementaries:sign_post wayfinding. Vanilla blocks only; original geometry. Shelter ALWAYS
open-fronted (the WNL rule). ISO: road at the FRONT (high-z); the banner-gate + open shed + bell + board face the road."""
from iso_render import Iso

S = Iso(U=14)

# ---- palette (literal) -- DISTINCT tones, WIDE luminance ladder so every material reads ----
# Stone-brick court ladder (dark->light): KERB < ANDES < BRICK < CRACK/CHIS; warm timber distinct;
# the spruce gable roof DARK so it pops off the pale court + the GABLE pitch reads as a real roof.
KERB   = "#5f6166"   # stone_brick_wall kerb ring (DARKEST stone -- frames + lifts the court)
KCAP   = "#9a9488"   # stone_brick_slab[top] kerb cap (mid -> the kerb reads as a wall+cap, not a slab)
GRASS  = "#6f8a47"   # biome top at the rim (grass shows through outside the kerb)
BRICK  = "#9d988d"   # stone_bricks floor cell (55% lead -- the dressed court field)
ANDES  = "#83868c"   # polished_andesite floor cell (25% -- cool grey pick)
CRACK  = "#857f72"   # cracked_stone_bricks floor cell (12% -- worn)
CHIS   = "#b3ada0"   # chiseled_stone_bricks floor cell (8% -- bright dressed accent)
APRON  = "#6a5532"   # dirt_path apron to the road deck
RING   = "#7c7468"   # cobblestone hearth-ring stones (dark -> flame pops)
HBASE  = "#9d988d"   # the 5x5 hearth base course (= BRICK tone, the raised plinth)
SOIL   = "#574631"   # dug fire hollow
CAMP   = "#5a4427"   # campfire charred bed
EMBER  = "#caa24e"   # campfire ember band
SMOKE  = "#6b6a6e"   # smoker stone body (grey machine block)
SMOKET = "#3f4248"   # smoker dark top vent
CAULD  = "#3f4248"   # cauldron iron
OAK    = "#b89160"   # stripped_oak seats / benches
OAKE   = "#8f6e44"   # stripped_oak end-grain
WLOG   = "#7a5c3a"   # stripped_spruce_log frame POSTS + the gate posts (structural timber)
WLOG2  = "#6a4f30"   # darker log pick (log seams / mid-posts)
PLANK  = "#9c7444"   # spruce_planks timber-frame infill + gable fill + bounty board (lighter warm)
ROOF   = "#43404a"   # spruce_stairs gable roof (DARK -> pops off the pale court)
ROOF2  = "#54505e"   # lighter roof course (the inset upper pitch -> reads the step-in)
RIDGE  = "#615d6b"   # spruce_slab ridge run (lightest roof tone -> the ridge line reads)
HAY    = "#d4b441"   # hay_block bed corner
BARR   = "#7a5c3a"   # barrel body
BARRT  = "#caa24e"   # barrel hoop band
BELL   = "#c9a23a"   # bronze bell (gold)
SIGN   = "#9c7444"   # hanging-sign boards / sign-post
CHAIN  = "#54545c"   # chains
BANNR  = "#a83535"   # ONE palette-tinted banner (deep red -- the single saturated accent)
BANND  = "#7e2a23"   # banner shadow fold (2-tone drape)
GLASS  = "#bfe6df"   # (held for parity -- unused at Highway; stained-glass arrives at Great Road)
LANT   = "#ffd47a"   # lantern glow

# =====================================================================================
# COURT (13x11): a raised KERBED stone-brick court. stone_brick_wall kerb + slab cap rings it;
# the floor is per-cell hash scatter (brick lead / andesite / cracked / chiseled); grass outside
# the kerb; a 3-wide dirt apron opens onto the road deck at the front.
# =====================================================================================
S.box(0, 0, 0, 13, 11, 0.5, KERB)                # kerb base slab under the whole court
# grass showing just outside the back/side kerb (one thin strip -> 'bare ground reads')
for gx in range(13):
    S.box(gx, 0, 0.5, 1, 0.4, 0.4, GRASS)        # back grass strip outside the kerb line
# laid floor (per-cell hash scatter) over the inner court (1..11 x, 1..9 z)
PAT = [
    "BABCBABCBABC",
    "ABBCABBKABBC",
    "BABCBAHBBABC",  # H = leave for hearth footprint (overwritten by base below); treat as BRICK
    "ABCBABBCABBK",
    "BCBABCBABCBA",
    "ABBCBABBKABC",
    "BABCBABCBABB",
    "ACBBABCBABBC",
    "BABCBABCBABC",
]
TONE = {"B":BRICK, "A":ANDES, "C":CRACK, "K":CHIS, "H":BRICK}
for r, row in enumerate(PAT):
    gz = r + 1
    for c, ch in enumerate(row):
        gx = c + 1
        if gx > 11 or gz > 9:
            continue
        S.box(gx, gz, 0.5, 1, 1, 0.4, TONE[ch])
# raised KERB ring (stone_brick_wall + slab cap), back + 2 sides; front centre open for the apron
S.box(0, 0, 0.5, 13, 1, 0.9, KERB); S.box(0, 0, 1.4, 13, 1, 0.25, KCAP)   # back kerb + cap
S.box(0, 1, 0.5, 1, 10, 0.9, KERB); S.box(0, 1, 1.4, 1, 10, 0.25, KCAP)   # left kerb + cap
S.box(12, 1, 0.5, 1, 10, 0.9, KERB); S.box(12,1, 1.4, 1, 10, 0.25, KCAP)  # right kerb + cap
S.box(0, 10, 0.5, 5, 1, 0.9, KERB); S.box(0, 10, 1.4, 5, 1, 0.25, KCAP)   # front-left kerb run + cap
S.box(8, 10, 0.5, 5, 1, 0.9, KERB); S.box(8, 10, 1.4, 5, 1, 0.25, KCAP)   # front-right kerb run + cap
# 3-wide dirt apron through the front kerb gap (x5..7)
S.box(5, 10, 0.5, 3, 1, 0.4, APRON)
S.box(5, 11, 0, 3, 1, 0.5, APRON)                # apron tongue to the road

# =====================================================================================
# HEARTH (raised, off-center toward the road): a 5x5 base course, a 3x3 fire ring on it, the
# campfire one block PROUD on a ring plinth, with a SMOKER + cauldron flanking it (a real cook-fire).
# =====================================================================================
HX, HZ = 3, 3                                    # hearth base foot (5x5), centre at (HX+2,HZ+2)
S.box(HX, HZ, 0.9, 5, 5, 0.5, HBASE)             # 5x5 raised base course (the cook platform)
# 3x3 fire ring on the base (8 stones, hollow centre)
RB = [(HX+1,HZ+1),(HX+2,HZ+1),(HX+3,HZ+1),(HX+1,HZ+2),(HX+3,HZ+2),(HX+1,HZ+3),(HX+2,HZ+3),(HX+3,HZ+3)]
for (sx, sz) in RB:
    S.box(sx, sz, 1.4, 1, 1, 0.6, RING, seam=True)
S.box(HX+2, HZ+2, 1.4, 1, 1, 0.5, RING)          # centre plinth -> the flame sits one block proud
S.box(HX+2.12, HZ+2.12, 1.9, 0.76, 0.76, 0.3, CAMP)   # campfire bed proud on the plinth
S.box(HX+2.18, HZ+2.18, 2.2, 0.64, 0.64, 0.16, EMBER) # ember band
# SMOKER + cauldron flanking on the base course (the cook-fire kit)
S.box(HX+0.1, HZ+2, 1.4, 1, 1, 1, SMOKE, seam=True)   # smoker body (left flank)
S.box(HX+0.2, HZ+2.1, 2.4, 0.8, 0.8, 0.18, SMOKET)    # smoker dark vent top
S.box(HX+4-0.1, HZ+2, 1.4, 0.9, 0.9, 0.7, CAULD, seam=True)  # cauldron (right flank)

# =====================================================================================
# CABIN-SHED (timber-framed, OPEN-fronted, GABLED) on the FAR side (back-left), footprint 5x4.
# POSTS y0-y2 at corners + 2 mid-posts; INFILL planks on back + both short sides; FRONT fully OPEN.
# GABLE ROOF (ridge runs the 4-long axis): eave stair course y3 on BOTH long eaves facing inward,
# inset 1 at y4, a spruce_slab ridge run at y5; gable triangles filled flush with planks.
# =====================================================================================
CX, CZ = 1, 1                                    # shed footprint x1..5, z1..4 (back-left, far side)
CW, CD = 5, 4
# 6 frame posts (4 corners + 2 mid on the long back) y0..2
POSTS = [(CX,CZ),(CX+CW-1,CZ),(CX,CZ+CD-1),(CX+CW-1,CZ+CD-1),(CX+2,CZ),(CX+2,CZ+CD-1)]
for (px, pz) in POSTS:
    S.box(px, pz, 0.9, 0.7, 0.7, 2.0, WLOG, seam=True)
# timber-frame INFILL planks: back wall (z=CZ) full + both SHORT side walls; FRONT (z=CZ+CD-1) OPEN
S.box(CX+0.6, CZ+0.1, 0.9, CW-1.2, 0.5, 1.9, PLANK, seam=True)      # back wall infill (low-z)
S.box(CX+0.1, CZ+0.6, 0.9, 0.5, CD-1.2, 1.9, PLANK, seam=True)      # left short side infill
S.box(CX+CW-0.6, CZ+0.6, 0.9, 0.5, CD-1.2, 1.9, PLANK, seam=True)   # right short side infill
# GABLE ROOF -- ridge runs the long (x) axis, centred at z=3 (CZ=1,CD=4). Two pitches slope DOWN
# from the central ridge to the front (high-z) eave and the back (low-z) eave. Build the gable END
# triangles FIRST (so the pitch is structurally read), then lay the eave + ridge courses across.
# gable triangle ends filled flush with planks on the two SHORT (x) ends -- a stepped A-frame:
for ex in (CX+0.15, CX+CW-0.85):
    S.box(ex, CZ+0.2, 1.9, 0.7, CD-0.4, 1.1, PLANK)               # gable base band (full depth, low)
    S.box(ex, CZ+0.9, 2.9, 0.7, CD-1.8, 1.0, PLANK)               # gable mid step (inset both sides)
    S.box(ex, CZ+1.5, 3.8, 0.7, CD-3.0, 0.9, PLANK)               # gable apex step (under the ridge)
# FRONT pitch: eave course (high-z, low) -> inset course (higher) climbing toward the ridge.
S.box(CX-0.3, CZ+CD-0.7, 2.9, CW+0.6, 1.0, 0.5, ROOF)             # front eave (high-z, lowest, proud)
S.box(CX-0.1, CZ+CD-1.6, 3.5, CW+0.2, 1.0, 0.5, ROOF2)           # front mid course (climbs in + up)
# BACK pitch: eave course (low-z, low) -> inset course climbing toward the ridge.
S.box(CX-0.3, CZ-0.3, 2.9, CW+0.6, 1.0, 0.5, ROOF)               # back eave (low-z, lowest, proud)
S.box(CX-0.1, CZ+0.6, 3.5, CW+0.2, 1.0, 0.5, ROOF2)              # back mid course (climbs in + up)
# RIDGE run (highest, centred at z=3) -- the spruce_slab cap where the two pitches meet.
S.box(CX-0.1, CZ+1.6, 4.1, CW+0.2, 0.8, 0.45, RIDGE)             # ridge slab run (lightest -> the peak line)
# hay-block bed corner inside (against the back+side -> grounded)
S.box(CX+0.7, CZ+0.7, 0.9, 1, 1, 0.6, HAY)

# =====================================================================================
# FURNISHINGS: a 5-6 seat log-bench arc round the hearth; 3 barrels + a 2-high crate; a BELL on a
# post near the road; a 2-board NOTICE/BOUNTY board on two posts. All grounded.
# =====================================================================================
# seating arc (far/left side of the fire) -- benches + single seats
S.box(HX-1.0, HZ+0.5, 0.9, 0.6, 3.0, 0.5, OAK)         # LEFT long bench (axis z)
S.box(HX-1.0, HZ+0.5, 0.9, 0.6, 0.55, 0.5, OAKE); S.box(HX-1.0, HZ+2.95, 0.9, 0.6, 0.55, 0.5, OAKE)
S.box(HX+0.5, HZ-1.0, 0.9, 3.0, 0.6, 0.5, OAK)         # BACK long bench (axis x)
S.box(HX+0.5, HZ-1.0, 0.9, 0.55, 0.6, 0.5, OAKE); S.box(HX+2.95, HZ-1.0, 0.9, 0.55, 0.6, 0.5, OAKE)
S.box(HX-1.0, HZ-1.0, 0.9, 0.7, 0.7, 0.5, OAK)         # corner stool closing the arc
# 3 barrels + a 2-high crate near the shed (grounded, abutting each other)
S.box(CX+CW+0.1, CZ+0.2, 0.9, 1, 1, 1, BARR, seam=True)        # barrel 1
S.box(CX+CW+0.1, CZ+1.2, 0.9, 1, 1, 1, BARR, seam=True)        # barrel 2 (abuts barrel 1)
S.box(CX+CW+0.1, CZ+0.2, 1.9, 1, 1, 1, BARR, seam=True)        # crate stacked on barrel 1 (2-high)
S.box(CX+CW+0.1, CZ+0.2, 2.85, 1, 1, 0.16, BARRT)             # crate hoop band
# BELL on a post near the road (waystation summons), right of the apron
S.box(9, 8, 0.9, 0.6, 0.6, 2.4, WLOG, seam=True)              # bell post
S.box(8.85, 7.85, 3.2, 0.9, 0.9, 0.7, BELL)                   # the bronze bell on the post top
# NOTICE/BOUNTY board: a 1x2 plank panel on two posts holding 2 hanging signs (right side, road-facing)
S.box(9.5, 5, 0.9, 0.5, 0.5, 2.6, WLOG)                       # board post A
S.box(11.0, 5, 0.9, 0.5, 0.5, 2.6, WLOG)                      # board post B
S.box(9.4, 5.0, 2.4, 2.1, 0.4, 1.1, PLANK)                    # the bounty plank panel (road-facing)
S.box(9.7, 4.95, 1.6, 0.5, 0.45, 0.7, SIGN)                   # hanging sign 1 under the panel
S.box(10.6, 4.95, 1.6, 0.5, 0.45, 0.7, SIGN)                  # hanging sign 2

# =====================================================================================
# TWIN-POST GATE-MARKER flanking the apron (the post signature grows to a banner-GATE): two 4-tall
# posts on floor plinths, a cross-lintel between them, chain+lantern each side, ONE banner on the
# taller post, a sign cluster at the base. Frames the road entrance (front, high-z).
# =====================================================================================
GLX, GRX, GZ = 4, 8, 9                            # gate posts straddling the x5..7 apron, at z9 (front)
# left gate post (the TALLER one -> carries the banner), 4 tall
S.box(GLX, GZ, 0.9, 0.8, 0.8, 0.5, BRICK)         # plinth
S.box(GLX+0.1, GZ+0.1, 1.4, 0.6, 0.6, 4.2, WLOG, seam=True)   # 4-tall post
# right gate post, slightly shorter
S.box(GRX, GZ, 0.9, 0.8, 0.8, 0.5, BRICK)
S.box(GRX+0.1, GZ+0.1, 1.4, 0.6, 0.6, 3.6, WLOG, seam=True)
# cross-lintel between the two posts (grounded on both)
S.box(GLX+0.1, GZ+0.25, 5.4, GRX-GLX, 0.4, 0.5, WLOG2)
# chain + lantern hung under the lintel each side (abut the lintel -> nothing floats)
S.box(GLX+0.5, GZ+0.3, 5.0, 0.16, 0.16, 0.4, CHAIN)
S.box(GRX+0.2, GZ+0.3, 5.0, 0.16, 0.16, 0.4, CHAIN)
# ONE palette-tinted banner down the front of the taller (left) post
S.box(GLX+0.12, GZ+0.85, 2.4, 0.6, 0.3, 2.6, BANNR)           # banner cloth (front face, road-facing)
S.box(GLX+0.12, GZ+1.12, 2.4, 0.6, 0.12, 2.6, BANND)         # shadow fold (2-tone drape)
# sign-post cluster at the gate base
S.box(GLX-0.7, GZ+0.7, 0.9, 0.5, 0.5, 1.8, WLOG2)            # sign post
S.box(GLX-1.3, GZ+0.7, 2.0, 1.2, 0.4, 0.7, SIGN)            # the directional board

# =====================================================================================
# ACCENTS: campfire flame, twin GATE lanterns, the ridge lantern (inside the shed), 1-2 seating-arc
# ground lanterns, a soft fill on the bounty board. ~5-6 lit sources (the waystation glows).
# =====================================================================================
S.accent(HX+2.5, HZ+2.5, 2.5, "glow", "#ff9a3c", r=3.6)      # campfire flame (proud on the plinth)
S.accent(GLX+0.4, GZ+0.5, 4.8, "glow", LANT, r=2.3)          # left gate lantern (under the lintel)
S.accent(GRX+0.4, GZ+0.5, 4.8, "glow", LANT, r=2.3)          # right gate lantern
S.accent(CX+2.5, CZ+2.0, 4.0, "glow", LANT, r=2.2)           # ridge lantern inside the shed
S.accent(HX-1.0, HZ+2.0, 1.5, "glow", LANT, r=1.9)           # seating-arc ground lantern (left)
S.accent(HX+2.0, HZ-1.0, 1.5, "glow", LANT, r=1.9)           # seating-arc ground lantern (back)
S.accent(10.4, 5.0, 3.0, "glow", "#cfe8e2", r=1.7)           # soft fill reading the bounty board

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(CX+2.5, CZ+2, 4.1, "timber-framed GABLED shed -- real ridge roof (eaves->inset->slab ridge)")
S.label(GLX+1, GZ+0.5, 5.4, "post -> a 4-tall TWIN-POST banner-GATE flanking the road apron")
S.label(HX+2.5, HZ+2.5, 2.4, "RAISED hearth -- flame one block proud + a SMOKER & cauldron cook-fire")
S.label(9, 8, 3.2, "a BELL on a post (waystation summons)")
S.label(10.2, 5, 2.4, "a 2-board BOUNTY / notice board")
S.label(0, 10, 1.4, "raised KERBED stone-brick court (wall + slab cap) + dirt apron")

out = S.svg(title="rest_stop R4 (Highway) -- a civic WAYSTATION: kerbed court, raised cook-hearth, a GABLED timber shed, bell + bounty board, a 4-tall twin-post banner-gate",
            size_label="13x11 court * h7 * 6 lanterns (the first GRAND payoff -- camp becomes civic infrastructure)",
            label_w=366)
open("detail_svg/rest_stop_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/rest_stop_highway.svg | bytes", len(out.encode()))
