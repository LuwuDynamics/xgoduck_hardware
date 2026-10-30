"""Ideal static force feasibility for sampled two-foot edge-transfer poses.

Uses vertical point reactions, rigid geometry and linprog to find the smallest
maximum joint gravity moment. It is neither dynamic nor a real servo test.
"""
from pathlib import Path
import contextlib,io,json,runpy
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()): e=runpy.run_path(str(HERE/'stance_pose_check.py'))
feet,soles,rows=e['feet'],e['soles'],e['rows'];rot,point=e['rot'],e['point'];floor=e['floor']
poses=json.loads((HERE/'edge_transfer_results.json').read_text())['poses']
gravity=np.array([0.,0.,-9.80665])
report={'scope':'sampled two-foot transfers, vertical contact force and ideal static joint moments',
 'method':'linear program chooses nonnegative vertical point reactions with force and moment balance, minimizing maximum absolute joint moment',
 'limits':['Partial load, assumed 10g camera and 12g speaker; multiple boards, wires and mounts omitted',
  'Ideal rigid floor and point contacts; no deformation, tipping edge geometry, friction or other contact forces',
  'No acceleration, impacts, servo speed/torque curve, current, voltage sag, backlash or dynamics',
  'Servo axes and positions assumed; measured hardware and horn interfaces absent',
  'Holding torque is not a continuous operating rating; static feasibility is not proof of walking'], 'poses':[]}
for pose in poses:
 if not pose['selected']:continue
 stance=pose['stance'];swing='right' if stance=='left' else 'left'
 theta=pose['body_roll_deg'];comp=pose['selected']['swing_ankle_deg']
 xs=-25.5 if stance=='left' else 25.5;xw=-xs
 B=rot(theta,[0,1,0],[xs,0,-71.5]);T=B@rot(comp,[0,1,0],[xw,0,-71.5])
 v=feet[swing].vertices;coords=v@T[:3,:3].T+T[:3,3]
 contact=coords[coords[:,2]<=floor+.03]
 # Reduce the many repeated mesh vertices to extrema of the contact projection.
 contact_xy=e['polygon_hull']([(p[0],p[1]) for p in contact]) if len(contact)>=3 else [(p[0],p[1]) for p in contact]
 contact_xy=list(dict.fromkeys((round(p[0],5),round(p[1],5)) for p in contact_xy))
 if len(contact_xy)==0:raise RuntimeError('No swing-foot contact points')
 support_xy=soles[stance];n0=len(support_xy);points=np.array(list(support_xy)+contact_xy)/1000.
 axes={'stance_ankle':(np.array([xs,0.,-71.5]),np.array([0.,1.,0.])),
       'stance_hip':(point(B,[xs,0,-40]),B[:3,:3]@np.array([0.,0.,1.])),
       'swing_hip':(point(B,[xw,0,-40]),B[:3,:3]@np.array([0.,0.,1.])),
       'swing_ankle':(point(B,[xw,0,-71.5]),B[:3,:3]@np.array([0.,1.,0.]))}
 grav={k:0. for k in axes};mass=0.;weighted=np.zeros(3)
 for row in rows:
  name=row['name'].lower();m=row['mass_g']/1000.
  if name==f'{stance}_foot':M=np.eye(4);parents=[]
  elif name==f'{swing}_foot':M=T;parents=list(axes)
  elif name in (f'{stance}_leg',f'{stance}_washer',f'{stance}_ankle_servo'):M=B;parents=['stance_ankle']
  elif name in (f'{swing}_leg',f'{swing}_washer',f'{swing}_ankle_servo'):M=B;parents=['stance_ankle','stance_hip','swing_hip']
  else:M=B;parents=['stance_ankle','stance_hip']
  r=point(M,row['center_mm'])/1000.;mass+=m;weighted+=m*r
  for key in parents:
   origin,axis=axes[key];grav[key]+=float(np.cross(r-origin/1000,m*gravity)@axis)
 com=weighted/mass;N=len(points)
 # Fn are vertical normal loads. Equilibrium requires resultant under COM.
 eq=np.zeros((3,N+1));eq[0,:N]=1.;eq[1,:N]=points[:,0]-com[0];eq[2,:N]=points[:,1]-com[1]
 rhs=np.array([mass*9.80665,0.,0.])
 coefficients={}
 for key,(origin,axis) in axes.items():
  coeff=np.zeros(N)
  for i in range(n0,N):
   p=np.array([points[i,0],points[i,1],floor/1000.]);coeff[i]=np.cross(p-origin/1000.,[0.,0.,1.])@axis
  coefficients[key]=coeff
 A=[];b=[]
 for key in axes:
  plus=np.zeros(N+1);plus[:N]=coefficients[key];plus[N]=-1.;A.append(plus);b.append(-grav[key])
  minus=np.zeros(N+1);minus[:N]=-coefficients[key];minus[N]=-1.;A.append(minus);b.append(grav[key])
 objective=np.zeros(N+1);objective[-1]=1.
 sol=linprog(objective,A_ub=np.array(A),b_ub=np.array(b),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
 record={'stance':stance,'body_roll_deg':theta,'swing_ankle_deg':comp,'solver_success':bool(sol.success)}
 if sol.success:
  loads=sol.x[:N];record.update({'optimal_max_abs_joint_moment_Nm':round(float(sol.x[-1]),5),
   'joint_gravity_plus_reaction_moments_Nm':{k:round(float(grav[k]+coefficients[k]@loads),5) for k in axes},
   'total_stance_normal_N':round(float(sum(loads[:n0])),4),
   'total_swing_normal_N':round(float(sum(loads[n0:])),4),
   'equilibrium_residual_max':float(np.max(np.abs(eq@sol.x-rhs)))})
 else:record['solver_message']=str(sol.message)
 report['poses'].append(record)
report['all_feasible']=bool(report['poses']) and all(p['solver_success'] for p in report['poses'])
(HERE/'edge_transfer_force_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
