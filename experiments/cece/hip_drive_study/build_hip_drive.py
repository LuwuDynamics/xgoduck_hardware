"""Recess study for the existing Otto/Cece leg; SG90 horn dimensions assumed.

The 3 x 15 x 2 mm horn proxy is only a test case, not a model of the
purchased horn. The STL outputs are for design inspection and test fitting.
"""
from pathlib import Path
import json,sys,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
import trimesh

def box(size,center):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def load(p):return trimesh.load(p,force='mesh')
def overlap(a,b):
    if (a.bounds[1] <= b.bounds[0]).any() or (b.bounds[1] <= a.bounds[0]).any():return 0.0
    return abs(float(trimesh.boolean.intersection([a,b],engine='manifold').volume))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()

result={'status':'TEST GEOMETRY ONLY: supplied horn, fastening, print strength and movement unverified',
        'horn_proxy_mm':[3,15,2], 'pocket_mm':[3.7,16.2,3.2],
        'side_clamp':'Two proposed M2 side screws press on horn edges; pilot holes Ø1.8 mm; physical retention and wear untested',
        'horn_center_z_mm':-43, 'results':{},
        'limitations':['Actual servo horn, spline and screw dimensions unknown',
           'Contact with and retention of real horn need physical inspection',
           'Side screws are an adjustable anti-backlash clamp trial and do not replace the servo horn central retaining screw',
           'Screw length, clearance, engagement, clamp pressure, plastic creep and repeatable torque must be physically tested',
           'Printed wall strength and torsional fatigue not assessed',
           'Ankle horn pocket, servo case and powered gait still need validation']}
for side,x in [('right',25.5),('left',-25.5)]:
    source=CECE/'ankle_v2'/f'Cece_{side}_leg_SG90_v2.stl'
    foot_path=CECE/'balance_study'/'wide_foot'/f'Cece_{side}_wide_foot.stl'
    original=load(source);foot=load(foot_path)
    cut=box((3.7,16.2,3.2),(x,0,-43.1))
    sign=1 if side=='right' else -1
    pilots=[trimesh.creation.cylinder(radius=.9,segment=np.array([[x+sign*1.8,y,-43.1],
               [x+sign*9.0,y,-43.1]]),sections=64) for y in (-5.5,5.5)]
    changed=trimesh.boolean.difference([original,cut,*pilots],engine='manifold')
    path=HERE/f'Cece_{side}_leg_hip_slot_TEST_ONLY.stl';changed.export(path);changed=load(path)
    horn=box((3,15,2),(x,0,-43))
    sweeps={}
    for angle in (-45,-30,-15,0,15,30,45):
        moved=changed.copy(); moved.apply_transform(trimesh.transformations.rotation_matrix(
            np.deg2rad(angle),[0,1,0],[x,0,-71.5]))
        sweeps[str(angle)]=round(overlap(moved,foot),5)
    variants={}
    for width in (2.5,3.0,3.4,3.8):
        p=box((width,15,2),(x,0,-43));variants[str(width)]=round(overlap(changed,p),5)
    result['results'][side]={'source_sha256':h(source),'output_sha256':h(path),
        'original_volume_mm3':round(original.volume,3),'revised_volume_mm3':round(changed.volume,3),
        'removed_volume_mm3':round(original.volume-changed.volume,3),
        'watertight':bool(changed.is_watertight),'connected_components':len(changed.split(only_watertight=False)),
        'sample_horn_original_overlap_mm3':round(overlap(original,horn),5),
        'sample_horn_revised_overlap_mm3':round(overlap(changed,horn),5),
        'horn_width_proxy_overlap_mm3':variants,'ankle_sweep_leg_vs_wide_foot_mm3':sweeps}
(HERE/'hip_drive_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
