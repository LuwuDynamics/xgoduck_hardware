from pathlib import Path
import math, json, xml.etree.ElementTree as ET
import numpy as np
import mujoco
from PIL import Image, ImageDraw
from base_rig import XML

here=Path(__file__).resolve().parent
parts=here.parent/'parts'
root=ET.fromstring(XML)
root.set('model','Cece four-servo provisional')
head=root.find('.//body[@name="head"]')
head.set('pos','0 0 .039')
head.remove(head.find('joint')) # fixed head: there is no fifth servo
root.find('.//body[@name="torso"]').remove(root.find('.//geom[@name="head_servo"]'))
act=root.find('actuator');act.remove(act.find('position[@name="head_yaw"]'))
assets=ET.Element('asset');root.insert(1,assets)
files={'body':'Cece_Otto_Body_OLED_Window.stl','head':'Cece_Otto_Head_LED_Ports.stl',
 'leg_l':'OttoDIY_Leg_V9.stl','leg_r':'leg_mirror.stl','foot_l':'OttoDIY_foot_V9.stl','foot_r':'foot_mirror.stl'}
for n,f in files.items(): ET.SubElement(assets,'mesh',name=n,file=str((parts/f).resolve()).replace('\\','/'),scale='.001 .001 .001')
for geom in root.findall('.//worldbody//geom'):
 if geom.get('name')!='floor':
  rgba=geom.get('rgba','0.3 0.3 0.3 1').split();rgba[-1]='0';geom.set('rgba',' '.join(rgba))
for name,asset,pos in [('torso','body','0 0 .039'),('head','head','0 0 0'),('left_leg','leg_l','0 -.024 .039'),('right_leg','leg_r','0 .024 .039'),('left_foot','foot_l','0 -.0345 .079'),('right_foot','foot_r','0 .0345 .079')]:
 b=root.find('.//body[@name="%s"]'%name)
 ET.SubElement(b,'geom',name='visual_'+name,type='mesh',mesh=asset,euler='0 0 90',pos=pos,mass='0',contype='0',conaffinity='0',rgba='.4 .78 .3 1')
xml=ET.tostring(root,encoding='unicode');m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
render=mujoco.Renderer(m,600,800); camera=mujoco.MjvCamera();camera.distance=.40;camera.azimuth=135;camera.elevation=-14
frames=[]; max_tilt=0; start=None
for i in range(1000):
 t=d.time; ramp=min(1,t/.7); phase=2*math.pi*t
 hip=math.radians(30)*math.sin(phase)*ramp;ankle=math.radians(20)*math.sin(phase-math.pi/2)*ramp
 d.ctrl[:]=[hip,ankle,-hip,ankle];mujoco.mj_step(m,d,nstep=5)
 torso=d.xpos[m.body('torso').id].copy()
 if start is None:start=torso.copy()
 mat=d.xmat[m.body('torso').id].reshape(3,3); tilt=math.degrees(math.acos(float(np.clip(mat[2,2],-1,1))));max_tilt=max(max_tilt,tilt)
 if i%5==0:
  camera.lookat[:]=torso+[0,0,.04];render.update_scene(d,camera=camera)
  im=Image.fromarray(render.render());ImageDraw.Draw(im).text((10,10),'Cece prototype | fixed head | four servos | %.2f s'%t,fill='white');frames.append(im)
 if tilt>55 or torso[2]<.018:break
render.close()
frames[0].save(here/'cece_four_servo.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,optimize=True)
r={'elapsed_s':round(float(d.time),2),'upright_at_end':bool(max_tilt<55 and torso[2]>=.018),'max_tilt_deg':round(max_tilt,2),'displacement_mm':np.round((torso-start)*1000,2).tolist(),'assumed_mass_g':round(float(sum(m.body_mass)*1000),1),'limitations':['Visual mesh only; collision bodies are generic boxes','Mass, center of gravity, servo torque, gait and contacts are assumed','Battery, driver, wires and real mechanical fit not simulated','Faceplate, OLED, sensor, LEDs and audio components are not rendered','Not hardware validation or proof of walking']}
(here/'result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
