"""Exact mesh Boolean checks for the candidate UC2 rear cassette."""
import json
import sys
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[4]
sys.path.insert(0, str(WORKSPACE / "cece_mesh_deps"))
import trimesh

warnings.filterwarnings("ignore", category=RuntimeWarning)
CECE = HERE.parents[1]
SOURCE = CECE / "parts_adafruit_draft"
PARTS = CECE / "parts"


def mesh(path):
    return trimesh.load(path, force="mesh")


def overlap(a, b):
    return round(abs(trimesh.boolean.intersection([a, b], engine="manifold").volume), 5)


body = mesh(CECE / "packaging_study" / "Cece_Body_4741_WindowV3_CANDIDATE.stl")
posts = mesh(HERE / "body_mounting_posts.stl")
tray = mesh(HERE / "removable_tray.stl")
lid = mesh(HERE / "retaining_bezel.stl")
charger = trimesh.creation.box(extents=[19.8, 39.6, 9.5])
charger.apply_translation([0, 63.3, -24.0])
slot = trimesh.creation.box(extents=[14.0, 10.2, 12.0])
slot.apply_translation([0.0, 36.6, -24.0])
modified = trimesh.boolean.union([body, posts], engine="manifold")
modified = trimesh.boolean.difference([modified, slot], engine="manifold")
modified.export(HERE / "cece_body_with_charger_posts_CANDIDATE.stl")
passage_probe = trimesh.creation.box(extents=[13.0, 11.9, 11.0])
passage_probe.apply_translation([0.0, 37.45, -24.0])
usb_probe = trimesh.creation.box(extents=[14.0, 4.6, 6.0])
usb_probe.apply_translation([0.0, 85.0, -24.0])


def ycylinder(radius, y0, y1, x, z):
    probe = trimesh.creation.cylinder(radius=radius, height=y1-y0, sections=64)
    probe.apply_transform(trimesh.transformations.rotation_matrix(3.141592653589793/2, [1, 0, 0]))
    probe.apply_translation([x, (y0+y1)/2, z])
    return probe


mount_screw_probes = [ycylinder(1.0, 34.65, 43.5, x, z)
                      for x in (-18.0, 18.0) for z in (-30.0, -18.0)]
mount_tool_probes = [ycylinder(2.5, 43.5, 82.0, x, z)
                     for x in (-18.0, 18.0) for z in (-30.0, -18.0)]
lid_screw_probes = [ycylinder(0.7, 82.1, 87.1, x, -24.0)
                    for x in (-18.0, 18.0)]

name = mesh(SOURCE / "Cece_Name_Back_Visual_Overlay.stl")
head = mesh(SOURCE / "Cece_Head_Centered_Antenna_DRAFT.stl")
speaker_pod = mesh(CECE / "packaging_study/speaker_pod" / "speaker_pod_tray.stl")
speaker_grille = mesh(CECE / "packaging_study/speaker_pod" / "speaker_retaining_grille.stl")
feet = [mesh(SOURCE / f"cece_foot_{side}_clean.stl") for side in ("left", "right")]
legs = [mesh(PARTS / f) for f in ("leg_mirror.stl", "OttoDIY_Leg_V9.stl")]

checks = {
    "body_posts_intended_overlap_mm3": overlap(body, posts),
    "balance_lead_slot_removed_from_v3_body_mm3": overlap(body, slot),
    "balance_lead_passage_probe_vs_modified_body_mm3": overlap(passage_probe, modified),
    "balance_lead_passage_probe_vs_tray_mm3": overlap(passage_probe, tray),
    "usb_rear_probe_vs_tray_mm3": overlap(usb_probe, tray),
    "usb_rear_probe_vs_lid_mm3": overlap(usb_probe, lid),
    "mount_screw_core_probe_vs_body_and_tray_mm3": [overlap(q, modified)+overlap(q, tray)
                                                       for q in mount_screw_probes],
    "rear_tool_access_probe_vs_tray_mm3": [overlap(q, tray) for q in mount_tool_probes],
    "lid_screw_core_probe_vs_tray_and_lid_mm3": [overlap(q, tray)+overlap(q, lid)
                                                 for q in lid_screw_probes],
    "lead_passage_probe_envelope_mm": [13.0, 11.9, 11.0],
    "duct_wall_thickness_nominal_mm": 2.0,
    "modified_body_watertight": modified.is_watertight,
    "modified_body_components": len(modified.split(only_watertight=False)),
    "posts_vs_tray_mm3": overlap(posts, tray),
    "tray_vs_v3_body_mm3": overlap(body, tray),
    "tray_vs_head_mm3": overlap(head, tray),
    "tray_vs_speaker_pod_mm3": overlap(speaker_pod, tray),
    "tray_vs_speaker_grille_mm3": overlap(speaker_grille, tray),
    "tray_vs_name_mm3": overlap(name, tray),
    "lid_vs_name_mm3": overlap(name, lid),
    "posts_vs_name_mm3": overlap(name, posts),
    "posts_vs_head_mm3": overlap(head, posts),
    "tray_vs_feet_mm3": [overlap(m, tray) for m in feet],
    "tray_vs_neutral_legs_mm3": [overlap(m, tray) for m in legs],
    "charger_vs_tray_mm3": overlap(charger, tray),
    "charger_vs_lid_mm3": overlap(charger, lid),
    "lid_vs_tray_mm3": overlap(lid, tray),
    "print_parts": {
        "body_with_posts": {"watertight": modified.is_watertight, "components": len(modified.split()), "volume_mm3": round(abs(modified.volume), 3)},
        "tray": {"watertight": tray.is_watertight, "components": len(tray.split()), "volume_mm3": round(abs(tray.volume), 3)},
        "lid": {"watertight": lid.is_watertight, "components": len(lid.split()), "volume_mm3": round(abs(lid.volume), 3)},
    },
    "moving_hip_test": {},
}

# Conservative coarse swing about an estimated hip axis. The actual hip axis
# must be checked before interpreting zero intersection as a motion pass.
for side, leg, x in (("left", legs[0], -25.5), ("right", legs[1], 25.5)):
    samples = {}
    for angle in range(-45, 46, 5):
        moving = leg.copy()
        moving.apply_transform(trimesh.transformations.rotation_matrix(
            angle * 3.141592653589793 / 180, [1, 0, 0], [x, 0, -48]))
        samples[str(angle)] = overlap(moving, tray)
    checks["moving_hip_test"][side] = {
        "estimated_pivot_xyz_mm": [x, 0, -48],
        "sampled_angles_deg": list(range(-45, 46, 5)),
        "tray_intersection_mm3": samples,
    }

(HERE / "mesh_validation.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
