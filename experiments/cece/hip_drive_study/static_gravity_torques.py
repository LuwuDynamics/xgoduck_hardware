"""Compute partial-load static gravity moments for the single-foot yaw poses.

These are ideal gravity moments about assumed joint axes, not motor torque
measurements and not a dynamic simulation. Input masses omit several boards,
wires, connectors and fasteners; speaker/camera mass are sensitivity values.
"""
from pathlib import Path
import contextlib,io,json,runpy
import numpy as np

HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    e=runpy.run_path(str(HERE/'stance_pose_check.py'))
rows=e['rows'];rot=e['rot'];point=e['point']
G=np.array([0.,0.,-9.80665]);out=[]

for stance,theta in [('left',-12),('right',12)]:
    swing='right' if stance=='left' else 'left'
    xs=-25.5 if stance=='left' else 25.5;xw=-xs
    B=rot(theta,[0,1,0],[xs,0,-71.5])
    for yaw in range(-10,11,2):
        S=rot(yaw,[0,0,1],[xs,0,-40])
        Y=rot(-yaw,[0,0,1],[xw,0,-40])
        C=rot(-theta,[0,1,0],[xw,0,-71.5])
        torso=B@S;swing_leg=torso@Y;swing_foot=swing_leg@C
        axes={
          'stance_ankle':(np.array([xs,0.,-71.5]),np.array([0.,1.,0.])),
          'stance_hip':(point(B,[xs,0,-40]),B[:3,:3]@np.array([0.,0.,1.])),
          'swing_hip':(point(torso,[xw,0,-40]),torso[:3,:3]@np.array([0.,0.,1.])),
          'swing_ankle':(point(swing_leg,[xw,0,-71.5]),swing_leg[:3,:3]@np.array([0.,1.,0.]))}
        moments={key:0. for key in axes}
        for row in rows:
            name=row['name'].lower();m=row['mass_g']/1000.
            if name==f'{stance}_foot':T=np.eye(4);parents=[]
            elif name==f'{swing}_foot':T=swing_foot;parents=list(axes)
            elif name in (f'{stance}_leg',f'{stance}_washer',f'{stance}_ankle_servo'):
                T=B;parents=['stance_ankle']
            elif name in (f'{swing}_leg',f'{swing}_washer',f'{swing}_ankle_servo'):
                T=swing_leg;parents=['stance_ankle','stance_hip','swing_hip']
            else:T=torso;parents=['stance_ankle','stance_hip']
            r=point(T,row['center_mm'])/1000.
            for key in parents:
                origin,axis=axes[key];torque=np.cross(r-origin/1000.,m*G)
                moments[key]+=float(torque@axis)
        out.append({'stance':stance,'stance_hip_yaw_deg':yaw,
                    'gravity_moments_Nm':{k:round(v,5) for k,v in moments.items()}})
report={'scope':'ideal static gravity moments in 22 single-support positions',
        'total_modeled_mass_g':round(sum(x['mass_g'] for x in rows),3),
        'sg90_seller_holding_rating_Nm_at_4p8V':0.1765,
        'poses':out,
        'max_abs_gravity_moment_Nm':{k:round(max(abs(p['gravity_moments_Nm'][k]) for p in out),5)
                                     for k in out[0]['gravity_moments_Nm']},
        'limitations':['Not a motor operating rating or proof of adequate torque; the published number is a holding figure',
         'No acceleration, speed/torque curve, inertia, friction, impacts, losses, control or electrical sag',
         'Actual servo shaft positions and horn stiffness unknown; outputs are ideal revolute joints',
         'Includes hypothetical 10g camera and 12g speaker; excludes other boards, wires, screws and mounts',
         'Single-support only; edge-transfer forces and loads are not calculated']}
(HERE/'static_gravity_torque_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
