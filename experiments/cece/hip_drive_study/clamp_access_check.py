"""Check proposed side screw pilot and straight screwdriver envelopes."""
from pathlib import Path
import json,sys
import numpy as np
HERE=Path(__file__).resolve().parent;CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
import trimesh
def load(p):return trimesh.load(p,force='mesh')
def overlap(a,b):
    if (a.bounds[1]<=b.bounds[0]).any() or (b.bounds[1]<=a.bounds[0]).any():return 0.
    v=trimesh.boolean.intersection([a,b],engine='manifold')
    return 0. if v.is_empty else abs(float(v.volume))
body=load(CECE/'packaging_study/head_body_joint/Cece_body_V4_four_screw_joint_CANDIDATE.stl')
out={'scope':'Four proposed 1.8 mm pilot holes and 5 mm straight tool envelopes at neutral pose',
     'checks':[],'limits':['Assumed M2 screw, pilot printability, real screw head and tool unknown',
     'Screw-to-horn contact, grip, crushing, creep, torque and disassembly are not tested',
     'Only neutral-pose printed meshes checked; real servo, cables, nuts and hardware omitted']}
for side,x,sign in [('right',25.5,1),('left',-25.5,-1)]:
    leg=load(HERE/f'Cece_{side}_leg_hip_slot_TEST_ONLY.stl')
    foot=load(HERE/f'Cece_{side}_wide_foot_clearance_TEST_ONLY.stl')
    for y in (-5.5,5.5):
        core=trimesh.creation.cylinder(radius=.8,segment=np.array([[x+sign*1.9,y,-43.1],[x+sign*9.1,y,-43.1]]),sections=48)
        tool=trimesh.creation.cylinder(radius=2.5,segment=np.array([[x+sign*8.6,y,-43.1],[x+sign*24,y,-43.1]]),sections=48)
        out['checks'].append({'side':side,'y_mm':y,'pilot_core_vs_leg_mm3':round(overlap(core,leg),4),
          'tool_vs_leg_mm3':round(overlap(tool,leg),4),'tool_vs_body_mm3':round(overlap(tool,body),4),
          'tool_vs_foot_mm3':round(overlap(tool,foot),4)})
(HERE/'clamp_access_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
