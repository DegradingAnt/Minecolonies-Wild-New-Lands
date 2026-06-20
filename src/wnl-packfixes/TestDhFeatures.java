import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*; import java.util.zip.*;

// Offline test for Fix 48: in DH InternalServerGenerator_neoforge, swap the GETSTATIC
//   ChunkStatus.FULL that feeds ChunkHolder.scheduleChunkGenerationTask  ->  ChunkStatus.FEATURES
// (reverts DH eb82ab14). Loads the REAL class from the DH jar, applies the same transform the JS
// coremod does, verifies exactly one swap, and re-serializes with COMPUTE_FRAMES (clean = valid).
public class TestDhFeatures {
    public static void main(String[] a) throws Exception {
        String OWNER = "com/seibel/distanthorizons/common/wrappers/worldGeneration/InternalServerGenerator_neoforge";
        String CS = "net/minecraft/world/level/chunk/status/ChunkStatus";
        String CSDESC = "Lnet/minecraft/world/level/chunk/status/ChunkStatus;";
        byte[] bytes;
        try (ZipFile zf = new ZipFile(a[0])) {
            ZipEntry e = zf.getEntry(OWNER + ".class");
            if (e == null) { System.out.println("FAIL: " + OWNER + ".class not in jar"); return; }
            try (InputStream is = zf.getInputStream(e)) { bytes = is.readAllBytes(); }
        }
        ClassNode cn = new ClassNode();
        new ClassReader(bytes).accept(cn, 0);

        int fullSeen = 0, swapped = 0;
        for (MethodNode m : cn.methods) {
            AbstractInsnNode[] insns = m.instructions.toArray();
            for (int j = 0; j < insns.length; j++) {
                if (!(insns[j] instanceof FieldInsnNode)) continue;
                FieldInsnNode f = (FieldInsnNode) insns[j];
                if (f.getOpcode() != Opcodes.GETSTATIC) continue;
                if (!f.owner.equals(CS) || !f.name.equals("FULL") || !f.desc.equals(CSDESC)) continue;
                fullSeen++;
                boolean feedsGen = false;
                for (int k = j + 1; k < insns.length && k < j + 15; k++) {
                    if (insns[k] instanceof MethodInsnNode) {
                        MethodInsnNode mi = (MethodInsnNode) insns[k];
                        if (mi.name.equals("scheduleChunkGenerationTask") || mi.name.equals("getOrScheduleFuture")) { feedsGen = true; break; }
                    }
                }
                if (feedsGen) { System.out.println("  FULL gen-request found in " + m.name + m.desc); f.name = "FEATURES"; swapped++; }
            }
        }
        System.out.println("total ChunkStatus.FULL GETSTATIC in class: " + fullSeen + " (want 1, scoped)");
        System.out.println("swapped FULL->FEATURES: " + swapped + (swapped == 1 ? "   PASS (exactly 1)" : "   FAIL/CHECK"));

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
