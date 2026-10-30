"""Test motor and horn proxies in the sampled second half-step poses."""
from pathlib import Path
import contextlib,io,json,runpy
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
 s=runpy.run_path(str(HERE/'second_step_check.py'))
 m=runpy.run_path(str(HERE/'motor_motion_clearance.py'))
proxies=m['proxies'];moved=m['moved'];overlap=m['overlap']
legs,feet,body=s['legs'],s['feet'],s['body'];SHIFT=s['SHIFT'];transforms=s['transforms']
poses=json.loads((HERE/'second_step_results.json').read_text())['poses']
result={'scope':'motor-case, shaft, turret and hip-horn proxies over sampled second half-step',
 'poses_checked':0,'collisions':[],
 'limits':['Servo cases, shaft and horn geometry are approximate, not measured purchased parts',
  'Servo ears, horn retaining screws, case clamps, cables and loads are missing',
  'Sampled positions only; no continuous clearance, dynamic response or physical verification']}
for p in poses:
 B,stance_leg,torso,swing_leg,swing_foot=transforms(p['roll_deg'],p['stance_hip_change_deg'],p['swing_ankle_deg'])
 frame={'right':{'leg':moved(legs['right'],stance_leg),'foot':moved(feet['right'],SHIFT),'T':stance_leg},
        'left':{'leg':moved(legs['left'],swing_leg),'foot':moved(feet['left'],swing_foot),'T':swing_leg}}
 body_m=moved(body,torso);bad={}
 for side in ('left','right'):
  other='right' if side=='left' else 'left'
  for kind,obj in proxies[side].items():
   T=frame[side]['T'] if kind.startswith('ankle') or kind=='hip_horn_box' else torso
   geom=moved(obj,T)
   targets={'leg':frame[side]['leg'],'foot':frame[side]['foot'],'other_foot':frame[other]['foot']}
   if kind.startswith('ankle') or kind=='hip_horn_box':targets['body']=body_m
   for name,target in targets.items():
    v=overlap(geom,target)
    if v>0.01:bad[f'{side}_{kind}__{name}']=round(v,4)
 result['poses_checked']+=1
 if bad:result['collisions'].append({'phase':p['phase'],'roll':p['roll_deg'],'hip_change':p['stance_hip_change_deg'],
                                     'ankle':p['swing_ankle_deg'],'overlap_mm3':bad})
(HERE/'second_step_motor_clearance_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
