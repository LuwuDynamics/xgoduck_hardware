"""Four removable side screws joining Cece V3 head to V4 body (candidate).

Creates new files only; source head/body remain unchanged. Measurements are in
assembled millimetres. Manifold mesh Booleans are reimported after STL export.
"""
from __future__ import annotations
import hashlib,json,sys,warnings
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
CECE=HERE.parents[1]
WORKSPACE=HERE.parents[4]
sys.path.insert(0,str(WORKSPACE/'cece_mesh_deps'))
import trimesh
warnings.filterwarnings('ignore',category=RuntimeWarning)

SOURCE_HEAD=CECE/'packaging_study/speaker_pod/side_route_v3/Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl'
SOURCE_BODY=CECE/'packaging_study/Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl'

def load(path):return trimesh.load(path,force='mesh')
def box(size,center):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def xcyl(radius,x0,x1,y,z):
    m=trimesh.creation.cylinder(radius=radius,segment=np.array([(x0,y,z),(x1,y,z)]),sections=96)
    return m
def union(*m):return trimesh.boolean.union(m,engine='manifold')
def cut(a,*m):return trimesh.boolean.difference([a,*m],engine='manifold')
def ov(a,b):return round(abs(float(trimesh.boolean.intersection([a,b],engine='manifold').volume)),5)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

head0=load(SOURCE_HEAD);body0=load(SOURCE_BODY)
centers=[(sx,sy) for sx in (-1,1) for sy in (-1,1)]
Y=22.5;Z=-8.0
head_add=[];head_pilot=[];body_collar=[];body_clear=[]
pilot_core=[];tool_approach=[];screw_head=[]
for sx,sy in centers:
    y=sy*Y
    # Inside tongue ends 0.3mm before the measured V4 inner side wall x±32.5.
    tongue=box((5.7,7.0,13.5),(sx*29.35,y,-6.25)) # |x|26.5..32.2,z-13..+0.5
    bridge=box((7.5,7.0,7.0),(sx*30.25,y,3.5)) # |x|26.5..34,z0..7
    head_add.extend((tongue,bridge))
    # Blind pilot retains 0.5mm of tongue at the innermost X face.
    a,b=(27.0,32.3) if sx>0 else (-32.3,-27.0)
    head_pilot.append(xcyl(1.25,a,b,y,Z))
    # A 1mm external collar gives an M3x8 screw 4.7mm printed engagement.
    a,b=(33.8,35.5) if sx>0 else (-35.5,-33.8)
    body_collar.append(xcyl(4.0,a,b,y,Z))
    a,b=(32.0,35.7) if sx>0 else (-35.7,-32.0)
    body_clear.append(xcyl(1.65,a,b,y,Z))
    a,b=(27.1,35.7) if sx>0 else (-35.7,-27.1)
    pilot_core.append(xcyl(1.0,a,b,y,Z))
    a,b=(37.6,55.0) if sx>0 else (-55.0,-37.6)
    tool_approach.append(xcyl(3.2,a,b,y,Z))
    a,b=(35.5,37.5) if sx>0 else (-37.5,-35.5)
    screw_head.append(xcyl(3.0,a,b,y,Z))

head=cut(union(head0,*head_add),*head_pilot)
body=cut(union(body0,*body_collar),*body_clear)
head_file=HERE/'Cece_head_V3_four_screw_joint_CANDIDATE.stl'
body_file=HERE/'Cece_body_V4_four_screw_joint_CANDIDATE.stl'
head.export(head_file);body.export(body_file)
head=load(head_file);body=load(body_file)
assert head.is_watertight and len(head.split(only_watertight=False))==1
assert body.is_watertight and len(body.split(only_watertight=False))==1

parts={
 'speaker_pod':load(CECE/'packaging_study/speaker_pod/side_route_v3/speaker_pod_side_wire_notch_V3_CANDIDATE.stl'),
 'speaker_grille':load(CECE/'packaging_study/speaker_pod/speaker_retaining_grille.stl'),
 'charger_tray':load(CECE/'packaging_study/charger_cassette/removable_tray.stl'),
 'charger_bezel':load(CECE/'packaging_study/charger_cassette/retaining_bezel.stl'),
 'heart_frame':load(CECE/'packaging_study/Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl'),
 'faceplate':load(CECE/'packaging_study/speaker_pod/side_route_v3/Cece_faceplate_M2_retained_V3_CANDIDATE.stl'),
 'left_leg':load(CECE/'ankle_v2/Cece_left_leg_SG90_v2.stl'),
 'right_leg':load(CECE/'ankle_v2/Cece_right_leg_SG90_v2.stl'),
 'left_foot':load(CECE/'balance_study/wide_foot/Cece_left_wide_foot.stl'),
 'right_foot':load(CECE/'balance_study/wide_foot/Cece_right_wide_foot.stl'),
}
antenna=load(CECE/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');antenna.apply_translation([0,0,27]);parts['antenna']=antenna
for side in (-1,1):
    arm=load(CECE/f'parts_adafruit_draft/Cece_{"Left" if side<0 else "Right"}_Arm_45_DRAFT.stl')
    arm.apply_translation([side*37.2,0,-15]);parts[f'{"left" if side<0 else "right"}_arm']=arm

modules={
 'battery':box((35,56,16),(0,3,-24)),
 'UBEC':box((21,56,14),(2.3,0,-8)),
 'ESP':box((28,8,21),(0,24,10)),
 'amp':box((22,22,6),(17,-6,24)),
 'mic':box((16,16,6),(-14,-5,24)),
 'sensor_PCB':box((45,1.6,20),(0,-18,14.5)),
 'driver_gross_box':box((52,12.3,25.4),(1,11.8,13)),
 'left_hip_SG90':box((12.2,23,22),(-25.5,-5.5,-24)),
 'right_hip_SG90':box((12.2,23,22),(25.5,-5.5,-24)),
}
result={
 'status':'candidate four-screw removable head/body joint, actual screws and print load untested',
 'source_head':str(SOURCE_HEAD),'source_head_sha256':sha(SOURCE_HEAD),
 'source_body':str(SOURCE_BODY),'source_body_sha256':sha(SOURCE_BODY),
 'screw_centers_xyz_mm':[[sx*33.5,sy*Y,Z] for sx,sy in centers],
 'tongue_x_abs_bounds_mm':[26.5,32.2],
 'measured_body_wall_x_abs_bounds_at_joints_mm':[32.5,34.5],
 'nominal_tongue_to_body_inner_wall_gap_mm':.3,
 'candidate_screw':'four M3x8 pan-head screws through Ø3.3mm body clearance into Ø2.5mm blind head pilots',
 'body_collar_diameter_height_mm':[8,1],
 'head_tongue_blind_pilot_depth_mm':5.3,
 'head_tongue_min_inner_web_mm':.5,
 'printed_STLs':{
  'head':{'watertight':head.is_watertight,'components':len(head.split(only_watertight=False)),'volume_mm3':round(abs(float(head.volume)),3),'bounds_xyz_mm':np.round(head.bounds,3).tolist()},
  'body':{'watertight':body.is_watertight,'components':len(body.split(only_watertight=False)),'volume_mm3':round(abs(float(body.volume)),3),'bounds_xyz_mm':np.round(body.bounds,3).tolist()},
 },
 'head_body_solid_overlap_mm3':ov(head,body),
 'head_vs_parts_mm3':{k:ov(head,p) for k,p in parts.items()},
 'body_vs_parts_mm3':{k:ov(body,p) for k,p in parts.items()},
 'new_head_vs_modules_mm3':{k:ov(head,m) for k,m in modules.items()},
 'new_body_vs_modules_mm3':{k:ov(body,m) for k,m in modules.items()},
 'screw_core_clearance_vs_head_body_mm3':[ov(p,head)+ov(p,body) for p in pilot_core],
 'screw_head_vs_head_body_mm3':[ov(p,head)+ov(p,body) for p in screw_head],
 'tool_approach_vs_printed_mm3':[
    {k:ov(t,p) for k,p in {'head':head,'body':body,**parts}.items()}
    for t in tool_approach],
 'intended_head_bridge_fusion_mm3':[ov(a,head0) for a in head_add[1::2]],
 'intended_body_collar_fusion_mm3':[ov(a,body0) for a in body_collar],
 'limits':[
  'Screw cores are void probes, not actual thread shape; four M3x8 screws need printed pilot and pull-out tests.',
  'Local wall thickness inferred from mesh slices at screw centres; FDM shrink/elephant-foot can close the 0.3mm gap.',
  'Modules are published/candidate boxes except PiicoDev, whose exact partial STEP is checked separately.',
  'Head/body circumferential rim contact, full insertion force, torque under walking and cable flex remain untested.',
 ]
}
(HERE/'mesh_validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
