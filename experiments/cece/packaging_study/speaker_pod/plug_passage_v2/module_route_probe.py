"""Check the widened speaker passage against currently proposed internals."""
from pathlib import Path
import json, sys
import numpy as np

HERE=Path(__file__).resolve().parent
WORKSPACE=HERE.parents[5]
sys.path.insert(0,str(WORKSPACE/'cece_mesh_deps'))
import trimesh

def load(name): return trimesh.load(HERE/name,force='mesh')
def box(size,center):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def segment(radius,p0,p1):
    return trimesh.creation.cylinder(radius=radius,segment=np.array([p0,p1]),sections=64)
def ov(a,b):
    m=trimesh.boolean.intersection([a,b],engine='manifold')
    return round(abs(float(m.volume)),3)

head=load('Cece_head_hood_speaker_plug_passage_V2_CANDIDATE.stl')
pod=load('speaker_pod_tray_plug_passage_V2_CANDIDATE.stl')
modules={
    'ESP32_C3_28x8x21':box((28,8,21),(0,24,10)),
    'Amp_22x22x6':box((22,22,6),(17,-5,24)),
    'Mic_16x16x6':box((16,16,6),(-14,-5,24)),
    'HC_SR04_PCB_45x1p6x20':box((45,1.6,20),(0,-18,14.5)),
    'Battery_35x56x16':box((35,56,16),(0,3,-24)),
    'UBEC_21x56x14':box((21,56,14),(2.3,0,-8)),
}
plug=box((8,16,7),(0,32,17))
# Straight 1mm-radius wire from the speaker opening toward amp's rear edge.
straight_wire=segment(1.0,(0,41.2,17),(0,6,17))
# Trial turn around the right of the ESP. This is only an obstruction check.
turn=[
    segment(1.0,(0,29.5,17),(17,29.5,17)),
    segment(1.0,(17,29.5,17),(17,6,17)),
    segment(1.0,(17,6,17),(17,6,24)),
    segment(1.0,(17,6,24),(17,-5,24)),
]
report={
    'status':'straight fitted-plug path is blocked by provisional ESP32 envelope; no validated lead-to-amp route',
    'plug_8x7x16_center_xyz':[0,32,17],
    'plug_bounds_xyz':[[ -4,24,13.5 ],[4,40,20.5]],
    'plug_vs_head_mm3':ov(plug,head),
    'plug_vs_pod_mm3':ov(plug,pod),
    'plug_vs_modules_mm3':{k:ov(plug,m) for k,m in modules.items()},
    'straight_wire_radius_mm':1,
    'straight_wire_vs_head_mm3':ov(straight_wire,head),
    'straight_wire_vs_modules_mm3':{k:ov(straight_wire,m) for k,m in modules.items()},
    'turn_right_of_ESP_trial_segments_mm3':[
        {'segment':i+1,'head':ov(s,head),'pod':ov(s,pod),
         'modules':{k:v for k,m in modules.items() if (v:=ov(s,m))>0}}
        for i,s in enumerate(turn)
    ],
    'note':'These are conservative rectangular module proxies, not exact installed CAD; route is a candidate obstruction test, not a bend-radius/strain test.'
}
(HERE/'module_route_probe.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
