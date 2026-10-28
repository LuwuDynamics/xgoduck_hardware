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
head=stl(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl');body=stl(P/'charger_cassette/cece_body_with_charger_posts_CANDIDATE.stl');ant=stl(P.parent/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');ant.translate(V(0,0,27))
src=Part.read(str(P/'reference/piicodev_ce09181.step'))
x,y,z=-1,13,13.7;r=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));driver=src.copy();driver.Placement=App.Placement(V(x,y,z)-r.multVec(V(97.282,-88.046,4.8)),r)
pin_y=y-6.15;plugs={f'Plug_{i}':box((9.6,18.15,3.2),(x-.044,pin_y-9.075,z+q)) for i,q in enumerate([7.62,2.54,-2.54,-7.62])}
edge={}
for label,X,T in [('USB',-14.708,8.51),('JST',13.3,9.423)]:
 for sign in [-1,1]:edge[f'{label}_{"top" if sign>0 else "bottom"}']=box((9,8,10),(x+X,y,z+sign*(T+5)))
modules={'Driver':driver,'ESP':box((28,8,21),(0,24,10)),'Amp':box((22,22,6),(17,-5,24)),'Mic':box((16,16,6),(-14,-5,24)),'Sensor_PCB':box((45,1.6,20),(0,-18,14.5)),'Speaker':Part.makeCylinder(14,7,V(0,32.5,15),V(0,1,0)),'UBEC':box((21,56,14),(0,0,-8)),'Battery':box((35,56,16),(0,3,-24)),**plugs,**{f'Corridor_{k}':v for k,v in edge.items()}}
report={'placements':{'driver_step_origin_mm':[x,y,z],'ESP_center_mm':[0,24,10],'amp_center_mm':[17,-5,24],'mic_center_mm':[-14,-5,24]},'collisions':{}}
for n,s in modules.items():
 q={'head':ov(s,head),'body':ov(s,body),'antenna':ov(s,ant)}
 for k,t in modules.items():
  if k!=n and ov(s,t)>0:q[k]=ov(s,t)
 report['collisions'][n]={k:v for k,v in q.items() if v>0}
Path('xgoduck_project_repo/experiments/cece/packaging_study/servo_plug_check/full_candidate_results.json').write_text(json.dumps(report,indent=2))
for n,v in report['collisions'].items():print(n,v)
