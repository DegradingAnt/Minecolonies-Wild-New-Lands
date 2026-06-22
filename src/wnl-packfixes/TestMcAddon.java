import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.openjdk.nashorn.api.scripting.ScriptObjectMirror;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

// Offline test for PackFixes Fix 54: make MineColonies addon mixin injectors require=0 so the
// minecolonies 1.1.1332 snapshot drift (out-of-range @At ordinals / moved call sites) no longer
// aborts the dedicated-server boot. Installs the EXACT NeoForge coremod Nashorn ClassFilter
// (whitelist verified against coremods-7.0.3 CoreModScriptingEngine -- AnnotationNode is NOT on
// it, so the coremod must never Java.type() it) and checks the require/expect ints are stored as
// java.lang.Integer (Nashorn auto-box), handlers are PRESERVED (optionalised, not stripped), and
// the transformed class re-serialises.
public class TestMcAddon {
    static final String JAR = "mods/MineColonies_Tweaks-1.21.1-3.30.jar";
    static final String CLS = "steve_gall/minecolonies_tweaks/mixin/common/minecolonies/FoodUtilsMixin";
    static final String ENTRY = "uvfixes_mcaddon_optional_steve_gall_minecolonies_tweaks_mixin_common_minecolonies_FoodUtilsMixin";

    static final Set<String> INJ = Set.of(
        "Lorg/spongepowered/asm/mixin/injection/Inject;","Lorg/spongepowered/asm/mixin/injection/Redirect;",
        "Lorg/spongepowered/asm/mixin/injection/ModifyArg;","Lorg/spongepowered/asm/mixin/injection/ModifyArgs;",
        "Lorg/spongepowered/asm/mixin/injection/ModifyConstant;","Lorg/spongepowered/asm/mixin/injection/ModifyVariable;");
    static boolean isInj(String d){ return d.startsWith("Lcom/llamalad7/mixinextras/injector/") || INJ.contains(d); }

    static class SafeWriter extends ClassWriter {
        SafeWriter(int f){ super(f);}
        @Override protected String getCommonSuperClass(String a,String b){ try{return super.getCommonSuperClass(a,b);}catch(Throwable t){return "java/lang/Object";} }
    }
    static Object annVal(AnnotationNode an, String key){
        if (an.values==null) return "ABSENT";
        for (int i=0;i<an.values.size();i+=2) if (key.equals(an.values.get(i))) return an.values.get(i+1);
        return "ABSENT";
    }

    public static void main(String[] a) throws Exception {
        // EXACT real coremod filter (CoreModScriptingEngine whitelist)
        Set<String> WC = Set.of("net.neoforged.coremod.api.ASMAPI",
          "org.objectweb.asm.Attribute","org.objectweb.asm.Handle","org.objectweb.asm.Label","org.objectweb.asm.Opcodes","org.objectweb.asm.Type","org.objectweb.asm.TypePath","org.objectweb.asm.TypeReference",
          "org.objectweb.asm.tree.AbstractInsnNode","org.objectweb.asm.tree.FieldInsnNode","org.objectweb.asm.tree.FieldNode","org.objectweb.asm.tree.FrameNode","org.objectweb.asm.tree.IincInsnNode","org.objectweb.asm.tree.InsnList","org.objectweb.asm.tree.InsnNode","org.objectweb.asm.tree.IntInsnNode","org.objectweb.asm.tree.InvokeDynamicInsnNode","org.objectweb.asm.tree.JumpInsnNode","org.objectweb.asm.tree.LabelNode","org.objectweb.asm.tree.LdcInsnNode","org.objectweb.asm.tree.LineNumberNode","org.objectweb.asm.tree.LocalVariableAnnotationNode","org.objectweb.asm.tree.LocalVariableNode","org.objectweb.asm.tree.LookupSwitchInsnNode","org.objectweb.asm.tree.MethodInsnNode","org.objectweb.asm.tree.MethodNode","org.objectweb.asm.tree.MultiANewArrayInsnNode","org.objectweb.asm.tree.ParameterNode","org.objectweb.asm.tree.TableSwitchInsnNode","org.objectweb.asm.tree.TryCatchBlockNode","org.objectweb.asm.tree.TypeAnnotationNode","org.objectweb.asm.tree.TypeInsnNode","org.objectweb.asm.tree.VarInsnNode");
        Set<String> WP = Set.of("java.util","java.util.function","org.objectweb.asm.util");
        org.openjdk.nashorn.api.scripting.ClassFilter f = n -> { if (WC.contains(n)) return true; int d=n.lastIndexOf('.'); return d!=-1 && WP.contains(n.substring(0,d)); };
        ScriptEngine e = new org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory().getScriptEngine(new String[]{"--language=es6"}, ClassLoader.getSystemClassLoader(), f);
        e.eval(Files.readString(Path.of("_dev/wnl-packfixes-src/coremods/uvfixes.js")));
        e.eval("log = function(s){ print('  [coremod] ' + s); };");
        System.out.println("[0] uvfixes.js evaluated under REAL filter: PASS (no blocked-class access at load)");
        // sanity: AnnotationNode must be BLOCKED (proves filter is the real, restrictive one)
        System.out.println("[0a] AnnotationNode Java.type = " + e.eval("var r;try{Java.type('org.objectweb.asm.tree.AnnotationNode');r='RESOLVED(BUG!)'}catch(x){r='BLOCKED(correct)'}r;"));
        ScriptObjectMirror T = (ScriptObjectMirror)((Invocable)e).invokeFunction("initializeCoreMod");
        System.out.println("[0b] initializeCoreMod entry count = " + T.size());

        byte[] b; try (java.util.zip.ZipFile z=new java.util.zip.ZipFile(JAR)) { b=z.getInputStream(z.getEntry(CLS+".class")).readAllBytes(); }
        ClassNode in=new ClassNode(); new ClassReader(b).accept(in,0);
        // count injectors before + record handler names
        int injBefore=0; boolean hadHandler=false; int requirePresentBefore=0;
        for (MethodNode m: in.methods) if (m.visibleAnnotations!=null) for (AnnotationNode an: m.visibleAnnotations) if (isInj(an.desc)) {
            injBefore++;
            if (!"ABSENT".equals(annVal(an,"require"))) requirePresentBefore++;
            if (m.name.equals("hasBestOptionInInv2")) hadHandler=true;
        }
        System.out.println("[1] FoodUtilsMixin injectors BEFORE = "+injBefore+" (require= present on "+requirePresentBefore+"); broken handler hasBestOptionInInv2 present="+hadHandler);

        ScriptObjectMirror entry=(ScriptObjectMirror)T.get(ENTRY);
        if (entry==null){System.out.println("FAIL: missing map entry '"+ENTRY+"'");return;}
        ClassNode out=(ClassNode)((ScriptObjectMirror)entry.get("transformer")).call(entry,in);

        int injAfter=0, ok0Int=0, bad=0; boolean stillHandler=false;
        for (MethodNode m: out.methods) if (m.visibleAnnotations!=null) for (AnnotationNode an: m.visibleAnnotations) if (isInj(an.desc)) {
            injAfter++;
            Object req=annVal(an,"require"), exp=annVal(an,"expect");
            boolean reqOk = (req instanceof Integer) && ((Integer)req)==0;
            boolean expOk = (exp instanceof Integer) && ((Integer)exp)==0;
            if (reqOk && expOk) ok0Int++; else { bad++; if(bad<=3) System.out.println("    !! "+m.name+" require="+req+"("+cls(req)+") expect="+exp+"("+cls(exp)+")"); }
            if (m.name.equals("hasBestOptionInInv2")) stillHandler=true;
        }
        System.out.println("[2] injectors AFTER = "+injAfter+"; require=0&expect=0 as java.lang.Integer on "+ok0Int+"; bad="+bad);
        System.out.println("[3] broken handler hasBestOptionInInv2 STILL present (optionalised, not stripped) = "+stillHandler);
        boolean w=false; try{ SafeWriter cw=new SafeWriter(ClassWriter.COMPUTE_FRAMES); out.accept(cw); cw.toByteArray(); w=true; }catch(Throwable t){System.out.println("  write err: "+t);}
        System.out.println("[4] re-serialize (COMPUTE_FRAMES) = "+w);

        // spot-check: Compatibility RecipeStorageMixin entry also registered
        boolean compatEntry = T.containsKey("uvfixes_mcaddon_optional_steve_gall_minecolonies_compatibility_mixin_common_minecolonies_RecipeStorageMixin");
        System.out.println("[5] Compatibility RecipeStorageMixin entry present = "+compatEntry);

        boolean pass = injBefore>0 && injAfter==injBefore && ok0Int==injAfter && bad==0 && hadHandler && stillHandler && w && compatEntry && T.size()>=109;
        System.out.println(pass? "\n==== Fix54 PASS (addon injectors optionalised, handlers preserved, Integer-boxed) ====" : "\n==== Fix54 FAIL ====");
    }
    static String cls(Object o){ return o==null?"null":o.getClass().getSimpleName(); }
}
