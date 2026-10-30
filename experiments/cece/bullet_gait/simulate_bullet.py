"""Run a four-servo free-standing Bullet dynamics experiment for Cece.

This is a candidate simulation with assumed contacts, motor behavior, inertias
and missing-component masses; it does not certify the real robot. CAD-derived
mesh is used for visualization and the sole polygon for ground collisions.
"""
from pathlib import Path
import argparse,hashlib,json,math,shutil,sys,time
import numpy as np
import pybullet as p
from scipy.spatial.transform import Rotation
HERE=Path(__file__).resolve().parent
CECE=HERE.parent; ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'cece_mesh_deps'))
sys.path.insert(0,str(CECE/'balance_study'))
import trimesh
from balance_study import polygon_hull,read_binary_stl

parser=argparse.ArgumentParser()
parser.add_argument('--friction',type=float,default=.8)
parser.add_argument('--torque',type=float,default=.08)
parser.add_argument('--phase-seconds',type=float,default=.8)
parser.add_argument('--steps',type=int,default=10)
parser.add_argument('--hz',type=int,default=240)
parser.add_argument('--trace-hz',type=int,default=10)
parser.add_argument('--geometry-trace',action='store_true')
parser.add_argument('--extra-payload-g',type=float,default=0.)
parser.add_argument('--push-force-n',type=float,default=0.)
parser.add_argument('--video',action='store_true')
parser.add_argument('--ffmpeg',default=None)
parser.add_argument('--name',default='nominal')
args=parser.parse_args()
if args.friction<0 or args.torque<=0 or args.phase_seconds<=0 or args.steps<=0 or args.extra_payload_g<0 or args.hz<120 or args.hz%120 or args.trace_hz<1 or args.hz%args.trace_hz:raise ValueError('Invalid simulation parameter')

def read(pth):return json.loads(pth.read_text(encoding='utf-8'))
old=read(CECE/'balance_study/latest_balance_results.json')
head=read(CECE/'rounded_head_study/balance_sensitivity.json')
study=CECE/'hip_drive_study'
replaced={'body','head','face','antenna','speaker_pod','speaker_grille','left_leg','right_leg','left_foot','right_foot'}
rows=[{'name':x['name'].lower(),'mass_g':x['solid_PLA_mass_g'],'center_mm':x['center_mm']}
      for x in old['printed_parts'] if x['name'] not in replaced]
rows += [{'name':x['name'].lower(),'mass_g':x['mass_g'],'center_mm':x['center_mm']} for x in head['new_parts']]
paths={}
for side in ('left','right'):
    for kind in ('leg','foot'):
        path=study/f'Cece_{side}_{"leg_hip_slot" if kind=="leg" else "wide_foot_clearance"}_TEST_ONLY.stl'
        m=trimesh.load(path,force='mesh');paths[f'{side}_{kind}']=path
        if not m.is_watertight or m.volume<=0:raise RuntimeError('bad mesh '+str(path))
        rows.append({'name':f'{side}_{kind}','mass_g':m.volume*.00124,'center_mm':m.center_mass.tolist()})
rows += [{'name':x['name'].lower(),'mass_g':x['mass_g'],'center_mm':x['center_mm']} for x in old['included_hardware']]
# Camera and speaker sensitivity masses as used in previous study; remaining
# hardware values are explicit estimates, NOT measured purchased-part data.
extras=[('speaker_hypothesis',12,[0,32.5,17]),('camera_hypothesis',10,[0,-29,38]),
        ('oled_hypothesis',12,[0,-38.4,-19]),('ultrasonic_hypothesis',7,[0,-18,14.5]),
        ('driver_hypothesis',8,[1,11.8,13]),('c3_hypothesis',5,[0,24,10]),
        ('amp_hypothesis',3,[17,-6,24]),('mic_hypothesis',2,[-14,-5,24]),
        ('perfboard_hypothesis',5,[0,7,43.3]),('wires_fasteners_hypothesis',8,[0,5,-5])]
if args.extra_payload_g:extras.append(('extra_payload_hypothesis',args.extra_payload_g,[0,0,20]))
rows += [{'name':n,'mass_g':m,'center_mm':c} for n,m,c in extras]

def group(name):
    if name in ('left_foot','right_foot'):return name
    for s in ('left','right'):
        if name in (f'{s}_leg',f'{s}_washer',f'{s}_ankle_servo'):return f'{s}_leg'
    return 'base'
grouped={n:[] for n in ('base','left_leg','left_foot','right_leg','right_foot')}
for row in rows:grouped[group(row['name'])].append(row)
plastic=read(HERE/'solid_plastic_mass_properties.json')
# Component box dimensions are estimates along the placed XYZ axes (mm).
box_dims={'battery':[35,56,16],'ubec':[21,56,14],'charger':[19.8,39.6,9.5],
 'speaker_hypothesis':[28,7,28],'camera_hypothesis':[23,17,19.8],
 'oled_hypothesis':[47,5.6,35.6],'ultrasonic_hypothesis':[45,14,20],
 'driver_hypothesis':[52,12.3,25.4],'c3_hypothesis':[28,8,21],
 'amp_hypothesis':[22,22,6],'mic_hypothesis':[16,16,6],
 'perfboard_hypothesis':[30,20,8],'wires_fasteners_hypothesis':[30,30,20]}
box_dims['extra_payload_hypothesis']=[20,20,20]
for s in ('left','right'):
 box_dims[f'{s}_hip_servo']=[12.2,23,22]
 box_dims[f'{s}_ankle_servo']=[12.2,22.5,23]

def group_mass(name,origin_mm):
    rs=grouped[name];mass=sum(x['mass_g'] for x in rs)/1000
    com=sum((x['mass_g']/1000)*np.array(x['center_mm']) for x in rs)/mass
    # Printed-part tensors are exact solid CAD geometry at assumed PLA density;
    # nonprinted modules are boxes with assumed dimensions and uniform mass.
    I=np.zeros((3,3))
    for x in rs:
        m=x['mass_g']/1000;r=(np.array(x['center_mm'])-com)/1000
        if x['name'] in plastic:
            q=plastic[x['name']]
            factor=m/(q['volume_mm3']*1.24e-6)
            I_local=np.array(q['inertia_mm5'])*1.24e-12*factor
        else:
            if x['name'] not in box_dims:raise KeyError('missing inertia envelope '+x['name'])
            dx,dy,dz=np.array(box_dims[x['name']])/1000
            I_local=np.diag([m*(dy*dy+dz*dz)/12,m*(dx*dx+dz*dz)/12,m*(dx*dx+dy*dy)/12])
        I += I_local + m*(np.dot(r,r)*np.eye(3)-np.outer(r,r))
    eigval,eigvec=np.linalg.eigh(I)
    if np.linalg.det(eigvec)<0:eigvec[:,0]*=-1
    quat=Rotation.from_matrix(eigvec).as_quat().tolist()
    return mass,(com-np.array(origin_mm))/1000,np.maximum(eigval,1e-9),com,quat
origins={'base':[0,0,0],'left_leg':[-25.5,0,-40],'left_foot':[-25.5,0,-71.5],
         'right_leg':[25.5,0,-40],'right_foot':[25.5,0,-71.5]}
props={n:group_mass(n,origins[n]) for n in grouped}
sole={}
for side in ('left','right'):
    vertices=read_binary_stl(paths[f'{side}_foot'])['vertices']
    z=min(v[2] for v in vertices)
    sole[side]=polygon_hull([(v[0],v[1]) for v in vertices if v[2]<=z+.1])

def mesh_hash(path):return hashlib.sha256(path.read_bytes()).hexdigest()
cid=p.connect(p.DIRECT)
p.resetSimulation();p.setGravity(0,0,-9.80665);p.setTimeStep(1/args.hz)
p.setPhysicsEngineParameter(numSolverIterations=120,enableConeFriction=1,deterministicOverlappingPairs=1)
floor=p.createMultiBody(baseMass=0,baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_PLANE))
p.changeDynamics(floor,-1,lateralFriction=args.friction,restitution=0)

# Collision geometry: exact convex hull of CAD sole contact polygon, extruded
# 5.02 mm. Other collisions are bounding boxes; self collision is disabled.
def foot_collision(side):
    x0=-25.5 if side=='left' else 25.5
    pts=[]
    for z in (-89.02,-84.0):
        pts.extend([[(x-x0)/1000,y/1000,(z+71.5)/1000] for x,y in sole[side]])
    return p.createCollisionShape(p.GEOM_MESH,vertices=pts)
def body_collision():
    half=[[.04095,.037,.0195],[.042,.0395,.0275],[.0225,.0238,.009]]
    pos=[[0,.0025,-.0195],[0,-.0005,.0275],[0,.0633,-.024]]
    return p.createCollisionShapeArray(shapeTypes=[p.GEOM_BOX]*3,halfExtents=half,collisionFramePositions=pos)
leg_collision=p.createCollisionShape(p.GEOM_BOX,halfExtents=[.0085,.020,.021],collisionFramePosition=[0,-.0035,-.021])

colors={'Body':[.86,.91,.95,1],'Rounded_Head_Study':[.9,.94,.98,1],
 'Rear_Cover_Study':[.75,.84,.92,1],'Heart_Frame_V3':[.9,.3,.45,1],
 'Antenna':[1,.72,.26,1],'Left_Arm':[.55,.72,.86,1],'Right_Arm':[.55,.72,.86,1],
 'Left_Leg':[.56,.7,.84,1],'Right_Leg':[.56,.7,.84,1],
 'Left_Foot':[.30,.49,.72,1],'Right_Foot':[.30,.49,.72,1],
 'OLED_Adafruit4741_Official_CAD':[.06,.13,.23,1],
 'HC_SR04_Left_Can':[.3,.78,.84,1],'HC_SR04_Right_Can':[.3,.78,.84,1],
 'Camera_Lens_Corridor_Provisional':[.06,.09,.12,1],
 'Charger_Tray':[.45,.65,.72,1],'Charger_Bezel':[.35,.55,.62,1]}
def visual(names,origin):
    names=[n for n in names if (HERE/'cad_visuals'/f'{n}.stl').exists()]
    if not names:return -1
    position=[[-v/1000 for v in origin] for _ in names]
    return p.createVisualShapeArray(shapeTypes=[p.GEOM_MESH]*len(names),
       fileNames=[str(HERE/'cad_visuals'/f'{n}.stl') for n in names],
       meshScales=[[.001,.001,.001]]*len(names),
       visualFramePositions=position,rgbaColors=[colors[n] for n in names])
base_names=[n for n in colors if n not in ('Left_Leg','Right_Leg','Left_Foot','Right_Foot')]
shape=p.createMultiBody(baseMass=props['base'][0],baseCollisionShapeIndex=body_collision(),
 baseVisualShapeIndex=visual(base_names,[0,0,0]),basePosition=[0,0,.08902],
 baseInertialFramePosition=props['base'][1].tolist(),baseInertialFrameOrientation=props['base'][4],
 linkMasses=[props[n][0] for n in ('left_leg','left_foot','right_leg','right_foot')],
 linkCollisionShapeIndices=[leg_collision,foot_collision('left'),leg_collision,foot_collision('right')],
 linkVisualShapeIndices=[visual(['Left_Leg'],origins['left_leg']),visual(['Left_Foot'],origins['left_foot']),
                         visual(['Right_Leg'],origins['right_leg']),visual(['Right_Foot'],origins['right_foot'])],
 linkPositions=[[-.0255,0,-.04],[0,0,-.0315],[.0255,0,-.04],[0,0,-.0315]],
 linkOrientations=[[0,0,0,1]]*4,
 linkInertialFramePositions=[props[n][1].tolist() for n in ('left_leg','left_foot','right_leg','right_foot')],
 linkInertialFrameOrientations=[props[n][4] for n in ('left_leg','left_foot','right_leg','right_foot')],linkParentIndices=[0,1,0,3],
 linkJointTypes=[p.JOINT_REVOLUTE]*4,linkJointAxis=[[0,0,1],[0,1,0],[0,0,1],[0,1,0]])
for idx,name in [(-1,'base'),(0,'left_leg'),(1,'left_foot'),(2,'right_leg'),(3,'right_foot')]:
    p.changeDynamics(shape,idx,localInertiaDiagonal=props[name][2].tolist(),lateralFriction=args.friction,
                     spinningFriction=.002,rollingFriction=.0005,restitution=0,linearDamping=.04,angularDamping=.04)
    if idx>=0:p.changeDynamics(shape,idx,jointDamping=.001)

def commands(deg):
    # Order: left hip, left ankle, right hip, right ankle.
    limits=[]
    for idx,angle in enumerate(deg):
        speed=abs(p.getJointState(shape,idx)[1])
        # A linear speed/torque envelope is only a crude motor assumption;
        # seller lists holding torque and no-load speed, not a measured curve.
        speed_fraction=min(1.,speed/math.radians(500))
        limit=min(args.torque,0.1765*(1.-speed_fraction))
        p.setJointMotorControl2(shape,idx,p.POSITION_CONTROL,targetPosition=math.radians(float(angle)),
          force=limit,maxVelocity=math.radians(500),positionGain=.12,velocityGain=.8)
        limits.append(limit)
    return limits

edge=read(study/'edge_transfer_results.json')['poses']
touch=read(study/'touchdown_pose_results.json')['poses']
edge_left=sorted([(abs(x['body_roll_deg']),abs(x['selected']['swing_ankle_deg'])) for x in edge if x['stance']=='left' and x['selected']])
edge_x=np.array([x[0] for x in edge_left]);edge_y=np.array([x[1] for x in edge_left])
def ease(t):return t*t*(3-2*t)
def interp(a,b,t):return a+(b-a)*ease(t)
def target(half,phase,u):
    # First half begins with aligned hips; later half-steps alternate ±10°.
    left_stance=(half%2==0);h0=0 if half==0 else (-10 if left_stance else 10);h1=10 if left_stance else -10
    sign=1 if left_stance else -1
    contact=float(np.interp(12,edge_x,edge_y));hip=h0
    if phase==0:
        roll=interp(0,12,u);a=roll;b=float(np.interp(roll,edge_x,edge_y))
    elif phase==1:
        a=12;b=interp(contact,12,u)
    elif phase==2:
        a=b=12;hip=interp(h0,h1,u)
    elif phase==3:
        a=12;b=interp(12,contact,u);hip=h1
    else:
        roll=interp(12,0,u);a=roll;b=float(np.interp(roll,edge_x,edge_y));hip=h1
    if left_stance:return [hip,sign*a,hip,sign*b]
    return [hip,sign*b,hip,sign*a]

def base_state():
    pos,ori=p.getBasePositionAndOrientation(shape)
    inverse_local=p.invertTransform([0,0,0],props['base'][4])[1]
    body_ori=p.multiplyTransforms([0,0,0],ori,[0,0,0],inverse_local)[1]
    matrix=np.array(p.getMatrixFromQuaternion(body_ori)).reshape(3,3)
    tilt=math.degrees(math.acos(np.clip(matrix[2,2],-1,1)))
    return np.array(pos),tilt

# Validate joint world frames are at predicted CAD pivots, before ground motion.
frames=[p.getLinkState(shape,i,computeForwardKinematics=True)[4] for i in range(4)]
expected=np.array([[-.0255,0,.04902],[-.0255,0,.01752],[.0255,0,.04902],[.0255,0,.01752]])
frame_error=float(np.max(np.abs(np.array(frames)-expected)))
if frame_error>1e-5:raise RuntimeError('Model joint frame differs from CAD by '+str(frame_error))

trace=[];max_tilt=0.;fail=None;completed=0;max_torque=0.;max_tracking_error=0.;saturated_joint_samples=0;contact_count={1:0,3:0};step_evidence=[]
initial_joints=[0,0,0,0]
commands(initial_joints)
for _ in range(args.hz):p.stepSimulation()
initial,tilt=base_state();max_tilt=max(max_tilt,tilt)
if tilt>20:fail='Unable to settle at neutral pose before gait'
writer=None;frames_written=0
if args.video:
    import subprocess
    from PIL import Image,ImageDraw,ImageFont
    executable=args.ffmpeg or shutil.which('ffmpeg')
    if not executable:raise RuntimeError('Provide --ffmpeg with the path to ffmpeg')
    W,H,FPS=800,600,12
    writer=subprocess.Popen([executable,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
        '-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',
        str(HERE/f'bullet_{args.name}.mp4')],stdin=subprocess.PIPE)
    font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',20)
    proj=p.computeProjectionMatrixFOV(fov=40,aspect=W/H,nearVal=.01,farVal=3)

tstep=0;steps_per_phase=round(args.phase_seconds*args.hz)
for half in range(args.steps):
    if fail:break
    swing_index=3 if half%2==0 else 1
    stance_index=1 if half%2==0 else 3
    peak_foot_height=0.;airborne_ticks=0;contact_in_final_phase=False
    stance_anchor=None;stance_max_drift=0.;stance_airborne_ticks=0
    for phase in range(5):
        if fail:break
        for k in range(steps_per_phase):
            u=(k+1)/steps_per_phase;angles=target(half,phase,u);limits=commands(angles)
            if args.push_force_n and 6.0<=tstep/args.hz<6.15:
                com,_=p.getBasePositionAndOrientation(shape)
                p.applyExternalForce(shape,-1,[args.push_force_n,0,0],
                                     [com[0],com[1],com[2]+.04],p.WORLD_FRAME)
            p.stepSimulation();tstep+=1
            pos,tilt=base_state();max_tilt=max(max_tilt,tilt)
            joint=[p.getJointState(shape,i) for i in range(4)]
            max_torque=max(max_torque,max(abs(x[3]) for x in joint))
            max_tracking_error=max(max_tracking_error,max(abs(float(a)-math.degrees(x[0])) for a,x in zip(angles,joint)))
            saturated_joint_samples+=sum(limit>1e-7 and abs(x[3])>=.98*limit for x,limit in zip(joint,limits))
            contacts=p.getContactPoints(bodyA=shape,bodyB=floor)
            touching={int(c[3]) for c in contacts}
            foot_bottom=float(p.getAABB(shape,swing_index)[0][2])
            if phase in (1,2,3):
                stance_position=np.asarray(p.getLinkState(shape,stance_index,computeForwardKinematics=True)[4])
                if stance_anchor is None:stance_anchor=stance_position.copy()
                stance_max_drift=max(stance_max_drift,float(np.linalg.norm((stance_position-stance_anchor)[:2])))
                if stance_index not in touching and p.getAABB(shape,stance_index)[0][2]>.001:stance_airborne_ticks+=1
            peak_foot_height=max(peak_foot_height,foot_bottom)
            if swing_index not in touching and foot_bottom>.001:airborne_ticks+=1
            if phase==4 and swing_index in touching:contact_in_final_phase=True
            for c in contacts:
                if c[3] in contact_count:contact_count[c[3]]+=1
            if tstep%(args.hz//args.trace_hz)==0:
                sample={'t_s':round(tstep/args.hz,4),'half_step':half,'phase':phase,
                 'base_com_m':np.round(pos,5).tolist(),'tilt_deg':round(tilt,3),
                 'target_deg':[round(a,2) for a in angles],
                 'actual_deg':[round(math.degrees(x[0]),2) for x in joint],
                 'contact_links':sorted(set(int(c[3]) for c in contacts)),
                 'swing_foot_aabb_bottom_mm':round(foot_bottom*1000,3),
                 'motor_torques_Nm':[round(float(x[3]),4) for x in joint]}
                if args.geometry_trace:
                    cp,cq=p.getBasePositionAndOrientation(shape)
                    ip,iq=p.invertTransform(props['base'][1].tolist(),props['base'][4])
                    bp,bq=p.multiplyTransforms(cp,cq,ip,iq)
                    sample['cad_link_frames']={'base':{'position_m':bp,'quaternion_xyzw':bq}}
                    for idx,n in enumerate(('left_leg','left_foot','right_leg','right_foot')):
                        state=p.getLinkState(shape,idx,computeForwardKinematics=True)
                        sample['cad_link_frames'][n]={'position_m':state[4],'quaternion_xyzw':state[5]}
                trace.append(sample)
            if writer and tstep%(args.hz//12)==0:
                view=p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=[0,-.03,.07],distance=.46,yaw=40,pitch=-10,roll=0,upAxisIndex=2)
                rgba=p.getCameraImage(W,H,viewMatrix=view,projectionMatrix=proj,renderer=p.ER_TINY_RENDERER)[2]
                im=Image.fromarray(np.asarray(rgba,dtype=np.uint8).reshape(H,W,4),'RGBA').convert('RGB');d=ImageDraw.Draw(im)
                d.rectangle((0,0,W,57),fill=(27,42,58));d.text((16,9),'BULLET DYNAMICS | MODEL ASSUMPTIONS | NOT HARDWARE PROOF',font=font,fill='white')
                d.text((16,33),f't={tstep/args.hz:.1f}s  tilt={tilt:.1f}deg  attempted step={half+1}',font=font,fill=(225,235,244))
                writer.stdin.write(np.asarray(im,dtype=np.uint8).tobytes());frames_written+=1
            if tilt>55 or pos[2]<.018:
                fail=f'Fell at {tstep/args.hz:.2f} s, half-step {half+1}, phase {phase+1}'
                break
    if not fail:
        completed+=1
        step_evidence.append({'half_step':half+1,'swing':'right' if swing_index==3 else 'left',
          'max_foot_aabb_bottom_mm':round(peak_foot_height*1000,2),
          'airborne_duration_s':round(airborne_ticks/args.hz,3),'ground_contact_during_final_phase':contact_in_final_phase,
          'ground_contact_at_step_end':swing_index in touching,
          'stance_foot_max_horizontal_drift_mm':round(stance_max_drift*1000,2),
          'stance_foot_airborne_duration_s':round(stance_airborne_ticks/args.hz,3)})
if writer:
    writer.stdin.close();exitcode=writer.wait()
    if exitcode:raise RuntimeError('ffmpeg exited '+str(exitcode))
final,final_tilt=base_state();delta=final-initial
report={'engine':'Bullet PyBullet conda-forge 3.25','status':'EXPERIMENTAL SIMULATION; NOT PROOF OF REAL ROBOT',
 'model':{'mass_g':round(sum(x['mass_g'] for x in rows),3),
   'body_masses_g':{n:round(props[n][0]*1000,3) for n in props},
   'additional_estimated_components_g':{n:m for n,m,c in extras},
   'joint_frame_error_mm':round(frame_error*1000,6),
   'friction_coefficient_each_surface':args.friction,
   'nominal_combined_friction_product':round(args.friction**2,3),'max_motor_torque_Nm':args.torque,
   'assumed_no_load_speed_deg_per_s':500,'assumed_holding_torque_Nm':0.1765,
   'servo_torque_speed_model':'linear decline to zero at no-load speed, additionally capped by max_motor_torque_Nm; not a measured curve',
   'phase_duration_s':args.phase_seconds,'physics_hz':args.hz,'trace_hz':args.trace_hz,
   'geometry_trace':args.geometry_trace,
   'side_push':'%.3f N for 0.15 s at 6 s, applied 40 mm above modeled base COM' % args.push_force_n,
   'collision':'sole convex polygon extruded 5.02 mm; body/head/legs are boxes; self-collision off',
   'inertia':'solid CAD inertia for printed parts; assumed uniform box inertia for hardware; assembled actual inertia not measured',
   'mass_model':'solid PLA model, known hardware masses plus explicitly assumed small components'},
 'result':{'requested_half_steps':args.steps,'completed_half_steps':completed,'fell':bool(fail),
   'failure':fail,'simulated_gait_time_s':round(tstep/args.hz,3),
   'net_base_displacement_mm':np.round(delta*1000,2).tolist(),
   'max_body_tilt_deg':round(max_tilt,2),'final_body_tilt_deg':round(final_tilt,2),
   'peak_motor_torque_Nm':round(max_torque,4),'max_joint_tracking_error_deg':round(max_tracking_error,2),
   'motor_limit_fraction_of_joint_time_samples':round(saturated_joint_samples/(4*max(tstep,1)),5),
   'foot_contact_point_observations':contact_count,
   'observed_lift_and_land_count':sum(x['airborne_duration_s']>=.05 and x['ground_contact_at_step_end'] for x in step_evidence),
   'step_evidence':step_evidence,
   'video_frames':frames_written},
 'asset_sha256':{**{k:mesh_hash(v) for k,v in paths.items()},
   'plastic_mass_properties':mesh_hash(HERE/'solid_plastic_mass_properties.json'),
   'source_cad':mesh_hash(study/'Cece_Full_Electronics_Study.FCStd'),
   'simulation_script':mesh_hash(Path(__file__).resolve())},
 'limitations':['A sensorless position controller and limit are approximations; exact servo speed/torque/current unknown',
  'Ground friction and floor properties assumed; contact modeling and sole stiffness unknown',
  'Collision shapes use sole hulls and simple body/leg boxes; self-collision, horns and wires not simulated',
  'Masses and inertias are incomplete/estimated; CAD servo positions and axes assumed',
  'No hardware validation, electronics/power sag, print tolerance, bearing friction or joint backlash'],
 'trace':trace}
(HERE/f'bullet_{args.name}_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='trace'},indent=2),flush=True)
p.disconnect()
