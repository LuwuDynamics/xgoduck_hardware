"""FreeCAD exact-solid widened Cece feet; same SG90 ankle V2 bearing/axis."""
from pathlib import Path
import json,sys
import FreeCAD as App, Part, Mesh
V=App.Vector
HERE=Path(__file__).resolve().parent
CECE=HERE.parents[1]
ANKLE=CECE/'ankle_v2'
sys.path.insert(0,str(HERE.parent))
from balance_study import read_binary_stl,polygon_hull,signed_margin_mm

def solid_from_stl(path):
    m=Mesh.Mesh(str(path));s=Part.Shape();s.makeShapeFromMesh(m.Topology,.01)
    if len(s.Shells)!=1:raise ValueError(f'{path}: {len(s.Shells)} shells')
    solid=Part.makeSolid(s.Shells[0]);
    if not solid.isValid():raise ValueError(f'{path}: invalid solid')
    return solid

def extrusion(sign):
    # Extend sole inward by 11 mm: original inner X edge +/-15 -> +/-4.
    pts=[(4,-22),(9,-27),(16,-27),(16,27),(9,27),(4,22)]
    pts=[(sign*x,y) for x,y in pts]
    wire=Part.makePolygon([V(x,y,-89.02) for x,y in pts+[pts[0]]])
    face=Part.Face(wire)
    return face.extrude(V(0,0,5.02))

def circle(r,h,x,y,z):return Part.makeCylinder(r,h,V(x,y,z),V(0,1,0))

def add(doc,name,shape):
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape;return o

doc=App.newDocument('Cece_Wider_Feet_Option')
shapes={};result={'status':'CAD_CANDIDATE_ONLY','modification':'11 mm inward sole flange; 8 mm neutral gap','tested':{}}
for side in ('left','right'):
    sign=-1 if side=='left' else 1
    foot=solid_from_stl(ANKLE/f'Cece_{side}_foot_bearing_v2.stl')
    extended=foot.fuse(extrusion(sign)).removeSplitter()
    if not extended.isValid() or len(extended.Solids)!=1:raise ValueError(f'{side} union not one valid solid')
    shapes[side]=extended
    obj=add(doc,side.title()+'_Foot_Wide',extended)
    Mesh.export([obj],str(HERE/f'Cece_{side}_wide_foot.stl'))
    result['tested'][side]={'valid':extended.isValid(),'solids':len(extended.Solids),'volume_mm3':round(extended.Volume,2),
                            'bounds_mm':[[round(getattr(extended.BoundBox,axis+'Min'),3) for axis in 'XYZ'],
                                         [round(getattr(extended.BoundBox,axis+'Max'),3) for axis in 'XYZ']]}
# Neutral contact and foot-to-foot clearance.
result['neutral_foot_overlap_mm3']=round(shapes['left'].common(shapes['right']).Volume,4)
result['neutral_gap_mm']=round(shapes['right'].BoundBox.XMin-shapes['left'].BoundBox.XMax,3)
# Sweep rotating leg / servo envelopes about the exact ankle axis of each planted foot.
for side in ('left','right'):
    sign=-1 if side=='left' else 1;x=sign*25.5;foot=shapes[side]
    leg=solid_from_stl(ANKLE/f'Cece_{side}_leg_SG90_v2.stl')
    servo=Part.makeBox(12.2,22.5,23,V(x-6.1,-14.75,-73.5))
    turret=circle(6.1,5,x,7.75,-71.5)
    shaft=circle(2.4,8.25,x,12.75,-71.5)
    washer=solid_from_stl(ANKLE/f'Cece_{side}_bearing_washer.stl')
    checks={}
    for angle in range(-45,46,5):
        entry={}
        for label,shape in [('leg',leg),('servo_body',servo),('turret',turret),('shaft',shaft),('washer',washer)]:
            moved=shape.copy();moved.rotate(V(x,0,-71.5),V(0,1,0),angle)
            entry[label]=round(moved.common(foot).Volume,4)
        checks[str(angle)]=entry
    result['tested'][side]['ankle_sweep_intersection_mm3']=checks
# Independent swing-foot check with the other foot held flat. This is NOT a gait.
for side in ('left','right'):
    sign=-1 if side=='left' else 1;x=sign*25.5
    other=shapes['right' if side=='left' else 'left']
    check={}
    for angle in range(-45,46,5):
        moving=shapes[side].copy();moving.rotate(V(x,0,-71.5),V(0,1,0),angle)
        check[str(angle)]=round(moving.common(other).Volume,4)
    result['tested'][side]['swing_foot_vs_opposite_foot_mm3']=check
# Sole polygon from actual exported STL vertices.
polys={};allpoints=[]
for side in ('left','right'):
    m=read_binary_stl(HERE/f'Cece_{side}_wide_foot.stl')
    zmin=min(v[2] for v in m['vertices'])
    pts=[(v[0],v[1]) for v in m['vertices'] if v[2] <= zmin+0.1]
    polys[side]=polygon_hull(pts);allpoints.extend(pts)
result['sole_polygons_xy_mm']={s:[[round(x,2),round(y,2)] for x,y in poly] for s,poly in polys.items()}
result['centered_com_single_foot_margin_mm']={s:round(signed_margin_mm((0,0),poly),3) for s,poly in polys.items()}
result['centered_com_shift_for_5mm_reserve_mm']={s:round(5-signed_margin_mm((0,0),poly),3) for s,poly in polys.items()}
result['limitations']=['11 mm flange is a first-pass geometry proposal; impact/fatigue, print orientation, horn and fastener fit not physically tested.','Foot-to-foot swing collision is tested for single-axis ankle rotation with the other foot fixed, not for an actual combined hip/ankle gait.','Servo body/turret/shaft are published-dimension proxies, not measured purchased hardware.','This foot change improves support but cannot alone validate full robot balance or walking.']
doc.recompute();doc.saveAs(str(HERE/'Cece_Wider_Feet_Option.FCStd'))
(HERE/'wide_foot_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'neutral_gap_mm':result['neutral_gap_mm'],'neutral_overlap':result['neutral_foot_overlap_mm3'],
                  'single_foot_margin':result['centered_com_single_foot_margin_mm'],
                  'swing_max':{s:max(result['tested'][s]['swing_foot_vs_opposite_foot_mm3'].values()) for s in ('left','right')},
                  'ankle_max':{s:max(v for item in result['tested'][s]['ankle_sweep_intersection_mm3'].values() for v in item.values()) for s in ('left','right')}},indent=2))
