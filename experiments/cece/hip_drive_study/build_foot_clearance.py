"""Narrow inner foot edges by 1.5 mm, then sample simultaneous hip yaw.

The CAD axes and neutral ankles are assumptions. This is not a gait test.
"""
from pathlib import Path
import json,sys,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent; CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
import trimesh
def load(p):return trimesh.load(p,force='mesh')
def box(extents,center):
    m=trimesh.creation.box(extents=extents);m.apply_translation(center);return m
def intersect(a,b):
    if (a.bounds[1]<=b.bounds[0]).any() or (b.bounds[1]<=a.bounds[0]).any():return 0.0
    c=trimesh.boolean.intersection([a,b],engine='manifold')
    return 0.0 if c.is_empty else round(abs(float(c.volume)),5)
result={'status':'GEOMETRY TEST ONLY, no physical fit, servo strength or gait validation',
 'change':'Inner edge of each existing wide foot moved 1.5 mm outwards',
 'new_inner_edge_x_mm':[-5.5,5.5], 'feet':{},'simultaneous_hip_yaw_overlap_mm3':{},
 'limits':['Ankle and hip axes assumed; both ankles held neutral',
           'Sampled 5 degree intervals, not continuous and not a dynamic gait',
           'Reduced width changes single-foot support; recompute loaded center of mass',
           'Real servo horn, attachment, print tolerance, strength, torque and floor friction unverified']}
feet={}
for side,sgn in [('left',-1),('right',1)]:
    original=load(CECE/f'balance_study/wide_foot/Cece_{side}_wide_foot.stl')
    # Subtract everything on the inside of the new inner straight edge.
    cut=box((120,100,50),(-54.5 if sgn==1 else 54.5,0,-75))
    revised=trimesh.boolean.difference([original,cut],engine='manifold')
    out=HERE/f'Cece_{side}_wide_foot_clearance_TEST_ONLY.stl';revised.export(out);revised=load(out)
    if not revised.is_watertight or len(revised.split(only_watertight=False))!=1:
        raise ValueError(f'{side} foot failed mesh validation')
    feet[side]=revised
    result['feet'][side]={'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
      'watertight':True,'components':1,'original_volume_mm3':round(original.volume,3),
      'revised_volume_mm3':round(revised.volume,3),'bounds_mm':revised.bounds.tolist()}
angles=list(range(-30,31,5))
for a in angles:
    l=feet['left'].copy();l.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(a),[0,0,1],[-25.5,0,-40]))
    for b in angles:
        r=feet['right'].copy();r.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(b),[0,0,1],[25.5,0,-40]))
        value=intersect(l,r)
        if value>0:result['simultaneous_hip_yaw_overlap_mm3'][f'{a},{b}']=value
result['pose_count']=len(angles)**2
(HERE/'foot_clearance_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
