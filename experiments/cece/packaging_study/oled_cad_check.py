"""Check the actual manufacturer 4741 CAD against the current Cece body/frame.

Run with FreeCAD 1.1 bundled Python. Coordinates in millimetres.
"""
from pathlib import Path
import json
import FreeCAD as App, Part, Mesh
V=App.Vector
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'parts_adafruit_draft'
def from_stl(p):
    mesh=Mesh.Mesh(str(p));s=Part.Shape();s.makeShapeFromMesh(mesh.Topology,.01)
    return Part.makeSolid(s.Shells[0])
body=from_stl(SRC/'cece_body_square_OLED_DRAFT.stl')
frame=from_stl(SRC/'cece_heart_frame_Adafruit4741_DRAFT.stl')
frame=frame.cut(Part.makeBox(48,1.1,36.56,V(-24,-4.8,-18.28))).removeSplitter()
frame.translate(V(0,-37.5,-19))
oled=Part.read(str(ROOT/'reference'/'adafruit_4741.step'))
# Local OLED XYZ -> assembly world (local Y, local Z, local X): 90-degree
# portrait-to-landscape rotation, with local -Z viewing face at world front -Y.
rotation=App.Rotation(V(1,1,1),-120)
local_center=V(17.78,18.415,1.715)
target_center=V(0,-38.4,-19)
oled.Placement=App.Placement(target_center-rotation.multVec(local_center),rotation)
bb=oled.BoundBox
active_local=V(17.907,22.089,-1.1)
active_world=oled.Placement.multVec(active_local)
window_center=V(0,-38,-19)
window_half=15.1
active_x_min=active_world.x-13.43
active_x_max=active_world.x+13.43
active_z_min=active_world.z-13.43
active_z_max=active_world.z+13.43
result={
 'source':'Adafruit official 4741 3D STEP, see reference/README.md',
 'oled_world_bbox_mm':[[round(bb.XMin,3),round(bb.YMin,3),round(bb.ZMin,3)],[round(bb.XMax,3),round(bb.YMax,3),round(bb.ZMax,3)]],
 'oled_vs_body_mm3':round(oled.common(body).Volume,3),
 'oled_vs_frame_v2_mm3':round(oled.common(frame).Volume,3),
 'active_center_world_mm':[round(active_world.x,3),round(active_world.y,3),round(active_world.z,3)],
 'active_x_bounds_mm':[round(active_x_min,3),round(active_x_max,3)],
 'active_z_bounds_mm':[round(active_z_min,3),round(active_z_max,3)],
 'current_window_x_bounds_mm':[-window_half,window_half],
 'current_window_z_bounds_mm':[-34.1,-3.9],
 'active_area_clipped_right_mm':round(max(0,active_x_max-window_half),3),
 'note':'Current centered 30.2 mm square aperture is offset from the manufacturer CAD active area; real glass position may vary.'
}
(ROOT/'oled_cad_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2),flush=True)
