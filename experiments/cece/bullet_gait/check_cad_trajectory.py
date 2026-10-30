"""Check actual STL geometry against Bullet link poses at sampled timestamps.

The physics model itself used simplified collision shapes and disabled robot
self-collision. This independent check uses manifold mesh intersections on the
revised body, legs and feet. Discrete samples are not continuous clearance.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy.spatial.transform import Rotation
HERE=Path(__file__).resolve().parent;CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
import trimesh
study=CECE/'hip_drive_study'
paths={'base':CECE/'packaging_study/head_body_joint/Cece_body_V4_four_screw_joint_CANDIDATE.stl',
 'left_leg':study/'Cece_left_leg_hip_slot_TEST_ONLY.stl',
 'right_leg':study/'Cece_right_leg_hip_slot_TEST_ONLY.stl',
 'left_foot':study/'Cece_left_wide_foot_clearance_TEST_ONLY.stl',
 'right_foot':study/'Cece_right_wide_foot_clearance_TEST_ONLY.stl'}
meshes={n:trimesh.load(p,force='mesh') for n,p in paths.items()}
for n,m in meshes.items():
 if not m.is_watertight or not m.is_volume:raise RuntimeError('Invalid mesh '+n)
origins={'base':[0,0,0],'left_leg':[-25.5,0,-40],'left_foot':[-25.5,0,-71.5],
 'right_leg':[25.5,0,-40],'right_foot':[25.5,0,-71.5]}
pairs=[('base','left_leg'),('base','right_leg'),('base','left_foot'),('base','right_foot'),
 ('left_leg','right_leg'),('left_leg','left_foot'),('right_leg','right_foot'),
 ('left_leg','right_foot'),('right_leg','left_foot'),('left_foot','right_foot')]
trace_path=HERE/'bullet_geometry_trace_results.json'
data=json.loads(trace_path.read_text(encoding='utf-8'))
if not data['model']['geometry_trace']:raise ValueError('No geometry trace')
def move(mesh,frame,origin):
 R=Rotation.from_quat(frame['quaternion_xyzw']).as_matrix();T=np.eye(4);T[:3,:3]=R
 T[:3,3]=np.asarray(frame['position_m'])*1000-R@np.asarray(origin)
 x=mesh.copy();x.apply_transform(T);return x
def overlap(a,b):
 if (a.bounds[1]<=b.bounds[0]).any() or (b.bounds[1]<=a.bounds[0]).any():return 0.
 c=trimesh.boolean.intersection([a,b],engine='manifold')
 return 0. if c.is_empty else abs(float(c.volume))
out={'scope':'discrete manifold-mesh overlap of ten body/leg/foot pairs along Bullet trajectory',
 'trace_rate_hz':data['model']['trace_hz'],'sample_count':len(data['trace']),
 'collision_threshold_mm3':.01,'collision_samples':[],'max_overlap_mm3':{},
 'limits':['Body, leg and foot STL solids only; not camera/head geometry, servo horns, ears, screws or cables',
  'This is sampled at fixed intervals, not continuous collision detection',
  'Bullet has no dynamic self-collision and assumes simplified floor contacts',
  'Real parts, print tolerance, loads and electronics remain unverified'],
 'source_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},
 'trace_sha256':hashlib.sha256(trace_path.read_bytes()).hexdigest()}
for i,sample in enumerate(data['trace']):
 frames=sample['cad_link_frames'];world={n:move(m,frames[n],origins[n]) for n,m in meshes.items()}
 clashes={}
 for a,b in pairs:
  v=overlap(world[a],world[b])
  if v>.01:
   key=f'{a}__{b}';clashes[key]=round(v,4);out['max_overlap_mm3'][key]=max(out['max_overlap_mm3'].get(key,0),round(v,4))
 if clashes:out['collision_samples'].append({'t_s':sample['t_s'],'half_step':sample['half_step'],
                                            'phase':sample['phase'],'overlap_mm3':clashes})
 if (i+1)%100==0:print(f'checked {i+1}/{len(data["trace"])}',flush=True)
out['colliding_sample_count']=len(out['collision_samples'])
(HERE/'cad_trajectory_clearance_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='collision_samples'},indent=2),flush=True)
