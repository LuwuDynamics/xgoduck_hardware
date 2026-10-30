"""Sample body and opposite-leg clashes during a neutral-ankle hip yaw sweep.

This checks geometry only. The hip axis is inferred from the current CAD;
the supplied servo output and horn have not been measured.
"""
import json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
import trimesh
def mesh(path):return trimesh.load(path,force='mesh')
def overlap(a,b):
    if (a.bounds[1]<=b.bounds[0]).any() or (b.bounds[1]<=a.bounds[0]).any():return 0.0
    value=trimesh.boolean.intersection([a,b],engine='manifold')
    return 0 if value.is_empty else round(abs(float(value.volume)),4)
body=mesh(CECE/'packaging_study/head_body_joint/Cece_body_V4_four_screw_joint_CANDIDATE.stl')
legs={s:mesh(HERE/f'Cece_{s}_leg_hip_slot_TEST_ONLY.stl') for s in ('left','right')}
feet={s:mesh(CECE/f'balance_study/wide_foot/Cece_{s}_wide_foot.stl') for s in ('left','right')}
report={'scope':'Single hip yaw with both ankle joints neutral; exact printed meshes, sampled static overlap',
        'degrees':[-30,-20,-10,0,10,20,30], 'results':{},
        'limits':['Hip axis assumed; horn and servo case not moving in this check',
                  'Floor contact, mass, torque, simultaneous hip movement, cable flex, and walking not simulated']}
for side,x,other in [('left',-25.5,'right'),('right',25.5,'left')]:
    report['results'][side]={}
    for deg in report['degrees']:
        t=trimesh.transformations.rotation_matrix(np.deg2rad(deg),[0,0,1],[x,0,-40])
        leg=legs[side].copy();leg.apply_transform(t)
        foot=feet[side].copy();foot.apply_transform(t)
        report['results'][side][str(deg)]={
            'leg_body':overlap(leg,body),'foot_body':overlap(foot,body),
            'leg_other_leg':overlap(leg,legs[other]),'leg_other_foot':overlap(leg,feet[other]),
            'foot_other_leg':overlap(foot,legs[other]),'foot_other_foot':overlap(foot,feet[other])}
(HERE/'hip_sweep_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
