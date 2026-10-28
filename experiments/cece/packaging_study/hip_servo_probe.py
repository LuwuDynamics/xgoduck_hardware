"""Hip servo envelope probe against exact Cece body and candidate battery.

This is not a hardware fit certification: dimensions and installed pose beyond the
servo shaft center are inferred from Otto V9 geometry and generic SG90 drawings.
"""
import json,sys,warnings
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]/'cece_mesh_deps'))
import trimesh
warnings.filterwarnings('ignore',category=RuntimeWarning)
HERE=Path(__file__).resolve().parent
BODY=HERE.parent/'parts_adafruit_draft'/'cece_body_square_OLED_DRAFT.stl'
body=trimesh.load(BODY,force='mesh')
def box(ext,center):
 b=trimesh.creation.box(extents=ext);b.apply_translation(center);return b
def ov(a,b):return round(abs(trimesh.boolean.intersection([a,b],engine='manifold').volume),2)
battery=box((56,35,16),(0,-3,-27))
ubec=box((56,21,14),(0,13,-10))
# Shaft x and y inferred from body underside round holes. SG90 body center y
# inferred from SG90's off-center shaft; z is deliberately swept below.
results={'method':'Actual body STL boolean intersection against SG90 rectangular envelopes','dimensions_mm':{'servo_body_box':[12.2,23,22],'battery_clearance':[56,35,16],'ubec_clearance':[56,21,14]},'nominal':{},'z_sweep':{},'limits':['SG90 retailer 23x12.2x29 overall size does not define rectangular case 22mm height. This is an illustrative body box, not a measured item.','Shaft center and y offset inferred from geometry; mounting lugs, turret, horn, cable, connectors, clearance and tolerances not included.','Battery and UBEC placement from existing packaging_study/layout_check.py; not a validated assembly.']}
for side,x in [('left',-25.5),('right',25.5)]:
 s=box((12.2,23,22),(x,-5.5,-24))
 results['nominal'][side]={'center_mm':[x,-5.5,-24],'servo_vs_body_mm3':ov(s,body),'servo_vs_battery_mm3':ov(s,battery),'servo_vs_ubec_mm3':ov(s,ubec)}
for z in [-28,-26,-24,-22,-20]:
 s=box((12.2,23,22),(25.5,-5.5,z));results['z_sweep'][str(z)]={'body':ov(s,body),'battery':ov(s,battery),'ubec':ov(s,ubec)}
(HERE/'hip_servo_probe_results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
