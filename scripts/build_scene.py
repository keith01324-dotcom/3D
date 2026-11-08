"""Deterministic plan-to-blend assembly, not automatic photo inference."""
import argparse, json, math
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--plan', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
plan_path = Path(a.plan).resolve()
plan = json.loads(plan_path.read_text(encoding='utf-8'))
out = Path(a.output).resolve()
out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
collections = {}
for spec in plan['objects']:
    name = spec['name']
    group = spec['collection']
    if group not in collections:
        col = bpy.data.collections.new(group)
        scene.collection.children.link(col)
        collections[group] = col
    if 'asset' in spec:
        asset = (plan_path.parent / spec['asset']).resolve()
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=str(asset))
        imported = set(bpy.data.objects) - before
        root = bpy.data.objects.new(name, None)
        collections[group].objects.link(root)
        for obj in imported:
            if obj.parent is None:
                obj.parent = root
            for col in list(obj.users_collection):
                col.objects.unlink(obj)
            collections[group].objects.link(obj)
        root.location = spec['location']
        root.scale = spec.get('scale', [1,1,1])
        root.rotation_euler = [math.radians(v) for v in spec.get('rotation_degrees', [0,0,0])]
    else:
        bpy.ops.mesh.primitive_cube_add(size=1, location=spec['location'])
        obj = bpy.context.object
        obj.name = name
        obj.dimensions = spec['dimensions']
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        for col in list(obj.users_collection):
            col.objects.unlink(obj)
        collections[group].objects.link(obj)
        mat = bpy.data.materials.new(name + '_Material')
        mat.diffuse_color = spec.get('color', [0.6,0.6,0.6,1])
        mat.use_nodes = True
        mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = mat.diffuse_color
        obj.data.materials.append(mat)
lighting = bpy.data.collections.new('Lighting')
scene.collection.children.link(lighting)
data = bpy.data.lights.new('Key', 'AREA')
data.energy = 1000
data.shape = 'DISK'
data.size = 5
light = bpy.data.objects.new('Key', data)
lighting.objects.link(light)
light.location = (1,-2,6)
camera_col = bpy.data.collections.new('Cameras')
scene.collection.children.link(camera_col)
for index, view in enumerate(plan['cameras']):
    data = bpy.data.cameras.new(view['name'])
    camera = bpy.data.objects.new(view['name'], data)
    camera_col.objects.link(camera)
    camera.location = view['location']
    camera.rotation_euler = (Vector(view.get('target', [0,0,1]))-camera.location).to_track_quat('-Z','Y').to_euler()
    data.lens = view.get('lens', 40)
    if index == 0:
        scene.camera = camera
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 8
scene.render.resolution_x = 640
scene.render.resolution_y = 480
scene.render.resolution_percentage = 100
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
for camera in camera_col.objects:
    scene.camera = camera
    scene.render.filepath = str(out/(camera.name+'.png'))
    bpy.ops.render.render(write_still=True)
print(json.dumps({'saved':str(out/'scene.blend'), 'objects':len(scene.objects)}))
