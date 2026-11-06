from PIL import Image
import numpy as np
from scipy import ndimage
def scan(path):
    im=Image.open(path).convert('RGBA'); a=np.array(im).astype(int); H,W=a.shape[:2]
    mask=(a[:,:,3]>30)&(a[:,:,1]>a[:,:,0]+25)&(a[:,:,1]>a[:,:,2]+60)
    lab,n=ndimage.label(mask)
    comps=[]
    for i,sl in enumerate(ndimage.find_objects(lab),1):
        y0,y1=sl[0].start,sl[0].stop; x0,x1=sl[1].start,sl[1].stop
        if y1>=0.78*H and (y1-y0)<=0.13*H and (x1-x0)<0.12*W: comps.append((x0,y0,x1,y1,i))
    comps.sort()
    return im,a,lab,comps
if __name__=='__main__':
    for f in ['logo/adzonex-logo-original.png','logo/adzonex-logo-transparent.png','logo/adzonex-logo-dark-text.png','app/logo.png']:
        im,a,lab,c=scan(f); print(f,im.size,len(c)); print([ (x0,x1,y0,y1) for x0,y0,x1,y1,i in c])
