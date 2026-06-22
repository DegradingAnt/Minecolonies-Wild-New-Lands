"""Lamp-post PATH (R2) -> detail_svg/lamp_post_path.svg.
Per deco_catalog_v2.json id 'lamp_post' tier Path (footprint 1x1, height 5): the real second
step -- a SQUARED stripped-oak-log standard (heavier than Trail's thin leaning fence) standing
UPRIGHT and dressed on a stubby cobblestone_wall masonry plinth, capped by an oak_fence finial
carrying a standing lantern. ALWAYS lit on civ placements. No lean -- this is a 'made', upright,
deliberate path fixture, taller (h5) and chunkier than Trail's leaning stub.

Escalation: a true non-linear second step (not a one-block delta): +2 height over Trail, the thin
leaning fence becomes an UPRIGHT 2-log squared standard on a masonry foot, and it is always lit.
Trail/Path/Road now read as three distinct silhouettes: stub -> dressed post -> engineered standard.

Originality/inspiration: medieval wayside lantern-post on a stone foot, technique only; credited in
CREDITS.md, no assets/NBT copied. Same wnl_lamp_post identity whose Great-Road top tier is the
twin-pier light-arch; the data builder hashes decay/light/palette live per post."""
from iso_render import Iso

S = Iso(U=30)

# --- palette (literal) -- a WIDE-CONTRAST ladder: dressed grey masonry foot -> warm squared
#     timber shaft -> warm light; each material reads as itself. Comment each ---
PAD   = "#8a8276"   # cobblestone footing pad (flush ground course)
WALL  = "#9b9488"   # cobblestone_wall plinth (lighter dressed masonry -> reads as the made foot)
WALLD = "#7c7468"   # cobblestone_wall shadowed inner -> reads the wall waist
LOG   = "#b08a4f"   # stripped_oak_log SQUARED post (warm timber, the heavier upright standard)
LOGL  = "#c49a5b"   # stripped_oak_log seam-lit edge (a touch warmer -> reads the log courses)
LOGE  = "#8a6c3c"   # stripped_oak_log end-grain ring at the cap (darker -> reads the cut top)
FENCE = "#a9874f"   # oak_fence finial cap (thinner than the log -> a clear neck under the lamp)
GROUND= "#5d5447"   # the path surface the pad sits flush in (darker -> reads grounded)

GLOW  = "#ffd47a"   # warm lantern light (ALWAYS lit on civ -- the first guaranteed light)

# Grid: 1x1, centred. Course-by-course straight up the centre column (upright, NEVER leaning).
# ============================================================================
# PATH CONTEXT -- a flush path-surface patch the footing pad sits IN (grounded, not on grass).
# ============================================================================
S.box(-0.25, -0.25, 0, 1.5, 1.5, 0.25, GROUND)       # path surface patch, pad sits flush in it

# ============================================================================
# L0 -- cobblestone footing PAD, flush; the ground course the plinth plants on.
# ============================================================================
S.box(0, 0, 0.25, 1, 1, 0.75, PAD, seam=True)        # footing pad, set flush into the path

# ============================================================================
# L1 -- stubby cobblestone_wall PLINTH (a dressed masonry foot -- the visible step up from
#       Trail's bare cobble): slightly inset so it reads as a turned wall post on the pad.
# ============================================================================
S.box(0.18, 0.18, 1.0, 0.64, 0.64, 1.0, WALL, seam=True)   # cobblestone_wall plinth post
S.box(0.18, 0.18, 1.0, 0.2, 0.64, 1.0, WALLD)              # shadowed west cheek -> reads the wall waist

# ============================================================================
# L2-L3 -- the SQUARED stripped-oak-log STANDARD: a 2-log upright post on the plinth (heavier
#          than Trail's thin fence -- THIS is the visible step up). Seam lines read the courses.
# ============================================================================
S.box(0.28, 0.28, 2.0, 0.44, 0.44, 2.0, LOG, seam=True)    # 2-log squared upright standard, y2..4
S.box(0.28, 0.72, 2.0, 0.44, 0.0, 2.0, LOGL)               # lit front edge reads the log courses
S.box(0.28, 0.28, 3.92, 0.44, 0.44, 0.08, LOGE)            # cut-top end-grain ring (the dressed cap)

# ============================================================================
# L4 (top) -- oak_fence FINIAL caps the log (a thinner neck under the lamp), carrying a STANDING
#             lantern on its cap. Always lit on civ placements (the first guaranteed light).
# ============================================================================
S.box(0.36, 0.36, 4.0, 0.28, 0.28, 0.7, FENCE, seam=True)  # oak_fence finial neck on the log cap

S.accent(0.5, 0.5, 4.95, "glow", GLOW, r=3.6)              # standing lantern on the finial (ALWAYS lit)

# ============================================================================
# CALLOUT LABELS
# ============================================================================
S.label(0.5, 0.5, 5.0, "standing lantern on the finial -- ALWAYS lit (first guaranteed light)")
S.label(0.5, 0.5, 4.2, "oak_fence finial neck (a thinner cap under the lamp)")
S.label(0.5, 0.5, 3.0, "SQUARED stripped-oak-log standard, UPRIGHT -- the visible step up from Trail")
S.label(0.5, 0.5, 1.5, "stubby cobblestone_wall plinth (a dressed masonry foot)")
S.label(-0.25, 0.5, 0.3, "cobblestone footing pad, set flush in the path (grounded)")

out = S.svg(title="Lamp-post R2 (Path) -- an UPRIGHT squared-log standard on a cobble-wall plinth, fence finial + standing lantern, always lit",
            size_label="1x1 foot * h5 * 1 lantern (a deliberate upright path fixture -- made, not leaning)",
            label_w=388)
open("detail_svg/lamp_post_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/lamp_post_path.svg | bytes", len(out.encode()))
