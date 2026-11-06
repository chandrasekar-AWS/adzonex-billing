"""Repairs the fused R+O in the 'GROW' tagline of the Ad ZoneX logo (all variants)."""
import sys; sys.path.insert(0,'/tmp')
from logoscan import scan
from PIL import Image, ImageDraw, ImageFont
import numpy as np
F='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
XSQ=0.89     # the logo lettering is ~11% narrower than stock Arial

def render_O(cap_h, o_h):
    S=8; size=int(round(72*cap_h/49.5))*S
    f=ImageFont.truetype(F,size); img=Image.new('L',(size*2,size*2),0); ImageDraw.Draw(img).text((size//2,size//4),'O',font=f,fill=255)
    arr=np.array(img); ys,xs=np.where(arr>8); crop=Image.fromarray(arr[ys.min():ys.max()+1, xs.min():xs.max()+1])
    tw=int(round(crop.width/S*XSQ)); return np.array(crop.resize((tw,o_h),Image.LANCZOS)).astype(float)/255

def fix(src, dst, gaps=(0.92,0.85)):
    im,a,lab,c=scan(src); A=np.array(im).copy(); H,W=A.shape[:2]
    assert len(c)==16, (src,len(c))
    opaque=A[:,:,3].min()==255
    G,RO,Wc,R=c[13],c[14],c[15],c[8]
    cap=R[3]-R[1]; s=cap/50.0
    # colour of the tagline, taken from real pixels
    rm=(lab==R[4]); col=np.median(A[rm][:,:3],axis=0).astype(int)
    # typical gap between letters inside the words DESIGN / BRAND (excluding the I and the dots)
    word=[c[i] for i in (0,1,2,4,5,7,8,9,10,11)]; g=[c[i+1][0]-c[i][0+2] for i in range(len(c)) if False]
    gl=[]; 
    for grp in ((0,1,2,3,4,5),(7,8,9,10,11)):
        for i,j in zip(grp,grp[1:]):
            if i==3 or j==3: continue
            gl.append(c[j][0]-c[i][2])
    gap=float(np.median(gl))
    P=4  # patch padding
    def patch(comp):
        x0,y0,x1,y1,_=comp; return (x0-P,y0-P,x1+P,y1+P)
    # --- masks for R and W glyphs
    def glyph_mask(box,bgcol):
        x0,y0,x1,y1=box; sub=A[y0:y1,x0:x1].astype(float)
        if not opaque: return sub[:,:,3]/255.0
        gch=sub[:,:,1]; return np.clip((gch-bgcol[1])/(col[1]-bgcol[1]),0,1)
    def bg_at(x,y): return A[y,x,:3].astype(float)
    ey0,ey1=G[1]-P-1,G[3]+P+1; ex0=G[2]+8; ex1=Wc[2]+P+1
    if not opaque:   # safety: nothing else may live inside the area we clear
        reg=A[ey0:ey1,ex0:ex1,3]>10; keep=np.zeros_like(reg)
        for comp in (RO,Wc): keep[comp[1]-ey0-1:comp[3]-ey0+1, comp[0]-ex0-1:comp[2]-ex0+1]=True
        assert not (reg&~keep).any(), 'something else is inside the erase area'
    bgL=A[ey0:ey1,ex0-3,:3].astype(float); bgR=A[ey0:ey1,ex1+3,:3].astype(float)
    Rbox=patch(R); Wbox=patch(Wc)
    Rm=glyph_mask(Rbox,bgL[len(bgL)//2]); Wm=glyph_mask(Wbox,bgL[len(bgL)//2])
    # --- erase
    if opaque:
        for k,yy in enumerate(range(ey0,ey1)):
            t=np.linspace(0,1,ex1-ex0)[:,None]; A[yy,ex0:ex1,:3]=(bgL[k]*(1-t)+bgR[k]*t).round()
    else: A[ey0:ey1,ex0:ex1,:]=0
    def put(m,x,y):
        h,w=m.shape; reg=A[y:y+h,x:x+w]
        if opaque:
            for ch in range(3): reg[:,:,ch]=np.clip(reg[:,:,ch]*(1-m)+col[ch]*m,0,255).round()
        else:
            na=np.clip(np.maximum(reg[:,:,3]/255.0,m),0,1); reg[:,:,:3]=col; reg[:,:,3]=(na*255).round()
    # --- layout
    rx=RO[0]-P; put(Rm,rx,Rbox[1]); r_end=RO[0]+(R[2]-R[0])
    om=render_O(cap,G[3]-G[1]); ox=int(round(r_end+gap*gaps[0])); put(om,ox,G[1])
    wx=int(round(ox+om.shape[1]+gap*gaps[1]))-P; put(Wm,wx,Wbox[1])
    out=Image.fromarray(A.astype('uint8'),'RGBA'); out.save(dst,optimize=True)
    return dict(gap=gap,color=tuple(col),R=(rx+P,),O=(ox,ox+om.shape[1]),W_old=Wc[0],W_new=wx+P,W_end=wx+P+(Wc[2]-Wc[0]))
if __name__=='__main__':
    import os
    for f in ['logo/adzonex-logo-original.png','logo/adzonex-logo-transparent.png','logo/adzonex-logo-dark-text.png']:
        d='/tmp/logofix/'+os.path.basename(f); print(f,fix('/home/claude/work/'+f,d))
