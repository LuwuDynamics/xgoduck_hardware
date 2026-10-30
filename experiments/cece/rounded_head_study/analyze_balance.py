"""Compare solid-plastic mass and neutral support using existing measured sole polygons.

Assumed camera mass is a sensitivity case, not a product specification.
"""
import json, sys
from pathlib import Path
import FreeCAD as App
HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent/'balance_study'
sys.path.insert(0,str(BALANCE))
from latest_balance import static_case

baseline=json.loads((BALANCE/'latest_balance_results.json').read_text())
doc=App.openDocument(str(HERE/'Cece_Rounded_Head_Camera_Study.FCStd'))
replaced={'body','head','face','antenna','speaker_pod','speaker_grille'}
rows=[{'name':p['name'],'mass_g':p['solid_PLA_mass_g'],'center_mm':p['center_mm']}
      for p in baseline['printed_parts'] if p['name'] not in replaced]
for name in ('Body','Rounded_Head_Study','Rear_Cover_Study','Antenna'):
    s=doc.getObject(name).Shape
    if len(s.Solids)!=1: raise ValueError(f'{name} must be one solid')
    s=s.Solids[0]; c=s.CenterOfMass
    rows.append({'name':name,'mass_g':s.Volume*.00124,'center_mm':[c.x,c.y,c.z]})
hardware=baseline['included_hardware']
support=baseline['support_polygons_xy_mm']; floor=baseline['floor_z_mm']
base=static_case(rows,hardware,support,floor,5)
extra=[{'name':'speaker_sensitivity','mass_g':12,'center_mm':[0,32.5,17]},
       {'name':'camera_sensitivity_not_measured','mass_g':10,'center_mm':[0,-29,38]}]
tested=static_case(rows,hardware+extra,support,floor,5)
report={'status':'SOLID PLA MASS SENSITIVITY ONLY - concept head, not finished design',
 'removed_original_parts':sorted(replaced),'new_parts':rows[-4:],
 'without_camera_or_speaker':base,'with_12g_speaker_and_hypothetical_10g_camera':tested,
 'limitations':['Camera and speaker weights are sensitivity assumptions, not measured components',
  'Missing other boards, wires, fasteners, speaker mounts, printer supports and plastic retention features',
  'All printed geometry assumed fully solid PLA at 1.24 g/cm3, not a slicer output',
  'Stationary level floor only; dynamic gait and servo torque are not calculated']}
(HERE/'balance_sensitivity.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
App.closeDocument(doc.Name)
