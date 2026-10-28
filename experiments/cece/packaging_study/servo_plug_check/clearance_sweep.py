"""Targeted clearance improvements with frozen head and V4 body."""
import json
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;O=Path(__file__).resolve().parent;P=O.parent

def stl(path):
 m=Mesh.Mesh(str(path));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
head=stl(O/'Cece_head_vertical_driver_hood_CANDIDATE.stl');body=stl(P/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
source=Part.read(str(P/'reference/piicodev_ce09181.step'));rot=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));driver=source.copy();driver.Placement=App.Placement(V(1,13,13)-rot.multVec(V(97.282,-88.046,4.8)),rot)
speaker=stl(P/'speaker_pod/speaker_pod_tray.stl');amp=box((22,22,6),(17,-5,24));mic=box((16,16,6),(-14,-5,24));ub_base=box((21,56,14),(2.3,0,-8));bat_base=box((35,56,16),(0,3,-24))
r={'esp_rear_sweep':{},'power_vertical_sweep':{},'limits':['Board and power modules are clearance envelopes; exact connectors/wire bends untested.','Distance to head solid is not a mounting clearance check and does not include 3D printed clip.']}
for y in [24,24.5,25,25.5,26,26.5,27,27.5,28]:
 esp=box((28,8,21),(0,y,10))
 r['esp_rear_sweep'][str(y)]={'head_overlap_mm3':ov(esp,head),'body_overlap_mm3':ov(esp,body),'speaker_pod_overlap_mm3':ov(esp,speaker),'driver_overlap_mm3':ov(esp,driver),'driver_gap_mm':round(esp.distToShape(driver)[0],3),'amp_overlap_mm3':ov(esp,amp),'mic_overlap_mm3':ov(esp,mic)}
for bat_z in [-24,-24.5,-25,-25.5,-26]:
 b=box((35,56,16),(0,3,bat_z))
 for ub_z in [-8,-8.5,-9,-9.5]:
  u=box((21,56,14),(2.3,0,ub_z))
  key=f'battery{bat_z}_ubec{ub_z}'
  r['power_vertical_sweep'][key]={'battery_body_overlap_mm3':ov(b,body),'ubec_body_overlap_mm3':ov(u,body),'battery_ubec_overlap_mm3':ov(b,u),'battery_ubec_gap_mm':round(b.distToShape(u)[0],3),'ubec_driver_overlap_mm3':ov(u,driver),'ubec_driver_gap_mm':round(u.distToShape(driver)[0],3)}
(O/'clearance_sweep_results.json').write_text(json.dumps(r,indent=2))
for k,v in r['esp_rear_sweep'].items():print('ESP',k,v)
for k,v in r['power_vertical_sweep'].items():
 if v['battery_body_overlap_mm3']==0 and v['ubec_body_overlap_mm3']==0 and v['battery_ubec_overlap_mm3']==0 and v['ubec_driver_overlap_mm3']==0 and v['battery_ubec_gap_mm']>=2 and v['ubec_driver_gap_mm']>=2:print('POWER_GOOD',k,v)
