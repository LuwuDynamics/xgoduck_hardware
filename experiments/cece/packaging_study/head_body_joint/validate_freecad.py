"""FreeCAD reimport and exact supplier STEP checks for head/body screw joint."""
from pathlib import Path
import json
import FreeCAD as App
import Mesh,Part

V=App.Vector;HERE=Path(__file__).resolve().parent;P=HERE.parent
HEAD=HERE/'Cece_head_V3_four_screw_joint_CANDIDATE.stl'
BODY=HERE/'Cece_body_V4_four_screw_joint_CANDIDATE.stl'

def solid(path):
    m=Mesh.Mesh(str(path));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01)
    assert len(s.Shells)==1,(path,'shells',len(s.Shells))
    a=Part.makeSolid(s.Shells[0]);assert a.isValid() and len(a.Solids)==1
    return a
def ov(a,b):
    if not a.BoundBox.intersect(b.BoundBox):return 0.0
    return round(a.common(b).Volume,5)

head=solid(HEAD);body=solid(BODY)
driver_src=Part.read(str(P/'reference/piicodev_ce09181.step'))
rot=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90))
x,y,z=1,11.8,13
driver=driver_src.copy();driver.Placement=App.Placement(V(x,y,z)-rot.multVec(V(97.282,-88.046,4.8)),rot)

oled=Part.read(str(P/'reference/adafruit_4741.step'))
oled_rot=App.Rotation(V(1,1,1),-120)
oled.Placement=App.Placement(V(0,-38.4,-19)-oled_rot.multVec(V(17.78,18.415,1.715)),oled_rot)

r={
 'head_valid':head.isValid(),'head_solids':len(head.Solids),
 'body_valid':body.isValid(),'body_solids':len(body.Solids),
 'head_body_overlap_mm3':ov(head,body),
 'head_partial_PiicoDev_STEP_overlap_mm3':ov(head,driver),
 'body_partial_PiicoDev_STEP_overlap_mm3':ov(body,driver),
 'head_official_Adafruit4741_STEP_overlap_mm3':ov(head,oled),
 'body_official_Adafruit4741_STEP_overlap_mm3':ov(body,oled),
 'limits':['Supplier PiicoDev STEP omits physical USB-C/JST-SH connectors and mated cables.',
           'Official OLED STEP excludes the selected harness and header bend.']}
(HERE/'freecad_validation.json').write_text(json.dumps(r,indent=2))

doc=App.newDocument('Cece_Head_Body_Four_Screw_Joint_Candidate')
for name,path in [('Head_4Screw_STL',HEAD),('Body_4Screw_STL',BODY)]:
    o=doc.addObject('Mesh::Feature',name);o.Mesh=Mesh.Mesh(str(path))
for name,shape in [('Driver_Partial_STEP_Reference',driver),('OLED_Official_STEP_Reference',oled)]:
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape
    if o.ViewObject is not None:o.ViewObject.Visibility=False
for sx in (-1,1):
 for sy in (-1,1):
    y=sy*22.5;z=-8
    start=V(sx*35.5,y,z);direction=V(-sx,0,0)
    shaft=Part.makeCylinder(1.5,8,start,direction)
    cap=Part.makeCylinder(3.0,2,start,V(sx,0,0))
    o=doc.addObject('PartDesign::Feature',f'M3x8_Screw_Envelope_{"R" if sx>0 else "L"}_{"Rear" if sy>0 else "Front"}')
    o.Shape=shaft.fuse(cap)
    if o.ViewObject is not None:o.ViewObject.Visibility=False
doc.recompute();doc.saveAs(str(HERE/'Cece_Head_Body_Four_Screw_Joint_CANDIDATE.FCStd'))
print(json.dumps(r,indent=2))
