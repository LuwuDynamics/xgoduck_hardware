"""FreeCAD envelope and interference study for Cece electronics.
Run build_oled_window_v3.py first, then this with FreeCAD 1.1 bundled Python.
This is a CAD audit, not an approved layout.
"""
from pathlib import Path
import json,math,hashlib
import FreeCAD as App, Part, Mesh
V=App.Vector
OUT=Path(__file__).resolve().parent
CECE=OUT.parent
PARTS=CECE/'parts_adafruit_draft'
ANKLE=CECE/'ankle_v2'
WIDE=CECE/'balance_study'/'wide_foot'
CASSETTE=OUT/'charger_cassette'
SPEAKER_POD=OUT/'speaker_pod'

def from_stl(path):
    mesh=Mesh.Mesh(str(path));shape=Part.Shape();shape.makeShapeFromMesh(mesh.Topology,0.01)
    if len(shape.Shells)!=1:raise ValueError(f'{path}: expected single shell')
    solid=Part.makeSolid(shape.Shells[0])
    if not solid.isValid() or len(solid.Solids)!=1:raise ValueError(f'{path}: invalid solid')
    return solid

def box(size,center):
    x,y,z=size;cx,cy,cz=center
    return Part.makeBox(x,y,z,V(cx-x/2,cy-y/2,cz-z/2))

def cylinder_y(radius,length,center):
    x,y,z=center
    return Part.makeCylinder(radius,length,V(x,y-length/2,z),V(0,1,0))

def place(shape,xyz):
    a=shape.copy();a.translate(V(*xyz));return a

def add(doc,name,shape):
    obj=doc.addObject('PartDesign::Feature',name);obj.Shape=shape;return obj

def common_volume(a,b):
    aa=a.BoundBox;bb=b.BoundBox
    if aa.XMax<=bb.XMin or bb.XMax<=aa.XMin or aa.YMax<=bb.YMin or bb.YMax<=aa.YMin or aa.ZMax<=bb.ZMin or bb.ZMax<=aa.ZMin:
        return 0.0
    return a.common(b).Volume

body=from_stl(OUT/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
head=from_stl(SPEAKER_POD/'side_route_v3'/'Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl')
frame=from_stl(OUT/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl')
face=from_stl(SPEAKER_POD/'side_route_v3'/'Cece_faceplate_M2_retained_V3_CANDIDATE.stl')
antenna=place(from_stl(PARTS/'Cece_Antenna_DRAFT.stl'),(0,0,27))
left_arm=place(from_stl(PARTS/'Cece_Left_Arm_45_DRAFT.stl'),(-37.2,0,-15))
right_arm=place(from_stl(PARTS/'Cece_Right_Arm_45_DRAFT.stl'),(37.2,0,-15))
plastic={
    'Body':body,'Head':head,'Heart_Frame_V3':frame,'Faceplate':face,
    'Antenna':antenna,'Left_Arm':left_arm,'Right_Arm':right_arm,
    'Left_Leg':from_stl(ANKLE/'Cece_left_leg_SG90_v2.stl'),
    'Right_Leg':from_stl(ANKLE/'Cece_right_leg_SG90_v2.stl'),
    'Left_Foot':from_stl(WIDE/'Cece_left_wide_foot.stl'),
    'Right_Foot':from_stl(WIDE/'Cece_right_wide_foot.stl'),
    'Left_Washer':from_stl(ANKLE/'Cece_left_bearing_washer.stl'),
    'Right_Washer':from_stl(ANKLE/'Cece_right_bearing_washer.stl'),
    'Charger_Tray':from_stl(CASSETTE/'removable_tray.stl'),
    'Charger_Bezel':from_stl(CASSETTE/'retaining_bezel.stl'),
    'Speaker_Pod':from_stl(SPEAKER_POD/'side_route_v3'/'speaker_pod_side_wire_notch_V3_CANDIDATE.stl'),
    'Speaker_Grille':from_stl(SPEAKER_POD/'speaker_retaining_grille.stl'),
}
# Published dimensions with explicit clearances; small-module depths and case
# details remain assumptions. The battery/UBEC are rotated to clear hip cases.
oled=Part.read(str(OUT/'reference'/'adafruit_4741.step'))
oled_rot=App.Rotation(V(1,1,1),-120)
oled.Placement=App.Placement(V(0,-38.4,-19)-oled_rot.multVec(V(17.78,18.415,1.715)),oled_rot)
driver_step=Part.read(str(OUT/'reference'/'piicodev_ce09181.step'))
driver_rot=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90))
driver_step.Placement=App.Placement(V(1,11.8,13)-driver_rot.multVec(V(97.282,-88.046,4.8)),driver_rot)
modules={
 'Battery_Clearance':box((35,56,16),(0,3,-24)),   # actual pack 31x52x12, 35g
 'UBEC_Clearance':box((21,56,14),(2.3,0,-8)),     # actual UBEC 17x50x10, 21g
 'Charger_UC2_Physical_Candidate':box((19.8,39.6,9.5),(0,63.3,-24)), # XH faces body, USB-C faces rear; unpurchased
 'OLED_Adafruit4741_Official_CAD':oled,
 'OLED_Rear_Header_Housing_Envelope':box((5,17,22),(20.96,-26,-17.7)),
 'OLED_Wire_Bend_Envelope':box((6,3,4),(17,-15,-9)),
 'OLED_Wire_Rise_Envelope':box((4,4,18),(15,-15,1)),
 'HC_SR04_PCB':box((45,1.6,20),(0,-18,14.5)),
 'HC_SR04_Left_Can':cylinder_y(8,12,(-13,-27,14.5)),
 'HC_SR04_Right_Can':cylinder_y(8,12,(13,-27,14.5)),
 'Speaker_COM21311_Clearance':cylinder_y(14,7,(0,44.7,17)),
 'PiicoDev_Driver_Official_Partial_STEP':driver_step,
 'PiicoDev_Upper_JST_Service_Envelope':box((9,8,10),(14.3,11.8,27.423)),
 'PiicoDev_Lower_USB_Service_Envelope':box((9,8,10),(-13.708,11.8,-0.51)),
 'ESP32_C3_Board_Envelope':box((28,8,21),(0,24,10)),
 'DFR0954_Amp_Envelope':box((22,22,6),(17,-6,24)),
 'INMP441_Breakout_Envelope':box((16,16,6),(-14,-5,24)),
 'Left_Hip_SG90_Proxy':box((12.2,23,22),(-25.5,-5.5,-24)),
 'Right_Hip_SG90_Proxy':box((12.2,23,22),(25.5,-5.5,-24)),
 'Left_Ankle_SG90_Proxy':box((12.2,22.5,23),(-25.5,-3.5,-62)),
 'Right_Ankle_SG90_Proxy':box((12.2,22.5,23),(25.5,-3.5,-62)),
}
for i,z_offset in enumerate((7.62,2.54,-2.54,-7.62),1):
    modules[f'SG90_Mated_Plug_{i}_Proxy']=box((9.6,18.15,3.2),(.956,-3.425,13+z_offset))
# Within-module contacts are expected; every other part pair must be disjoint.
exempt={frozenset(('HC_SR04_PCB','HC_SR04_Left_Can')),frozenset(('HC_SR04_PCB','HC_SR04_Right_Can'))}
exempt.add(frozenset(('OLED_Wire_Bend_Envelope','OLED_Wire_Rise_Envelope')))
for i in range(1,5):exempt.add(frozenset((f'SG90_Mated_Plug_{i}_Proxy','PiicoDev_Driver_Official_Partial_STEP')))
exempt.add(frozenset(('PiicoDev_Driver_Official_Partial_STEP','PiicoDev_Upper_JST_Service_Envelope')))
exempt.add(frozenset(('PiicoDev_Driver_Official_Partial_STEP','PiicoDev_Lower_USB_Service_Envelope')))
doc=App.newDocument('Cece_Electronics_Packaging_Study')
for n,s in plastic.items():add(doc,n,s)
for n,s in modules.items():add(doc,n,s)
report={'scope':'Exact printed shells, official OLED CAD and published/candidate component envelopes; static neutral pose','status':'NOT FIT VERIFIED: charger port, OLED I2C cable, servo wire bends, mounting, heat and full payload remain incomplete','locations_mm':{},'source_sha256':{},'shell_clashes_mm3':{},'module_clashes_mm3':{},'plastic_clashes_mm3':{},'selected_gaps_mm':{},'frame':{},'cassette':{},'speaker_pod':{},'driver':{},'mass':{},'limits':[]}
for source_path in [
    OUT/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl',
    SPEAKER_POD/'side_route_v3'/'Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl',
    SPEAKER_POD/'side_route_v3'/'Cece_faceplate_M2_retained_V3_CANDIDATE.stl',
    OUT/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl',
    OUT/'reference'/'adafruit_4741.step',
    OUT/'reference'/'piicodev_ce09181.step',
    CASSETTE/'removable_tray.stl',
    SPEAKER_POD/'side_route_v3'/'speaker_pod_side_wire_notch_V3_CANDIDATE.stl',
    WIDE/'Cece_left_wide_foot.stl',WIDE/'Cece_right_wide_foot.stl',
]:
    report['source_sha256'][str(source_path.relative_to(CECE))]=hashlib.sha256(source_path.read_bytes()).hexdigest()
for n,s in modules.items():
    bb=s.BoundBox; report['locations_mm'][n]={'center':[round((bb.XMin+bb.XMax)/2,2),round((bb.YMin+bb.YMax)/2,2),round((bb.ZMin+bb.ZMax)/2,2)],'envelope':[round(bb.XLength,2),round(bb.YLength,2),round(bb.ZLength,2)]}
    for pn,ps in plastic.items():
        v=common_volume(s,ps)
        if v>0.01:report['shell_clashes_mm3'][n+'__'+pn]=round(v,3)
keys=list(modules)
for i,n in enumerate(keys):
    for k in keys[i+1:]:
        if frozenset((n,k)) in exempt:continue
        v=common_volume(modules[n],modules[k])
        if v>0.01:report['module_clashes_mm3'][n+'__'+k]=round(v,3)
for n,k in [
 ('Battery_Clearance','UBEC_Clearance'),
 ('Battery_Clearance','Left_Hip_SG90_Proxy'),
 ('Battery_Clearance','Right_Hip_SG90_Proxy'),
 ('UBEC_Clearance','PiicoDev_Driver_Official_Partial_STEP'),
 ('PiicoDev_Driver_Official_Partial_STEP','ESP32_C3_Board_Envelope'),
 ('SG90_Mated_Plug_1_Proxy','ESP32_C3_Board_Envelope'),
 ('SG90_Mated_Plug_1_Proxy','Head'),
 ('ESP32_C3_Board_Envelope','DFR0954_Amp_Envelope'),
 ('DFR0954_Amp_Envelope','Speaker_COM21311_Clearance'),
]:
    aa=modules[n];bb=modules[k] if k in modules else plastic[k]
    report['selected_gaps_mm'][n+'__'+k]=round(aa.distToShape(bb)[0],3)
plastic_keys=list(plastic)
for i,n in enumerate(plastic_keys):
    for k in plastic_keys[i+1:]:
        v=common_volume(plastic[n],plastic[k])
        if v>0.01:report['plastic_clashes_mm3'][n+'__'+k]=round(v,3)
# Frontal board interference and active-window margin from official CAD.
old_frame=place(from_stl(PARTS/'cece_heart_frame_Adafruit4741_DRAFT.stl'),(0,-37.5,-19))
report['frame']={'old_frame_oled_overlap_mm3':round(common_volume(old_frame,oled),3),'v3_frame_oled_overlap_mm3':round(common_volume(frame,oled),3),'v3_frame_valid':frame.isValid(),'v3_frame_solid_count':len(frame.Solids),'v3_front_wall_nominal_mm':1.35,'active_window_check':json.loads((OUT/'oled_window_v3_results.json').read_text()),'warning':'Real OLED glass position, mounting and cable exit still unverified'}
report['frame']['v4_header_route']=json.loads((OUT/'oled_header_route_v4_mesh_results.json').read_text())
report['frame']['v4_connector_probe']=json.loads((OUT/'oled_connector_probe_results.json').read_text())['probes']
report['cassette']=json.loads((CASSETTE/'mesh_validation.json').read_text())
report['speaker_pod']={'baseline':json.loads((SPEAKER_POD/'mesh_validation.json').read_text()),'side_route_v3':json.loads((SPEAKER_POD/'side_route_v3'/'mesh_validation.json').read_text()),'exact_driver_v3':json.loads((SPEAKER_POD/'side_route_v3'/'exact_driver_check.json').read_text())}
db=driver_step.BoundBox
report['driver']={'orientation':'vertical, servo headers facing front','center_mm':[1,11.8,13],'partial_official_step_bbox_mm':[[round(db.XMin,3),round(db.YMin,3),round(db.ZMin,3)],[round(db.XMax,3),round(db.YMax,3),round(db.ZMax,3)]],'warning':'Official KiCad-derived STEP omits USB-C and JST-SH sockets; selected 10 mm service boxes and four mated servo plug boxes are proxies, actual wire bends unverified'}
# Theoretical solid plastic baseline, NOT FDM slicer/scale mass.
density=1.24
plastic_entries={}
total_mass=0.;sumx=sumy=sumz=0.
for n,s in plastic.items():
    mass=s.Volume/1000*density
    # Mesh-to-BRep conversions can be Compounds even with one valid solid.
    com=s.Solids[0].CenterOfMass
    plastic_entries[n]={'solid_PLA_g':round(mass,3),'com_mm':[round(com.x,3),round(com.y,3),round(com.z,3)]}
    total_mass+=mass;sumx+=mass*com.x;sumy+=mass*com.y;sumz+=mass*com.z
report['mass']['solid_geometry_PLA']={'parts':plastic_entries,'total_g':round(total_mass,3),'com_mm':[round(sumx/total_mass,3),round(sumy/total_mass,3),round(sumz/total_mass,3)],'warning':'Actual print mass requires slicer result or a scale; supports and infill change mass'}
report['mass']['known_purchased_g']={'Dualsky_2S_550mAh':35,'Hobbywing_UBEC_5A':21,'SG90_four':36,'sum':92}
report['mass']['charger_candidate_g']=6
report['mass']['incomplete_g']=['PiicoDev board','OLED module','HC-SR04','ESP32-C3','speaker','microphone breakout','amplifier','LEDs/resistors','switch/protection','wiring/connectors','fasteners','printed retention/mounts']
report['limits']=[
 'Component boxes are not supplier 3D models; some listed PCB heights and exact module variants are unknown.',
 'PiicoDev USB-C and JST-SH sockets are omitted from the official KiCad-derived STEP. Selected 10mm plug service corridors and four servo plug envelopes clear, but actual housings, cable bends, screws, board mounts and service access are not verified.',
 'Battery discharge lead and balance connector envelope not established; LiPo must not be squeezed.',
 'Rotated battery/UBEC leave very little end clearance for their leads despite zero box overlap.',
 'ISDT UC2 is an unpurchased rear-cassette candidate; confirm delivered battery balance lead is XH 2.54 and isolate robot load while charging.',
 'Cassette has post/screw attachment, a nominal rear USB opening and body balance-lead duct, but exact mated plugs, switch mount, cable bend, charger heat and retention are not verified.',
 'Nominal Adafruit CAD active area fits shifted V3 window, but real glass position varies; proposed pocket has only ~1.35 mm front wall.',
 'V4 body gives a zero-clash nominal route for a 1x8 rear through-hole OLED header/housing and wire bundle; exact keyed connector, OLED retainer, cable bend and electrical pinout are still unverified.',
 'Core speaker is 28mm diameter, >4mm thick; 7mm depth allowance is provisional. Mic breakout exact size and mass are unknown.',
 'V3 rear speaker pod has a nominal 12mm side plug passage and a tie saddle, but actual plug dimensions, lead bend into the amplifier, strain relief, acoustic response and real speaker thickness are unverified.',
 'V3 faceplate has two M2 screw-boss candidates; pilot grip, screw length, sensor and LED retention still require physical testing.',
 'SG90 hip/ankle case bodies are proxies inferred from shell openings and retailer overall size; horns, ears and wire exits are not modeled.',
 'Mated SG90 servo plug boxes use a published Futaba-type 14x9.6x2.7mm female housing with additional vertical reserve; exact SG90 plug and wire-bend dimensions remain unknown.',
 'Neutral pose clearance says nothing about head attachment, arm swing, gait, strength, heat or actual printed tolerances.',
]
doc.recompute();doc.saveAs(str(OUT/'Cece_Electronics_Packaging_Study.FCStd'))
(OUT/'packaging_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'shell_clashes':report['shell_clashes_mm3'],'module_clashes':report['module_clashes_mm3'],'plastic_clashes':report['plastic_clashes_mm3'],'solid_PLA_g':report['mass']['solid_geometry_PLA']['total_g']},indent=2))
