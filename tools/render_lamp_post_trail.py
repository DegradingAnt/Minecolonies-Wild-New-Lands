"""Lamp-post TRAIL (R1, floor of the ladder) -> detail_svg/lamp_post_trail.svg.
Per deco_catalog_v2.json id 'lamp_post' tier Trail (footprint 1x1, height 3): the humblest
grounded light-marker -- a single half-sunk cobblestone footing with a thin oak_fence post that
LEANS crooked over it (the footing is offset one cell on ~50% of spawns -> the post sits settled,
NOT a rotated block; every node still rests on the node below), capped by a standing lantern that
is OFTEN ABSENT far from civ (drawn here as the lit civ case). Reads as a worn stub by silhouette
in daylight -- short, leaning, frequently unlit. The lean is the catalog's signature build-technique
(A): faked by offsetting the footing, never floating.

Escalation: floor of the ladder -- distinguished from Path not by one block but by being SHORT
(h3), LEANING/half-sunk, and the only rung that is frequently UNLIT. A worn stub, not a fixture.

Originality/inspiration: the universal leaning roadside marker-post folk form, technique only;
the Roman milliarium read at its humblest. Credited in CREDITS.md, no assets/NBT copied. Same
wnl_lamp_post identity whose Great-Road top tier is the twin-pier light-arch; the data builder
hashes lean/decay/light live per post."""
from iso_render import Iso

S = Iso(U=30)

# --- palette (literal) -- a humble cobble + bare timber + warm light ladder; comment each ---
CORE  = "#8a8276"   # cobblestone footing pad (the common pick)
MOSS  = "#6f7d56"   # mossy_cobblestone (wear creeps in by distance -- footing swap)
POST  = "#a9874f"   # oak_fence post (warm bare timber -- the thin leaning stub)
POSTL = "#bd9a5c"   # oak_fence seam-lit edge (a touch warmer, reads the rails)
GROUND= "#5d5447"   # the trodden trail surface the footing sinks INTO (darker -> reads sunk)

GLOW  = "#ffd47a"   # warm lantern light (often ABSENT on this rung -- shown lit, the civ case)

# Grid: 1x1 footing. The LEAN: the footing is shoved off-centre toward FRONT-EAST (the visible
# faces) by ~0.3 so the post column above sits crooked over it -- a settled post, not a drop.
# ============================================================================
# TRAIL CONTEXT -- a sunk trodden-ground patch the footing roots INTO (never floats on grass).
# ============================================================================
S.box(-0.3, -0.3, 0, 1.6, 1.6, 0.35, GROUND)         # trodden trail patch, the footing sinks into it

# ============================================================================
# L0 -- half-sunk cobblestone FOOTING, offset front-east (the lean seed); reads rooted.
# ============================================================================
S.box(0.3, 0.3, 0.2, 1, 1, 0.85, CORE, seam=True)    # footing pad, sunk 0.2 into the trodden ground
S.box(0.45, 0.65, 0.55, 0.55, 0.4, 0.4, MOSS)        # moss creeping the sunk front edge (wear note)

# ============================================================================
# L1 -- the thin oak_fence POST, sitting CROOKED over the offset footing (the lean). The post
#       base abuts the footing top; it leans back-west toward centre so the inner half bears on
#       the footing below (a settled post, supported -- never a floating or rotated block).
# ============================================================================
S.box(0.12, 0.16, 1.05, 0.34, 0.34, 1.55, POST, seam=True)   # leaning fence post, base resting on footing top
S.box(0.12, 0.5, 1.05, 0.34, 0.0, 1.55, POSTL)               # (thin lit front edge reads the rails)

# ============================================================================
# L2 (top) -- standing lantern on the post cap (the CIV case; OFTEN ABSENT far from civ ->
#             the most-remote post reads dead/unlit). Rests on the fence cap, never floating.
# ============================================================================
S.accent(0.29, 0.33, 2.75, "glow", GLOW, r=3.4)      # standing lantern on the post cap (often absent)

# ============================================================================
# CALLOUT LABELS
# ============================================================================
S.label(0.29, 0.33, 2.8, "standing lantern on the cap -- OFTEN ABSENT far from civ (dead marker)")
S.label(0.3, 0.3, 1.8, "thin oak_fence post LEANS crooked over the offset footing (settled, supported)")
S.label(0.8, 0.8, 0.5, "half-sunk cobblestone footing, shoved off-centre (the lean seed)")
S.label(-0.3, 0.3, 0.2, "sunk into the trodden trail ground (rooted, never floats on grass)")

out = S.svg(title="Lamp-post R1 (Trail) -- a leaning half-sunk worn marker-post, short + often UNLIT, reads by silhouette",
            size_label="1x1 foot * h3 * 0-1 lanterns (ladder floor -- a worn leaning roadside stub)",
            label_w=384)
open("detail_svg/lamp_post_trail.svg", "w", encoding="utf-8").write(out)
print("wrote detail_svg/lamp_post_trail.svg | bytes", len(out.encode()))
