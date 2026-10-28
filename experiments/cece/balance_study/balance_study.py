"""Reproducible Cece V2 support and centre-of-mass study.

Uses binary STL tetrahedra for geometric volume/centroid and the actual sole
vertices for support polygons. Requires only Python 3 standard library.
Optional measured_inputs.json supplies *measured* masses and CAD placements.
"""
from __future__ import annotations
import json
import math
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
CECE = HERE.parent
OLD = CECE / 'parts_adafruit_draft'
NEW = CECE / 'ankle_v2'
DENSITY_G_CM3 = 1.24  # nominal PLA assumption, NOT a filament weighing result
G = 9.80665
RESERVE_MM = 5.0  # explicit analysis threshold, not a demonstrated gait margin

# Transforms from design/analyze_geometry.py; ankle_v2 files replace old feet/legs.
PARTS = [
    ('body', OLD/'cece_body_square_OLED_DRAFT.stl', (0, 0, 0)),
    ('head', OLD/'Cece_Head_Centered_Antenna_DRAFT.stl', (0, 0, 0)),
    ('face', OLD/'Cece_Happy_Faceplate_DRAFT.stl', (0, 0, 0)),
    ('frame', OLD/'cece_heart_frame_Adafruit4741_DRAFT.stl', (0, -37.5, -19)),
    ('antenna', OLD/'Cece_Antenna_DRAFT.stl', (0, 0, 27)),
    ('left_arm', OLD/'Cece_Left_Arm_45_DRAFT.stl', (-37.2, 0, -15)),
    ('right_arm', OLD/'Cece_Right_Arm_45_DRAFT.stl', (37.2, 0, -15)),
    ('left_leg', NEW/'Cece_left_leg_SG90_v2.stl', (0, 0, 0)),
    ('right_leg', NEW/'Cece_right_leg_SG90_v2.stl', (0, 0, 0)),
    ('left_foot', NEW/'Cece_left_foot_bearing_v2.stl', (0, 0, 0)),
    ('right_foot', NEW/'Cece_right_foot_bearing_v2.stl', (0, 0, 0)),
    ('left_washer', NEW/'Cece_left_bearing_washer.stl', (0, 0, 0)),
    ('right_washer', NEW/'Cece_right_bearing_washer.stl', (0, 0, 0)),
]
REQUIRED_HARDWARE = [
    'left_ankle_sg90', 'right_ankle_sg90', 'left_hip_sg90', 'right_hip_sg90',
    'battery', 'battery_charger', 'ubec', 'esp32_c3', 'servo_driver',
    'oled', 'ultrasonic_sensor', 'microphone', 'amplifier', 'speaker',
    'leds_and_resistors', 'switch_and_connectors', 'cables_and_fasteners',
]

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def read_binary_stl(path):
    raw = path.read_bytes()
    if len(raw) < 84:
        raise ValueError(f'{path}: too short for binary STL')
    count = struct.unpack_from('<I', raw, 80)[0]
    if len(raw) != 84 + 50*count:
        raise ValueError(f'{path}: expected binary STL with {count} faces')
    signed_volume = 0.0
    moments = [0.0, 0.0, 0.0]
    verts = []
    for row in struct.iter_unpack('<12fH', raw[84:]):
        a, b, c = row[3:6], row[6:9], row[9:12]
        volume = dot(a, cross(b, c))/6.0
        signed_volume += volume
        for axis in range(3):
            moments[axis] += volume*(a[axis]+b[axis]+c[axis])/4.0
        verts.extend((a, b, c))
    if abs(signed_volume) < 1e-8:
        raise ValueError(f'{path}: zero or badly oriented volume')
    center = tuple(x/signed_volume for x in moments)
    return {'volume_mm3': abs(signed_volume), 'center_local_mm': center, 'vertices': verts, 'triangle_count': count}

def polygon_hull(points):
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in points))
    if len(pts) < 3:
        raise ValueError('Contact polygon has fewer than 3 distinct points')
    def turn(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 1e-8:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 1e-8:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def signed_margin_mm(point, polygon):
    # CCW convex polygon; positive inside. Min edge distance controls tipping.
    px, py = point
    values = []
    for a, b in zip(polygon, polygon[1:]+polygon[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        values.append((dx*(py-a[1])-dy*(px-a[0]))/math.hypot(dx, dy))
    return min(values)

def weighted_com(items):
    mass = sum(item['mass_g'] for item in items)
    if mass <= 0:
        raise ValueError('nonpositive total mass')
    return mass, [sum(item['mass_g']*item['center_mm'][i] for item in items)/mass for i in range(3)]

def round_list(values, n=3):
    return [round(float(x), n) for x in values]

def main():
    source = json.loads((HERE/'measured_inputs.json').read_text(encoding='utf-8'))
    part_masses = source.get('printed_part_masses_g', {})
    hardware = source.get('hardware', {})
    shell_items = []
    missing_print_masses = []
    meshes = {}
    for name, path, offset in PARTS:
        data = read_binary_stl(path)
        meshes[name] = data
        geometric_mass = data['volume_mm3']/1000.0*DENSITY_G_CM3
        measured = part_masses.get(name)
        if measured is None:
            missing_print_masses.append(name)
        elif not isinstance(measured, (int, float)) or measured <= 0:
            raise ValueError(f'Invalid printed mass for {name}')
        m = float(measured) if measured is not None else geometric_mass
        center = [data['center_local_mm'][i]+offset[i] for i in range(3)]
        shell_items.append({'name': name, 'source_stl': str(path.relative_to(CECE)).replace('\\', '/'),
                            'source': 'measured_print_mass' if measured is not None else 'nominal_solid_PLA_geometry',
                            'volume_mm3': round(data['volume_mm3'], 3),
                            'mass_g': round(m, 4), 'center_mm': round_list(center)})
    floor_z = min(v[2] for name in ('left_foot','right_foot') for v in meshes[name]['vertices'])
    sole_polygons = {}
    all_sole = []
    for name in ('left_foot', 'right_foot'):
        verts = meshes[name]['vertices']
        ground = [(v[0], v[1]) for v in verts if v[2] <= floor_z+0.1]
        if not ground:
            raise ValueError(f'{name}: no sole points at ground')
        sole_polygons[name] = polygon_hull(ground)
        all_sole.extend(ground)
    support = {'both_feet': polygon_hull(all_sole),
               'left_foot': sole_polygons['left_foot'],
               'right_foot': sole_polygons['right_foot']}
    shell_mass, shell_com = weighted_com(shell_items)
    shell_height = shell_com[2]-floor_z
    shell_margins = {k: signed_margin_mm(shell_com[:2], poly) for k, poly in support.items()}
    hardware_items, missing_hardware = [], []
    for name in REQUIRED_HARDWARE:
        record = hardware.get(name, {})
        mass, center = record.get('mass_g'), record.get('center_mm')
        if mass is None or center is None:
            missing_hardware.append(name)
            continue
        if not isinstance(mass, (int,float)) or mass <= 0 or not isinstance(center, list) or len(center) != 3:
            raise ValueError(f'Invalid hardware mass/center for {name}')
        if not all(isinstance(v, (int,float)) for v in center):
            raise ValueError(f'Invalid hardware center for {name}')
        hardware_items.append({'name': name, 'mass_g': float(mass), 'center_mm': center,
                               'source': record.get('source', 'user_provided_unattributed')})
    full = {'status': 'INCOMPLETE', 'missing_print_masses': missing_print_masses,
            'missing_hardware': missing_hardware}
    if not missing_print_masses and not missing_hardware:
        m, com = weighted_com(shell_items+hardware_items)
        h = com[2]-floor_z
        margins = {k: signed_margin_mm(com[:2], poly) for k, poly in support.items()}
        full = {'status':'INPUT_MASS_STATIC_SCREEN_ONLY','mass_g':round(m,3),
                'center_mm':round_list(com),'height_above_floor_mm':round(h,3),
                'signed_support_margin_mm':{k:round(v,3) for k,v in margins.items()},
                'at_rest_with_both_feet':'inside' if margins['both_feet']>0 else 'outside',
                'single_foot_static_pass':{k: margins[k] >= RESERVE_MM for k in ('left_foot','right_foot')},
                'one_foot_dynamic_acceleration_limit_m_s2_at_current_pose':
                    {k: round(G*max(0,margins[k]-RESERVE_MM)/h,3) if h>0 else None
                     for k in ('left_foot','right_foot')},
                'warning':'These are one fixed pose only; a gait needs pose-by-pose COM, angular momentum, contact and actuator limits.'}
    # Shift-to-support is geometric and valid even before hardware mass is known
    # if the assembled COM is later provided. For this shell-only reference,
    # inner edges at y near zero are exactly +/-15 mm.
    right_inner = min(v[0] for v in support['right_foot'])
    left_inner = max(v[0] for v in support['left_foot'])
    shell_right_shift = right_inner+RESERVE_MM-shell_com[0]
    shell_left_shift = shell_com[0]-(left_inner-RESERVE_MM)
    report = {
        'status':'FULL_ROBOT_NOT_VERIFIED' if full['status']=='INCOMPLETE' else 'STATIC_ONLY',
        'coordinates':'STL assembled mm; ground is minimum sole Z; X is left/right; Y is front/back',
        'method':'Exact STL tetrahedron volumes/centroids, documented assembled transforms, convex hull of sole vertices at ground +0.1 mm; no rigid-body dynamics engine',
        'assumptions':{'nominal_PLA_density_g_cm3':DENSITY_G_CM3,'ground_z_mm':round(floor_z,4),
                       'reserve_to_support_edge_mm':RESERVE_MM,'gravity_m_s2':G},
        'parts':shell_items,
        'support_polygons_xy_mm':{k:[round_list(v,2) for v in poly] for k,poly in support.items()},
        'shell_only_nominal_solid_PLA':{
            'mass_g':round(shell_mass,3),'center_mm':round_list(shell_com),
            'height_above_floor_mm':round(shell_height,3),
            'signed_support_margin_mm':{k:round(v,3) for k,v in shell_margins.items()},
            'lateral_shift_for_single_foot_with_reserve_mm':{'right':round(shell_right_shift,3),'left':round(shell_left_shift,3)},
            'equivalent_rigid_body_tilt_deg':{'right':round(math.degrees(math.atan2(shell_right_shift,shell_height)),2),
                                             'left':round(math.degrees(math.atan2(shell_left_shift,shell_height)),2)},
            'outward_acceleration_limit_m_s2_if_5mm_single_foot_margin':round(G*RESERVE_MM/shell_height,3),
            'caveat':'Bare printed-shell geometry only; density 1.24 and 100%-solid material are not a slicer or scale result.'},
        'full_hardware':full,
        'dynamic_method':'For each gait sample: transform every mass/centre into its actual pose; determine contacting sole polygon; compute COM position/velocity/acceleration and angular-momentum rate. Approximate lateral zero-moment point on level ground: x_ZMP=x_COM-h*a_x/(g+a_z)-Hdot_y/[M*(g+a_z)] with consistent sign convention. Require ZMP inside the active support polygon with reserve, plus positive normal force, friction and measured servo torque/current margin.',
        'limitations':['No measured print masses or complete electronics masses/placements yet.',
                       'No actual foot pressure map, friction, battery charge position, servo current or torque under motion.',
                       'Convex hull is a theoretical flat-foot contact area; real print and floor may touch less area.',
                       '5 mm reserve is a design criterion, not a validated safe threshold.',
                       'The previous MuJoCo run used box contacts and assumed masses; it does not validate balance or walking.']}
    (HERE/'balance_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'shell_only_nominal_solid_PLA':report['shell_only_nominal_solid_PLA'],
                      'full_hardware':full,'support_polygons_xy_mm':report['support_polygons_xy_mm']},indent=2))

if __name__=='__main__':main()
