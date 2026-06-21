import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

// Offline test for PackFixes Fix 50: lower Continuity SpriteLoaderMixin @Mixin priority 1000 -> 800.
public class TestFix50 {
    static final String MIXIN_DESC = "Lorg/spongepowered/asm/mixin/Mixin;";
    static final String CLASS_PATH = ".uvrun/sl_test/me/pepperbell/continuity/client/mixin/SpriteLoaderMixin.class";

    static Integer priorityOf(ClassNode cn) {
        if (cn.invisibleAnnotations == null) return null;
        for (AnnotationNode a : cn.invisibleAnnotations) {
            if (!a.desc.equals(MIXIN_DESC)) continue;
            List<Object> v = a.values;
            if (v == null) return null;
            for (int j = 0; j + 1 < v.size(); j += 2)
                if ("priority".equals(v.get(j))) return (Integer) v.get(j + 1);
            return null; // @Mixin present but no explicit priority (defaults to 1000)
        }
        return null;
    }

    public static void main(String[] args) throws Exception {
        // FAITHFUL sandbox: reproduce the coremod's Nashorn ClassFilter EXACTLY
        // (net.neoforged.coremod.CoreModScriptingEngine.checkClass) — whitelist the java.util /
        // java.util.function / org.objectweb.asm.util packages + a fixed class set. Running Nashorn
        // WITHOUT this filter is precisely what masked all THREE java.lang.Integer gotchas.
        final java.util.Set<String> WL_CLASSES = java.util.Set.of(
            "net.neoforged.coremod.api.ASMAPI",
            "org.objectweb.asm.Attribute","org.objectweb.asm.Handle","org.objectweb.asm.Label",
            "org.objectweb.asm.Opcodes","org.objectweb.asm.Type","org.objectweb.asm.TypePath",
            "org.objectweb.asm.TypeReference",
            "org.objectweb.asm.tree.AbstractInsnNode","org.objectweb.asm.tree.FieldInsnNode",
            "org.objectweb.asm.tree.FieldNode","org.objectweb.asm.tree.FrameNode",
            "org.objectweb.asm.tree.IincInsnNode","org.objectweb.asm.tree.InsnList",
            "org.objectweb.asm.tree.InsnNode","org.objectweb.asm.tree.IntInsnNode",
            "org.objectweb.asm.tree.InvokeDynamicInsnNode","org.objectweb.asm.tree.JumpInsnNode",
            "org.objectweb.asm.tree.LabelNode","org.objectweb.asm.tree.LdcInsnNode",
            "org.objectweb.asm.tree.LineNumberNode","org.objectweb.asm.tree.LocalVariableAnnotationNode",
            "org.objectweb.asm.tree.LocalVariableNode","org.objectweb.asm.tree.LookupSwitchInsnNode",
            "org.objectweb.asm.tree.MethodInsnNode","org.objectweb.asm.tree.MethodNode",
            "org.objectweb.asm.tree.MultiANewArrayInsnNode","org.objectweb.asm.tree.ParameterNode",
            "org.objectweb.asm.tree.TableSwitchInsnNode","org.objectweb.asm.tree.TryCatchBlockNode",
            "org.objectweb.asm.tree.TypeAnnotationNode","org.objectweb.asm.tree.TypeInsnNode",
            "org.objectweb.asm.tree.VarInsnNode");
        final java.util.Set<String> WL_PKGS = java.util.Set.of("java.util","java.util.function","org.objectweb.asm.util");
        org.openjdk.nashorn.api.scripting.ClassFilter filter = name -> {
            if (WL_CLASSES.contains(name)) return true;
            int dot = name.lastIndexOf('.');
            return dot != -1 && WL_PKGS.contains(name.substring(0, dot));
        };
        ScriptEngine engine = new org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory()
            .getScriptEngine(new String[]{"--language=es6"}, ClassLoader.getSystemClassLoader(), filter);
        engine.eval(Files.readString(Path.of("_dev/wnl-packfixes-src/coremods/uvfixes.js")));
        engine.eval("log = function(s){ print('  [coremod] ' + s); };"); // built-in print (java.lang.System is filtered out)
        System.out.println("[0] uvfixes.js evaluated under FAITHFUL ClassFilter WITHOUT error: PASS");
        // Negative control: the filter MUST block java.lang.Integer exactly as the runtime sandbox does,
        // otherwise the whole test is a lie (a non-faithful filter is what hid the bug 3 times).
        Object blocked = engine.eval("var r; try { Java.type('java.lang.Integer'); r='RESOLVED'; } catch(e){ r='BLOCKED'; } r;");
        boolean faithful = "BLOCKED".equals(blocked);
        System.out.println("[0a] Java.type('java.lang.Integer') under filter = " + blocked
            + (faithful ? "  (faithful sandbox: PASS)" : "  (NOT faithful: FAIL)"));
        ScriptObjectMirror transformers =
            (ScriptObjectMirror) ((Invocable) engine).invokeFunction("initializeCoreMod");
        System.out.println("[0b] initializeCoreMod() entries=" + transformers.size());

        ClassNode in = new ClassNode();
        new ClassReader(Files.readAllBytes(Path.of(CLASS_PATH))).accept(in, 0);
        Integer before = priorityOf(in);
        System.out.println("[1] SpriteLoaderMixin priority BEFORE = " + before + " (null = default 1000)");

        ScriptObjectMirror entry = (ScriptObjectMirror) transformers.get("uvfixes_continuity_spriteloader_priority");
        if (entry == null) { System.out.println("FAIL: missing entry uvfixes_continuity_spriteloader_priority"); return; }
        ScriptObjectMirror fn = (ScriptObjectMirror) entry.get("transformer");
        ClassNode out = (ClassNode) fn.call(entry, in);

        Integer after = priorityOf(out);
        System.out.println("[2] SpriteLoaderMixin priority AFTER  = " + after);

        boolean writes = false;
        try {
            ClassWriter cw = new ClassWriter(0); // annotation-only change: no frame/maxs recompute needed
            out.accept(cw); writes = true;
        } catch (Throwable t) { System.out.println("  write error: " + t); }

        boolean pass = after != null && after == 800 && writes;
        System.out.println("[3] re-serialize = " + writes);
        System.out.println(pass ? "\n==== Fix50 PASS (priority -> 800) ====" : "\n==== Fix50 FAIL ====");
    }
}
