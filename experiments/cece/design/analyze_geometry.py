import sys,json
from pathlib import Path
sys.path.insert(0,str(Path.cwd().parent/'cece_mesh_deps'))
import trimesh,numpy as np
p=Path('experiments/cece'); q=p/'parts_adafruit_draft'; r=p/'parts'
parts=[('body',q/'cece_body_square_OLED_DRAFT.stl',[0,0,0]),('head',q/'Cece_Head_Centered_Antenna_DRAFT.stl',[0,0,0]),('face',q/'Cece_Happy_Faceplate_DRAFT.stl',[0,0,0]),('frame',q/'cece_heart_frame_Adafruit4741_DRAFT.stl',[0,-37.5,-19]),('antenna',q/'Cece_Antenna_DRAFT.stl',[0,0,27]),('left_arm',q/'Cece_Left_Arm_45_DRAFT.stl',[-37.2,0,-15]),('right_arm',q/'Cece_Right_Arm_45_DRAFT.stl',[37.2,0,-15]),('leg_left',r/'leg_mirror.stl',[0,0,0]),('leg_right',r/'OttoDIY_Leg_V9.stl',[0,0,0]),('foot_left',q/'cece_foot_left_clean.stl',[0,0,0]),('foot_right',q/'cece_foot_right_clean.stl',[0,0,0])]
rows=[];limits=[]
for n,f,trans in parts:
 m=trimesh.load(f,force='mesh');b=m.bounds+trans;limits.append(b)
 rows.append({'part':n,'watertight':bool(m.is_watertight),'components':len(m.split()),'dimensions_mm':m.extents.round(2).tolist(),'volume_cm3':round(float(abs(m.volume))/1000,3),'solid_PLA_g_at_1_24':round(float(abs(m.volume))*1.24/1000,2)})
B=np.stack(limits);bbox=[B[:,0,:].min(0).tolist(),B[:,1,:].max(0).tolist()]
body=trimesh.load(q/'cece_body_square_OLED_DRAFT.stl',force='mesh');candidates=[]
for orientation in (0,1):
 ext=([53,32,13] if orientation==0 else [32,53,13])
 for x in (-3,0,3):
  for y in (-4,0,4):
   for z in (-8,-14,-20,-26):
    box=trimesh.creation.box(extents=ext);box.apply_translation([x,y,z]);coll=trimesh.boolean.intersection([box,body],engine='manifold');vol=0 if coll.is_empty else abs(float(coll.volume))
    candidates.append({'orientation':orientation,'center':[x,y,z],'overlap_mm3':round(vol,2)})
report={'measurement':'geometry-only static envelopes, not assembly fit or balance validation','parts':rows,'bbox_mm':np.round(bbox,2).tolist(),'bbox_size_mm':np.round(np.array(bbox[1])-np.array(bbox[0]),2).tolist(),'total_100pct_solid_PLA_g':round(sum(x['solid_PLA_g_at_1_24'] for x in rows),2),'density_g_cm3':1.24,'battery_test_box_mm':[53,32,13],'tested_battery_orientations':[0,90],'zero_overlap_positions':[x for x in candidates if x['overlap_mm3']<.01], 'lowest_overlap_candidates':sorted(candidates,key=lambda x:x['overlap_mm3'])[:8], 'limits':['100% solid is a theoretical solid plastic mass; no infill, walls, supports or slicer are modeled','Battery tests intersect only printed body; do not include servo motors, wiring, retention or other electronics','Bounding box is a static nominal pose, not a motion envelope','No centre of mass calculation without item positions, mass and support geometry','Adafruit OLED fit is an untested provisional envelope']}
(q/'geometry_mass_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
