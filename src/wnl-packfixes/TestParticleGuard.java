import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*; import java.nio.file.*; import java.util.zip.*;

// Offline test for Fix 45: HEAD null-check on ClientLevel.addParticle(ParticleOptions,Z,D6)V.
// Loads the REAL class from the mojmap (-srg) MC jar, applies the same transform the JS coremod does
// (ALOAD 1 / IFNONNULL cont / RETURN / cont at the method head), and re-serializes with COMPUTE_FRAMES.
// A clean write = the guarded method verifies (the only real risk for a HEAD insert).
public class TestParticleGuard {
    public static void main(String[] a) throws Exception {
        String DESC = "(Lnet/minecraft/core/particles/ParticleOptions;ZDDDDDD)V";
        byte[] bytes;
        try (ZipFile zf = new ZipFile(a[0])) {
            ZipEntry e = zf.getEntry("net/minecraft/client/multiplayer/ClientLevel.class");
            if (e == null) { System.out.println("FAIL: ClientLevel.class not in jar"); return; }
            try (InputStream is = zf.getInputStream(e)) { bytes = is.readAllBytes(); }
        }
        ClassNode cn = new ClassNode();
        new ClassReader(bytes).accept(cn, 0);

        MethodNode m = null;
        for (MethodNode mm : cn.methods) if (mm.name.equals("addParticle") && mm.desc.equals(DESC)) m = mm;
        if (m == null) { System.out.println("FAIL: addParticle" + DESC + " not found (mappings changed?)"); return; }

        int insnBefore = m.instructions.size();

        // ---- replicate the Fix 45 transform exactly ----
        InsnList list = new InsnList();
        LabelNode cont = new LabelNode();
        list.add(new VarInsnNode(Opcodes.ALOAD, 1));
        list.add(new JumpInsnNode(Opcodes.IFNONNULL, cont));
        list.add(new InsnNode(Opcodes.RETURN));
        list.add(cont);
        m.instructions.insert(list);
        if (m.maxStack < 1) m.maxStack = 1;

        System.out.println("addParticle: insns " + insnBefore + "->" + m.instructions.size()
                + (m.instructions.size() == insnBefore + 4 ? "   (+4 PASS)" : "   FAIL"));

        // ---- the real check: COMPUTE_FRAMES must re-serialize the guarded method cleanly ----
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES) {
            @Override protected String getCommonSuperClass(String x, String y) { return "java/lang/Object"; }
        };
        try {
            cn.accept(cw);
            byte[] out = cw.toByteArray();
            System.out.println("COMPUTE_FRAMES re-serialize: OK (" + out.length + " bytes)   PASS");
        } catch (Throwable t) {
            System.out.println("COMPUTE_FRAMES re-serialize: THREW -> " + t);
            System.out.println("   FAIL");
        }
    }
}
