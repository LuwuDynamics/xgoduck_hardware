"""Sample transition from edge contact to lifted foot while body stays tilted.

This is geometric/quasi-static screening, not a powered movement test.
"""
from pathlib import Path
import contextlib,io,json,runpy
import numpy as np
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    e=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,soles,rows,legs,body=e['feet'],e['soles'],e['rows'],e['legs'],e['body']
rot,point,intersect,margin=e['rot'],e['point'],e['intersect'],e['signed_margin_mm']
floor=e['floor']
edge=json.loads((HERE/'edge_transfer_results.json').read_text())
result={'scope':'Sampled stationary stages while lifting a foot from edge contact after 12 degree weight transfer',
 'limits':['Assumed camera/speaker mass; missing electronics and fasteners',
           'Known servo axes are approximations; no motor torque, time, friction or dynamics',
           'No real horn/gear/screw geometry or contact-force feasibility check'], 'poses':[]}
for stance,theta in [('left',-12),('right',12)]:
    swing='right' if stance=='left' else 'left';xs=-25.5 if stance=='left' else 25.5;xw=-xs
    B=rot(theta,[0,1,0],[xs,0,-71.5])
    match=next(p for p in edge['poses'] if p['stance']==stance and p['body_roll_deg']==theta)
    if match['selected'] is None:raise ValueError('No clear edge-contact pose')
    start=match['selected']['swing_ankle_deg'];end=-theta
    for comp in np.linspace(start,end,12):
        T=B@rot(float(comp),[0,1,0],[xw,0,-71.5])
        total=np.zeros(3);mass=0.
        for row in rows:
            name=row['name'].lower()
            M=np.eye(4) if name==f'{stance}_foot' else T if name==f'{swing}_foot' else B
            mass+=row['mass_g'];total+=row['mass_g']*point(M,row['center_mm'])
        com=total/mass
        foot=feet[swing].copy();foot.apply_transform(T)
        leg=legs[swing].copy();leg.apply_transform(B)
        stance_leg=legs[stance].copy();stance_leg.apply_transform(B)
        moving_body=body.copy();moving_body.apply_transform(B)
        result['poses'].append({'stance':stance,'swing_ankle_deg':round(float(comp),3),
         'stance_margin_mm':round(margin(com[:2],soles[stance]),3),
         'swing_foot_height_mm':round(float(foot.bounds[0,2]-floor),3),
         'foot_vs_foot_mm3':round(intersect(foot,feet[stance]),4),
         'foot_vs_leg_mm3':round(intersect(foot,leg),4),
         'foot_vs_other_leg_mm3':round(intersect(foot,stance_leg),4),
         'stance_foot_vs_leg_mm3':round(intersect(feet[stance],stance_leg),4),
         'foot_vs_body_mm3':round(intersect(foot,moving_body),4)})
(HERE/'lift_transition_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
