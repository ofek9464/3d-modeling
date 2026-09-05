from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]

import cv2,numpy as np,manifold3d as md,trimesh
OUT=ROOT/'generated';OUT.mkdir(exist_ok=True,parents=True)
logo=cv2.imread(str(ROOT/'inputs/logo.png'))
qrimg=cv2.imread(str(ROOT/'inputs/qr.png'))
payload,corners,decoded_grid=cv2.QRCodeDetector().detectAndDecode(qrimg)
assert payload and decoded_grid.shape==(25,25)
# Sample the supplied pixels directly. Adaptive decoder thresholding mistakes
# the slightly lighter finder centers for white in this particular image.
src=corners[0].astype('float32')
dst=np.array([[0,0],[500,0],[500,500],[0,500]],dtype='float32')
warp=cv2.warpPerspective(cv2.cvtColor(qrimg,cv2.COLOR_BGR2GRAY),cv2.getPerspectiveTransform(src,dst),(501,501))
qr=np.array([[0 if warp[r*20+10,c*20+10]<128 else 255 for c in range(25)] for r in range(25)],dtype=np.uint8)
b,g,r=cv2.split(logo.astype(np.int16))
masks={'green':((g>r+9)&(g>b+5)&(g<170)),
       'black':((r<90)&(g<90)&(b<90)),
       'gold':((r>105)&(g>105)&(b<g*.78)&(r>g*.8))}
for m in masks.values():m[:,:45]=False
combined=np.logical_or.reduce(list(masks.values()))
ys,xs=np.where(combined);xmin,xmax=xs.min(),xs.max();ymin,ymax=ys.min(),ys.max()
scale=62/(xmax-xmin);cx=(xmin+xmax)/2;cy=(ymin+ymax)/2
parts={}
for name,mask in masks.items():
    contours,_=cv2.findContours(mask.astype('uint8')*255,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    polygons=[]
    for c in contours:
        if cv2.contourArea(c)<12:continue
        p=cv2.approxPolyDP(c,.55,True).reshape(-1,2).astype(float)
        p[:,0]=(p[:,0]-cx)*scale;p[:,1]=-(p[:,1]-cy)*scale-1
        if len(p)>2:polygons.append(p)
    parts[name]=md.CrossSection(polygons,md.FillRule.EvenOdd)
    cv2.imwrite(str(OUT/(name+'_source_mask.png')),mask.astype('uint8')*255)
gy,gx=np.where(masks['green']);left,right=int(gx.min()),int(gx.max())
columns=np.arange(left,right+1)
top=np.array([np.where(masks['green'][:,x])[0].min() for x in columns],dtype=np.float32)
bottom=np.array([np.where(masks['green'][:,x])[0].max() for x in columns],dtype=np.float32)
# Bridge only the stethoscope's occlusion of the book border, filling the pages.
top=cv2.medianBlur(top.reshape(1,-1),5).ravel()
top=cv2.erode(top.reshape(1,-1),np.ones((1,31),np.uint8)).ravel()
p=np.concatenate([np.column_stack((columns,top)),np.column_stack((columns[::-1],bottom[::-1]))]).astype(np.float32)
p=cv2.approxPolyDP(p.reshape(-1,1,2),.65,True).reshape(-1,2).astype(float)
p[:,0]=(p[:,0]-cx)*scale;p[:,1]=-(p[:,1]-cy)*scale-1
book=md.CrossSection([p],md.FillRule.EvenOdd).offset(.35,md.JoinType.Round,32)
# The book is the backing; only the stethoscope silhouette extends above it.
body=book+parts['black'].offset(.55,md.JoinType.Round,32)
body=body.simplify(.025)
body+=md.CrossSection.circle(4.6,64).translate((-25,16.4))
hole=md.CrossSection.circle(2.1,64).translate((-25,16.4))
body-=hole
front=body.extrude(1.6)
art=md.CrossSection.batch_boolean(list(parts.values()),md.OpType.Add).offset(.015,md.JoinType.Round,16).simplify(.01)
art-=hole.offset(.08)
art=md.CrossSection.batch_boolean([art,body.offset(-.05)],md.OpType.Intersect).simplify(.015)
front+=art.extrude(.72).translate((0,0,1.58))
# Find the largest upright square in the usable back, sampled every 0.05 mm.
# The square includes four blank modules on every side plus the cut expansion.
usable=md.CrossSection.batch_boolean([book.mirror((1,0)),body.mirror((1,0))],md.OpType.Intersect).offset(-.5)
ppm=20;origin=np.array([40.,35.])
canvas=np.zeros((1400,1600),np.uint8)
polys=[np.rint((np.asarray(poly)+origin)*ppm).astype(np.int32) for poly in usable.to_polygons()]
cv2.fillPoly(canvas,polys,255)
lo,hi=1,1000
while lo<hi:
    mid=(lo+hi+1)//2
    eroded=cv2.erode(canvas,np.ones((mid,mid),np.uint8),borderType=cv2.BORDER_CONSTANT,borderValue=0)
    if np.any(eroded):lo=mid
    else:hi=mid-1
eroded=cv2.erode(canvas,np.ones((lo,lo),np.uint8),borderType=cv2.BORDER_CONSTANT,borderValue=0)
rr,cc=np.where(eroded)
centers=np.column_stack((cc,rr))/ppm-origin
center=centers[np.argmin(np.sum((centers-np.array([0,-5]))**2,axis=1))]
side=(lo-2)/ppm
while (md.CrossSection.square((side,side),center=True).translate(center)-usable).area()>1e-7:side-=.05
pitch=(side-.08)/33
qx,qy=map(float,center)
print('MAX_QR',pitch,'CENTER',center,'TOTAL_WITH_MARGIN',side,flush=True)
qparts=[]
for row,col in zip(*np.where(qr==0)):
    qparts.append(md.CrossSection.square((pitch,pitch)).translate(((col-12.5)*pitch,(11.5-row)*pitch)))
qpattern=md.CrossSection.batch_boolean(qparts,md.OpType.Add).offset(.04,md.JoinType.Round,16).translate((qx,qy))
# Require the entire code and its four-module quiet zone to lie on the book.
quiet=md.CrossSection.square((side,side),center=True).translate((qx,qy))
print('BOOK',book.bounds(),book.area(),'OUTSIDE',(quiet-book).area())
assert (quiet-usable).area()<1e-6,'QR quiet zone exceeds usable back'
back=body.mirror((1,0)).extrude(1.6)-qpattern.extrude(.65).translate((0,0,1.1))
# Back pattern appears normally when the completed keychain is turned over.
full=front.translate((0,0,1.6))+back.rotate((0,180,0)).translate((0,0,1.6))
audits=[]
def export(solid,name):
    solid=solid.simplify(.001)
    print(name,solid.status(),len(solid.decompose()),flush=True)
    data=solid.to_mesh()
    mesh=trimesh.Trimesh(np.asarray(data.vert_properties)[:,:3],np.asarray(data.tri_verts),process=True)
    mesh.export(OUT/name);m=trimesh.load_mesh(OUT/name,process=True)
    print('AUDIT',m.is_watertight,m.is_winding_consistent,m.volume,len(m.split(only_watertight=False)),flush=True)
    assert m.is_watertight and m.is_winding_consistent and m.volume>0
    assert len(m.split(only_watertight=False))==1
    assert m.area_faces.min()>1e-10
    audits.append({'file':name,'watertight':True,'connected_components':1,'winding_consistent':True,'triangles':len(m.faces),'dimensions_mm':m.extents.tolist(),'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()})
export(front,'keychain_front_glue_half.stl');export(back,'keychain_qr_glue_half.stl');export(full,'keychain_complete.stl')
# Verify a projection reconstructed from the actual exported QR half's recess floors.
m=trimesh.load_mesh(OUT/'keychain_qr_glue_half.stl',process=True)
projection=np.full((660,660),255,np.uint8)
for tri in m.triangles:
    if np.all(np.abs(tri[:,2]-1.1)<1e-4):
        uv=np.column_stack(((tri[:,0]-qx)/pitch*20+330,-(tri[:,1]-qy)/pitch*20+330)).round().astype('int32')
        cv2.fillConvexPoly(projection,uv,0)
decoded,_,_=cv2.QRCodeDetector().detectAndDecode(projection)
cv2.imwrite(str(OUT/'qr_from_exported_mesh.png'),projection)
assert decoded==payload,(decoded,payload)
cv2.imwrite(str(OUT/'qr_from_exported_mesh.png'),projection)
(OUT/'validation.json').write_text(json.dumps({'qr_destination':payload,'qr_grid':25,'module_mm':pitch,'pattern_width_mm':25*pitch+.08,'quiet_zone_min_mm':4*pitch,'edge_clearance_mm':.5,'search_resolution_mm':.05,'qr_center_xy':center.tolist(),'quiet_zone_inside_book':True,'qr_mesh_projection_decoded':decoded,'physical_scan_tested':False,'meshes':audits},indent=2))
(OUT/'logo_geometry.json').write_text(json.dumps({'bbox':[int(xmin),int(ymin),int(xmax),int(ymax)],'scale':scale,'cx':cx,'cy':cy}))
print(json.dumps(audits));print('QR_MESH_DECODED',decoded)
