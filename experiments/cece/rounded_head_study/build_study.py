"""Cece rounded head / camera feasibility study. Not a printable release.

Run with FreeCAD 1.1 bundled Python. Uses the existing electronic geometry
and makes an intentionally provisional shell around it. No source CAD is
overwritten. All dimensions are mm in the original Cece coordinates.
"""
import json
from pathlib import Path
import FreeCAD as App
import Part, Mesh

V=App.Vector
HERE=Path(__file__).resolve().parent
CECE=HERE.parent
SOURCE=CECE/'packaging_study'/'Cece_Electronics_Packaging_Study.FCStd'
OUT=HERE/'Cece_Rounded_Head_Camera_Study.FCStd'
doc0=App.openDocument(str(SOURCE))
doc=App.newDocument('Cece_Rounded_Head_Camera_Study')

def rounded_prism(x0,y0,z0,dx,dy,dz,r):
    s=Part.makeBox(dx,dy,dz,V(x0,y0,z0))
    edges=[e for e in s.Edges if abs(e.Length-dy)<1e-7 and abs(e.Vertexes[0].Point.y-e.Vertexes[-1].Point.y)>dy-1e-7]
    return s.makeFillet(r,edges)
def box(dx,dy,dz,x,y,z):
    return Part.makeBox(dx,dy,dz,V(x-dx/2,y-dy/2,z-dz/2))
def add(name,shape,color,transparency=0):
    o=doc.addObject('PartDesign::Feature',name); o.Shape=shape
    if App.GuiUp:
        o.ViewObject.ShapeColor=color; o.ViewObject.Transparency=transparency
    return o
def overlap(a,b):
    if not a.BoundBox.intersect(b.BoundBox): return 0.0
    return a.common(b).Volume

# An 84 x 79 x 55 head, 1.6 mm shell walls. Back is a removable separate plate;
# opening the bottom is provisional, with attachment and routing undecided.
outer=rounded_prism(-42,-40,0,84,77.4,55,10)
inner=rounded_prism(-40.4,-38.4,-5,80.8,76.8,58.4,8.4)
shell=outer.cut(inner)
for x in (-13,13):
    shell=shell.cut(Part.makeCylinder(8.7,5,V(x,-41,14.5),V(0,1,0)))
# Concept-only assumed lens location. Camera's exact lens offset remains unknown.
shell=shell.cut(Part.makeCylinder(4,5,V(0,-41,38),V(0,1,0)))
# Little 3.2 mm smile LED passages, individually replaceable.
for x,z in [(-8,5.8),(-4,4.8),(0,4.4),(4,4.8),(8,5.8)]:
    shell=shell.cut(Part.makeCylinder(1.6,5,V(x,-41,z),V(0,1,0)))
# A nominal peg hole for the existing decorative antenna; retention unproven.
shell=shell.cut(Part.makeCylinder(1.65,4,V(0,0,53),V(0,0,1)))
# Four side screw tongues match the existing separate body-joint candidate.
# Wider braces connect the tongues to this larger head's side walls.
for sx in (-1,1):
    for sy in (-1,1):
        y=sy*22.5
        tongue=box(5.7,7,13.5,sx*29.35,y,-6.25)
        brace=box(15.5,7,7,sx*34.25,y,3.5)
        shell=shell.fuse(tongue).fuse(brace)
        x0=27.0 if sx>0 else -32.3
        shell=shell.cut(Part.makeCylinder(1.25,5.3,V(x0,y,-8),V(1,0,0)))
# Four small rear-cover posts with ribs into the side wall. They are trial
# printed pilots, not evidence of screw pull-out strength or fit.
for sx in (-1,1):
    for z in (10,45):
        x=sx*36
        post=Part.makeCylinder(3,7.4,V(x,30,z),V(0,1,0))
        rib=box(6,7.4,5,sx*39,33.7,z)
        shell=shell.fuse(post).fuse(rib)
        shell=shell.cut(Part.makeCylinder(.8,7.6,V(x,30,z),V(0,1,0)))
shell=shell.removeSplitter()
rear=rounded_prism(-42,37.4,0,84,1.6,55,10)
for x in (-36,36):
    for z in (10,45):
        rear=rear.cut(Part.makeCylinder(1.1,3,V(x,37,z),V(0,1,0)))
# Candidate grille pattern above existing speaker envelope. Avoids unmodeled lid fasteners.
for x in range(-10,11,5):
    for z in range(7,28,5):
        if x*x+(z-17)**2 <= 120:
            rear=rear.cut(Part.makeCylinder(1.3,4,V(x,37, z),V(0,1,0)))
rear=rear.removeSplitter()

# The nominal Sense stack is 21 x 17.8 x 15, with 1 mm reserve on every side.
# Its lens and flexible lead are not represented by this rectangular placeholder.
camera=box(23,17,19.8,0,-29,38)
camera_lens=Part.makeCylinder(3.5,5,V(0,-41,38),V(0,1,0))

module_names=['Battery_Clearance','UBEC_Clearance','OLED_Adafruit4741_Official_CAD',
 'OLED_Rear_Header_Housing_Envelope','OLED_Wire_Bend_Envelope','OLED_Wire_Rise_Envelope',
 'HC_SR04_PCB','HC_SR04_Left_Can','HC_SR04_Right_Can','Speaker_COM21311_Clearance',
 'PiicoDev_Driver_Official_Partial_STEP','PiicoDev_Upper_JST_Service_Envelope',
 'PiicoDev_Lower_USB_Service_Envelope','ESP32_C3_Board_Envelope','DFR0954_Amp_Envelope',
 'INMP441_Breakout_Envelope','Left_Hip_SG90_Proxy','Right_Hip_SG90_Proxy',
 'Left_Ankle_SG90_Proxy','Right_Ankle_SG90_Proxy']+[f'SG90_Mated_Plug_{i}_Proxy' for i in range(1,5)]
plastic_names=['Body','Heart_Frame_V3','Antenna','Left_Arm','Right_Arm','Left_Leg','Right_Leg',
 'Left_Foot','Right_Foot','Left_Washer','Right_Washer','Charger_Tray','Charger_Bezel']
items={name:doc0.getObject(name).Shape.copy() for name in module_names+plastic_names}
# Move the 28 mm speaker envelope forward into the new back wall. Its actual
# terminals, fastening and wire route remain unmodeled.
items['Speaker_COM21311_Clearance'].translate(V(0,-12.2,0))
# Swap in the separately checked candidate with four screw clearances.
body_stl=CECE/'packaging_study'/'head_body_joint'/'Cece_body_V4_four_screw_joint_CANDIDATE.stl'
mesh=Mesh.Mesh(str(body_stl)); bs=Part.Shape(); bs.makeShapeFromMesh(mesh.Topology,0.01)
items['Body']=Part.makeSolid(bs.Shells[0])
# Reposition the original antenna so its peg sits in the new roof aperture.
items['Antenna'].translate(V(0,0,26.5))
colors={'Body':(.84,.9,.95),'Heart_Frame_V3':(.92,.30,.48),
        'Left_Foot':(.34,.53,.72),'Right_Foot':(.34,.53,.72)}
add('Rounded_Head_Study',shell,(.90,.94,.98),40)
add('Rear_Cover_Study',rear,(.80,.88,.94),20)
add('Camera_Stack_Clearance_Provisional',camera,(.3,.8,.5),30)
add('Camera_Lens_Corridor_Provisional',camera_lens,(.2,.65,.35),40)
for name,shape in items.items():
    is_module=name in module_names
    add(name,shape,colors.get(name,(.6,.75,.86) if not is_module else (.87,.68,.3)),65 if is_module else 0)
doc.recompute(); doc.saveAs(str(OUT))

report={'status':'FEASIBILITY STUDY ONLY: attachments, mounting, wiring, print and walking not validated',
 'dimensions_mm':{'head_outer_width':84,'head_depth_including_cover':79,'head_height':55,'wall':1.6},
 'camera':{'manufacturer_stack_mm':[21,17.8,15], 'envelope_xyz_mm':[23,17,19.8],
   'center_xyz_mm':[0,-29,38],'lens_opening_diameter_mm':8,
   'warning':'The lens position, ribbon shape, USB/antenna and mating cable clearances are assumptions.'},
 'source':'../packaging_study/Cece_Electronics_Packaging_Study.FCStd',
 'shell_valid':shell.isValid(),'shell_solid_count':len(shell.Solids),
 'cover_valid':rear.isValid(),'cover_solid_count':len(rear.Solids),
 'shell_volume_mm3':round(shell.Volume,2),'cover_volume_mm3':round(rear.Volume,2),
 'camera_clashes_mm3':{},'shell_clashes_mm3':{},'rear_cover_clashes_mm3':{},'speaker_clashes_mm3':{},
 'limits':['Head/body tongues and braces are new; printed pilots, tool access and joint strength have not been verified',
  'Head is a spatial study; no board retainers',
  'Rear cover M2 screw pilot geometry is untested; no speaker support, wire channels, switch, connector geometry or strain relief',
  'Camera lens position, connector, lens focus, PCB stack and antenna dimensions need exact selected variant',
  'Relocated antenna peg has no positive retainer; fit and pull-out untested',
  'Charger cassette remains exposed; revised body and charger cover are not yet designed',
  'Servo horns, hip drive and actual fasteners remain unverified',
  '1.6 mm walls have not been load or impact tested',
  'No print orientation, strength, walking, servo torque or full assembly verified']}
for name,shape in items.items():
    for label,probe in [('camera_clashes_mm3',camera),('shell_clashes_mm3',shell),('rear_cover_clashes_mm3',rear)]:
        try:
            value=overlap(probe,shape)
            if value>0.01: report[label][name]=round(value,3)
        except Exception as exc: report[label][name]='CHECK FAILED: '+str(exc)
report['camera_vs_shell_mm3']=round(overlap(camera,shell),4)
report['camera_vs_cover_mm3']=round(overlap(camera,rear),4)
report['lens_corridor_vs_shell_mm3']=round(overlap(camera_lens,shell),4)
report['head_vs_cover_mm3']=round(overlap(shell,rear),4)
speaker=items['Speaker_COM21311_Clearance']
for name in module_names:
    if name=='Speaker_COM21311_Clearance': continue
    value=overlap(speaker,items[name])
    if value>0.01: report['speaker_clashes_mm3'][name]=round(value,3)
report['selected_minimum_gaps_mm']={
 'speaker_to_ESP_envelope':round(speaker.distToShape(items['ESP32_C3_Board_Envelope'])[0],3),
 'camera_to_ultrasonic_PCB':round(camera.distToShape(items['HC_SR04_PCB'])[0],3),
 'camera_to_amp_envelope':round(camera.distToShape(items['DFR0954_Amp_Envelope'])[0],3),
}
report['screw_checks']={'head_body_core_overlaps_mm3':[],'rear_cover_core_overlaps_mm3':[],
                        'rear_tool_vs_components_mm3':[]}
for sx in (-1,1):
    for sy in (-1,1):
        start=27.1 if sx>0 else -35.7
        probe=Part.makeCylinder(1.0,8.6,V(start,sy*22.5,-8),V(1,0,0))
        report['screw_checks']['head_body_core_overlaps_mm3'].append(round(overlap(probe,shell)+overlap(probe,items['Body']),4))
for x in (-36,36):
    for z in (10,45):
        core=Part.makeCylinder(.75,9.0,V(x,30.2,z),V(0,1,0))
        tool=Part.makeCylinder(2.8,18,V(x,39.01,z),V(0,1,0))
        report['screw_checks']['rear_cover_core_overlaps_mm3'].append(round(overlap(core,shell)+overlap(core,rear),4))
        clashes={n:round(overlap(tool,s),4) for n,s in items.items() if n!='Antenna' and overlap(tool,s)>0.01}
        report['screw_checks']['rear_tool_vs_components_mm3'].append(clashes)
(HERE/'camera_fit_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
App.closeDocument(doc.Name); App.closeDocument(doc0.Name)
