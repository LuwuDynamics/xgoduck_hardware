"""Bounded axis aligned electronics placement scan, with provisional hip boxes."""
import sys,itertools,json,warnings
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'cece_mesh_deps'))
import trimesh
warnings.filterwarnings('ignore',category=RuntimeWarning)
HERE=Path(__file__).resolve().parent
BODY=trimesh.load(HERE.parent/'parts_adafruit_draft'/'cece_body_square_OLED_DRAFT.stl',force='mesh')
def box(ext,center):
 m=trimesh.creation.box(extents=ext);m.apply_translation(center);return m
def ov(a,b):return round(abs(trimesh.boolean.intersection([a,b],engine='manifold').volume),3)
hip={k:box((12.2,23,22),(x,-5.5,-24)) for k,x in [('left',-25.5),('right',25.5)]}
placements={
 'battery':((35,56,16),(0,3,-24)), # rotated 56x35x16 clearance envelope
 'ubec':((21,56,14),(0,0,-8)), # rotated 56x21x14 clearance envelope
}
models={k:box(*v) for k,v in placements.items()}
report={'method':'Exact body STL boolean intersections; other modules axis-aligned boxes; charger bounded 2 mm center grid','fixed_provisional_placements':{},'charger_scan':{},'limitations':['SG90 case height and placement inferred; pocket shaft center from STL, not purchased servo measurements.','Battery and UBEC clearance boxes from packaging_study/layout_check.py; charger box is unpurchased candidate.','Exact body STL intersection zero is not a clearance/assembly/retention certification.','Charger scan is finite and axis aligned; it does not exclude rotated, shifted, or external designs.']}
for name,m in models.items():report['fixed_provisional_placements'][name]={'size_mm':placements[name][0],'center_mm':placements[name][1],'body_overlap_mm3':ov(m,BODY),'hip_overlap_mm3':{h:ov(m,s) for h,s in hip.items()}}
report['fixed_provisional_placements']['battery_vs_ubec_overlap_mm3']=ov(models['battery'],models['ubec'])
# Conservative approximate interior AABB. Filter using no-overlap condition before
# expensive exact body boolean. Bounds themselves may include inaccessible space.
inner=np.array([[-32,32],[-32,32],[-37,-1]],float)
fixed=[*placements.values(),((12.2,23,22),(-25.5,-5.5,-24)),((12.2,23,22),(25.5,-5.5,-24))]
for size in sorted(set(itertools.permutations((43.6,23.8,13.5)))):
 s=np.array(size);grids=[np.arange(np.ceil((lo+a/2)/2)*2,(hi-a/2)+.001,2) for (lo,hi),a in zip(inner,s)]
 clear=[]
 for xyz in itertools.product(*grids):
  c=np.array(xyz)
  if all(np.any(np.abs(c-np.array(fc)) >= (s+np.array(fs))/2) for fs,fc in fixed):clear.append(xyz)
 report['charger_scan'][str(size)]={'sample_centers':int(np.prod([len(g) for g in grids])),'module_disjoint_candidates':len(clear),'first_centers':clear[:3]}
(HERE/'layout_search_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
