"""Explosion detector: run every render_*.py with Iso.box patched to record cuboids, then voxelise
each piece into columns and flag any column with an AIR POCKET (a vertical gap > ~1 block between
occupied spans) -- i.e. mass floating over empty space (the gatehouse-road bug). Pure geometry, no
image reads. Prints the scripts to fix + the offending columns/heights."""
import glob, math, iso_render

REC = []
_orig = iso_render.Iso.box
def _patched(self, x, z, y, dx, dz, dy, color, seam=False):
    REC.append((float(x), float(z), float(y), float(dx), float(dz), float(dy)))
    return _orig(self, x, z, y, dx, dz, dy, color, seam)
iso_render.Iso.box = _patched

MERGE = 0.55   # spans closer than this vertically are the same mass (tolerates thin trim / leans)
GAP   = 0.9    # an air pocket bigger than this between masses in a column = floating

def columns(boxes):
    cols = {}
    for x, z, y, dx, dz, dy in boxes:
        xi0, xi1 = math.floor(x + 0.001), math.ceil(x + dx - 0.001)
        zi0, zi1 = math.floor(z + 0.001), math.ceil(z + dz - 0.001)
        for xi in range(xi0, max(xi1, xi0 + 1)):
            for zi in range(zi0, max(zi1, zi0 + 1)):
                cx, cz = xi + 0.5, zi + 0.5
                if x - 0.5 <= cx <= x + dx + 0.5 and z - 0.5 <= cz <= z + dz + 0.5:
                    cols.setdefault((xi, zi), []).append((y, y + dy))
    return cols

def air_pockets(spans):
    spans = sorted(spans)
    merged = [list(spans[0])]
    for a, b in spans[1:]:
        if a <= merged[-1][1] + MERGE:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    gaps = []
    for i in range(1, len(merged)):
        g = merged[i][0] - merged[i-1][1]
        if g > GAP:
            gaps.append((round(merged[i-1][1], 1), round(merged[i][0], 1), round(g, 1)))
    return gaps

flagged = {}
for sc in sorted(glob.glob("render_*.py")):
    REC.clear()
    try:
        exec(compile(open(sc, encoding="utf-8").read(), sc, "exec"),
             {"__name__": "__main__", "__file__": sc})
    except Exception as e:
        flagged[sc] = [("EXEC ERROR", str(e)[:120])]
        continue
    hits = []
    for (xi, zi), spans in columns(list(REC)).items():
        for lo, hi, g in air_pockets(spans):
            hits.append((xi, zi, lo, hi, g))
    if hits:
        flagged[sc] = sorted(hits, key=lambda h: -h[4])

if not flagged:
    print("CLEAN -- no air pockets in any render.")
else:
    for sc in sorted(flagged):
        h = flagged[sc]
        print(f"{sc}: {len(h)} floating column(s)")
        for x, z, lo, hi, g in h[:5] if isinstance(h[0], tuple) and len(h[0]) == 5 else []:
            print(f"    col(x={x},z={z})  gap {lo}->{hi}  ({g} blocks of air under floating mass)")
        if h and not (len(h[0]) == 5):
            print("   ", h[0])
