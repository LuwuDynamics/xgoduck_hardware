"""Sample coordinated stance/swing hip yaw and single-foot support geometry.

All poses are static. This is not a dynamic or powered walking simulation.
"""
from pathlib import Path
import contextlib,io,json,runpy
import numpy as np
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()): e=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,soles,rows,legs,body=e['feet'],e['soles'],e['rows'],e['legs'],e['body']
rot,point,intersect,margin=e['rot'],e['point'],e['intersect'],e['signed_margin_mm']
floor=e['floor']
result={'scope':'Stationary samples of coordinated hip yaw with one planted foot',
 'limits':['Masses incomplete; camera and speaker are hypothetical sensitivity masses',
  'Approximate joint axes, no real horn, servo body/ears or flex geometry',
  'No torque, friction, contact force, motion between samples, dynamics or hardware test'], 'poses':[]}
for stance,theta in [('left',-12),('right',12)]:
 swing='right' if stance=='left' else 'left';xs=-25.5 if stance=='left' else 25.5;xw=-xs
 B=rot(theta,[0,1,0],[xs,0,-71.5])
 for hip in range(-10,11,2):
    S=rot(hip,[0,0,1],[xs,0,-40]);Y=rot(-hip,[0,0,1],[xw,0,-40]);C=rot(-theta,[0,1,0],[xw,0,-71.5])
    torso=B@S;swing_leg=torso@Y;swing_foot=swing_leg@C
    total=np.zeros(3);mass=0.
    for row in rows:
        name=row['name'].lower()
        if name==f'{stance}_foot':M=np.eye(4)
        elif name==f'{swing}_foot':M=swing_foot
        elif name in (f'{stance}_leg',f'{stance}_washer',f'{stance}_ankle_servo'):M=B
        elif name in (f'{swing}_leg',f'{swing}_washer',f'{swing}_ankle_servo'):M=swing_leg
        else:M=torso
        mass+=row['mass_g'];total+=row['mass_g']*point(M,row['center_mm'])
    com=total/mass
    foot=feet[swing].copy();foot.apply_transform(swing_foot)
    moving_leg=legs[swing].copy();moving_leg.apply_transform(swing_leg)
    grounded_leg=legs[stance].copy();grounded_leg.apply_transform(B)
    moving_body=body.copy();moving_body.apply_transform(torso)
    ankle=point(swing_leg,[xw,0,-71.5]);
    result['poses'].append({'stance':stance,'body_roll_deg':theta,'stance_hip_yaw_deg':hip,
     'swing_hip_yaw_deg':-hip,'swing_ankle_deg':-theta,
     'swing_ankle_y_mm':round(float(ankle[1]),3),
     'stance_support_margin_mm':round(margin(com[:2],soles[stance]),3),
     'swing_foot_floor_clearance_mm':round(float(foot.bounds[0,2]-floor),3),
     'swing_foot_vs_stance_foot_mm3':round(intersect(foot,feet[stance]),4),
     'swing_foot_vs_swing_leg_mm3':round(intersect(foot,moving_leg),4),
     'swing_foot_vs_stance_leg_mm3':round(intersect(foot,grounded_leg),4),
     'stance_foot_vs_stance_leg_mm3':round(intersect(feet[stance],grounded_leg),4),
     'swing_leg_vs_body_mm3':round(intersect(moving_leg,moving_body),4),
     'stance_leg_vs_body_mm3':round(intersect(grounded_leg,moving_body),4),
     'swing_foot_vs_body_mm3':round(intersect(foot,moving_body),4)})
(HERE/'stride_pose_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
