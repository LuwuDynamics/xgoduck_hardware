"""FreeCAD exact partial-PiicoDev STEP clash check for combined V3 head."""
import json
from pathlib import Path
import FreeCAD as App
import Part,Mesh

V=App.Vector;HERE=Path(__file__).resolve().parent;P=HERE.parents[1]
def stl(path):
    m=Mesh.Mesh(str(path));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01)
    assert len(s.Shells)==1
    return Part.makeSolid(s.Shells[0])
def box(ext,c):
    dx,dy,dz=ext;x,y,z=c
    return Part.makeBox(dx,dy,dz,V(x-dx/2,y-dy/2,z-dz/2))
def ov(a,b):
    if not a.BoundBox.intersect(b.BoundBox):return 0.0
    return round(a.common(b).Volume,5)

head=stl(HERE/'Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl')
face=stl(HERE/'Cece_faceplate_M2_retained_V3_CANDIDATE.stl')
src=Part.read(str(P/'reference/piicodev_ce09181.step'))
rot=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90))
x,y,z=1,11.8,13
driver=src.copy();driver.Placement=App.Placement(V(x,y,z)-rot.multVec(V(97.282,-88.046,4.8)),rot)
plugs={f'plug_{i}':box((9.6,18.15,3.2),(x-.044,y-6.15-9.075,z+q)) for i,q in enumerate([7.62,2.54,-2.54,-7.62])}
mods={
 'driver_partial_STEP':driver,
 'top_JST_10mm_service_box':box((9,8,10),(x+13.3,y,z+9.423+5)),
 'bottom_USB_10mm_service_box':box((9,8,10),(x-14.708,y,z-8.51-5)),
 'ESP':box((28,8,21),(0,24,10)),
 'Amp':box((22,22,6),(17,-6,24)),
 'Mic':box((16,16,6),(-14,-5,24)),
 'Sensor_PCB':box((45,1.6,20),(0,-18,14.5)),
 **plugs,
}
r={'source_driver_step':'packaging_study/reference/piicodev_ce09181.step','placement':[x,y,z],
   'head_overlaps_mm3':{k:ov(head,v) for k,v in mods.items()},
   'face_overlaps_mm3':{k:ov(face,v) for k,v in mods.items()},
   'limits':['USB-C and JST-SH connector solids absent from manufacturer STEP','Proposed service boxes are ideal straight corridors, not actual cable bends']}
(HERE/'exact_driver_check.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
