"""Screen landing and return to two-foot support after a small hip-driven step.

Stationary samples with assumed geometry; no time evolution or contact forces.
"""
from pathlib import Path
import contextlib,io,json,runpy
import numpy as np
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):e=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,soles,rows,legs,body=e['feet'],e['soles'],e['rows'],e['legs'],e['body']
rot,point,intersect,margin,hull=e['rot'],e['point'],e['intersect'],e['signed_margin_mm'],e['polygon_hull']
floor=e['floor']
out={'scope':'sampled landing and return to two-foot support after 10 degree stance hip yaw',
 'limits':['Sampled static configurations, no force equilibrium, timing, friction or servo torque',
  'Ideal floor and approximated axes; no actual horn, wires, screw, surface compliance or measured masses',
  'Model lacks full cycle linking second stance frame and actual hardware'], 'poses':[]}
for stance,sign in [('left',-1),('right',1)]:
 swing='right' if stance=='left' else 'left';xs=-25.5 if stance=='left' else 25.5;xw=-xs;hip=sign*10
 def transforms(theta,comp):
    B=rot(theta,[0,1,0],[xs,0,-71.5]);S=rot(hip,[0,0,1],[xs,0,-40]);Y=rot(-hip,[0,0,1],[xw,0,-40]);C=rot(comp,[0,1,0],[xw,0,-71.5])
    return B,B@S,B@S@Y,B@S@Y@C
 def gap(theta,comp):
    *_,T=transforms(theta,comp);v=feet[swing].vertices;return float((v@T[:3,:3].T+T[:3,3])[:,2].min()-floor)
 def root(theta):
    grid=np.linspace(-45,45,361);vals=[gap(theta,c) for c in grid];solutions=[]
    for i in range(len(grid)-1):
        if vals[i]*vals[i+1]>0:continue
        lo,hi=grid[i],grid[i+1];a=vals[i]
        for _ in range(25):
            mid=(lo+hi)/2;v=gap(theta,mid)
            if a*v<=0:hi=mid
            else:lo=mid;a=v
        s=(lo+hi)/2
        if not any(abs(s-q)<.01 for q in solutions):solutions.append(s)
    if not solutions:raise ValueError(f'No ground contact for {stance} {theta}')
    return min(solutions,key=lambda q:abs(q+theta))
 def measure(phase,theta,comp):
    B,torso,sleg,T=transforms(theta,comp);total=np.zeros(3);mass=0.
    for row in rows:
        n=row['name'].lower()
        if n==f'{stance}_foot':M=np.eye(4)
        elif n==f'{swing}_foot':M=T
        elif n in (f'{stance}_leg',f'{stance}_washer',f'{stance}_ankle_servo'):M=B
        elif n in (f'{swing}_leg',f'{swing}_washer',f'{swing}_ankle_servo'):M=sleg
        else:M=torso
        mass+=row['mass_g'];total+=row['mass_g']*point(M,row['center_mm'])
    com=total/mass
    f=feet[swing].copy();f.apply_transform(T)
    l=legs[swing].copy();l.apply_transform(sleg)
    sl=legs[stance].copy();sl.apply_transform(B)
    b=body.copy();b.apply_transform(torso)
    z=float(f.bounds[0,2]-floor); contacts=f.vertices[f.vertices[:,2]<=floor+.03]
    support=hull(list(soles[stance])+[(p[0],p[1]) for p in contacts]) if len(contacts) else soles[stance]
    return {'phase':phase,'stance':stance,'body_roll_deg':round(theta,3),'stance_hip_yaw_deg':hip,
      'swing_hip_yaw_deg':-hip,'swing_ankle_deg':round(float(comp),3),'floor_clearance_mm':round(z,4),
      'support_margin_mm':round(margin(com[:2],support),3),
      'swing_foot_vs_stance_foot_mm3':round(intersect(f,feet[stance]),4),
      'swing_foot_vs_own_leg_mm3':round(intersect(f,l),4),
      'swing_foot_vs_stance_leg_mm3':round(intersect(f,sl),4),
      'stance_foot_vs_own_leg_mm3':round(intersect(feet[stance],sl),4),
      'swing_foot_vs_body_mm3':round(intersect(f,b),4),
      'swing_leg_vs_body_mm3':round(intersect(l,b),4),
      'stance_leg_vs_body_mm3':round(intersect(sl,b),4)}
 theta=sign*12;contact=root(theta)
 for c in np.linspace(-theta,contact,12):out['poses'].append(measure('lower_foot',theta,c))
 for d in (10,8,6,4,2,0):
    theta=sign*d;out['poses'].append(measure('return_two_foot',theta,root(theta)))
(HERE/'touchdown_pose_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
