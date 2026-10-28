"""Candidate UC2 rear cassette. Run with FreeCAD 1.1 bundled python.exe.

All dimensions millimetres, in Cece's assembled coordinate frame. The
charger is a rectangular *envelope*; its USB connector location is unknown.
"""
from pathlib import Path
import json

import FreeCAD as App
import Part
import Mesh
import MeshPart

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BODY = ROOT / "packaging_study" / "Cece_Body_4741_WindowV3_CANDIDATE.stl"
assert BODY.is_file(), BODY

V = App.Vector
doc = App.newDocument("Cece_UC2_charger_cassette_candidate")


def box(x0, y0, z0, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x0, y0, z0))


def ycyl(x, y, z, radius, depth):
    return Part.makeCylinder(radius, depth, V(x, y, z), V(0, 1, 0))


def xcyl(x, y, z, radius, depth):
    return Part.makeCylinder(radius, depth, V(x, y, z), V(1, 0, 0))


def add_shape(name, shape, color):
    item = doc.addObject("PartDesign::Feature", name)
    item.Shape = shape.removeSplitter()
    if item.ViewObject is not None:
        item.ViewObject.ShapeColor = color
    return item


body_mesh = doc.addObject("Mesh::Feature", "Existing_Cece_Body_Reference")
body_mesh.Mesh = Mesh.Mesh(str(BODY))
if body_mesh.ViewObject is not None:
    body_mesh.ViewObject.ShapeColor = (0.70, 0.78, 0.84)
    body_mesh.ViewObject.Transparency = 68

modified_body_path = HERE / "cece_body_with_charger_posts_CANDIDATE.stl"
if modified_body_path.is_file():
    modified_body_mesh = doc.addObject("Mesh::Feature", "Candidate_Body_With_Posts_Print")
    modified_body_mesh.Mesh = Mesh.Mesh(str(modified_body_path))
    if modified_body_mesh.ViewObject is not None:
        modified_body_mesh.ViewObject.ShapeColor = (0.70, 0.78, 0.84)
        body_mesh.ViewObject.Visibility = False

# The rear wall is ~2 mm thick at these x/z coordinates. Four posts spread the
# load of the longer front-to-back charger pod across two vertical rows.
bosses = []
for x in (-18.0, 18.0):
    for z in (-30.0, -18.0):
        boss = box(x - 4.0, 32.5, z - 3.0, 8.0, 7.0, 6.0)
        boss = boss.cut(ycyl(x, 34.65, z, 1.25, 4.95))
        bosses.append(boss)
# Reinforced rectangular duct around a candidate balance-lead opening. The
# through-slot in the *body* itself is cut by validate_meshes.py after fusion.
duct = box(-9.0, 32.5, -32.0, 18.0, 7.0, 16.0)
duct = duct.cut(box(-7.0, 32.4, -30.0, 14.0, 7.2, 12.0))
boss_shape = bosses[0]
for b in bosses[1:]:
    boss_shape = boss_shape.fuse(b)
boss_shape = boss_shape.fuse(duct)
boss_obj = add_shape("Body_rear_mounting_posts", boss_shape, (0.48, 0.70, 0.80))

# UC2 ports are on opposite short ends. The 39.6 mm axis therefore points
# rearward along Y: XH balance socket toward the body, USB-C toward rear.
# Module X=19.8, Y=39.6, Z=9.5. Cavity adds >=2 mm per side.
outer = box(-13.9, 39.5, -32.75, 27.8, 45.6, 17.5)
cavity = box(-11.9, 41.5, -30.75, 23.8, 43.8, 13.5)
tray = outer.cut(cavity)
tray = tray.cut(box(-7.0, 39.4, -30.0, 14.0, 2.3, 12.0))
for x in (-18.0, 18.0):
    x0 = -22.5 if x < 0 else 13.5
    for z in (-30.0, -18.0):
        tray = tray.fuse(box(x0, 39.5, z - 3.0, 9.0, 4.0, 6.0))
        tray = tray.cut(ycyl(x, 39.4, z, 1.65, 4.2))
    # Rear tabs support a removable USB-access bezel without reducing the
    # 2 mm axial connector space at the end of the charger envelope.
    tray = tray.fuse(box(x0, 82.1, -27.0, 9.0, 3.0, 6.0))
    tray = tray.cut(ycyl(x, 82.0, -24.0, 0.9, 3.2))
tray_obj = add_shape("Removable_tray", tray, (0.26, 0.62, 0.83))

# Rearward exposed USB-C end. The central 16 x 7.5 opening is intentionally
# generous, but its relation to the real socket is not verified.
lid = box(-13.9, 85.1, -32.75, 27.8, 2.0, 17.5)
lid = lid.cut(box(-8.0, 85.0, -27.75, 16.0, 2.2, 7.5))
for x in (-18.0, 18.0):
    x0 = -22.5 if x < 0 else 13.5
    lid = lid.fuse(box(x0, 85.1, -27.0, 9.0, 2.0, 6.0))
    lid = lid.cut(ycyl(x, 85.0, -24.0, 1.1, 2.2))
lid_obj = add_shape("Retaining_bezel", lid, (0.90, 0.61, 0.28))

charger = box(-9.9, 43.5, -28.75, 19.8, 39.6, 9.5)
charger_obj = add_shape("UC2_size_envelope_ONLY", charger, (0.86, 0.42, 0.20))
if charger_obj.ViewObject is not None:
    charger_obj.ViewObject.Transparency = 65

doc.recompute()
doc.saveAs(str(HERE / "Cece_UC2_charger_cassette_candidate.FCStd"))

for name, shape in (("body_mounting_posts", boss_shape), ("removable_tray", tray), ("retaining_bezel", lid)):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False)
    mesh.write(str(HERE / f"{name}.stl"))

report = {
    "module_published_envelope_mm": [39.6, 19.8, 9.5],
    "internal_clearance_each_side_mm": 2.0,
    "module_assumed_bounds_xyz_mm": [[-9.9, 43.5, -28.75], [9.9, 83.1, -19.25]],
    "cavity_bounds_xyz_mm": [[-11.9, 41.5, -30.75], [11.9, 85.1, -17.25]],
    "tray_outer_bounds_xyz_mm": [[-22.5, 39.5, -33.0], [22.5, 85.1, -15.0]],
    "lid_rear_y_mm": 87.1,
    "body_attachment": "four added body posts at x +/-18, z -30 and -18; four M3 x 10 screws through tray ears into 2.5 mm blind pilot holes",
    "lid_attachment": "two M2 x 5 screws through separate rear tabs into 1.8 mm pilot holes",
    "battery_balance_lead_slot_xyz_mm": [[-7.0, 31.5, -30.0], [7.0, 41.7, -18.0]],
    "lead_slot_status": "candidate 14 x 12 mm passage, not verified for the actual plug or cable bend",
    "usb_rear_window_mm": [16.0, 7.5],
    "port_orientation": "official UC2 image shows XH and USB-C on opposite short ends; XH faces body, USB-C faces rear",
    "unknown": "exact UC2 port offset, plug body sizes, strain relief, charge isolation, heat, retention strength, print tolerance, and balance",
}
(HERE / "design_dimensions.json").write_text(json.dumps(report, indent=2))
print(json.dumps({"body": str(BODY), "boss_volume_mm3": boss_shape.Volume,
                  "tray_volume_mm3": tray.Volume, "lid_volume_mm3": lid.Volume,
                  "charger_envelope_volume_mm3": charger.Volume}, indent=2))
