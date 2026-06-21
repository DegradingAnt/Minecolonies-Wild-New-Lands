import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.nio.file.Files;
import java.nio.file.Path;

// Minimal: does uvfixes.js PARSE + does initializeCoreMod() expose Fix 50? (catches the
// catastrophic syntax-error case that would break ALL coremod fixes). No ASM — transformer
// bodies are not executed at eval, so no Opcodes/InsnList globals are needed.
public class TestJsParse {
    public static void main(String[] args) throws Exception {
        ScriptEngine engine = new org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory().getScriptEngine();
        // stub Java.type so the top-level `var X = Java.type('...')` lines return dummies — this
        // validates JS SYNTAX + the initializeCoreMod() structure without the real coremod/ASM env.
        engine.eval("var Java = { type: function(n){ return {}; } };");
        engine.eval(Files.readString(Path.of("_dev/wnl-packfixes-src/coremods/uvfixes.js")));
        System.out.println("[0] uvfixes.js evaluated WITHOUT error: PASS (JS syntax OK)");
        ScriptObjectMirror t = (ScriptObjectMirror) ((Invocable) engine).invokeFunction("initializeCoreMod");
        boolean has = t.containsKey("uvfixes_continuity_spriteloader_priority");
        System.out.println("[1] initializeCoreMod() entries=" + t.size()
                + " | Fix50 entry present=" + has);
        ScriptObjectMirror e = (ScriptObjectMirror) t.get("uvfixes_continuity_spriteloader_priority");
        Object target = e == null ? null : ((ScriptObjectMirror) e.get("target")).get("name");
        boolean fnOk = e != null && (e.get("transformer") instanceof ScriptObjectMirror);
        System.out.println("[2] Fix50 target=" + target + " | transformer-is-fn=" + fnOk);
        System.out.println(has && fnOk ? "\n==== JS PARSE + Fix50 PASS ====" : "\n==== FAIL ====");
    }
}
