package com.wnl.dhsmooth;

import com.seibel.distanthorizons.api.interfaces.config.IDhApiConfigValue;
import com.seibel.distanthorizons.core.api.external.methods.config.client.DhApiMultiThreadingConfig;
import net.minecraft.client.Minecraft;

/**
 * Adaptive DH worker-thread governor — "do more when there's headroom, throttle when perf drops".
 *
 * WHY: a JFR while DH was generating showed the FPS cost is NOT DH's render-thread time
 * (DH is ~1.5% of the render thread). It's CPU CONTENTION: DH's worker pools (LOD build,
 * world-gen, render-load — the {@code DH-Render Loader Thread}s) run hot alongside Sodium's
 * chunk meshers and the server world-gen thread, saturating cores so the render thread is
 * starved -> frames drop while terrain streams in.
 *
 * HOW: DH already self-limits every worker by a "run-time ratio" — each thread runs that
 * fraction of the time and sleeps the rest (see {@code RateLimitedThreadPoolExecutor.runTimeRatioConfig};
 * exposed via the public API {@code IDhApiMultiThreadingConfig.threadRuntimeRatio()}). We drive
 * that ratio from the live frame-rate:
 *   - plenty of FPS headroom  -> ratio toward CEIL (DH works full speed, terrain fills fast)
 *   - render thread starved   -> ratio toward FLOOR (DH backs off, the render thread recovers)
 * Only worker SPEED changes — never LOD quality or range — so the graphics floor is intact and
 * we never touch the user's distanthorizons.toml. Fully reversible: on disable we hand DH back
 * the exact ratio it had. Any API hiccup -> we stop touching DH and it behaves normally.
 *
 * Config keys live in config/wnl_dhsmooth.properties (governor*), loaded by {@link DhSmooth}.
 */
public final class DhThreadGovernor {

    public static volatile boolean ENABLED = true;
    public static volatile double GOOD_FPS = 70.0;    // at/above -> full speed (ceil)
    public static volatile double BAD_FPS = 45.0;     // at/below -> throttled (floor)
    public static volatile double FLOOR_RATIO = 0.10; // min worker run-time ratio under load
    public static volatile double CEIL_RATIO = 1.00;  // max worker run-time ratio with headroom
    public static volatile double SMOOTH = 0.20;      // easing per update (0..1), anti-oscillation

    private static double current = -1.0;   // last ratio we applied; -1 until initialised
    private static Double original = null;  // the user's DH ratio, captured once on first in-world run
    private static long tick = 0L;
    private static int warmup = 0;          // in-world ticks waited before engaging
    private static final int WARMUP_TICKS = 100; // ~5s in-world — let DH finish setting up its threading
    private static boolean broken = false;  // after any API error, stop touching DH for the session

    private DhThreadGovernor() {}

    /**
     * Fired every client tick (20/s). We act 5x/s (every 4th tick) — DH's worker cadence and the
     * FPS counter both move slower than that, so finer would just be noise. Never throws.
     */
    public static void onClientTick() {
        if (broken || !ENABLED) {
            return; // disabled or already errored -> NEVER touch DH (avoids the menu <clinit> poison)
        }
        // CRITICAL — client ticks fire at the TITLE SCREEN, before DH sets up its threading/config.
        // Touching DhApiMultiThreadingConfig there runs ThreadPresetConfigEventHandler.<clinit> too
        // early -> NPE -> ExceptionInInitializerError -> that class is PERMANENTLY poisoned and DH
        // itself breaks (the SAME <clinit>-too-early trap as the FFAPI cascade). So gate on a loaded
        // level + a short warm-up before EVER referencing a DH class.
        if (Minecraft.getInstance().level == null) {
            warmup = 0;
            return;
        }
        if (warmup < WARMUP_TICKS) {
            warmup++;
            return;
        }
        try {
            DhApiMultiThreadingConfig cfg = DhApiMultiThreadingConfig.INSTANCE;
            if (cfg == null) {
                return; // DH not ready yet
            }
            IDhApiConfigValue<Double> ratio = cfg.threadRuntimeRatio();
            if (ratio == null) {
                return;
            }

            // First run: remember the user's configured ratio so a sane starting point eases in.
            if (original == null) {
                Double cur = ratio.getValue();
                original = (cur != null) ? cur : CEIL_RATIO;
                current = original;
            }

            if ((tick++ & 3L) != 0L) {
                return; // act ~5x/sec
            }

            double fps = Minecraft.getInstance().getFps();
            double headroom; // 0.0 (struggling) .. 1.0 (plenty)
            if (fps >= GOOD_FPS) {
                headroom = 1.0;
            } else if (fps <= BAD_FPS) {
                headroom = 0.0;
            } else {
                headroom = (fps - BAD_FPS) / (GOOD_FPS - BAD_FPS);
            }

            double target = FLOOR_RATIO + headroom * (CEIL_RATIO - FLOOR_RATIO);
            current += (target - current) * SMOOTH; // ease so the rate doesn't oscillate

            double lo = orDefault(ratio.getMinValue(), 0.01);
            double hi = orDefault(ratio.getMaxValue(), 1.0);
            double applied = Math.max(lo, Math.min(hi, current));
            ratio.setValue(applied);
        } catch (Throwable t) {
            broken = true;
            DhSmooth.LOGGER.warn("[wnl_dhsmooth] thread governor disabled (DH API changed?): {}", t.toString());
        }
    }

    private static double orDefault(Double v, double def) {
        return (v != null) ? v : def;
    }
}
