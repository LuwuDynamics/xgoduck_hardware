"""Adafruit 4741 1.5in square OLED packaging EXPERIMENT.
Dimensions are published board envelope assumptions; connector orientation,
active window placement, retention, and collision with internals unverified.
"""
from pathlib import Path
import json, shutil
import numpy as np
import trimesh
root=Path(__file__).resolve().parents[1];src=root/'parts_heart_draft';out=root/'parts_adafruit_draft';out.mkdir(exist_ok=True)
def box(size,center):
 m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def save(n,m):
 if not m.is_watertight or len(m.split())!=1:raise ValueError(n+' must be one watertight mesh')
 m.export(out/(n+'.stl'));return {'file':n+'.stl','watertight':True,'components':1,'bounds_mm':m.bounds.round(2).tolist()}
def union(parts):return trimesh.boolean.union(parts,engine='manifold')
def diff(m,others):return trimesh.boolean.difference([m]+others,engine='manifold')
# Original Otto front is the negative-Y wall; body coordinates are millimetres.
body=trimesh.load(src/'Cece_Body_Rounded_DRAFT.stl',force='mesh')
# Open square 30.2 mm window for an approximately 26.86 mm active area.
# Nominal center z=-19 mm is an assumption; panel/board offsets unverified.
body=diff(body,[box([30.2,10,30.2],[0,-33.8,-19])])
# The frame is outside the body and must be removed to access its rear pocket.
# 47.0 x 35.56 mm rotated board envelope plus 0.5 mm on each side; thickness 6.5 mm assumed.
# Board retention, isolation, cable access, glazing and screws not engineered.
back=box([52.5,8,38.8],[0,-1,0]) # y range -5..+3
pocket=box([48.0,6.8,36.56],[0,-.35,0]) # y range -3.75..+3.05
# Draw heart silhouette in X,Z and extrude on outer face of rectangular backing.
t=np.linspace(0,2*np.pi,129)[:-1];x=29*np.sin(t)**3
zraw=13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
z=(zraw-(zraw.max()+zraw.min())/2)*38/(zraw.max()-zraw.min())
# Keep the lower heart sides wide enough around the square screen.
x=np.sign(x)*np.minimum(29,np.abs(x)*(1+1.7*np.clip((-z-3)/12,0,1)))
v=np.vstack([[0.,0.],np.column_stack([x,z])]);tri=np.array([[0,1+i,1+((i+1)%len(t))] for i in range(len(t))])
plate=trimesh.creation.extrude_triangulation(v,tri,height=1.2)
plate.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));plate.apply_translation([0,-4.9,0])
# Keep the backing inside the heart's outline; this is a concept and the
# thin remaining walls, board retention and cable exit need physical design.
mask=trimesh.creation.extrude_triangulation(v,tri,height=20)
mask.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
mask.apply_translation([0,10,0])
back=trimesh.boolean.intersection([back,mask],engine='manifold')
frame=union([back,plate]);frame=diff(frame,[pocket,box([30.2,12,30.2],[0,-2,0])])
# Narrow reinforcing surround joins the lobes and point around the square.
ring=diff(box([34.8,1.2,34.8],[0,-5.5,0]),[box([30.2,4,30.2],[0,-5.5,0])])
frame=union([frame,ring])
rows=[save('cece_body_square_OLED_DRAFT',body),save('cece_heart_frame_Adafruit4741_DRAFT',frame)]
for filename in ['Cece_Head_Centered_Antenna_DRAFT.stl','Cece_Happy_Faceplate_DRAFT.stl','Cece_Antenna_DRAFT.stl','Cece_Left_Arm_45_DRAFT.stl','Cece_Right_Arm_45_DRAFT.stl','Cece_Name_Back_Visual_Overlay.stl']:
 shutil.copy2(src/filename,out/filename)
# With nominal frame translated [0,-37.5,-19], frame y <= -34.5 and body
# front y >= -34.5. Report only volume intersection, not assembly fit.
f=frame.copy();f.apply_translation([0,-37.5,-19]);cross=trimesh.boolean.intersection([body,f],engine='manifold')
report={'status':'concept, NOT final print or fit verified','module':'Adafruit 4741 (rotated 90 degrees)','published_board_xy_mm':[47.0,35.56],'footprint_window_mm':[29.0,26.85],
 'assumptions_mm':{'square_window':30.2,'board_pocket':[48.0,36.56,6.8],'window_center_xyz':[0,-33.8,-19], 'frame_translation':[0,-37.5,-19]},
 'body_frame_intersection_mm3':0 if cross.is_empty else round(abs(float(cross.volume)),6),'parts':rows,
 'unresolved':['Board active area and cable location relative to PCB not validated','No module retainer or frame attachment designed','Rotated PCB mounting holes, STEMMA QT connectors, cable exits and offset glass alignment unverified','servo, battery, charging, wiring and other internal collisions not checked','External frame may conflict with body/head joint or arms']}
(out/'fit_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
