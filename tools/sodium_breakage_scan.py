#!/usr/bin/env python3
"""Scan every mod jar for Sodium-targeting mixins whose target class is ABSENT in the
installed Sodium 0.8.12-beta.2 (i.e. silently non-applying = candidate perf/feature breakage).

Heuristic sweep: for each mixin class listed in a mod's mixin configs, find references to
sodium/embeddium/rubidium classes in its bytecode and check membership against the real
0.8.12 class set (incl. JiJ'd core). Absent target => flag. Judgment layer refines later.
"""
import zipfile, io, json, re, os, sys, collections

MODS = "mods"
SODIUM_JAR = "mods/sodium-neoforge-0.8.12-beta.2+mc1.21.1.jar"

# ONLY the Sodium renderer packages we actually run. jellysquid = pre-0.6 Sodium (definitely
# gone on 0.8.12). caffeinemc = current package (absent class => targets an older 0.6.x layout).
# Deliberately excludes net/irisshaders, embeddium, rubidium (separate jars / not installed).
SODIUM_PKG_RE = re.compile(rb'(?:net/caffeinemc/mods/sodium|me/jellysquid/mods/sodium)[A-Za-z0-9/_$]+')

def build_sodium_classes():
    """internal-name set of all classes provided by the installed Sodium (outer + JiJ core)."""
    classes = set()
    methods = collections.defaultdict(set)  # class -> set(method names)
    z = zipfile.ZipFile(SODIUM_JAR)
    jars = [None]  # outer
    for n in z.namelist():
        if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
            jars.append(n)
    for jarname in jars:
        zz = zipfile.ZipFile(io.BytesIO(z.read(jarname))) if jarname else z
        for n in zz.namelist():
            if n.endswith(".class"):
                cls = n[:-6]
                classes.add(cls)
                # crude method-name harvest from bytecode strings (for later method checks)
                try:
                    data = zz.read(n)
                    for m in re.findall(rb'[a-zA-Z_$][a-zA-Z0-9_$]{2,40}', data):
                        methods[cls].add(m.decode())
                except Exception:
                    pass
    return classes, methods

def mixin_configs(z):
    """yield (configname, package, [mixin classes]) for each mixin json in the jar."""
    for n in z.namelist():
        if n.endswith(".json") and ("mixin" in n.lower()):
            try:
                j = json.loads(z.read(n).decode("utf-8", "replace"))
            except Exception:
                continue
            if not isinstance(j, dict) or "package" not in j:
                continue
            pkg = j.get("package", "")
            mixins = []
            for key in ("mixins", "client", "server"):
                v = j.get(key)
                if isinstance(v, list):
                    mixins += [m for m in v if isinstance(m, str)]
            yield n, pkg, mixins

def main():
    print("Building Sodium 0.8.12 class set...", file=sys.stderr)
    sod_classes, sod_methods = build_sodium_classes()
    print(f"  {len(sod_classes)} sodium classes indexed", file=sys.stderr)

    results = []  # (mod, mixinclass, target_internal, exists_bool)
    jars = sorted(f for f in os.listdir(MODS) if f.endswith(".jar"))
    for jf in jars:
        if jf.startswith("sodium-neoforge"):  # don't scan sodium itself
            continue
        path = os.path.join(MODS, jf)
        try:
            z = zipfile.ZipFile(path)
        except Exception:
            continue
        for cfg, pkg, mixins in mixin_configs(z):
            for mx in mixins:
                cls_internal = (pkg.replace(".", "/") + "/" + mx.replace(".", "/")) if pkg else mx.replace(".", "/")
                entry = cls_internal + ".class"
                try:
                    data = z.read(entry)
                except KeyError:
                    # try without package prefix
                    alt = mx.replace(".", "/") + ".class"
                    try:
                        data = z.read(alt)
                    except KeyError:
                        continue
                refs = set(SODIUM_PKG_RE.findall(data))
                if not refs:
                    continue
                for r in refs:
                    target = r.decode()
                    # strip trailing $Inner descriptors? keep as-is; check membership + outer class
                    base = target.split("$")[0]
                    exists = (target in sod_classes) or (base in sod_classes)
                    results.append((jf, mx, target, exists))
        z.close()

    # report: group by mod, show absent (broken) targets first
    broken = [r for r in results if not r[3]]
    bymod = collections.defaultdict(lambda: {"absent": set(), "present": set()})
    for mod, mx, tgt, ex in results:
        bymod[mod]["present" if ex else "absent"].add(tgt)

    print("=" * 70)
    print("SODIUM-BREAKAGE SWEEP — mods with mixins targeting ABSENT Sodium classes")
    print("=" * 70)
    flagged = sorted((m for m in bymod if bymod[m]["absent"]), key=lambda m: -len(bymod[m]["absent"]))
    if not flagged:
        print("  (none — no mod targets a missing Sodium class)")
    for mod in flagged:
        ab = bymod[mod]["absent"]
        print(f"\n### {mod}  ({len(ab)} absent target(s))")
        for t in sorted(ab):
            print(f"    ABSENT: {t}")
    print("\n" + "=" * 70)
    print(f"SUMMARY: {len(flagged)} mods reference >=1 missing Sodium class")
    print(f"         {len(bymod)} mods total have Sodium-targeting mixins")
    # also list mods that hook sodium but all-present (for completeness)
    okmods = sorted(m for m in bymod if not bymod[m]["absent"])
    print(f"\nMods with Sodium mixins, all targets PRESENT ({len(okmods)}):")
    print("  " + ", ".join(okmods))

if __name__ == "__main__":
    main()
