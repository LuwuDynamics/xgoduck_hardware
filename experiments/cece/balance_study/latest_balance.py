"""Static mass/COM/support audit for the current Cece speaker and UC2 candidates.

Run from any working directory. The 20% infill case is a stated analytical
estimate, *not* a slicer result. All module masses omitted from the input are
excluded rather than silently guessed.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from balance_study import polygon_hull, read_binary_stl, round_list, signed_margin_mm, weighted_com

HERE = Path(__file__).resolve().parent
CECE = HERE.parent
INPUT = HERE / 'latest_inputs.json'
OUTPUT = HERE / 'latest_balance_results.json'
G = 9.80665


def surface_area_mm2(vertices):
    """Sum exact triangular facet areas of the binary STL."""
    area = 0.0
    for i in range(0, len(vertices), 3):
        a, b, c = vertices[i:i+3]
        ux, uy, uz = (b[j]-a[j] for j in range(3))
        vx, vy, vz = (c[j]-a[j] for j in range(3))
        cx, cy, cz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        area += 0.5*math.sqrt(cx*cx+cy*cy+cz*cz)
    return area


def shift_for_reserve(com, polygon, direction, reserve):
    """Pure lateral COM translation to the specified polygon edge reserve."""
    def margin(d):
        return signed_margin_mm((com[0]+direction*d, com[1]), polygon)
    if margin(0.0) >= reserve:
        return 0.0
    hi = 1.0
    while hi < 128 and margin(hi) < reserve:
        hi *= 2
    if margin(hi) < reserve:
        return None
    lo = 0.0
    for _ in range(50):
        mid = (lo+hi)/2
        if margin(mid) >= reserve:
            hi = mid
        else:
            lo = mid
    return hi


def static_case(print_rows, hardware_rows, support, floor_z, reserve):
    shell_mass, shell_com = weighted_com(print_rows)
    mass, com = weighted_com(print_rows+hardware_rows)
    height = com[2]-floor_z
    margins = {k: signed_margin_mm(com[:2], poly) for k, poly in support.items()}
    shifts = {
        'left_foot': shift_for_reserve(com, support['left_foot'], -1, reserve),
        'right_foot': shift_for_reserve(com, support['right_foot'], 1, reserve),
    }
    return {
        'printed_mass_g': round(shell_mass, 3),
        'printed_center_mm': round_list(shell_com),
        'included_hardware_mass_g': round(sum(row['mass_g'] for row in hardware_rows), 3),
        'included_total_mass_g': round(mass, 3),
        'included_center_mm': round_list(com),
        'center_height_above_floor_mm': round(height, 3),
        'signed_support_margin_mm': {k: round(v, 3) for k,v in margins.items()},
        'lateral_COM_shift_for_reserve_mm':
            {k: None if v is None else round(v, 3) for k,v in shifts.items()},
        'equivalent_rigid_tilt_for_shift_deg':
            {k: None if v is None else round(math.degrees(math.atan2(v, height)), 2)
             for k,v in shifts.items()},
        'outward_lateral_acceleration_limit_from_current_one_foot_pose_m_s2':
            {k: round(G*max(0.0, margins[k])/height, 3)
             for k in ('left_foot','right_foot')},
        'outward_lateral_acceleration_limit_if_shifted_to_5mm_edge_margin_m_s2':
            round(G*reserve/height, 3),
    }


def main():
    source = json.loads(INPUT.read_text(encoding='utf-8'))
    model = source['print_model']
    rho = float(model['pla_density_g_cm3'])
    fill = float(model['infill_fraction'])
    skin_t = float(model['equivalent_outer_skin_thickness_mm'])
    reserve = float(source['support_reserve_mm'])
    if not (rho > 0 and 0 <= fill <= 1 and skin_t > 0 and reserve >= 0):
        raise ValueError('Invalid print-model parameters')

    parts, exact_parts, soles = [], [], {}
    for record in source['printed_parts']:
        name = record['name']
        path = CECE / record['stl']
        offset = record['translation_mm']
        mesh = read_binary_stl(path)
        V = mesh['volume_mm3']
        A = surface_area_mm2(mesh['vertices'])
        skin_fraction = min(1.0, A*skin_t/V)
        nominal_fraction = skin_fraction + fill*(1.0-skin_fraction)
        mass_solid = rho*V/1000
        center = [mesh['center_local_mm'][i]+offset[i] for i in range(3)]
        exact_parts.append({'name': name, 'solid_PLA_mass_g': mass_solid,
                            'nominal_20pct_infill_mass_g': mass_solid*nominal_fraction,
                            'center_mm': center})
        parts.append({
            'name': name, 'stl': record['stl'],
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'translation_mm': offset, 'solid_volume_mm3': round(V, 3),
            'surface_area_mm2': round(A, 3),
            'estimated_solid_skin_fraction': round(skin_fraction, 5),
            'estimated_20pct_infill_material_fraction': round(nominal_fraction, 5),
            'solid_PLA_mass_g': round(mass_solid, 4),
            'nominal_20pct_infill_mass_g': round(mass_solid*nominal_fraction, 4),
            'center_mm': round_list(center),
        })
        if name in ('left_foot','right_foot'):
            soles[name] = [(v[0]+offset[0],v[1]+offset[1],v[2]+offset[2])
                           for v in mesh['vertices']]
    if set(soles) != {'left_foot','right_foot'}:
        raise ValueError('Both wider foot meshes are required')
    floor_z = min(v[2] for vertices in soles.values() for v in vertices)
    foot_xy = {name: [(x,y) for x,y,z in vertices if z <= floor_z+0.1]
               for name,vertices in soles.items()}
    support = {name: polygon_hull(xy) for name,xy in foot_xy.items()}
    support['both_feet'] = polygon_hull(foot_xy['left_foot']+foot_xy['right_foot'])

    hardware = source['known_hardware']
    if any(row['mass_g'] <= 0 or len(row['center_mm']) != 3 for row in hardware):
        raise ValueError('Invalid hardware mass or center')
    speaker = source['speaker_sensitivity']
    if speaker['mass_g'] <= 0 or len(speaker['center_mm']) != 3:
        raise ValueError('Invalid speaker sensitivity')
    speaker_row = {k: speaker[k] for k in ('name','mass_g','center_mm')}
    cases = {}
    for model_name, mass_field in (
        ('solid_PLA_bound', 'solid_PLA_mass_g'),
        ('nominal_20pct_infill', 'nominal_20pct_infill_mass_g'),
    ):
        plastic = [{'name': p['name'], 'mass_g': p[mass_field],
                    'center_mm': p['center_mm']} for p in exact_parts]
        cases[model_name] = {
            'listed_heavy_hardware_only': static_case(plastic, hardware, support,
                                                     floor_z, reserve),
            'plus_12g_speaker_sensitivity': static_case(plastic,
                    hardware+[speaker_row], support, floor_z, reserve),
        }
    # The other boards have known candidate positions but no verified masses.
    # A fixed 10 g perturbation at each position exposes their effect without
    # pretending 10 g is the actual mass of any board.
    nominal_plastic = [{'name': p['name'],
                        'mass_g': p['nominal_20pct_infill_mass_g'],
                        'center_mm': p['center_mm']} for p in exact_parts]
    nominal_base = cases['nominal_20pct_infill']['plus_12g_speaker_sensitivity']
    unit_sensitivity = {}
    for module in source['unmeasured_modules']:
        if module['center_mm'] is None:
            continue
        perturbed = static_case(nominal_plastic,
                                hardware+[speaker_row, {'name': module['name'],
                                                        'mass_g': 10.0,
                                                        'center_mm': module['center_mm']}],
                                support, floor_z, reserve)
        unit_sensitivity[module['name']] = {
            'test_mass_g': 10.0,
            'test_center_mm': module['center_mm'],
            'delta_center_mm': round_list([
                perturbed['included_center_mm'][i]-nominal_base['included_center_mm'][i]
                for i in range(3)]),
            'delta_two_foot_margin_mm': round(
                perturbed['signed_support_margin_mm']['both_feet']
                - nominal_base['signed_support_margin_mm']['both_feet'], 3),
            'left_foot_margin_after_test_mm':
                perturbed['signed_support_margin_mm']['left_foot'],
            'right_foot_margin_after_test_mm':
                perturbed['signed_support_margin_mm']['right_foot'],
        }
    report = {
        'status': 'INTERIM_NEUTRAL_STATIC_ONLY; FULL_PAYLOAD_AND_GAIT_UNVERIFIED',
        'source_input': INPUT.name,
        'print_model': model,
        'print_model_limits': [
            'The solid PLA case is the full CAD plastic volume, not a scale measurement; support material and hardware are additional.',
            'The 20% case uses a first-order surface-area skin estimate, not toolpaths from a slicer. It assumes the same solid-volume centroid for each printed part.',
            'A 1.2 mm equivalent skin approximates three 0.4 mm walls and similar top/bottom skin. Local thin features may be fully solid; corners and overlapping skins are approximate.',
            'Actual nozzle width, wall count, top/bottom layers, infill pattern, support material and filament density require a slicer result or weighed parts.',
        ],
        'support_method': 'Convex hull of true bottom STL vertices within 0.1 mm of the minimum sole Z, for a level floor and fully flat neutral feet',
        'floor_z_mm': round(floor_z, 3),
        'support_reserve_mm': reserve,
        'support_polygons_xy_mm': {k: [round_list(p,2) for p in poly]
                                   for k,poly in support.items()},
        'printed_parts': parts,
        'included_hardware': hardware,
        'speaker_sensitivity': speaker,
        'unmeasured_modules': source['unmeasured_modules'],
        'unmeasured_module_10g_position_sensitivity': unit_sensitivity,
        'unresolved_fit': source['unresolved_fit'],
        'cases': cases,
        'interpretation': 'A positive two-foot margin is an ideal at-rest geometric result for the included masses. Negative single-foot margins mean the neutral-pose COM lies outside either individual sole. Static support does not verify joint torque, usable gait, foot contact, floor friction, cable reach or charging safety.',
    }
    OUTPUT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'status':report['status'], 'floor_z_mm':report['floor_z_mm'],
                      'cases':cases, 'unmeasured_modules':source['unmeasured_modules']}, indent=2))


if __name__ == '__main__':
    main()
