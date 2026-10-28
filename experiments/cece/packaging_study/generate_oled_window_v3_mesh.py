"""Generate manifold Cece body/heart STLs with the corrected 4741 window.

Run with Python containing numpy, trimesh and manifold3d. The body starts
from the pre-window Cece shell; the frame is recreated from its parametric
heart silhouette, avoiding a seam patch in a narrow front wall.
"""
from pathlib import Path
import json
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
CECE=ROOT.parent
def box(size,center):
    m=trimesh.creation.box(extents=size);m.apply_translation(center);return m
def union(parts):return trimesh.boolean.union(parts,engine='manifold')
def diff(m,tools):return trimesh.boolean.difference([m]+tools,engine='manifold')
def save(name,m):
    pieces=m.split()
    if not m.is_watertight or len(pieces)!=1 or not m.is_winding_consistent:raise ValueError(f'{name}: bad mesh')
    m.export(ROOT/name)
    reloaded=trimesh.load(ROOT/name,force='mesh')
    if not reloaded.is_watertight or len(reloaded.split())!=1 or not reloaded.is_winding_consistent:raise ValueError(f'{name}: STL roundtrip invalid')
    return {'file':name,'watertight':True,'single_component':True,'winding_consistent':True,'triangles':len(m.faces),'volume_mm3':round(m.volume,3)}

body0=trimesh.load(CECE/'parts_heart_draft'/'Cece_Body_Rounded_DRAFT.stl',force='mesh')
body=diff(body0,[box((30.2,10,30.2),(3.1,-33.8,-19))])
body_result=save('Cece_Body_4741_WindowV3_CANDIDATE.stl',body)

back=box((52.5,8,38.8),(0,-1,0))
t=np.linspace(0,2*np.pi,129)[:-1]
x=29*np.sin(t)**3
zraw=13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
z=(zraw-(zraw.max()+zraw.min())/2)*38/(zraw.max()-zraw.min())
x=np.sign(x)*np.minimum(29,np.abs(x)*(1+1.7*np.clip((-z-3)/12,0,1)))
verts=np.vstack([[0.,0.],np.column_stack([x,z])])
faces=np.array([[0,1+i,1+((i+1)%len(t))] for i in range(len(t))])
plate=trimesh.creation.extrude_triangulation(verts,faces,height=1.2)
plate.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
plate.apply_translation([0,-4.9,0])
mask=trimesh.creation.extrude_triangulation(verts,faces,height=20)
mask.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
mask.apply_translation([0,10,0])
back=trimesh.boolean.intersection([back,mask],engine='manifold')
ring=diff(box((34.8,1.2,34.8),(3.1,-5.5,0)),[box((30.2,4,30.2),(3.1,-5.5,0))])
frame=union([back,plate,ring])
frame=diff(frame,[box((48,7.85,36.56),(0,-.875,0)),box((30.2,12,30.2),(3.1,-2,0))])
frame.apply_translation([0,-37.5,-19])
frame_result=save('Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl',frame)
report={'method':'Manifold3D mesh Booleans; heart shape from original Cece Adafruit concept generator','window_center_x_mm':3.1,'window_size_mm':[30.2,30.2],'body':body_result,'frame':frame_result,'limits':['Candidate geometry only; mounts and real OLED glass location not signed off.']}
(ROOT/'oled_window_v3_mesh_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
