import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.nio.file.Files;
import java.nio.file.Path;

// Offline test for PackFixes Fix 51: guard knightlib GreatChaliceRecipe.<init> so the unbound
// EMPTY_GRAIL/FILLED_GRAIL .get() can't throw (ExceptionInInitializerError cascade -> boot crash).
public class TestKnightLib {
    static final String JAR = "mods/knightlib-neoforge-1.21.1-1.5.3.jar";
    static final String CLS = "dev/xylonity/knightlib/common/recipe/GreatChaliceRecipe.class";

    // COMPUTE_FRAMES writer that never needs the full MC classpath (our handler frame is trivial).
    static class SafeWriter extends ClassWriter {
        SafeWriter(int f) { super(f); }
        @Override protected String getCommonSuperClass(String a, String b) {
            try { return super.getCommonSuperClass(a, b); } catch (Throwable t) { return "java/lang/Object"; }
        }
    }

    static int tcbOfInit(ClassNode cn) {
        for (MethodNode m : cn.methods)
            if (m.name.equals("<init>") && m.desc.equals("()V"))
                return m.tryCatchBlocks == null ? 0 : m.tryCatchBlocks.size();
        return -1;
    }

    public static void main(String[] args) throws Exception {
        // FAITHFUL sandbox: reproduce the coremod Nashorn ClassFilter EXACTLY.
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
        engine.eval("log = function(s){ print('  [coremod] ' + s); };");
        System.out.println("[0] uvfixes.js evaluated under FAITHFUL ClassFilter: PASS");
        Object blocked = engine.eval("var r; try { Java.type('java.lang.Integer'); r='RESOLVED'; } catch(e){ r='BLOCKED'; } r;");
        System.out.println("[0a] Java.type('java.lang.Integer') = " + blocked + ("BLOCKED".equals(blocked) ? " (faithful: PASS)" : " (NOT faithful: FAIL)"));
        ScriptObjectMirror transformers = (ScriptObjectMirror) ((Invocable) engine).invokeFunction("initializeCoreMod");
        System.out.println("[0b] initializeCoreMod() entries=" + transformers.size());

        byte[] bytes;
        try (java.util.zip.ZipFile zf = new java.util.zip.ZipFile(JAR)) {
            java.util.zip.ZipEntry e = zf.getEntry(CLS);
            bytes = zf.getInputStream(e).readAllBytes();
        }
        ClassNode in = new ClassNode();
        new ClassReader(bytes).accept(in, 0);
        int before = tcbOfInit(in);
        System.out.println("[1] GreatChaliceRecipe.<init>()V tryCatchBlocks BEFORE = " + before);

        ScriptObjectMirror entry = (ScriptObjectMirror) transformers.get("uvfixes_knightlib_chalice_ctor");
        if (entry == null) { System.out.println("FAIL: missing entry uvfixes_knightlib_chalice_ctor"); return; }
        ScriptObjectMirror fn = (ScriptObjectMirror) entry.get("transformer");
        ClassNode out = (ClassNode) fn.call(entry, in);
        int after = tcbOfInit(out);
        System.out.println("[2] GreatChaliceRecipe.<init>()V tryCatchBlocks AFTER  = " + after);

        // verify the handler installs the EMPTY-fallback putfields
        int emptyGets = 0, putInput = 0, putOutput = 0;
        for (MethodNode m : out.methods) if (m.name.equals("<init>") && m.desc.equals("()V"))
            for (AbstractInsnNode n : m.instructions.toArray()) {
                if (n instanceof FieldInsnNode f) {
                    if (f.getOpcode()==Opcodes.GETSTATIC && f.owner.equals("net/minecraft/world/item/ItemStack") && f.name.equals("EMPTY")) emptyGets++;
                    if (f.getOpcode()==Opcodes.PUTFIELD && f.name.equals("input")) putInput++;
                    if (f.getOpcode()==Opcodes.PUTFIELD && f.name.equals("output")) putOutput++;
                }
            }
        System.out.println("[3] handler: ItemStack.EMPTY gets=" + emptyGets + " (>=2), putInput=" + putInput + " putOutput=" + putOutput);

        boolean writes = false;
        try { SafeWriter cw = new SafeWriter(ClassWriter.COMPUTE_FRAMES); out.accept(cw); cw.toByteArray(); writes = true; }
        catch (Throwable t) { System.out.println("  COMPUTE_FRAMES write error: " + t); }
        System.out.println("[4] re-serialize (COMPUTE_FRAMES) = " + writes);

        boolean pass = before == 0 && after == 1 && emptyGets >= 2 && putInput >= 1 && putOutput >= 1 && writes;
        System.out.println(pass ? "\n==== Fix51 PASS (ctor guarded, frames recompute clean) ====" : "\n==== Fix51 FAIL ====");
    }
}
