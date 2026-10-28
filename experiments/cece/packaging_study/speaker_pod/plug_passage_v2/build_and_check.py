"""Candidate installed-speaker-plug passage for Cece's hooded speaker head.

Run with workspace Python. Uses manifold3d through trimesh for closed mesh
Booleans. The real COM-21311 connector has not been measured.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CECE = HERE.parents[2]
WORKSPACE = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE / "cece_mesh_deps"))
import trimesh

SOURCE_HEAD = CECE / "packaging_study/servo_plug_check/Cece_head_vertical_driver_hood_CANDIDATE.stl"
SOURCE_POD = HERE.parent / "speaker_pod_tray.stl"
SOURCE_GRILLE = HERE.parent / "speaker_retaining_grille.stl"


def mesh(path: Path) -> trimesh.Trimesh:
    return trimesh.load(path, force="mesh")


def ycylinder(radius: float, y0: float, y1: float, x=0.0, z=17.0) -> trimesh.Trimesh:
    m = trimesh.creation.cylinder(radius=radius, height=y1-y0, sections=128)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    m.apply_translation([x, (y0+y1)/2, z])
    return m


def box(extents, center) -> trimesh.Trimesh:
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    return m


def union(*parts):
    return trimesh.boolean.union(parts, engine="manifold")


def difference(part, *cuts):
    return trimesh.boolean.difference([part, *cuts], engine="manifold")


def overlap(a, b) -> float:
    c = trimesh.boolean.intersection([a, b], engine="manifold")
    return round(abs(float(c.volume)), 5)


head = mesh(SOURCE_HEAD)
pod = mesh(SOURCE_POD)
grille = mesh(SOURCE_GRILLE)

# A 12 mm bore is bigger than the 5.8 x 6.85 mm JST PHR-2 reference envelope.
# The extra radial key relief deliberately makes orientation visible; it is not
# an actual mating connector key. The supplied COM-21311 plug series is unknown.
outer_sleeve = ycylinder(9.0, 30.0, 37.2)
round_bore = ycylinder(6.0, 27.0, 39.3)
key_relief = box((1.5, 12.3, 3.0), (6.4, 33.15, 17.0))
plug_passage = union(round_bore, key_relief)

new_head = difference(union(head, outer_sleeve), plug_passage)
new_pod = difference(pod, plug_passage)

head_path = HERE / "Cece_head_hood_speaker_plug_passage_V2_CANDIDATE.stl"
pod_path = HERE / "speaker_pod_tray_plug_passage_V2_CANDIDATE.stl"
new_head.export(head_path)
new_pod.export(pod_path)

# Reimport the actual exported STLs. STL coordinate quantization sometimes
# breaks a manifold that was sound in memory.
new_head = mesh(head_path)
new_pod = mesh(pod_path)
assert new_head.is_watertight and len(new_head.split(only_watertight=False)) == 1
assert new_pod.is_watertight and len(new_pod.split(only_watertight=False)) == 1

body = mesh(CECE / "packaging_study/Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl")
faceplate = mesh(CECE / "parts_adafruit_draft/Cece_Happy_Faceplate_DRAFT.stl")
frame = mesh(CECE / "packaging_study/Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl")
charger_tray = mesh(CECE / "packaging_study/charger_cassette/removable_tray.stl")
speaker = ycylinder(14.0, 41.2, 48.2)

# A short 8 x 7 mm surrogate for a pre-attached 2-pin plug is passed straight
# through the shell. This is a geometric trial, not identification of the plug.
plug_probe = box((8.0, 16.0, 7.0), (0.0, 32.0, 17.0))
wire_probe = ycylinder(1.5, 27.0, 41.3)
checks = {
    "status": "candidate only; purchased speaker plug unmeasured",
    "source_head": str(SOURCE_HEAD),
    "bore_diameter_mm": 12.0,
    "outer_sleeve_diameter_mm": 18.0,
    "key_relief_bounds_xyz_mm": [[5.65, 27.0, 15.5], [7.15, 39.3, 18.5]],
    "exported_parts": {},
    "intended_sleeve_vs_source_head_overlap_mm3": overlap(outer_sleeve, head),
    "plug_probe_8x7x16_vs_head_pod_mm3": overlap(plug_probe, new_head) + overlap(plug_probe, new_pod),
    "bare_wire_probe_vs_head_pod_mm3": overlap(wire_probe, new_head) + overlap(wire_probe, new_pod),
    "solid_overlaps_mm3": {
        "head_vs_body_v4": overlap(new_head, body),
        "head_vs_faceplate": overlap(new_head, faceplate),
        "head_vs_heart_frame": overlap(new_head, frame),
        "pod_vs_head": overlap(new_pod, new_head),
        "pod_vs_body_v4": overlap(new_pod, body),
        "pod_vs_charger_tray": overlap(new_pod, charger_tray),
        "pod_vs_grille": overlap(new_pod, grille),
        "speaker_envelope_vs_pod": overlap(speaker, new_pod),
        "speaker_envelope_vs_grille": overlap(speaker, grille),
    },
    "limits": [
        "SparkFun/Core call the attached connector only two-wire JST; series and size are unspecified.",
        "The 8 x 7 mm plug probe is a trial envelope, not a measurement of the delivered part.",
        "Head-to-body, speaker seating, terminal relief, strain relief and actual cable bend still require physical checks.",
    ],
}
for name, part in (("head", new_head), ("pod", new_pod)):
    checks["exported_parts"][name] = {
        "watertight": bool(part.is_watertight),
        "components": len(part.split(only_watertight=False)),
        "bounds_xyz_mm": np.round(part.bounds, 3).tolist(),
        "solid_volume_mm3": round(abs(float(part.volume)), 3),
    }
assert checks["plug_probe_8x7x16_vs_head_pod_mm3"] == 0.0
assert checks["bare_wire_probe_vs_head_pod_mm3"] == 0.0
assert all(v == 0.0 for v in checks["solid_overlaps_mm3"].values())
(HERE / "mesh_validation.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
