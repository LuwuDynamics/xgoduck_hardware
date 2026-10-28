"""Explore a right-side rear speaker entrance without modifying source files."""
from pathlib import Path
import json, sys, math
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[5]/'cece_mesh_deps'))
import trimesh

def load(path): return trimesh.load(path,force='mesh')
def box(size,center):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def cyl_y(r,y0,y1,x,z):
    return trimesh.creation.cylinder(radius=r,segment=np.array([(x,y0,z),(x,y1,z)]),sections=96)
def seg(r,p0,p1): return trimesh.creation.cylinder(radius=r,segment=np.array([p0,p1]),sections=48)
def ov(a,b): return round(abs(float(trimesh.boolean.intersection([a,b],engine='manifold').volume)),3)

CECE=HERE.parents[2]
head=load(CECE/'packaging_study/servo_plug_check/Cece_head_vertical_driver_hood_CANDIDATE.stl')
pod=load(HERE.parent/'speaker_pod_tray.stl')
esp=box((28,8,21),(0,24,10))
hood=box((13,24,13),(14.3,19,33.5))
mount_pilot=cyl_y(1.25,30,50,23,17)
results=[]
for x,z in [(24,24),(25,25),(26,25),(27,26),(28,26),(28,27),(30,27)]:
    bore=cyl_y(6,24,39.3,x,z)
    plug=box((8,16,7),(x,32,z))
    forward=seg(1,(x,24,z),(x,6,z))
    result={
        'center_xz':[x,z],
        'screw_pilot_to_bore_web_mm':round(math.hypot(x-23,z-17)-6-1.25,3),
        'source_head_material_to_remove_mm3':ov(bore,head),
        'bore_hits_mount_pilot_mm3':ov(bore,mount_pilot),
        'plug_hits_ESP_mm3':ov(plug,esp),
        'plug_hits_hood_outer_envelope_mm3':ov(plug,hood),
        'straight_forward_wire_hits_source_head_mm3':ov(forward,head),
        'bore_hits_pod_mm3':ov(bore,pod),
    }
    results.append(result)
(HERE/'side_route_sweep.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
