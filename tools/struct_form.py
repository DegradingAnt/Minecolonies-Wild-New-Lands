import struct, gzip, zipfile, sys
def _rd(f, t):
    if t==1: return struct.unpack('>b',f.read(1))[0]
    if t==2: return struct.unpack('>h',f.read(2))[0]
    if t==3: return struct.unpack('>i',f.read(4))[0]
    if t==4: return struct.unpack('>q',f.read(8))[0]
    if t==5: return struct.unpack('>f',f.read(4))[0]
    if t==6: return struct.unpack('>d',f.read(8))[0]
    if t==7:
        n=struct.unpack('>i',f.read(4))[0]; return f.read(n)
    if t==8:
        n=struct.unpack('>H',f.read(2))[0]; return f.read(n).decode('utf-8','replace')
    if t==9:
        it=f.read(1)[0]; n=struct.unpack('>i',f.read(4))[0]
        return [_rd(f,it) for _ in range(n)]
    if t==10:
        d={}
        while True:
            tt=f.read(1)[0]
            if tt==0: break
            ln=struct.unpack('>H',f.read(2))[0]; nm=f.read(ln).decode('utf-8','replace')
            d[nm]=_rd(f,tt)
        return d
    if t==11:
        n=struct.unpack('>i',f.read(4))[0]; return [struct.unpack('>i',f.read(4))[0] for _ in range(n)]
    if t==12:
        n=struct.unpack('>i',f.read(4))[0]; return [struct.unpack('>q',f.read(8))[0] for _ in range(n)]
    raise ValueError("tag "+str(t))
def load(data):
    try: data=gzip.decompress(data)
    except: pass
    f=__import__('io').BytesIO(data)
    t=f.read(1)[0]; ln=struct.unpack('>H',f.read(2))[0]; f.read(ln)
    return _rd(f,t)
def schema(o, pre='', depth=0):
    if depth>2: return
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(v,(dict,)): print(f"{pre}{k}: compound({len(v)})"); schema(v,pre+'  ',depth+1)
            elif isinstance(v,list): print(f"{pre}{k}: list[{len(v)}] of {type(v[0]).__name__ if v else '?'}"); 
            else: print(f"{pre}{k}: {type(v).__name__} = {str(v)[:40]}")
jar, entry = sys.argv[1], sys.argv[2]
data = zipfile.ZipFile(jar).read(entry)
root = load(data)
print("=== ROOT SCHEMA:", entry, "===")
schema(root)

def short_name(n):
    return n.split(':')[-1]
AIRY={'air','cave_air','void_air','blocksubstitution','blocksolidsubstitution','blockfluidsubstitution'}
def analyze(jar, entry):
    root=load(zipfile.ZipFile(jar).read(entry))
    sx,sy,sz=root['size_x'],root['size_y'],root['size_z']
    pal=[p.get('Name','?') for p in root['palette']]
    packed=root['blocks']
    idx=[]
    for v in packed:
        v&=0xFFFFFFFF
        idx.append((v>>16)&0xFFFF); idx.append(v&0xFFFF)
    idx=idx[:sx*sy*sz]
    import collections
    layfill=[]; palcount=collections.Counter()
    for y in range(sy):
        c=0
        for j in range(sz*sx):
            p=idx[y*sz*sx+j]
            if p<len(pal):
                nm=short_name(pal[p])
                if nm not in AIRY:
                    c+=1; palcount[nm]+=1
        layfill.append(c)
    tot=sz*sx
    print(f"DIMS {sx}w x {sz}d x {sy}h   (footprint {sx*sz}, {sum(layfill)} solid blocks)")
    print("PROFILE (bottom->top, % of footprint filled):")
    print("  "+" ".join(f"{round(100*c/tot):>3d}" for c in layfill))
    print("TOP BLOCKS: "+", ".join(f"{b}:{n}" for b,n in palcount.most_common(12)))

if __name__=='__main__' and len(sys.argv)>3 and sys.argv[3]=='analyze':
    analyze(sys.argv[1], sys.argv[2])
