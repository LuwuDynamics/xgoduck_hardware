"""FreeCAD inspection document for the preattached-plug speaker passage."""
from pathlib import Path
import FreeCAD as App
import Mesh
import Part

HERE = Path(__file__).resolve().parent
CECE = HERE.parents[2]
doc = App.newDocument("Cece_speaker_plug_passage_V2_candidate")


def add_mesh(name, path, visible=True):
    obj = doc.addObject("Mesh::Feature", name)
    obj.Mesh = Mesh.Mesh(str(path))
    if obj.ViewObject is not None:
        obj.ViewObject.Visibility = visible
    return obj


add_mesh("Prior_4mm_head_reference", CECE / "packaging_study/servo_plug_check/Cece_head_vertical_driver_hood_CANDIDATE.stl", False)
add_mesh("New_12mm_passage_head", HERE / "Cece_head_hood_speaker_plug_passage_V2_CANDIDATE.stl")
add_mesh("New_12mm_passage_pod", HERE / "speaker_pod_tray_plug_passage_V2_CANDIDATE.stl")
add_mesh("Existing_speaker_grille", HERE.parent / "speaker_retaining_grille.stl")
probe = doc.addObject("PartDesign::Feature", "Trial_8x7mm_plug_clearance")
probe.Shape = Part.makeBox(8, 16, 7, App.Vector(-4, 24, 13.5))
if probe.ViewObject is not None:
    probe.ViewObject.Visibility = False
doc.recompute()
doc.saveAs(str(HERE / "Cece_speaker_plug_passage_V2_CANDIDATE.FCStd"))
print("Saved FreeCAD candidate")
