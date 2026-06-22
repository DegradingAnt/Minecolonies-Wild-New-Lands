"""Reusable box-grid -> 2.5D isometric SVG renderer for wnl_pathways deco renders.
Define a piece as a list of cuboids in BLOCK grid coords (x right, z depth/back-to-front, y up);
this projects + depth-sorts + auto-shades 3 visible faces per cuboid, and places accent markers
(lanterns/flames/finials) + right-hand callout labels. Literal colors only (GitHub-safe).

Projection: screenX = (x - z)*U ; screenY = (x + z)*V - y*BH   (V = U/2, BH = U)
Larger (x+z) = lower on screen = nearer the viewer -> painter's order = ascending (x0+z0, y0)."""
import html

def _clamp(v): return max(0, min(255, int(round(v))))
def shade(hexc, f):
    h = hexc.lstrip("#"); r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return "#%02x%02x%02x" % (_clamp(r*f), _clamp(g*f), _clamp(b*f))

class Iso:
    def __init__(self, U=12):
        self.U=U; self.V=U/2.0; self.BH=U
        self.boxes=[]; self.accents=[]; self.labels=[]
    def P(self, x, z, y):
        return (round((x - z)*self.U, 1), round((x + z)*self.V - y*self.BH, 1))
    def box(self, x, z, y, dx, dz, dy, color, seam=False):
        self.boxes.append((x, z, y, dx, dz, dy, color, seam))
    def accent(self, x, z, y, kind, color="#ffd47a", r=3.2):
        self.accents.append((x, z, y, kind, color, r))   # kind: 'glow','dot','finial'
    def label(self, x, z, y, text, side="right"):
        self.labels.append((x, z, y, text, side))

    def _faces(self, b):
        x,z,y,dx,dz,dy,color,seam = b
        P=self.P
        top=[P(x,z,y+dy),P(x+dx,z,y+dy),P(x+dx,z+dz,y+dy),P(x,z+dz,y+dy)]
        south=[P(x,z+dz,y),P(x+dx,z+dz,y),P(x+dx,z+dz,y+dy),P(x,z+dz,y+dy)]
        east=[P(x+dx,z,y),P(x+dx,z+dz,y),P(x+dx,z+dz,y+dy),P(x+dx,z,y+dy)]
        def poly(pts, fill, st):
            return f'<polygon points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="{fill}" stroke="{st}" stroke-width="0.6"/>'
        ct, cs, ce = color, shade(color,0.84), shade(color,0.70)
        out=[poly(south,cs,shade(cs,0.8)), poly(east,ce,shade(ce,0.8)), poly(top,ct,shade(ct,0.82))]
        if seam:
            for hy in range(1,int(dy)):
                if dy>8 and hy%2: continue
                a=P(x,z+dz,y+hy); b2=P(x+dx,z+dz,y+hy)
                out.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b2[0]}" y2="{b2[1]}" stroke="{shade(cs,0.7)}" stroke-width="0.4" opacity="0.45"/>')
        return out

    def svg(self, title="", size_label="", pad=22, label_w=232):
        order = sorted(self.boxes, key=lambda b:(b[0]+b[1], b[2], b[0]))
        body=[]
        for b in order: body += self._faces(b)
        # accents (foreground)
        acc=[]
        for x,z,y,kind,color,r in self.accents:
            sx,sy=self.P(x,z,y)
            if kind=="glow":
                acc.append(f'<circle cx="{sx}" cy="{sy}" r="{r*2.6:.1f}" fill="{color}" opacity="0.22"/>')
                acc.append(f'<rect x="{sx-r:.1f}" y="{sy-r:.1f}" width="{r*2:.1f}" height="{r*2:.1f}" rx="1.2" fill="{color}" stroke="{shade(color,0.7)}" stroke-width="0.6"/>')
            elif kind=="finial":
                acc.append(f'<line x1="{sx}" y1="{sy}" x2="{sx}" y2="{sy-9}" stroke="#5e472c" stroke-width="1.4"/>')
                acc.append(f'<circle cx="{sx}" cy="{sy-10:.1f}" r="2.4" fill="#eafff8" stroke="#9cc4bb" stroke-width="0.6"/>')
            else:
                acc.append(f'<circle cx="{sx}" cy="{sy}" r="{r:.1f}" fill="{color}" stroke="{shade(color,0.7)}" stroke-width="0.6"/>')
        # bounds
        pts=[]
        for b in self.boxes:
            for f in self._faces(b):
                pass
        xs=[]; ys=[]
        for b in self.boxes:
            x,z,y,dx,dz,dy,_,_=b
            for cx in (x,x+dx):
                for cz in (z,z+dz):
                    for cy in (y,y+dy):
                        sx,sy=self.P(cx,cz,cy); xs.append(sx); ys.append(sy)
        minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
        ox=pad-minx; oy=pad-miny
        gw=maxx-minx; gh=maxy-miny
        W=gw+pad*2+label_w; H=gh+pad*2+24
        # offset everything by (ox,oy) via a group translate
        lab=[]
        lx=gw+pad*2-6  # label column start (just right of geometry)
        ly0=pad+14
        for i,(x,z,y,text,side) in enumerate(self.labels):
            sx,sy=self.P(x,z,y); sx+=ox; sy+=oy
            ty=ly0+i*20
            lab.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{lx:.1f}" y2="{ty-3}" stroke="#76767e" stroke-width="0.5" stroke-dasharray="2 2"/>')
            lab.append(f'<text x="{lx+6:.1f}" y="{ty}" font-family="system-ui,sans-serif" font-size="12" fill="#a6a6ae">{html.escape(text)}</text>')
        head=(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
              f'font-family="system-ui,sans-serif"><title>{html.escape(title)}</title>')
        g=f'<g transform="translate({ox:.1f},{oy:.1f})">' + "".join(body)+"".join(acc) + '</g>'
        extra="".join(lab)
        if size_label:
            extra+=f'<text x="{pad}" y="{H-8:.0f}" font-family="system-ui,sans-serif" font-size="12" fill="#76767e">{html.escape(size_label)}</text>'
        return head+g+extra+"</svg>\n"
