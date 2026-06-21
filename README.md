# Minecolonies: Wild New Lands

> ## Alpha — not finished
> Heads up: I'm still building this, so things are unbalanced, some parts are half-done, and
> stuff will change or break between versions. It's playable, and honestly I already think it's
> a good time, but please treat it as a work in progress rather than a finished pack. If
> something seems broken, that's probably why.

Hi, I'm DegradingAnt. Wild New Lands started as me trying to build the Minecraft pack I actually
wanted to play, and it's grown into a bit of an obsession. It's a Minecolonies pack on NeoForge
1.21.1, built around Distant Horizons so the world feels genuinely big and worth wandering through.
What I'm going for is a huge, living world that still runs smoothly and feels like one cohesive
thing rather than a pile of mods stapled together. Most of that is the quiet kind of work: tuning
around 700 mods so they play nicely together, plus a handful of small mods I wrote myself to smooth
over the gaps no existing mod covers.

This repo isn't the playable pack itself. The pack lives on CurseForge, since it needs all the
third-party mods I can't redistribute here. What's in this repo is just my own part of it: the
add-on mods I wrote, the configs I've hand-tuned, and the tooling I use to keep everything stable.

## My add-on mods
Each one is small and does a single job, then gets out of the way.

- **WNL PackFixes** — a coremod that applies around 43 runtime bytecode fixes, so I can patch mod
  bugs without ever editing anyone else's jar.
- **WNL DHSmooth** — smooths out the frame spikes Distant Horizons causes when it redraws distant
  terrain.
- **WNL MineColonies Cache** — caches the MineColonies item-discovery scan to disk. Saves about
  5-6 seconds on every world join after the first.
- **WNL Colony Border Patrols** — moves raid and patrol mobs to the edge of your colony instead of
  letting them spawn right in the middle of it.
- **WNL Join Gate** — force-loads the chunks where you actually land, so the world is solid under
  your feet right away instead of popping in around you.
- **WNL JEIBoost, Archers Attr Fix, FTB Chunks Offload** — smaller, more targeted fixes.

There's more I'm working on that isn't here yet. The worldgen road mod in particular is staying in
a private repo until it's actually ready to show.

## What else is in here
- **configs/** — the config files I've deliberately tuned (Distant Horizons, the performance mods,
  and so on).
- **resourcepacks/** — my own custom resource packs for the pack.
- **tools/** — my Python tooling: scanning mods, harvesting logs, building compatibility datapacks,
  profiling, and exporting the pack.

## Credit
No third-party mod jars or assets are included here, only my own work, and anything I drew
inspiration from is credited. A pack like this only exists because of the wider modding community,
so a genuine thank you to everyone whose work it's built on. And thanks for taking a look.
