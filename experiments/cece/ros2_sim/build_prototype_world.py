"""Build a provisional Gazebo world using Cece's current CAD visuals.

Axes and joint positions follow the existing Bullet experiment. Masses and
simple collision shapes are estimates; never treat this as a verified robot.
Run this on Linux/WSL so mesh file URLs refer to Linux paths.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
CECE = HERE.parent
MESHES = CECE / "bullet_gait" / "cad_visuals"
RESULTS = CECE / "bullet_gait" / "bullet_current_cece_results.json"
OUT = HERE / "generated" / "starter_cece.sdf"

def element(parent, tag, text=None, **attrs):
    child = ET.SubElement(parent, tag, attrs)
    if text is not None:
        child.text = str(text)
    return child

def link(model, name, xyz, mass, shape_size, shape_pos):
    item = element(model, "link", name=name)
    element(item, "pose", f"{xyz[0]} {xyz[1]} {xyz[2]} 0 0 0")
    inertial = element(item, "inertial")
    element(inertial, "mass", mass)
    inertia = element(inertial, "inertia")
    # Uniform-box approximation, not the mass tensor from CAD.
    sx, sy, sz = shape_size
    for tag, value in (("ixx", mass * (sy*sy + sz*sz)/12),
                       ("iyy", mass * (sx*sx + sz*sz)/12),
                       ("izz", mass * (sx*sx + sy*sy)/12),
                       ("ixy", 0), ("ixz", 0), ("iyz", 0)):
        element(inertia, tag, value)
    collision = element(item, "collision", name=name + "_collision")
    element(collision, "pose", " ".join(map(str, shape_pos)) + " 0 0 0")
    geometry = element(collision, "geometry")
    element(element(geometry, "box"), "size", " ".join(map(str, shape_size)))
    return item

def visual(link_item, name, path, origin, color):
    if not path.is_file():
        raise FileNotFoundError(path)
    item = element(link_item, "visual", name=name)
    element(item, "pose", " ".join(str(-x) for x in origin) + " 0 0 0")
    mesh = element(element(item, "geometry"), "mesh")
    element(mesh, "uri", path.resolve().as_uri())
    element(mesh, "scale", "0.001 0.001 0.001")
    mat = element(item, "material")
    element(mat, "ambient", color)
    element(mat, "diffuse", color)

def joint(model, name, parent, child, axis):
    item = element(model, "joint", name=name, type="revolute")
    element(item, "parent", parent)
    element(item, "child", child)
    ax = element(item, "axis")
    element(ax, "xyz", axis)
    limit = element(ax, "limit")
    for name, value in (("lower", -0.52), ("upper", 0.52), ("effort", 0.08), ("velocity", 2.5)):
        element(limit, name, value)
    element(element(ax, "dynamics"), "damping", 0.001)

def main():
    tree = ET.parse(HERE / "worlds" / "starter_room.sdf")
    world = tree.getroot().find("world")
    model = element(world, "model", name="cece_prototype")
    element(model, "pose", "0 0 0.08902 0 0 0")
    masses = json.loads(RESULTS.read_text())["model"]["body_masses_g"]
    base = link(model, "base", (0, 0, 0), masses["base"]/1000,
                (.082, .079, .095), (0, 0, 0.008))
    colors = {"Body": "0.86 0.91 0.95 1", "Rounded_Head_Study": "0.9 0.94 0.98 1",
              "Heart_Frame_V3": "0.9 0.3 0.45 1", "Antenna": "1 0.72 0.26 1",
              "Left_Arm": "0.55 0.72 0.86 1", "Right_Arm": "0.55 0.72 0.86 1",
              "OLED_Adafruit4741_Official_CAD": "0.06 0.13 0.23 1",
              "HC_SR04_Left_Can": "0.3 0.78 0.84 1", "HC_SR04_Right_Can": "0.3 0.78 0.84 1"}
    for name, color in colors.items():
        path = MESHES / (name + ".stl")
        if name == "Heart_Frame_V3":
            path = CECE / "heart_v4" / "Cece_Heart_Frame_V4_TEST_ONLY.stl"
        if name == "Rounded_Head_Study":
            path = CECE / "no_led_mouth" / "Cece_Head_No_LED_Mouth_TEST_ONLY.stl"
        visual(base, name, path, (0, 0, 0), color)
    for side, x in (("left", -0.0255), ("right", 0.0255)):
        leg_origin = (x, 0, -0.04)
        foot_origin = (x, 0, -0.0715)
        leg = link(model, side + "_leg", leg_origin, masses[side + "_leg"]/1000,
                   (.017, .04, .042), (0, -.0035, -.021))
        foot = link(model, side + "_foot", foot_origin, masses[side + "_foot"]/1000,
                    (.05, .07, .005), (0, 0, -.015))
        visual(leg, side + "_leg_visual", MESHES / (side.title() + "_Leg.stl"),
               leg_origin, "0.56 0.7 0.84 1")
        visual(foot, side + "_foot_visual", MESHES / (side.title() + "_Foot.stl"),
               foot_origin, "0.3 0.49 0.72 1")
        joint(model, side + "_hip", "base", side + "_leg", "0 0 1")
        joint(model, side + "_ankle", side + "_leg", side + "_foot", "0 1 0")
    OUT.parent.mkdir(exist_ok=True)
    ET.indent(tree, space="  ")
    tree.write(OUT, encoding="utf-8", xml_declaration=True)
    print(OUT)

if __name__ == "__main__":
    main()
