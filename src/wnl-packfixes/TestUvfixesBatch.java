import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

// Offline test for PackFixes 1.42.0 Fixes 55-57 + the quark modelBake UOE-guard.
// Faithfully reproduces the coremod Nashorn ClassFilter, loads uvfixes.js, applies each new
// transformer to its REAL target class (from the jars), asserts the intended change, and
// re-serializes with COMPUTE_FRAMES (Object-fallback super resolver) to verify the bytecode.
public class TestUvfixesBatch {
    static final String INSTALL = "C:/Users/linde/curseforge/minecraft/Install";
    static final String SRG = INSTALL + "/libraries/net/minecraft/client/1.21.1-20240808.144430/client-1.21.1-20240808.144430-srg.jar";

    static byte[] fromJar(String jar, String entry) throws Exception {
        try (ZipFile z = new ZipFile(jar)) {
            ZipEntry e = z.getEntry(entry);
            if (e == null) throw new RuntimeException("entry not found: " + entry + " in " + jar);
            try (InputStream in = z.getInputStream(e)) { return in.readAllBytes(); }
        }
    }
    static ClassNode read(byte[] b) { ClassNode cn = new ClassNode(); new ClassReader(b).accept(cn, 0); return cn; }
    static MethodNode method(ClassNode cn, String name) {
        for (MethodNode m : cn.methods) if (m.name.equals(name)) return m;
        return null;
    }
    static MethodNode methodStarts(ClassNode cn, String pfx, String desc) {
        for (MethodNode m : cn.methods) if (m.name.startsWith(pfx) && m.desc.equals(desc)) return m;
        return null;
    }
    static final class SafeCW extends ClassWriter {
        SafeCW(int f) { super(f); }
        @Override protected String getCommonSuperClass(String a, String b) {
            try { return super.getCommonSuperClass(a, b); } catch (Throwable t) { return "java/lang/Object"; }
        }
    }
    static boolean verify(ClassNode cn, String tag) {
        try { ClassWriter cw = new SafeCW(ClassWriter.COMPUTE_FRAMES | ClassWriter.COMPUTE_MAXS); cn.accept(cw); return true; }
        catch (Throwable t) { System.out.println("    [" + tag + "] VERIFY/WRITE ERROR: " + t); return false; }
    }
    static int countLdc(MethodNode m, String s) {
        int n = 0; for (AbstractInsnNode i : m.instructions.toArray())
            if (i instanceof LdcInsnNode && s.equals(((LdcInsnNode) i).cst)) n++;
        return n;
    }
    static int countInvoke(MethodNode m, String owner, String name) {
        int n = 0; for (AbstractInsnNode i : m.instructions.toArray())
            if (i instanceof MethodInsnNode && ((MethodInsnNode) i).owner.equals(owner) && ((MethodInsnNode) i).name.equals(name)) n++;
        return n;
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
        System.out.println("[0] uvfixes.js evaluated under FAITHFUL ClassFilter: PASS");
        Object blocked = engine.eval("var r; try { Java.type('java.lang.Integer'); r='RESOLVED'; } catch(e){ r='BLOCKED'; } r;");
        System.out.println("[0a] java.lang.Integer = " + blocked + ("BLOCKED".equals(blocked) ? " (faithful: PASS)" : " (NOT faithful: FAIL)"));
        ScriptObjectMirror T = (ScriptObjectMirror) ((Invocable) engine).invokeFunction("initializeCoreMod");
        System.out.println("[0b] initializeCoreMod() entries = " + T.size());

        int pass = 0, total = 4;

        // --- Fix 55: citresewn empty prefix -> "/" ---
        {
            ClassNode cn = read(fromJar("mods/citresewn-neoforge-1.21.1-0.jar", "schm/shsupercm/citresewn/mixin/AbstractFileResourcePackMixin.class"));
            MethodNode m = method(cn, "citresewn$brokenpaths$parseMetadata");
            int emptyBefore = m == null ? -1 : countLdc(m, ""), slashBefore = m == null ? -1 : countLdc(m, "/");
            apply(T, "uvfixes_citresewn_brokenpaths_empty_prefix", cn);
            MethodNode m2 = method(cn, "citresewn$brokenpaths$parseMetadata");
            int emptyAfter = countLdc(m2, ""), slashAfter = countLdc(m2, "/");
            boolean ok = emptyBefore >= 1 && emptyAfter == 0 && slashAfter == slashBefore + emptyBefore && verify(cn, "citresewn");
            System.out.println("[55 citresewn] \"\" " + emptyBefore + "->" + emptyAfter + ", \"/\" " + slashBefore + "->" + slashAfter + " :: " + (ok ? "PASS" : "FAIL"));
            if (ok) pass++;
        }
        // --- quark modelBake UOE-guard (extension of uvfixes_quark_potato) ---
        {
            ClassNode cn = read(fromJar("mods/Quark-4.1-480.jar", "org/violetmoon/quark/addons/oddities/module/TinyPotatoModule$Client.class"));
            MethodNode m = method(cn, "modelBake");
            int tcbBefore = (m == null || m.tryCatchBlocks == null) ? -1 : m.tryCatchBlocks.size();
            apply(T, "uvfixes_quark_potato", cn);
            MethodNode m2 = method(cn, "modelBake");
            int tcbAfter = m2.tryCatchBlocks == null ? 0 : m2.tryCatchBlocks.size();
            boolean hasUoe = false;
            if (m2.tryCatchBlocks != null) for (TryCatchBlockNode t : m2.tryCatchBlocks) if ("java/lang/UnsupportedOperationException".equals(t.type)) hasUoe = true;
            boolean ok = m != null && tcbAfter == tcbBefore + 1 && hasUoe && verify(cn, "quark");
            System.out.println("[1b quark modelBake] tryCatch " + tcbBefore + "->" + tcbAfter + ", UOE-handler=" + hasUoe + " :: " + (ok ? "PASS" : "FAIL"));
            if (ok) pass++;
        }
        // --- Fix 56: ItemStack invalid-item log suppress (RETURN at head) ---
        {
            ClassNode cn = read(fromJar(SRG, "net/minecraft/world/item/ItemStack.class"));
            apply(T, "uvfixes_itemstack_invalid_item_log", cn);
            // find the lambda whose body LDCs the message + assert its first real insn is RETURN
            boolean ok = false;
            for (MethodNode m : cn.methods) {
                if (!(m.name.startsWith("lambda$parse$") && m.desc.equals("(Ljava/lang/String;)V"))) continue;
                if (countLdc(m, "Tried to load invalid item: '{}'") < 1) continue;
                AbstractInsnNode first = m.instructions.getFirst();
                ok = first != null && first.getOpcode() == Opcodes.RETURN;
                break;
            }
            ok = ok && verify(cn, "itemstack");
            System.out.println("[56 itemstack] first insn of invalid-item lambda = RETURN :: " + (ok ? "PASS" : "FAIL"));
            if (ok) pass++;
        }
        // --- Fix 57: AllTheLeaks ColoredMapHandler refs removed ---
        {
            String CMH = "net/mehvahdjukaar/supplementaries/common/misc/map_data/ColoredMapHandler";
            ClassNode cn = read(fromJar("mods/alltheleaks-1.1.9+1.21.1-neoforge.jar", "dev/uncandango/alltheleaks/leaks/common/mods/supplementaries/UntrackedIssue001.class"));
            MethodNode clr = method(cn, "clearRemaining"); MethodNode cl = method(cn, "<clinit>");
            int crBefore = clr == null ? -1 : countInvoke(clr, CMH, "clearIdCache");
            int cmhLdcBefore = 0; if (cl != null) for (AbstractInsnNode i : cl.instructions.toArray())
                if (i instanceof LdcInsnNode && ((LdcInsnNode) i).cst instanceof Type && ((Type) ((LdcInsnNode) i).cst).getInternalName().equals(CMH)) cmhLdcBefore++;
            apply(T, "uvfixes_alltheleaks_coloredmaphandler", cn);
            int crAfter = countInvoke(method(cn, "clearRemaining"), CMH, "clearIdCache");
            int cmhLdcAfter = 0; for (AbstractInsnNode i : method(cn, "<clinit>").instructions.toArray())
                if (i instanceof LdcInsnNode && ((LdcInsnNode) i).cst instanceof Type && ((Type) ((LdcInsnNode) i).cst).getInternalName().equals(CMH)) cmhLdcAfter++;
            boolean ok = crBefore == 1 && crAfter == 0 && cmhLdcBefore == 1 && cmhLdcAfter == 0 && verify(cn, "alltheleaks");
            System.out.println("[57 alltheleaks] clearRemaining-call " + crBefore + "->" + crAfter + ", <clinit>-classref " + cmhLdcBefore + "->" + cmhLdcAfter + " :: " + (ok ? "PASS" : "FAIL"));
            if (ok) pass++;
        }

        System.out.println("\n==== TestUvfixesBatch: " + pass + "/" + total + (pass == total ? " PASS ====" : " FAIL ===="));
    }

    static void apply(ScriptObjectMirror T, String key, ClassNode cn) {
        ScriptObjectMirror entry = (ScriptObjectMirror) T.get(key);
        if (entry == null) { System.out.println("  MISSING entry " + key); return; }
        ScriptObjectMirror fn = (ScriptObjectMirror) entry.get("transformer");
        fn.call(entry, cn);
    }
}
