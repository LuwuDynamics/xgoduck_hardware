"""Export the upstream MuJoCo standing pose as individual world-space STLs.

The input remains in xgoduck_rl_reference. Outputs are for local inspection;
this script does not modify or claim ownership of the upstream assets.
"""
import json, os, struct
import numpy as np
import mujoco

ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(ROOT, 'xgoduck_rl_reference', 'src', 'mjlab_microduck', 'robot', 'xgoduck')
OUT = os.path.join(ROOT, 'xgoduck_freecad_reference')
STLS = os.path.join(OUT, 'posed_meshes')
os.makedirs(STLS, exist_ok=True)
model = mujoco.MjModel.from_xml_path(os.path.join(MODEL, 'scene_walk.xml'))
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model,data,model.key('STAND').id)
mujoco.mj_forward(model,data)
manifest=[]
for geom_id in range(model.ngeom):
    if model.geom_type[geom_id] != mujoco.mjtGeom.mjGEOM_MESH or model.geom_group[geom_id] != 2:
        continue
    mesh_id = int(model.geom_dataid[geom_id])
    mesh_name = model.mesh(mesh_id).name
    va, vn = int(model.mesh_vertadr[mesh_id]), int(model.mesh_vertnum[mesh_id])
    fa, fn = int(model.mesh_faceadr[mesh_id]), int(model.mesh_facenum[mesh_id])
    vertices = np.asarray(model.mesh_vert[va:va+vn], dtype=float)
    faces = np.asarray(model.mesh_face[fa:fa+fn], dtype=int)
    rotation = data.geom_xmat[geom_id].reshape(3,3)
    world_mm = (vertices @ rotation.T + data.geom_xpos[geom_id]) * 1000
    triangles = world_mm[faces]
    path=os.path.join(STLS,mesh_name+'.stl')
    with open(path,'wb') as f:
        f.write(b'XGO-Duck upstream model - transformed for FreeCAD'.ljust(80,b' '))
        f.write(struct.pack('<I',len(triangles)))
        for triangle in triangles:
            normal=np.cross(triangle[1]-triangle[0],triangle[2]-triangle[0])
            length=float(np.linalg.norm(normal))
            normal=normal/length if length else normal
            f.write(struct.pack('<12fH',*(normal.tolist()+triangle.flatten().tolist()),0))
    manifest.append({'name':mesh_name,'source_body':model.body(model.geom_bodyid[geom_id]).name,
                     'triangles':len(triangles),'bounds_mm':np.round([world_mm.min(axis=0),world_mm.max(axis=0)],3).tolist()})
if len(manifest)!=15:
    raise RuntimeError('Expected 15 visual link meshes, got %d' % len(manifest))
with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump(manifest,f,indent=2)
print('Exported %d links in original STAND pose, with metres converted to millimetres.'%len(manifest))
