"""Check whether forward driver movement makes room for rear ESP."""
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
head=stl(O/'Cece_head_vertical_driver_hood_CANDIDATE.stl');body=stl(P/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl');src=Part.read(str(P/'reference/piicodev_ce09181.step'));rot=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90))
esp=box((28,8,21),(0,24,10));amp=box((22,22,6),(17,-6,24));mic=box((16,16,6),(-14,-5,24));ub=box((21,56,14),(2.3,0,-8));bat=box((35,56,16),(0,3,-24));sensor=box((45,1.6,20),(0,-18,14.5))
r={}
for y in [11.8,12,12.5,13]:
 x,z=1,13;d=src.copy();d.Placement=App.Placement(V(x,y,z)-rot.multVec(V(97.282,-88.046,4.8)),rot)
 upper=box((9,8,10),(x+13.3,y,z+9.423+5));lower=box((9,8,10),(x-14.708,y,z-8.51-5));plugs=[box((9.6,18.15,3.2),(x-.044,y-6.15-9.075,z+q)) for q in [7.62,2.54,-2.54,-7.62]]
 r[str(y)]={'driver_esp_gap_mm':round(d.distToShape(esp)[0],3),'driver_head_overlap_mm3':ov(d,head),'driver_amp_overlap_mm3':ov(d,amp),'driver_mic_overlap_mm3':ov(d,mic),'driver_UBEC_overlap_mm3':ov(d,ub),'upper_JST_hood_overlap_mm3':ov(upper,head),'lower_USB_body_overlap_mm3':ov(lower,body),'lower_USB_UBEC_overlap_mm3':ov(lower,ub),'servo_plug_head_overlap_mm3':[ov(p,head) for p in plugs],'servo_plug_sensor_overlap_mm3':[ov(p,sensor) for p in plugs],'servo_plug_amp_overlap_mm3':[ov(p,amp) for p in plugs],'servo_plug_mic_overlap_mm3':[ov(p,mic) for p in plugs]}
(O/'driver_forward_results.json').write_text(json.dumps(r,indent=2))
for k,v in r.items():print(k,v)
