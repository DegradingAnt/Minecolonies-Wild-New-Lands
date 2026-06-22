"""Gatehouse PATH (R2) -> detail_svg/gatehouse_path.svg.
Per deco_catalog_v2.json id 'gatehouse' tier Path (footprint 7x3, opening 5 clear, height 6):
a small step from Trail -- the timber goalpost gains a MASONRY FOOT (stone-brick plinth before
the timber), CARPENTER KNEE-BRACES (inward stairs at each post-to-beam corner so the arch reads
built, not lashed), a CENTRED CROWN sign on the beam, and a SECOND lantern (now a two-lantern
crown). Still a single-plane data-driven arch -- NO towers (the big leaps are saved for Road and up,
non-linear ladder). Same wnl_gatehouse family as render_gatehouse.py (Great Road top).

ISO: road-facing FRONT = high-z (south, z=2 face) + high-x (east); the carved sign turned to that
front. Inspiration: timber way-arch / lych-gate folk form + carpentry knee-bracing -- technique only,
credited in CREDITS.md, no assets/NBT copied."""
from iso_render import Iso

S = Iso(U=20)

# ---- palette (literal) -- WIDE-CONTRAST ladder, each material reads as itself.
#      luminance dark->light: FOOT < PLINTH < BEAM < POST < BRACE < SIGN < SIGNF ; LANT warm.
FOOT  = "#6f685d"   # cobblestone footing pad (dark grey -> rooted, heavy)
PLINTH= "#8f897c"   # stone_bricks masonry foot before the timber (mid grey -> the NEW masonry note)
POST  = "#8a6a3f"   # oak LOG upright post (warm mid timber)
BEAM  = "#7a5c3a"   # stripped-log lintel beam (darker timber -> spans read distinct from posts)
BRACE = "#a07c4a"   # oak_stairs knee-brace (lighter timber -> the carpentered diagonal reads)
SIGN  = "#b9b3a5"   # chiseled_stone_bricks / sign-board crown block (bright -> the carved face pops)
SIGNF = "#403c34"   # the recessed carved face turned to the road (dark inset)
POSTW = "#9a7448"   # short sign-post on the beam (timber, holds the sign up)

# =====================================================================================
# Course 0 (ground): two stone FOOTING PADS, each 1x2 along z, at x=0 and x=6 (z=0..1) so the
# posts read planted deep. Opening between = 5 clear -> the path passes through.
# =====================================================================================
S.box(0, 0, 0, 1, 2, 1, FOOT, seam=True)          # left footing pad 1x2 (rooted)
S.box(6, 0, 0, 1, 2, 1, FOOT, seam=True)          # right footing pad 1x2

# =====================================================================================
# Courses 1-2 (plinth): on each footing a 1x1 stone-brick MASONRY FOOT before the timber --
# the new idea over Trail (a built base, not a log stood on dirt). Centred on the footing.
# =====================================================================================
S.box(0, 0.5, 1, 1, 1, 1, PLINTH, seam=True)      # left masonry foot
S.box(6, 0.5, 1, 1, 1, 1, PLINTH, seam=True)      # right masonry foot

# =====================================================================================
# Courses 2-5 (posts): two LIGHT timber posts, 1x1 log columns rising from each plinth to y=5.
# Seated squarely on the masonry foot (full bearing, grounded).
# =====================================================================================
S.box(0, 0.5, 2, 1, 1, 3, POST, seam=True)        # left post y2..4
S.box(6, 0.5, 2, 1, 1, 3, POST, seam=True)        # right post y2..4

# =====================================================================================
# Course 5 (braced lintel): a LIGHT timber BEAM spanning x=0..6 across the post tops, plus a
# KNEE-BRACE stair tucked into each post-to-beam INNER corner (facing inward, half=top) so the
# arch reads carpentered. Each brace abuts BOTH its post and the beam (grounded in the corner).
# =====================================================================================
S.box(0, 0.5, 5, 7, 1, 1, BEAM, seam=True)        # lintel beam x0..6 across the post tops
# inner knee-braces: rise from the post top, lean in to meet the beam underside (corner-filling)
S.box(1.0, 0.55, 4.3, 0.9, 0.9, 0.7, BRACE)       # left knee-brace (abuts left post + beam underside)
S.box(5.1, 0.55, 4.3, 0.9, 0.9, 0.7, BRACE)       # right knee-brace (abuts right post + beam underside)

# =====================================================================================
# Course 6 (crown): a centred CARVED SIGN on a short post on the beam at x=3, carved face turned
# to the road (front, high-z). Grounded: the sign-post rises from the beam top directly below.
# =====================================================================================
S.box(3.0, 0.6, 6, 1, 0.8, 1, POSTW)              # short sign-post on the beam (grounded on beam top)
S.box(2.7, 0.55, 6.2, 1.6, 0.7, 1.0, SIGN)        # the sign board (bright dressed stone, faces road)
S.box(2.8, 1.2, 6.45, 1.4, 0.12, 0.6, SIGNF)      # recessed carved face turned to the road (front)

# =====================================================================================
# LIGHTING: TWO hanging lanterns slung under the beam soffit, one near each post (x=1, x=5), each
# held by the beam directly above -> grounded by suspension. The two-lantern crown (Trail had 1).
# =====================================================================================
S.accent(1.3, 1.0, 4.75, "glow", "#ffd47a", r=2.4)   # left hanging lantern under the beam
S.accent(5.3, 1.0, 4.75, "glow", "#ffd47a", r=2.4)   # right hanging lantern under the beam

S.label(3.0, 0.5, 6.3, "centred carved sign on a beam-post -- face turned to the road")
S.label(5.3, 1.0, 4.8, "TWO-lantern crown (second lantern -- Trail had one)")
S.label(1.0, 0.5, 4.4, "carpenter knee-braces (inward stairs) -- the arch reads built")
S.label(6.0, 0.5, 1.5, "stone-brick masonry foot before the timber posts")
S.label(0.0, 0.5, 0.4, "two 1x2 stone footing pads (5 clear -- path passes through)")

out = S.svg(title="Gatehouse R2 (Path) -- timber arch gains a masonry foot, knee-braces, a sign crown + a 2nd lantern",
            size_label="7x3 foot (5 clear) * h6 * 2 lanterns (a made gate, still light timber construction)",
            label_w=372)
open("detail_svg/gatehouse_path.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/gatehouse_path.svg | bytes", len(out.encode()))
