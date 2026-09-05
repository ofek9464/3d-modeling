import bpy,struct,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parents[1]/'generated'
scene=bpy.context.scene
assert set(bpy.data.objects.keys())=={'Cube','Camera','Light'}
for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
materials=[]
for name,color in [('ivory',(.85,.85,.8,1)),('green',(.018,.14,.07,1)),('black',(.008,.008,.008,1)),('gold',(.48,.42,.08,1))]:
    mat=bpy.data.materials.new('MAT-'+name);mat.diffuse_color=color;mat.use_nodes=True
    shader=mat.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=color
    shader.inputs['Roughness'].default_value=.65;materials.append(mat)
geo=json.loads((OUT/'logo_geometry.json').read_text())
masks={}
for name in ['green','gold']:
    im=bpy.data.images.load(str(OUT/(name+'_source_mask.png')))
    masks[name]=(im.size[:],list(im.pixels[:]))
def hit(name,x,y):
    size,pixels=masks[name];w,h=size
    px=round(x/geo['scale']+geo['cx']);py=round(-(y+1)/geo['scale']+geo['cy'])
    return 0<=px<w and 0<=py<h and pixels[((h-1-py)*w+px)*4]>.5
for fname,offset in [('keychain_front_glue_half.stl',-35),('keychain_qr_glue_half.stl',35)]:
    raw=(OUT/fname).read_bytes();vertices=[];faces=[];lookup={}
    for i in range(struct.unpack_from('<I',raw,80)[0]):
        values=struct.unpack_from('<12fH',raw,84+i*50);face=[]
        for j in [3,6,9]:
            v=tuple(values[j:j+3])
            if v not in lookup:lookup[v]=len(vertices);vertices.append(v)
            face.append(lookup[v])
        faces.append(face)
    mesh=bpy.data.meshes.new(fname);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new('GEO-'+fname,mesh);scene.collection.objects.link(obj);obj.location.x=offset
    for mat in materials:mesh.materials.append(mat)
    for p in mesh.polygons:
        x,y,z=p.center
        if offset<0 and z>1.61:p.material_index=1 if hit('green',x,y) else 3 if hit('gold',x,y) else 2
        elif offset>0 and 1.05<z<1.59:p.material_index=2
    obj['note']='Preview colors indicate paint; STL geometry contains no color.'
camera_data=bpy.data.cameras.new('CAM-both-sides');camera=bpy.data.objects.new('CAM-both-sides',camera_data);scene.collection.objects.link(camera)
scene.camera=camera;camera.location=(0,-65,155);target=Vector((0,2,0))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera_data.type='ORTHO';camera_data.ortho_scale=146
for name,loc,energy,size in [('key',(-40,-40,100),100000,80),('fill',(65,25,85),65000,70)]:
    data=bpy.data.lights.new('LGT-'+name,'AREA');data.energy=energy;data.size=size
    obj=bpy.data.objects.new('LGT-'+name,data);scene.collection.objects.link(obj);obj.location=loc
    obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
scene.world.color=(.3,.3,.3);scene.render.engine='CYCLES';scene.cycles.samples=48
scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=850
scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'preview.png')
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'keychain.blend'))
