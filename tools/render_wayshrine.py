"""Wayshrine R5 (Great Road) detail render -> detail_svg/wayshrine.svg.
The top rung of the wayshrine ladder: a monumental colonnaded lantern-CHAPEL on a three-step
temenos plinth, with a GRAND corbel-arch GATEWAY straddling the road the traveller passes under.
Faithful to deco_catalog_v2 'wayshrine' Great-Road tier (17x17 precinct, h18, asymmetric porch +
lower colonnade, arched backing-wall niche + marker stele, solid entablature, stepped-hip roof
with supported finial-lantern, banners, gateway arch, flanking lamp-posts, benches, bollards).

v3 HERO PASS (author: "bare next to gatehouse/harbour — does not match hero quality"):
finer U=8 grid for real detail. Articulated the cella: LIT LANCET/ARCHED window niches down the
side wall + BUTTRESSES/pilasters between them; ROOF now has an eave overhang, a clear RIDGE line,
corner HIPS, and a GABLE FACE carrying a rose-window niche; columns gained base+capital+flute hint;
the GATEWAY is grander + clearly connected straddling the road (taller 2x2 piers, deep stepped
corbel voussoir + bright keystone, gate lanterns); more lamp-posts + grounded finial. Every top
element sits on real support below it (grounded build technique per spec).

Inspiration (FORM/scale/technique ONLY, nothing reproduced; credited in CREDITS.md): the European
wayside aedicula / lantern-of-the-dead / wayside chapel + the Roman columned roadside monument and
corbel gateway-over-the-road. All vanilla blocks; geometry/arch/niche/plinth are original WNL."""
from iso_render import Iso

S = Iso(U=8, occlusion=True)

# ---- palette (literal) -- a clear luminance ladder so no two adjacent faces blend.
#      Convention (gatehouse/plaza): the COLONNADE + dressed accents read LIGHT, the cella WALL is
#      a DARKER warm stone so the pale columns + window frames + buttress caps pop off it.
#      Ladder dark->light: SLATE < RIDGE < ROAD < WALL < AND < STB < ARCH < PAD < CAP < COL < KEY.
STB   = "#8f897c"   # stone bricks (base plinth step, warm mid)
AND   = "#83868b"   # polished andesite (mid plinth step, cool -> separates the courses)
PAD   = "#cdc8bd"   # smooth-stone / chiselled paved terrace (light, the yard you walk on)
WALL  = "#79735f"   # cella stone-brick body (DARK warm dressed stone -> pale columns + frames pop)
BUTT  = "#beb7a3"   # buttress / pilaster bodies on the cella sides (light mid, proud of the wall)
COL   = "#e7e2d5"   # colonnade + porch shafts (near-white dressed stone -- the hero light mass)
CAP   = "#aaa395"   # column base + capital + architrave band (warm mid, frames the light shafts)
ARCH  = "#9a927e"   # gateway voussoir + niche reveal -- DEEP warm stone (the arch reads recessed)
ARCHK = "#b1a991"   # voussoir highlight course (a touch lighter -> each corbel step reads stepped)
KEY   = "#efe9d4"   # chiselled keystone / lintel / finial / abacus (brightest dressed stone)
FRAME = "#cabf9d"   # chiselled window-frame + sill stone (warm, lit niche reads framed)
GLASS = "#5fa0bd"   # lancet glazing (deep teal -> reads as glass, not pale stone)
GLOWP = "#bfe9f2"   # lit-pane / lantern highlight (icy night-glow)
SLATE = "#3f3b48"   # hipped roof field (darkest slate -> strong contrast vs pale columns)
RIDGE = "#534e5b"   # roof ridge / hip arrises (lighter slate -> stepped read)
BANNER= "#a83a31"   # heraldic banner cloth (the one saturated accent)
BANNERD="#7e2a23"   # banner shadow fold (2-tone drape)
TIMBER= "#7a5c3a"   # lamp-post standards (warm timber)
ROAD  = "#5c4a2e"   # dirt path through the precinct (clearly earth)

# geometry anchors -- chapel core x2..15 (back terrace), road runs front-to-back through x8..11
CELLA_X = 3         # cella body left edge
CELLA_W = 11        # cella body width (x3..14)

# =====================================================================================
# 1) THREE-STEP MONUMENTAL TEMENOS PLINTH (17x17 -> 15x15 -> 11x11 core) + paved yard
# =====================================================================================
S.box(0, 0, 0, 17, 17, 1, STB)                    # course 1: stone bricks 17x17
S.box(1, 1, 1, 15, 15, 1, AND)                    # course 2: polished andesite 15x15
S.box(2, 1, 2, 13, 8, 1, PAD)                     # course 3: chiselled/smooth back terrace the chapel stands on
S.box(2, 9, 2, 13, 6, 1, AND)                     # front yard paving (a touch darker -> the terrace reads raised)
# chiselled corner inlay nodes dotting the paved yard (spec: yard inlay nodes)
for ix, iz in [(2,13),(14,13),(2,9),(14,9)]:
    S.box(ix, iz, 3, 1, 1, 1, KEY)
# broad 7-wide grand front stair down to the road yard (spec: 7-wide grand stair)
S.box(5, 14, 2, 7, 1, 1, PAD)                     # stair lip / tread

# =====================================================================================
# 2) GRAND GATEWAY ARCH straddling the road (great-road EXCLUSIVE mass)
#    Two 2x2 piers flank the carriageway; a deep stepped corbel voussoir spans to a bright
#    keystone, so the traveller passes UNDER the shrine. Tall + clearly connected to the yard.
# =====================================================================================
# the road slot the gate straddles (front yard, under the arch, into the precinct)
S.box(8, 9, 2, 4, 8, 1, ROAD)                     # paved/dirt road slot x8..11, z9..16
# -- twin 2x2 piers straddling the road, set FORWARD (z=14, nearer the viewer) so the gate reads
#    as its own grand mass out IN FRONT of the chapel, not buried in the colonnade. TALL (y3..12). --
def gate_pier(px):
    S.box(px-0.3, 13.7, 2, 2.6, 2.6, 1, CAP)      # moulded footing (proud -> reads as a base)
    S.box(px, 14, 3, 2, 2, 9, COL, seam=True)     # 2x2 pier shaft y3..12 (light dressed stone, tall)
    S.box(px-0.25, 13.75, 12, 2.5, 2.5, 1, CAP)   # pier cap / impost the arch springs from
gate_pier(6)                                       # west pier (x6..7), road opening x8..11
gate_pier(12)                                      # east pier (x12..13)
# -- DEEP stepped corbel voussoir arch over the 4-wide opening (each course steps inward 1,
#    supported by the course beneath; alternating ARCH/ARCHK so every corbel step reads) --
S.box(8, 14, 12, 1, 2, 1, ARCH)                   # left springer (off the west impost)
S.box(11, 14, 12, 1, 2, 1, ARCH)                  # right springer (off the east impost)
S.box(8.5, 14, 13, 1, 2, 1, ARCHK)               # 2nd corbel course, stepped in
S.box(10.5, 14, 13, 1, 2, 1, ARCHK)
S.box(9, 14, 14, 1, 2, 1, ARCH)                   # 3rd corbel course
S.box(10, 14, 14, 1, 2, 1, ARCH)
S.box(9, 14, 15, 2, 2, 1, KEY)                    # bright chiselled keystone closing the crown
S.box(8, 14, 16, 4, 2, 1, ARCH)                   # solid backing course locking the keystone (spec)
S.box(8.6, 13.9, 17, 2.8, 0.4, 1, CAP)           # gate coping band along the crown (a clean cornice line)
S.box(9, 14, 17, 2, 2, 1, KEY)                    # small chiselled cresting on the gate (grounded peak)

# =====================================================================================
# 3) THE CELLA -- colonnaded lantern-chapel body on the back terrace (y=3), x3..14 z2..7
#    DARK dressed-stone walls ARTICULATED with LIT LANCET window niches + BUTTRESSES.
# =====================================================================================
# -- main cella mass (back wall + side walls, a real room) --
S.box(CELLA_X, 2, 3, CELLA_W, 5, 6, WALL, seam=True)   # cella body x3..14, z2..7, y3..9
# a continuous dressed string-course belt midway up breaks the tall flat face
S.box(CELLA_X-0.3, 1.7, 6, CELLA_W+0.6, 5.6, 0.5, CAP) # proud belt course (warm -> reads as a shadow line)

# -- BUTTRESSES / engaged pilasters on the visible EAST (x=14) + FRONT (z=7) faces --
#    stepped offsets (battered foot -> shaft -> weathered cap), light so they stand proud.
def buttress(bx, bz, face):                        # face 'east' or 'front'
    if face == "east":
        S.box(bx, bz, 3, 0.8, 1.4, 5, BUTT)        # buttress body proud of the east wall
        S.box(bx-0.15, bz-0.15, 7.6, 1.1, 1.7, 0.7, CAP)   # weathered set-off cap
        S.box(bx+0.05, bz+0.1, 8.3, 0.6, 1.2, 0.6, KEY)    # small pinnacle stub (grounded on the cap)
    else:
        S.box(bx, bz, 3, 1.4, 0.8, 5, BUTT)
        S.box(bx-0.15, bz-0.15, 7.6, 1.7, 1.1, 0.7, CAP)
        S.box(bx+0.1, bz+0.05, 8.3, 1.2, 0.6, 0.6, KEY)
buttress(14, 2.6, "east")                          # east wall buttress (back)
buttress(14, 5.4, "east")                          # east wall buttress (front) -> brackets a window bay
buttress(CELLA_X-0.5, 7, "front")                  # front-left corner buttress

# -- LIT LANCET / ARCHED window niches in the EAST wall (the cella 'glows') --
#    deep dark reveal + teal glazing + pointed stone apex + sill ledge, set proud of x=14 face.
for wz in (3.4, 6.0):                              # two tall lights bracketed by the buttresses
    S.box(14.55, wz, 4.3, 0.5, 0.9, 3, FRAME)      # chiselled jamb frame (light, recessed read)
    S.box(14.6, wz+0.15, 4.5, 0.45, 0.6, 2.3, GLASS)   # tall glazed light (deep teal)
    S.box(14.6, wz+0.15, 6.8, 0.45, 0.6, 0.5, FRAME)   # pointed lancet apex stone
    S.box(14.5, wz-0.05, 4.1, 0.55, 0.9, 0.4, FRAME)   # window sill ledge
# -- a window niche on the FRONT (z=7) face too, beside the porch, so both visible faces read --
S.box(CELLA_X+0.6, 7.55, 4.3, 0.9, 0.5, 3, FRAME)
S.box(CELLA_X+0.75, 7.6, 4.5, 0.6, 0.45, 2.3, GLASS)
S.box(CELLA_X+0.75, 7.6, 6.8, 0.6, 0.45, 0.5, FRAME)

# -- the ARCHED PRINCIPAL NICHE in the back, opening through the front porch: a 3-wide recess
#    with a chiselled backing panel, corner-stair arch + keystone, marker stele + candle row. --
S.box(7, 6.6, 3, 3, 0.6, 4, WALL)                 # recessed dark back panel of the niche (front face z6.6)
S.box(7, 6.5, 3, 3, 0.4, 0.4, KEY)                # chiselled offering-ledge / threshold
S.box(7.4, 6.55, 3, 2.2, 0.4, 0.5, FRAME)         # marker-stele slab table (smooth slab on a plinth)
S.box(7, 6.5, 7, 1, 0.5, 1, ARCH)                 # niche arch left corner stair
S.box(9, 6.5, 7, 1, 0.5, 1, ARCH)                 # niche arch right corner stair
S.box(8, 6.5, 7, 1, 0.5, 1, KEY)                  # niche keystone

# =====================================================================================
# 4) ASYMMETRIC COLONNADE -- double-height FRONT PORCH piers + lower side columns
#    light shafts standing proud, each with a BASE + CAPITAL + a fluting hint, on z=8 (1 proud).
# =====================================================================================
def column(cx, height, wide=1.0):                  # grounded column: base -> fluted shaft -> capital
    S.box(cx, 8, 3, wide, 1, 1, CAP)               # base block
    S.box(cx+0.06, 8.1, 4, wide-0.12, 0.8, height, COL, seam=True)   # shaft (light) -- inset = a flute/relief hint
    S.box(cx, 8, 4, 0.12, 0.8, height, BUTT)       # left flute shadow strip
    S.box(cx+wide-0.12, 8, 4, 0.12, 0.8, height, BUTT)   # right flute shadow strip
    S.box(cx-0.12, 7.88, 4+height, wide+0.24, 1.2, 0.9, CAP)   # spreading capital (proud -> casts a line)
    S.box(cx, 8.1, 4.9+height, wide, 0.8, 0.4, KEY)            # bright abacus crown on the capital
# double-height FRONT PORCH: two tall 2-wide piers framing the principal niche (spec: porch)
column(4.5, 7, wide=2.0)                            # tall west porch pier (x4.5..6.5)
column(10.5, 7, wide=2.0)                           # tall east porch pier (x10.5..12.5)
# lower SIDE colonnade columns (the asymmetric rhythm, shorter shafts)
for cx in (3.2, 13.0):
    column(cx, 5, wide=1.0)

# -- SOLID entablature ring across the porch-pier capitals (block-to-block, supported at piers) --
S.box(4.2, 7.9, 12.1, 8.8, 1.0, 0.8, CAP)         # architrave beam over the porch (warm band)
S.box(4.2, 7.85, 12.9, 8.8, 1.0, 0.4, KEY)        # bright cornice fillet above the architrave

# =====================================================================================
# 5) GRAND STEPPED-HIP ROOF over the cella core -- eave overhang, ridge line, corner hips,
#    a GABLE FACE with a rose-window niche, and a grounded stepped-apex finial.
# =====================================================================================
# -- broad eave course overhanging the walls + porch on all sides (1.5-block overhang) --
S.box(CELLA_X-1.0, 0.8, 9, CELLA_W+2.4, 7.4, 1, SLATE)   # eave course (proud overhang -> shadow line)
# -- a clear GABLE FACE on the front (z), filling the triangle, carrying a rose-window niche --
S.box(CELLA_X+1, 6.6, 9, CELLA_W-2, 0.5, 2, WALL)       # gable tympanum field (dressed stone, fills the face)
S.box(7.6, 6.5, 9.6, 1.8, 0.4, 1.8, FRAME)             # rose-window stone frame ring (light)
S.box(7.9, 6.45, 9.9, 1.2, 0.4, 1.2, GLASS)            # rose-window glazing (teal, lit at night)
S.box(CELLA_X+1, 6.55, 11, CELLA_W-2, 0.5, 1, KEY)     # gable-coping run capping the tympanum
# -- the hip roof climbing inward course by course to a RIDGE (each course inset 1, grounded) --
S.box(CELLA_X, 1.8, 10, CELLA_W, 5.4, 1, SLATE)        # first roof course
S.box(CELLA_X+1, 2.8, 11, CELLA_W-2, 3.4, 1, RIDGE)    # second course (lighter -> stepped read)
S.box(CELLA_X+2, 3.8, 12, CELLA_W-4, 1.4, 1, SLATE)    # third course
S.box(CELLA_X+2, 4.0, 13, CELLA_W-4, 1.0, 1, RIDGE)    # RIDGE run (the clear horizontal crest line)
# -- corner HIP arrises: lighter diagonal slate runs picking out the four hips off the eaves --
S.box(CELLA_X+0.3, 2.1, 10, 1, 1, 1, RIDGE)
S.box(CELLA_X+CELLA_W-1.3, 2.1, 10, 1, 1, 1, RIDGE)
S.box(CELLA_X+0.3, 6.0, 10, 1, 1, 1, RIDGE)
S.box(CELLA_X+CELLA_W-1.3, 6.0, 10, 1, 1, 1, RIDGE)
# -- grounded STEPPED-APEX finial: a 3x3 -> 1x1 chiselled block-stack on the ridge (not a spike) --
S.box(CELLA_X+3.5, 3.8, 14, 3, 1.4, 1, KEY)           # 3-wide finial base (sits on the ridge course)
S.box(CELLA_X+4.5, 4.1, 15, 1, 0.8, 1, KEY)           # 1-wide finial cap (the crowning block)

# =====================================================================================
# 6) BANNERS on the front-porch pier faces (heraldic, 2-tone drape) + benches/bollards
# =====================================================================================
for px in (5.0, 11.0):
    S.box(px, 7.55, 6, 1, 0.4, 4, BANNER)             # banner cloth on the porch pier face (z7)
    S.box(px, 7.95, 6, 1, 0.2, 4, BANNERD)            # shadowed trailing fold (2-tone)
# low bollards + benches lining the approach (spec: a PLACE to stop)
for bx in (4, 13):
    S.box(bx, 10, 3, 0.8, 0.8, 1, CAP)               # bollard flanking the road approach
S.box(2.5, 11.2, 3, 2, 0.8, 0.5, PAD)                # bench W (smooth-slab seat)
S.box(12.5, 11.2, 3, 2, 0.8, 0.5, PAD)               # bench E

# =====================================================================================
# 7) FREE-STANDING GRAND FLANKING LAMP-POSTS flanking the grand stair (spec payoff)
#    set on the front corners of the yard, clear of the forward gate piers.
# =====================================================================================
for lx in (2.4, 13.6):
    S.box(lx-0.2, 15.0, 2, 1.4, 1.4, 1, CAP)         # stone footing on the yard front corner
    S.box(lx, 15.2, 3, 1, 1, 4, TIMBER)              # lamp standard
    S.box(lx-0.25, 14.95, 7, 1.5, 1.5, 0.6, CAP)     # solid cap / collar (the lantern hangs under it)
    S.box(lx-0.1, 15.1, 7.6, 1.2, 1.2, 1.1, GLOWP)   # glazed lantern head (lit)
    S.box(lx+0.1, 15.3, 8.7, 0.8, 0.8, 0.5, SLATE)   # lantern roof cap

# =====================================================================================
# ACCENTS -- niche flame focal, lit lancet glows, gate + lamp lights, rose window, finial
# =====================================================================================
S.accent(8.5, 6.6, 4.2, "glow", "#ffd47a", r=3.2)    # abstract flame-in-niche focal (candle row + soul-lantern)
# lit lancet window glows on the cella east face (the chapel reads lit at night)
S.accent(14.9, 3.85, 5.6, "glow", GLOWP, r=1.9)
S.accent(14.9, 6.45, 5.6, "glow", GLOWP, r=1.9)
S.accent(CELLA_X+1.05, 7.9, 5.6, "glow", GLOWP, r=1.7)   # front-face lancet glow
S.accent(8.5, 6.9, 10.5, "glow", GLOWP, r=2.2)       # rose-window glow on the gable
# gateway-arch pier lanterns (each pier carries a lantern -> the gate reads lit)
S.accent(6.5, 13.5, 11.6, "glow", r=2.8)
S.accent(13.5, 13.5, 11.6, "glow", r=2.8)
# grand flanking lamp-post heads (front corners)
S.accent(2.9, 15.7, 8.1, "glow", "#ffe6a8", r=2.6)
S.accent(14.1, 15.7, 8.1, "glow", "#ffe6a8", r=2.6)
# roof-finial crowning lantern (hung under the supported finial block) + finial marker
S.accent(8.5, 4.5, 15.0, "glow", "#eafff8", r=2.4)
S.accent(8.5, 4.5, 15.2, "finial")

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(9, 3, 13, "stepped-hip roof: eave, ridge line + corner hips")
S.label(8.5, 6.6, 10, "gable face + rose-window niche")
S.label(14.9, 4.5, 5.6, "lit lancet windows + buttresses on the cella")
S.label(8.5, 6.6, 4.2, "arched principal niche -- flame-in-niche + stele")
S.label(9, 14, 16, "grand corbel gateway straddles the road")
S.label(11, 8, 11, "asymmetric porch + colonnade (base + capital + flute)")
S.label(3, 15, 1, "three-step temenos plinth (17 -> 15 -> 11)")

out = S.svg(title="Wayshrine R5 (Great Road) -- colonnaded lantern-chapel + grand gateway over the road",
            size_label="17x17 precinct . h18 . gateway straddles the carriageway",
            pad=20, label_w=320)
open("detail_svg/wayshrine.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/wayshrine.svg | bytes", len(out.encode()))
