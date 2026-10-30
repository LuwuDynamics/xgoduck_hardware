"""Find two-foot edge-contact transfer poses using exact candidate foot meshes.

Geometric force-balance screening only. Friction, compliance, gravity-driven
rotation, servo loads, and transitions between these sampled poses are absent.
"""
import contextlib,io,json,runpy
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    env=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,soles,rows,legs,body=env['feet'],env['soles'],env['rows'],env['legs'],env['body']
rot,point,intersect=env['rot'],env['point'],env['intersect']
polygon_hull,signed_margin_mm=env['polygon_hull'],env['signed_margin_mm']
floor=env['floor']

def evaluate(stance,theta,comp):
    swing='right' if stance=='left' else 'left'
    xs=-25.5 if stance=='left' else 25.5;xw=-xs
    B=rot(theta,[0,1,0],[xs,0,-71.5]);C=rot(comp,[0,1,0],[xw,0,-71.5]);T=B@C
    v=feet[swing].vertices; coords=v@T[:3,:3].T+T[:3,3]
    return float(np.min(coords[:,2])-floor),coords,B,T,swing

report={'scope':'sampled stationary two-foot edge-contact configurations, 0–14 degrees body roll',
        'floor_z_mm':floor,'poses':[],
        'limitations':['Sole edge contact uses ideal rigid horizontal floor; no friction, forces, torque or deformation',
         'Sampled static poses only; transitioning and feasibility of contact forces not demonstrated',
         'Partial mass estimate, camera/speaker assumptions and assumed servo axes',
         'Only selected printed meshes checked; actual parts, horn and joint clearances remain unverified']}
for stance,sign in [('left',-1),('right',1)]:
 for degree in range(0,15,2):
    theta=sign*degree
    candidates=[]
    sample=np.linspace(-45,45,361)
    vals=[evaluate(stance,theta,c)[0] for c in sample]
    for i in range(len(sample)-1):
        if vals[i]*vals[i+1]>0:continue
        lo,hi=sample[i],sample[i+1]; f0=vals[i]
        for _ in range(25):
            mid=(lo+hi)/2;fm=evaluate(stance,theta,mid)[0]
            if f0*fm<=0:hi=mid
            else:lo=mid;f0=fm
        c=(lo+hi)/2
        if any(abs(c-x)<.01 for x in candidates):continue
        candidates.append(c)
    options=[]
    for comp in candidates:
        gap,coords,B,T,swing=evaluate(stance,theta,comp)
        contact=coords[coords[:,2] <= floor+.03]
        hull=polygon_hull(list(soles[stance])+[(p[0],p[1]) for p in contact])
        mass=0.;total=np.zeros(3)
        for row in rows:
            name=row['name'].lower()
            M=np.eye(4) if name==f'{stance}_foot' else T if name==f'{swing}_foot' else B
            mass+=row['mass_g'];total+=row['mass_g']*point(M,row['center_mm'])
        com=total/mass
        moving=feet[swing].copy();moving.apply_transform(T)
        leg_swing=legs[swing].copy();leg_swing.apply_transform(B)
        leg_stance=legs[stance].copy();leg_stance.apply_transform(B)
        moved_body=body.copy();moved_body.apply_transform(B)
        options.append({'swing_ankle_deg':round(comp,3),'floor_gap_mm':round(gap,4),
           'contact_vertices':len(contact),'static_support_margin_mm':round(signed_margin_mm(com[:2],hull),3),
           'foot_overlap_mm3':round(intersect(moving,feet[stance]),4),
           'swing_foot_vs_swing_leg_mm3':round(intersect(moving,leg_swing),4),
           'swing_foot_vs_stance_leg_mm3':round(intersect(moving,leg_stance),4),
           'stance_foot_vs_stance_leg_mm3':round(intersect(feet[stance],leg_stance),4),
           'swing_foot_vs_body_mm3':round(intersect(moving,moved_body),4)})
    viable=[o for o in options if all(o[k]==0 for k in ('foot_overlap_mm3','swing_foot_vs_swing_leg_mm3',
          'swing_foot_vs_stance_leg_mm3','stance_foot_vs_stance_leg_mm3','swing_foot_vs_body_mm3'))]
    selected=max(viable,key=lambda x:x['static_support_margin_mm']) if viable else None
    report['poses'].append({'stance':stance,'body_roll_deg':theta,'selected':selected,'options':options})
(HERE/'edge_transfer_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
