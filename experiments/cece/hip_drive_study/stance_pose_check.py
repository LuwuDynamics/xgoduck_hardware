"""Conservative CAD pose check, not a dynamic walking simulation.

Roll the entire robot about one fixed ankle, rotate the opposite hip and
counter-rotate its ankle. Measure static COM/support, floor clearance, and
selected mesh collisions. Omits unweighed hardware and deformations.
"""
from pathlib import Path
import json,sys
import numpy as np
HERE=Path(__file__).resolve().parent; CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
sys.path.insert(0,str(CECE/'balance_study'))
import trimesh
from balance_study import polygon_hull,read_binary_stl,signed_margin_mm

def load(path):return trimesh.load(path,force='mesh')
def rot(deg,axis,point):return trimesh.transformations.rotation_matrix(np.deg2rad(deg),axis,point)
def point(m,p):return (m@np.array([*p,1.]))[:3]
def intersect(a,b):
    if (a.bounds[1]<=b.bounds[0]).any() or (b.bounds[1]<=a.bounds[0]).any():return 0.
    c=trimesh.boolean.intersection([a,b],engine='manifold')
    return 0. if c.is_empty else abs(float(c.volume))

baseline=json.loads((CECE/'balance_study/latest_balance_results.json').read_text())
head=json.loads((CECE/'rounded_head_study/balance_sensitivity.json').read_text())
replaced={'body','head','face','antenna','speaker_pod','speaker_grille','left_leg','right_leg','left_foot','right_foot'}
rows=[{'name':p['name'],'mass_g':p['solid_PLA_mass_g'],'center_mm':p['center_mm']}
      for p in baseline['printed_parts'] if p['name'] not in replaced]
rows.extend(head['new_parts'])
feet={};legs={};soles={}
for side in ('left','right'):
    for kind in ('leg','foot'):
        f=HERE/f'Cece_{side}_{"leg_hip_slot" if kind=="leg" else "wide_foot_clearance"}_TEST_ONLY.stl'
        m=load(f);(legs if kind=='leg' else feet)[side]=m
        rows.append({'name':f'{side}_{kind}','mass_g':m.volume*.00124,'center_mm':m.center_mass.tolist()})
        if kind=='foot':
            v=read_binary_stl(f)['vertices']; zmin=min(q[2] for q in v)
            soles[side]=polygon_hull([(q[0],q[1]) for q in v if q[2]<=zmin+0.1])
rows+=baseline['included_hardware']
rows += [{'name':'speaker_sensitivity','mass_g':12,'center_mm':[0,32.5,17]},
         {'name':'camera_sensitivity','mass_g':10,'center_mm':[0,-29,38]}]
body=load(CECE/'packaging_study/head_body_joint/Cece_body_V4_four_screw_joint_CANDIDATE.stl')
floor=-89.02
result={'scope':'Static one-foot poses with assumed axes and partial load; no dynamics or torque',
 'floor_z_mm':floor,'camera_sensitivity_g':10,'speaker_sensitivity_g':12,'poses':[],
 'limits':['Camera/speaker masses are assumed; board/wire/screw masses excluded',
 'Yaw axis and servo centers are assumed, ankle pivots simplified, no horn or real servo geometry',
 'Only selected print mesh collisions, floor clearance and COM checked',
 'Gravity moment is for modeled mass excluding stance foot, not actual servo torque; support from other foot and all dynamic effects ignored',
 'No motor torque, friction, impacts, trajectory transitions or physical test']}
tests=[(s,sign*t,y,'lifted_step') for s,sign in [('left',-1),('right',1)] for t in (12,14) for y in (-10,0,10)]
tests += [(s,sign*t,0,'initial_weight_transfer') for s,sign in [('left',-1),('right',1)] for t in (0,2,4,6,8,10,12)]
for stance,theta,yaw,phase in tests:
    swing='right' if stance=='left' else 'left'
    xs=-25.5 if stance=='left' else 25.5; xw=-xs
    B=rot(theta,[0,1,0],[xs,0,-71.5])
    if True:
        Y=rot(yaw,[0,0,1],[xw,0,-40]); C=rot(-theta,[0,1,0],[xw,0,-71.5])
        swing_leg=B@Y; swing_foot=B@Y@C
        mass=0.;weighted=np.zeros(3);upper_mass=0.;upper_weighted_x=0.
        for row in rows:
            name=row['name'].lower()
            if name==f'{stance}_foot': t=np.eye(4)
            elif name==f'{swing}_foot': t=swing_foot
            elif name in (f'{swing}_leg',f'{swing}_washer',f'{swing}_ankle_servo'): t=swing_leg
            else:t=B
            mass+=row['mass_g'];weighted+=row['mass_g']*point(t,row['center_mm'])
            if name!=f'{stance}_foot':
                upper_mass+=row['mass_g']/1000
                upper_weighted_x+=(row['mass_g']/1000)*point(t,row['center_mm'])[0]
        com=weighted/mass
        other=feet[swing].copy();other.apply_transform(swing_foot)
        moving_leg=legs[swing].copy();moving_leg.apply_transform(swing_leg)
        stance_leg=legs[stance].copy();stance_leg.apply_transform(B)
        moving_body=body.copy();moving_body.apply_transform(B)
        result['poses'].append({'phase':phase,'stance':stance,'body_roll_deg':theta,'swing_hip_yaw_deg':yaw,
           'swing_ankle_compensation_deg':-theta,'total_included_mass_g':round(mass,2),
           'com_xyz_mm':np.round(com,3).tolist(),
           'gravity_moment_about_stance_ankle_Nm':round(abs(9.80665*(upper_weighted_x-upper_mass*xs)/1000),4),
           'stance_support_margin_mm':round(signed_margin_mm(com[:2],soles[stance]),3),
           'swing_sole_min_height_mm':round(float(other.bounds[0,2]-floor),3),
           'swing_foot_vs_stance_foot_mm3':round(intersect(other,feet[stance]),4),
           'swing_foot_vs_own_leg_mm3':round(intersect(other,moving_leg),4),
           'stance_foot_vs_own_leg_mm3':round(intersect(feet[stance],stance_leg),4),
           'swing_foot_vs_body_mm3':round(intersect(other,moving_body),4),
           'swing_leg_vs_stance_foot_mm3':round(intersect(moving_leg,feet[stance]),4),
           'swing_leg_vs_body_mm3':round(intersect(moving_leg,moving_body),4)})
(HERE/'stance_pose_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
