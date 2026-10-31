"""Export exact solid-geometry inertia tensors for modeled printed parts."""
from pathlib import Path
import json
import FreeCAD as App
HERE=Path(__file__).resolve().parent
doc=App.openDocument(str(HERE.parent/'no_led_mouth'/'Cece_No_LED_Mouth_Assembly.FCStd'))
names={'body':'Body','rounded_head_study':'Rounded_Head_Study','rear_cover_study':'Rear_Cover_Study',
 'antenna':'Antenna','frame':'Heart_Frame_V3','left_arm':'Left_Arm','right_arm':'Right_Arm',
 'left_leg':'Left_Leg','right_leg':'Right_Leg','left_foot':'Left_Foot','right_foot':'Right_Foot',
 'left_washer':'Left_Washer','right_washer':'Right_Washer',
 'charger_tray':'Charger_Tray','charger_bezel':'Charger_Bezel'}
out={}
for key,name in names.items():
 shape=doc.getObject(name).Shape
 if len(shape.Solids)!=1:raise ValueError(name+' is not a single solid')
 s=shape.Solids[0];M=s.MatrixOfInertia; c=s.CenterOfMass
 out[key]={'volume_mm3':s.Volume,'com_mm':[c.x,c.y,c.z],
   'inertia_mm5':[[M.A11,M.A12,M.A13],[M.A21,M.A22,M.A23],[M.A31,M.A32,M.A33]]}
(HERE/'solid_plastic_mass_properties_cece_current.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
App.closeDocument(doc.Name);print('Exported',len(out),'part inertia tensors')

