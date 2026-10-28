"""Generate EXPERIMENTAL decorative and passive-arm Cece revision.
Requires trimesh, numpy and manifold3d. Dimensions are prototypes in mm.
Outputs use original Otto assembly coordinates, not build-plate coordinates.
"""
from pathlib import Path
import json
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'parts'; OUT=ROOT/'parts_passive_arms_draft'; OUT.mkdir(exist_ok=True)

def box(ext,center):
 m=trimesh.creation.box(extents=ext);m.apply_translation(center);return m

def cyl(r,length,center,axis='z'):
 m=trimesh.creation.cylinder(radius=r,height=length,sections=48)
 if axis=='x':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
 m.apply_translation(center);return m

def union(items):return trimesh.boolean.union(items,engine='manifold')
def diff(item,cutters):return trimesh.boolean.difference([item]+cutters,engine='manifold')
def save(name,m):
 if not m.is_watertight or not len(m.faces):raise ValueError(name+' not watertight')
 m.export(OUT/(name+'.stl'))
 return {'name':name,'watertight':m.is_watertight,'components':len(m.split()),'bounds_mm':m.bounds.round(2).tolist()}

body=trimesh.load(SRC/'Cece_Otto_Body_OLED_Window.stl',force='mesh')
head=trimesh.load(SRC/'Cece_Otto_Head_LED_Ports.stl',force='mesh')
letters=trimesh.load(SRC/'Cece_Name_Letters.stl',force='mesh')
# Original geometry contains debossed ottodiy.com: body rear external face and
# head inside ceiling. Fill only each confirmed engraving region, keeping source
# credit in documentation. Fuse slightly beyond nominal surfaces for continuity.
body=union([body,box([39,0.55,7.4],[.8,34.275,-33.05])])
head=union([head,box([44.5,8.2,.55],[-.75,.14,28.225])])
# Name lettering overlaps front wall by 0.14 mm rather than merely touching it.
letters.apply_translation([0,.15,0]); body=union([body,letters])
# Two slotted integral spring pins for movable, non-actuated arms, X axis.
# Peg diameter 3.2, nominal bore 3.7, retention lip 4.2. PLA tolerances and
# fatigue are unknown: this is a printable trial, not an approved snap joint.
pins=[]
for side in [-1,1]:
 base=cyl(3.2,1.3,[side*34.85,0,-15],'x')
 stem=cyl(1.6,5.9,[side*37.75,0,-15],'x')
 lip=cyl(2.1,1.0,[side*40.45,0,-15],'x')
 pin=union([base,stem,lip])
 # split outer 4.3 mm of each pin, leave solid near body for strength
 pin=diff(pin,[box([4.3,.8,5.5],[side*39.15,0,-15])])
 pins.append(pin)
body=union([body]+pins)
# Decorative antenna inserted into a hole in the crown; no electrical role.
head=diff(head,[cyl(1.65,5,[20,15,29.5])])
antenna=union([cyl(1.45,5,[0,0,2.5]),cyl(2.4,1.4,[0,0,5.7]),
               cyl(1.25,12.5,[0,0,12.5]),trimesh.creation.icosphere(subdivisions=3,radius=3).apply_translation([0,0,20])])
# Two identical passive paddles: separate print, each mounted on one side pin.
# They swing in the Y/Z plane; no motor or active gait coupling.
arm=union([box([2.8,11,20],[0,0,-10]),cyl(5.5,2.8,[0,0,0],'x'),
           cyl(5.5,2.8,[0,0,-20],'x')])
arm=diff(arm,[cyl(1.85,5,[0,0,0],'x')])
rows=[save('Cece_Body_Name_Passive_Pin_DRAFT',body),save('Cece_Head_Antenna_DRAFT',head),
      save('Cece_Passive_Arm_x2_DRAFT',arm),save('Cece_Antenna_DRAFT',antenna)]
(OUT/'report.json').write_text(json.dumps({'status':'prototype, not fit validated','parts':rows,
 'notes':['No charger socket cut: connector and 2S balance-charge design not selected',
 'Passive arms may swing by inertia only; not linked to leg servos',
 'Spring pins, mounting strength, servo clearance and antenna attachment need physical testing',
 'Head/body inherited tabs unverified; not a new validated click fit',
 'Markings removed only at two detected locations on head and body']},indent=2))
print(json.dumps(rows,indent=2))
