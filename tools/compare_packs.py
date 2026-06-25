"""Side-by-side texture-pack comparison in the voxel viewer (Stay True | Fresh Textures).
Builds a small showcase scene of common blocks, resolves each block's top/side texture from each pack
(pack override -> vanilla block_tex/ fallback, exactly like in-game), and emits a self-contained
render3d/pack_compare.html: ONE shared camera, TWO scenes/canvases rendered in lock-step so dragging
either side rotates both. Private dev tool. Run: python .uvrun/compare_packs.py"""
import os, io, json, base64, zipfile
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
RP = os.path.join(ROOT, "resourcepacks")
TEXDIR = os.path.join(DIR, "block_tex")          # vanilla fallback
OUT = os.path.join(DIR, "render3d", "pack_compare.html")

def find(key):
    for f in os.listdir(RP):
        if key.lower() in f.lower() and f.endswith(".zip"):
            return os.path.join(RP, f)
    raise SystemExit("pack not found: " + key)

PACK_L = ("Stay True", find("Stay True 1.21.5"))
PACK_R = ("Fresh Textures", find("Fresh Textures 1.4.4"))

# block -> (top_texname, side_texname, kind)   kind: cube | grass | glass | water
BLOCKS = {
    "grass_block":       ("grass_block_top", "grass_block_side", "grass"),
    "dirt":              ("dirt", "dirt", "cube"),
    "coarse_dirt":       ("coarse_dirt", "coarse_dirt", "cube"),
    "stone":             ("stone", "stone", "cube"),
    "cobblestone":       ("cobblestone", "cobblestone", "cube"),
    "mossy_cobblestone": ("mossy_cobblestone", "mossy_cobblestone", "cube"),
    "stone_bricks":      ("stone_bricks", "stone_bricks", "cube"),
    "oak_log":           ("oak_log_top", "oak_log", "cube"),
    "oak_planks":        ("oak_planks", "oak_planks", "cube"),
    "bricks":            ("bricks", "bricks", "cube"),
    "gravel":            ("gravel", "gravel", "cube"),
    "sand":              ("sand", "sand", "cube"),
    "andesite":          ("andesite", "andesite", "cube"),
    "glass":             ("glass", "glass", "glass"),
    "water":             ("water_still", "water_still", "water"),
}
GRASS_TINT = (124, 189, 107)   # plains foliage-ish, baked into grass top (same for both -> fair)

def load_tex(z, texname):
    p = "assets/minecraft/textures/block/%s.png" % texname
    data = None
    try:
        data = z.read(p)                       # pack override
    except KeyError:
        vp = os.path.join(TEXDIR, texname + ".png")
        if os.path.exists(vp):
            data = open(vp, "rb").read()        # vanilla fallback (exactly like in-game)
    if data is None:
        return None
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    if im.height > im.width and im.width in (16, 32) and im.height % im.width == 0:
        im = im.crop((0, 0, im.width, im.width))   # animated strip -> first frame
    if im.size != (16, 16):
        im = im.resize((16, 16), Image.NEAREST)
    return im

def tint(im, col):
    r, g, b, a = im.split()
    r = r.point(lambda v: v * col[0] // 255)
    g = g.point(lambda v: v * col[1] // 255)
    b = b.point(lambda v: v * col[2] // 255)
    return Image.merge("RGBA", (r, g, b, a))

def datauri(im):
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def build_tex(packpath):
    z = zipfile.ZipFile(packpath)
    tex = {}
    overrides = 0
    for blk, (tt, ts, kind) in BLOCKS.items():
        # count whether this pack actually overrides (for the report)
        if any(("assets/minecraft/textures/block/%s.png" % t) in z.namelist() for t in (tt, ts)):
            overrides += 1
        top = load_tex(z, tt) or Image.new("RGBA", (16, 16), (140, 140, 142, 255))
        side = load_tex(z, ts) or top
        if kind == "grass":
            top = tint(top, GRASS_TINT)
        tex[blk] = {"top": datauri(top), "side": datauri(side), "kind": kind}
    return tex, overrides

TEXL, ovL = build_tex(PACK_L[1])
TEXR, ovR = build_tex(PACK_R[1])

# ---- showcase scene: a small cottage-corner vignette (grid dict -> cells) ----
g = {}
def put(x, y, z, b): g[(x, y, z)] = b
W = 9
for x in range(W):
    for z in range(W):
        put(x, 0, z, "grass_block")            # grass ground
for x in range(W):                             # a coarse-dirt path across z=4
    put(x, 0, 4, "coarse_dirt")
# water pool + sand beach, front-right
for x in range(6, 8):
    for z in range(6, 8):
        put(x, 0, z, "water")
for x in range(5, 9):                          # sand ring around the pool
    for z in range(5, 9):
        if (x, 0, z) in g and g[(x, 0, z)] == "grass_block":
            put(x, 0, z, "sand")
# cottage corner, back-left (x1..3, z1..3): cobble foundation, oak frame, plank walls, glass window
for x in range(1, 4):
    for z in range(1, 4):
        put(x, 1, z, "cobblestone")            # foundation ring (filled, simpler)
for (cx, cz) in [(1, 1), (3, 1), (1, 3), (3, 3)]:
    for y in (2, 3, 4):
        put(cx, y, cz, "oak_log")              # corner posts
for y in (2, 3):                               # back wall (z=1) + left wall (x=1) planks
    for x in range(1, 4):
        if (x, y, 1) not in g: put(x, y, 1, "oak_planks")
    for z in range(1, 4):
        if (1, y, z) not in g: put(1, y, z, "oak_planks")
put(2, 3, 1, "glass")                          # window in the back wall
put(2, 1, 0, "stone_bricks")                   # entrance step (front)
# a little rock cluster back-right: mossy cobble + andesite + stone + bricks sample
put(6, 1, 1, "mossy_cobblestone"); put(7, 1, 1, "andesite"); put(7, 1, 2, "stone")
put(6, 1, 2, "mossy_cobblestone"); put(6, 2, 1, "andesite")
put(0, 1, 7, "bricks"); put(0, 1, 8, "bricks"); put(1, 1, 8, "gravel"); put(0, 2, 8, "bricks")

blocks = sorted(set(g.values()))
bi = {b: i for i, b in enumerate(blocks)}
xs = [c[0] for c in g]; ys = [c[1] for c in g]; zs = [c[2] for c in g]
mnx, mny, mnz = min(xs), min(ys), min(zs)
cells = [[c[0] - mnx, c[1] - mny, c[2] - mnz, bi[b]] for c, b in g.items()]
GEO = {"pal": blocks, "cells": cells,
       "w": max(xs) - mnx + 1, "h": max(ys) - mny + 1, "d": max(zs) - mnz + 1}

DATA = "window.GEO=%s;\nwindow.TEXL=%s;\nwindow.TEXR=%s;\nwindow.PACKS=%s;\n" % (
    json.dumps(GEO, separators=(",", ":")),
    json.dumps(TEXL, separators=(",", ":")),
    json.dumps(TEXR, separators=(",", ":")),
    json.dumps([PACK_L[0], PACK_R[0]]),
)

HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Texture compare — __L__ | __R__</title>
<style>
 html,body{margin:0;height:100%;background:#0f1218;color:#e7e7e7;font-family:system-ui,Segoe UI,Arial,sans-serif;overflow:hidden}
 #wrap{display:flex;width:100vw;height:100vh}
 .pane{position:relative;flex:1;border-right:2px solid #000}
 .pane:last-child{border-right:none}
 canvas{display:block;width:100%;height:100%}
 .tag{position:absolute;top:10px;left:10px;background:#1b1f27dd;border:1px solid #3a3e45;border-radius:7px;padding:7px 12px;font-size:15px;font-weight:600}
 #hint{position:fixed;bottom:8px;left:50%;transform:translateX(-50%);font-size:12px;color:#8a929c;background:#1b1f27cc;padding:5px 12px;border-radius:6px}
</style></head><body>
<div id="wrap">
  <div class="pane"><div class="tag" id="tagL"></div><canvas id="cL"></canvas></div>
  <div class="pane"><div class="tag" id="tagR"></div><canvas id="cR"></canvas></div>
</div>
<div id="hint">drag either side = rotate both · wheel = zoom · right-drag = pan</div>
<script src="viewer/lib/three.min.js"></script>
<script>__DATA__</script>
<script>
const GEO=window.GEO;
document.getElementById('tagL').textContent='◀ '+window.PACKS[0];
document.getElementById('tagR').textContent=window.PACKS[1]+' ▶';
function mkRenderer(id){const r=new THREE.WebGLRenderer({canvas:document.getElementById(id),antialias:true});
 r.setPixelRatio(Math.min(devicePixelRatio,2));r.outputEncoding=THREE.sRGBEncoding;return r;}
const rL=mkRenderer('cL'), rR=mkRenderer('cR');
const camera=new THREE.PerspectiveCamera(48,1,0.1,4000);
function mkScene(TEX){
 const s=new THREE.Scene();s.background=new THREE.Color(0x8fb4d6);s.fog=new THREE.Fog(0x8fb4d6,90,300);
 s.add(new THREE.AmbientLight(0xffffff,0.9));
 const d=new THREE.DirectionalLight(0xffffff,0.5);d.position.set(40,90,30);s.add(d);
 const d2=new THREE.DirectionalLight(0xffffff,0.22);d2.position.set(-30,40,-50);s.add(d2);
 const texCache={},matCache={};
 function texFor(b,f){const k=b+'|'+f;if(texCache[k])return texCache[k];
  const uri=(TEX[b]&&TEX[b][f])||(TEX['stone']&&TEX['stone'][f]);const img=new Image();const t=new THREE.Texture(img);
  img.onload=()=>{t.needsUpdate=true;};img.src=uri;t.magFilter=THREE.NearestFilter;t.minFilter=THREE.NearestFilter;
  t.generateMipmaps=false;t.encoding=THREE.sRGBEncoding;texCache[k]=t;return t;}
 function kindOf(b){return (TEX[b]&&TEX[b].kind)||'cube';}
 function singleMat(b,f){const k=b+'|'+f;if(matCache[k])return matCache[k];let m;const kd=kindOf(b);
  if(kd==='water')m=new THREE.MeshLambertMaterial({color:0x3f73c4,transparent:true,opacity:0.72,side:THREE.DoubleSide});
  else if(kd==='glass')m=new THREE.MeshLambertMaterial({map:texFor(b,f),transparent:true,opacity:0.55,depthWrite:false,side:THREE.DoubleSide});
  else m=new THREE.MeshLambertMaterial({map:texFor(b,f),side:THREE.DoubleSide});
  matCache[k]=m;return m;}
 // culled cube mesher (top/side split), matching the deco viewer
 const FACES=[{d:[1,0,0],t:0,c:[[1,0,1],[1,0,0],[1,1,0],[1,1,1]]},{d:[-1,0,0],t:0,c:[[0,0,0],[0,0,1],[0,1,1],[0,1,0]]},
  {d:[0,1,0],t:1,c:[[0,1,1],[1,1,1],[1,1,0],[0,1,0]]},{d:[0,-1,0],t:0,c:[[0,0,0],[1,0,0],[1,0,1],[0,0,1]]},
  {d:[0,0,1],t:0,c:[[1,0,1],[0,0,1],[0,1,1],[1,1,1]]},{d:[0,0,-1],t:0,c:[[0,0,0],[1,0,0],[1,1,0],[0,1,0]]}];
 const UVQ=[[0,0],[1,0],[1,1],[0,1]];const pal=GEO.pal;
 const occ=new Map();for(const c of GEO.cells)occ.set(c[0]+','+c[1]+','+c[2],c);
 let mnx=1e9,mnz=1e9,mxx=-1e9,mxz=-1e9,mxy=-1e9;
 for(const c of GEO.cells){mnx=Math.min(mnx,c[0]);mnz=Math.min(mnz,c[2]);mxx=Math.max(mxx,c[0]+1);mxz=Math.max(mxz,c[2]+1);mxy=Math.max(mxy,c[1]+1);}
 const cx=(mnx+mxx)/2,cz=(mnz+mxz)/2;
 const buf={};function B(bi){if(!buf[bi])buf[bi]={0:{p:[],n:[],u:[]},1:{p:[],n:[],u:[]}};return buf[bi];}
 function solid(b){const k=kindOf(b);return k==='cube'||k==='grass';}
 for(const c of GEO.cells){const[x,y,z,bi]=c;const blk=pal[bi];
  if(!solid(blk)){const m=new THREE.Mesh(new THREE.BoxGeometry(1,1,1),[singleMat(blk,'side'),singleMat(blk,'side'),singleMat(blk,'top'),singleMat(blk,'side'),singleMat(blk,'side'),singleMat(blk,'side')]);
   m.position.set(x-cx+0.5,y+0.5,z-cz+0.5);s.add(m);continue;}
  for(const f of FACES){const nb=occ.get((x+f.d[0])+','+(y+f.d[1])+','+(z+f.d[2]));
   if(nb&&solid(pal[nb[3]]))continue;const tgt=B(bi)[f.t];const tri=[0,1,2,0,2,3];
   for(const idx of tri){const co=f.c[idx];tgt.p.push(x-cx+co[0],y+co[1],z-cz+co[2]);tgt.n.push(f.d[0],f.d[1],f.d[2]);tgt.u.push(UVQ[idx][0],UVQ[idx][1]);}}}
 for(const bi in buf)for(const face of[0,1]){const a=buf[bi][face];if(!a.p.length)continue;
  const gg=new THREE.BufferGeometry();gg.setAttribute('position',new THREE.Float32BufferAttribute(a.p,3));
  gg.setAttribute('normal',new THREE.Float32BufferAttribute(a.n,3));gg.setAttribute('uv',new THREE.Float32BufferAttribute(a.u,2));
  s.add(new THREE.Mesh(gg,singleMat(pal[bi],face?'top':'side')));}
 s._bounds={w:mxx-mnx,h:mxy,d:mxz-mnz};return s;}
const sceneL=mkScene(window.TEXL), sceneR=mkScene(window.TEXR);
// shared camera
const bd=sceneL._bounds;const target=new THREE.Vector3(0,bd.h*0.42,0);
let theta=0.82,phi=1.02,radius=Math.max(bd.w,bd.d,bd.h)*1.7+8;
function updateCam(){camera.position.set(target.x+radius*Math.sin(phi)*Math.sin(theta),target.y+radius*Math.cos(phi),target.z+radius*Math.sin(phi)*Math.cos(theta));camera.lookAt(target);}
let drag=null;
function bindDrag(canvas){canvas.addEventListener('mousedown',e=>{drag={b:e.button,x:e.clientX,y:e.clientY};});
 canvas.addEventListener('contextmenu',e=>e.preventDefault());
 canvas.addEventListener('wheel',e=>{e.preventDefault();radius=Math.max(4,Math.min(400,radius*(1+e.deltaY*0.0012)));updateCam();},{passive:false});}
bindDrag(rL.domElement);bindDrag(rR.domElement);
addEventListener('mouseup',()=>drag=null);
addEventListener('mousemove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;drag.x=e.clientX;drag.y=e.clientY;
 if(drag.b===2){const pan=radius*0.0016;const rt=new THREE.Vector3().subVectors(camera.position,target).normalize();
  const right=new THREE.Vector3().crossVectors(camera.up,rt).normalize();const up=new THREE.Vector3().crossVectors(rt,right).normalize();
  target.addScaledVector(right,-dx*pan);target.addScaledVector(up,dy*pan);}
 else{theta-=dx*0.01;phi=Math.max(0.05,Math.min(Math.PI-0.05,phi-dy*0.01));}updateCam();});
function resize(){const w=innerWidth/2,h=innerHeight;rL.setSize(w,h);rR.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}
addEventListener('resize',resize);resize();updateCam();
function loop(){requestAnimationFrame(loop);rL.render(sceneL,camera);rR.render(sceneR,camera);}
loop();
</script></body></html>"""

html = (HTML.replace("__DATA__", DATA)
            .replace("__L__", PACK_L[0]).replace("__R__", PACK_R[0]))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT)
print("  scene: %d cells, %d block types" % (len(cells), len(blocks)))
print("  %s overrides %d/%d showcase blocks; %s overrides %d/%d"
      % (PACK_L[0], ovL, len(BLOCKS), PACK_R[0], ovR, len(BLOCKS)))
print("  size: %.0f KB" % (len(html) / 1024))
