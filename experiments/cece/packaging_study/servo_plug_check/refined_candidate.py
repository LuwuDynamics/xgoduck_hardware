import json
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;O=Path(__file__).resolve().parent;P=O.parent
def stl(p):
 m=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
head=stl(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl');body=stl(P/'charger_cassette/cece_body_with_charger_posts_CANDIDATE.stl');ant=stl(P.parent/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');ant.translate(V(0,0,27));src=Part.read(str(P/'reference/piicodev_ce09181.step'));r=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));x,y,z=1,13,13;driver=src.copy();driver.Placement=App.Placement(V(x,y,z)-r.multVec(V(97.282,-88.046,4.8)),r)
mod={'ESP':box((28,8,21),(0,24,10)),'Amp':box((22,22,6),(17,-5,24)),'Mic':box((16,16,6),(-14,-5,24)),'Sensor':box((45,1.6,20),(0,-18,14.5)),'UBEC':box((21,56,14),(2.3,0,-8)),'Battery':box((35,56,16),(0,3,-24)),'Top_JST_exit':box((9,8,10),(x+13.3,y,z+9.423+5)),'Bottom_USB_exit':box((9,8,10),(x-14.708,y,z-8.51-5))}
plugs={f'Plug{i}':box((9.6,18.15,3.2),(x-.044,y-6.15-9.075,z+q)) for i,q in enumerate([7.62,2.54,-2.54,-7.62])}
mod['Driver']=driver;mod.update(plugs)
report={}
for n,s in mod.items():
 v={}
 for p,t in [('Head',head),('Body',body),('Antenna',ant)]:
  vol=ov(s,t)
  if vol>0:v[p]=vol
 for k,t in mod.items():
  if k==n:continue
  if k.startswith('Plug') and n=='Driver':continue
  if n.startswith('Plug') and k=='Driver':continue
  if k.endswith('_exit') and n=='Driver':continue
  if n.endswith('_exit') and k=='Driver':continue
  vol=ov(s,t)
  if vol>0:v[k]=vol
 report[n]=v
(O/'refined_candidate_results.json').write_text(json.dumps(report,indent=2))
for n,v in report.items():print(n,v)
