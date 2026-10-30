from pathlib import Path
import json
import FreeCAD as App, Part, Mesh
H=Path(__file__).resolve().parent
source=H.parent/'hip_drive_study'/'Cece_Full_Electronics_Study.FCStd'
src=App.openDocument(str(source)); doc=App.newDocument('Cece_Heart_V4_Assembly')
m=Mesh.Mesh(str(H/'Cece_Heart_Frame_V4_TEST_ONLY.stl'))
s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01); s=Part.makeSolid(s.Shells[0]); s=s.removeSplitter()
print('HEART',s.isValid(),len(s.Solids),s.Volume,flush=True)
conflicts=[]
for obj in src.Objects:
 if not hasattr(obj,'Shape') or obj.Shape.isNull(): continue
 shape=s if obj.Name=='Heart_Frame_V3' else obj.Shape
 new=doc.addObject('PartDesign::Feature',obj.Name);new.Label='Heart Frame V4 candidate' if obj.Name=='Heart_Frame_V3' else obj.Label;new.Shape=shape
 if obj.Name!='Heart_Frame_V3' and s.BoundBox.intersect(shape.BoundBox):
  try:
   v=s.common(shape).Volume
   if v>0.01: conflicts.append({'object':obj.Name,'volume_mm3':v})
  except Exception as e: conflicts.append({'object':obj.Name,'error':str(e)})
print('CONFLICTS',conflicts,flush=True)
doc.recompute();doc.saveAs(str(H/'Cece_Heart_V4_Assembly.FCStd'))
(H/'heart_assembly_fit_results.json').write_text(json.dumps({'source':str(source.name),'heart_valid':s.isValid(),'heart_solids':len(s.Solids),'heart_volume_mm3':s.Volume,'heart_center_mm':[s.CenterOfMass.x,s.CenterOfMass.y,s.CenterOfMass.z],'neutral_pose_overlaps_above_0_01_mm3':conflicts,'limitation':'CAD geometry only; connectors, assembly hardware and motion not verified.'},indent=2))
App.closeDocument(doc.Name);App.closeDocument(src.Name)
