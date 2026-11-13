"""Interactive XGO-Duck MuJoCo walk using the project's published ONNX policy.

Uses the upstream standing scene and its simplified PD actuator model; this
is a physics experiment, not a physical-robot validation. Space pauses; R resets.
"""
import time, math, numpy as np, mujoco, mujoco.viewer
from xgoduck_walk_simulation import SCENE, Policy, POLICY_INDEX, JOINTS

model=mujoco.MjModel.from_xml_path(str(SCENE))
data=mujoco.MjData(model)
stand=model.key('STAND').id
mujoco.mj_resetDataKeyframe(model,data,stand)
mujoco.mj_forward(model,data)
qadr=np.array([model.joint(n).qposadr[0] for n in JOINTS])
vadr=np.array([model.joint(n).dofadr[0] for n in JOINTS])
assert [model.actuator(i).name for i in range(model.nu)]==JOINTS
policy=Policy();ok,message=policy.load()
if not ok:raise RuntimeError(message)
steps=round(0.02/model.opt.timestep)
if abs(steps*model.opt.timestep-.02)>1e-9:raise RuntimeError('Bad control period')
state={'pause':False,'reset':False}
def key(k):
    if k==32:state['pause']=not state['pause']
    if k in (ord('R'),ord('r')):state['reset']=True

with mujoco.viewer.launch_passive(model,data,key_callback=key,show_left_ui=True,show_right_ui=False) as viewer:
    viewer.cam.distance=.65;viewer.cam.azimuth=135;viewer.cam.elevation=-15
    while viewer.is_running():
        t0=time.perf_counter()
        if state['reset']:
            mujoco.mj_resetDataKeyframe(model,data,stand);mujoco.mj_forward(model,data)
            policy.reset_action_filter();state['reset']=False
        if not state['pause']:
            rotation=data.site_xmat[model.site('imu').id].reshape(3,3)
            gravity=rotation.T @ np.array([0.,0.,-1.])
            gyro=data.sensor('imu_ang_vel').data.copy()
            angles=np.zeros(15);velocity=np.zeros(15)
            angles[POLICY_INDEX]=np.rad2deg(data.qpos[qadr])
            velocity[POLICY_INDEX]=np.rad2deg(data.qvel[vadr])
            speed=.3*max(0,min(1,(data.time-.5)))
            action=policy.infer(gravity,gyro,angles.tolist(),velocity.tolist(),[speed,0,0],[0,0,0,0])
            data.ctrl[:]=np.deg2rad(np.asarray(policy.action_to_deg(action))[POLICY_INDEX])
            mujoco.mj_step(model,data,nstep=steps)
        viewer.cam.lookat[:]=data.xpos[model.body('trunk_base').id]+[0,0,.04]
        viewer.sync()
        remaining=.02-(time.perf_counter()-t0)
        if remaining>0:time.sleep(remaining)
