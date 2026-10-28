"""Trial Cece right-side speaker feed and screwed faceplate on PiicoDev V2 hood.

This is not a final print release. It uses nominal connector and module boxes.
"""
from __future__ import annotations
import hashlib, json, sys, warnings
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
CECE=HERE.parents[2]
sys.path.insert(0,str(HERE.parents[5]/'cece_mesh_deps'))
import trimesh
warnings.filterwarnings('ignore',category=RuntimeWarning)

SOURCE_HEAD=CECE/'packaging_study/servo_plug_check/Cece_head_vertical_driver_hood_V2_CANDIDATE.stl'
SOURCE_FACE=CECE/'parts_adafruit_draft/Cece_Happy_Faceplate_DRAFT.stl'
SOURCE_POD=HERE.parent/'speaker_pod_tray.stl'
SOURCE_GRILLE=HERE.parent/'speaker_retaining_grille.stl'

def mesh(path):return trimesh.load(path,force='mesh')
def box(size,center):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def ycyl(r,y0,y1,x=0,z=17):
    return trimesh.creation.cylinder(radius=r,segment=np.array([(x,y0,z),(x,y1,z)]),sections=128)
def zcyl(r,z0,z1,x,y):
    return trimesh.creation.cylinder(radius=r,segment=np.array([(x,y,z0),(x,y,z1)]),sections=96)
def seg(r,p0,p1):
    return trimesh.creation.cylinder(radius=r,segment=np.array([p0,p1]),sections=64)
def union(*parts):return trimesh.boolean.union(parts,engine='manifold')
def cut(part,*tools):return trimesh.boolean.difference([part,*tools],engine='manifold')
def ov(a,b):return round(abs(float(trimesh.boolean.intersection([a,b],engine='manifold').volume)),5)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

head0=mesh(SOURCE_HEAD);face0=mesh(SOURCE_FACE);pod0=mesh(SOURCE_POD);grille=mesh(SOURCE_GRILLE)

# Enter rear upper-right shell away from ESP x±14 and from PiicoDev hood x≤20.8.
# Keep about 3.05mm radial web to speaker pod's M3 pilot at (23,17).
speaker_sleeve=ycyl(9,30.0,37.2,28,26)
speaker_bore=ycyl(6,24.0,39.3,28,26)
speaker_key_relief=box((1.4,15.3,3),(34.3,31.65,26))

# Two front head screw bosses outside the HC-SR04 PCB's x±22.5 estimate.
bosses=[ycyl(3,-32.0,-25.0,x,11) for x in (-25.5,25.5)]
pilots=[ycyl(.9,-32.5,-26.0,x,11) for x in (-25.5,25.5)]
head=cut(union(head0,speaker_sleeve,*bosses),speaker_bore,speaker_key_relief,*pilots)

# Faceplate gets M2 through holes and shallow flat-head recesses. Screw shape
# and actual head diameter remain unmeasured; the holes are a print trial.
face_through=[ycyl(1.15,-34.5,-32.0,x,11) for x in (-25.5,25.5)]
face_counterbore=[ycyl(2.0,-34.5,-33.5,x,11) for x in (-25.5,25.5)]
face=cut(face0,*face_through,*face_counterbore)

# An open 3mm cable slot near the speaker upper-right rim accepts bare lead
# after the attached plug has been threaded through the head. It is not a
# through-pod plug channel. Route remains exposed pending a strain relief.
notch=box((10,11.6,3.0),(17,44.6,27)) # x12..22,y38.8..50.4,z25.5..28.5
# A small external lug joins the right rail and provides two through holes for
# a narrow tie. It holds the bare wire near the head entry after the plug has
# passed through the head; it cannot guarantee actual cable strain radius.
tie_lug=box((7,8,9),(30.5,42,17.5)) # x27..34,y38..46,z13..22
tie_holes=[zcyl(1.2,12.8,22.2,31,y) for y in (39.7,44.3)]
pod=cut(union(pod0,tie_lug),notch,*tie_holes)

paths={
    'head':HERE/'Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl',
    'face':HERE/'Cece_faceplate_M2_retained_V3_CANDIDATE.stl',
    'pod':HERE/'speaker_pod_side_wire_notch_V3_CANDIDATE.stl',
}
for k,m in [('head',head),('face',face),('pod',pod)]:m.export(paths[k])
# Reimport exported STL to catch float32 seam defects.
head,face,pod=[mesh(paths[k]) for k in ('head','face','pod')]
for k,m in [('head',head),('face',face),('pod',pod)]:
    assert m.is_watertight and len(m.split(only_watertight=False))==1,(k,'invalid STL')

body=mesh(CECE/'packaging_study/Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
frame=mesh(CECE/'packaging_study/Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl')
charger=mesh(CECE/'packaging_study/charger_cassette/removable_tray.stl')
antenna=mesh(CECE/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl');antenna.apply_translation([0,0,27])
speaker=ycyl(14,41.2,48.2)
esp=box((28,8,21),(0,24,10))
amp=box((22,22,6),(17,-6,24))
mic=box((16,16,6),(-14,-5,24))
sensor=box((45,1.6,20),(0,-18,14.5))
ubec=box((21,56,14),(2.3,0,-8))
battery=box((35,56,16),(0,3,-24))
driver_bbox=box((52,12.3,25.4),(1,11.8,13))
plug=box((8,16,7),(28,32,26))
wire_forward=seg(1,(28,24,26),(28,6.5,26))
wire_external=seg(1,(16,43,27),(28,37.2,26))
tie_probes=[zcyl(1.0,12.8,22.2,31,y) for y in (39.7,44.3)]
mount_screws=[ycyl(1.0,32.3,50.2,x,17) for x in (-23,23)]
face_screws=[ycyl(.75,-34.5,-26.1,x,11) for x in (-25.5,25.5)]

solid_checks={
 'head_body':ov(head,body), 'head_frame':ov(head,frame),
 'face_head':ov(face,head), 'head_antenna':ov(head,antenna),
 'pod_head':ov(pod,head), 'pod_body':ov(pod,body),
 'pod_charger':ov(pod,charger), 'pod_grille':ov(pod,grille),
 'speaker_pod':ov(speaker,pod), 'speaker_grille':ov(speaker,grille),
 'head_ESP':ov(head,esp), 'head_amp':ov(head,amp),
 'head_mic':ov(head,mic), 'head_sensor_PCB':ov(head,sensor),
 'head_UBEC':ov(head,ubec), 'head_battery':ov(head,battery),
 'head_gross_driver_box':ov(head,driver_bbox),
}
module_checks={
 'plug_head':ov(plug,head),'plug_pod':ov(plug,pod),
 'plug_ESP':ov(plug,esp),'plug_hood_gross':ov(plug,box((13,25.2,13),(14.3,18.4,33.5))),
 'wire_forward_head':ov(wire_forward,head),
 'wire_forward_ESP':ov(wire_forward,esp),
 'wire_forward_driver_gross':ov(wire_forward,driver_bbox),
 'wire_forward_amp':ov(wire_forward,amp),
 'wire_external_pod':ov(wire_external,pod),
 'wire_external_head':ov(wire_external,head),
 'cable_tie_holes_vs_pod':[ov(t,pod) for t in tie_probes],
 'speaker_mount_screw_cores_vs_head_pod':[ov(s,head)+ov(s,pod) for s in mount_screws],
 'face_screw_cores_vs_face_head':[ov(s,face)+ov(s,head) for s in face_screws],
}
result={
 'status':'V3 right-side speaker/faceplate retention geometry candidate; actual plug, lead path to amp and screw holding not validated',
 'source_head':str(SOURCE_HEAD),'source_head_sha256':sha(SOURCE_HEAD),
 'side_passage_xyz_mm':[28,None,26],'bore_diameter_mm':12,'sleeve_diameter_mm':18,
 'face_screw_centers_xz_mm':[[-25.5,11],[25.5,11]],
 'face_through_diameter_mm':2.3,'head_pilot_diameter_mm':1.8,
 'face_counterbore_diameter_depth_mm':[4,1],
 'speaker_mount_pilot_web_mm':round(float(np.hypot(28-23,26-17)-6-1.25),3),
 'source_head_vs_added_sleeve_intended_mm3':ov(head0,speaker_sleeve),
 'source_head_vs_face_bosses_intended_mm3':[ov(head0,b) for b in bosses],
 'stls':{k:{'watertight':m.is_watertight,'components':len(m.split(only_watertight=False)),
            'volume_mm3':round(abs(float(m.volume)),3),'bounds_xyz_mm':np.round(m.bounds,3).tolist()}
         for k,m in [('head',head),('face',face),('pod',pod)]},
 'printed_part_and_module_overlaps_mm3':solid_checks,
 'trial_plug_wire_and_screw_probes_mm3':module_checks,
 'limitations':[
  'The actual speaker JST family/plug shape is unspecified; 8x7mm plug is assumed.',
  'Open pod notch routes wire externally; two printed tie holes are a candidate restraint, not a tested strain relief.',
  'A narrow cable tie can go through two reinforced Ø2.4mm pod holes; actual tie/wire size and bending still require a physical check.',
  'Only straight lead forward to y6.5 is checked; path into actual amplifier connector and bend radius remain unknown.',
  'Driver is a conservative gross box, not the partial manufacturer STEP; socket/plug geometry missing.',
  'M2 face screws/counterbores/pilots need physical screw-length and pull-out tests.',
 ]
}
(HERE/'mesh_validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
