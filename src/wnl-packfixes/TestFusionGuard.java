import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*; import java.util.zip.*;

// Offline test for Fix 47: HEAD guard on the STATIC method
//   FusionBlockModelData.containsFusionModelsOrTextures(BlockModel)Z
// Loads the REAL class from the fusion jar, applies the same transform the JS coremod does
//   GETSTATIC atlasStitchResults:Ljava/util/Map; / IFNONNULL cont / ICONST_0 / IRETURN / cont
// and re-serializes with COMPUTE_FRAMES. Clean write = the guarded method verifies.
public class TestFusionGuard {
    public static void main(String[] a) throws Exception {
        String OWNER = "com/supermartijn642/fusion/model/FusionBlockModelData";
        String DESC  = "(Lnet/minecraft/client/renderer/block/model/BlockModel;)Z";
        byte[] bytes;
        try (ZipFile zf = new ZipFile(a[0])) {
            ZipEntry e = zf.getEntry(OWNER + ".class");
            if (e == null) { System.out.println("FAIL: FusionBlockModelData.class not in jar"); return; }
            try (InputStream is = zf.getInputStream(e)) { bytes = is.readAllBytes(); }
        }
        ClassNode cn = new ClassNode();
        new ClassReader(bytes).accept(cn, 0);

        MethodNode m = null;
        for (MethodNode mm : cn.methods)
            if (mm.name.equals("containsFusionModelsOrTextures") && mm.desc.equals(DESC)) m = mm;
        if (m == null) { System.out.println("FAIL: containsFusionModelsOrTextures" + DESC + " not found"); return; }
        boolean isStatic = (m.access & Opcodes.ACC_STATIC) != 0;
        System.out.println("method found, static=" + isStatic);

        int insnBefore = m.instructions.size();

        // ---- replicate the Fix 47 transform exactly ----
        InsnList list = new InsnList();
        LabelNode cont = new LabelNode();
        list.add(new FieldInsnNode(Opcodes.GETSTATIC, OWNER, "atlasStitchResults", "Ljava/util/Map;"));
        list.add(new JumpInsnNode(Opcodes.IFNONNULL, cont));
        list.add(new InsnNode(Opcodes.ICONST_0));
        list.add(new InsnNode(Opcodes.IRETURN));
        list.add(cont);
        m.instructions.insert(list);
        if (m.maxStack < 1) m.maxStack = 1;

        System.out.println("insns " + insnBefore + "->" + m.instructions.size()
                + (m.instructions.size() == insnBefore + 5 ? "   (+5 PASS)" : "   FAIL"));

        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES) {
            @Override protected String getCommonSuperClass(String x, String y) { return "java/lang/Object"; }
        };
        try {
            cn.accept(cw);
            byte[] out = cw.toByteArray();
            System.out.println("COMPUTE_FRAMES re-serialize: OK (" + out.length + " bytes)   PASS");
        } catch (Throwable t) {
            System.out.println("COMPUTE_FRAMES re-serialize: THREW -> " + t + "   FAIL");
        }
    }
}
