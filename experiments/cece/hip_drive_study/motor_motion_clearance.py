"""Check approximate motor cases, shafts, turrets and hip horns in stance poses.

Neither the shaft locations nor the horn proxy are measured from the purchased
parts. Solid intersection samples do not validate print tolerances or dynamics.
"""
from pathlib import Path
import contextlib,io,json,runpy,sys
import numpy as np
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):e=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,legs,body=e['feet'],e['legs'],e['body'];rot,overlap=e['rot'],e['intersect']
import trimesh
def box(size,center):
    obj=trimesh.creation.box(extents=size);obj.apply_translation(center);return obj
def cyl(radius,ends):return trimesh.creation.cylinder(radius=radius,segment=np.array(ends),sections=48)
proxies={}
for side,x in [('left',-25.5),('right',25.5)]:
    proxies[side]={
      'hip_case':box((12.2,23,22),(x,-5.5,-24)),
      'hip_turret':cyl(5.5,[[x,0,-39],[x,0,-35]]),
      'hip_shaft':cyl(2.,[[x,0,-44],[x,0,-39]]),
      'hip_horn_box':box((3,15,2),(x,0,-43)),
      'ankle_case':box((12.2,22.5,23),(x,-3.5,-62)),
      'ankle_turret':cyl(6.1,[[x,7.75,-71.5],[x,12.75,-71.5]]),
      'ankle_shaft':cyl(2.4,[[x,12.75,-71.5],[x,21,-71.5]])}

def moved(m,T):q=m.copy();q.apply_transform(T);return q
result={'scope':'22 sampled tilted-body/one-foot poses, with motor and hip horn proxies',
 'collisions':[],'poses_checked':0,
 'limits':['Case/shaft/turret and 3x15x2 hip horn are approximate, not measured purchased parts',
  'Hip horn/shaft and servo-to-case contacts are intentionally omitted',
  'Only specified pairs are tested; not continuous and not dynamic',
  'Servo mounting ears, screw heads, cable exit and real actuator hardware are not represented']}
for stance,theta in [('left',-12),('right',12)]:
    swing='right' if stance=='left' else 'left'
    xs=-25.5 if stance=='left' else 25.5;xw=-xs
    B=rot(theta,[0,1,0],[xs,0,-71.5])
    for yaw in range(-10,11,2):
        S=rot(yaw,[0,0,1],[xs,0,-40]);Y=rot(-yaw,[0,0,1],[xw,0,-40]);C=rot(-theta,[0,1,0],[xw,0,-71.5])
        torso=B@S;swing_leg=torso@Y;swing_foot=swing_leg@C
        moving_body=moved(body,torso)
        frame={stance:{'leg':moved(legs[stance],B),'foot':feet[stance], 'leg_transform':B},
               swing:{'leg':moved(legs[swing],swing_leg),'foot':moved(feet[swing],swing_foot),'leg_transform':swing_leg}}
        violations={}
        for side in ('left','right'):
            other='right' if side=='left' else 'left'
            leg=frame[side]['leg'];foot=frame[side]['foot'];legT=frame[side]['leg_transform']
            for kind,p in proxies[side].items():
                T=legT if kind.startswith('ankle') or kind=='hip_horn_box' else torso
                geom=moved(p,T)
                pairs={'leg':leg,'own_foot':foot,'other_foot':frame[other]['foot']}
                if kind.startswith('ankle') or kind=='hip_horn_box':pairs['body']=moving_body
                for target,solid in pairs.items():
                    vol=overlap(geom,solid)
                    if vol>0.01:violations[f'{side}_{kind}__{target}']=round(vol,4)
        result['poses_checked']+=1
        if violations:result['collisions'].append({'stance':stance,'yaw_deg':yaw,'overlap_mm3':violations})
(HERE/'motor_motion_clearance_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
