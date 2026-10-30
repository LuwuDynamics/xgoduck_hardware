"""Make a more recognizable heart fascia while retaining the existing OLED fit.

The output is a CAD candidate, not a validated attachment or a full print set.
Uses the existing V3 frame's backing geometry and exact display opening.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent; CECE=HERE.parent
sys.path.insert(0,str(HERE.parents[3]/'cece_mesh_deps'))
import trimesh
source=CECE/'packaging_study/Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl'
old=trimesh.load(source,force='mesh')
def bezier(a,b,c,d,n=40):
 t=np.linspace(0,1,n,endpoint=False)[:,None]
 return (1-t)**3*np.asarray(a)+3*(1-t)**2*t*np.asarray(b)+3*(1-t)*t*t*np.asarray(c)+t**3*np.asarray(d)

# Points are x,z in assembled robot mm. The shallow central notch clears the
# near-square display; the lower tip extends below the torso without touching
# either leg. The result is front-facing decoration, not a load-bearing mount.
right=np.vstack([
 bezier((0,-2),(7,.8),(20,1.8),(29,-2)),
 bezier((29,-2),(38,-6),(38,-16),(33,-25)),
 bezier((33,-25),(27,-34),(13,-44),(0,-49)),
 np.array([[0.,-49.]])])
left=right[-2:0:-1].copy();left[:,0]*=-1
outline=np.vstack([right,left])
signed=.5*np.sum(outline[:,0]*np.roll(outline[:,1],-1)-np.roll(outline[:,0],-1)*outline[:,1])
vertices=np.vstack([[0.,-19.],outline]);n=len(outline)
faces=np.array([[0,1+i,1+(i+1)%n] if signed>0 else [0,1+(i+1)%n,1+i] for i in range(n)])
plate=trimesh.creation.extrude_triangulation(vertices,faces,height=1.8)
plate.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));plate.apply_translation([0,-42.8,0])
window=trimesh.creation.box(extents=[30.2,16,30.2]);window.apply_translation([3.1,-40,-19])
combined=trimesh.boolean.union([old,plate],engine='manifold')
new=trimesh.boolean.difference([combined,window],engine='manifold')
dest=HERE/'Cece_Heart_Frame_V4_TEST_ONLY.stl';new.export(dest);new=trimesh.load(dest,force='mesh')
if not new.is_watertight or not new.is_winding_consistent or len(new.split(only_watertight=False))!=1:
 raise ValueError('Heart STL did not round-trip as a watertight single mesh')

def inside(q,poly):
 x,y=q;hit=False
 for a,b in zip(poly,np.roll(poly,-1,axis=0)):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:hit=not hit
 return hit
def edge_distance(q,poly):
 a=poly;b=np.roll(poly,-1,axis=0);v=b-a;u=np.clip(np.sum((q-a)*v,axis=1)/np.sum(v*v,axis=1),0,1)
 return float(np.linalg.norm(a+u[:,None]*v-q,axis=1).min())
xx=np.linspace(-12,18.2,101);zz=np.linspace(-34.1,-3.9,101)
border=np.vstack([np.c_[xx,np.full_like(xx,-34.1)],np.c_[xx,np.full_like(xx,-3.9)],
                  np.c_[np.full_like(zz,-12),zz],np.c_[np.full_like(zz,18.2),zz]])
window_inside=all(inside(p,outline) for p in border)
margin=min(edge_distance(p,outline) for p in border)
if not window_inside:raise ValueError('Heart silhouette intersects the display opening')
report={'status':'TEST ONLY: recognizable heart shape, exact screen CAD and mounting still require confirmation',
 'source_frame_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'new_frame_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
 'silhouette_bounds_xz_mm':[[round(float(outline[:,0].min()),3),round(float(outline[:,1].min()),3)],
                             [round(float(outline[:,0].max()),3),round(float(outline[:,1].max()),3)]],
 'window_bounds_xz_mm':[[-12,-34.1],[18.2,-3.9]],
 'window_border_min_distance_to_outer_heart_mm':round(margin,3),
 'frame_bounds_xyz_mm':new.bounds.round(3).tolist(),
 'frame_volume_mm3':round(float(new.volume),3),
 'old_frame_volume_mm3':round(float(old.volume),3),
 'solid_PLA_mass_change_g':round(float((new.volume-old.volume)*.00124),3),
 'watertight':bool(new.is_watertight),'component_count':len(new.split(only_watertight=False)),
 'limitations':['Not a validated OLED retainer or body fastener',
   'Bottom heart tip extends below the body and may need impact/print support testing',
   'Printer tolerance, real screen dimensions and connector access remain unverified',
   'Changes to mass require the balance and gait assumptions to be revisited']}
(HERE/'heart_geometry_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

# Quick face-on silhouette check, explicitly distinct from a final robot render.
im=Image.new('RGB',(820,740),'#f3f7fa');d=ImageDraw.Draw(im)
def xy(p):return (int(410+p[0]*8),int(145-p[1]*8))
d.polygon([xy(p) for p in outline],fill='#e65178',outline='#a7284b',width=4)
d.rounded_rectangle((xy((-12,-3.9)),xy((18.2,-34.1))),radius=8,fill='#173049',outline='white',width=3)
font=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',26)
d.text((25,25),'Heart fascia geometry - CAD candidate',font=font,fill='#253a4b')
im.save(HERE/'heart_shape_preview.png')
print(json.dumps(report,indent=2),flush=True)
