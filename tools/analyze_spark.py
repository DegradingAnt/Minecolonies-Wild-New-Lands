import struct, sys, re
PATH = sys.argv[1] if len(sys.argv)>1 else ".uvrun/sparkdl/raw_BFJNHQxE9L.bin"
data = open(PATH,"rb").read()

def rv(b,i):
    s=0;r=0
    while True:
        if i>=len(b): raise IndexError
        x=b[i];i+=1;r|=(x&0x7f)<<s;s+=7
        if not(x&0x80):break
    return r,i
def fields(b):
    i=0;out=[]
    while i<len(b):
        tag,i=rv(b,i);f=tag>>3;wt=tag&7
        if wt==0:v,i=rv(b,i)
        elif wt==1:
            if i+8>len(b):raise IndexError
            v=struct.unpack("<d",b[i:i+8])[0];i+=8
        elif wt==2:
            ln,i=rv(b,i)
            if i+ln>len(b):raise IndexError
            v=b[i:i+ln];i+=ln
        elif wt==5:
            v=struct.unpack("<f",b[i:i+4])[0];i+=4
        else:raise ValueError(wt)
        out.append((f,wt,v))
    return out
def as_text(b):
    try:t=b.decode("utf-8")
    except:return None
    if not t:return None
    return t if all(32<=ord(c)<127 or c in '._/$<>[]' for c in t) else None

CLASS_RE=re.compile(r'^[A-Za-z_][\w$]*(\.[A-Za-z_$][\w$]*)+$')   # has dots, no spaces
def is_classname(t): return bool(t) and CLASS_RE.match(t) and ' ' not in t and len(t)>3

def parse_msg(b):
    try: return fields(b)
    except: return None

# A frame = message with a className string field + (method string) + child frames/times
def frame_info(fs):
    cls=None; meth=None; times=[]; childmsgs=[]
    for f,wt,v in fs:
        if wt==1: times.append(v)
        elif wt==2:
            t=as_text(v)
            if t and is_classname(t) and cls is None: cls=t
            elif t and meth is None and not is_classname(t) and re.match(r'^[\w$<>]+$',t): meth=t
            else:
                # could be packed doubles (times) or a child message
                sub=parse_msg(v)
                if sub is not None:
                    childmsgs.append((v,sub))
                if len(v)>0 and len(v)%8==0 and len(v)<=8*64:
                    try:
                        ds=struct.unpack("<%dd"%(len(v)//8), v)
                        if all(abs(d)<1e12 for d in ds): times.append(sum(ds))
                    except: pass
    return cls,meth,times,childmsgs

# subsystem buckets
BUCKETS=[
 ("DistantHorizons", ("com.seibel.distanthorizons","loadercommon")),
 ("minecolonies", ("com.minecolonies","com.ldtteam")),
 ("create", ("com.simibubi.create","com.railwayteam","plus.dragons","com.rabbitminers","com.copycat")),
 ("netty/network", ("io.netty","net.minecraft.network","net.neoforged.neoforge.network")),
 ("worldgen/chunk", ("net.minecraft.world.level.chunk","net.minecraft.server.level.ChunkMap","net.minecraft.world.level.levelgen","net.minecraft.server.level.ServerChunkCache")),
 ("entity tick", ("net.minecraft.world.entity",)),
 ("pathfinding", ("net.minecraft.world.level.pathfinder","net.minecraft.world.entity.ai")),
 ("blockentity tick", ("net.minecraft.world.level.block.entity",)),
 ("server tick core", ("net.minecraft.server.MinecraftServer","net.minecraft.server.level.ServerLevel","net.minecraft.world.level.Level")),
 ("GC/JVM", ()),
]
def bucket(cls):
    if not cls: return None
    for name,prefs in BUCKETS:
        for p in prefs:
            if cls.startswith(p): return name
    if cls.startswith("net.minecraft"): return "vanilla other"
    return None

self_by_method={}; self_by_bucket={}; self_by_mod={}
total_self=0.0
threads={}

def modkey(cls):
    parts=cls.split('.')
    return '.'.join(parts[:3]) if len(parts)>=3 else cls

def walk(b, sub, thread, depth):
    global total_self
    cls,meth,times,kids=frame_info(sub)
    incl=sum(times) if times else 0.0
    child_incl=0.0
    for cb,cs in kids:
        child_incl+=walk(cb,cs,thread,depth+1)
    # if this node has no times but has kids, treat incl as child sum
    if incl==0.0 and child_incl>0: incl=child_incl
    self_t=incl-child_incl
    if self_t<0: self_t=0.0
    if cls and self_t>0:
        key=cls+"#"+(meth or "?")
        self_by_method[key]=self_by_method.get(key,0)+self_t
        bk=bucket(cls)
        if bk: self_by_bucket[bk]=self_by_bucket.get(bk,0)+self_t
        self_by_mod[modkey(cls)]=self_by_mod.get(modkey(cls),0)+self_t
        total_self+=self_t
        if thread: threads[thread]=threads.get(thread,0)+self_t
    return incl

# Find thread roots: messages with a name string (has space or non-class) whose children are frames
def find_threads(b, depth=0):
    fs=parse_msg(b)
    if fs is None or depth>6: return
    name=None; framekids=[]
    for f,wt,v in fs:
        if wt==2:
            t=as_text(v)
            if t and (' ' in t or not is_classname(t)) and re.search(r'[A-Za-z]',t) and len(t)<60 and '.' not in t.split()[0] if t and t.split() else False:
                pass
    # simpler: recurse to locate frames directly; assign thread by nearest name
    for f,wt,v in fs:
        if wt==2:
            sub=parse_msg(v)
            if sub is None: continue
            c,m,ti,kd=frame_info(sub)
            if c and is_classname(c):
                # v is a frame; find a sibling/ancestor name -> use generic
                walk(v,sub,current_thread[0],depth)
            else:
                # maybe this is a thread node: has a name string + frame children
                nm=None;hasframe=False
                for ff,fwt,fv in sub:
                    if fwt==2:
                        tt=as_text(fv)
                        if tt and not is_classname(tt) and re.search(r'[A-Za-z]',tt) and len(tt)<60: nm=nm or tt
                        ss=parse_msg(fv)
                        if ss:
                            cc,_,_,_=frame_info(ss)
                            if cc and is_classname(cc): hasframe=True
                if nm and hasframe:
                    current_thread[0]=nm
                    walk(v,sub,nm,depth)
                else:
                    find_threads(v,depth+1)

current_thread=[None]
top=fields(data)
# descend into the big f1 and scan all its fields for thread trees
big=top[0][2]
find_threads(big,0)

# metadata
meta=fields(big)
start=end=samples=None
for f,wt,v in meta:
    if f==2 and wt==0: start=v
    elif f==11 and wt==0: end=v
    elif f==12 and wt==0: samples=v
durs = (end-start)/1000.0 if start and end else None

print(f"=== SERVER SPARK PROFILE ===")
if durs: print(f"duration ~{durs:.0f}s   samples~{samples}")
print(f"total attributed self-time units: {total_self:.0f}\n")

print("== self-time by THREAD (top 12) ==")
for k,v in sorted(threads.items(),key=lambda x:-x[1])[:12]:
    print(f"  {v/total_self*100:5.1f}%  {v:10.0f}  {k}")

print("\n== self-time by SUBSYSTEM ==")
for k,v in sorted(self_by_bucket.items(),key=lambda x:-x[1]):
    print(f"  {v/total_self*100:5.1f}%  {v:10.0f}  {k}")

print("\n== top MODS/packages by self-time (top 20) ==")
for k,v in sorted(self_by_mod.items(),key=lambda x:-x[1])[:20]:
    print(f"  {v/total_self*100:5.1f}%  {v:10.0f}  {k}")

print("\n== hottest METHODS by self-time (top 30) ==")
for k,v in sorted(self_by_method.items(),key=lambda x:-x[1])[:30]:
    print(f"  {v/total_self*100:5.1f}%  {v:9.0f}  {k}")
