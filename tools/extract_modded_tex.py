"""Resolve + extract a MODDED block's real texture (blockstate -> model -> textures), handling the
cases the block-id-name shortcut misses (CTM base tiles, model indirection, parent inheritance).
Foundation of the deco renderer's modded palette (SPEC §3 / §3.2). Input: a JSON list of block ids.
Output: block_tex/<ns>__<tex>.png + modded_tex_map.json (block id -> texture filename). Renders show
the REAL modded block; the palette stays data-driven so the vanilla-only port is a data swap."""
import json, glob, zipfile, os, sys

MODS = glob.glob("mods/*.jar")
TEXDIR = "block_tex"
_names = {}


def _namelist(j):
    if j not in _names:
        try:
            with zipfile.ZipFile(j) as z:
                _names[j] = set(z.namelist())
        except Exception:
            _names[j] = set()
    return _names[j]


def _find(path):
    for j in MODS:
        if path in _namelist(j):
            return j
    return None


def _read(jar, path):
    with zipfile.ZipFile(jar) as z:
        return json.loads(z.read(path))


def _model_textures(ns, ref, depth=0):
    """Follow a model ref (ns:block/x or block/x) + parents; merge their texture dicts (child wins)."""
    if depth > 6 or not ref:
        return {}
    mns, mpath = ref.split(":", 1) if ":" in ref else (ns, ref)
    apath = "assets/%s/models/%s.json" % (mns, mpath)
    jar = _find(apath)
    if not jar:
        return {}
    m = _read(jar, apath)
    tex = {}
    if "parent" in m:
        tex.update(_model_textures(ns, m["parent"], depth + 1))
    tex.update(m.get("textures", {}))
    return tex


def resolve(block_id):
    """Return texture ref 'ns:block/x' for a sensible visible face of the block, or None."""
    ns, name = block_id.split(":", 1)
    if _find("assets/%s/textures/block/%s.png" % (ns, name)):
        return "%s:block/%s" % (ns, name)
    jar = _find("assets/%s/blockstates/%s.json" % (ns, name))
    if not jar:
        return None
    bs = _read(jar, "assets/%s/blockstates/%s.json" % (ns, name))
    model = None
    if "variants" in bs:
        v = next(iter(bs["variants"].values()))
        if isinstance(v, list):
            v = v[0]
        model = v.get("model")
    elif "multipart" in bs:
        for part in bs["multipart"]:
            a = part.get("apply")
            if isinstance(a, list):
                a = a[0]
            if a and a.get("model"):
                model = a["model"]; break
    tex = _model_textures(ns, model)
    for key in ("all", "texture", "side", "end", "top", "north", "wall", "0", "1"):
        if key in tex and not str(tex[key]).startswith("#"):
            return tex[key]
    for k, v in tex.items():
        if k != "particle" and not str(v).startswith("#"):
            return v
    return None


def extract(block_ids):
    os.makedirs(TEXDIR, exist_ok=True)
    out = {}
    miss = []
    for bid in block_ids:
        ref = resolve(bid)
        if not ref:
            miss.append(bid); continue
        rns, rpath = ref.split(":", 1) if ":" in ref else (bid.split(":")[0], ref)
        apath = "assets/%s/textures/%s.png" % (rns, rpath)
        jar = _find(apath)
        if not jar:
            miss.append(bid); continue
        fn = "%s__%s.png" % (rns, rpath.replace("/", "_"))
        with zipfile.ZipFile(jar) as z:
            open(os.path.join(TEXDIR, fn), "wb").write(z.read(apath))
        out[bid] = fn
    json.dump(out, open("modded_tex_map.json", "w"), indent=1)
    print("resolved %d/%d  (missed %d)" % (len(out), len(block_ids), len(miss)))
    for m in miss:
        print("  MISS", m)
    return out


if __name__ == "__main__":
    ids = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else []
    for bid, fn in extract(ids).items():
        print("  OK", bid, "->", fn)
