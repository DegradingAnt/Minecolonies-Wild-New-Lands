import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*; import java.util.zip.*;

// Offline test for Fix 46: wrap structurize Blueprint.setRotationMirrorRelative(RotationMirror,Level)V body
// in try/catch(IllegalStateException)->return. Loads the REAL class from the structurize jar, applies the
// same transform the JS coremod does, and re-serializes with COMPUTE_FRAMES. A clean write = the wrapped
// method verifies (the only real risk). Arg: path to structurize jar.
public class TestWorldMismatchGuard {
    public static void main(String[] a) throws Exception {
        String DESC = "(Lcom/ldtteam/structurize/api/RotationMirror;Lnet/minecraft/world/level/Level;)V";
        byte[] bytes;
        try (ZipFile zf = new ZipFile(a[0])) {
            ZipEntry e = zf.getEntry("com/ldtteam/structurize/blueprints/v1/Blueprint.class");
            if (e == null) { System.out.println("FAIL: Blueprint.class not in jar"); return; }
            try (InputStream is = zf.getInputStream(e)) { bytes = is.readAllBytes(); }
        }
        ClassNode cn = new ClassNode();
        new ClassReader(bytes).accept(cn, 0);

        MethodNode m = null;
        for (MethodNode mm : cn.methods) if (mm.name.equals("setRotationMirrorRelative") && mm.desc.equals(DESC)) m = mm;
        if (m == null) { System.out.println("FAIL: setRotationMirrorRelative" + DESC + " not found (structurize changed?)"); return; }

        int tcBefore = m.tryCatchBlocks == null ? 0 : m.tryCatchBlocks.size();

        // ---- replicate the Fix 46 transform exactly ----
        LabelNode L_start = new LabelNode(), L_handler = new LabelNode();
        m.instructions.insert(L_start);
        m.instructions.add(L_handler);
        m.instructions.add(new InsnNode(Opcodes.POP));
        m.instructions.add(new InsnNode(Opcodes.RETURN));
        m.tryCatchBlocks.add(new TryCatchBlockNode(L_start, L_handler, L_handler, "java/lang/IllegalStateException"));
        if (m.maxStack < 2) m.maxStack = 2;

        int tcAfter = m.tryCatchBlocks.size();
        System.out.println("setRotationMirrorRelative: tryCatch " + tcBefore + "->" + tcAfter
                + (tcAfter == tcBefore + 1 ? "   (+1 PASS)" : "   FAIL"));

        // ---- the real check: COMPUTE_FRAMES must re-serialize the wrapped method cleanly ----
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
