"""Candidate Ø2 speaker cable centerlines from right rear entrance toward amp."""
from pathlib import Path
import json,sys
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[5]/'cece_mesh_deps'))
import trimesh
def m(path):return trimesh.load(path,force='mesh')
def box(s,c):
    a=trimesh.creation.box(extents=s);a.apply_translation(c);return a
def segment(p,q):return trimesh.creation.cylinder(radius=1,segment=np.array([p,q]),sections=64)
def ov(a,b):return round(abs(float(trimesh.boolean.intersection([a,b],engine='manifold').volume)),3)
CECE=HERE.parents[2];head=m(CECE/'packaging_study/servo_plug_check/Cece_head_vertical_driver_hood_CANDIDATE.stl')
modules={
 'ESP':box((28,8,21),(0,24,10)),
 'Driver_gross_bbox':box((52,12.3,25.4),(1,13,13)),
 'Amp':box((22,22,6),(17,-5,24)),
 'Mic':box((16,16,6),(-14,-5,24)),
}
paths={
 'high_over_amp':[(28,24,26),(28,6.5,26),(28,6.5,28.5),(17,6.5,28.5),(17,-5,28.5)],
 'right_edge_around_amp':[(28,24,26),(28,6.5,26),(29.5,6.5,26),(29.5,-16,26),(17,-17,26)],
 'mid_side_to_amp_rear':[(28,24,26),(28,6.5,26),(17,6.5,26)],
}
out={}
for name,points in paths.items():
    rows=[]
    for a,b in zip(points,points[1:]):
        s=segment(a,b)
        rows.append({'from':a,'to':b,'head':ov(s,head),'modules':{k:ov(s,v) for k,v in modules.items()}})
    out[name]=rows
(HERE/'side_route_path_probe.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
