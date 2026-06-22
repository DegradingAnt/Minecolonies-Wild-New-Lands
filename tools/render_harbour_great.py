"""Harbour rung 3 (great_harbour, the Highway-long-haul / Great Road tier)
   -> detail_svg/harbour_great.svg.
Per deco_catalog_v2.json id 'harbour' tier 'Highway (long-haul) / Great Road -> great_harbour'
(30x15 kinked main quay + a short RETURN ARM beginning to enclose a basin + 3-4 fingers + a 6x5x8
warehouse + an 8-tall crane + a small SEA-CHAPEL (mariners' wayside shrine, 5x5x9) at the road-gate +
a hung gate banner; envelope ~36x22; height 13).

BRIDGES harbour->grand_port (per escalation_note): adds the FIRST VERTICAL CIVIC MASS (the chapel),
starts ENCLOSING A BASIN with a return arm, DRESSES the plinth into a stepped esplanade, and
introduces the HUNG BANNER -- but holds the true landmark (the lighthouse) back so grand_port stays
a real leap. NEW IDEA this rung: the SEA-CHAPEL (original secular mariners' oratory, apsidal end +
lit votive niche behind iron_bars) + the return-arm basin + the dressed esplanade + the gate banner.

Massing translated course-by-course from the catalog:
  - WATERLINE (Y=-1..-3): dark_prismarine 3 courses wrapping seaward + return-arm faces; sea_lanterns
    flush at ~6-block intervals; a polished_blackstone string-course CAP where the masonry steps up.
  - STEPPED PLINTH / ESPLANADE (Y=-1..+1): a 2-step dressed plinth (stone_brick_stairs over a
    stone_bricks riser over the dark_prismarine face) -- the platform reads BUILT, like an esplanade.
  - DECK (Y=0): polished_andesite + stone_bricks banding, a 2-3-wide chiseled_stone_bricks AVENUE
    continuing the road's paving onto the quay; cut-stone parapet = stone_brick_wall + chiseled piers.
  - SEA-CHAPEL (5x5x9, at the landward road-gate): lime-washed mariners' oratory -- stone_bricks
    walls + cut_sandstone corner quoins, a round-arched doorway (stairs voussoirs + chiseled keystone),
    an APSIDAL (rounded) seaward end stepped back 1/course in a 3-block half-ring softened with stairs,
    a steep spruce_stairs gable + a tiny spirelet, and ONE lit VOTIVE NICHE (lantern behind iron_bars).
    ORIGINAL, fully secular -- NO altar/idol/cross.
  - WAREHOUSE (6x5x8): stone_bricks plinth + spruce frame, spruce_stairs hip roof, a gable HOIST BEAM
    (stripped_spruce_log) with chain + lantern, barrel/hay_block stacks.
  - GRAND CRANE (8-tall A-frame, jib 5 out) + a winch DRUM + a stone_bricks counterweight cradle.
  - FINGERS (x3-4, 2-wide, out 7-9): plank decks on stone-collared stilted piles, lanterns + bollards.
  - GATE: lantern-topped twin-post threshold + a way_sign + ONE single hung white_banner over the lintel.

Original WNL geometry. Inspiration (FORM/SCALE/TECHNIQUE only, credited in CREDITS.md): Towns&Towers /
Tidal Towns docks; MineColonies/Byzantine monumental dressed-stone civic scale (stepped plinths, hung
banners); the medieval mariners' WAYSIDE SHRINE for the sea-chapel FORM (apsidal end, votive niche) --
rebuilt entirely original, secular, no real chapel reproduced; the Roman harbour MOLE for the
esplanade. The kinked dog-leg / return-arm BASIN plan + the dark-prismarine waterline 'tell' are WNL
signatures. Same wnl_harbour data builder as render_harbour.py (the grand_port top rung); placer hashes
chapel spirelet height / apse depth / return-arm length / finger count / banner pattern / lantern
interval live.
ISO: viewer-visible faces are SOUTH (max-z FRONT) + EAST (max-x) + TOP -> the chapel doorway + the
votive niche + the fingers + the crane jib + the gate banner all turned to the high-z FRONT so they read.
"""
from iso_render import Iso

S = Iso(U=9)

# ---- palette (literal hex ~ vanilla blocks) -- WIDE-CONTRAST ladder, each material reads apart ----
WATER = "#356f93"   # sea / basin water (cool blue -- pushes the stone off it)
WET   = "#14302f"   # dark_prismarine WATERLINE 'tell' (near-black wet band -- the signature)
WETST = "#27514e"   # dark_prismarine_stairs chamfer (lifted off WET so the chamfered step reads)
DECK  = "#8f9499"   # stone_bricks deck -- cool grey-blue working stone
ANDE  = "#bdc0c2"   # polished_andesite banding (pale cool)
AVEN  = "#d6cdb3"   # chiseled_stone_bricks formal AVENUE + pier-caps (warm bone -> the civic road reads)
COBB  = "#6c6f72"   # cobblestone worn scatter
FOUND = "#5a5d60"   # cobblestone foundation mass (darkest stone)
MOSS  = "#5f7050"   # mossy_cobblestone fleck
PLINTH= "#a39c8a"   # stone_brick_stairs dressed plinth / esplanade riser (warm mid -> the step reads)
TRIM  = "#cdc6b4"   # smooth plinth tread lip (pale -> reads the esplanade step)
BLACK = "#322e3a"   # polished_blackstone string-course (the dark civic dressed band)
WALL  = "#9a948a"   # stone_brick_wall parapet
SAND  = "#dcc585"   # cut_sandstone chapel quoins (warm pale accent, distinct from bone avenue)
CHAP  = "#c2b694"   # chapel nave walls (warm dressed stone -> pops off the cool quay)
NICHE = "#2a2622"   # votive-niche recess / doorway recess (dark -> reads carved-in)
GRILL = "#6e6a62"   # iron_bars grille over the votive niche
TIMB  = "#86603a"   # spruce_planks / frames (warm timber)
TIMBD = "#5a4026"   # spruce_log posts / spruce_fence piles (darker -> the frame reads)
STRIP = "#a98455"   # stripped_spruce_log crane jib + hoist beam (lighter timber)
ROOF  = "#3f2f1c"   # spruce_stairs roofs (dark warm -> roofs sit DOWN, silhouette sharp)
HEEL  = "#7d7468"   # stone_bricks crane counterweight cradle
HAY   = "#caa83e"   # hay_block cargo (warm gold)
BARR  = "#7a5c3a"   # barrel cargo
BANNER= "#e4ddcd"   # hung white_banner (lightened -> reads as cloth, not stone)
DIRT  = "#5d4f3a"   # coarse_dirt landward keying
LANT  = "#ffd47a"   # lantern glow
SEAL  = "#cfeede"   # sea_lantern glow (flush in the waterline + at ~6 intervals)

# ============================================================================
# 0) WATER FIELD (drawn first / back)
# ============================================================================
S.box(0, 0, 0, 38, 24, 1, WATER)

# ============================================================================
# 1) KINKED MAIN QUAY (30x15) + a short RETURN ARM beginning to enclose a basin
#    main arm along the back (x 3..27, z 3..11), dog-leg ~2/3 along (front edge jogs forward),
#    return arm down the right (x 24..30, z 11..19) -> starts to wrap a 3-sided basin.
# ============================================================================
# -- waterline 'tell': 3 dark_prismarine courses on seaward + return-arm faces --
def wet3(x, z, dx, dz):
    S.box(x, z, 0, dx, dz, 1, WET)               # wet course 1 (Y=-1)
    S.box(x, z, 1, dx, dz, 1, WET)               # wet course 2 (Y=-2)
    S.box(x, z, 2, dx, dz, 1, WETST)             # wet course 3 / chamfer (Y=-3, lifted -> step reads)
wet3(3, 11, 21, 1)                               # main-arm seaward wet face
wet3(24, 11, 1, 8)                               # return-arm inner wet face (basin side)
wet3(29, 11, 1, 8)                               # return-arm outer (open-sea) wet face
wet3(3, 3, 1, 8)                                 # west end wet face

# -- foundation mass following the kinked + return-arm plan --
S.box(3, 3, 2, 24, 8, 1, FOUND)                  # main-arm foundation
S.box(24, 11, 2, 6, 8, 1, FOUND)                 # return-arm foundation
S.box(8, 11, 2, 2, 1, 1, MOSS)                   # mossy fleck at the waterline
S.box(18, 11, 2, 2, 1, 1, MOSS)
S.box(1, 4, 2, 2, 4, 1, DIRT)                    # landward keying (coarse_dirt back-west)

# -- STEPPED PLINTH / ESPLANADE on the seaward + return-arm edge: stairs over a riser over the wet
#    face (a 2-step dressed edge -> reads as a built Roman mole, not one raw drop) --
S.box(3, 10, 2, 21, 1, 1, PLINTH)                # esplanade riser (main arm)
S.box(3, 10, 3, 21, 1, 0.4, TRIM)               # esplanade tread lip (reads the step)
S.box(24, 11, 2, 1, 8, 1, PLINTH)               # esplanade riser (return arm)
# -- polished_blackstone string-course CAP where the masonry steps up (the civic dark band) --
S.box(3, 11, 3, 21, 1, 1, BLACK)                 # seaward string-course
S.box(29, 11, 3, 1, 8, 1, BLACK)                 # return-arm string-course

# ============================================================================
# 2) DECK COURSE (Y=0) -- polished_andesite + stone_bricks banding + a chiseled AVENUE + parapet
# ============================================================================
S.box(3, 3, 3, 24, 8, 1, DECK)                   # main-arm deck base
S.box(24, 11, 3, 6, 8, 1, DECK)                  # return-arm deck base
# polished_andesite banding (formal, ~15%)
S.box(5, 4, 4, 4, 1, 1, ANDE)
S.box(14, 8, 4, 4, 1, 1, ANDE)
S.box(20, 5, 4, 3, 1, 1, ANDE)
S.box(26, 14, 4, 3, 1, 1, ANDE)
# worn cobble scatter
S.box(10, 5, 4, 2, 2, 1, COBB)
S.box(22, 8, 4, 2, 2, 1, COBB)
# -- chiseled_stone_bricks formal AVENUE (2-3 wide) continuing the road's paving onto the quay --
S.box(4, 6, 4, 20, 2, 1, AVEN)                   # main-arm avenue spine
S.box(25, 8, 4, 2, 7, 1, AVEN)                   # avenue turns down the return arm
# -- cut-stone PARAPET (stone_brick_wall) + chiseled piers every 5 along the seaward edge --
S.box(3, 11, 4, 21, 1, 1, WALL)                  # seaward parapet
S.box(29, 11, 4, 1, 8, 1, WALL)                  # return-arm parapet
for px in range(6, 26, 5):
    S.box(px, 11, 5, 1, 1, 1, AVEN)              # chiseled pier-caps standing proud of the wall

# ============================================================================
# 3) BOLLARD ROW -- cobble column + wall cap, every ~4 along the seaward kerb
# ============================================================================
def bollard(bx, bz):
    S.box(bx, bz, 4, 1, 1, 1, COBB)
    S.box(bx, bz, 5, 1, 1, 1, WALL)
bollard(7, 11); bollard(15, 11); bollard(21, 11); bollard(29, 14)

# ============================================================================
# 4) SEA-CHAPEL (5x5x9) -- the FIRST VERTICAL CIVIC MASS, at the landward road-gate
#    secular mariners' oratory: nave + cut_sandstone quoins + round-arched door + apsidal seaward
#    end + spruce_stairs gable + spirelet + ONE lit VOTIVE NICHE (lantern behind iron_bars).
#    Reserved 5x5 pad on the main arm just inside the gate (x 4..9, z 3..8).
# ============================================================================
CH_X, CH_Z = 4, 3
S.box(CH_X, CH_Z, 3, 5, 4, 1, BLACK)             # dark socle course (lifts the oratory off the deck)
S.box(CH_X, CH_Z, 4, 5, 4, 4, CHAP, seam=True)   # nave body (warm dressed -> pops off the cool quay)
for qx, qz in [(CH_X, CH_Z), (CH_X+4, CH_Z), (CH_X, CH_Z+3), (CH_X+4, CH_Z+3)]:
    S.box(qx, qz, 4, 1, 1, 4, SAND)              # warm cut_sandstone quoin pilasters at each corner
# round-arched DOORWAY facing the road (high-z FRONT face so the viewer reads it): recess + keystone
S.box(CH_X+2, CH_Z+3, 4, 1, 1, 2, NICHE)         # dark doorway recess (front)
S.box(CH_X+2, CH_Z+3, 6, 1, 1, 1, AVEN)          # chiseled keystone over the arch
# APSIDAL (rounded) SEAWARD end -- stepped-back half-ring softened with stairs, faces the basin/front
S.box(CH_X+1, CH_Z+4, 4, 3, 1, 3, CHAP)          # apse first step (proud of the nave, toward the basin)
S.box(CH_X+1, CH_Z+5, 4, 3, 1, 2, SAND)          # apse second step (rounds the end)
# lit VOTIVE NICHE in the apse seaward wall (lantern behind an iron_bars grille -- a candle for sailors)
S.box(CH_X+2, CH_Z+5, 4, 1, 1, 1, NICHE)         # niche recess (dark)
S.box(CH_X+2, CH_Z+6, 4, 1, 0.3, 1, GRILL)       # iron_bars grille over the niche (proud, abuts the wall)
# steep spruce_stairs GABLE + a tiny spirelet
S.box(CH_X-0.3, CH_Z-0.3, 8, 5.6, 4.6, 1, ROOF)  # proud gable eave (overhang -> shadow line)
S.box(CH_X+1, CH_Z+1, 9, 3, 2, 1, ROOF)          # ridge
S.box(CH_X+2, CH_Z+1, 10, 1, 1, 2, SAND)         # spirelet (warm, the chapel's vertical accent)

# ============================================================================
# 5) WAREHOUSE (6x5x8) -- landward pad mid-quay (x 12..18, z 3..8)
# ============================================================================
W_X, W_Z = 12, 3
S.box(W_X, W_Z, 3, 6, 5, 1, COBB)                # stone_bricks plinth course
S.box(W_X, W_Z, 4, 6, 5, 3, TIMB, seam=True)     # spruce-frame walls
for cx, cz in [(W_X, W_Z), (W_X+5, W_Z), (W_X, W_Z+4), (W_X+5, W_Z+4)]:
    S.box(cx, cz, 4, 0.7, 0.7, 3, TIMBD)         # spruce_log corner-posts (frame, not a dark box)
# loading bay + shutter on the high-z FRONT
S.box(W_X+1, W_Z+4, 4, 3, 1, 1, NICHE)           # wide loading-bay opening (dark, at deck level)
S.box(W_X+4, W_Z+4, 6, 1, 1, 1, NICHE)           # upper shutter recess
# spruce_stairs HIP roof, courses inset + climbing
S.box(W_X-0.3, W_Z-0.3, 7, 6.6, 5.6, 1, ROOF)    # proud eave
S.box(W_X+1, W_Z+1, 8, 4, 3, 1, ROOF)            # mid hip
S.box(W_X+2, W_Z+1, 9, 2, 3, 1, ROOF)            # ridge
# gable HOIST BEAM (stripped_spruce_log) cantilevering over the apron w/ chain + lantern
S.box(W_X+2, W_Z+5, 6, 2, 1, 1, STRIP)           # hoist beam out over the loading apron
S.box(W_X+2, W_Z+6, 6, 1, 1, 1, TIMBD)           # beam tip (the chain falls from here)
# cargo on the apron (abut the warehouse -- grounded)
S.box(W_X+1, W_Z+5, 3, 1, 1, 1, HAY)             # hay_block
S.box(W_X+4, W_Z+5, 3, 1, 1, 2, BARR)            # barrel stack (taller, by the water)

# ============================================================================
# 6) GRAND CRANE (8-tall A-frame, jib 5 out) at the return-arm head -- legs separated across X
#    so the A reads in iso; winch DRUM at the base; stone_bricks counterweight cradle at the heel.
#    Stood at the front-right of the return arm, isolated over the basin water.
# ============================================================================
CR_X, CR_Z = 25, 13
# -- WEST leg rakes UP + EAST; EAST leg rakes UP + WEST; meet at an apex ~8 up (3 courses each) --
S.box(CR_X, CR_Z, 4, 1, 1, 2, TIMBD)             # west leg foot
S.box(CR_X+1, CR_Z, 6, 1, 1, 2, TIMBD)           # west leg mid (steps EAST 1 per 2 of rise)
S.box(CR_X+2, CR_Z, 8, 1, 1, 2, TIMBD)           # west leg upper
S.box(CR_X+5, CR_Z, 4, 1, 1, 2, TIMBD)           # east leg foot
S.box(CR_X+4, CR_Z, 6, 1, 1, 2, TIMBD)           # east leg mid (steps WEST 1 per 2 of rise)
S.box(CR_X+3, CR_Z, 8, 1, 1, 2, TIMBD)           # east leg upper (converges over centre)
S.box(CR_X+2, CR_Z, 10, 2, 1, 1, STRIP)          # apex beam (legs meet; jib pivots here)
# heel COUNTERWEIGHT cradle on the landward side (back-balances the cantilever)
S.box(CR_X+1, CR_Z, 10, 1, 1, 1, HEEL)           # stone_bricks counterweight cradle (the anchor)
# stripped_spruce_log JIB cantilevering FORWARD over the basin (toward viewer, +z, 5 long)
S.box(CR_X+2, CR_Z+1, 10, 1, 5, 1, STRIP)        # jib arm
S.box(CR_X+2, CR_Z+6, 10, 1, 1, 1, TIMBD)        # jib-tip head (chain falls hang here)
S.box(CR_X+2, CR_Z+6, 6, 1, 1, 1, HEEL)          # hanging hook-block (mid-air load, on the chain falls)
# winch DRUM slung between the legs at deck level (stripped-log spool)
S.box(CR_X+2, CR_Z, 4, 2, 1, 1, STRIP)           # winch drum

# ============================================================================
# 7) MOORING FINGERS (x3, 2-wide, out 7-9) reaching into the basin
# ============================================================================
def finger(fx, fz0, length, width=2):
    for k in range(length):
        fz = fz0 + k
        S.box(fx, fz, 0, width, 1, 1, TIMBD)     # spruce piles (grounded down to bed)
    for k in range(0, length, 2):
        S.box(fx, fz0 + k, 0, width, 1, 1, WET)  # dark_prismarine collars at every-other waterline
    S.box(fx, fz0, 1, width, length, 1, TIMB)    # plank deck spanning the piles
    S.box(fx, fz0 + length - 1, 2, 1, 1, 1, TIMBD)  # tip post (carries the hanging lantern)
    S.box(fx, fz0 + 1, 2, 1, 1, 1, COBB)         # a stone bollard along the finger

finger(9, 12, 7)                                 # finger 1
finger(15, 12, 8)                                # finger 2
finger(20, 12, 7)                                # finger 3

# ============================================================================
# 8) GATE -- lantern-topped twin-post threshold at the road->quay end (landward LEFT) + way_sign +
#    ONE single hung white_banner over the lintel (the banner appears great_harbour+).
# ============================================================================
S.box(1, 5, 3, 1, 1, 1, DIRT)                    # road approach landing
S.box(2, 4, 4, 1, 1, 4, TIMBD)                   # west gate post
S.box(2, 7, 4, 1, 1, 4, TIMBD)                   # east gate post
S.box(2, 4, 8, 1, 4, 1, BLACK)                   # gate lintel spanning the posts (way_sign mounts here)
S.box(3, 4, 9, 1, 4, 1, BANNER)                  # ONE hung white_banner over the lintel

# ============================================================================
# 9) ACCENTS -- sea_lanterns flush in the waterline at ~6 intervals + chapel votive + crane +
#    hoist + finger + gate lanterns
# ============================================================================
# sea_lanterns recessed flush in the dark-prismarine waterline (the wet-edge glow at ~6 intervals)
for gx in range(6, 25, 6):
    S.accent(gx, 11.5, 2.4, "glow", SEAL, r=2.0)
S.accent(29.5, 14.5, 2.4, "glow", SEAL, r=2.0)   # return-arm sea_lantern
# chapel VOTIVE NICHE (warm candle behind the iron_bars grille, seaward wall)
S.accent(CH_X + 2.5, CH_Z + 6, 5.0, "glow", LANT, r=1.9)
# warehouse hoist-beam lantern + loading-bay glow
S.accent(W_X + 2.5, W_Z + 6, 6.2, "glow", LANT, r=2.0)
# crane hook-block lantern (chain falls over the basin)
S.accent(CR_X + 2.5, CR_Z + 6.5, 6.4, "glow", LANT, r=2.1)
# finger-tip hanging lanterns
S.accent(9.5, 18.5, 3.2, "glow", LANT, r=1.9)
S.accent(15.5, 19.5, 3.2, "glow", LANT, r=1.9)
S.accent(20.5, 18.5, 3.2, "glow", LANT, r=1.9)
# gate-post lanterns (twin posts)
S.accent(2.5, 4.5, 9.3, "glow", LANT, r=1.9)
S.accent(2.5, 7.5, 9.3, "glow", LANT, r=1.9)

# ============================================================================
# 10) CALLOUT LABELS
# ============================================================================
S.label(CH_X + 2, CH_Z + 2, 10, "SEA-CHAPEL (5x5x9) -- secular mariners' oratory: apsidal end + lit votive niche")
S.label(CR_X + 2.5, CR_Z, 10.5, "8-tall grand crane (return-arm head) -- winch drum + counterweight cradle, jib 5 out")
S.label(W_X + 3, W_Z + 1, 9, "6x5x8 hoist warehouse -- gable hoist beam, barrel + hay_block cargo")
S.label(26, 14, 4, "RETURN ARM begins to enclose a 3-sided basin (the fingers sit inside)")
S.label(2.5, 5, 9, "lantern-topped gate + way_sign + the FIRST hung white_banner")
S.label(3, 10, 3, "dressed STEPPED ESPLANADE (Roman-mole plinth) + polished-blackstone string-course")
S.label(6, 11, 2.4, "sea_lanterns flush in the dark-prismarine waterline (~6 intervals)")

out = S.svg(title="Harbour R3 (great_harbour) -- a harbour town's port: the sea-chapel raises the first vertical civic mass, a return arm starts a basin, a dressed esplanade + hung banner",
            size_label="30x15 kinked quay + return arm + 3 fingers * h13 * ~14 lanterns (bridges harbour -> grand_port; the lighthouse is held back)",
            label_w=384)
open("detail_svg/harbour_great.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/harbour_great.svg | bytes", len(out.encode()))
