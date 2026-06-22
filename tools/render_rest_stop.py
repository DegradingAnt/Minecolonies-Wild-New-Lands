"""rest_stop R5 (Great Road) detail render -> detail_svg/rest_stop.svg.
A believable roadside TRAVELLER'S CAMP on a medieval-wayshrine / Roman-mansio civic form: a
kerbed court with a single clear FOCAL hearth at its centre (stepped fire-monument + proud
campfire), a SEATING RING of log benches actually wrapping the hearth (the thing a traveller
builds to sit by the fire), ONE tall wayshrine STANDARD behind it as the single landmark
vertical, a tidy OPEN lean-to shelter off to one side, and a neat service corner with a
hitching rail, hay + a sunk water trough, plus a way-sign at the apron mouth.

DESIGN PRIORITY (readability at board scale): one clear focal centre (the hearth + seating
ring), ONE hero vertical (the standard), and everything else kept LOW and to the edges so the
layout reads as a sensible little camp, not a thicket of competing posts. Each element is
grounded on real support directly below it; no floating, no unsupported cantilevers.

Conventions copied from render_gatehouse.py / render_harbour.py: a named literal palette with
DISTINCT tones on a clear luminance ladder; columns stand PROUD with darker base/capital bands;
lanterns/flame via accents; right-hand callout labels; a size_label.

Inspiration (FORM/scale/technique only, never copied; CREDITS.md): medieval roadside
wayshrines + Roman mansio/mutatio road-stations; CTOV / Moog's Paths roadside camps;
MineColonies / Byzantine timber-frame shelters; structurize stepped-plinth civic massing.
Built entirely from original geometry in vanilla blocks; no assets/NBT/palette taken."""
from iso_render import Iso

S = Iso(U=12)

# ---- palette (literal) -- DISTINCT tones, WIDE luminance spread so every element reads ----
# Stone ladder (dark->light): KERB < FLOOR < STEP < CAP < DAIS < COL ; warm timber family kept
# DARK + LOW so the furniture/shelter sit DOWN and the pale standard + hearth read as the heroes.
KERB  = "#6d7177"   # polished-andesite kerb ring (DARKEST stone -- frames + lifts the court)
FLOOR = "#9d988d"   # court field (mid stone-brick grey)
FLR2  = "#857f72"   # darker floor variant (worn/mossy scatter -- reads as laid cells)
APRON = "#6a5532"   # dirt-path ceremonial apron to the avenue (deeper earth)
STEP  = "#c2bdb0"   # hearth-monument stepped courses (PALE dressed stone, pops off FLOOR)
RING  = "#75786f"   # hearth fire-ring stone (dark, so the flame pops hard)
COL   = "#ece7da"   # dressed-stone standard plinth / shelter posts (near-white, HIGH contrast)
CAP   = "#aa9f88"   # base + capital + cornice bands (WARM mid -- distinct from STEP)
DAIS  = "#bdb6a4"   # shelter dais (its own warm-pale tone)
WALL  = "#7c7363"   # shelter back-wall infill (DARK warm, posts pop on it)
MAST  = "#caa24e"   # wayshrine-standard shaft -- GOLD-OAK (the one tall hero vertical)
POST  = "#6f5230"   # warm timber posts / log benches / hitching rail
BEAM  = "#5a4427"   # darker beams + rail + sign frame
PLANK = "#9c7444"   # plank panels / sign board / barrels (lighter warm timber)
SLATE = "#34303b"   # dark spruce roof eave (max contrast vs pale stone)
SLAT2 = "#474252"   # roof mid course (lighter -> reads the step-in)
SLAT3 = "#5a5566"   # roof ridge cap (lightest roof tone -> the ridge reads)
HAY   = "#d4b441"   # hay block (gold)
WATER = "#3f78b4"   # trough water (brighter blue -> reads as water, not shadow)
TROUF = "#8a8478"   # trough kerb stone (distinct from court so the basin reads)
GLASS = "#bfe6df"   # stained-glass / lantern-box accent (cool cyan, pops on warm)
BANNR = "#a83535"   # ONE palette-tinted civic banner (deep red, the single saturated accent)

# =====================================================================================
# COURT: raised kerb ring + stone-brick field (light per-cell scatter) + ceremonial apron
# court grid x0..15, z0..13 ; apron runs out the front (high z = nearer viewer)
# A tighter court than a civic forum -- this is a CAMP, sized so the hearth fills it.
# =====================================================================================
S.box(0, 0, 0, 15, 13, 1, KERB)                 # kerb base slab (whole footprint)
S.box(1, 1, 1, 13, 11, 1, FLOOR)                # raised court field, kerb proud 1 all round
# light per-cell worn scatter (reads as laid cells without busying the field)
for (fx, fz) in [(2, 2), (10, 2), (3, 9), (11, 9)]:
    S.box(fx, fz, 1, 2, 1, 1, FLR2)
# raised kerb wall lip on the back + two sides (front centre open for the apron)
S.box(0, 0, 1, 15, 1, 1, KERB)                  # back kerb wall
S.box(0, 1, 1, 1, 11, 1, KERB)                  # left kerb wall
S.box(14, 1, 1, 1, 11, 1, KERB)                 # right kerb wall
# 3-wide ceremonial dirt apron meeting the avenue (front, through a kerb gap)
S.box(5, 12, 1, 1, 1, 1, KERB); S.box(9, 12, 1, 1, 1, 1, KERB)  # the two kerb cheeks
S.box(6, 12, 1, 3, 1, 1, APRON)                 # the open path slot through the kerb gap
S.box(6, 13, 0, 3, 2, 1, APRON)                 # apron tongue running out to the road

# =====================================================================================
# FOCAL HEARTH (court CENTRE): a low stepped fire-monument 5x5 -> 3x3 + a proud campfire.
# Kept LOW (3 courses) and central so it is unmistakably the heart of the camp, with the
# seating ring (below) wrapping it -- the legible thing a traveller actually builds.
# =====================================================================================
HX, HZ = 5, 4                                    # hearth centred in the court
S.box(HX,   HZ,   1, 5, 5, 1, STEP)              # step 1 (5x5 pale plinth)
S.box(HX+1, HZ+1, 2, 3, 3, 1, RING)             # step 2 / fire-ring base (3x3, dark)
S.box(HX+1, HZ+1, 3, 3, 3, 1, RING, seam=True)  # ring wall course (hollow centre below)
S.box(HX+2, HZ+2, 3, 1, 1, 1, RING)             # centre fire plinth (flame sits proud)

# =====================================================================================
# SEATING RING: four flat log benches set back off the hearth's pale plinth, one to a side,
# so the camp reads as 'sit by the fire'. Grounded flat on the court (1 course).
# =====================================================================================
S.box(HX+1, HZ-1, 1, 3, 1, 1, POST)             # back bench (behind the hearth)
S.box(HX+1, HZ+5, 1, 3, 1, 1, POST)             # front bench (nearest the viewer)
S.box(HX-1, HZ+1, 1, 1, 3, 1, POST)             # left bench
S.box(HX+5, HZ+1, 1, 1, 3, 1, POST)             # right bench

# =====================================================================================
# WAYSHRINE STANDARD (the single tall hero vertical): a 3x3 stepped plinth -> a tall gold-oak
# shaft -> a cross-arm with lanterns -> a cornice cap + glass lantern-box crown + ONE banner.
# Placed in the BACK-LEFT corner (low x, low z = up-left on screen) so it stands CLEAR of the
# central hearth instead of occluding it, while still reading as the tallest landmark vertical.
# =====================================================================================
MX, MZ = 1, 1                                    # standard foot in the back-left corner
S.box(MX, MZ, 1, 3, 3, 1, KERB)                  # broad kerb-stone plinth step A (3x3 dark base)
S.box(MX, MZ, 2, 3, 3, 1, CAP)                   # plinth step B (warm inset-read course)
S.box(MX+1, MZ+1, 3, 1, 1, 1, COL)               # dressed socket band (reads the step-up)
S.box(MX+1, MZ+1, 4, 1, 1, 7, MAST, seam=True)   # the GOLD-OAK shaft (y4..y10) -- the distant vertical
S.box(MX, MZ+1, 9, 3, 1, 1, BEAM)               # cross-arm carrying lanterns (dark, reads)
S.box(MX+1, MZ+1, 11, 1, 1, 1, CAP)             # carved cornice cap band
S.box(MX+1, MZ+1, 12, 1, 1, 1, GLASS)           # stained-glass lantern-box crown (y12)
# ONE tinted banner hanging down the front (near-viewer) face of the shaft -- the sole banner
S.box(MX+1, MZ+2, 5, 1, 1, 4, BANNR)

# =====================================================================================
# OPEN LEAN-TO SHELTER (4x4) off to the RIGHT side, kept subordinate to the standard.
# A real lean-to: the OPEN FACE looks toward the hearth (near/high-z side) on two TALL light
# posts; a LOWER dark-timber back wall closes the far (low-z) side; a single-pitch SHED roof
# slopes from high-over-the-open-front DOWN to the low back, with a proud eave overhang. Each
# roof course steps down onto real support below it -- no cantilever, no floating.
# =====================================================================================
PX, PZ = 10, 6                                   # shelter footprint x10..13, z6..9 (open face at z9)
S.box(PX, PZ, 1, 4, 4, 1, DAIS)                  # raised stone dais one course proud
# LOW back wall closing the far side (low-z) -- dark timber infill, y2..y5
S.box(PX, PZ, 2, 4, 1, 4, WALL, seam=True)       # back-wall panel run (far side, z=PZ)
# back corner posts (short, frame the closed back) + TALL front posts (the open face)
for (cx, cz) in [(PX, PZ), (PX+3, PZ)]:           # back posts -- to y5 (back is the LOW side)
    S.box(cx, cz, 2, 1, 1, 1, CAP)               # base band
    S.box(cx, cz, 3, 1, 1, 2, COL)               # short light shaft (y3..y4)
    S.box(cx, cz, 5, 1, 1, 1, CAP)               # capital band
for (cx, cz) in [(PX, PZ+3), (PX+3, PZ+3)]:       # FRONT posts -- TALL to y7 (open face, high side)
    S.box(cx, cz, 2, 1, 1, 1, CAP)               # base band
    S.box(cx, cz, 3, 1, 1, 4, COL)               # tall light shaft (y3..y6)
    S.box(cx, cz, 7, 1, 1, 1, CAP)               # capital band carrying the eave
# single-pitch SHED roof: HIGH over the open front (y8) -> steps DOWN to the low back (y6).
# alternating SLATE/SLAT2 tones so each descending course reads as a distinct slope step.
S.box(PX-0.4, PZ+3, 8, 4.8, 1.4, 1, SLATE)       # front eave (proud overhang over the tall front posts)
S.box(PX, PZ+2, 8, 4, 1, 1, SLAT2)               # 2nd course (one back, same height -> ridge band)
S.box(PX, PZ+1, 7, 4, 1, 1, SLAT3)               # 3rd course steps DOWN (lit tone, reads the pitch)
S.box(PX-0.4, PZ-0.4, 6, 4.8, 1.4, 1, SLATE)     # back eave course (lowest, proud over the back wall)
# a small bench inside the shelter, facing the open front
S.box(PX+1, PZ+1, 2, 2, 1, 1, POST)

# =====================================================================================
# SERVICE CORNER (back-right): a tidy hitching rail with hay + a sunk water trough.
# Two posts carry a rail; hay bales beside it; the trough is a stone basin with water.
# All low and grouped so it reads as one functional corner.
# =====================================================================================
S.box(11, 1, 1, 1, 1, 2, POST)                   # hitch post A
S.box(13, 1, 1, 1, 1, 2, POST)                   # hitch post B
S.box(11, 1, 2, 3, 1, 1, BEAM)                   # hitch rail spanning the posts (grounded on A+B)
S.box(11, 2, 1, 1, 1, 1, HAY)                    # hay bale 1
S.box(12, 2, 1, 1, 1, 1, HAY)                    # hay bale 2
# water trough: two stone end-kerbs with water in the gap between (no overlap)
S.box(11, 3, 1, 1, 1, 1, TROUF)                  # basin end-kerb (left)
S.box(13, 3, 1, 1, 1, 1, TROUF)                  # basin end-kerb (right)
S.box(12, 3, 1, 1, 1, 1, WATER)                  # water surface in the basin gap

# =====================================================================================
# WAY-SIGN at the apron mouth (front): a single post carrying two hanging direction boards.
# The ONLY furniture at the front, so the apron reads clean as the road entrance.
# =====================================================================================
S.box(7, 11, 1, 1, 1, 3, POST)                   # sign post on the court edge by the apron
S.box(6, 11, 3, 1, 1, 1, PLANK)                  # left hanging board
S.box(8, 11, 3, 1, 1, 1, PLANK)                  # right hanging board

# =====================================================================================
# A BARREL PAIR by the shelter (small lived-in touch, kept to one tidy spot)
# =====================================================================================
S.box(9, 9, 1, 1, 1, 1, PLANK)                   # barrel
S.box(9, 10, 1, 1, 1, 2, PLANK)                  # crate stack (2 high)

# =====================================================================================
# ACCENTS: the hearth flame, the standard lanterns + crown + finial, shelter eave lanterns,
# the way-sign lantern. Every glow sits on a real post/arm/bracket directly below it.
# =====================================================================================
# hearth campfire flame -- proud on the fire-ring plinth (the focal warmth)
S.accent(HX+2.5, HZ+2.5, 4.4, "glow", "#ff9a3c", r=4.2)
# wayshrine-standard cross-arm lanterns + glass-box crown + finial
S.accent(MX+0.4, MZ+1.5, 9.4, "glow", r=2.4)
S.accent(MX+2.6, MZ+1.5, 9.4, "glow", r=2.4)
S.accent(MX+1.5, MZ+1.5, 12.6, "glow", "#eafff8", r=2.8)
S.accent(MX+1.5, MZ+1.5, 12.8, "finial")
# shelter eave lanterns (hung under the tall front eave, on the two open-face front posts)
S.accent(PX+0.3, PZ+3.5, 7.4, "glow", r=2.2)
S.accent(PX+3.7, PZ+3.5, 7.4, "glow", r=2.2)
# way-sign lantern at the apron mouth
S.accent(7.5, 11.5, 4.4, "glow", r=2.0)

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(HX+2.5, HZ+2.5, 3, "central hearth + log-bench ring — the camp's heart")
S.label(MX+1.5, MZ+1.5, 12, "tall wayshrine standard — the single landmark vertical")
S.label(PX+2, PZ+2, 8, "open lean-to shelter — tall front, shed roof slopes to a low back")
S.label(12, 2, 2, "hitching rail — hay + sunk water trough")
S.label(7, 11, 3, "way-sign marks where the road meets the camp")
S.label(7.5, 14, 1, "3-wide dirt apron meets the avenue")

out = S.svg(title="rest_stop R5 (Great Road) — a believable roadside traveller's camp (mansio / wayshrine form)",
            size_label="15×13 court · h13 (wayshrine standard reads from afar)")
open("detail_svg/rest_stop.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/rest_stop.svg | bytes", len(out.encode()))
