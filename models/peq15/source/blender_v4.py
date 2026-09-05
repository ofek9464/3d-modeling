"""Finish, export, and render the cosmetic miniature in Blender, in mm."""
import bpy, math, json, struct
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/blender'
STAGE=ROOT/'generated/stage'
OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
# This process is launched with --factory-startup for this new project only.
assert set(bpy.data.objects.keys())=={'Cube','Camera','Light'}
for obj in list(bpy.data.objects): bpy.data.objects.remove(obj,do_unlink=True)
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=.001
scene.unit_settings.length_unit='MILLIMETERS'
models=[]
def import_exact_stl(source):
    # Preserve small valid CAD triangles that Blender's STL importer drops.
    raw=source.read_bytes(); count=struct.unpack_from('<I',raw,80)[0]
    vertices=[]; faces=[]; lookup={}
    for i in range(count):
        vals=struct.unpack_from('<12fH',raw,84+50*i)
        face=[]
        for j in (3,6,9):
            xyz=tuple(vals[j:j+3])
            if xyz not in lookup:
                lookup[xyz]=len(vertices); vertices.append(xyz)
            face.append(lookup[xyz])
        faces.append(face)
    mesh=bpy.data.meshes.new('CAD-triangles');mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new('GEO-'+source.stem,mesh);scene.collection.objects.link(obj)
    for old in bpy.context.selected_objects: old.select_set(False)
    obj.select_set(True);bpy.context.view_layer.objects.active=obj
    return obj
for source in sorted(STAGE.glob('*.stl')):
    obj=import_exact_stl(source)
    obj.name='GEO-'+source.stem
    bpy.ops.wm.stl_export(filepath=str(OUT/source.name),export_selected_objects=True,
                          apply_modifiers=True,global_scale=1.0,use_scene_unit=False)
    obj.hide_render=True; obj.hide_set(True)
    models.append(obj)
# Re-import the exact exported main STL for all render evidence.
for obj in bpy.context.selected_objects: obj.select_set(False)
hero=import_exact_stl(OUT/'peq15_channel_7p4mm.stl'); hero.name='GEO-print-preview-7p4'
mat=bpy.data.materials.new('MAT-olive-print-resin'); mat.diffuse_color=(.34,.35,.26,1)
mat.use_nodes=True
bsdf=mat.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value=(.34,.35,.26,1)
bsdf.inputs['Roughness'].default_value=.68
hero.data.materials.append(mat)
scene.render.engine='CYCLES'; scene.cycles.device='CPU'
scene.cycles.samples=32; scene.cycles.use_denoising=True
scene.render.resolution_x=960; scene.render.resolution_y=960
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=True
scene.world.color=(.35,.35,.35)
scene.view_settings.view_transform='AgX'
target=Vector((0,-1,7))
camdata=bpy.data.cameras.new('CAM-inspection')
cam=bpy.data.objects.new('CAM-inspection',camdata); scene.collection.objects.link(cam)
scene.camera=cam; camdata.type='ORTHO'; camdata.ortho_scale=49
for name,loc,power,size in [('key',(20,-35,65),45000,45),('fill',(-40,-15,35),14000,40),('rim',(10,45,40),28000,30)]:
    data=bpy.data.lights.new('LGT-'+name,'AREA'); data.energy=power; data.shape='DISK';data.size=size
    obj=bpy.data.objects.new('LGT-'+name,data);scene.collection.objects.link(obj)
    obj.location=loc; obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
views=[('front',(48,-65,61)),('rear',(-48,65,50)),('top',(0,0,90)),('underside',(45,-60,-42))]
for name,loc in views:
    cam.location=loc; cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(OUT/(name+'.png'))
    bpy.ops.render.render(write_still=True)
cam.location=views[0][1]; cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=58
        area.spaces.active.region_3d.view_location=target
        area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'peq15_v4.blend'))
print('V4_BLENDER_COMPLETE',bpy.app.version_string)
