"""Interactive MuJoCo visual prototype. The arm joints and masses are illustrative.
No electronics, cable clearances, measured material properties or fit are modeled.
Close the viewer to stop. The simulation automatically restarts after 10 s or a fall.
"""
from pathlib import Path
import math, time, xml.etree.ElementTree as ET
import numpy as np
import mujoco
import mujoco.viewer
from base_rig import XML

here=Path(__file__).resolve().parent
parts=here.parent/'parts';draft=here.parent/'parts_happy_draft'
root=ET.fromstring(XML);root.set('model','Cece Happy - prototype four servos and passive arms')
torso=root.find('.//body[@name="torso"]');head=root.find('.//body[@name="head"]');head.set('pos','0 0 .039')
head.remove(head.find('joint'));torso.remove(root.find('.//geom[@name="head_servo"]'))
act=root.find('actuator');act.remove(act.find('position[@name="head_yaw"]'))
assets=ET.Element('asset');root.insert(1,assets)
files={'body':draft/'Cece_Body_Rounded_DRAFT.stl','head':draft/'Cece_Head_Centered_Antenna_DRAFT.stl',
 'arm_l':draft/'Cece_Left_Arm_45_DRAFT.stl','arm_r':draft/'Cece_Right_Arm_45_DRAFT.stl','antenna':draft/'Cece_Antenna_DRAFT.stl',
 'face':draft/'Cece_Happy_Faceplate_DRAFT.stl','oled':parts/'Cece_OLED_Retaining_Frame.stl',
 'leg_l':parts/'OttoDIY_Leg_V9.stl','leg_r':parts/'leg_mirror.stl',
 'foot_l':parts/'OttoDIY_foot_V9.stl','foot_r':parts/'foot_mirror.stl'}
for name,path in files.items():
 ET.SubElement(assets,'mesh',name=name,file=str(path.resolve()).replace('\\','/'),scale='.001 .001 .001')
for geom in root.findall('.//worldbody//geom'):
 if geom.get('name')!='floor':
  rgba=geom.get('rgba','0.3 0.3 0.3 1').split();rgba[-1]='0';geom.set('rgba',' '.join(rgba))
for name,asset,pos in [('torso','body','0 0 .039'),('head','head','0 0 0'),('left_leg','leg_l','0 -.024 .039'),('right_leg','leg_r','0 .024 .039'),('left_foot','foot_l','0 -.0345 .079'),('right_foot','foot_r','0 .0345 .079')]:
 b=root.find('.//body[@name="%s"]'%name)
 ET.SubElement(b,'geom',name='visual_'+name,type='mesh',mesh=asset,euler='0 0 90',pos=pos,
               mass='0',contype='0',conaffinity='0',rgba='.35 .8 .29 1')
for label,asset,b,pos in [('face','face',head,'0 0 0'),('oled','oled',torso,'.0375 0 .020'),('antenna','antenna',head,'0 0 .027')]:
 ET.SubElement(b,'geom',name='visual_'+label,type='mesh',mesh=asset,euler='0 0 90',pos=pos,
               mass='0',contype='0',conaffinity='0',rgba='.75 .85 .25 1')
for sign in [-1,1]:
 b=ET.SubElement(torso,'body',name='passive_arm_'+str(sign),pos=f'0 {sign*.0372} .024')
 ET.SubElement(b,'joint',type='hinge',name='arm_joint_'+str(sign),axis='0 1 0',range='-65 65',damping='.0003')
 ET.SubElement(b,'geom',type='mesh',mesh=('arm_l' if sign < 0 else 'arm_r'),euler='0 0 90',mass='.003',contype='0',conaffinity='0',rgba='.2 .65 .2 1')
# Coloured visual placeholders: LEDs, dark ultrasonic cans and OLED surface.
for x,z,r,c in [(-.025,.023,.0026,'.1 .8 1 1'),(.025,.023,.0026,'.1 .8 1 1'),(-.0055,.0045,.0016,'1 .2 .1 1'),(0,.002,.0016,'1 .2 .1 1'),(.0055,.0045,.0016,'1 .2 .1 1')]:
 ET.SubElement(head,'geom',type='sphere',size=str(r),pos=f'.035 {x} {z}',mass='0',contype='0',conaffinity='0',rgba=c)
for y in (-.013,.013):
 ET.SubElement(head,'geom',type='sphere',size='.0075',pos=f'.0325 {y} .0145',mass='0',contype='0',conaffinity='0',rgba='.15 .15 .15 1')
ET.SubElement(torso,'geom',type='box',size='.0003 .012 .0038',pos='.041 0 .020',mass='0',contype='0',conaffinity='0',rgba='.02 .04 .05 1')
model=mujoco.MjModel.from_xml_string(ET.tostring(root,encoding='unicode'));data=mujoco.MjData(model)
print('MuJoCo Cece: fixed head, four driven legs and two passive visual arms. Close window to exit.',flush=True)
with mujoco.viewer.launch_passive(model,data) as viewer:
 viewer.cam.distance=.45;viewer.cam.azimuth=135;viewer.cam.elevation=-14
 while viewer.is_running():
  start=time.perf_counter();t=data.time;ramp=min(1,t/.7);phase=2*math.pi*t
  hip=math.radians(30)*math.sin(phase)*ramp;ankle=math.radians(20)*math.sin(phase-math.pi/2)*ramp
  data.ctrl[:]=[hip,ankle,-hip,ankle];mujoco.mj_step(model,data,nstep=5)
  pos=data.xpos[model.body('torso').id].copy();viewer.cam.lookat[:]=pos+[0,0,.04]
  viewer.sync()
  mat=data.xmat[model.body('torso').id].reshape(3,3);tilt=math.degrees(math.acos(float(np.clip(mat[2,2],-1,1))))
  if t>10 or tilt>55 or pos[2]<.018:mujoco.mj_resetData(model,data)
  time.sleep(max(0,.01-(time.perf_counter()-start)))
