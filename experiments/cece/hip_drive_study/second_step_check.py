"""Screen the second half-step using the first half-step's final placements.

Uses static rigid geometry, fixed foot contacts and assumed axes. It does not
simulate dynamics, real motors, friction or actual electronic masses.
"""
from pathlib import Path
import contextlib,io,json,runpy
import numpy as np
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):e=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,soles,rows,legs,body=e['feet'],e['soles'],e['rows'],e['legs'],e['body']
rot,point,intersect,margin,hull=e['rot'],e['point'],e['intersect'],e['signed_margin_mm'],e['polygon_hull']
floor=e['floor'];first_stance_x=-25.5;stance_x=25.5; stance='right';swing='left'
# First half-step ended with body yaw -10°, opposite hip +10°, feet flat.
S0=rot(-10,[0,0,1],[first_stance_x,0,-40]);Y0=rot(10,[0,0,1],[stance_x,0,-40]);SHIFT=S0@Y0
new_ankle=point(SHIFT,[stance_x,0,-71.5]);new_hip=point(SHIFT,[stance_x,0,-40])
support_stance=feet[stance].copy();support_stance.apply_transform(SHIFT)
contact_vertices=support_stance.vertices[support_stance.vertices[:,2]<=floor+.1]
support=hull([(p[0],p[1]) for p in contact_vertices])

def transforms(theta,phi,comp):
    B=rot(theta,[0,1,0],new_ankle);S=rot(phi,[0,0,1],new_hip)
    Y=rot(-phi,[0,0,1],[first_stance_x,0,-40]);C=rot(comp,[0,1,0],[first_stance_x,0,-71.5])
    return B,B@SHIFT,B@S@S0,B@S@Y,B@S@Y@C
def coords(theta,phi,comp):
    *_,T=transforms(theta,phi,comp);v=feet[swing].vertices
    return v@T[:3,:3].T+T[:3,3]
def gap(theta,phi,comp):return float(coords(theta,phi,comp)[:,2].min()-floor)
def root(theta,phi):
    grid=np.linspace(-45,45,361);vals=[gap(theta,phi,c) for c in grid];candidates=[]
    for i in range(len(grid)-1):
        if vals[i]*vals[i+1]>0:continue
        lo,hi=grid[i],grid[i+1];a=vals[i]
        for _ in range(25):
            mid=(lo+hi)/2;v=gap(theta,phi,mid)
            if a*v<=0:hi=mid
            else:lo=mid;a=v
        s=(lo+hi)/2
        if not any(abs(s-q)<.01 for q in candidates):candidates.append(s)
    if not candidates:raise ValueError(f'no root at roll {theta}, yaw {phi}')
    return min(candidates,key=lambda x:abs(x+theta))

out={'scope':'second half-step after first forward foot placement, sampled static poses',
 'first_right_foot_shift_mm':np.round(SHIFT[:3,3],3).tolist(),
 'limits':['Assumed axes, partial masses, ideal rigid floor and selected printed-mesh intersections',
 'No dynamic stability, friction, torque, force feasibility, current or real mechanical interfaces',
 'This is not a validated repeatable continuous gait or a real walking test'], 'poses':[]}
def measure(phase,theta,phi,comp):
    B,stance_leg,torso,sleg,T=transforms(theta,phi,comp);total=np.zeros(3);mass=0.
    for row in rows:
        n=row['name'].lower()
        if n==f'{stance}_foot':M=SHIFT
        elif n==f'{swing}_foot':M=T
        elif n in (f'{stance}_leg',f'{stance}_washer',f'{stance}_ankle_servo'):M=stance_leg
        elif n in (f'{swing}_leg',f'{swing}_washer',f'{swing}_ankle_servo'):M=sleg
        else:M=torso
        mass+=row['mass_g'];total+=row['mass_g']*point(M,row['center_mm'])
    com=total/mass
    f=feet[swing].copy();f.apply_transform(T)
    l=legs[swing].copy();l.apply_transform(sleg)
    sl=legs[stance].copy();sl.apply_transform(stance_leg)
    b=body.copy();b.apply_transform(torso)
    z=float(f.bounds[0,2]-floor); contact=f.vertices[f.vertices[:,2]<=floor+.03]
    poly=hull(list(support)+[(p[0],p[1]) for p in contact]) if len(contact) else support
    return {'phase':phase,'roll_deg':round(theta,3),'stance_hip_change_deg':round(phi,3),
      'swing_ankle_deg':round(float(comp),3),'floor_clearance_mm':round(z,4),
      'swing_ankle_world_mm':np.round(point(sleg,[first_stance_x,0,-71.5]),3).tolist(),
      'support_margin_mm':round(margin(com[:2],poly),3),
      'foot_vs_stance_foot_mm3':round(intersect(f,support_stance),4),
      'foot_vs_swing_leg_mm3':round(intersect(f,l),4),
      'foot_vs_stance_leg_mm3':round(intersect(f,sl),4),
      'stance_foot_vs_stance_leg_mm3':round(intersect(support_stance,sl),4),
      'foot_vs_body_mm3':round(intersect(f,b),4),
      'swing_leg_vs_body_mm3':round(intersect(l,b),4),
      'stance_leg_vs_body_mm3':round(intersect(sl,b),4)}

for theta in (0,2,4,6,8,10,12):out['poses'].append(measure('transfer',theta,0,root(theta,0)))
start=root(12,0)
for comp in np.linspace(start,-12,12):out['poses'].append(measure('lift',12,0,comp))
for phi in range(0,21,2):out['poses'].append(measure('swing',12,phi,-12))
contact=root(12,20)
for comp in np.linspace(-12,contact,12):out['poses'].append(measure('landing',12,20,comp))
for theta in (10,8,6,4,2,0):out['poses'].append(measure('two_feet',theta,20,root(theta,20)))
(HERE/'second_step_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
