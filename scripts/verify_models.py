"""Check published mesh downloads and the saved QR projection, without a printer."""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET
import numpy as np
import trimesh,manifold3d as md,cv2
ROOT=Path(__file__).resolve().parents[1]
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
def solid(mesh):
    result=md.Manifold(md.Mesh64(np.asarray(mesh.vertices,dtype=np.float64),np.asarray(mesh.faces,dtype=np.uint64)))
    assert result.status()==md.Error.NoError
    return result
def check_mesh(mesh,name):
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name
    assert np.isfinite(mesh.vertices).all(),name
    assert mesh.area_faces.min()>0,name
    _,counts=np.unique(np.sort(mesh.edges,axis=1),axis=0,return_counts=True)
    assert np.all(counts==2),name
stls=list((ROOT/'models').rglob('*.stl'))
stls=[p for p in stls if 'generated' not in p.parts]
for p in stls:check_mesh(trimesh.load_mesh(p,process=True),p.name)
three_mfs=list((ROOT/'models/peq15/3mf').glob('*.3mf'))
for p in three_mfs:
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        root=ET.fromstring(z.read('3D/3dmodel.model'))
    assert root.get('unit')=='millimeter'
    parts=[]
    for o in root.findall('.//m:object',NS):
        mesh=o.find('m:mesh',NS)
        if mesh is None:continue
        v=[[float(e.get(a)) for a in ('x','y','z')] for e in mesh.find('m:vertices',NS)]
        f=[[int(e.get(a)) for a in ('v1','v2','v3')] for e in mesh.find('m:triangles',NS)]
        m=trimesh.Trimesh(v,f,process=False)
        check_mesh(m,o.get('name'));parts.append(solid(m))
    assert len(parts)==21
    key=p.stem.split('_')[-1]
    reference=solid(trimesh.load_mesh(ROOT/f'models/peq15/stl/peq15_channel_{key}.stl',process=True))
    merged=md.Manifold.batch_boolean(parts,md.OpType.Add)
    assert (reference-merged).volume()<1e-4 and (merged-reference).volume()<1e-4,p.name
    assert abs(sum(s.volume() for s in parts)-merged.volume())<1e-4,p.name
qr=ROOT/'models/logo-keychain/previews/qr_from_exported_mesh.png'
decoded,_,_=cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(qr)))
assert decoded=='www.thedvmauthor.com'
print(json.dumps({'STLs_checked':len(stls),'multipart_3MFs_checked':len(three_mfs),'parts_per_3MF':21,'saved_QR_projection':decoded,'physical_tests':'not performed'},indent=2))
