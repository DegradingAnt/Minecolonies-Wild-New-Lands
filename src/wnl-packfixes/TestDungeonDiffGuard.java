import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

// Offline test for PackFixes Fix 62: uvfixes_dungeondiff_nonblocking_structure_lookup.
// Loads dungeon_difficulty's PatternMatching$LocationData, runs the REAL JS transformer through the same
// Nashorn ClassFilter sandbox as runtime, asserts a non-blocking ServerLevel.hasChunkAt(BlockPos) guard was
// inserted in matches(Filters,ServerLevel) (with the blocking startsForStructure preserved, not removed),
// and that the class re-serializes under COMPUTE_FRAMES -- which validates the inserted IFEQ + the stack-map
// frame at its jump target (the convergence label before `new Match`).
public class TestDungeonDiffGuard {
    static final String JAR = "mods/dungeon_difficulty-neoforge-3.6.10+1.21.1.jar";
    static final String CLS = "net/dungeon_difficulty/logic/PatternMatching$LocationData.class";
    static final String MATCH_DESC = "(Lnet/dungeon_difficulty/config/Config$Zone$Filters;Lnet/minecraft/server/level/ServerLevel;)Lnet/dungeon_difficulty/logic/PatternMatching$LocationData$Match;";

    static byte[] fromJar(String jar, String entry) throws Exception {
        try (ZipFile z = new ZipFile(jar)) {
            ZipEntry e = z.getEntry(entry);
            if (e == null) throw new RuntimeException("entry not found: " + entry);
            try (InputStream in = z.getInputStream(e)) { return in.readAllBytes(); }
        }
    }
    static ClassNode read(byte[] b) { ClassNode cn = new ClassNode(); new ClassReader(b).accept(cn, 0); return cn; }
    static final class SafeCW extends ClassWriter {
        SafeCW(int f) { super(f); }
        @Override protected String getCommonSuperClass(String a, String b) {
            try { return super.getCommonSuperClass(a, b); } catch (Throwable t) { return "java/lang/Object"; }
        }
    }
    static boolean verify(ClassNode cn) {
        try { ClassWriter cw = new SafeCW(ClassWriter.COMPUTE_FRAMES | ClassWriter.COMPUTE_MAXS); cn.accept(cw); return true; }
        catch (Throwable t) { System.out.println("    VERIFY/WRITE ERROR: " + t); return false; }
    }
    // in matches(Filters,ServerLevel): count the inserted hasChunkAt guard + the preserved startsForStructure
    static int[] counts(ClassNode cn) {
        int hca = 0, sfs = 0;
        for (MethodNode m : cn.methods) {
            if (!(m.name.equals("matches") && m.desc.equals(MATCH_DESC))) continue;
            for (AbstractInsnNode i : m.instructions.toArray()) {
                if (i instanceof MethodInsnNode mi && mi.getOpcode() == Opcodes.INVOKEVIRTUAL
                    && mi.owner.equals("net/minecraft/server/level/ServerLevel") && mi.name.equals("hasChunkAt")) hca++;
                if (i instanceof MethodInsnNode mi2 && mi2.name.equals("startsForStructure")) sfs++;
            }
        }
        return new int[]{hca, sfs};
    }

    public static void main(String[] args) throws Exception {
        java.util.Set<String> WL_CLASSES = java.util.Set.of(
            "net.neoforged.coremod.api.ASMAPI",
            "org.objectweb.asm.Attribute","org.objectweb.asm.Handle","org.objectweb.asm.Label",
            "org.objectweb.asm.Opcodes","org.objectweb.asm.Type","org.objectweb.asm.TypePath",
            "org.objectweb.asm.TypeReference","org.objectweb.asm.tree.AbstractInsnNode",
            "org.objectweb.asm.tree.FieldInsnNode","org.objectweb.asm.tree.FieldNode","org.objectweb.asm.tree.FrameNode",
            "org.objectweb.asm.tree.IincInsnNode","org.objectweb.asm.tree.InsnList","org.objectweb.asm.tree.InsnNode",
            "org.objectweb.asm.tree.IntInsnNode","org.objectweb.asm.tree.InvokeDynamicInsnNode","org.objectweb.asm.tree.JumpInsnNode",
            "org.objectweb.asm.tree.LabelNode","org.objectweb.asm.tree.LdcInsnNode","org.objectweb.asm.tree.LineNumberNode",
            "org.objectweb.asm.tree.LocalVariableAnnotationNode","org.objectweb.asm.tree.LocalVariableNode",
            "org.objectweb.asm.tree.LookupSwitchInsnNode","org.objectweb.asm.tree.MethodInsnNode","org.objectweb.asm.tree.MethodNode",
            "org.objectweb.asm.tree.MultiANewArrayInsnNode","org.objectweb.asm.tree.ParameterNode",
            "org.objectweb.asm.tree.TableSwitchInsnNode","org.objectweb.asm.tree.TryCatchBlockNode",
            "org.objectweb.asm.tree.TypeAnnotationNode","org.objectweb.asm.tree.TypeInsnNode","org.objectweb.asm.tree.VarInsnNode");
        java.util.Set<String> WL_PKGS = java.util.Set.of("java.util","java.util.function","org.objectweb.asm.util");
        org.openjdk.nashorn.api.scripting.ClassFilter filter = name -> {
            if (WL_CLASSES.contains(name)) return true;
            int dot = name.lastIndexOf('.');
            return dot != -1 && WL_PKGS.contains(name.substring(0, dot));
        };
        ScriptEngine engine = new org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory()
            .getScriptEngine(new String[]{"--language=es6"}, ClassLoader.getSystemClassLoader(), filter);
        engine.eval(Files.readString(Path.of("_dev/wnl-packfixes-src/coremods/uvfixes.js")));
        engine.eval("log = function(s){ print('    [coremod] ' + s); };");
        ScriptObjectMirror T = (ScriptObjectMirror) ((Invocable) engine).invokeFunction("initializeCoreMod");

        ClassNode cn = read(fromJar(JAR, CLS));
        int[] before = counts(cn);

        ScriptObjectMirror entry = (ScriptObjectMirror) T.get("uvfixes_dungeondiff_nonblocking_structure_lookup");
        if (entry == null) { System.out.println("FAIL: Fix 62 entry missing"); return; }
        ((ScriptObjectMirror) entry.get("transformer")).call(entry, cn);

        int[] after = counts(cn);
        boolean verified = verify(cn);

        System.out.println("hasChunkAt INVOKEVIRTUAL (inserted guard): " + before[0] + " -> " + after[0]);
        System.out.println("startsForStructure calls (preserved):     " + before[1] + " -> " + after[1]);
        System.out.println("COMPUTE_FRAMES re-serialize:               " + (verified ? "OK" : "FAILED"));
        boolean ok = before[0] == 0 && after[0] == 1 && before[1] == 1 && after[1] == 1 && verified;
        System.out.println("\n==== TestDungeonDiffGuard: " + (ok ? "PASS ====" : "FAIL ===="));
    }
}
