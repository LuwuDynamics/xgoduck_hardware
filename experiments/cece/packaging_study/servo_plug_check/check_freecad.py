import json
from pathlib import Path
import FreeCAD as App, Part, Mesh
V=App.Vector
O=Path(__file__).resolve().parent;P=O.parent; C=P.parent
def from_stl(p):
 m=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
head=from_stl(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl')
body=from_stl(P/'charger_cassette/cece_body_with_charger_posts_CANDIDATE.stl')
source=Part.read(str(P/'reference/piicodev_ce09181.step'))
rot=App.Rotation(V(0,0,1),-90)
source.Placement=App.Placement(V(0,0,8)-rot.multVec(V(97.282,-88.046,4.8)),rot)
header_y=[7.62,2.54,-2.54,-7.62]
# Nominal 9.6x2.7x14 mm Futaba/JR housing sourced from Muldental.
# Extra 0.5 mm Y and 4.15 mm Z guard the unknown actual mated insertion height.
plugs={f'Plug_{i+1}':box((9.6,3.2,18.15),(-.044,y,19.075)) for i,y in enumerate(header_y)}
old_esp=box((28,21,8),(0,-5,21));new_esp=box((21,28,8),(-18.5,-1,21))
vertical_rear_esp=box((28,8,21),(0,22,10))
vertical_rear_esp_y20=box((28,8,21),(0,20,10))
old_mic=box((16,16,6),(-14,17,24));new_mic=box((16,16,6),(-14,21,24))
amp=box((22,22,6),(10,17,24));sensor=box((45,1.6,20),(0,-18,14.5));speaker=Part.makeCylinder(14,7,V(0,32.5,15),V(0,1,0))
variants={'Current_ESP':old_esp,'Rotated_Left_ESP':new_esp,'Vertical_Rear_ESP':vertical_rear_esp,'Vertical_Rear_ESP_Y20':vertical_rear_esp_y20,'Current_Mic':old_mic,'Rear_Mic':new_mic}
r={'source':'PiicoDev official KiCad board + partial STEP; Rapid SG90 plug unspecified; surrogate Futaba connector dimensions 14x9.6x2.7 mm','header_centers_xyz_mm':[[ -.044,y,14.15] for y in header_y],'plug_proxy_size_mm':[9.6,3.2,18.15],'plug_proxy_z_mm':[10,28.15],'checks':{},'limits':['Proxy includes over-height reserve; actual SG90 plug geometry and insertion depth unknown.','Only housings represented, wires and bend radius absent.','ESP and mic dimension envelopes are assumed; actual board headers and cable paths absent.','Head shell is latest speaker-mount candidate STL.']}
for name,s in variants.items():
 r['checks'][name]={'head_overlap_mm3':ov(s,head),'body_overlap_mm3':ov(s,body),'driver_step_overlap_mm3':ov(s,source),'plug_overlap_mm3':{pn:ov(s,ps) for pn,ps in plugs.items()},'sensor_overlap_mm3':ov(s,sensor),'speaker_overlap_mm3':ov(s,speaker),'amp_overlap_mm3':ov(s,amp),'mic_overlap_mm3':ov(s,old_mic)}
 if name=='Vertical_Rear_ESP_Y20':
  r['checks'][name]['min_gaps_mm']={qn:round(s.distToShape(qs)[0],3) for qn,qs in {'head':head,'body':body,'driver_step':source,'plug_1':plugs['Plug_1'],'plug_2':plugs['Plug_2'],'plug_3':plugs['Plug_3'],'plug_4':plugs['Plug_4'],'sensor':sensor,'speaker':speaker,'amp':amp,'mic':old_mic}.items()}
r['checks']['Rotated_Left_ESP']['rear_mic_overlap_mm3']=ov(new_esp,new_mic)
r['checks']['Rear_Mic']['rotated_esp_overlap_mm3']=ov(new_mic,new_esp)
(O/'results.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
