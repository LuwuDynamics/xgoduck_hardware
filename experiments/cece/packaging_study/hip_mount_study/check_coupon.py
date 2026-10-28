"""Reproducible static clearance audit for the exact V4 right-hip coupon.

Only a real fit of the purchased SG90, screws and supplied horn can settle their
unpublished mounting and spline dimensions.
"""
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / "cece_mesh_deps"))
import trimesh

CECE = HERE.parents[1]
PACK = HERE.parent

def load(path):
    return trimesh.load(path, force="mesh")

def box(size, center):
    part = trimesh.creation.box(extents=size)
    part.apply_translation(center)
    return part

def cylinder(radius, height, center):
    part = trimesh.creation.cylinder(radius=radius, height=height, sections=64)
    part.apply_translation(center)
    return part

def overlap(a, b):
    aa, bb = a.bounds, b.bounds
    if any(aa[1, i] <= bb[0, i] or bb[1, i] <= aa[0, i] for i in range(3)):
        return 0.0
    return round(abs(trimesh.boolean.intersection([a, b], engine="manifold").volume), 3)

body = load(PACK / "Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl")
coupon = load(HERE / "Cece_Right_Hip_Fit_Coupon.stl")
leg = load(CECE / "ankle_v2" / "Cece_right_leg_SG90_v2.stl")
foot = load(CECE / "balance_study" / "wide_foot" / "Cece_right_wide_foot.stl")
battery = box((35, 56, 16), (0, 3, -24))
ubec = box((21, 56, 14), (2.3, 0, -8))
hip_case = box((12.2, 23, 22), (25.5, -5.5, -24))
ankle_case = box((12.2, 22.5, 23), (25.5, -3.5, -62))
# Conservative *test* shapes, not measured parts: 2 mm radius output shaft
# and a 3 x 15 x 2 mm trimmed straight horn arm, seated along the leg's Y slot.
shaft = cylinder(2, 11, (25.5, 0, -40))
horn = box((3, 15, 2), (25.5, 0, -43))

parts = {
    "body": body, "coupon": coupon, "leg": leg, "wide_foot": foot,
    "battery_clearance": battery, "ubec_clearance": ubec,
    "hip_case_proxy": hip_case, "ankle_case_proxy": ankle_case,
}
checks = [
    ("body", "leg"), ("body", "wide_foot"), ("leg", "wide_foot"),
    ("body", "hip_case_proxy"), ("coupon", "leg"),
    ("coupon", "wide_foot"), ("coupon", "battery_clearance"),
    ("coupon", "ubec_clearance"), ("coupon", "hip_case_proxy"),
    ("hip_case_proxy", "battery_clearance"), ("hip_case_proxy", "ubec_clearance"),
    ("hip_case_proxy", "leg"), ("hip_case_proxy", "wide_foot"),
    ("ankle_case_proxy", "leg"), ("ankle_case_proxy", "wide_foot"),
]
result = {
    "coupon_watertight": bool(coupon.is_watertight),
    "coupon_components": len(coupon.split(only_watertight=False)),
    "coupon_volume_mm3": round(coupon.volume, 3),
    "nominal_overlap_mm3": {f"{a}__{b}": overlap(parts[a], parts[b]) for a, b in checks},
    "shaft_proxy_overlap_mm3": {n: overlap(p, shaft) for n, p in [("body", body), ("leg", leg), ("hip_case", hip_case)]},
    "horn_proxy_overlap_mm3": {n: overlap(p, horn) for n, p in [("body", body), ("leg", leg), ("hip_case", hip_case)]},
    "limits": [
        "Case envelopes and component placements are inferred; mounting ears, output turret and wire exit are not dimensioned by the seller.",
        "Shaft and trimmed horn proxies are illustrative test solids. Their non-overlap does not prove spline or screw fit.",
        "Neutral-pose intersections do not certify dynamic gait clearance or printed tolerances.",
    ],
}
(HERE / "coupon_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
