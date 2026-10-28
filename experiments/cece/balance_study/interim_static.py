"""Reproduce the *interim* Cece static balance calculation.

The mounted centres are candidate coordinates, not measured assemblies. This
script deliberately leaves missing hardware and actual FDM print weights out
of the calculated mass. It uses the actual sole vertices from the two foot
STLs, rather than a rectangular foot approximation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from balance_study import (DENSITY_G_CM3, G, PARTS, REQUIRED_HARDWARE,
                           RESERVE_MM, polygon_hull, read_binary_stl,
                           round_list, signed_margin_mm, weighted_com)

HERE = Path(__file__).resolve().parent
CECE = HERE.parent
INPUT = HERE / 'interim_inputs.json'
OUTPUT = HERE / 'interim_static_results.json'
FRAME_V2 = CECE / 'packaging_study' / 'Cece_Adafruit4741_Heart_Frame_V2_CANDIDATE.stl'
WIDE_FEET = HERE / 'wide_foot'


def part_spec(name: str, original: Path, translation: tuple,
              variant: str, source: dict) -> tuple[Path, tuple]:
    override = source.get('part_overrides', {}).get(name)
    if override:
        path = CECE / override['stl']
        translation = tuple(override['translation_mm'])
    elif name == 'frame':
        path = FRAME_V2
        # V2 was exported *after* placement in packaging_study/layout_check.py.
        translation = (0, 0, 0)
    else:
        path = original
    if variant == 'wider' and name in ('left_foot', 'right_foot'):
        side = name.split('_')[0]
        path = WIDE_FEET / f'Cece_{side}_wide_foot.stl'
    return path, translation


def box_overlap_mm3(size_a, center_a, size_b, center_b):
    """Exact axis-aligned box intersection for candidate clearance envelopes."""
    lengths = [max(0.0, min(ca+sa/2, cb+sb/2)-max(ca-sa/2, cb-sb/2))
               for sa,ca,sb,cb in zip(size_a,center_a,size_b,center_b)]
    return math.prod(lengths)


def case_for(variant: str, hardware: list[dict], source: dict) -> dict:
    shell = []
    soles = {}
    sole_vertices = []
    floor_z = None
    specs = [(name, *part_spec(name, original, translation, variant, source))
             for name, original, translation in PARTS]
    specs += [(row['name'], CECE / row['stl'], tuple(row['translation_mm']))
              for row in source.get('additional_printed_parts', [])]
    for name, path, translation in specs:
        mesh = read_binary_stl(path)
        mass = mesh['volume_mm3'] * DENSITY_G_CM3 / 1000.0
        center = [a+b for a,b in zip(mesh['center_local_mm'], translation)]
        shell.append({'name': name, 'mass_g': mass, 'center_mm': center,
                      'stl': path.relative_to(CECE).as_posix(),
                      'stl_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        if name.endswith('_foot'):
            z = min(v[2] + translation[2] for v in mesh['vertices'])
            floor_z = z if floor_z is None else min(floor_z, z)
            soles[name] = [(v[0] + translation[0], v[1] + translation[1],
                            v[2] + translation[2]) for v in mesh['vertices']]

    support = {}
    for name, verts in soles.items():
        xy = [(x, y) for x, y, z in verts if z <= floor_z + 0.1]
        sole_vertices.extend(xy)
        support[name] = polygon_hull(xy)
    support['both_feet'] = polygon_hull(sole_vertices)

    shell_mass, shell_com = weighted_com(shell)
    included = shell + hardware
    included_mass, com = weighted_com(included)
    h = com[2] - floor_z
    margins = {k: signed_margin_mm(com[:2], p) for k, p in support.items()}

    # Solve the required pure lateral COM translation on the *actual* polygon,
    # preserving the current Y coordinate. This is a geometric condition only.
    shifts = {}
    for side in ('left_foot', 'right_foot'):
        direction = -1 if side == 'left_foot' else 1
        def margin_at(distance):
            return signed_margin_mm((com[0] + direction*distance, com[1]),
                                    support[side])
        if margin_at(0) >= RESERVE_MM:
            shifts[side] = 0.0
            continue
        high = 1.0
        while high < 128.0 and margin_at(high) < RESERVE_MM:
            high *= 2
        if margin_at(high) < RESERVE_MM:
            shifts[side] = None
            continue
        low = 0.0
        for _ in range(50):
            mid = (low + high)/2
            if margin_at(mid) >= RESERVE_MM:
                high = mid
            else:
                low = mid
        shifts[side] = high

    return {
        'variant': variant,
        'shell_nominal_100_percent_solid_PLA_mass_g': round(shell_mass, 3),
        'shell_nominal_center_mm': round_list(shell_com),
        'included_nonplastic_hardware_mass_g': round(sum(x['mass_g'] for x in hardware), 3),
        'included_combined_nominal_mass_g': round(included_mass, 3),
        'included_combined_center_mm': round_list(com),
        'combined_center_height_above_floor_mm': round(h, 3),
        'floor_z_mm': round(floor_z, 3),
        'signed_support_margin_mm': {k: round(v, 3) for k, v in margins.items()},
        'lateral_COM_shift_for_5mm_single_foot_margin_mm':
            {k: None if v is None else round(v, 3) for k, v in shifts.items()},
        'equivalent_rigid_body_tilt_for_shift_deg':
            {k: None if v is None else round(math.degrees(math.atan2(v, h)), 2)
             for k, v in shifts.items()},
        'approx_outward_lateral_acceleration_budget_m_s2_at_current_pose':
            {k: round(G*max(0.0, v-RESERVE_MM)/h, 3)
             for k, v in margins.items() if k in ('left_foot', 'right_foot')},
        'support_polygon_xy_mm':
            {k: [round_list(point, 2) for point in p] for k,p in support.items()},
        'shell_parts':
            [{**x, 'mass_g': round(x['mass_g'], 4),
              'center_mm': round_list(x['center_mm'])} for x in shell],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=INPUT)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    source = json.loads(args.input.read_text(encoding='utf-8'))
    hardware = source.get('included_hardware', source.get('included_purchased_hardware'))
    if hardware is None:
        raise ValueError('Missing included_hardware')
    for entry in hardware:
        if not isinstance(entry['mass_g'], (int, float)) or entry['mass_g'] <= 0:
            raise ValueError(f"Bad mass for {entry['name']}")
        if not isinstance(entry['center_mm'], list) or len(entry['center_mm']) != 3:
            raise ValueError(f"Bad center for {entry['name']}")
        if not all(isinstance(v, (int, float)) for v in entry['center_mm']):
            raise ValueError(f"Bad center for {entry['name']}")
    known_names = {x['name'] for x in hardware}
    by_name = {x['name']: x for x in hardware}
    sizes = source['collision_proxy_sizes_mm']
    box_names = list(sizes)
    for name in box_names:
        if name not in by_name or len(sizes[name]) != 3 or any(v <= 0 for v in sizes[name]):
            raise ValueError(f'Invalid collision envelope for {name}')
    box_pair_overlaps = {}
    for i, name in enumerate(box_names):
        for other in box_names[i+1:]:
            box_pair_overlaps[f'{name}__{other}'] = round(
                box_overlap_mm3(sizes[name], by_name[name]['center_mm'],
                                sizes[other], by_name[other]['center_mm']), 3)
    has_collision = any(v > 0 for v in box_pair_overlaps.values())
    missing = [x for x in REQUIRED_HARDWARE if x not in known_names]
    variants = source.get('foot_variants', ['baseline', 'wider'])
    if not variants or any(v not in ('baseline', 'wider') for v in variants):
        raise ValueError('foot_variants must contain baseline and/or wider')
    cases = {v: case_for(v, hardware, source) for v in variants}
    shell_names = [name for name, _, _ in PARTS]
    shell_names += [row['name'] for row in source.get('additional_printed_parts', [])]
    report = {
        'status': ('INTERIM_MASS_SCENARIO_HAS_KNOWN_PACKAGING_COLLISION; FULL_ROBOT_NOT_VERIFIED'
                   if has_collision else 'INTERIM_STATIC_SCENARIO_ONLY; FULL_ROBOT_NOT_VERIFIED'),
        'coordinate_system': 'Assembled Cece CAD XYZ in mm; X left/right, Y front/back; floor is the lowest sole vertex',
        'inputs': source,
        'candidate_unpurchased_hardware': source.get('candidate_unpurchased_hardware', []),
        'known_layout_conflicts': source.get('known_layout_conflicts', []),
        'candidate_box_pair_overlap_mm3': box_pair_overlaps,
        'model': {
            'plastic': 'Exact STL mesh tetrahedral volume and centroid, nominal 1.24 g/cm3 100%-solid PLA; no slicer infill or measured print mass',
            'hardware': 'Supplier-listed mass or explicitly identified candidate estimate at candidate mounted center; servo case centroid proxy is not a measured mass centroid',
            'support': 'Convex hull of actual sole STL vertices within 0.1 mm of minimum Z; assumes both listed feet are flat and fully contacting a level floor',
            'design_reserve_mm': RESERVE_MM,
            'gravity_m_s2': G,
        },
        'cases': cases,
        'unmodeled': {
            'hardware': missing,
            'actual_printed_part_masses': shell_names,
            'additional': ['Printed supports, infill density/distribution and mounting parts',
                           'Exact mounted servo hardware positions and mass centroids',
                           'Cable bends, connector boots, screws, adhesive and floor pads',
                           'Gait pose changes, active support contacts, angular momentum, floor friction and servo torque'],
        },
        'interpretation': 'Only a fixed neutral pose. A negative one-foot margin means the current COM projection is outside that planted foot. Zero acceleration budget in that pose is not a walking-speed measurement. A positive two-foot margin says only that ideal at-rest support is geometrically possible for the included masses.',
    }
    args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    compact = {'status': report['status'],
               'included_hardware': [x['name'] for x in hardware],
               'cases': {k: {f: v[f] for f in ('included_combined_nominal_mass_g',
                      'included_combined_center_mm', 'combined_center_height_above_floor_mm',
                      'signed_support_margin_mm',
                      'lateral_COM_shift_for_5mm_single_foot_margin_mm')}
                      for k, v in cases.items()},
               'missing_hardware': missing,
               'candidate_unpurchased_hardware': report['candidate_unpurchased_hardware'],
               'candidate_box_pair_overlap_mm3': box_pair_overlaps,
               'known_layout_conflicts': report['known_layout_conflicts']}
    print(json.dumps(compact, indent=2))


if __name__ == '__main__':
    main()
