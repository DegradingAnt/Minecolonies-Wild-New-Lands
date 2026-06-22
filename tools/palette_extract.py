"""Foundation of the hex->block map (the linchpin for textured renders / layer slices / /wnp showroom).
Parse every render_*.py palette line `NAME = "#hex"  # comment`, guess the vanilla block from the
comment text (the comments almost always name the material), and emit a PER-PIECE draft palette map
+ a global review table. The draft is then hand-confirmed into the canonical map.
Grid colors -> blocks per piece, because the same hex can mean different materials in different pieces."""
import re, glob, json, os

# vanilla-block keyword -> minecraft id. Longest/most-specific keys first so "mossy_cobblestone"
# wins over "cobblestone", "stripped_oak_log" over "oak_log", etc.
BLOCK_KEYWORDS = [
    ("chiseled_stone_brick", "minecraft:chiseled_stone_bricks"),
    ("mossy_stone_brick", "minecraft:mossy_stone_bricks"),
    ("cracked_stone_brick", "minecraft:cracked_stone_bricks"),
    ("stone_brick", "minecraft:stone_bricks"),
    ("mossy_cobblestone", "minecraft:mossy_cobblestone"),
    ("cobbled_deepslate", "minecraft:cobbled_deepslate"),
    ("polished_andesite", "minecraft:polished_andesite"),
    ("smooth_stone_slab", "minecraft:smooth_stone_slab"),
    ("smooth_stone", "minecraft:smooth_stone"),
    ("cobblestone", "minecraft:cobblestone"),
    ("deepslate", "minecraft:deepslate"),
    ("andesite", "minecraft:andesite"),
    ("packed_mud", "minecraft:packed_mud"),
    ("mud_brick", "minecraft:mud_bricks"),
    ("coarse_dirt", "minecraft:coarse_dirt"),
    ("stripped_oak_log", "minecraft:stripped_oak_log"),
    ("stripped_spruce_log", "minecraft:stripped_spruce_log"),
    ("spruce_plank", "minecraft:spruce_planks"),
    ("spruce_slab", "minecraft:spruce_slab"),
    ("spruce_stair", "minecraft:spruce_stairs"),
    ("spruce_trapdoor", "minecraft:spruce_trapdoor"),
    ("spruce_door", "minecraft:spruce_door"),
    ("spruce", "minecraft:spruce_planks"),
    ("oak_log", "minecraft:oak_log"),
    ("oak_fence", "minecraft:oak_fence"),
    ("oak_trapdoor", "minecraft:oak_trapdoor"),
    ("oak_plank", "minecraft:oak_planks"),
    ("oak", "minecraft:oak_planks"),
    ("cobblestone_wall", "minecraft:cobblestone_wall"),
    ("stone_brick_wall", "minecraft:stone_brick_wall"),
    ("iron_bars", "minecraft:iron_bars"),
    ("iron_block", "minecraft:iron_block"),
    ("iron", "minecraft:iron_block"),
    ("chain", "minecraft:chain"),
    ("lantern", "minecraft:lantern"),
    ("campfire", "minecraft:campfire"),
    ("barrel", "minecraft:barrel"),
    ("composter", "minecraft:composter"),
    ("chest", "minecraft:chest"),
    ("gravel", "minecraft:gravel"),
    ("dirt", "minecraft:dirt"),
    ("water", "minecraft:water"),
    ("glass", "minecraft:glass"),
    ("banner", "minecraft:white_banner"),
    ("sign", "minecraft:oak_sign"),
    ("stone", "minecraft:stone"),
    ("slab", "minecraft:smooth_stone_slab"),
    ("stair", "minecraft:cobblestone_stairs"),
    ("plank", "minecraft:oak_planks"),
    ("log", "minecraft:oak_log"),
    ("timber", "minecraft:oak_log"),
    ("roof", "minecraft:spruce_stairs"),
    ("moss", "minecraft:mossy_cobblestone"),
]

def guess_block(comment):
    c = comment.lower()
    for kw, blk in BLOCK_KEYWORDS:
        if kw in c:
            return blk
    return None  # falls through to role resolver

# Role-name fallback for the colours whose comment names the JOB not the material. A sensible vanilla
# BASELINE (the user swaps to modded blocks in-game; the map format takes any block id, vanilla OR modded).
ROLE_DEFAULTS = [
    (["plaque", "panel", "engraved", "chiseled", "relief", "inscription"], "minecraft:chiseled_stone_bricks"),
    (["niche", "recess", "reveal", "doorway", "tunnel", "vault-back", "dark recess"], "minecraft:polished_deepslate"),
    (["post", "finial", "neck", "standard", "pylon", "mullion", "pillar", "gantry"], "minecraft:stone_brick_wall"),
    (["roof", "pitch", "ridge", "eave", "gable", "shingle", "louvre", "soffit"], "minecraft:spruce_stairs"),
    (["loft", "floor", "sill", "deck", "plank board"], "minecraft:spruce_planks"),
    (["deck", "apron", "approach", "trodden", "earth", "path", "threshold", "avenue"], "minecraft:packed_mud"),
    (["frame", "lintel", "bressumer", "beam", "boom", "drum", "architrave", "corbel"], "minecraft:stripped_oak_log"),
    (["plinth", "step", "base", "body", "course", "mass", "band", "trim", "plate", "wall",
      "infill", "skirt", "kerb", "footing", "tower", "drum", "block"], "minecraft:stone_bricks"),
]
def resolve_role(comment):
    c = comment.lower()
    for kws, blk in ROLE_DEFAULTS:
        if any(k in c for k in kws):
            return blk
    return "minecraft:stone_bricks"  # final fallback (dressed stone)

PAL_RE = re.compile(r'^\s*([A-Z][A-Z0-9_]*)\s*=\s*"(#[0-9a-fA-F]{6})"\s*#\s*(.*)$')

per_piece = {}      # piece -> { hex -> {block, var, comment} }
review_rows = []    # (piece, var, hex, guessed_block, comment)
unmapped = 0
for f in sorted(glob.glob("render_*.py")):
    piece = f[len("render_"):-3]
    pal = {}
    for line in open(f, encoding="utf-8"):
        m = PAL_RE.match(line)
        if not m:
            continue
        var, hexc, comment = m.group(1), m.group(2).lower(), m.group(3).strip()
        blk = guess_block(comment)
        role = False
        if blk is None:
            blk = resolve_role(comment); role = True; unmapped += 1
        pal[hexc] = {"block": blk, "var": var, "comment": comment, "role_default": role}
        review_rows.append((piece, var, hexc, blk + (" *(role default — confirm in-game)*" if role else ""), comment[:70]))
    if pal:
        per_piece[piece] = pal

json.dump(per_piece, open("hex_block_map.json", "w", encoding="utf-8"), indent=1)
# review markdown
with open("hex_block_map_review.md", "w", encoding="utf-8") as out:
    out.write("# hex -> block draft map (review: fix any `??` / wrong guesses)\n\n")
    out.write("| piece | var | hex | block (guessed) | comment |\n|---|---|---|---|---|\n")
    for piece, var, hexc, blk, comment in review_rows:
        out.write(f"| {piece} | {var} | `{hexc}` | {blk} | {comment} |\n")

npieces = len(per_piece); ncolors = sum(len(p) for p in per_piece.values())
print(f"pieces={npieces}  palette-colors={ncolors}  unmapped(??)={unmapped}")
print("wrote hex_block_map.json + hex_block_map_review.md")
