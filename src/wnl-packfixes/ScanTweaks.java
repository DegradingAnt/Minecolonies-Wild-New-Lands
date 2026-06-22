import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*;
import java.util.*;
import java.util.zip.*;

// Offline scanner: find MineColonies-addon mixin injectors that no longer resolve against the
// CURRENT minecolonies jar (today's 1.1.1332 snapshot). Two break modes:
//   (1) target method named by `method=` selector is GONE from the target class -> 0 target(s).
//   (2) target method present, but the @At INVOKE/FIELD target+ordinal no longer matches enough
//       call sites in its body (e.g. ordinal=2 but only 2 occurrences -> ordinals 0,1) -> 0 points.
// Either way mixin throws a Critical InjectionError (defaultRequire=1) and the dedicated server
// boot-loops. This lists EXACTLY which handlers to neutralise so we fix all of them in one pass.
public class ScanTweaks {
    static Map<String,ClassNode> mcCache = new HashMap<>();
    static List<String> mcJars = new ArrayList<>();

    static ClassNode readClass(byte[] b){ ClassNode cn=new ClassNode(); new ClassReader(b).accept(cn, ClassReader.SKIP_FRAMES); return cn; }

    // Lazy-load a target class (com/minecolonies/...) from any of the provided mc jars.
    static ClassNode mcClass(String internalName) {
        if (mcCache.containsKey(internalName)) return mcCache.get(internalName);
        ClassNode cn = null;
        for (String jp : mcJars) {
            try (ZipFile z = new ZipFile(jp)) {
                ZipEntry e = z.getEntry(internalName + ".class");
                if (e != null) { cn = readClass(z.getInputStream(e).readAllBytes()); break; }
            } catch (Exception ex) {}
        }
        mcCache.put(internalName, cn);
        return cn;
    }

    static String av(AnnotationNode an, String key) {
        if (an.values==null) return null;
        for (int i=0;i<an.values.size();i+=2) if (key.equals(an.values.get(i))) { Object v=an.values.get(i+1); return v==null?null:v.toString(); }
        return null;
    }
    static Object avRaw(AnnotationNode an, String key) {
        if (an.values==null) return null;
        for (int i=0;i<an.values.size();i+=2) if (key.equals(an.values.get(i))) return an.values.get(i+1);
        return null;
    }

    static final Set<String> INJECTORS = new HashSet<>(Arrays.asList(
        "Lorg/spongepowered/asm/mixin/injection/Inject;",
        "Lorg/spongepowered/asm/mixin/injection/Redirect;",
        "Lorg/spongepowered/asm/mixin/injection/ModifyArg;",
        "Lorg/spongepowered/asm/mixin/injection/ModifyArgs;",
        "Lorg/spongepowered/asm/mixin/injection/ModifyConstant;",
        "Lorg/spongepowered/asm/mixin/injection/ModifyVariable;"));
    static boolean isMixinExtras(String d){ return d.startsWith("Lcom/llamalad7/mixinextras/injector/"); }

    public static void main(String[] a) throws Exception {
        // args: <minecoloniesJar> <addonJar1> [addonJar2 ...]
        mcJars.add(a[0]);
        List<String> addonJars = new ArrayList<>();
        for (int i=1;i<a.length;i++){ addonJars.add(a[i]); mcJars.add(a[i]); } // addons can also be targets
        int brokenCount=0;
        for (String addon : addonJars) {
            String modName = new File(addon).getName();
            try (ZipFile z = new ZipFile(addon)) {
                // find mixin config jsons (top-level *.json mentioning "mixins"/"client"/"package")
                List<String> mixinClasses = new ArrayList<>();
                Enumeration<? extends ZipEntry> en = z.entries();
                while (en.hasMoreElements()) {
                    ZipEntry e = en.nextElement();
                    String n = e.getName();
                    if (n.contains("/")) continue; if (!n.endsWith(".json")) continue;
                    String body = new String(z.getInputStream(e).readAllBytes());
                    if (!body.contains("\"package\"") || !(body.contains("\"mixins\"")||body.contains("\"client\"")||body.contains("\"server\""))) continue;
                    String pkg = jstr(body, "package");
                    if (pkg==null) continue;
                    for (String cls : jarr(body, "mixins")) mixinClasses.add(pkg.replace('.','/')+"/"+cls.replace('.','/'));
                    for (String cls : jarr(body, "client")) mixinClasses.add(pkg.replace('.','/')+"/"+cls.replace('.','/'));
                    for (String cls : jarr(body, "server")) mixinClasses.add(pkg.replace('.','/')+"/"+cls.replace('.','/'));
                }
                for (String mc : mixinClasses) {
                    ZipEntry me = z.getEntry(mc + ".class");
                    if (me==null) continue;
                    ClassNode cn = readClass(z.getInputStream(me).readAllBytes());
                    // @Mixin targets
                    List<String> targets = new ArrayList<>();
                    List<AnnotationNode> ca = new ArrayList<>();
                    if (cn.invisibleAnnotations!=null) ca.addAll(cn.invisibleAnnotations);
                    if (cn.visibleAnnotations!=null) ca.addAll(cn.visibleAnnotations);
                    for (AnnotationNode an : ca) if (an.desc.equals("Lorg/spongepowered/asm/mixin/Mixin;")) {
                        Object val = avRaw(an,"value");
                        if (val instanceof List) for (Object o : (List<?>)val) if (o instanceof Type) targets.add(((Type)o).getInternalName());
                        Object tg = avRaw(an,"targets");
                        if (tg instanceof List) for (Object o : (List<?>)tg) targets.add(o.toString().replace('.','/'));
                    }
                    // only scan minecolonies targets (that's what changed today)
                    List<String> mcTargets = new ArrayList<>();
                    for (String t : targets) if (t.startsWith("com/minecolonies/")) mcTargets.add(t);
                    if (mcTargets.isEmpty()) continue;

                    for (MethodNode m : cn.methods) {
                        if (m.visibleAnnotations==null) continue;
                        // --- @Accessor/@Invoker blind-spot check (these do NOT honor require=) ---
                        for (AnnotationNode an : m.visibleAnnotations) {
                            boolean acc = an.desc.equals("Lorg/spongepowered/asm/mixin/gen/Accessor;");
                            boolean inv = an.desc.equals("Lorg/spongepowered/asm/mixin/gen/Invoker;");
                            if (!acc && !inv) continue;
                            String explicit = av(an,"value");
                            for (String tgt : mcTargets) {
                                ClassNode tc = mcClass(tgt); if (tc==null) continue;
                                if (acc) {
                                    // accessor target = explicit value, else strip get/set/is + lowercase first
                                    String fld = explicit;
                                    if (fld==null) { String mn=m.name; String base=mn.replaceFirst("^(get|set|is)",""); if(base.length()>0) fld=Character.toLowerCase(base.charAt(0))+base.substring(1); }
                                    boolean ok=false; if(fld!=null) for(FieldNode fn: tc.fields) if(fn.name.equals(fld)||fn.name.equals(explicit)) ok=true;
                                    if(!ok && fld!=null && explicit==null) { /* inferred name uncertain */ continue; }
                                    if(!ok && fld!=null){ report(modName,mc,m,"Accessor",tgt+".#"+fld,"ACCESSOR field MISSING (no require= remedy)"); brokenCount++; }
                                } else {
                                    String mth = explicit; if(mth==null){ String mn=m.name; mth=mn.replaceFirst("^(call|invoke|new|create)",""); if(mth.length()>0) mth=Character.toLowerCase(mth.charAt(0))+mth.substring(1); }
                                    boolean ok=false; if(mth!=null) for(MethodNode tm: tc.methods) if(tm.name.equals(mth)||tm.name.equals(explicit)) ok=true;
                                    if(!ok && explicit==null) continue;
                                    if(!ok){ report(modName,mc,m,"Invoker",tgt+".#"+mth,"INVOKER method MISSING (no require= remedy)"); brokenCount++; }
                                }
                            }
                        }
                        for (AnnotationNode an : m.visibleAnnotations) {
                            boolean inj = INJECTORS.contains(an.desc) || isMixinExtras(an.desc);
                            if (!inj) continue;
                            List<String> selectors = new ArrayList<>();
                            Object ms = avRaw(an,"method");
                            if (ms instanceof List) for (Object o : (List<?>)ms) selectors.add(o.toString());
                            // collect @At list
                            List<AnnotationNode> ats = new ArrayList<>();
                            Object at = avRaw(an,"at");
                            if (at instanceof AnnotationNode) ats.add((AnnotationNode)at);
                            else if (at instanceof List) for (Object o:(List<?>)at) if (o instanceof AnnotationNode) ats.add((AnnotationNode)o);
                            String injType = an.desc.substring(an.desc.lastIndexOf('/')+1).replace(";","");

                            for (String tgt : mcTargets) {
                                ClassNode tc = mcClass(tgt);
                                if (tc==null) { report(modName, mc, m, injType, tgt, "TARGET CLASS NOT FOUND"); brokenCount++; continue; }
                                for (String sel : selectors) {
                                    String selName = sel; String selDesc=null;
                                    int p = sel.indexOf('(');
                                    if (p>=0){ selName=sel.substring(0,p); selDesc=sel.substring(p); }
                                    // wildcard selectors (* or regex) -> skip (can't statically resolve safely)
                                    if (selName.contains("*")||selName.startsWith("@")) continue;
                                    List<MethodNode> found = new ArrayList<>();
                                    for (MethodNode tm : tc.methods) if (tm.name.equals(selName) && (selDesc==null || tm.desc.startsWith(selDesc)||tm.desc.equals(selDesc))) found.add(tm);
                                    if (found.isEmpty()) { report(modName, mc, m, injType, tgt+"."+selName, "MODE1 target method GONE (0 methods named '"+selName+"')"); brokenCount++; continue; }
                                    // mode-2: @At INVOKE/FIELD with target+ordinal
                                    for (AnnotationNode atn : ats) {
                                        String atVal = av(atn,"value");
                                        String atTgt = av(atn,"target");
                                        Object ordO = avRaw(atn,"ordinal");
                                        int ordinal = ordO instanceof Integer ? (Integer)ordO : -1;
                                        if (atTgt==null) continue; // HEAD/RETURN/TAIL etc. -> mode1 already passed
                                        if (atVal!=null && !(atVal.equals("INVOKE")||atVal.equals("INVOKE_ASSIGN")||atVal.startsWith("FIELD"))) continue;
                                        // parse atTgt: Lowner;name(desc)ret  OR  Lowner;name:fieldDesc
                                        int maxCount=0;
                                        for (MethodNode tm : found) {
                                            int c = countCallSites(tm, atTgt);
                                            if (c>maxCount) maxCount=c;
                                        }
                                        if (maxCount==0) { report(modName, mc, m, injType, tgt+"."+selName, "MODE2 @At "+atVal+" target NOT CALLED in body: "+atTgt); brokenCount++; }
                                        else if (ordinal>=0 && ordinal>=maxCount) { report(modName, mc, m, injType, tgt+"."+selName, "MODE2 @At ordinal="+ordinal+" but only "+maxCount+" occurrence(s) of "+atTgt); brokenCount++; }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        System.out.println("\n==== ScanTweaks done: "+brokenCount+" broken injector(s) ====");
        System.out.println("\n==== ALL minecolonies-targeting mixin classes (dot form) ====");
        java.util.TreeMap<String,java.util.List<String>> byMod = new java.util.TreeMap<>();
        for (String addon : addonJars) byMod.put(new File(addon).getName(), new java.util.ArrayList<>());
        // re-scan just to list (cheap)
        for (String addon : addonJars) {
            String modName = new File(addon).getName();
            try (ZipFile z = new ZipFile(addon)) {
                List<String> mixinClasses = new ArrayList<>();
                Enumeration<? extends ZipEntry> en = z.entries();
                while (en.hasMoreElements()) { ZipEntry e=en.nextElement(); String n=e.getName();
                    if (n.contains("/")||!n.endsWith(".json")) continue;
                    String body=new String(z.getInputStream(e).readAllBytes());
                    if (!body.contains("\"package\"")) continue;
                    String pkg=jstr(body,"package"); if(pkg==null) continue;
                    for (String c: jarr(body,"mixins")) mixinClasses.add(pkg.replace('.','/')+"/"+c.replace('.','/'));
                    for (String c: jarr(body,"client")) mixinClasses.add(pkg.replace('.','/')+"/"+c.replace('.','/'));
                    for (String c: jarr(body,"server")) mixinClasses.add(pkg.replace('.','/')+"/"+c.replace('.','/'));
                }
                for (String mc: mixinClasses) {
                    ZipEntry me=z.getEntry(mc+".class"); if(me==null) continue;
                    ClassNode cn=readClass(z.getInputStream(me).readAllBytes());
                    List<AnnotationNode> ca=new ArrayList<>();
                    if(cn.invisibleAnnotations!=null) ca.addAll(cn.invisibleAnnotations);
                    if(cn.visibleAnnotations!=null) ca.addAll(cn.visibleAnnotations);
                    boolean mco=false;
                    for(AnnotationNode an:ca) if(an.desc.equals("Lorg/spongepowered/asm/mixin/Mixin;")){
                        Object val=avRaw(an,"value");
                        if(val instanceof List) for(Object o:(List<?>)val) if(o instanceof Type && ((Type)o).getInternalName().startsWith("com/minecolonies/")) mco=true;
                        Object tg=avRaw(an,"targets");
                        if(tg instanceof List) for(Object o:(List<?>)tg) if(o.toString().replace('.','/').startsWith("com/minecolonies/")) mco=true;
                    }
                    if(mco) byMod.get(modName).add(mc.replace('/','.'));
                }
            }
        }
        for (Map.Entry<String,java.util.List<String>> e: byMod.entrySet()) {
            System.out.println("// "+e.getKey()+" ("+e.getValue().size()+")");
            java.util.Collections.sort(e.getValue());
            for (String c: e.getValue()) System.out.println("'"+c+"',");
        }
    }

    static int countCallSites(MethodNode tm, String atTgt) {
        // Mixin MemberInfo: [Lowner;]name[(args)ret | :fieldDesc]. owner is OPTIONAL (owner-less ->
        // match by name [+desc] regardless of owner; that's how mixin resolves it against the body).
        String owner=null,name=null,desc=null; boolean field=false;
        try {
            String rest = atTgt;
            if (atTgt.startsWith("L")) {
                int semi = atTgt.indexOf(';');
                int paren0 = atTgt.indexOf('(');
                // only treat leading L...; as an owner if the ';' comes before any '(' (else it's a desc)
                if (semi>=0 && (paren0<0 || semi<paren0)) { owner = atTgt.substring(1, semi); rest = atTgt.substring(semi+1); }
            }
            int paren = rest.indexOf('(');
            int colon = rest.indexOf(':');
            if (paren>=0){ name=rest.substring(0,paren); desc=rest.substring(paren); }
            else if (colon>=0){ field=true; name=rest.substring(0,colon); desc=rest.substring(colon+1); }
            else { name=rest; }
        } catch(Exception e){ return -1; }
        if (name==null||name.isEmpty()) return -1;
        int c=0;
        for (AbstractInsnNode in : tm.instructions.toArray()) {
            if (!field && in instanceof MethodInsnNode){ MethodInsnNode mi=(MethodInsnNode)in;
                if ((owner==null||mi.owner.equals(owner)) && mi.name.equals(name) && (desc==null||mi.desc.equals(desc))) c++; }
            else if (field && in instanceof FieldInsnNode){ FieldInsnNode fi=(FieldInsnNode)in;
                if ((owner==null||fi.owner.equals(owner)) && fi.name.equals(name)) c++; }
        }
        return c;
    }

    static void report(String mod,String mixin,MethodNode m,String injType,String tgt,String reason){
        System.out.println("BROKEN ["+mod+"]");
        System.out.println("   mixin  : "+mixin.substring(mixin.lastIndexOf('/')+1));
        System.out.println("   handler: "+m.name+m.desc+"   @"+injType);
        System.out.println("   target : "+tgt);
        System.out.println("   reason : "+reason);
    }

    // --- tiny JSON helpers (configs are simple) ---
    static String jstr(String body,String key){ int i=body.indexOf("\""+key+"\""); if(i<0)return null; int c=body.indexOf(':',i); int q1=body.indexOf('"',c+1); if(q1<0)return null; int q2=body.indexOf('"',q1+1); return body.substring(q1+1,q2); }
    static List<String> jarr(String body,String key){ List<String> out=new ArrayList<>(); int i=body.indexOf("\""+key+"\""); if(i<0)return out; int lb=body.indexOf('[',i); if(lb<0)return out; int rb=body.indexOf(']',lb); String seg=body.substring(lb+1,rb);
        java.util.regex.Matcher mm=java.util.regex.Pattern.compile("\"([^\"]+)\"").matcher(seg); while(mm.find()) out.add(mm.group(1)); return out; }
}
