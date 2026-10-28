"""Five-servo Otto-style research rig: four legs and a yawing head.

Simplified rigid boxes and actuator model, not a dimension-exact Otto CAD
assembly and not a physical validation. Gravity and ground contacts are live.
"""
import argparse, json, math, time
from pathlib import Path
import numpy as np
import mujoco
import mujoco.viewer
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'otto_head_simulation';OUT.mkdir(exist_ok=True)

XML='''<mujoco model="Otto-style with moving head">
<compiler angle="degree"/>
<option timestep="0.002" integrator="implicitfast" iterations="100"/>
<visual><global offwidth="800" offheight="600"/></visual>
<default><joint damping="0.002" armature="0.00002"/><geom friction="0.85 0.005 0.0001" condim="4" solref="0.008 1"/></default>
<worldbody>
<light pos="0 -1 2"/>
<geom name="floor" type="plane" size="3 3 .05" rgba=".65 .72 .77 1"/>
<body name="torso" pos="0 0 .0495"><freejoint/>
 <geom name="body" type="box" size=".0335 .034 .019" pos="0 0 .019" mass=".120" rgba=".2 .65 .22 1"/>
 <geom name="head_servo" type="box" size=".0115 .006 .011" pos="0 0 .041" mass=".009" rgba=".17 .25 .17 1"/>
 <body name="head" pos="0 0 .050"><joint name="head_yaw" type="hinge" axis="0 0 1" range="-45 45"/>
  <geom name="head" type="box" size=".0335 .034 .017" pos="0 0 .017" mass=".045" rgba=".4 .8 .3 1"/>
  <geom name="eye1" type="sphere" size=".003" pos=".0335 -.012 .020" mass=".0001" rgba=".05 .05 .05 1" contype="0" conaffinity="0"/>
  <geom name="eye2" type="sphere" size=".003" pos=".0335 .012 .020" mass=".0001" rgba=".05 .05 .05 1" contype="0" conaffinity="0"/>
 </body>
 <body name="left_leg" pos="0 .024 0"><joint name="left_hip" type="hinge" axis="0 0 1" range="-40 40"/>
  <geom type="box" size=".012 .008 .020" pos="0 0 -.020" mass=".010" rgba=".3 .7 .24 1"/>
  <body name="left_foot" pos="0 .0105 -.040"><joint name="left_ankle" type="hinge" axis="1 0 0" range="-30 30"/>
   <geom name="left_sole" type="box" size=".031 .020 .004" pos="0 0 -.005" mass=".012" rgba=".9 .56 .16 1"/>
  </body>
 </body>
 <body name="right_leg" pos="0 -.024 0"><joint name="right_hip" type="hinge" axis="0 0 -1" range="-40 40"/>
  <geom type="box" size=".012 .008 .020" pos="0 0 -.020" mass=".010" rgba=".3 .7 .24 1"/>
  <body name="right_foot" pos="0 -.0105 -.040"><joint name="right_ankle" type="hinge" axis="1 0 0" range="-30 30"/>
   <geom name="right_sole" type="box" size=".031 .020 .004" pos="0 0 -.005" mass=".012" rgba=".9 .56 .16 1"/>
  </body>
 </body>
</body></worldbody>
<actuator>
 <position name="left_hip" joint="left_hip" kp="0.7" kv="0.025" forcelimited="true" forcerange="-.08 .08"/>
 <position name="left_ankle" joint="left_ankle" kp="0.7" kv="0.025" forcelimited="true" forcerange="-.08 .08"/>
 <position name="right_hip" joint="right_hip" kp="0.7" kv="0.025" forcelimited="true" forcerange="-.08 .08"/>
 <position name="right_ankle" joint="right_ankle" kp="0.7" kv="0.025" forcelimited="true" forcerange="-.08 .08"/>
 <position name="head_yaw" joint="head_yaw" kp="0.2" kv="0.01" forcelimited="true" forcerange="-.05 .05"/>
</actuator></mujoco>'''

def run(cfg,video=False,live=False):
    m=mujoco.MjModel.from_xml_string(XML);d=mujoco.MjData(m);dt=m.opt.timestep
    renderer=mujoco.Renderer(m,600,800) if video else None
    viewer=mujoco.viewer.launch_passive(m,d) if live else None
    camera=mujoco.MjvCamera();camera.distance=.40;camera.azimuth=135;camera.elevation=-14
    frames=[];trace=[];contacts_last=0;transitions=0;tiltmax=0;motor_peak=0;start=None
    head_min=1e3;head_max=-1e3;requested=3600 if live else 10
    for i in range(round(requested/.01)):
        tick=time.perf_counter();t=d.time;ramp=max(0,min(1,t/.7));phase=2*math.pi*cfg['hz']*t
        hip=math.radians(cfg['hip'])*math.sin(phase)*ramp
        ankle=math.radians(cfg['ankle'])*math.sin(phase-math.pi/2)*ramp
        d.ctrl[:]=[hip,ankle,cfg['hipsign']*hip,cfg['anklesign']*ankle,math.radians(25)*math.sin(2*math.pi*.20*t)*ramp]
        mujoco.mj_step(m,d,nstep=5)
        torso=d.xpos[m.body('torso').id].copy()
        if start is None:start=torso.copy()
        mat=d.xmat[m.body('torso').id].reshape(3,3)
        tilt=math.degrees(math.acos(float(np.clip(mat[2,2],-1,1))));tiltmax=max(tiltmax,tilt)
        angle=math.degrees(float(d.joint('head_yaw').qpos[0]));head_min=min(head_min,angle);head_max=max(head_max,angle)
        motor_peak=max(motor_peak,float(max(abs(d.actuator_force))))
        contacts=set()
        for c in d.contact:
            names=[m.geom(c.geom1).name,m.geom(c.geom2).name]
            if 'floor' in names:contacts.update(n for n in names if n in ('left_sole','right_sole'))
        support=1 if contacts=={'left_sole'} else (2 if contacts=={'right_sole'} else 0)
        if support and support!=contacts_last:
            if contacts_last:transitions+=1
            contacts_last=support
        if i%10==0:trace.append([round(float(t),3),*np.round(torso-start,5).tolist(),round(angle,2),round(tilt,2)])
        if renderer and i%4==0:
            camera.lookat[:]=torso+[0,0,.04];renderer.update_scene(d,camera=camera)
            im=Image.fromarray(renderer.render());draw=ImageDraw.Draw(im)
            draw.rectangle((0,0,800,38),fill='white');draw.text((10,10),'SIMULATION | simplified 4-servo Otto + head yaw | %.2f s'%t,fill='black')
            frames.append(im)
        if viewer:
            if not viewer.is_running():break
            viewer.cam.lookat[:]=torso+[0,0,.04];viewer.cam.distance=.45;viewer.cam.azimuth=135;viewer.cam.elevation=-14
            viewer.sync();time.sleep(max(0,.01-(time.perf_counter()-tick)))
        if tilt>55 or torso[2]<.018:break
    displacement=torso-start
    result={'config':cfg,'duration_s':round(float(d.time),2),'total_mass_g':round(float(sum(m.body_mass)*1000),1),
      'head_yaw_deg':[round(head_min,1),round(head_max,1)],'travel_mm':np.round(displacement*1000,2).tolist(),
      'tilt_max_deg':round(tiltmax,1),'single_support_transitions':transitions,'max_joint_torque_nm':round(motor_peak,4),
      'upright':bool(tiltmax<55 and d.time>=requested-.02),
      'limitations':['Simplified boxes and assumed masses, not original Otto STL collision geometry',
      'Generic torque-limited position actuator; no validated FS90 servo speed/current model',
      'No physical prototype, mount, battery or hardware validation', 'No external support or scripted body translation']}
    if renderer:
        frames[0].save(OUT/'otto_head_walk.gif',save_all=True,append_images=frames[1:],duration=40,loop=0,optimize=False);renderer.close()
    if viewer:viewer.close()
    return result,trace

if __name__=='__main__':
    (OUT/'otto_head_model.xml').write_text(XML)
    p=argparse.ArgumentParser();p.add_argument('--sweep',action='store_true');p.add_argument('--video',action='store_true');p.add_argument('--live',action='store_true');args=p.parse_args()
    if args.sweep:
        results=[]
        for hz in [.7,1.,1.3]:
          for hs in [-1,1]:
           for a in [-1,1]:
            cfg={'hz':hz,'hip':30,'ankle':20,'hipsign':hs,'anklesign':a};r,_=run(cfg);results.append(r)
        (OUT/'sweep.json').write_text(json.dumps(results,indent=2))
        print(json.dumps(results,indent=2))
    else:
        cfg=json.loads((OUT/'chosen_config.json').read_text())
        r,trace=run(cfg,args.video,args.live)
        (OUT/'result.json').write_text(json.dumps(r,indent=2));(OUT/'trace.json').write_text(json.dumps(trace,indent=2))
        print(json.dumps(r,indent=2))
