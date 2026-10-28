"""Vertical PiicoDev driver exploratory fit using partial official STEP."""
import json
from pathlib import Path
import FreeCAD as App, Part, Mesh
V=App.Vector
O=Path(__file__).resolve().parent;P=O.parent

def from_stl(p):
 m=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
head=from_stl(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl')
body=from_stl(P/'charger_cassette/cece_body_with_charger_posts_CANDIDATE.stl')
antenna=from_stl(P.parent/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');antenna.translate(V(0,0,27))
sensor=box((45,1.6,20),(0,-18,14.5))
amp=box((22,22,6),(10,17,24));mic=box((16,16,6),(-14,17,24))
source=Part.read(str(P/'reference/piicodev_ce09181.step'))
r={'limits':['Partial KiCad STEP omits USB-C and JST-SH physical connector solids.','Plug envelopes are conservative 3-pin servo housing surrogate; real SG90 housing/engagement unknown.','Edge USB-C/JST service corridors are 10mm straight boxes and do not establish bend radius or cable connector fit.'] ,'candidates':{}}
for face,deg in [('front',90),('rear',-90)]:
 for Z in [9,11,14]:
  Y=13
  rz=App.Rotation(V(0,0,1),-90);rx=App.Rotation(V(1,0,0),deg);rot=rx.multiply(rz)
  step=source.copy();step.Placement=App.Placement(V(0,Y,Z)-rot.multVec(V(97.282,-88.046,4.8)),rot)
  # pin tips are 6.15mm along board front/back from its central plane.
  pin_y=Y+(-6.15 if deg==90 else 6.15)
  # Conservative mated plug extends 18.15mm away from pin-tip plane.
  py=pin_y+(-18.15/2 if deg==90 else 18.15/2)
  plugs=[box((9.6,18.15,3.2),(-.044,py,Z+z)) for z in [7.62,2.54,-2.54,-7.62]]
  # USB-C and JST-SH sockets at short-edge positions in PCB source;
  # service corridors run 10mm vertically outward from each edge.
  edge=[]
  for X,T in [(-14.708,8.51),(13.3,9.423)]:
   for sgn in [-1,1]:
    edge.append(box((9,8,10),(X,Y, Z+sgn*(T+5))))
  c={'driver_bbox_mm':[[round(step.BoundBox.XMin,2),round(step.BoundBox.YMin,2),round(step.BoundBox.ZMin,2)],[round(step.BoundBox.XMax,2),round(step.BoundBox.YMax,2),round(step.BoundBox.ZMax,2)]], 'driver_overlap_mm3':{'head':ov(step,head),'body':ov(step,body),'sensor':ov(step,sensor),'amp':ov(step,amp),'mic':ov(step,mic)}, 'plug_overlap_mm3':{'head':[ov(p,head) for p in plugs],'body':[ov(p,body) for p in plugs],'sensor':[ov(p,sensor) for p in plugs],'antenna':[ov(p,antenna) for p in plugs]},'edge_corridor_overlap_mm3':{'head':[ov(e,head) for e in edge],'body':[ov(e,body) for e in edge],'antenna':[ov(e,antenna) for e in edge]}}
  r['candidates'][f'{face}_Y{Y}_Z{Z}']=c
(O/'vertical_driver_results.json').write_text(json.dumps(r,indent=2))
for n,c in r['candidates'].items():print(n,c)
