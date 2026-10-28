import json
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;P=Path('xgoduck_project_repo/experiments/cece/packaging_study')
def stl(p):
 m=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
head=stl(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl');body=stl(P/'charger_cassette/cece_body_with_charger_posts_CANDIDATE.stl');ant=stl(P.parent/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');ant.translate(V(0,0,27));src=Part.read(str(P/'reference/piicodev_ce09181.step'))
ub=box((21,56,14),(0,0,-8));bat=box((35,56,16),(0,3,-24));esp=box((28,8,21),(0,24,10));amp=box((22,22,6),(17,-5,24));mic=box((16,16,6),(-14,-5,24));sensor=box((45,1.6,20),(0,-18,14.5))
for z in [13,13.2,13.5,13.7]:
 x,y=-1,13;r=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));driver=src.copy();driver.Placement=App.Placement(V(x,y,z)-r.multVec(V(97.282,-88.046,4.8)),r)
 top_jst=box((9,8,10),(x+13.3,y,z+9.423+5));bottom_usb=box((9,8,10),(x-14.708,y,z-8.51-5));plugs=[box((9.6,18.15,3.2),(x-.044,y-6.15-9.075,z+q)) for q in [7.62,2.54,-2.54,-7.62]]
 print('z',z,'driver',{'head':ov(driver,head),'body':ov(driver,body),'UBEC':ov(driver,ub),'ESP':ov(driver,esp),'amp':ov(driver,amp),'mic':ov(driver,mic)},'topJST',{'head':ov(top_jst,head),'antenna':ov(top_jst,ant)},'bottomUSB',{'UBEC':ov(bottom_usb,ub),'body':ov(bottom_usb,body)},'plugs',{'head':[ov(p,head) for p in plugs],'sensor':[ov(p,sensor) for p in plugs],'amp':[ov(p,amp) for p in plugs],'mic':[ov(p,mic) for p in plugs]})
