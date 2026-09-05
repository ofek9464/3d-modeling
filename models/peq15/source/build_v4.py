"""Solid cosmetic miniature sculpt from the supplied image and online photos.

Units: millimeters. The rail profile is provisional, not measured GoatGuns data.
Run with numpy, matplotlib, trimesh and manifold3d available. Local packages are
loaded from python-packages beside this script when present.
"""
from pathlib import Path
import sys
import json
import math
import hashlib
import argparse

HERE = Path(__file__).resolve().parent

import numpy as np
import manifold3d as md
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=HERE.parent/'generated/stage')
OUT = parser.parse_args().output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
M = md.Manifold
SEGMENTS = 64


def box(size, xyz):
    return M.cube(size, center=True).translate(xyz)


def cylinder(r, length, xyz, axis='z', segments=SEGMENTS):
    obj = M.cylinder(length, r, r, segments, center=True)
    if axis == 'y':
        obj = obj.rotate((90, 0, 0))
    if axis == 'x':
        obj = obj.rotate((0, 90, 0))
    return obj.translate(xyz)


def chamfer_box(size, xyz, bevel=0.7):
    # Convex hull of the three inset rectangular prisms gives planar chamfers.
    half = np.asarray(size) / 2
    points = []
    for axis in range(3):
        ext = half - bevel
        ext[axis] = half[axis]
        for i in (-1, 1):
            for j in (-1, 1):
                for k in (-1, 1):
                    points.append(np.asarray([i, j, k]) * ext + xyz)
    return M.hull_points(np.asarray(points))


def union_all(parts):
    return M.batch_boolean(parts, md.OpType.Add)


def subtract_all(solid, parts):
    return solid - union_all(parts)


def outline_ring(size, xyz, width=0.38, bevel=0.8):
    a = chamfer_box(size, xyz, bevel)
    inner = (size[0]-width*2, size[1]-width*2, size[2]+2)
    return a - chamfer_box(inner, xyz, min(bevel, 0.3))


def screw(x, y, z, radius=0.7):
    head = cylinder(radius, 0.42, (x, y, z))
    return head - box((radius*1.35, 0.32, 0.3), (x, y, z+0.17))


def rounded_box(size, xyz, radius=0.6):
    """Convex hull of sampled corner spheres, with genuinely rounded edges."""
    half = np.asarray(size)/2-radius
    phi = np.linspace(0,math.pi,13)
    theta = np.linspace(0,2*math.pi,24,endpoint=False)
    sphere = np.array([[math.sin(p)*math.cos(t),math.sin(p)*math.sin(t),math.cos(p)]
                       for p in phi for t in theta])*radius
    points = []
    for x in (-1,1):
        for y in (-1,1):
            for z in (-1,1):
                points.extend(sphere+half*np.array([x,y,z])+np.asarray(xyz))
    return M.hull_points(np.asarray(points))


def tube_between(a,b,r):
    a,b=np.array(a,dtype=float),np.array(b,dtype=float)
    direction=b-a; length=np.linalg.norm(direction); n=direction/length
    helper=np.array([0.,0.,1.]) if abs(n[2])<0.9 else np.array([1.,0.,0.])
    u=np.cross(helper,n); u/=np.linalg.norm(u); v=np.cross(n,u)
    matrix=np.column_stack([u,v,n,(a+b)/2])
    return cylinder(r,length,(0,0,0),segments=16).transform(matrix)


def tether(points,r=0.32):
    parts=[tube_between(a,b,r) for a,b in zip(points[:-1],points[1:])]
    for p in points[1:-1]:
        parts.append(rounded_box((r*2,r*2,r*2),p,r))
    return union_all(parts)


def build_body():
    from sculpt_v4 import build_body as sculpt
    return sculpt(globals())


def channel(width, length):
    """Provisional slide-on miniature rail cavity, open below and at both ends.

    Width variants change horizontal clearance only. No scaled weapon standard
    or manufacturer drawing is being asserted by these dimensions.
    """
    throat = width - 1.6
    profile = [(-throat/2,-1),(throat/2,-1),(throat/2,0.8),
               (width/2,1.6),(width/2,2.8),(-width/2,2.8),
               (-width/2,1.6),(-throat/2,0.8)]
    # CrossSection XY maps to world XZ; extrusion is centered along world Y.
    return md.CrossSection([profile]).extrude(length).rotate((90,0,0)).translate((0,length/2,0))


def mount(width, length=13.5):
    outer = chamfer_box((11.2,length,4.4),(0,0,2.2),0.35)
    return outer - channel(width,length+2)


def fit_coupon(width, index):
    test = mount(width,7.0)
    # Dot count identifies the matching STL without tiny printed text.
    for i in range(index):
        test += cylinder(0.48,0.5,((i-(index-1)/2)*1.7,0,4.48))
    # Print vertically along the rail channel. No bridge or supports needed.
    test = test.rotate((90,0,0)).translate((0,4.73,3.5))
    return test


def export_checked(solid, name):
    assert solid.status() == md.Error.NoError, (name, solid.status())
    assert len(solid.decompose()) == 1, (name, 'disconnected geometry',[(p.volume(),p.bounding_box()) for p in solid.decompose()])
    data = solid.to_mesh()
    mesh = trimesh.Trimesh(vertices=np.asarray(data.vert_properties)[:,:3],
                           faces=np.asarray(data.tri_verts),process=True)
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0, name
    path = OUT / name
    mesh.export(path)
    # Independently reload the exact exported STL and inspect its topology.
    mesh = trimesh.load_mesh(path,process=True)
    edges = np.sort(np.asarray(mesh.edges),axis=1)
    _,counts = np.unique(edges,axis=0,return_counts=True)
    assert np.all(counts==2), (name,'non-manifold edges')
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0, name
    faces = np.asarray(mesh.vertices)[np.asarray(mesh.faces)]
    areas = np.linalg.norm(np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]),axis=1)/2
    assert areas.min()>1e-10, (name,'degenerate faces')
    assert len(mesh.split(only_watertight=False)) == 1, (name,'disconnected STL')
    return mesh, {
        'file':name,'extents_xyz_mm':mesh.extents.round(4).tolist(),
        'triangles':len(mesh.faces),'volume_mm3':round(float(mesh.volume),3),
        'watertight':bool(mesh.is_watertight),'consistent_winding':bool(mesh.is_winding_consistent),
        'connected_components':1,'all_edge_incidence_two':True,
        'minimum_triangle_area_mm2':float(areas.min()),
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'physical_fit_tested':False,
    }


def plot_mesh(ax, mesh, elev, azim, title):
    vertices = np.asarray(mesh.vertices)
    faces = vertices[np.asarray(mesh.faces)]
    normals = np.asarray(mesh.face_normals)
    light = np.array([-0.45,-0.55,0.85]); light /= np.linalg.norm(light)
    shade = 0.5 + 0.5*np.maximum(0,normals@light)
    colors = np.array([0.65,0.66,0.59])[None,:]*shade[:,None]
    ax.add_collection3d(Poly3DCollection(faces,facecolors=colors,edgecolors='none',antialiased=False,zsort='average'))
    lo,hi = mesh.bounds
    center = (lo+hi)/2
    radius = max(hi-lo)/2+2
    ax.set(xlim=(center[0]-radius,center[0]+radius),
           ylim=(center[1]-radius,center[1]+radius),zlim=(center[2]-radius,center[2]+radius))
    ax.set_box_aspect((1,1,1),zoom=1.4)
    ax.view_init(elev=elev,azim=azim)
    ax.set_axis_off()
    ax.set_title(title,fontsize=13,pad=0,color='#26332e')


def preview(mesh, coupon):
    plt.rcParams['font.family']='DejaVu Sans'
    fig=plt.figure(figsize=(14,10),facecolor='#f5f3ed')
    for i,(elev,azim,title) in enumerate([(52,-55,'Front and top'),(34,126,'Rear and top'),
                                         (-32,-61,'Underside slide-on mount')],1):
        ax=fig.add_subplot(2,2,i,projection='3d',facecolor='#f5f3ed')
        plot_mesh(ax,mesh,elev,azim,title)
    ax=fig.add_subplot(2,2,4,facecolor='#f5f3ed')
    w=7.4; th=w-1.6
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon([(-5.6,0),(5.6,0),(5.6,4.4),(-5.6,4.4)],color='#9b9475'))
    ax.add_patch(Polygon([(-th/2,-0.1),(th/2,-0.1),(th/2,0.8),(w/2,1.6),(w/2,2.8),
                          (-w/2,2.8),(-w/2,1.6),(-th/2,0.8)],color='#f5f3ed'))
    ax.annotate('',xy=(-w/2,2.1),xytext=(w/2,2.1),arrowprops=dict(arrowstyle='<->',color='#315e64'))
    ax.text(0,2.3,'7.4 mm',ha='center',fontsize=12,color='#315e64')
    ax.text(0,-0.7,'Open underside',ha='center',fontsize=11,color='#26332e')
    ax.set(xlim=(-7,7),ylim=(-3.2,6.7),aspect='equal')
    ax.axis('off')
    ax.set_title('Provisional mount cross-section',fontsize=13,color='#26332e')
    ax.text(0,-2.2,'Test channels: 7.2 / 7.4 / 7.6 mm\nRail dimensions are not manufacturer-verified.',
            ha='center',fontsize=11,color='#5e625c',linespacing=1.6)
    fig.suptitle('PEQ-15 miniature | Photo-based revision 4',fontsize=22,color='#26332e',y=0.97)
    fig.text(.5,.915,'Original cosmetic sculpt  |  Solid body  |  Millimeters',ha='center',fontsize=12,color='#5e625c')
    fig.text(.5,.035,'Actual exported STL mesh. Exterior reconstructed from multiple reference photographs. Fit remains untested.',
             ha='center',fontsize=11,color='#5e625c')
    fig.subplots_adjust(top=.88,bottom=.07,wspace=.02,hspace=.03)
    fig.savefig(OUT/'preview.png',dpi=165,facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    body=build_body()
    results=[]
    for index,width in enumerate([7.2,7.4,7.6],1):
        key=f'{width:.1f}'.replace('.','p')
        solid=body+mount(width)
        mesh,audit=export_checked(solid,f'peq15_channel_{key}mm.stl')
        audit['channel_max_width_mm']=width
        results.append(audit)
        coupon,c_audit=export_checked(fit_coupon(width,index),f'fit_test_{index}dot_{key}mm.stl')
        results.append(c_audit)
        if index==2:
            preview(mesh,coupon)
    (OUT/'mesh_validation.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
