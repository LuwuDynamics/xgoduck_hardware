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
parts=here.parent/'parts';draft=here.parent/'parts_adafruit_draft'
root=ET.fromstring(XML);root.set('model','cece - Adafruit display concept and cleaned feet')
torso=root.find('.//body[@name="torso"]');head=root.find('.//body[@name="head"]');head.set('pos','0 0 .039')
head.remove(head.find('joint'));torso.remove(root.find('.//geom[@name="head_servo"]'))
act=root.find('actuator');act.remove(act.find('position[@name="head_yaw"]'))
assets=ET.Element('asset');root.insert(1,assets)
files={'body':draft/'cece_body_square_OLED_DRAFT.stl','head':draft/'Cece_Head_Centered_Antenna_DRAFT.stl',
 'arm_l':draft/'Cece_Left_Arm_45_DRAFT.stl','arm_r':draft/'Cece_Right_Arm_45_DRAFT.stl','antenna':draft/'Cece_Antenna_DRAFT.stl',
 'name':draft/'Cece_Name_Back_Visual_Overlay.stl',
 'face':draft/'Cece_Happy_Faceplate_DRAFT.stl','oled':draft/'cece_heart_frame_Adafruit4741_DRAFT.stl',
 'leg_l':parts/'OttoDIY_Leg_V9.stl','leg_r':parts/'leg_mirror.stl',
 'foot_l':draft/'cece_foot_right_clean.stl','foot_r':draft/'cece_foot_left_clean.stl'}
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
               mass='0',contype='0',conaffinity='0',rgba=('1 .18 .27 1' if label=='oled' else '.75 .85 .25 1'))
# Contrast overlays are visual only; same raised details are fused into the STL.
for name,colour in [('name','1 .96 .8 1')]:
 ET.SubElement(torso,'geom',name='visual_'+name,type='mesh',mesh=name,euler='0 0 90',
               pos='-.00008 0 .039',mass='0',contype='0',conaffinity='0',rgba=colour)
for sign in [-1,1]:
 b=ET.SubElement(torso,'body',name='passive_arm_'+str(sign),pos=f'0 {sign*.0372} .024')
 ET.SubElement(b,'joint',type='hinge',name='arm_joint_'+str(sign),axis='0 1 0',range='-65 65',damping='.0003')
 ET.SubElement(b,'geom',type='mesh',mesh=('arm_l' if sign < 0 else 'arm_r'),euler='0 0 90',mass='.003',contype='0',conaffinity='0',rgba='.2 .65 .2 1')
# Coloured visual placeholders: LEDs, dark ultrasonic cans and OLED surface.
for x,z,r,c in [(-.025,.023,.0026,'.1 .8 1 1'),(.025,.023,.0026,'.1 .8 1 1'),(-.008,.004,.0016,'1 .2 .1 1'),(-.004,.0029,.0016,'1 .2 .1 1'),(0,.0022,.0016,'1 .2 .1 1'),(.004,.0029,.0016,'1 .2 .1 1'),(.008,.004,.0016,'1 .2 .1 1')]:
 ET.SubElement(head,'geom',type='sphere',size=str(r),pos=f'.035 {x} {z}',mass='0',contype='0',conaffinity='0',rgba=c)
for y in (-.013,.013):
 ET.SubElement(head,'geom',type='sphere',size='.0075',pos=f'.0325 {y} .0145',mass='0',contype='0',conaffinity='0',rgba='.15 .15 .15 1')
ET.SubElement(torso,'geom',type='box',size='.0003 .0151 .0151',pos='.0437 0 .020',mass='0',contype='0',conaffinity='0',rgba='.02 .04 .05 1')
model=mujoco.MjModel.from_xml_string(ET.tostring(root,encoding='unicode'));data=mujoco.MjData(model)

import json
mx=0.;start=None;fall=False
for i in range(1000):
 t=data.time;ramp=min(1,t/.7);phase=2*math.pi*t
 hip=math.radians(30)*math.sin(phase)*ramp;ankle=math.radians(20)*math.sin(phase-math.pi/2)*ramp
 data.ctrl[:]=[hip,ankle,-hip,ankle];mujoco.mj_step(model,data,nstep=5)
 pos=data.xpos[model.body('torso').id].copy()
 if start is None:start=pos.copy()
 mat=data.xmat[model.body('torso').id].reshape(3,3);tilt=math.degrees(math.acos(float(np.clip(mat[2,2],-1,1))));mx=max(mx,tilt)
 if tilt>55 or pos[2]<.018:fall=True;break
report={'duration_s':round(float(data.time),2),'fell_in_model':fall,'max_tilt_degrees':round(mx,2),'displacement_mm':np.round((pos-start)*1000,1).tolist(),'assumed_total_mass_g':round(float(sum(model.body_mass)*1000),1),'limits':['proxy box contacts and assumed masses/actuator behavior','battery, OLED, electronics, wiring and charging hardware are absent','not a verified center-of-mass or real-world stability test']}
(here/'adafruit_proxy_motion_result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
