from pathlib import Path
import sys,json,zipfile,xml.etree.ElementTree as ET
import numpy as np
import argparse
MODEL=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--input',type=Path,default=MODEL/'stl')
parser.add_argument('--output',type=Path,default=MODEL/'generated/color')
args=parser.parse_args()

import manifold3d as md
import trimesh
OUT=args.output.resolve();OUT.mkdir(exist_ok=True,parents=True)
M=md.Manifold
def box(size,xyz):return M.cube(size,center=True).translate(xyz)
def cyl(r,h,xyz,axis='z'):
    m=M.cylinder(h,r,r,64,center=True)
    if axis=='y':m=m.rotate((90,0,0))
    if axis=='x':m=m.rotate((0,90,0))
    return m.translate(xyz)
def load_solid(path):
    m=trimesh.load_mesh(path,process=True)
    return M(md.Mesh64(np.asarray(m.vertices,dtype=np.float64),np.asarray(m.faces,dtype=np.uint64)))
colors=[('Olive','#888C68'),('Black','#252829'),('Brass','#B39C58'),('Blue','#277BAB')]
cutters=[]
def region(name,color,shape):cutters.append((name,color,shape))
# Partition the existing volume. Every region is removed from the remainder,
# so parts share boundaries without intentional gaps or overlapping interiors.
region('Blue selector screw',3,cyl(.68,2.7,(-8.5,8.85,11.4)))
region('Fire button',1,cyl(3.46,1.7,(0,3,11.35)))
region('Selector knob',0,cyl(2.12,3.0,(-6,10,12.05))+box((1.35,2.5,2),(-6,8.55,12.2)))
for x,label in [(-7.1,'Left'),(7.1,'Right')]:
    region(label+' top screw center',1,cyl(1.25,1.15,(x,-2,12.45)))
    region(label+' top screw surround',2,cyl(2.44,1.3,(x,-2,12.48)))
for sign,label in [(-1,'Left'),(1,'Right')]:
    region(label+' side screw center',1,cyl(.98,1.2,(sign*11.55,.15,6.85),'x'))
    region(label+' side screw surround',2,cyl(2.20,1.3,(sign*11.45,.15,6.85),'x'))
region('Front strap fastener',2,cyl(1.56,1.0,(-6.85,-10.45,12.9)))
# Strap volumes follow the existing diagonal and cylindrical surface geometry.
strap=M.hull_points([(-6.85+dx,y,z) for dx in (-.94,.94) for y,z in [(-13.5,12.28),(-13.5,13.3),(-18.6,10.15),(-18.6,11.3)]])
region('Left cover strap',0,strap+box((1.88,4.1,.9),(-6.85,-11.9,12.75)))
region('Right cover strap',0,box((1.88,6.3,1.3),(6.8,-18.15,10.65)))
region('Left aperture inserts',1,cyl(.93,1.7,(-5.55,-18.5,7.65),'y')+cyl(.81,1.7,(-8.09,-18.5,7.25),'y'))
region('Right aperture insert',1,cyl(.99,1.7,(6.8,-20.8,7.35),'y'))
region('Left front cover',0,box((9,8,12),(-6.85,-19.9,7.45)))
region('Right front cover',0,box((9,9,12),(6.8,-20.4,7.35)))
region('Rear battery cap',0,box((9,6,12),(7,18.3,8)))
region('Miniature rail mount',1,box((12,14,3.25),(0,0,1.625)))

NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
def node(parent,tag,**attrs):return ET.SubElement(parent,'{'+NS+'}'+tag,{k:str(v) for k,v in attrs.items()})
def mesh_arrays(s):
    m=s.to_mesh64();return np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts)
def serialize(parts,path):
    root=ET.Element('{'+NS+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'})
    node(root,'metadata',name='Title').text='PEQ-15 cosmetic miniature - editable color parts'
    res=node(root,'resources');bases=node(res,'basematerials',id=1)
    for name,color in colors:node(bases,'base',name=name,displaycolor=color)
    for i,(name,color,solid) in enumerate(parts,2):
        obj=node(res,'object',id=i,type='model',name=name,partnumber=f'PEQ-{i-1:02}',pid=1,pindex=color)
        mesh=node(obj,'mesh');vs=node(mesh,'vertices');ts=node(mesh,'triangles')
        verts,faces=mesh_arrays(solid)
        for x,y,z in verts:node(vs,'vertex',x=f'{x:.12g}',y=f'{y:.12g}',z=f'{z:.12g}')
        for a,b,c in faces:node(ts,'triangle',v1=a,v2=b,v3=c)
    assembly=node(res,'object',id=100,type='model',name='PEQ-15 miniature');comp=node(assembly,'components')
    for i in range(2,len(parts)+2):node(comp,'component',objectid=i)
    node(node(root,'build'),'item',objectid=100)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    # Re-open the delivered 3MF and check the actual serialized meshes.
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        decoded=ET.fromstring(z.read('3D/3dmodel.model'))
    reloaded=[]
    for obj in decoded.findall('.//{'+NS+'}object'):
        mesh=obj.find('{'+NS+'}mesh')
        if mesh is None:continue
        verts=np.array([[float(v.get(a)) for a in ('x','y','z')] for v in mesh.find('{'+NS+'}vertices')])
        faces=np.array([[int(t.get(a)) for a in ('v1','v2','v3')] for t in mesh.find('{'+NS+'}triangles')])
        tm=trimesh.Trimesh(verts,faces,process=False)
        assert tm.is_watertight and tm.is_winding_consistent and tm.volume>0,obj.get('name')
        s=M(md.Mesh64(np.array(tm.vertices,dtype=np.float64),np.array(tm.faces,dtype=np.uint64)))
        assert s.status()==md.Error.NoError,obj.get('name')
        reloaded.append(s)
    return reloaded

audits=[]
for key in ['7p2','7p4','7p6']:
    original=load_solid(args.input/f'peq15_channel_{key}mm.stl')
    assert original.status()==md.Error.NoError
    remaining=original;parts=[]
    for name,color,cutter in cutters:
        part=remaining^cutter
        if part.volume()<=1e-7:raise ValueError('Empty part '+name)
        remaining=remaining-cutter
        parts.append((name,color,part))
    parts.insert(0,('Housing',0,remaining))
    path=OUT/f'PEQ15_colorable_{key}mm.3mf'
    solids=serialize(parts,path)
    merged=M.batch_boolean(solids,md.OpType.Add)
    missing=(original-merged).volume();extra=(merged-original).volume()
    overlap=sum(s.volume() for s in solids)-merged.volume()
    assert missing<1e-4 and extra<1e-4 and abs(overlap)<1e-4,(missing,extra,overlap)
    audits.append({'file':path.name,'named_parts':len(parts),'all_parts_watertight':True,'missing_volume_mm3':missing,'extra_volume_mm3':extra,'overlapping_volume_mm3':overlap,'physical_fit_tested':False})
    if key=='7p4':
        stls=OUT/'separate-parts-7p4';stls.mkdir(exist_ok=True)
        for i,(name,color,s) in enumerate(parts,1):
            v,f=mesh_arrays(s);trimesh.Trimesh(v,f,process=False).export(stls/f'{i:02}-{name.replace(" ","_")}.stl')
(OUT/'validation.json').write_text(json.dumps(audits,indent=2))
print(json.dumps(audits,indent=2))
