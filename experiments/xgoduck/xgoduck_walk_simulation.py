"""XGO-Duck upstream ONNX policy in upstream MuJoCo scene; local experiment.

Uses the runtime's own observation builder and action smoothing.  The project's
training actuator implementation is not present here: scene_walk.xml uses its
documented simplified PD actuators, so this is not the original training or
physical deployment environment.
"""
import os, sys, json, math, argparse, hashlib
from pathlib import Path
import numpy as np
import mujoco
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'xgoduck_runtime_reference'/'python'))
sys.path.insert(1,str(ROOT/'xgoduck_sim_deps'))
from policy import Policy
from rl_core import POLICY_INDEX

SCENE=ROOT/'xgoduck_rl_reference'/'src'/'mjlab_microduck'/'robot'/'xgoduck'/'scene_walk.xml'
OUT=ROOT/'xgoduck_walk_output'
OUT.mkdir(exist_ok=True)
JOINTS=['left_hip_yaw','left_hip_roll','left_hip_pitch','left_knee','left_ankle',
        'neck_pitch','head_pitch','head_yaw','head_roll',
        'right_hip_yaw','right_hip_roll','right_hip_pitch','right_knee','right_ankle']

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seconds',type=float,default=8)
    p.add_argument('--speed',type=float,default=0.08)
    p.add_argument('--video',action='store_true')
    args=p.parse_args()
    m=mujoco.MjModel.from_xml_path(str(SCENE))
    d=mujoco.MjData(m)
    mujoco.mj_resetDataKeyframe(m,d,m.key('STAND').id)
    mujoco.mj_forward(m,d)
    assert m.nu==len(JOINTS) and [m.actuator(i).name for i in range(m.nu)]==JOINTS
    qa=np.array([m.joint(n).qposadr[0] for n in JOINTS])
    va=np.array([m.joint(n).dofadr[0] for n in JOINTS])
    policy=Policy();ok,msg=policy.load()
    if not ok:raise RuntimeError('Unable to load walking policy: '+msg)
    dt=float(m.opt.timestep);control_steps=round(.02/dt)
    if abs(control_steps*dt-.02)>1e-9:raise RuntimeError('Timestep does not divide policy period')
    if args.video:
        m.vis.global_.offwidth=800;m.vis.global_.offheight=600
    renderer=mujoco.Renderer(m,600,800) if args.video else None
    camera=mujoco.MjvCamera();camera.distance=.68;camera.azimuth=135;camera.elevation=-15
    frame_list=[];trace=[];max_tilt=0.;max_abs_roll=0.;events=[];last=0
    start=d.xpos[m.body('trunk_base').id].copy()
    for k in range(round(args.seconds/.02)):
        R=d.site_xmat[m.site('imu').id].reshape(3,3)
        grav=R.T @ np.array([0,0,-1.])
        gyro=d.sensor('imu_ang_vel').data.copy()
        angles=np.zeros(15);vels=np.zeros(15)
        angles[POLICY_INDEX]=np.rad2deg(d.qpos[qa]);vels[POLICY_INDEX]=np.rad2deg(d.qvel[va])
        # Start at rest, then gradually command forward movement.
        speed=args.speed*max(0,min(1,(d.time-0.5)/1.0))
        action=policy.infer(grav,gyro,angles.tolist(),vels.tolist(),[speed,0,0],[0,0,0,0])
        targets=np.deg2rad(np.asarray(policy.action_to_deg(action))[POLICY_INDEX])
        d.ctrl[:]=targets
        mujoco.mj_step(m,d,nstep=control_steps)
        R=d.xmat[m.body('trunk_base').id].reshape(3,3)
        tilt=math.degrees(math.acos(float(np.clip(R[2,2],-1,1))))
        max_tilt=max(max_tilt,tilt)
        pos=d.xpos[m.body('trunk_base').id].copy()
        contacts=set()
        for contact in d.contact:
            names=[m.geom(contact.geom1).name,m.geom(contact.geom2).name]
            if 'floor' in names:
                contacts.update(n for n in names if n in ('left_foot_collision','right_foot_collision'))
        support=1 if contacts=={'left_foot_collision'} else (2 if contacts=={'right_foot_collision'} else 0)
        if support and support!=last:
            if last:events.append({'time_s':round(float(d.time),2),'support':support})
            last=support
        trace.append({'t':round(float(d.time),3),'x_m':round(float(pos[0]-start[0]),5),
                      'y_m':round(float(pos[1]-start[1]),5),'height_m':round(float(pos[2]),5),
                      'tilt_deg':round(tilt,2),'contacts':sorted(contacts)})
        if renderer and k%2==0:
            camera.lookat[:]=pos+[0,0,.04]
            renderer.update_scene(d,camera=camera)
            im=Image.fromarray(renderer.render());draw=ImageDraw.Draw(im)
            draw.rectangle((0,0,800,37),fill=(255,255,255))
            draw.text((10,9),'MuJoCo simulation | XGO-Duck walking policy | %.2f s'%d.time,fill=(0,0,0))
            frame_list.append(im)
        if tilt>60 or pos[2]<0.045:
            break
    final=d.xpos[m.body('trunk_base').id].copy()
    result={'scene':'upstream scene_walk.xml STAND pose, simplified position actuators',
            'policy':'upstream xgoduck_walk.onnx with policy.py observation and filtering',
            'policy_sha256':hashlib.sha256((ROOT/'xgoduck_runtime_reference'/'python'/'xgoduck_walk.onnx').read_bytes()).hexdigest(),
            'simulation_duration_s':round(float(d.time),3),'command_forward_m_s':args.speed,
            'displacement_world_m':np.round(final-start,4).tolist(),'maximum_tilt_deg':round(max_tilt,1),
            'remained_upright':bool(max_tilt<=60 and final[2]>=.045 and d.time>=args.seconds-.03),
            'single_foot_support_transitions':len(events),'support_events':events,
            'limitations':['Simplified PD actuators from upstream scene, not BAM training actuator dynamics',
                           'Idealized direct IMU gravity and gyro; no deployment sensor noise or filtering',
                           'Physics simulation only; no physical robot or hardware validation',
                           'No external support or scripted body translation'],
            'policy_load':msg}
    (OUT/'result.json').write_text(json.dumps(result,indent=2))
    (OUT/'trace.json').write_text(json.dumps(trace,indent=2))
    if renderer:
        frame_list[0].save(OUT/'walking.gif',save_all=True,append_images=frame_list[1:],duration=40,loop=0,optimize=False)
        renderer.close()
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
