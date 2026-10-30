"""Add an explicit unpurchased charger and provisional through-hole board.

This is a packaging visualization and targeted interference test, not a
complete electrical design. Existing board and servo shapes include proxies.
"""
from pathlib import Path
import json
import FreeCAD as App,Part
V=App.Vector
HERE=Path(__file__).resolve().parent;CECE=HERE.parent
src=App.openDocument(str(HERE/'Cece_Whole_Robot_Leg_Study.FCStd'))
old=App.openDocument(str(CECE/'packaging_study'/'Cece_Electronics_Packaging_Study.FCStd'))
doc=App.newDocument('Cece_Full_Electronics_Study')
shapes={}
for o in src.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull():shapes[o.Name]=o.Shape.copy()
shapes['Charger_UC2_Unpurchased_Proxy']=old.getObject('Charger_UC2_Physical_Candidate').Shape.copy()
def box(size,center):
 x,y,z=size;cx,cy,cz=center
 return Part.makeBox(x,y,z,V(cx-x/2,cy-y/2,cz-z/2))
# Sized spatial allowance only. Component heights, solder tails, wiring,
# fasteners, and final perfboard positions have not been established.
shapes['Perfboard_Provisional_30x20']=box((30,20,1.6),(0,7,43.3))
shapes['Perfboard_Component_Allowance']=box((32,22,8),(0,7,46.5))
for i,(x,z) in enumerate([(-8,5.8),(-4,4.8),(0,4.4),(4,4.8),(8,5.8)],1):
 shapes[f'LED_{i}_Body_Proxy']=Part.makeCylinder(1.5,4.5,V(x,-40,z),V(0,1,0))
# Output shapes copied from prior joint proxy assumptions, not measured SG90s.
for side,x in [('Left',-25.5),('Right',25.5)]:
 shapes[f'{side}_Hip_Turret_Proxy']=Part.makeCylinder(5.5,4,V(x,0,-39),V(0,0,1))
 shapes[f'{side}_Hip_Output_Shaft_Proxy']=Part.makeCylinder(2,5,V(x,0,-44),V(0,0,1))
 shapes[f'{side}_Ankle_Turret_Proxy']=Part.makeCylinder(6.1,5,V(x,7.75,-71.5),V(0,1,0))
 shapes[f'{side}_Ankle_Output_Shaft_Proxy']=Part.makeCylinder(2.4,8.25,V(x,12.75,-71.5),V(0,1,0))
for name,s in shapes.items():
 o=doc.addObject('PartDesign::Feature',name);o.Shape=s
doc.recompute();doc.saveAs(str(HERE/'Cece_Full_Electronics_Study.FCStd'))
def overlap(a,b):
 if not a.BoundBox.intersect(b.BoundBox):return 0.
 return a.common(b).Volume
targets=[n for n in shapes if n not in ('Perfboard_Provisional_30x20','Perfboard_Component_Allowance') and not n.startswith('LED_')]
report={'status':'SPATIAL PROXIES ONLY; no full assembly, mounts, cable routing or electrical verification',
 'perfboard_mm':[30,20,1.6],'perfboard_assumption':'30 x 20 mm proposed, not measured or purchased',
 'perfboard_component_allowance_mm':[32,22,8],'perfboard_vs_other_mm3':{},
 'component_allowance_vs_other_mm3':{},'charger_vs_other_mm3':{},'led_vs_other_mm3':{},
 'motor_output_vs_printed_mm3':{},
 'limits':['All SG90 shapes are case envelopes; supplied horns and hardware absent',
  'C3, camera, amplifier, microphone, speaker, battery, UBEC, charger and connectors use envelopes or partial CAD',
  'Charger UC2 and camera are unpurchased candidate parts; 2S battery connector not verified',
  'Perfboard dimensions and positions of through-hole resistors, capacitors, switch and wiring are assumptions',
  'USB-C, speaker terminal, display header, servo wires and battery leads are missing or simplified',
  'No retainers or service access for most boards; no full robot gait, strength or physical fit verification']}
for name in targets:
 for label,probe in [('perfboard_vs_other_mm3',shapes['Perfboard_Provisional_30x20']),
                     ('component_allowance_vs_other_mm3',shapes['Perfboard_Component_Allowance'])]:
  val=overlap(probe,shapes[name])
  if val>.01:report[label][name]=round(val,3)
for name in targets:
 if name=='Charger_UC2_Unpurchased_Proxy':continue
 val=overlap(shapes['Charger_UC2_Unpurchased_Proxy'],shapes[name])
 if val>.01:report['charger_vs_other_mm3'][name]=round(val,3)
for i in range(1,6):
 led=shapes[f'LED_{i}_Body_Proxy']
 for name in targets:
  val=overlap(led,shapes[name])
  if val>.01:report['led_vs_other_mm3'][f'LED_{i}__{name}']=round(val,3)
for side in ('Left','Right'):
 for joint in ('Hip','Ankle'):
  for kind in ('Turret','Output_Shaft'):
   key=f'{side}_{joint}_{kind}_Proxy'
   for item in ('Body',f'{side}_Leg',f'{side}_Foot'):
    val=overlap(shapes[key],shapes[item])
    if val>.01:report['motor_output_vs_printed_mm3'][f'{key}__{item}']=round(val,3)
(HERE/'full_electronics_fit_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
App.closeDocument(doc.Name);App.closeDocument(src.Name);App.closeDocument(old.Name)
