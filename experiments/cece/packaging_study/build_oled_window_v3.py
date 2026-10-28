"""Candidate Cece heart/window correction against official Adafruit 4741 STEP.

Run generate_oled_window_v3_mesh.py first, then this with FreeCAD 1.1 Python.
This does not finish board retention or shell mounts.
"""
from pathlib import Path
import json
import FreeCAD as App,Part,Mesh
V=App.Vector
ROOT=Path(__file__).resolve().parent
def from_stl(p):
    mesh=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(mesh.Topology,.01)
    return Part.makeSolid(s.Shells[0])
def valid(s,n):
    if not s.isValid() or len(s.Solids)!=1:raise ValueError(f'{n}: invalid or not one solid')
def add(doc,name,shape,color):
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape
    if o.ViewObject is not None:o.ViewObject.ShapeColor=color
    return o

body=from_stl(ROOT/'Cece_Body_4741_WindowV3_CANDIDATE.stl');valid(body,'body')
frame=from_stl(ROOT/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl');valid(frame,'frame')

oled=Part.read(str(ROOT/'reference'/'adafruit_4741.step'))
rot=App.Rotation(V(1,1,1),-120)
oled.Placement=App.Placement(V(0,-38.4,-19)-rot.multVec(V(17.78,18.415,1.715)),rot)
active=oled.Placement.multVec(V(17.907,22.089,-1.1))
window_x=(-12.0,18.2);window_z=(-34.1,-3.9)
active_x=(active.x-13.43,active.x+13.43)
active_z=(active.z-13.43,active.z+13.43)
result={
 'status':'candidate window geometry only; not print-ready whole robot',
 'window_center_x_mm':3.1,'window_size_mm':[30.2,30.2],
 'nominal_active_center_x_mm':round(active.x,3),
 'active_bounds_x_mm':[round(x,3) for x in active_x],
 'active_bounds_z_mm':[round(x,3) for x in active_z],
 'window_bounds_x_mm':list(window_x),'window_bounds_z_mm':list(window_z),
 'nominal_active_margins_mm':{
   'left':round(active_x[0]-window_x[0],3),'right':round(window_x[1]-active_x[1],3),
   'bottom':round(active_z[0]-window_z[0],3),'top':round(window_z[1]-active_z[1],3)},
 'body_valid':body.isValid(),'frame_valid':frame.isValid(),
 'body_vs_frame_mm3':round(body.common(frame).Volume,3),
 'oled_vs_body_mm3':round(oled.common(body).Volume,3),
 'oled_vs_frame_mm3':round(oled.common(frame).Volume,3),
 'limits':['Actual OLED glass placement can vary from official model.','Frame front wall remains nominally 1.35 mm; impact/fatigue untested.','No screen retainer, cable exit, body mounting or connector clearance proven.','Body window may affect front wall rigidity or servo support; physical check required.']
}
doc=App.newDocument('Cece_OLED_Window_V3_Candidate')
bo=add(doc,'Body_Window_V3',body,(.85,.88,.93))
fo=add(doc,'Heart_Frame_Window_V3',frame,(1,.35,.35))
oo=add(doc,'Adafruit_4741_Official_CAD',oled,(.15,.2,.24))
if oo.ViewObject is not None:oo.ViewObject.Transparency=35
doc.recompute()
doc.saveAs(str(ROOT/'Cece_OLED_Window_V3_Candidate.FCStd'))
(ROOT/'oled_window_v3_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2),flush=True)
