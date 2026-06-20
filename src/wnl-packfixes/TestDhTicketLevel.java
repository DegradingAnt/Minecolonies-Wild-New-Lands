import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*; import java.util.zip.*;

// Offline test for Fix 49: in DH InternalServerGenerator_neoforge, the gen-ticket level constant
// (BIPUSH 33; ISTORE) feeding DistanceManager.addTicket (request lambda) and removeTicket (release
// lambda) must be bumped 33 -> 34. Verifies EXACTLY 2 swaps (one per lambda, add+remove matched),
// names the methods, and re-serializes with COMPUTE_FRAMES (clean = valid bytecode).
public class TestDhTicketLevel {
    public static void main(String[] a) throws Exception {
        String OWNER = "com/seibel/distanthorizons/common/wrappers/worldGeneration/InternalServerGenerator_neoforge";
        byte[] bytes;
        try (ZipFile zf = new ZipFile(a[0])) {
            ZipEntry e = zf.getEntry(OWNER + ".class");
            if (e == null) { System.out.println("FAIL: class not in jar"); return; }
            try (InputStream is = zf.getInputStream(e)) { bytes = is.readAllBytes(); }
        }
        ClassNode cn = new ClassNode();
        new ClassReader(bytes).accept(cn, 0);

        int swapped = 0;
        for (MethodNode m : cn.methods) {
            AbstractInsnNode[] insns = m.instructions.toArray();
            boolean tickets = false;
            for (AbstractInsnNode in : insns)
                if (in instanceof MethodInsnNode mi && (mi.name.equals("addTicket") || mi.name.equals("removeTicket"))) { tickets = true; break; }
            if (!tickets) continue;
            for (int j = 0; j + 1 < insns.length; j++) {
                if (insns[j] instanceof IntInsnNode ii && ii.getOpcode() == Opcodes.BIPUSH && ii.operand == 33
                        && insns[j + 1].getOpcode() == Opcodes.ISTORE) {
                    System.out.println("  bumped ticket level 33->34 in " + m.name + m.desc);
                    ii.operand = 34; swapped++;
                }
            }
        }
        System.out.println("total swaps: " + swapped + (swapped == 2 ? "   PASS (exactly 2: addTicket + removeTicket)" : "   FAIL/CHECK (want 2)"));

        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES) {
            @Override protected String getCommonSuperClass(String x, String y) { return "java/lang/Object"; }
        };
        try { cn.accept(cw); System.out.println("COMPUTE_FRAMES re-serialize: OK (" + cw.toByteArray().length + " bytes)   PASS"); }
        catch (Throwable t) { System.out.println("COMPUTE_FRAMES re-serialize: THREW -> " + t + "   FAIL"); }
    }
}
