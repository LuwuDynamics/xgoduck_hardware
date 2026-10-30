"""Remove the five LED mouth passages from the candidate head and assembly."""
from pathlib import Path
import json
import FreeCAD as App, Part, Mesh
V=App.Vector; H=Path(__file__).resolve().parent
src=App.openDocument(str(H.parent/'heart_v4'/'Cece_Heart_V4_Assembly.FCStd'))
doc=App.newDocument('Cece_No_LED_Mouth')
old=src.getObject('Rounded_Head_Study').Shape
# Reconstruct the exact original unperforated rounded shell region and fill
# only the five specified LED cylinders, preserving all other openings.
def rounded(x,y,z,dx,dy,dz,r):
 s=Part.makeBox(dx,dy,dz,V(x,y,z))
 edges=[e for e in s.Edges if abs(e.Length-dy)<1e-7 and abs(e.Vertexes[0].Point.y-e.Vertexes[-1].Point.y)>dy-1e-7]
 return s.makeFillet(r,edges)
outer=rounded(-42,-40,0,84,77.4,55,10)
inner=rounded(-40.4,-38.4,-5,80.8,76.8,58.4,8.4)
wall=outer.cut(inner)
head=old
for x,z in [(-8,5.8),(-4,4.8),(0,4.4),(4,4.8),(8,5.8)]:
 fill=wall.common(Part.makeCylinder(1.6,5,V(x,-41,z),V(0,1,0)))
 head=head.fuse(fill)
head=head.removeSplitter()
conflicts=[]
for obj in src.Objects:
 if not hasattr(obj,'Shape') or obj.Shape.isNull(): continue
 if 'mouth' in obj.Name.lower() or (obj.Name.startswith('LED_') and obj.Name.endswith('_Body_Proxy')): continue
 shape=head if obj.Name=='Rounded_Head_Study' else obj.Shape
 new=doc.addObject('PartDesign::Feature',obj.Name);new.Label=obj.Label;new.Shape=shape
 # Compare only added material to other parts to identify newly introduced conflicts.
 if obj.Name!='Rounded_Head_Study' and head.BoundBox.intersect(shape.BoundBox):
  added=head.cut(old)
  if added.BoundBox.intersect(shape.BoundBox):
   try:
    v=added.common(shape).Volume
    if v>0.01: conflicts.append({'object':obj.Name,'volume_mm3':v})
   except Exception as e: conflicts.append({'object':obj.Name,'error':str(e)})
doc.recompute();doc.saveAs(str(H/'Cece_No_LED_Mouth_Assembly.FCStd'))
Mesh.export([doc.getObject('Rounded_Head_Study')],str(H/'Cece_Head_No_LED_Mouth_TEST_ONLY.stl'))
res={'head_valid':head.isValid(),'head_solids':len(head.Solids),'added_volume_mm3':head.Volume-old.Volume,'new_material_overlaps_above_0_01_mm3':conflicts,'scope':'Neutral CAD check of material added to fill five LED passages only; no physical validation.'}
(H/'check_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2),flush=True)
App.closeDocument(doc.Name);App.closeDocument(src.Name)

