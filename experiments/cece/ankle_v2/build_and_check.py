"""Create and check SG90 Otto/Cece ankle revision in FreeCAD 1.1.
Run with C:/Program Files/FreeCAD 1.1/bin/python.exe.
"""
from pathlib import Path
import json
import FreeCAD as App, Part, Mesh
V=App.Vector
OUT=Path(__file__).resolve().parent
if (OUT.parent/'xgoduck_project_repo/experiments/cece').exists():
    SRC=OUT.parent/'xgoduck_project_repo/experiments/cece'
elif (OUT.parent/'parts').exists() and (OUT.parent/'parts_adafruit_draft').exists():
    SRC=OUT.parent
else:
    raise RuntimeError('Cannot find Cece source parts next to this design')

def solid_from_stl(path):
    mesh=Mesh.Mesh(str(path));shape=Part.Shape();shape.makeShapeFromMesh(mesh.Topology,0.01)
    if len(shape.Shells)!=1:raise ValueError(f'{path} has {len(shape.Shells)} shells')
    s=Part.makeSolid(shape.Shells[0]);
    if not s.isValid():raise ValueError(f'{path} invalid BRep')
    return s

def cyl(r,length,base,direction):return Part.makeCylinder(r,length,V(*base),V(*direction))

def create_leg(side):
    sign=1 if side=='right' else -1
    path=SRC/'parts'/('OttoDIY_Leg_V9.stl' if sign==1 else 'leg_mirror.stl')
    leg=solid_from_stl(path);x=25.5*sign
    # Enlarge the real servo insertion corridor and pocket, without removing hip features.
    # x clearance .8/side, y .5/side, z .8/side for published SG90 envelope.
    pocket=Part.makeBox(13.8,23.5,32.5,V(x-6.9,-15.25,-82.2))
    leg=leg.cut(pocket)
    if sign==1:
        pegcut=Part.makeBox(10,4.7,10,V(x-5,-22.1,-76.5))
        peg=cyl(2.35,8.05,(x,-24.55,-71.5),(0,1,0))
        collar=cyl(3.8,.5,(x,-18.0,-71.5),(0,1,0))
        pilot=cyl(.8,7.0,(x,-24.6,-71.5),(0,1,0))
    else:
        # Mirroring X changes only handedness, not fore/aft shaft orientation.
        pegcut=Part.makeBox(10,4.7,10,V(x-5,-22.1,-76.5))
        peg=cyl(2.35,8.05,(x,-24.55,-71.5),(0,1,0))
        collar=cyl(3.8,.5,(x,-18.0,-71.5),(0,1,0))
        pilot=cyl(.8,7.0,(x,-24.6,-71.5),(0,1,0))
    leg=leg.cut(pegcut).fuse(peg).fuse(collar).cut(pilot)
    # Two shallow channels keep narrow nylon ties from sliding along the leg.
    # The ties clamp the servo case against the pocket; no ear-hole position is assumed.
    for z in (-54.5,-59.5):
        exterior=Part.makeBox(20,33,2.5,V(x-10,-21,z-1.25))
        interior=Part.makeBox(16.2,28.0,2.7,V(x-8.1,-17.1,z-1.35))
        leg=leg.cut(exterior.cut(interior))
    leg=leg.removeSplitter()
    return leg

def make_washer(x):
    washer=cyl(4.4,1.6,(x,-26.15,-71.5),(0,1,0))
    return washer.cut(cyl(1.1,1.8,(x,-26.25,-71.5),(0,1,0)))

def open_bearing_bores(foot,x):
    """Increase original ~5 mm bearing bores to 5.4 mm for print clearance."""
    negative=cyl(2.7,6.5,(x,-24.5,-71.5),(0,1,0))
    positive=cyl(2.7,6.5,(x,18.0,-71.5),(0,1,0))
    return foot.cut(negative).cut(positive).removeSplitter()

def obj(doc,name,shape,color):
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape;return o

doc=App.newDocument('Cece_SG90_Ankle_V2')
result={'design':'SG90 ankle V2, retained opposite bearing, enlarged servo insertion corridor','published_servo_size_mm':[23,12.2,29], 'servo_proxy_body_xyz_mm':[12.2,22.5,23], 'servo_proxy_body_center_xyz_mm':[25.5,-3.5,-62], 'shaft_direction':'+Y','bearing_diameter_mm':4.7,'foot_bearing_bore_mm':5.4,'pilot_diameter_mm':1.6,'washer_od_mm':8.8,'washer_hole_mm':2.2,'tie_groove_centers_z_mm':[-54.5,-59.5],'tested':{},'limitations':['SG90 shaft, horn and screw dimensions are not published for the exact purchased item.','Washer requires a suitable M2 x 8 pointed screw or equivalent; included screw length/count unconfirmed.','Two narrow nylon cable ties per ankle are used to secure the servo body; fit and tie tension require physical testing.','Servo body box is an approximation to the published overall size; final physical fit still required.','Strength, torque, wiring, gait and balance not tested.']}
for side in ['right','left']:
    sign=1 if side=='right' else -1;x=25.5*sign
    leg=create_leg(side)
    foot=open_bearing_bores(solid_from_stl(SRC/'parts_adafruit_draft'/f'cece_foot_{side}_clean.stl'),x)
    washer=make_washer(x)
    servo=Part.makeBox(12.2,22.5,23,V(x-6.1,-14.75,-73.5))
    turret=cyl(6.1,5,(x,7.75,-71.5),(0,1,0))
    shaft=cyl(2.4,8.25,(x,12.75,-71.5),(0,1,0))
    enlarged_servo=Part.makeBox(13.2,23.5,24,V(x-6.6,-15.25,-74))
    # Loose tie volume to check clearance from the foot, not a molded solid.
    ties=[]
    for z in (-54.5,-59.5):
        outside=Part.makeBox(19,29,2.5,V(x-9.5,-18,z-1.25))
        inside=Part.makeBox(17,27,2.7,V(x-8.5,-17,z-1.35))
        ties.append(outside.cut(inside))
    obj(doc,side.title()+'_Leg_V2',leg,(.96,.59,.21))
    obj(doc,side.title()+'_Foot_Bearing_V2',foot,(.2,.5,.8))
    obj(doc,side.title()+'_Bearing_Washer',washer,(.8,.8,.8))
    o=obj(doc,side.title()+'_SG90_Body_Proxy',servo,(.55,.35,.8));
    o=obj(doc,side.title()+'_Turret_Proxy',turret,(.7,.25,.25));
    o=obj(doc,side.title()+'_Shaft_Proxy',shaft,(.7,.25,.25));
    for index,tie in enumerate(ties,1):obj(doc,side.title()+f'_Tie_Clearance_{index}',tie,(.1,.1,.1))
    cases={'leg_vs_foot':leg.common(foot).Volume,'washer_vs_foot':washer.common(foot).Volume,'servo_body_vs_leg':servo.common(leg).Volume,'enlarged_body_vs_leg':enlarged_servo.common(leg).Volume,'servo_body_vs_foot':servo.common(foot).Volume,'turret_vs_leg':turret.common(leg).Volume,'turret_vs_foot':turret.common(foot).Volume,'shaft_vs_leg':shaft.common(leg).Volume,'shaft_vs_foot':shaft.common(foot).Volume}
    sweep={}
    for angle in range(-45,46,5):
        rot=App.Rotation(V(0,1,0),angle)
        transform=App.Placement(V(x,0,-71.5),rot).multiply(App.Placement(V(-x,0,71.5),App.Rotation()))
        sweep[str(angle)]={}
        for label,shape in [('leg',leg),('servo_body',servo),('turret',turret),('shaft',shaft),('bearing_washer',washer),('tie_1',ties[0]),('tie_2',ties[1])]:
            moved=shape.copy();moved.Placement=transform
            sweep[str(angle)][label+'_vs_foot']=round(moved.common(foot).Volume,5)
    result['tested'][side]={'leg_volume_mm3':leg.Volume,'leg_valid':leg.isValid(),'leg_solids':len(leg.Solids),'foot_valid':foot.isValid(),'foot_solids':len(foot.Solids),'washer_valid':washer.isValid(),'static_overlap_mm3':{k:round(v,5) for k,v in cases.items()},'assembly_sweep_overlap_mm3':sweep}
    Part.export([obj for obj in []],str(OUT/'unused.stl')) if False else None
    Mesh.export([doc.getObject(side.title()+'_Leg_V2')],str(OUT/f'Cece_{side}_leg_SG90_v2.stl'))
    Mesh.export([doc.getObject(side.title()+'_Bearing_Washer')],str(OUT/f'Cece_{side}_bearing_washer.stl'))
    Mesh.export([doc.getObject(side.title()+'_Foot_Bearing_V2')],str(OUT/f'Cece_{side}_foot_bearing_v2.stl'))
for thickness in (0.6,0.8):
    shim=Part.makeBox(thickness,20,18,V(0,0,0))
    name=f'SG90_Shimming_Strip_{str(thickness).replace(".","p")}'
    obj(doc,name,shim,(.8,.8,.8))
    Mesh.export([doc.getObject(name)],str(OUT/f'{name}.stl'))
doc.recompute();doc.saveAs(str(OUT/'Cece_SG90_Ankle_V2.FCStd'))
(OUT/'freecad_fit_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
