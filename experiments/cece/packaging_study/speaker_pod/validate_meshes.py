"""Full mesh Boolean checks for the rear speaker pod candidate."""
import json
import sys
import warnings
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[4]
CECE = HERE.parents[1]
sys.path.insert(0, str(WORKSPACE / "cece_mesh_deps"))
import trimesh

warnings.filterwarnings("ignore", category=RuntimeWarning)


def mesh(path):
    return trimesh.load(path, force="mesh")


def overlap(a, b):
    return round(abs(trimesh.boolean.intersection([a, b], engine="manifold").volume), 5)


head = mesh(CECE / "parts_adafruit_draft" / "Cece_Head_Centered_Antenna_DRAFT.stl")
mount = mesh(HERE / "head_mounting_posts_and_wire_sleeve.stl")
pod = mesh(HERE / "speaker_pod_tray.stl")
grille = mesh(HERE / "speaker_retaining_grille.stl")
speaker = trimesh.creation.cylinder(radius=14.0, height=7.0, sections=96)
speaker.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
speaker.apply_translation([0, 44.7, 17.0])

wire_cut = trimesh.creation.cylinder(radius=2.0, height=7.5, sections=96)
wire_cut.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
wire_cut.apply_translation([0, 33.5, 17.0])  # spans Y=29.75..37.25
combined = trimesh.boolean.union([head, mount], engine="manifold")
modified = trimesh.boolean.difference([combined, wire_cut], engine="manifold")
modified.export(HERE / "cece_head_with_speaker_mount_CANDIDATE.stl")


def ycylinder(radius, y0, y1, x, z=17.0):
    probe = trimesh.creation.cylinder(radius=radius, height=y1-y0, sections=64)
    probe.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    probe.apply_translation([x, (y0+y1)/2, z])
    return probe


mount_screw_probes = [ycylinder(1.0, 32.3, 50.2, x) for x in (-23.0, 23.0)]
grille_screw_probes = [ycylinder(0.7, 47.1, 52.2, x) for x in (-28.0, 28.0)]
wire_probe = ycylinder(1.5, 29.8, 41.1, 0.0)

name = mesh(CECE / "parts_adafruit_draft" / "Cece_Name_Back_Visual_Overlay.stl")
body = mesh(CECE / "packaging_study/charger_cassette" / "cece_body_with_charger_posts_CANDIDATE.stl")
faceplate = mesh(CECE / "parts_adafruit_draft" / "Cece_Happy_Faceplate_DRAFT.stl")
antenna = mesh(CECE / "parts_adafruit_draft" / "Cece_Antenna_DRAFT.stl")
antenna.apply_translation([0, 0, 27.0])  # approximate assembly position from Cece visual scene
charger_tray = mesh(CECE / "packaging_study/charger_cassette" / "removable_tray.stl")
charger_bezel = mesh(CECE / "packaging_study/charger_cassette" / "retaining_bezel.stl")
feet = [mesh(CECE / "parts_adafruit_draft" / f"cece_foot_{side}_clean.stl") for side in ("left", "right")]

checks = {
    "modified_head_watertight": modified.is_watertight,
    "modified_head_components": len(modified.split(only_watertight=False)),
    "mount_vs_original_head_intended_overlap_mm3": overlap(mount, head),
    "wire_cut_vs_original_head_removed_mm3": overlap(wire_cut, head),
    "pod_vs_modified_head_mm3": overlap(pod, modified),
    "pod_vs_v3_body_with_charger_posts_mm3": overlap(pod, body),
    "pod_vs_rear_cece_name_mm3": overlap(pod, name),
    "pod_vs_faceplate_mm3": overlap(pod, faceplate),
    "pod_vs_antenna_approx_position_mm3": overlap(pod, antenna),
    "pod_vs_charger_tray_mm3": overlap(pod, charger_tray),
    "pod_vs_charger_bezel_mm3": overlap(pod, charger_bezel),
    "pod_vs_feet_mm3": [overlap(pod, m) for m in feet],
    "grille_vs_pod_mm3": overlap(grille, pod),
    "speaker_vs_pod_mm3": overlap(speaker, pod),
    "speaker_vs_grille_mm3": overlap(speaker, grille),
    "mount_screw_core_probe_vs_modified_head_and_pod_mm3": [
        overlap(q, modified) + overlap(q, pod) for q in mount_screw_probes],
    "grille_screw_core_probe_vs_pod_and_grille_mm3": [
        overlap(q, pod) + overlap(q, grille) for q in grille_screw_probes],
    "speaker_wire_probe_vs_head_and_pod_mm3": overlap(wire_probe, modified) + overlap(wire_probe, pod),
    "parts": {},
}
for name, item in (("modified_head", modified), ("pod", pod), ("grille", grille)):
    checks["parts"][name] = {
        "watertight": item.is_watertight,
        "components": len(item.split(only_watertight=False)),
        "solid_volume_mm3": round(abs(item.volume), 3),
        "bounds_xyz_mm": np.round(item.bounds, 3).tolist(),
    }

(HERE / "mesh_validation.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
