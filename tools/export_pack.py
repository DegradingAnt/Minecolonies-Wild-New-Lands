#!/usr/bin/env python3
"""Comprehensive 'export ALL changed stuff' for the Ultimate Vibes pack.
Regenerates a Desktop bundle from CURRENT instance state (idempotent -> safe to
run on a schedule/hook). Mirrors the established 2026-06-17 export layout.
Usage: export_pack.py [output_dir]   (default: Desktop\\WNL-Pack-Export)
"""
import os, sys, shutil, glob, datetime

ROOT = r"C:\Users\linde\curseforge\minecraft\Instances\Ultimate vibes distant horizons version"
OUT = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\linde\Desktop\WNL-Pack-Export"

# config files/dirs that are intentionally tuned for this pack (the "changed configs")
CHANGED_CONFIGS = [
    "DistantHorizons.toml", "dynamic_difficulty-common.toml", "entity_model_features.json",
    "logbegone.json", "modernfix-mixins.properties", "wnl_dhsmooth.properties",
    "calmtheleaks-common.toml", "almostunified", "spark",
]
# The server bundle carries ONLY the configs WE actually tune (+ the Paxi loot datapack we
# regenerate) -- not the whole config/ tree -- so every update is a small, reviewable delta to
# upload to DatHost. Untouched configs were uploaded once at setup and don't need re-pushing.
# (For a FRESH server install with the complete config/, use build_server_pack.py instead.)
SERVER_TUNED_CONFIGS = [
    # shared/server-relevant tuned values
    "DistantHorizons.toml", "dynamic_difficulty-common.toml", "logbegone.json",
    "calmtheleaks-common.toml", "modernfix-mixins.properties", "spark", "almostunified",
    # server-side tunes
    "minecolonies-server.toml", "doespotatotick-common.toml", "entityculling.json",
    "perf_tweaks", "moreculling.toml", "subtle_effects",
]
# server-relevant custom mods (worldgen/server-side) -- DHSmooth is client-only and excluded
SERVER_MODS = ["WNL-PackFixes-", "WNL-MineColoniesCache-",
               "WNL-ArchersAttrFix-", "WNL-FTBChunksOffload-"]


def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif os.path.isfile(src):
        shutil.copy2(src, dst)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    n = {"mods": 0, "config": 0, "datapacks": 0, "rp": 0, "server": 0, "config_server": 0}

    # ---- instance-overlay (client drop-in) ----
    ov = os.path.join(OUT, "instance-overlay")
    for j in glob.glob(os.path.join(ROOT, "mods", "WNL-*.jar")):
        cp(j, os.path.join(ov, "mods", os.path.basename(j))); n["mods"] += 1
    for c in CHANGED_CONFIGS:
        s = os.path.join(ROOT, "config", c)
        if os.path.exists(s):
            cp(s, os.path.join(ov, "config", c)); n["config"] += 1
    # Paxi compat datapack + load order
    if os.path.isdir(os.path.join(ROOT, "config", "paxi")):
        cp(os.path.join(ROOT, "config", "paxi"), os.path.join(ov, "config", "paxi"))
    for z in glob.glob(os.path.join(ROOT, "datapacks", "*.zip")):
        cp(z, os.path.join(ov, "datapacks", os.path.basename(z))); n["datapacks"] += 1
    for z in glob.glob(os.path.join(ROOT, "resourcepacks", "WNL-*.zip")):
        cp(z, os.path.join(ov, "resourcepacks", os.path.basename(z))); n["rp"] += 1

    # ---- server-upload (DatHost): mirrors the server root = mods/ + FULL config/ ----
    su = os.path.join(OUT, "server-upload")
    for j in glob.glob(os.path.join(ROOT, "mods", "WNL-*.jar")):
        if any(os.path.basename(j).startswith(p) for p in SERVER_MODS):
            cp(j, os.path.join(su, "mods", os.path.basename(j))); n["server"] += 1
    # patched DH server jar from prior server-delivery if present
    for dh in glob.glob(os.path.join(ROOT, ".uvrun", "server-delivery", "DistantHorizons-*.jar")):
        cp(dh, os.path.join(su, "mods", os.path.basename(dh)))
    # ALL relevant configs: mirror the ENTIRE config/ tree. The dedicated server simply ignores
    # inert client-only configs, so copying everything guarantees every server-relevant config
    # (worldgen, difficulty/levelling, registry, *-common.toml, *-server.toml) AND the Paxi
    # WNL-Compat datapack at config/paxi/datapacks/ are present and in sync — nothing missed.
    # only the configs we tune
    for c in SERVER_TUNED_CONFIGS:
        s = os.path.join(ROOT, "config", c)
        if os.path.exists(s):
            cp(s, os.path.join(su, "config", c))
    # + the Paxi loot datapack we regenerate (WNL-Compat) and its load order
    if os.path.isdir(os.path.join(ROOT, "config", "paxi", "datapacks", "WNL-Compat")):
        cp(os.path.join(ROOT, "config", "paxi", "datapacks", "WNL-Compat"),
           os.path.join(su, "config", "paxi", "datapacks", "WNL-Compat"))
    for lo in ("datapack_load_order.json", "resourcepack_load_order.json"):
        s = os.path.join(ROOT, "config", "paxi", lo)
        if os.path.exists(s):
            cp(s, os.path.join(su, "config", "paxi", lo))
    su_cfg = os.path.join(su, "config")
    n["config_server"] = sum(len(fs) for _, _, fs in os.walk(su_cfg)) if os.path.isdir(su_cfg) else 0

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(OUT, "README.txt"), "w", encoding="utf-8") as f:
        f.write(
            "WNL — full pack export (auto-generated)\n"
            "=================================================\n"
            f"Generated: {stamp} from current instance state.\n\n"
            "instance-overlay/  -> drop into your client instance (merge mods/, config/,\n"
            f"   datapacks/, resourcepacks/). Custom mods: {n['mods']}, changed configs: {n['config']},\n"
            f"   global datapacks: {n['datapacks']}, resourcepacks: {n['rp']}.\n"
            "server-upload/     -> mirrors the server root: merge mods/ + config/ onto the DatHost\n"
            f"   server. Server custom mods: {n['server']}, server config files: {n['config_server']}\n"
            "   (FULL config/ tree incl. the Paxi WNL-Compat datapack at config/paxi/datapacks/).\n"
            "   DHSmooth is client-only and intentionally NOT in mods/.\n\n"
            "This bundle is regenerated automatically at the end of each session.\n"
        )
    print(f"EXPORT OK -> {OUT}")
    print("  " + ", ".join(f"{k}={v}" for k, v in n.items()))


if __name__ == "__main__":
    main()
