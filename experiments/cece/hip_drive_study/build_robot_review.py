"""Build full robot FreeCAD review using the revised experimental legs/feet."""
from pathlib import Path
import FreeCAD as App, Part, Mesh
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'rounded_head_study'/'Cece_Rounded_Head_Camera_Study.FCStd'
src=App.openDocument(str(SOURCE)); doc=App.newDocument('Cece_Whole_Robot_Leg_Study')
replacement={
 'Left_Leg':'Cece_left_leg_hip_slot_TEST_ONLY.stl',
 'Right_Leg':'Cece_right_leg_hip_slot_TEST_ONLY.stl',
 'Left_Foot':'Cece_left_wide_foot_clearance_TEST_ONLY.stl',
 'Right_Foot':'Cece_right_wide_foot_clearance_TEST_ONLY.stl'}
for original in src.Objects:
    if not hasattr(original,'Shape') or original.Shape.isNull():continue
    shape=original.Shape.copy()
    if original.Name in replacement:
        mesh=Mesh.Mesh(str(HERE/replacement[original.Name])); s=Part.Shape();s.makeShapeFromMesh(mesh.Topology,0.01)
        if len(s.Shells)!=1:raise RuntimeError('Invalid mesh '+original.Name)
        shape=Part.makeSolid(s.Shells[0])
        if not shape.isValid() or len(shape.Solids)!=1:raise RuntimeError('Invalid solid '+original.Name)
    obj=doc.addObject('PartDesign::Feature',original.Name);obj.Label=original.Label;obj.Shape=shape
doc.recompute();doc.saveAs(str(HERE/'Cece_Whole_Robot_Leg_Study.FCStd'))
print('Created whole-robot review with experimental leg and foot geometry',flush=True)
App.closeDocument(doc.Name);App.closeDocument(src.Name)
