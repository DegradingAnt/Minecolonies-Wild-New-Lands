import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.nio.file.Files;
import java.nio.file.Path;

// Offline test for PackFixes Fix 53: neutralise minecolonies ItemFood.getTooltipImage so it no
// longer references Minecraft/ClientLevel (the dedicated-server item-registry abort + cascade root).
public class TestItemFood {
    static final String JAR = "mods/minecolonies-1.1.1332-1.21.1-snapshot.jar";
    static final String CLS = "com/minecolonies/core/items/ItemFood.class";
    static final String MN = "getTooltipImage", MD = "(Lnet/minecraft/world/item/ItemStack;)Ljava/util/Optional;";

    static class SafeWriter extends ClassWriter {
        SafeWriter(int f){ super(f);}
        @Override protected String getCommonSuperClass(String a,String b){ try{return super.getCommonSuperClass(a,b);}catch(Throwable t){return "java/lang/Object";} }
    }
    static int clientRefsIn(ClassNode cn, String mn, String md) {
        int n=0;
        for (MethodNode m: cn.methods) if (m.name.equals(mn)&&m.desc.equals(md))
            for (AbstractInsnNode in: m.instructions.toArray()) {
                String s = in instanceof MethodInsnNode mi ? mi.owner : in instanceof FieldInsnNode fi ? fi.owner+" "+fi.desc : in instanceof TypeInsnNode ti ? ti.desc : "";
                if (s.contains("client/multiplayer/ClientLevel") || s.contains("client/Minecraft")) n++;
            }
        return n;
    }

    public static void main(String[] a) throws Exception {
        java.util.Set<String> WC = java.util.Set.of("net.neoforged.coremod.api.ASMAPI",
          "org.objectweb.asm.Attribute","org.objectweb.asm.Handle","org.objectweb.asm.Label","org.objectweb.asm.Opcodes","org.objectweb.asm.Type","org.objectweb.asm.TypePath","org.objectweb.asm.TypeReference",
          "org.objectweb.asm.tree.AbstractInsnNode","org.objectweb.asm.tree.FieldInsnNode","org.objectweb.asm.tree.FieldNode","org.objectweb.asm.tree.FrameNode","org.objectweb.asm.tree.IincInsnNode","org.objectweb.asm.tree.InsnList","org.objectweb.asm.tree.InsnNode","org.objectweb.asm.tree.IntInsnNode","org.objectweb.asm.tree.InvokeDynamicInsnNode","org.objectweb.asm.tree.JumpInsnNode","org.objectweb.asm.tree.LabelNode","org.objectweb.asm.tree.LdcInsnNode","org.objectweb.asm.tree.LineNumberNode","org.objectweb.asm.tree.LocalVariableAnnotationNode","org.objectweb.asm.tree.LocalVariableNode","org.objectweb.asm.tree.LookupSwitchInsnNode","org.objectweb.asm.tree.MethodInsnNode","org.objectweb.asm.tree.MethodNode","org.objectweb.asm.tree.MultiANewArrayInsnNode","org.objectweb.asm.tree.ParameterNode","org.objectweb.asm.tree.TableSwitchInsnNode","org.objectweb.asm.tree.TryCatchBlockNode","org.objectweb.asm.tree.TypeAnnotationNode","org.objectweb.asm.tree.TypeInsnNode","org.objectweb.asm.tree.VarInsnNode");
        java.util.Set<String> WP = java.util.Set.of("java.util","java.util.function","org.objectweb.asm.util");
        org.openjdk.nashorn.api.scripting.ClassFilter f = n -> { if (WC.contains(n)) return true; int d=n.lastIndexOf('.'); return d!=-1 && WP.contains(n.substring(0,d)); };
        ScriptEngine e = new org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory().getScriptEngine(new String[]{"--language=es6"}, ClassLoader.getSystemClassLoader(), f);
        e.eval(Files.readString(Path.of("_dev/wnl-packfixes-src/coremods/uvfixes.js")));
        e.eval("log = function(s){ print('  [coremod] ' + s); };");
        System.out.println("[0] uvfixes.js evaluated: PASS");
        System.out.println("[0a] Integer = " + e.eval("var r;try{Java.type('java.lang.Integer');r='RESOLVED'}catch(x){r='BLOCKED'}r;"));
        ScriptObjectMirror T = (ScriptObjectMirror)((Invocable)e).invokeFunction("initializeCoreMod");

        byte[] b; try (java.util.zip.ZipFile z=new java.util.zip.ZipFile(JAR)) { b=z.getInputStream(z.getEntry(CLS)).readAllBytes(); }
        ClassNode in=new ClassNode(); new ClassReader(b).accept(in,0);
        int before=clientRefsIn(in,MN,MD);
        System.out.println("[1] getTooltipImage client refs BEFORE = "+before+" (>0 expected)");
        ScriptObjectMirror entry=(ScriptObjectMirror)T.get("uvfixes_minecolonies_itemfood_clientlevel");
        if (entry==null){System.out.println("FAIL: missing entry");return;}
        ClassNode out=(ClassNode)((ScriptObjectMirror)entry.get("transformer")).call(entry,in);
        int after=clientRefsIn(out,MN,MD);
        System.out.println("[2] getTooltipImage client refs AFTER  = "+after+" (must be 0)");
        // body now = Optional.empty + areturn
        int emptyCall=0,aret=0;
        for (MethodNode m: out.methods) if (m.name.equals(MN)&&m.desc.equals(MD))
            for (AbstractInsnNode n: m.instructions.toArray()){
                if (n instanceof MethodInsnNode mi && mi.owner.equals("java/util/Optional")&&mi.name.equals("empty")) emptyCall++;
                if (n.getOpcode()==Opcodes.ARETURN) aret++;
            }
        System.out.println("[3] body: Optional.empty="+emptyCall+" ARETURN="+aret);
        boolean w=false; try{ SafeWriter cw=new SafeWriter(ClassWriter.COMPUTE_FRAMES); out.accept(cw); cw.toByteArray(); w=true; }catch(Throwable t){System.out.println("  write err: "+t);}
        System.out.println("[4] re-serialize (COMPUTE_FRAMES) = "+w);
        boolean pass = before>0 && after==0 && emptyCall==1 && aret==1 && w;
        System.out.println(pass? "\n==== Fix53 PASS (ItemFood ClientLevel ref removed) ====" : "\n==== Fix53 FAIL ====");
    }
}
