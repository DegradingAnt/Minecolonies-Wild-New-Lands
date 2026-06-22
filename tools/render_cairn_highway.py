"""Cairn HIGHWAY (R4) -> detail_svg/cairn_highway.svg.
Per deco_catalog_v2.json id 'cairn' tier Highway (footprint 3x3 sustained body on a stepped
5x5->4x4 plinth, height 9): the BIG non-linear jump below the Great Road top -- a stepped
monumental plinth, a SUSTAINED 3x3 cut-stone body (mass held to shoulder height, NOT a taper to a
needle) with a recessed road-facing PLAQUE NICHE, a corner-post parapet carrying 2 flanking
lanterns, then the wonky-stacked 2x2 capstone cluster crowned by a nested lantern (3 lanterns).
Engineered cut-stone artery, still hand-stacked at heart. This is the rung directly under the
Great Road monument (render_cairn.py, h13/5 lanterns) -- same wnl_cairn builder, same identity,
one step less grand. Inspiration (drystone cairn + Roman milestone + wayside-shrine recess +
stepped-plinth massing) credited in CREDITS.md; no assets/NBT copied.
ISO: road-facing FRONT = high-z (south) + high-x (east); niche + parapet read on that front."""
from iso_render import Iso

S = Iso(U=17)

PBASE = "#7a746a"   # 5x5 plinth base (stone_bricks, dressed)
STAIR = "#625d54"   # stepped stair foot skirt (darkest -> the corbel shadow)
TRIM  = "#b3ada0"   # smooth-slab step tread / trim lip
STEP  = "#867f74"   # 4x4 plinth step body
ACCNT = "#8f7f63"   # chiseled_stone_bricks corners (warm dressed accent)
BODY  = "#ddd8cb"   # sustained 3x3 cut-stone body (near-white -> pops above the plinth)
BAND  = "#c4beb0"   # mossy_stone_bricks mid band (breaks the pale mass)
NICHE = "#403c34"   # recessed plaque-niche back (dark recess reads carved-in)
PLAQ  = "#cfc8b6"   # chiseled plaque panel inside the niche
POST  = "#9a9384"   # corner-post parapet necks (stone_brick_wall posts)
DRESS = "#b3ac9d"   # capstone-cluster dressed cut blocks
CAPAC = "#43404a"   # slate-dark cap accent (crowns the pale stack)
LEDGE = "#7a5c3a"   # warm offering note
LANT  = "#ffd47a"   # lantern glow

# Course 0 (y0): 5x5 PLINTH, stone_bricks, stepped stair foot all round, chiseled corners.
S.box(0,0,0, 5,5,1, PBASE, seam=True)
S.box(0,0,0, 5,1,1, STAIR); S.box(0,4,0, 5,1,1, STAIR)     # back + FRONT stair foot
S.box(0,0,0, 1,5,1, STAIR); S.box(4,0,0, 1,5,1, STAIR)     # west + east stair foot
for (cx,cz) in [(0,0),(4,0),(0,4),(4,4)]:
    S.box(cx,cz,0, 1,1,1, ACCNT, seam=True)                # chiseled corners

# Course 1 (y1): 4x4 PLINTH step inset 1, stone_brick_slab tread on the exposed ledge.
S.box(0.5,0.5,1, 4,4,1, STEP, seam=True)
S.box(0.5,4.0,2, 4,0.5,0.3, TRIM)                          # front step tread lip (reads the step)
S.box(4.0,0.5,2, 0.5,4,0.3, TRIM)                          # east step tread lip

# Course 2 (y2): 3x3 SOLID body begins; recessed PLAQUE NICHE on the FRONT (road) face.
S.box(1,1,2, 3,3,1, BODY, seam=True)
S.box(1.5,3,2, 2,1,1, NICHE)                               # niche mouth (front row, darkened)
S.box(1.5,3.55,2, 2,0.4,1, PLAQ)                           # engraved plaque panel in the recess

# Course 3 (y3): 3x3 body continues; ONE perimeter block dropped to a slab/shifted (the wonk).
S.box(1,1,3, 3,3,1, BODY, seam=True)
S.box(3.0,3.4,3, 1,1,0.7, BAND)                            # front-east block nudged out + dropped (hand-stacked lean)

# Course 4 (y4): 3x3 body SUSTAINED (mass held to shoulder); corners begin as wall posts.
S.box(1,1,4, 3,3,1, BAND, seam=True)                       # mossy band course breaks the pale mass

# Course 5 (y5): corner-post parapet -- 4 wall posts ring a slabbed centre; 2 carry lanterns.
for (px,pz) in [(1,1),(3,1),(1,3),(3,3)]:
    S.box(px,pz,5, 1,1,1, POST, seam=True)
S.box(1.7,1.7,5, 1.6,1.6,0.4, TRIM)                        # slabbed parapet centre
S.box(3,3,6, 1,1,0.3, LEDGE)                               # offering ledge on the front-east post

# Course 6 (y6): body steps to a 2x2 dressed cut block (START of the cluster, NOT a 1x1 neck).
S.box(1.4,1.4,6, 2,2,1, DRESS, seam=True)

# Course 7 (y7): deliberately-OFFSET 2x2 capstone cluster (hand-stacked signature scaled down).
S.box(1.1,1.7,7, 2,2,1, CAPAC)

# Course 8 (y8): final wonky cap -- nested offset stones, single lantern seated in the GAP.
S.box(1.7,1.2,8, 1.4,1.4,1, DRESS)

# ACCENTS: 2 parapet flanking lanterns (front posts) + 1 nested cap lantern = 3.
S.accent(1.5, 3.5, 6.15, "glow", LANT, r=2.3)              # front-west parapet lantern
S.accent(3.5, 3.5, 6.15, "glow", LANT, r=2.3)              # front-east parapet lantern
S.accent(2.4, 2.0, 8.9, "glow", "#eafff8", r=2.6)          # nested cap lantern in the cluster gap
S.accent(2.4, 2.0, 9.0, "finial")
S.accent(2.5, 3.6, 2.9, "glow", "#cfe8e2", r=1.9)          # soft fill reading the front plaque niche

S.label(2.3, 2.0, 8.4, "wonky 2x2 capstone cluster + nested cap lantern")
S.label(3, 3, 5.6, "corner-post parapet -- 2 flanking lanterns")
S.label(2.5, 3.5, 3.2, "recessed plaque niche (road-facing front)")
S.label(2, 2, 3.5, "SUSTAINED 3x3 cut-stone body (mass held -- not a needle)")
S.label(0, 4, 1, "stepped 5x5 -> 4x4 plinth, stair foot + chiseled corners")

out = S.svg(title="Cairn R4 (Highway) -- monumental cut-stone artery marker: stepped plinth, sustained 3x3 body, parapet + capstone crown",
            size_label="5x5 foot -> 3x3 body * h9 * 3 lanterns (one step under the Great Road monument)",
            label_w=346)
open("detail_svg/cairn_highway.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/cairn_highway.svg | bytes", len(out.encode()))
