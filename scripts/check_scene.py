import argparse, json, math
from pathlib import Path
import bpy
p = argparse.ArgumentParser()
p.add_argument('--blend', required=True)
p.add_argument('--report', required=True)
p.add_argument('--plan', required=True)
a=p.parse_args()
bpy.ops.wm.open_mainfile(filepath=str(Path(a.blend).resolve()))
plan=json.loads(Path(a.plan).read_text(encoding='utf-8'))
objects=bpy.context.scene.objects
meshes=[o for o in objects if o.type=='MESH']
missing_objects=[o['name'] for o in plan['objects'] if o['name'] not in objects]
missing_textures=[i.filepath for i in bpy.data.images if i.source=='FILE' and not i.packed_file and not Path(bpy.path.abspath(i.filepath)).is_file()]
invalid=[o.name for o in objects if not all(math.isfinite(v) for row in o.matrix_world for v in row)]
report={'blender':bpy.app.version_string,'mesh_count':len(meshes),'materials':len(bpy.data.materials),'collections':[c.name for c in bpy.data.collections], 'cameras':[o.name for o in objects if o.type=='CAMERA'],'missing_objects':missing_objects,'missing_textures':missing_textures,'invalid_transforms':invalid}
report['passed']=bool(meshes and report['materials'] and len(report['cameras'])>=4 and not missing_objects and not missing_textures and not invalid and all(o['collection'] in bpy.data.collections for o in plan['objects']))
Path(a.report).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
raise SystemExit(0 if report['passed'] else 1)
