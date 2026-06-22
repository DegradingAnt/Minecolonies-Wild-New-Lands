"""Textured isometric renderer — re-skins iso_render boxes with REAL Minecraft block textures.

Reuses iso_render's projection (Iso.P) + occlusion order (_occlusion_order); for each cuboid
face it tiles the block's 16px texture across the face's block-span, shades it to the face
brightness (top 1.0 / south 0.84 / east 0.70 — matching iso_render.shade), and affine-warps it
onto the face parallelogram with PIL (NEAREST = crisp pixel-art), supersampled for clean edges.
Driven by .uvrun/hex_block_map.json (per-piece hex->block) + .uvrun/block_tex/ (vanilla 1.21.1
textures). A face parallelogram is an affine image of the texture rectangle, so a single affine
per face is exact (no perspective needed)."""
import os, json, math, zlib
from PIL import Image, ImageDraw
from iso_render import _occlusion_order

_DIR = os.path.dirname(os.path.abspath(__file__))
TEXDIR = os.path.join(_DIR, "block_tex")
HEXMAP = json.load(open(os.path.join(_DIR, "hex_block_map.json"), encoding="utf-8"))

# block ids whose id != a standalone texture file -> the file MC actually renders the block from
TEX_REMAP = {
    "smooth_stone_slab": "smooth_stone", "cobblestone_stairs": "cobblestone",
    "spruce_stairs": "spruce_planks", "spruce_slab": "spruce_planks",
    "stone_brick_wall": "stone_bricks", "cobblestone_wall": "cobblestone",
    "white_banner": "white_wool", "oak_sign": "oak_planks", "oak_fence": "oak_planks",
    "campfire": "campfire_log", "water": "water_still",
}
_BUILD_SUFFIX = ("_slab", "_stairs", "_wall", "_fence_gate", "_fence", "_door", "_trapdoor",
                 "_button", "_pressure_plate")
_tcache = {}


def _load_tex(name):
    if name in _tcache:
        return _tcache[name]
    p = os.path.join(TEXDIR, name + ".png")
    img = None
    if os.path.exists(p):
        img = Image.open(p).convert("RGBA")
        # animated strips (e.g. water_still = 16x(16*N)) -> use the first frame
        if img.height > img.width and img.width in (16, 32) and img.height % img.width == 0:
            img = img.crop((0, 0, img.width, img.width))
        if img.size != (16, 16):
            img = img.resize((16, 16), Image.NEAREST)
        if name == "water_still":           # semi-transparent -> back with opaque blue so it reads
            base = Image.new("RGBA", img.size, (54, 84, 170, 255))
            img = Image.alpha_composite(base, img)
    _tcache[name] = img
    return img


def _hex2rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _candidates(block, face):
    """Texture-name candidates for a block id + face ('top'|'side'), best first."""
    n = block.split(":", 1)[-1]
    base = TEX_REMAP.get(n, n)
    out = ([base + "_top", base] if face == "top" else [base, base + "_top"])
    for suf in _BUILD_SUFFIX:                       # X_slab/_stairs/_wall -> material X
        if n.endswith(suf):
            mat = n[:-len(suf)]
            out += [mat, mat + "_planks", mat + "_top"]
    out += ["stone"]                                # final fallback
    return out


def _face_tex(block, face):
    for c in _candidates(block, face):
        t = _load_tex(c)
        if t is not None:
            return t
    return None


def _tiled(tex, nx, ny):
    nx = max(1, int(round(nx))); ny = max(1, int(round(ny)))
    out = Image.new("RGBA", (16 * nx, 16 * ny))
    for ix in range(nx):
        for iy in range(ny):
            out.paste(tex, (ix * 16, iy * 16))
    return out


def _shade(img, f):
    if f >= 0.999:
        return img
    lut = [min(255, int(i * f)) for i in range(256)]
    r, g, b, a = img.split()
    return Image.merge("RGBA", (r.point(lut), g.point(lut), b.point(lut), a))


def _inv_affine(O, Pu, Pv, W, H):
    """forward (u,v)->screen: (0,0)->O, (W,0)->Pu, (0,H)->Pv. Return PIL AFFINE inverse coeffs."""
    a = (Pu[0] - O[0]) / W; d = (Pu[1] - O[1]) / W
    b = (Pv[0] - O[0]) / H; e = (Pv[1] - O[1]) / H
    c, f = O[0], O[1]
    det = a * e - b * d or 1e-9
    ia, ib = e / det, -b / det
    id_, ie = -d / det, a / det
    return (ia, ib, -(ia * c + ib * f), id_, ie, -(id_ * c + ie * f))


# --- block-choice VARIATION driven by condition.json (SPEC §3.2). Each base block -> a CLASS-LOCKED
# weighted family (log<->log, brick<->brick — NEVER log<->plank). Picked DETERMINISTICALLY (crc32 seed)
# so it's stable across re-renders + identical to the in-game VariantPalette (same shared config). Role
# gates GRANULARITY: bulk fields scatter per-cell, structural members vary as ONE unit, accents stay fixed.
_COND = (json.load(open(os.path.join(_DIR, "condition.json"), encoding="utf-8"))
         if os.path.exists(os.path.join(_DIR, "condition.json")) else {})
FAMILIES = {k: v for k, v in _COND.get("families", {}).items() if k.startswith("minecraft:")}
INTENSITY = float(_COND.get("intensity", 1.0))
ROLE_GRAN = _COND.get("role_granularity", {})
ROLE_KW = _COND.get("role_keywords", {})
_ROLE_ORDER = ["accent", "timber", "pillar", "floor", "ground", "trim", "facing"]


def _role_of(comment):
    """Classify a palette slot's ROLE from its comment (accent checked first so a 'lantern post' is fixed,
    not a varying timber member)."""
    c = (comment or "").lower()
    for role in _ROLE_ORDER:
        for kw in ROLE_KW.get(role, []):
            if kw and not kw.startswith("_") and kw in c:
                return role
    return "default"


def _gran(role):
    return ROLE_GRAN.get(role, ROLE_GRAN.get("default", "cell"))


# --- THEME palette: the proper modded in-game palette (modded_palette.json, by theme->role), mapped
# through render_proxy.json (modded -> nearest vanilla) for the board's representative preview. A piece
# resolves its per-role base block via piece_themes.json; falls back to the hex_block_map baseline.
def _loadj(name):
    p = os.path.join(_DIR, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


MODDED_PALETTE = _loadj("modded_palette.json")
PIECE_THEMES = _loadj("piece_themes.json").get("pieces", {})
PROXY = _loadj("render_proxy.json")
_TIER_SUF = ("_great_road", "_highway", "_road", "_path", "_trail", "_long", "_great", "_small", "_harbour")


def _theme_base(piece, role):
    """Theme base block for piece+role, mapped through the render proxy (modded->vanilla for the board).
    None when no theme palette applies -> fall back to the hex_block_map baseline."""
    bp = piece if piece in PIECE_THEMES else None
    if bp is None:
        for suf in _TIER_SUF:
            if piece.endswith(suf) and piece[:-len(suf)] in PIECE_THEMES:
                bp = piece[:-len(suf)]; break
    theme = PIECE_THEMES.get(bp) if bp else None
    fam = (MODDED_PALETTE.get(theme) or {}).get("roles", {}).get(role) if theme else None
    if fam:
        return PROXY.get(fam[0], fam[0])
    return None


def _pick_variant(block, seed):
    """Deterministic weighted pick from the block's class-locked family; INTENSITY scales the NON-base
    weights (0 = always base, 1 = as-tuned, >1 = punchier)."""
    fam = FAMILIES.get(block)
    if not fam:
        return block
    weights = [w if i == 0 else w * INTENSITY for i, (_b, w) in enumerate(fam)]
    total = sum(weights) or 1.0
    r = (zlib.crc32(seed.encode()) & 0x7fffffff) % 10000 / 10000.0 * total
    acc = 0.0
    for (blk, _w), w in zip(fam, weights):
        acc += w
        if r < acc:
            return blk
    return fam[-1][0]


def _wcell(name, x, z, y, dx, dz, dy, ix, iy):
    """World block-cell (wx,wy,wz) for tile (ix,iy) on a face — so a block's variant is consistent
    across its visible faces (corner block's top + side tiles hash the same cell)."""
    fx, fz, ytop = math.floor(x), math.floor(z), math.floor(y + dy) - 1
    if name == "top":
        return (fx + ix, ytop, fz + iy)
    if name == "south":
        return (fx + ix, ytop - iy, math.floor(z + dz) - 1)
    return (math.floor(x + dx) - 1, ytop - iy, fz + ix)   # east


def _build_face(piece, base, role, member, name, tf, x, z, y, dx, dz, dy):
    """Tiled face image. Granularity by ROLE: 'fixed' = base everywhere (accents/trim), 'member' = ONE
    variant (member) for the whole structural element (a post never speckles), 'cell' = per-world-cell
    class-locked scatter (bulk walls/floors/road)."""
    if name == "top":
        nx, ny = round(dx), round(dz)
    elif name == "south":
        nx, ny = round(dx), round(dy)
    else:
        nx, ny = round(dz), round(dy)
    nx, ny = max(1, int(nx)), max(1, int(ny))
    gran = _gran(role)
    out = Image.new("RGBA", (16 * nx, 16 * ny))
    for ix in range(nx):
        for iy in range(ny):
            if gran == "fixed":
                blk = base
            elif gran == "member":
                blk = member
            else:
                wx, wy, wz = _wcell(name, x, z, y, dx, dz, dy, ix, iy)
                blk = _pick_variant(base, f"{piece}:{wx}:{wy}:{wz}")
            t = _face_tex(blk, tf) or _face_tex(base, tf)
            if t is not None:
                out.paste(t, (ix * 16, iy * 16))
    return out


# face brightness — matches iso_render.shade factors (top full, south .84, east .70)
_FAC = {"top": 1.0, "south": 0.84, "east": 0.70}


def render(iso, piece, out_path, SS=3, pad=26, bg=(24, 24, 28, 255), out_scale=2.6):
    """Render an Iso instance's boxes as a textured PNG. SS = supersample factor (edge AA);
    out_scale = final px multiplier over the base projection (hi-res output, ~free: we just
    downscale the SS canvas to out_scale× instead of 1×, keeping AA headroom while raising res)."""
    boxes = iso.boxes
    pal = HEXMAP.get(piece, {})
    P = iso.P
    xs, ys = [], []
    for b in boxes:
        x, z, y, dx, dz, dy = b[:6]
        for cx in (x, x + dx):
            for cz in (z, z + dz):
                for cy in (y, y + dy):
                    sx, sy = P(cx, cz, cy); xs.append(sx); ys.append(sy)
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    ox, oy = pad - minx, pad - miny
    CW = int(round((maxx - minx + pad * 2))) * SS
    CH = int(round((maxy - miny + pad * 2))) * SS
    canvas = Image.new("RGBA", (CW, CH), bg)

    def SP(x, z, y):
        sx, sy = P(x, z, y)
        return ((sx + ox) * SS, (sy + oy) * SS)

    for b in _occlusion_order(boxes):
        x, z, y, dx, dz, dy, color = b[0], b[1], b[2], b[3], b[4], b[5], b[6]
        slot = pal.get(str(color).lower(), {})
        role = _role_of(slot.get("comment", ""))
        base = _theme_base(piece, role) or slot.get("block", "minecraft:stone")
        member = _pick_variant(base, f"{piece}:member:{x}:{y}:{z}") if _gran(role) == "member" else base
        faces = [
            ("east",  SP(x + dx, z, y + dy),   SP(x + dx, z + dz, y + dy), SP(x + dx, z, y),     "side"),
            ("south", SP(x, z + dz, y + dy),   SP(x + dx, z + dz, y + dy), SP(x, z + dz, y),     "side"),
            ("top",   SP(x, z, y + dy),        SP(x + dx, z, y + dy),      SP(x, z + dz, y + dy), "top"),
        ]
        for name, O, Pu, Pv, tf in faces:
            tiled = _shade(_build_face(piece, base, role, member, name, tf, x, z, y, dx, dz, dy), _FAC[name])
            W, H = tiled.size
            warped = tiled.transform((CW, CH), Image.AFFINE, _inv_affine(O, Pu, Pv, W, H),
                                     resample=Image.NEAREST)
            poly = [O, Pu, (Pu[0] + Pv[0] - O[0], Pu[1] + Pv[1] - O[1]), Pv]
            clip = Image.new("L", (CW, CH), 0)
            ImageDraw.Draw(clip).polygon(poly, fill=255)
            alpha = Image.composite(warped.split()[3], Image.new("L", (CW, CH), 0), clip)
            # thin edge line for face definition
            ImageDraw.Draw(warped).polygon(poly, outline=(0, 0, 0, 60))
            canvas.paste(warped, (0, 0), alpha)

    # accents — soft radial glow + real lantern sprite (glow), bright cap (finial/dot)
    lantern = _load_tex("lantern")
    for ax, az, ay, kind, ac, r in getattr(iso, "accents", []):
        sx, sy = SP(ax, az, ay)
        rr = max(2.0, r * SS)
        col = _hex2rgb(ac) if isinstance(ac, str) else tuple(ac[:3])
        gs = max(8, int(rr * 7))
        glow = Image.new("RGBA", (gs, gs), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        steps = max(2, int(rr * 3))
        for k in range(steps, 0, -1):
            gd.ellipse([gs / 2 - k, gs / 2 - k, gs / 2 + k, gs / 2 + k],
                       fill=col + (int(46 * (1 - k / steps)),))
        canvas.alpha_composite(glow, (int(sx - gs / 2), int(sy - gs / 2)))
        if kind == "glow" and lantern is not None:
            w, h = int(rr * 1.9), int(rr * 2.3)
            spr = lantern.resize((max(2, w), max(2, h)), Image.NEAREST)
            canvas.alpha_composite(spr, (int(sx - w / 2), int(sy - h / 2)))
        else:
            ImageDraw.Draw(canvas).rectangle([sx - rr, sy - rr, sx + rr, sy + rr],
                                             fill=col + (255,), outline=(0, 0, 0, 120))

    fw, fh = max(1, round(CW / SS * out_scale)), max(1, round(CH / SS * out_scale))
    if (fw, fh) != (CW, CH):
        canvas = canvas.resize((fw, fh), Image.LANCZOS)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    canvas.convert("RGB").save(out_path)
    return out_path


def render_script(script_path, out_path, **kw):
    """Import a render_*.py module, grab its Iso instance, render it textured."""
    import importlib.util
    from iso_render import Iso
    piece = os.path.basename(script_path)[len("render_"):-3]
    spec = importlib.util.spec_from_file_location("_r_" + piece, script_path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    iso = getattr(m, "S", None)
    if not isinstance(iso, Iso):
        iso = next((v for v in vars(m).values() if isinstance(v, Iso)), None)
    if iso is None:
        raise RuntimeError(f"no Iso instance found in {script_path}")
    # piece-name in hex_block_map may differ from filename slug; try filename first
    pkey = piece if piece in HEXMAP else piece
    return render(iso, pkey, out_path, **kw)
