"""Provisional Cece adaptation of original Otto v09 meshes.

Creates belly window, head wire holes, LED faceplate with locating rings,
and an OLED retaining frame. Mounts/clearances are prototype dimensions.
"""
import sys,json,os
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

import trimesh

SRC=ROOT.parent/'otto'/'otto_reference'/'3Dprint';OUT=ROOT/'parts_heart_base';OUT.mkdir(exist_ok=True)
def box(size,center):
    a=trimesh.creation.box(extents=size);a.apply_translation(center);return a
def hole(radius,length,center,axis='y'):
    a=trimesh.creation.cylinder(radius=radius,height=length,sections=48)
    if axis=='y':a.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
    a.apply_translation(center);return a
def unite(parts):return trimesh.boolean.union(parts,engine='manifold')
def cut(part,cutters):return trimesh.boolean.difference([part]+cutters,engine='manifold')
def save(name,m):
    if not m.is_watertight or len(m.faces)==0:raise ValueError(name+' is not a closed mesh')
    m.export(OUT/(name+'.stl'));return {'name':name,'volume_mm3':round(float(m.volume),2),'watertight':m.is_watertight}
body=trimesh.load(SRC/'OttoDIY_body_V9.stl',force='mesh');head=trimesh.load(SRC/'OttoDIY_head_V9.stl',force='mesh')
if not body.is_watertight or not head.is_watertight:raise ValueError('Input STL not closed')

# Body is in upstream assembled coordinates; front = negative Y.
# Actual display clear area 25 x 7 mm; clearance 0.6 mm per opening.
body_drills=[box([25.6,9,7.6],[0,-33,-19]),hole(2.5,9,[0,-33,-34])]
body_drills += [hole(1.2,9,[x,-33,-19+z]) for x in (-19.3,19.3) for z in (-9,9)]
body_mod=cut(body,body_drills)
# Candidate support ledges for Pololu #1150 (59 x 32 x 15 mm) in upper torso.
# Attach to existing side walls; yoke ends reach into side walls by ~0.5 mm.
ledges=[box([6.5,34,1.8],[x,0,-22.4]) for x in (-30.75,30.75)]
# Remove AA holder ledges: ordered battery is a 2S LiPo, not an AA holder.
# Battery mount will be designed after checking actual dimensions and wiring.

rows=[save('Cece_Otto_Body_OLED_Window',body_mod)]

# Five scattered laughing mouth LED wire holes and one microphone port in the original head.
# Original two 16.5 mm eye openings accept the removable LED faceplate below.
head_drills=[hole(1.65,10,[x,-31,z]) for x,z in ((-8,4.0),(-4,2.9),(0,2.2),(4,2.9),(8,4.0))]
head_drills.append(hole(1.2,10,[23.5,-31,6]))
# HC-SR04 cans: nominal 16 mm diameter, 26 mm centres; extra clearance for prototype.
head_drills += [hole(8.6,12,[x,-31,14.5]) for x in (-13,13)]
head_drills += [hole(2.6,12,[x,-31,23]) for x in (-25,25)]
head_drills += [hole(.9,9,[x,31,14.5+z]) for x in (-6,-3,0,3,6) for z in (-6,-3,0,3,6)]
head_mod=cut(head,head_drills)
# Rear inner locating rim for candidate 28 mm speaker; retainer is unfinished.
rim=cut(hole(15.2,2,[0,29.4,14.5]),[hole(14.2,4,[0,29.4,14.5])])
head_mod=unite([head_mod,rim])
rows.append(save('Cece_Otto_Head_LED_Ports',head_mod))

# Flat faceplate: outer surface y=-34.4; matching eye hole centres measured
# from the original front mesh. Two shallow sleeves locate in the eye holes.
plate=box([57,2,27],[0,-33.3,14])
locators=[hole(7.8,2.0,[x,-31.3,14.5]) for x in (-13.5,13.5)]
plate=unite([plate]+locators)
# Keep transducer faces unobstructed; LED eyes moved outside the sensor cans.
drills=[hole(8.6,8,[x,-32,14.5]) for x in (-13,13)]
drills += [hole(2.6,8,[x,-32,23]) for x in (-25,25)]
drills += [hole(1.6,8,[x,-33,z]) for x,z in ((-8,4.0),(-4,2.9),(0,2.2),(4,2.9),(8,4.0))]
drills += [hole(1.2,8,[23.5,-33,6])]
plate=cut(plate,drills)
rows.append(save('Cece_LED_Faceplate',plate))

# Display retaining frame, two adhesive attachment pads and side retainers.
# Board envelope 35 x 20 x 4 mm, 0.4 mm side clearance; no reliance on
# unverified PCB hole spacing. Slot fits 35.8 x 20.8 x 4.4 mm.
outer=box([43,6,24],[0,0,0])
slot=box([35.8,4.4,20.8],[0,.9,0])
wire_exit=box([8,7,4],[0,0,-11])
window=box([25.6,10,7.6],[0,0,0])
frame_drills=[hole(.8,8,[x,0,z]) for x in (-19.3,19.3) for z in (-9,9)]
frame=cut(outer,[slot,window,wire_exit]+frame_drills)
rows.append(save('Cece_OLED_Retaining_Frame',frame))
lid=box([43,1.6,24],[0,0,0])
lid=cut(lid,[hole(1.2,4,[x,0,z]) for x in (-19.3,19.3) for z in (-9,9)])
rows.append(save('Cece_OLED_Frame_Rear_Cover',lid))

report={'source':'OttoDIY v09, original STL geometry, https://github.com/Open-Hardware-Leaders/OttoDIY',
        'status':'Prototype, not final fit or walking validated',
        'parts':rows,'dimensions_mm':{'oled_opening':[25.6,7.6],'oled_board_assumed':[35,20,4],
        'eyes_nominal_led_diameter':5,'mouth_nominal_led_diameter':3},
        'unresolved':['HC-SR04 front fit and sensor PCB rear clearance untested; add a retainer',
          'HC-SR04 echo needs 3.3 V level conversion and firmware',
          'Fixed head attachment and clearance are unverified',
          'Body-to-frame screw fit and board connector access not proven',
          '2S 550 mAh Dualsky LiPo holder and servo/wire clearances not designed',
          'Speaker locating rim has no retention clip; head yaw sweep and head wiring unverified',
          'ESP32, amplifier, regulator and switch mounts and wiring not yet designed',
          'Head and OLED installation and joint clearances need physical verification',
          'Static fit, component mass, power and real walking not validated']}
(OUT/'geometry_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
