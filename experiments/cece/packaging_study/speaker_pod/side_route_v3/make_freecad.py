"""FreeCAD inspection scene for right-side speaker route + M2 faceplate trial."""
from pathlib import Path
import FreeCAD as App, Mesh, Part

HERE=Path(__file__).resolve().parent
CECE=HERE.parents[2]
doc=App.newDocument('Cece_Side_Speaker_Faceplate_V3_CANDIDATE')

def add_mesh(name,path,visible=True):
    o=doc.addObject('Mesh::Feature',name);o.Mesh=Mesh.Mesh(str(path))
    if o.ViewObject is not None:o.ViewObject.Visibility=visible
    return o

add_mesh('Source_V2_PiicoDev_Hood_Reference',CECE/'packaging_study/servo_plug_check/Cece_head_vertical_driver_hood_V2_CANDIDATE.stl',False)
add_mesh('V3_Combined_Head',HERE/'Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl')
add_mesh('V3_Faceplate',HERE/'Cece_faceplate_M2_retained_V3_CANDIDATE.stl')
add_mesh('V3_Speaker_Pod_With_Wire_Lug',HERE/'speaker_pod_side_wire_notch_V3_CANDIDATE.stl')
add_mesh('Original_Speaker_Grille',HERE.parent/'speaker_retaining_grille.stl')
speaker=doc.addObject('PartDesign::Feature','Trial_Speaker_28x7mm')
speaker.Shape=Part.makeCylinder(14,7,App.Vector(0,41.2,17),App.Vector(0,1,0))
plug=doc.addObject('PartDesign::Feature','Trial_Speaker_Plug_8x7x16mm')
plug.Shape=Part.makeBox(8,16,7,App.Vector(24,24,22.5))
if speaker.ViewObject is not None:speaker.ViewObject.Visibility=False
if plug.ViewObject is not None:plug.ViewObject.Visibility=False
doc.recompute();doc.saveAs(str(HERE/'Cece_Side_Speaker_Faceplate_V3_CANDIDATE.FCStd'))
print('Saved FreeCAD V3 candidate')
