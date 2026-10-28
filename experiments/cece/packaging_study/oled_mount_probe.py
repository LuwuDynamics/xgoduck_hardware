"""Check official 4741 corner holes against a candidate four-screw stack.

The nominal hole pitches come from Adafruit's Eagle board: installed X pitch
41.91 mm and installed Z pitch 30.48 mm. This does not specify fastener length
or approve printed boss strength.
"""
from pathlib import Path
import json
import FreeCAD as App,Part,Mesh

V=App.Vector; ROOT=Path(__file__).resolve().parent
def from_stl(path):
 m=Mesh.Mesh(str(path)); s=Part.Shape();s.makeShapeFromMesh(m.Topology,.01)
 return Part.makeSolid(s.Shells[0])
body=from_stl(ROOT/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
frame=from_stl(ROOT/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl')
oled=Part.read(str(ROOT/'reference'/'adafruit_4741.step'))
r=App.Rotation(V(1,1,1),-120)
oled.Placement=App.Placement(V(0,-38.4,-19)-r.multVec(V(17.78,18.415,1.715)),r)
parts={'Body':body,'Frame':frame,'OLED':oled}
out={'nominal_pitch_mm':[41.91,30.48],'holes':{},'warning':'CAD hole alignment only; screws, boss load and OLED variation unverified'}
for x in (-20.955,20.955):
 for z in (-34.24,-3.76):
  key=f'{x:+.3f},{z:+.3f}'
  pilot=Part.makeCylinder(1.1,16,V(x,-44,z),V(0,1,0))
  boss=Part.makeCylinder(2.6,7,V(x,-38,z),V(0,1,0))
  out['holes'][key]={
    'pilot_overlap_mm3':{n:round(pilot.common(s).Volume,4) for n,s in parts.items()},
    'boss_overlap_mm3':{n:round(boss.common(s).Volume,4) for n,s in parts.items()},
  }
(ROOT/'oled_mount_probe_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
