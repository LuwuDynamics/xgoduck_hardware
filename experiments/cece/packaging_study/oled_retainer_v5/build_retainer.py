"""Prototype screw mounting for the Adafruit 4741 and decorative heart frame.

Uses the official PCB mounting-hole pitch. This is CAD-only and still requires
actual board/screw fit, printed pilot pull-out and display service testing.
"""
from pathlib import Path
import json
import numpy as np
import trimesh

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BODY_SRC=ROOT/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl'
FRAME_SRC=ROOT/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl'

def cyl(radius,y0,y1,x,z):
    m=trimesh.creation.cylinder(radius=radius,height=y1-y0,sections=64)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
    m.apply_translation((x,(y0+y1)/2,z))
    return m
def union(parts):return trimesh.boolean.union(parts,engine='manifold')
def cut(mesh,tools):return trimesh.boolean.difference([mesh]+tools,engine='manifold')
def export(name,m):
    p=HERE/name
    if not m.is_watertight or len(m.split())!=1 or not m.is_winding_consistent:raise ValueError(f'{name}: invalid mesh')
    m.export(p)
    back=trimesh.load(p,force='mesh')
    if not back.is_watertight or len(back.split())!=1 or not back.is_winding_consistent:raise ValueError(f'{name}: bad STL roundtrip')
    return {'file':name,'watertight':True,'one_component':True,'volume_mm3':round(m.volume,3),'bounds_mm':np.round(m.bounds,3).tolist()}

body=trimesh.load(BODY_SRC,force='mesh')
frame=trimesh.load(FRAME_SRC,force='mesh')
# PCB installed X/Z pitch = 41.91 / 30.48 mm. Boss starts at Y=-38.4,
# just behind the official PCB's rear Y=-38.545 face, with 0.145mm nominal gap.
pcb_holes=[(x,z) for x in (-20.955,20.955) for z in (-34.24,-3.76)]
body=union([body]+[cyl(2.6,-38.4,-31.0,x,z) for x,z in pcb_holes])
body=cut(body,[cyl(0.9,-39.1,-31.0,x,z) for x,z in pcb_holes])
# Frame screw axes lie outside the PCB at the widest part of the heart.
frame_holes=[(-26.5,-10),(26.5,-10)]
body=union([body]+[cyl(2.7,-34.3,-29.0,x,z) for x,z in frame_holes])
body=cut(body,[cyl(0.9,-34.7,-29.0,x,z) for x,z in frame_holes])
frame=cut(frame,[cyl(1.15,-44.0,-34.3,x,z) for x,z in frame_holes])

body_result=export('Cece_Body_4741_OLED_ScrewPosts_V5_CANDIDATE.stl',body)
frame_result=export('Cece_Heart_Frame_4741_Screwed_V4_CANDIDATE.stl',frame)
report={'status':'candidate printed screw geometry; actual board/fasteners unverified',
        'source_body':str(BODY_SRC.relative_to(ROOT)),'source_frame':str(FRAME_SRC.relative_to(ROOT)),
        'pcb_hole_centres_xz_mm':pcb_holes,'frame_hole_centres_xz_mm':frame_holes,
        'pcb_post_diameter_mm':5.2,'pcb_pilot_diameter_mm':1.8,
        'frame_post_diameter_mm':5.4,'frame_pilot_diameter_mm':1.8,
        'frame_clearance_diameter_mm':2.3,'frame_counterbore_diameter_depth_mm':None,
        'nominal_pcb_back_to_post_gap_mm':0.145,
        'body':body_result,'frame':frame_result,
        'limits':['Official STEP hole pitch used; delivered OLED variation and header housing still need a dry fit.',
                  '0.145mm nominal rear PCB gap may need a thin insulating shim; do not clamp or bend the board.',
                  'M2 screw lengths, pilot grip, head clearance, frame strength and service order need physical checks.',
                  'The rear header channel from V4 remains, but actual keyed connector/wiring are unverified.']}
(HERE/'mesh_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
