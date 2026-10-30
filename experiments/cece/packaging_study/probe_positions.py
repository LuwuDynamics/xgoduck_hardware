"""Temporary fast scan of candidate occupied volumes against the exact shells."""
from pathlib import Path
import FreeCAD as App, Part, Mesh
V=App.Vector
base=Path(__file__).resolve().parent.parent/'parts_adafruit_draft'
def solid(path):
    m=Mesh.Mesh(str(path));s=Part.Shape();s.makeShapeFromMesh(m.Topology,.01)
    return Part.makeSolid(s.Shells[0])
def box(sz,c):
    return Part.makeBox(*sz,V(*[c[i]-sz[i]/2 for i in range(3)]))
body=solid(base/'cece_body_square_OLED_DRAFT.stl')
head=solid(base/'Cece_Head_Centered_Antenna_DRAFT.stl')
def v(a,b):
    aa=a.BoundBox;bb=b.BoundBox
    if aa.XMax<=bb.XMin or bb.XMax<=aa.XMin or aa.YMax<=bb.YMin or bb.YMax<=aa.YMin or aa.ZMax<=bb.ZMin or bb.ZMax<=aa.ZMin:return 0
    return round(a.common(b).Volume,2)
for label,sz,centers,shell in [
 ('esp_front',(28,21,8),[(0,-5,20)],head),
 ('amp_head_rear',(22,22,6),[(x,y,24) for x in (0,10,14) for y in (16,17,18)],head),
 ('mic_head_rear',(16,16,6),[(x,y,24) for x in (-20,-16,-14,14,16,20) for y in (16,17,18)],head),
]:
    print(label,[(c,v(box(sz,c),shell)) for c in centers],flush=True)
