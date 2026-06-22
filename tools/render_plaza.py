"""Plaza R5 (Great Road) detail render -> detail_svg/plaza.svg.
A colonnaded civic FORUM: engineered level disc, full peristyle ON the circle, K roofed corner
pavilions, a grand stepped central dais carrying a tall tiered fountain spire (a landmark read
from a distance), radial spokes + lighting.
v2 (author: "could be grander"): 16-column peristyle, taller light-contrast shafts w/ base+capital,
5-step dais, a tall tiered fountain spire, bigger pavilions."""
import math
from iso_render import Iso

S = Iso(U=8)
C = 16.0          # disc centre on a 0..32 grid
R_COL = 13.0      # colonnade radius
NCOL = 16         # full peristyle

# palette -- columns LIGHT vs a darker floor so the colonnade reads
ANDE  = "#83868b"   # polished andesite kerb ring (darker)
FLOOR = "#b4b1aa"   # forum field (mid grey, darker than the pale columns)
SPOKE = "#9aa0a6"   # radial spoke inlay
COL   = "#e4dfd3"   # peristyle shafts (near-white dressed stone -- high contrast)
CAP   = "#b2ac9f"   # column base + capital band
DAIS  = "#b0aa9c"   # stepped dais
WELL  = "#b6b0a3"   # fountain rings
POST  = "#7a5c3a"   # fountain timber posts
SLATE = "#4b4750"   # pavilion + spire hip roofs

def corner(cx, cz): return (cx-0.5, cz-0.5)

# --- engineered level floor: kerb ring + raised forum field + radial spokes ---
S.box(0,0,0, 32,32,1, ANDE)
S.box(2,2,1, 28,28,1, FLOOR)
S.box(15,2,1, 2,28,1, SPOKE)          # N-S spoke
S.box(2,15,1, 28,2,1, SPOKE)          # E-W spoke

# --- full peristyle ON the circle (taller, light shafts w/ base + capital) ---
pav_idx = {2,6,10,14}
cols = []
for i in range(NCOL):
    a = 2*math.pi*i/NCOL
    cx = C + R_COL*math.cos(a); cz = C + R_COL*math.sin(a)
    cols.append((cx,cz))
    if i in pav_idx:
        # GROUNDED pavilion: a 2x2 cluster of piers carries a 4x4 hip roof (no floating roof)
        for ox,oz in [(-1,-1),(0,-1),(-1,0),(0,0)]:
            S.box(cx+ox,cz+oz,1, 1,1,1, CAP)       # base
            S.box(cx+ox,cz+oz,2, 1,1,6, COL)       # pier
            S.box(cx+ox,cz+oz,8, 1,1,1, CAP)       # capital
        S.box(cx-1.5,cz-1.5,9, 4,4,1, SLATE)       # roof eave (rests on the 2x2 cluster)
        S.box(cx-1.0,cz-1.0,10, 3,3,1, SLATE)
        S.box(cx-0.5,cz-0.5,11, 2,2,1, SLATE)      # ridge
    else:
        bx,bz = corner(cx,cz)
        S.box(bx,bz,1, 1,1,1, CAP)                 # base
        S.box(bx,bz,2, 1,1,6, COL)                 # tall shaft (light -> reads)
        S.box(bx,bz,8, 1,1,1, CAP)                 # capital

# --- grand stepped central dais (15->13->11->9->7, five courses) ---
for side,y in [(15,1),(13,2),(11,3),(9,4),(7,5)]:
    h = side/2.0
    S.box(C-h, C-h, y, side, side, 1, DAIS)

# --- tall tiered fountain spire on the dais (the distance landmark) ---
S.box(C-2.5,C-2.5,6, 5,5,2, WELL, seam=True)        # ringed well base
for (px,pz) in [(C-2.2,C-2.2),(C+1.2,C-2.2),(C-2.2,C+1.2),(C+1.2,C+1.2)]:
    S.box(px,pz,6, 1,1,6, POST)                      # 4 corner posts rising
S.box(C-1.5,C-1.5,8, 3,3,2, WELL)                    # tier 1
S.box(C-1.0,C-1.0,10, 2,2,2, WELL)                   # tier 2
S.box(C-1.5,C-1.5,12, 3,3,1, SLATE)                  # pitched cap
S.box(C-0.5,C-0.5,13, 1,1,2, "#cfe8e2")              # crowning lantern spire

# --- accents: pavilion + dais + fountain lights only (de-cluttered: no per-column lanterns) ---
for i,(cx,cz) in enumerate(cols):
    if i in pav_idx: S.accent(cx, cz, 11.8, "glow", r=2.6)   # pavilion light
for (bx,bz) in [(C-5.5,C-5.5),(C+5.5,C-5.5),(C-5.5,C+5.5),(C+5.5,C+5.5)]:
    S.accent(bx,bz,5.0, "glow", r=2.0)               # dais bollards
S.accent(C, C, 15.2, "glow", "#eafff8", r=3.4)       # fountain sea-lantern crown
S.accent(C, C, 15.4, "finial")

# --- callout labels ---
S.label(cols[12][0], cols[12][1], 8, "full peristyle — 16 monumental columns")
S.label(cols[2][0], cols[2][1], 11, "roofed corner pavilions (K widest gaps)")
S.label(C, C, 13, "grand stepped dais + tiered fountain spire")
S.label(23, 4, 1, "radial forum floor — per-arm-gap spokes")

out = S.svg(title="Plaza R5 — grand colonnaded civic forum (peristyle, pavilions, dais + fountain spire)",
            size_label="~37×37 forum precinct · h12 (spire reads from afar)")
open("detail_svg/plaza.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/plaza.svg | bytes", len(out.encode()))
