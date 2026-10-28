"""Generate EXPERIMENTAL decorative and passive-arm Cece revision.
Requires trimesh, numpy and manifold3d. Dimensions are prototypes in mm.
Outputs use original Otto assembly coordinates, not build-plate coordinates.
"""
from pathlib import Path
import json
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'parts_happy_base'; OUT=ROOT/'parts_happy_draft'; OUT.mkdir(exist_ok=True)

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
letters=trimesh.load(ROOT/'parts'/'Cece_Name_Letters.stl',force='mesh')
# Original geometry contains debossed ottodiy.com: body rear external face and
# head inside ceiling. Fill only each confirmed engraving region, keeping source
# credit in documentation. Fuse slightly beyond nominal surfaces for continuity.
body=union([body,box([39,0.55,7.4],[.8,34.275,-33.05])])
head=union([head,box([44.5,8.2,.55],[-.75,.14,28.225])])
# Taller raised name for tactile/visual contrast. It overlaps the wall.
letters.vertices[:,1]=-34.5 + (letters.vertices[:,1]+34.5)*1.8
letters.apply_translation([0,.15,0])
# Heart below OLED frame, offset from the center wire hole; a shallow
# raised ornament fused to the body, not a separate electronic component.
# Triangle is in local XY, extruded then rotated into the XZ front plane.
heart_tri=trimesh.creation.extrude_triangulation(
 np.array([[8.4,-34.1],[15.6,-34.1],[12.,-38.7]]),
 np.array([[0,1,2]]), height=1.25)
heart_tri.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
heart_tri.apply_translation([0,-34.35,0])
def front_cyl(x,z):
 m=trimesh.creation.cylinder(radius=1.85,height=1.25,sections=48)
 m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
 m.apply_translation([x,-34.975,z]);return m
heart=union([heart_tri,front_cyl(10.25,-33.8),front_cyl(13.75,-33.8)])
body=union([body,letters,heart])
# Visual overlays use these exact shapes; set color in slicer or paint after
# printing, since a single-material STL does not encode color.
letters.export(OUT/'Cece_Name_Visual_Overlay.stl')
heart.export(OUT/'Cece_Heart_Visual_Overlay.stl')
# Round four external vertical corners with a 5 mm radius, using cutters
# only at the extreme corner quadrants. Servo and OLED clearances unverified.
for sx in (-1,1):
 for sy in (-1,1):
  square=box([5,5,39.2],[sx*32,sy*32,-19.5])
  circle=cyl(5,40,[sx*29.5,sy*29.5,-19.5])
  body=diff(body,[diff(square,[circle])])
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
head=diff(head,[cyl(1.65,5,[0,0,29.5])])
antenna=union([cyl(1.45,5,[0,0,2.5]),cyl(2.4,1.4,[0,0,5.7]),
               cyl(1.25,12.5,[0,0,12.5]),trimesh.creation.icosphere(subdivisions=3,radius=3).apply_translation([0,0,20])])
# Distinct left and right arms, 45-degree outward shoulder-to-hand axis.
# Unactuated, attached to same X-axis spring pegs; larger round hands.
def ball(r,center):
 m=trimesh.creation.icosphere(subdivisions=3,radius=r);m.apply_translation(center);return m

def arm_for(side):
 # Construct an axis-aligned cylinder between two diagonal endpoints.
 p1=np.array([side*2.8,0.,-2.8]);p2=np.array([side*17.,0.,-17.])
 seg=trimesh.creation.cylinder(radius=3.8,segment=np.array([p1,p2]),sections=48)
 arm=union([cyl(5.5,2.8,[0,0,0],'x'),seg,ball(4.0,p1),ball(6.0,p2)])
 # Slot entire peg entry path; physical snap fit remains untested.
 return diff(arm,[cyl(1.85,30,[side*5,0,0],'x'), cyl(2.25,9,[side*7.1,0,0],'x')])
left=arm_for(-1);right=arm_for(1)
rows=[save('Cece_Body_Rounded_DRAFT',body),save('Cece_Head_Centered_Antenna_DRAFT',head),
      save('Cece_Left_Arm_45_DRAFT',left),save('Cece_Right_Arm_45_DRAFT',right),save('Cece_Antenna_DRAFT',antenna)]
face=trimesh.load(SRC/'Cece_LED_Faceplate.stl',force='mesh')
rows.append(save('Cece_Happy_Faceplate_DRAFT',face))
(OUT/'report.json').write_text(json.dumps({'status':'prototype, not fit validated','parts':rows,
 'notes':['No charger socket cut: connector and 2S balance-charge design not selected',
 'Passive arms may swing by inertia only; not linked to leg servos',
 'Spring pins, mounting strength, servo clearance and antenna attachment need physical testing',
 'Head/body inherited tabs unverified; not a new validated click fit',
 'Markings removed only at two detected locations on head and body']},indent=2))
print(json.dumps(rows,indent=2))
