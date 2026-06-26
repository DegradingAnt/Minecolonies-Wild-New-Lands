package com.wnl.dhsmooth;

import net.neoforged.fml.common.Mod;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

/**
 * Smooths Distant Horizons LOD draw-batch spikes WITHOUT lowering graphics.
 *
 * DH builds + uploads LOD render buffers async; when a batch finishes, the next
 * frame's near->far draw list jumps and that one frame draws all the new geometry
 * at once -> on a GPU already saturated by DH-through-shaders, a multi-hundred-ms
 * hitch. This caps how many GENUINELY-NEW (just-built) buffers join the draw per
 * frame so a batch fades in over a few frames instead of one.
 *
 * v1.1.0: terrain shown within the last {@code rememberFrames} frames is brought
 * back INSTANTLY (no ramp) -- so turning the camera around, or re-entering a view
 * you just had, shows immediately (those LODs are already on the GPU; there is no
 * spike to smooth). Only never-recently-seen geometry is ramped. The per-frame
 * admit rate is adaptive: it scales up with the new-buffer backlog (capped) so
 * exploring into fresh terrain fills in fast while a lone batch still eases in.
 * Quality-neutral: identical pixels, nothing lowered.
 *
 * config/wnl_dhsmooth.properties:
 *   enabled=true
 *   newBuffersPerFrame=16   base admit rate for brand-new LODs (higher = faster fill-in)
 *   maxBuffersPerFrame=64   adaptive cap when exploring (a big backlog admits up to this)
 *   rememberFrames=200      how long (frames) a shown LOD is remembered -> instant on return
 *   adaptive=true           scale the admit rate with the backlog
 */
@Mod("wnl_dhsmooth")
public class DhSmooth {
    public static final Logger LOGGER = LogManager.getLogger("wnl_dhsmooth");

    public static volatile boolean ENABLED = true;
    public static volatile boolean ADAPTIVE = true;
    public static volatile int NEW_BUFFERS_PER_FRAME = 16;
    public static volatile int MAX_BUFFERS_PER_FRAME = 64;
    public static volatile int REMEMBER_FRAMES = 200;

    public DhSmooth() {
        loadConfig();
        LOGGER.info("[wnl_dhsmooth] loaded — DH LOD draw-batch smoothing (enabled={}, new/frame={}, max/frame={}, remember={}f, adaptive={})",
                ENABLED, NEW_BUFFERS_PER_FRAME, MAX_BUFFERS_PER_FRAME, REMEMBER_FRAMES, ADAPTIVE);
        // Adaptive worker-thread governor: scale DH's worker run-time ratio by live FPS so chunk
        // generation stops starving the render thread. Game-bus (client) listener; never throws.
        try {
            net.neoforged.neoforge.common.NeoForge.EVENT_BUS.addListener(
                    (net.neoforged.neoforge.client.event.ClientTickEvent.Post e) -> DhThreadGovernor.onClientTick());
            LOGGER.info("[wnl_dhsmooth] adaptive thread governor registered (enabled={}, good={}fps, bad={}fps, ratio {}–{})",
                    DhThreadGovernor.ENABLED, DhThreadGovernor.GOOD_FPS, DhThreadGovernor.BAD_FPS,
                    DhThreadGovernor.FLOOR_RATIO, DhThreadGovernor.CEIL_RATIO);
        } catch (Throwable t) {
            LOGGER.warn("[wnl_dhsmooth] governor registration failed: {}", t.toString());
        }
    }

    private static int clampInt(String v, int def, int lo, int hi) {
        try {
            return Math.max(lo, Math.min(hi, Integer.parseInt(v.trim())));
        } catch (Exception e) {
            return def;
        }
    }

    private static double clampDouble(String v, double def, double lo, double hi) {
        try {
            return Math.max(lo, Math.min(hi, Double.parseDouble(v.trim())));
        } catch (Exception e) {
            return def;
        }
    }

    private static void loadConfig() {
        Path f = Path.of("config", "wnl_dhsmooth.properties");
        try {
            if (Files.isRegularFile(f)) {
                Properties p = new Properties();
                try (var in = Files.newInputStream(f)) {
                    p.load(in);
                }
                ENABLED = Boolean.parseBoolean(p.getProperty("enabled", "true").trim());
                ADAPTIVE = Boolean.parseBoolean(p.getProperty("adaptive", "true").trim());
                NEW_BUFFERS_PER_FRAME = clampInt(p.getProperty("newBuffersPerFrame", "16"), 16, 1, 4096);
                MAX_BUFFERS_PER_FRAME = clampInt(p.getProperty("maxBuffersPerFrame", "64"), 64, NEW_BUFFERS_PER_FRAME, 8192);
                REMEMBER_FRAMES = clampInt(p.getProperty("rememberFrames", "200"), 200, 0, 100000);
                DhThreadGovernor.ENABLED = Boolean.parseBoolean(p.getProperty("governor", "true").trim());
                DhThreadGovernor.GOOD_FPS = clampDouble(p.getProperty("governorGoodFps", "70"), 70, 15, 1000);
                DhThreadGovernor.BAD_FPS = clampDouble(p.getProperty("governorBadFps", "45"), 45, 5, 999);
                DhThreadGovernor.FLOOR_RATIO = clampDouble(p.getProperty("governorFloorRatio", "0.10"), 0.10, 0.01, 1.0);
                DhThreadGovernor.CEIL_RATIO = clampDouble(p.getProperty("governorCeilRatio", "1.00"), 1.00, 0.05, 1.0);
                DhThreadGovernor.SMOOTH = clampDouble(p.getProperty("governorSmooth", "0.20"), 0.20, 0.01, 1.0);
                return;
            }
            Files.createDirectories(f.getParent());
            Files.writeString(f, "# UltimateVibes DH LOD draw-batch smoothing\n"
                    + "enabled=true\n"
                    + "# Base number of brand-new distant-LOD buffers drawn per frame.\n"
                    + "# Higher = new terrain fills in faster but bigger draw spikes. 8-32 sensible.\n"
                    + "newBuffersPerFrame=16\n"
                    + "# Adaptive cap: when exploring (big backlog) the rate rises up to this.\n"
                    + "maxBuffersPerFrame=64\n"
                    + "# How long (in frames) a shown LOD is remembered so it returns INSTANTLY\n"
                    + "# (turning around / re-entering a view). ~200 = a couple seconds.\n"
                    + "rememberFrames=200\n"
                    + "adaptive=true\n"
                    + "\n"
                    + "# --- Adaptive DH worker-thread governor (smooths FPS during chunk generation) ---\n"
                    + "# DH's LOD/world-gen workers compete with Sodium + worldgen for CPU; under load that\n"
                    + "# starves the render thread. This scales DH's worker run-time ratio by your live FPS:\n"
                    + "# full speed when FPS is high, throttled when it dips. LOD quality/range NEVER change.\n"
                    + "governor=true\n"
                    + "# At/above this FPS, DH runs at governorCeilRatio (full speed).\n"
                    + "governorGoodFps=70\n"
                    + "# At/below this FPS, DH is throttled to governorFloorRatio.\n"
                    + "governorBadFps=45\n"
                    + "# Min/max DH worker run-time ratio (fraction of time workers run vs sleep).\n"
                    + "governorFloorRatio=0.10\n"
                    + "governorCeilRatio=1.00\n"
                    + "# Easing per update (0..1) so the rate doesn't oscillate.\n"
                    + "governorSmooth=0.20\n");
        } catch (Throwable t) {
            LOGGER.warn("[wnl_dhsmooth] config load failed, using defaults: {}", t.toString());
        }
    }
}
