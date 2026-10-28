"""Probe conservative Adafruit 4741 mated connector volumes against Cece plastics."""
from pathlib import Path
import json
import FreeCAD as App, Part, Mesh

V=App.Vector
ROOT=Path(__file__).resolve().parent

def mesh_solid(path):
    m=Mesh.Mesh(str(path)); s=Part.Shape(); s.makeShapeFromMesh(m.Topology,0.01)
    return Part.makeSolid(s.Shells[0])

def box(size,center):
    x,y,z=size; cx,cy,cz=center
    return Part.makeBox(x,y,z,V(cx-x/2,cy-y/2,cz-z/2))

def overlap(a,b):
    return round(a.common(b).Volume,3)

body=mesh_solid(ROOT/'charger_cassette'/'cece_body_with_charger_posts_CANDIDATE.stl')
body_v4=mesh_solid(ROOT/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
frame=mesh_solid(ROOT/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl')
head=mesh_solid(ROOT/'speaker_pod'/'cece_head_with_speaker_mount_CANDIDATE.stl')
oled=Part.read(str(ROOT/'reference'/'adafruit_4741.step'))
rot=App.Rotation(V(1,1,1),-120)
oled.Placement=App.Placement(V(0,-38.4,-19)-rot.multVec(V(17.78,18.415,1.715)),rot)
bb=oled.BoundBox
result={'oled_world_bbox':[[bb.XMin,bb.YMin,bb.ZMin],[bb.XMax,bb.YMax,bb.ZMax]],'subsolids':[],'probes':{}}
for i,s in enumerate(oled.Solids):
    b=s.BoundBox
    result['subsolids'].append({'i':i,'bounds':[[round(b.XMin,3),round(b.YMin,3),round(b.ZMin,3)],[round(b.XMax,3),round(b.YMax,3),round(b.ZMax,3)]],'volume':round(s.Volume,3)})
# Right-angle 1x8 header/housing idea: PTH row world X about 20.96,
# world Z around -17.7. Check several rear and left-facing housing pockets.
for yy in [-37,-35,-33,-31,-29,-27,-25]:
    candidate=box((11,4,21),(16,yy,-17.7))
    result['probes'][f'right_angle_header_housing_y{yy}']={
        'body':overlap(candidate,body),'frame':overlap(candidate,frame),
        'head':overlap(candidate,head),'oled':overlap(candidate,oled)}
for name,candidate in {
    'top_sh_plug_8x6x14':box((8,6,14),(0,-35,1)),
    'top_sh_wire_8x6x14':box((8,6,14),(0,-33,12)),
    'bottom_sh_plug_8x6x14':box((8,6,14),(0,-35,-39)),
    'rear_pth_housing_5x17x22':box((5,17,22),(20.96,-26,-17.7)),
}.items():
    result['probes'][name]={
        'body':overlap(candidate,body),'frame':overlap(candidate,frame),
        'head':overlap(candidate,head),'oled':overlap(candidate,oled)}
for name,candidate in {
    'v4_rear_pth_housing':box((5,17,22),(20.96,-26,-17.7)),
    'v4_wire_bend_left':box((6,3,4),(17,-15,-9)),
    'v4_wire_rise':box((4,4,18),(15,-15,1)),
}.items():
    hip=box((12.2,23,22),(25.5,-5.5,-24))
    ubec=box((21,56,14),(0,0,-8))
    battery=box((35,56,16),(0,3,-24))
    result['probes'][name]={
        'body_v4':overlap(candidate,body_v4),'frame':overlap(candidate,frame),
        'head':overlap(candidate,head),'oled':overlap(candidate,oled),
        'right_hip':overlap(candidate,hip),'ubec':overlap(candidate,ubec),
        'battery':overlap(candidate,battery)}
(ROOT/'oled_connector_probe_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'bbox':result['oled_world_bbox'],'solids':len(oled.Solids),'probes':result['probes']},indent=2))
