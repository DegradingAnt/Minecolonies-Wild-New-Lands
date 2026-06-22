"""Cairn R5 (Great Road) detail render -> detail_svg/cairn.svg.
The top-tier wnl_cairn: a ~13-tall hand-stacked-at-heart MONUMENT that grows its own civic
plinth only at the crown of the ladder. A grand 2-step plinth (7x7 -> 5x5) carries a SUSTAINED
3x3 dressed body (held to y7, mass not a needle) with a recessed engraved PLAQUE NICHE turned to
the road, a 4-lantern corner-post crown, flanking (unlit) gateway posts at the FRONT foot, then
the signature wonky OFFSET-stacked capstone cluster crowned by a single nested cap lantern.

Per deco_catalog_v2.json id 'cairn' / Great Road tier (height 13, footprint 7x7->5x5->3x3).
Originality: deliberate per-course hashed-offset stacking + sustained-mass-then-wonky-crown
profile (NOT a fat tower, NOT a needle finial). Form/scale studied for technique only from the
universal drystone trail-cairn folk form + Roman milestone / medieval wayside-shrine tradition
+ structurize big-well stepped-plinth massing -- credited in CREDITS.md, no assets/NBT copied.
The per-course wonk here is drawn as a fixed representative lean (the data builder hashes it live).

ISO note: south (max-z) + east (max-x) faces are the visible ones, so the ROAD-FACING front
(niche + flanking gateway posts) is built on the high-z front face, where the viewer reads it."""
from iso_render import Iso

S = Iso(U=17)

# palette (literal) -- a deliberately WIDE-CONTRAST ladder so every element reads as its own
# material: a deep plinth -> a near-white body that POPS -> a mid dressed cap -> a dark slate
# crown accent -> a true chiseled accent for corners/plaque -> a warm timber offering note.
PBASE = "#6f6a60"   # plinth base course      (DEEP dressed stone -> the pale body pops hard above)
PSTEP = "#827d72"   # plinth 2nd step         (clearly lighter than base, reads the step face)
STAIR = "#5f5a51"   # stepped-foot stairs      (DARKEST -> reads as the corbel skirt shadow line)
TRIM  = "#b9b3a5"   # smooth-stone-slab plinth-top trim band (a pale lip capping each plinth tier)
BODY  = "#e7e2d6"   # sustained 3x3 dressed body (near-white polished stone -- highest contrast)
BAND  = "#c9c3b4"   # polished-andesite banding course inside the body (a mid seam vs the white)
DRESS = "#b3ac9d"   # capstone-cluster dressed stone (mid band, clearly below the pale body)
ACCNT = "#8f7f63"   # chiseled accent: plinth corners + gateway posts (warm dressed-stone tone)
NICHE = "#403c34"   # recessed plaque-niche back (very dark recess so the niche reads carved-in)
PLAQ  = "#cfc8b6"   # engraved plaque panel inside the niche (bright -> the inscription reads)
POST  = "#9a9384"   # corner wall-posts (the lit-crown necks) -- between body-pale and dress
LEDGE = "#7a5c3a"   # warm timber offering-ledge slab (the one warm note for contrast)
CAPAC = "#403d47"   # slate trim on the wonky cap cluster (dark accent crowning the pale stack)
CAPLT = "#5b5763"   # lighter slate (alternating cap so the offset stones separate by tone)
LANT  = "#ffd47a"   # lantern glow

# ---------------------------------------------------------------------------
# GRAND 2-STEP PLINTH  (7x7 -> 5x5).  Stepped foot faked with an outward stair skirt;
# chiseled corner accents + a pale smooth-slab trim lip cap each tier so the steps READ.
# grid: plinth occupies x0..7, z0..7.  Visible front = high-z (south) + high-x (east) faces.
# ---------------------------------------------------------------------------
# Course 0: 7x7 base plinth, DEEP dressed stone, with a stepped-stair foot skirt all round.
S.box(0,0,0, 7,7,1, PBASE, seam=True)                 # solid 7x7 footing
# stepped-stair foot skirt (the corbel; a 1-tall dressed ring sitting just outside the body edge)
S.box(0,0,0, 7,1,1, STAIR)                            # back (z=0) skirt  -- darkest
S.box(0,6,0, 7,1,1, STAIR)                            # FRONT (z=6) stair tread band  -- the read edge
S.box(0,0,0, 1,7,1, STAIR)                            # west skirt
S.box(6,0,0, 1,7,1, STAIR)                            # east skirt
# chiseled CORNER accents on the base (per spec: corners chiseled_stone_bricks)
for (cx,cz) in [(0,0),(6,0),(0,6),(6,6)]:
    S.box(cx,cz,0, 1,1,1, ACCNT, seam=True)

# Course 1: 7x7 solid plinth body, 1 high, then a pale smooth-slab TRIM lip on the front+side edge.
S.box(0,0,1, 7,7,1, PSTEP, seam=True)
S.box(0,6,2, 7,1,0.35, TRIM)                          # front trim lip (pale lip reads the plinth top)
S.box(6,0,2, 1,7,0.35, TRIM)                          # east trim lip

# Course 2: 5x5 step inset 1 all round, with a stair tread skirt + chiseled corners.
S.box(1,1,2, 5,5,1, PSTEP, seam=True)                 # 5x5 step body
S.box(1,1,2, 5,1,1, STAIR)                            # tread skirt back edge
S.box(1,5,2, 5,1,1, STAIR)                            # tread skirt FRONT edge (read)
S.box(1,1,2, 1,5,1, STAIR)                            # tread skirt west
S.box(5,1,2, 1,5,1, STAIR)                            # tread skirt east
for (cx,cz) in [(1,1),(5,1),(1,5),(5,5)]:
    S.box(cx,cz,2, 1,1,1, ACCNT)                      # chiseled 5x5 corners

# Course 3: 5x5 SOLID course carrying the recessed PLAQUE NICHE on the FRONT (road) face (high-z).
S.box(1,1,3, 5,5,1, PSTEP, seam=True)                 # full 5x5 body
S.box(1,6,4, 5,1,0.35, TRIM)                          # pale trim lip along the 5x5 front top edge
# carve the niche into the FRONT face: a dark recess set into the z=5..6 front row, with a
# bright engraved plaque panel behind it (higher x+z -> paints after the body, so it reads).
S.box(2,5,3, 3,1,1, NICHE)                            # the recess mouth (front row, darkened)
S.box(2,5.55,3, 3,0.45,1, PLAQ)                       # engraved plaque panel set into the recess back
S.box(1,5,3, 1,1,1, ACCNT)                            # chiseled jamb (left of the niche)
S.box(5,5,3, 1,1,1, ACCNT)                            # chiseled jamb (right of the niche)

# ---------------------------------------------------------------------------
# FLANKING GATEWAY POSTS -- at the two FRONT corners of the plinth (z=6), rising clear ABOVE
# the plinth so they read as a gateway you pass through (chiseled, UNLIT waymarker posts).
# ---------------------------------------------------------------------------
S.box(0,6,1, 1,1,4, ACCNT, seam=True)                 # front-west gateway post (y1..5)
S.box(6,6,1, 1,1,4, ACCNT, seam=True)                 # front-east gateway post
S.box(0,6,5, 1,1,0.4, CAPLT)                          # slate cap nub on the west post
S.box(6,6,5, 1,1,0.4, CAPLT)                          # slate cap nub on the east post

# ---------------------------------------------------------------------------
# SUSTAINED 3x3 DRESSED BODY  (y4..y7) -- the monumental mass, held (not a needle).
# 3x3 occupies x2..5, z2..5.  A polished-andesite BAND course breaks the white for richness.
# A subtle representative wonk: one corner block nudged out at y4.
# ---------------------------------------------------------------------------
S.box(2,2,4, 3,3,1, BODY, seam=True)                  # y4 body course begins (steps in from 5x5)
S.box(4,4.4,4, 1,1,1, DRESS, seam=True)               # ONE front-east corner block nudged OUT 0.4 toward the road (hand-stacked wonk, supported, reads on the front face)
S.box(2,5,4, 3,1,1, STAIR)                            # stair tread skirt around the 3x3 step (front, reads)
S.box(2,2,4, 1,3,1, STAIR)                            # tread skirt (west)
S.box(4,2,4, 1,3,1, STAIR)                            # tread skirt (east)

S.box(2,2,5, 3,3,1, BAND, seam=True)                  # y5 ANDESITE BAND (mid seam breaks the white mass)
S.box(2,2,6, 3,3,1, BODY, seam=True)                  # y6 body (mass held -- the monumental fix)
S.box(2,2,7, 3,3,1, BODY, seam=True)                  # y7 body holds ONE more course (true mass above eye-height)

# 4 corner WALL-POST necks rising off the body (y5..y7), each carrying a crown lantern above.
for (px,pz) in [(2,2),(4,2),(2,4),(4,4)]:
    S.box(px,pz,5, 1,1,3, POST, seam=True)            # corner-post neck (y5..8 top)

# warm timber OFFERING LEDGE slab tucked against the front-east post (the one warm contrast note)
S.box(4,5,5, 1,1,0.5, LEDGE)

# ---------------------------------------------------------------------------
# WONKY OFFSET CAPSTONE CLUSTER  (y8..y12) -- the hand-stacked signature scaled up.
# Each cap stone is shifted a little + leans alternately, with ALTERNATING tone (dress vs slate)
# so the offset stones separate clearly; cap lantern sits in the GAP, on a stone top face.
# ---------------------------------------------------------------------------
S.box(2.3,2.3,8, 2,2,1, DRESS, seam=True)             # y8: 2x2 dressed cap, shifted (START of cluster)
S.box(2.0,2.6,9, 2,2,1, CAPLT)                        # y9: 2x2 cluster stone, leaned the other way (lighter slate)
S.box(2.7,2.0,10, 1.6,1.6,1, CAPAC)                   # y10: narrows to a dark slate-trimmed offset cap
S.box(2.4,2.7,11, 1.4,1.4,1, DRESS)                   # y11: dressed stacked cap stone, nested with a gap
S.box(2.7,2.3,12, 1.1,1.1,1, CAPAC)                   # y12: topmost dark offset cap stone (the gap-seat)

# ---------------------------------------------------------------------------
# ACCENTS -- 4-lantern corner crown (on the posts) + 1 nested cap lantern = 5 total.
# Foot gateway posts UNLIT (waymarker, not light-source). Glow sits ABOVE each post's top face.
# ---------------------------------------------------------------------------
for (px,pz) in [(2,2),(4,2),(2,4),(4,4)]:
    S.accent(px+0.5, pz+0.5, 8.2, "glow", LANT, r=2.6)    # 4-lantern corner crown
S.accent(3.3, 3.0, 12.8, "glow", "#eafff8", r=2.9)        # nested CAP lantern in the cluster gap
S.accent(3.3, 3.0, 13.0, "finial")                         # crowning finial nub
S.accent(3.5, 6.2, 3.9, "glow", "#cfe8e2", r=2.1)          # soft fill on the FRONT plaque niche (reads the engraving)

# ---------------------------------------------------------------------------
# CALLOUT LABELS
# ---------------------------------------------------------------------------
S.label(3.5,3.5,11, "wonky offset-stacked capstone cluster + nested cap lantern")
S.label(4,4,7, "sustained 3x3 dressed body — 4-lantern corner-post crown")
S.label(3.5,6,4, "recessed engraved plaque niche (road-facing front)")
S.label(6,6,4, "flanking gateway posts (front corners, unlit)")
S.label(0,6,1, "grand 2-step plinth (7×7 → 5×5), stair-skirt + chiseled corners + trim lip")

out = S.svg(title="Cairn R5 (Great Road) — monumental hand-stacked waymarker: 2-step plinth, sustained 3×3 body, wonky capstone crown",
            size_label="7×7 foot · h13 · 5 lanterns (out-reaches the big-well anchor in presence)",
            label_w=340)
open("detail_svg/cairn.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/cairn.svg | bytes", len(out.encode()))
