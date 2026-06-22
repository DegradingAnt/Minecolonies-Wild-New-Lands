"""Export every deco piece's GEOMETRY to a mod-readable JSON (the bridge from the Python render scripts
to the in-game DecoPlacer + /wnp showroom). Runs each render_*.py, captures its Iso boxes, resolves the
IN-GAME block per box (the theme's MODDED base where a theme applies — NOT the board's vanilla proxy —
else the hex_block_map baseline) + the role, and maps iso coords (x right, z depth, y up) to world
(x,y,z). VariantPalette applies the class-locked scatter at placement; this stores the base block+role."""
import importlib.util, glob, json
import iso_tex
from iso_render import Iso

_TIER = iso_tex._TIER_SUF


def theme_family(piece, role, hexc):
    """(base block, theme family list | None). The theme's MODDED family for this role (un-proxied), so
    the placer scatters across it in-game; else the hex baseline (None family -> condition.json families
    scatter it instead)."""
    bp = piece if piece in iso_tex.PIECE_THEMES else None
    if bp is None:
        for suf in _TIER:
            if piece.endswith(suf) and piece[:-len(suf)] in iso_tex.PIECE_THEMES:
                bp = piece[:-len(suf)]; break
    theme = iso_tex.PIECE_THEMES.get(bp) if bp else None
    fam = (iso_tex.MODDED_PALETTE.get(theme) or {}).get("roles", {}).get(role) if theme else None
    if fam:
        return fam[0], list(fam)
    return iso_tex.HEXMAP.get(piece, {}).get(hexc, {}).get("block", "minecraft:stone"), None


out = {}
for sp in sorted(glob.glob("render_*.py")):
    piece = sp[len("render_"):-3]
    spec = importlib.util.spec_from_file_location("_geo_" + piece, sp)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    iso = getattr(m, "S", None)
    if not isinstance(iso, Iso):
        iso = next((v for v in vars(m).values() if isinstance(v, Iso)), None)
    if iso is None:
        continue
    pal = iso_tex.HEXMAP.get(piece, {})
    boxes = []
    for b in iso.boxes:
        x, z, y, dx, dz, dy, color = b[0], b[1], b[2], b[3], b[4], b[5], b[6]
        slot = pal.get(str(color).lower(), {})
        role = iso_tex._role_of(slot.get("comment", ""))
        blk, fam = theme_family(piece, role, str(color).lower())
        box = {"x": round(x, 2), "y": round(y, 2), "z": round(z, 2),
               "dx": max(1, int(round(dx))), "dy": max(1, int(round(dy))), "dz": max(1, int(round(dz))),
               "block": blk, "role": role}
        if fam and len(fam) > 1:
            box["family"] = fam
        boxes.append(box)
    accents = [{"x": round(a[0], 2), "y": round(a[2], 2), "z": round(a[1], 2),
                "kind": a[3]} for a in getattr(iso, "accents", [])]
    xs = [b["x"] for b in boxes] + [b["x"] + b["dx"] for b in boxes]
    zs = [b["z"] for b in boxes] + [b["z"] + b["dz"] for b in boxes]
    ys = [b["y"] + b["dy"] for b in boxes]
    out[piece] = {"boxes": boxes, "accents": accents,
                  "w": int(round(max(xs) - min(xs))) if xs else 0,
                  "d": int(round(max(zs) - min(zs))) if zs else 0,
                  "h": int(round(max(ys))) if ys else 0, "n": len(boxes)}

json.dump(out, open("piece_geometry.json", "w", encoding="utf-8"), separators=(",", ":"))
print("exported %d pieces | %d boxes total | %d accents" % (
    len(out), sum(v["n"] for v in out.values()), sum(len(v["accents"]) for v in out.values())))
mods = sorted({b["block"].split(":")[0] for v in out.values() for b in v["boxes"] if ":" in b["block"]})
print("block namespaces used:", ", ".join(mods))
