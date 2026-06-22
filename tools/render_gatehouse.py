"""Gatehouse H6 (Great Road) detail render -> detail_svg/gatehouse.svg.
The grandest rung: a monumental ceremonial twin-tower city-gate the avenue passes UNDER,
seated on a 3-step Roman dais. Double-chamfered twin towers flank a pointed-vault carriageway;
a glass-galleried lit upper storey bridges them under its own peaked roof; deep machicolation,
crenellated banner-flanked parapets, peaked finialed tower roofs, engaged pilasters framing the
mouth, soffit lanterns down the tunnel, and free-standing flanking lamp-posts on the dais.

Conventions copied from render_wayshrine.py / render_plaza.py: named literal palette; dressed-stone
towers stand PROUD and read LIGHT against darker walls/roofs; warm timber + banners for contrast;
lanterns/flames via accents; callout labels; a size_label.

Original WNL composition. Inspiration (form/scale/technique study ONLY, nothing reproduced):
Roman city gates + triumphal arches (Porta Nigra Trier, Arch of Constantine) for the twin-mass +
pilaster-framed carriageway + chamber-over-the-gate; medieval castle gatehouses (machicolation,
crenellation, arrow-slits); MineColonies/CTOV/D&T gatehouse-towers for tower proportion/feel.
Credited in CREDITS.md; geometry/vault/machicolation/plinth/gallery are entirely original.
"""
from iso_render import Iso

S = Iso(U=8)

# ---- palette (literal) -- DISTINCT tones spread on a clear luminance ladder so NO two
#      adjacent faces blend. v3 contrast pass: pushed the dais cool+dark away from the warm
#      walls; sank ARCH well below CHAMF so the vault reads as a recessed dark band; cooled +
#      darkened GLASS so it reads as glazing (not pale stone); split SILL clear of PMOULD.
#      Ladder (luminance, dark->light): SLATE < RIDGE < PLINTH < WALL < GLASS < PMOULD <
#      ARCH < SILL < CHAMF < PILAST < TOWER < KEY  -- every neighbour pair separated.
PLINTH = "#5f6166"   # dais core -- cool slate-grey base mass (clearly DARKER + cooler than walls)
PMOULD = "#9a9488"   # plinth moulded riser / stair edging (warm mid)
WALL   = "#766f60"   # carriageway + chamber walls (DARK warm dressed stone, towers pop off it)
TOWER  = "#e3ddce"   # tower shafts (near-white dressed stone -- the LIGHT hero mass)
CHAMF  = "#c4bda9"   # chamfer / base step / capital + machicolation band (light mid stone)
PILAST = "#d4ccb6"   # engaged pilasters framing the mouth (light, between wall + tower)
ARCH   = "#928a78"   # carriageway voussoir / vault -- DEEP warm stone, the vault reads recessed
ARCHK  = "#a59c87"   # vault corbel highlight course (a touch lighter than ARCH for stepped read)
KEY    = "#efe8d2"   # chiseled keystone + finials (brightest dressed stone)
GLASS  = "#5fa6bd"   # gallery glass-pane window band (deep teal -- glazing, NOT pale stone)
GLASSL = "#bfe9f2"   # glass mullion-lit highlight panes (icy, the night-glow read)
SLATE  = "#3c3744"   # peaked hip roofs (darkest slate -- strong contrast vs pale towers)
RIDGE  = "#534e5b"   # roof ridge / upper courses (slightly lighter slate)
TIMBER = "#7a5c3a"   # lamp-post + banner-post + wall-posts (warm timber)
BANNER = "#a83a31"   # heraldic banner cloth (deep red -- the one saturated accent)
BANNERD= "#7e2a23"   # banner shadow fold (darker red -- gives the cloth a 2-tone drape)
SILL   = "#b0a896"   # gallery slab floor / sills + lancet-window stone frames (mid-light)

# geometry anchors
TL = 0      # left tower x0..5  (6 wide)
TR = 19     # right tower x19..24 (6 wide)
CW0 = 6     # carriageway opening x6..18 -> 13 span... use 7..17 = 11 clear (parametric default)
ROOF_Y = 21 # nominal crown reference

# =====================================================================================
# 1) THREE-STEP MONUMENTAL DAIS (Roman ziggurat plinth: 25x15 -> 23x13 -> 21x11)
#    raised ~1.5 above the avenue; each step edged as a moulded riser.
# =====================================================================================
S.box(0, 0, 0, 25, 15, 1, PLINTH)                 # bottom step 25x15
S.box(1, 1, 1, 23, 13, 1, PMOULD)                 # second step 23x13 (moulded riser)
S.box(2, 2, 2, 21, 11, 1, PLINTH)                 # top step 21x11 (towers + gate seat on this)
# moulded riser lip along the front (z=14 face) reading as a stair edging
S.box(2, 13, 1, 21, 1, 1, PMOULD)

# the avenue ramps onto the dais through the central mouth (paved threshold)
S.box(7, 12, 3, 11, 3, 1, "#6f5d3e")              # warm paved carriageway floor (z12..15 front apron)

# =====================================================================================
# 2) TWIN GATE-TOWERS  (x0..5 and x19..24, depth z2..13 = 11 deep, double-chamfered base)
#    raised on the top dais step (y=3). Base steps inward twice -> octagonal-ish heavy foot.
# =====================================================================================
def tower(tx, east_face=False):
    # double-chamfered battered base (two inward steps, capped mid-stone)
    S.box(tx,   2, 3, 6, 11, 1, CHAMF)            # base course (full 6x11)
    S.box(tx+1, 3, 3.5, 4, 9, 1, PMOULD)          # base torus moulding (warm mid -> reads off CHAMF)
    S.box(tx+1, 3, 4, 4, 9,  1, CHAMF)            # 1st chamfer step in
    # main shaft -- LIGHT dressed stone, stands proud, seam courses for masonry read
    S.box(tx+1, 3, 5, 4, 9, 9, TOWER, seam=True)  # shaft y5..14 (tall)
    # --- string-course belt midway up the shaft (breaks the tall flat face, casts a line) ---
    S.box(tx+0.6, 2.6, 9, 4.8, 9.8, 0.5, PMOULD)  # proud belt course at y9 (warm, reads as a seam shadow)
    # --- recessed LANCET WINDOWS on the near (south, z=13) face: dark reveal + lit pane + apex ---
    #     three tall lights per face (spec: 2-4), so the tower 'glows'. Placed proud of z=13 so visible.
    for wx in (tx+1, tx+2.4, tx+3.8):             # 3 lancets across the 4-wide near face
        S.box(wx, 12.6, 6, 0.8, 0.7, 4, WALL)     # deep dark reveal/jamb (recessed read)
        S.box(wx+0.1, 12.8, 6.3, 0.6, 0.6, 3, GLASS)   # tall glazed light
        S.box(wx+0.1, 12.8, 9.3, 0.6, 0.6, 0.5, SILL)  # pointed lancet apex (stone)
        S.box(wx-0.05, 12.7, 5.7, 0.8, 0.6, 0.4, SILL) # window sill ledge
    # --- lancet on the right tower's east (x=24) face too, since that face is viewer-visible ---
    if east_face:
        for wy in (6.5, 10.5):
            S.box(tx+5.6, 4, wy, 0.6, 1.2, 2.6, WALL)     # dark reveal on east face
            S.box(tx+5.75, 4.3, wy+0.3, 0.4, 0.6, 1.8, GLASS)  # glazed light
    # capital / cornice band before the crown (two-step: cyma + oversail -> richer cornice)
    S.box(tx+0.5, 2.5, 13.5, 5, 10, 0.5, PMOULD)  # cyma moulding under the cornice (warm line)
    S.box(tx,   2, 14, 6, 11, 1, CHAMF)           # cornice oversail (1 proud all round)

tower(TL)
tower(TR, east_face=True)

# engaged pilasters framing the carriageway mouth (triumphal-arch read), front face z=12
# now with a proper BASE plinth + CAPITAL so they read as columns, not flat strips.
def pilaster(px):
    S.box(px, 10, 3, 1, 2, 1, CHAMF)              # base plinth (mid stone)
    S.box(px, 10, 4, 1, 2, 8, PILAST, seam=True)  # fluted shaft (light)
    S.box(px-0.2, 9.8, 12, 1.4, 2.4, 1, CHAMF)    # capital oversail (proud, casts a shadow line)
    S.box(px, 10, 13, 1, 2, 0.5, KEY)             # bright abacus crown
pilaster(6)                                       # left pilaster (inner edge of L tower)
pilaster(18)                                      # right pilaster (inner edge of R tower)

# =====================================================================================
# 3) CARRIAGEWAY WALLS + POINTED VAULT  (parametric span: opening x7..17 = 11 clear)
#    deep ceremonial tunnel z2..12; pointed corbel-stair voussoir with chiseled keystone.
# =====================================================================================
# inner carriageway side-walls (the dark wall the towers pop against), full tunnel depth
S.box(6,  2, 3, 1, 11, 7, WALL, seam=True)        # left tunnel wall (under the L tower inner face)
S.box(18, 2, 3, 1, 11, 7, WALL, seam=True)        # right tunnel wall
# BLIND-ARCADE relief on the tunnel walls: a string-course band + a rhythm of pilaster bosses
# (proud chiseled blocks) between blind-arch bays -> the wall reads carved, not a flat slab.
S.box(6,  2, 6, 1, 11, 1, ARCH)                   # left arcade string-course
S.box(18, 2, 6, 1, 11, 1, ARCH)                   # right arcade string-course
for bz in (3.0, 6.5, 10.0):                       # blind-arch pilaster bosses down each wall
    S.box(6.0,  bz, 4, 1, 0.9, 5, ARCHK)          # left boss (proud, lighter -> catches light)
    S.box(18.0, bz, 4, 1, 0.9, 5, ARCHK)          # right boss
# DETAIL relief panel + banner-niche midway down each carriageway wall (spec: wall relief)
S.box(6.0,  7.2, 7.5, 1, 1.6, 2.5, KEY)           # left chiseled relief panel (bright dressed stone)
S.box(18.0, 7.2, 7.5, 1, 1.6, 2.5, KEY)           # right relief panel

# pointed barrel vault over the 11-wide opening (front rib, z=12, springers->corbels->keystone)
# voussoirs alternate ARCH / ARCHK course-to-course so each corbel step reads as a distinct stone.
S.box(7,  11, 9,  1, 2, 1, ARCH)                  # left springer
S.box(17, 11, 9,  1, 2, 1, ARCH)                  # right springer
S.box(8,  11, 10, 1, 2, 1, ARCHK)
S.box(16, 11, 10, 1, 2, 1, ARCHK)
S.box(9,  11, 11, 1, 2, 1, ARCH)
S.box(15, 11, 11, 1, 2, 1, ARCH)
S.box(10, 11, 12, 1, 2, 1, ARCHK)
S.box(14, 11, 12, 1, 2, 1, ARCHK)
S.box(11, 11, 13, 1, 2, 1, ARCH)
S.box(13, 11, 13, 1, 2, 1, ARCH)
S.box(12, 11, 14, 1, 2, 1, KEY)                   # pointed chiseled keystone at the crown
# vault haunch fill above tunnel back so it reads solid behind (closes the wall plane).
# Use SLATE (dark) so the deep tunnel interior reads as a shadowed mouth behind the pale rib.
S.box(7, 2, 9, 11, 2, 5, SLATE)                   # spandrel/tunnel-back mass (dark, deep-mouth read)

# =====================================================================================
# 4) GLASS-GALLERIED LIT UPPER STOREY  (bridges the towers over the carriageway)
#    walled chamber x6..18 z4..11, glass-pane window band on the road face, peaked roof.
# =====================================================================================
S.box(6, 4, 15, 13, 7, 1, SILL)                   # gallery slab floor (spans tower-to-tower)
S.box(6, 4, 15.6, 13, 7, 0.4, CHAMF)              # floor cornice lip (proud, casts a base line)
S.box(6, 4, 16, 13, 7, 3, WALL, seam=True)        # gallery walls y16..18
# continuous SILL course + lintel framing the glazed band (so the glass reads as a real window run)
S.box(6.5, 9.8, 16, 12, 1, 0.5, SILL)            # window sill ledge under the glazing
S.box(6.5, 9.8, 18.5, 12, 1, 0.5, SILL)          # window lintel over the glazing
# glass-pane window band on the front (road-facing) long side, in bays between mullions.
# alternate deep-teal panes with bright LIT panes -> the 'manned room glowing at night' read.
bay_lit = True
for bx in (7, 8, 10, 11, 13, 14, 16, 17):
    S.box(bx, 10, 16.5, 1, 1, 2, GLASSL if bay_lit else GLASS)   # glazed bay (lit / dark alternation)
    bay_lit = not bay_lit
# mullion piers breaking the glass band (colonnade read) -> at every bay division
for mx in (6.5, 9, 12, 15, 17.5):
    S.box(mx, 9.9, 16, 0.9, 1.1, 3, PILAST)       # slender stone mullion (light, proud of glass)
# gallery peaked ridge roof (its own pitched roof between the towers) + eaves overhang.
# Kept BELOW the tower finials (y23) so the towers stay the hero mass: crest at y22.
S.box(5.6, 3.6, 19, 13.8, 7.8, 1, SLATE)          # eaves course (proud overhang -> shadow line)
S.box(6, 4, 20, 13, 7, 1, SLATE)
S.box(7, 5, 21, 11, 5, 1, RIDGE)                  # mid pitch (lighter slate -> stepped read)
S.box(9, 6, 22, 7, 3, 1, SLATE)                   # upper pitch
S.box(10, 7, 22, 5, 1, 1, KEY)                    # ridge crest (y22, under the tower peaks)

# =====================================================================================
# 5) TOWER CROWNS: machicolation ring -> crenellated parapet -> peaked finialed roof
# =====================================================================================
def crown(tx):
    # cantilevered MACHICOLATION: a dark corbel shadow course UNDER a proud light slab band,
    # so the overhang reads as a true cantilever (not just a wider block).
    S.box(tx-0.3, 1.7, 15, 6.6, 11.6, 0.5, SLATE) # corbel shadow course (dark, recessed read)
    S.box(tx-0.5, 1.5, 15.5, 7, 12, 0.8, CHAMF)   # proud machicolation slab band (light, cantilevered)
    # crenellated parapet wall -- parapet ring sits a touch DARKER (PMOULD) so the pale merlons pop.
    S.box(tx, 2, 16, 6, 11, 1, PMOULD)            # parapet base ring (mid -> merlons read against it)
    for mx in range(0, 6, 2):                     # front + back merlons (alternating block/gap)
        S.box(tx+mx, 12, 17, 1, 1, 1, TOWER)      # near (viewer-facing) merlon, z=12
        S.box(tx+mx, 2, 17, 1, 1, 1, TOWER)       # far merlon, z=2
    for mz in (2, 4, 6, 8, 10, 12):
        S.box(tx, mz, 17, 1, 1, 1, TOWER)         # left side merlons
        S.box(tx+5, mz, 17, 1, 1, 1, TOWER)       # right side merlons
    # steep peaked hip roof stepping inward to a finial (alternating SLATE/RIDGE for stepped read)
    S.box(tx-0.3, 1.7, 18, 6.6, 11.6, 1, SLATE)   # roof eaves (proud overhang -> shadow line)
    S.box(tx+1, 3, 19, 4, 9, 1, RIDGE)
    S.box(tx+1, 4, 20, 4, 7, 1, SLATE)
    S.box(tx+2, 5, 21, 2, 5, 1, RIDGE)
    S.box(tx+2, 6, 22, 2, 3, 1, SLATE)
    S.box(tx+2.5, 7, 23, 1, 1, 1, KEY)            # chiseled finial block

crown(TL)
crown(TR)

# banner-posts on each tower's NEAR (viewer-facing, z=12) front merlon, cloth draped toward the
# avenue so the heraldry actually faces out. Two-tone cloth (lit face + shadow fold) for a real drape.
for tx in (TL, TR):
    S.box(tx+2, 12, 18, 1, 1, 3, TIMBER)          # banner-post on the near merlon (3 tall)
    S.box(tx+2, 12.9, 19, 1, 0.5, 2.4, BANNER)    # banner cloth facing the avenue (near face)
    S.box(tx+2, 13.4, 19, 1, 0.2, 2.4, BANNERD)   # shadowed trailing fold edge (2-tone drape)

# =====================================================================================
# 6) FREE-STANDING FLANKING LAMP-POSTS  (sibling wnl_lamp_post) on the dais front corners
#    Now a fuller lantern: stone footing -> tapered standard -> bracket -> glass head + finial.
# =====================================================================================
for lx in (2.5, 21.5):
    S.box(lx-0.2, 12.8, 1, 1.4, 1.4, 1, CHAMF)    # stepped stone footing/plinth on the dais
    S.box(lx, 13.0, 2, 1, 1, 5, TIMBER)           # lamp standard (timber)
    S.box(lx-0.25, 12.75, 7, 1.5, 1.5, 0.6, CHAMF)# lamp head bracket / collar
    S.box(lx-0.1, 12.9, 7.6, 1.2, 1.2, 1.2, GLASSL)  # glazed lantern head (lit)
    S.box(lx+0.1, 13.1, 8.8, 0.8, 0.8, 0.5, SLATE)   # lantern roof cap

# =====================================================================================
# ACCENTS: soffit tunnel lanterns, gallery glow, crenel + lamp-post lights, finials
# =====================================================================================
# pointed-vault soffit lantern row -- one per ~3 blocks of the 11-deep tunnel (z front->back)
for lz in (3.0, 6.0, 9.0, 11.5):
    S.accent(12, lz, 8.3, "glow", r=2.6)          # hanging soffit lanterns down the carriageway
# pilaster-mouth lanterns flanking the opening (on the near pilaster capitals)
S.accent(6.5, 11.6, 12.4, "glow", r=2.8)
S.accent(18.5, 11.6, 12.4, "glow", r=2.8)
# lancet-window glow on both tower near faces (the towers reading lit at night)
for tx in (TL, TR):
    for wx in (tx+1.3, tx+2.7, tx+4.1):
        S.accent(wx, 13.0, 7.6, "glow", "#bfe9f2", r=1.7)
# right-tower east-face lancets glowing too
S.accent(24.4, 4.6, 7.5, "glow", "#bfe9f2", r=1.6)
S.accent(24.4, 4.6, 11.5, "glow", "#bfe9f2", r=1.6)
# gallery window-band glow (the manned room reading at night), centred on the lit bays
S.accent(12, 10.6, 17.6, "glow", "#eafff8", r=3.4)
# lanterns marching along the NEAR (viewer-facing, z=12) crenellation
S.accent(1.0, 12.0, 17.6, "glow", r=2.2)
S.accent(5.0, 12.0, 17.6, "glow", r=2.2)
S.accent(20.0, 12.0, 17.6, "glow", r=2.2)
S.accent(24.0, 12.0, 17.6, "glow", r=2.2)
# free-standing flanking lamp-post heads (glazed head + crown glow)
S.accent(3.0, 13.5, 8.2, "glow", "#ffe6a8", r=2.8)
S.accent(22.0, 13.5, 8.2, "glow", "#ffe6a8", r=2.8)
# tower finials + gallery ridge crest crowned
S.accent(3.0, 7.5, 23.4, "finial")
S.accent(22.0, 7.5, 23.4, "finial")
S.accent(12.0, 7.5, 22.6, "glow", "#eafff8", r=2.2)

# =====================================================================================
# CALLOUT LABELS
# =====================================================================================
S.label(3, 7, 23, "double-chamfered twin gate-towers (peaked finialed roofs)")
S.label(3, 13, 8, "tall lancet windows — the towers glow at night")
S.label(12, 11, 14, "pointed corbel-voussoir vault — chiseled keystone")
S.label(12, 10, 17, "glass-galleried lit chamber-over-the-gate")
S.label(22, 12, 18, "cantilevered machicolation + banner-flanked crenel")
S.label(6, 11, 12, "pilasters w/ base + capital frame the mouth")
S.label(21.5, 13, 8, "free-standing flanking lamp-posts")
S.label(2, 13, 1, "3-step monumental Roman dais (25→23→21)")

out = S.svg(title="Gatehouse H6 (Great Road) — monumental ceremonial twin-tower city-gate on a stepped dais",
            size_label="25×15 footprint · h21 · carriageway 11 clear (parametric ≥ road width)",
            pad=20, label_w=258)
open("detail_svg/gatehouse.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/gatehouse.svg | bytes", len(out.encode()))
