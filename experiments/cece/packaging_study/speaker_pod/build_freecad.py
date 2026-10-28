"""Rear 28 mm speaker pod candidate in Cece assembled coordinates.

Run with FreeCAD 1.1 bundled python.exe. Speaker terminals and wires are
unknown. The 28 x 7 mm cylinder is a clearance envelope, not purchased CAD.
"""
from pathlib import Path
import json

import FreeCAD as App
import Part
import Mesh
import MeshPart

HERE = Path(__file__).resolve().parent
CECE = HERE.parents[1]
HEAD = CECE / "parts_adafruit_draft" / "Cece_Head_Centered_Antenna_DRAFT.stl"
V = App.Vector
doc = App.newDocument("Cece_rear_speaker_pod_candidate")


def box(x, y, z, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x, y, z))


def cyl(r, y, h, x=0.0, z=17.0):
    return Part.makeCylinder(r, h, V(x, y, z), V(0, 1, 0))


def feature(name, shape):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape.removeSplitter()
    assert obj.Shape.isValid(), name
    return obj


head_ref = doc.addObject("Mesh::Feature", "Existing_Cece_Head_Reference")
head_ref.Mesh = Mesh.Mesh(str(HEAD))
head_candidate_path = HERE / "cece_head_with_speaker_mount_CANDIDATE.stl"
if head_candidate_path.exists():
    candidate = doc.addObject("Mesh::Feature", "Candidate_Head_With_Mount_Print")
    candidate.Mesh = Mesh.Mesh(str(head_candidate_path))
    if head_ref.ViewObject is not None:
        head_ref.ViewObject.Visibility = False

# Two external M3 fixing posts are integrated into a replacement head. A
# central wire sleeve bridges the 5 mm gap to the pod; only bare wires fit.
posts = []
for x in (-23.0, 23.0):
    post = box(x - 5, 30.2, 11.0, 10.0, 7.0, 12.0)
    post = post.cut(cyl(1.25, 32.3, 5.0, x=x))
    posts.append(post)
sleeve = cyl(3.0, 30.2, 7.0).cut(cyl(2.0, 30.1, 7.2))
head_mount = posts[0].fuse(posts[1]).fuse(sleeve)
feature("Head_mounting_posts_and_wire_sleeve", head_mount)

# Front of pod y37.2, open rear y50.2. Outer Ø34.5, cavity Ø30.5.
pod = cyl(17.25, 37.2, 13.0).cut(cyl(15.25, 39.2, 11.2))
# Ring supports outer edge of Ø28 x 7 mm speaker at y41.2.
front_ledge = cyl(15.25, 39.2, 2.0).cut(cyl(12.8, 39.1, 2.2))
pod = pod.fuse(front_ledge)
for x0 in (-31.0, 16.0):
    pod = pod.fuse(box(x0, 37.2, 13.0, 15.0, 13.0, 8.0))
pod = pod.cut(cyl(2.0, 37.1, 2.3))  # wire passage aligned with head sleeve
for x in (-23.0, 23.0):
    pod = pod.cut(cyl(1.65, 37.1, 13.2, x=x))  # M3 through hole
    pod = pod.cut(cyl(3.0, 42.7, 7.6, x=x))    # rear screwdriver / head access
for x in (-28.0, 28.0):
    pod = pod.cut(cyl(0.9, 47.1, 3.2, x=x))   # separate M2 grille pilot
feature("Speaker_pod_tray", pod)

# Rear grille retains the speaker by its rim; holes permit rearward sound.
grille = cyl(17.25, 50.2, 2.0)
rim = cyl(14.9, 48.2, 2.0).cut(cyl(12.8, 48.1, 2.2))
grille = grille.fuse(rim)
for x0 in (-31.0, 16.0):
    grille = grille.fuse(box(x0, 50.2, 13.0, 15.0, 2.0, 8.0))
holes = []
for x in (-10.0, -5.0, 0.0, 5.0, 10.0):
    for dz in (-10.0, -5.0, 0.0, 5.0, 10.0):
        if x * x + dz * dz <= 125:
            holes.append(cyl(1.55, 50.1, 2.2, x=x, z=17 + dz))
for hole in holes:
    grille = grille.cut(hole)
for x in (-28.0, 28.0):
    grille = grille.cut(cyl(1.1, 50.1, 2.2, x=x))
feature("Speaker_retaining_grille", grille)

speaker = cyl(14.0, 41.2, 7.0)
feature("Speaker_28x7mm_envelope_ONLY", speaker)
doc.recompute()
doc.saveAs(str(HERE / "Cece_rear_speaker_pod_candidate.FCStd"))

for name, shape in (("head_mounting_posts_and_wire_sleeve", head_mount),
                    ("speaker_pod_tray", pod), ("speaker_retaining_grille", grille)):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05,
                                  AngularDeflection=0.2, Relative=False)
    mesh.write(str(HERE / f"{name}.stl"))

(HERE / "design_dimensions.json").write_text(json.dumps({
    "head_source": str(HEAD),
    "speaker_envelope_mm": {"diameter": 28.0, "thickness": 7.0,
                             "axis": "Y", "center_xyz": [0, 44.7, 17]},
    "pod_outer_mm": {"diameter": 34.5, "front_y": 37.2,
                      "rear_y": 50.2, "center_xz": [0, 17]},
    "grille_rear_y_mm": 52.2,
    "module_radial_clearance_mm": 1.25,
    "speaker_seat_axial_gap_mm": 7.0,
    "speaker_seat_note": "front/rear printed rim touch a nominal 7mm speaker; thinner speakers need a compressible shim, thicker ones require geometry revision",
    "head_mount": "two rear posts at x +/-23,z17; two M3x10 screws from recessed rear access holes into blind 2.5mm pilot holes",
    "grille_mount": "two M2x5 screws at x +/-28,z17 into separate 1.8mm pilot holes in pod side rails",
    "wire_hole": "4mm diameter at x0,z17, through modified head and pod front",
    "unknown": "speaker terminals, wire plug, acoustic response, screw fit, heat, print tolerance",
}, indent=2))
print("FreeCAD speaker pod solids valid; files exported")
