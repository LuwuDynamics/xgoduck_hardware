import json
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;P=Path('xgoduck_project_repo/experiments/cece/packaging_study')
def shape(p):
 m=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
head=shape(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl')
source=Part.read(str(P/'reference/piicodev_ce09181.step'));r=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));source.Placement=App.Placement(V(0,13,9)-r.multVec(V(97.282,-88.046,4.8)),r)
for name,size,c in [('ESP_y24',(28,8,21),(0,24,10)),('amp_z25',(22,22,6),(10,17,25)),('mic_z25',(16,16,6),(-14,17,25)),('amp_z26',(22,22,6),(10,17,26)),('mic_z26',(16,16,6),(-14,17,26))]:
 s=box(size,c);print(name,'head',ov(s,head),'driver',ov(s,source))
c=box((9,8,10),(13.3,13,23.423));i=c.common(head);b=i.BoundBox;print('upper JST corridor-head overlap',i.Volume,'bounds',[[b.XMin,b.YMin,b.ZMin],[b.XMax,b.YMax,b.ZMax]])
