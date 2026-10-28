"""Cross-check vertical-driver hood against latest body and speaker pieces."""
import json
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;O=Path(__file__).resolve().parent;P=O.parent;C=P.parent

def stl(path):
 m=Mesh.Mesh(str(path));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);return Part.makeSolid(s.Shells[0])
def box(ext,c):
 x,y,z=ext;a,b,d=c;return Part.makeBox(x,y,z,V(a-x/2,b-y/2,d-z/2))
def ov(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return round(a.common(b).Volume,3)
hood=stl(O/'Cece_head_vertical_driver_hood_CANDIDATE.stl')
body=stl(P/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
ant=stl(C/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');ant.translate(V(0,0,27))
pod=stl(P/'speaker_pod/speaker_pod_tray.stl');grille=stl(P/'speaker_pod/speaker_retaining_grille.stl')
frame=stl(P/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl');frame.translate(V(0,-37.5,-19))
src=Part.read(str(P/'reference/piicodev_ce09181.step'));rot=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));x,y,z=1,13,13;driver=src.copy();driver.Placement=App.Placement(V(x,y,z)-rot.multVec(V(97.282,-88.046,4.8)),rot)
plugs={f'Plug{i}':box((9.6,18.15,3.2),(x-.044,y-6.15-9.075,z+q)) for i,q in enumerate([7.62,2.54,-2.54,-7.62])}
other={'V4_Body':body,'Antenna':ant,'Speaker_Pod':pod,'Speaker_Grille':grille,'OLED_Frame':frame,'Driver_STEP':driver,'ESP':box((28,8,21),(0,24,10)),'Amp':box((22,22,6),(17,-5,24)),'Mic':box((16,16,6),(-14,-5,24)),'Sensor_PCB':box((45,1.6,20),(0,-18,14.5)),'UBEC':box((21,56,14),(2.3,0,-8)),'Battery':box((35,56,16),(0,3,-24)),'Top_JST_Exit':box((9,8,10),(x+13.3,y,z+9.423+5)),'Bottom_USB_Exit':box((9,8,10),(x-14.708,y,z-8.51-5)),**plugs}
r={'hood_vs':{n:ov(hood,s) for n,s in other.items()},'selected_vs_body':{n:ov(body,s) for n,s in other.items() if n!='V4_Body'},'limits':['Official STEP omits PiicoDev USB-C and JST-SH sockets; selected exit boxes are conservative proxies.','Only static neutral geometry and assumed ESP/amp/mic/servo connector envelopes checked.','Head/body joint, retention/fastener details, wire flex and actual measured hardware still require validation.']}
(O/'final_integration_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
