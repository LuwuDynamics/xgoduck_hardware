"""Scan heart-frame material at potential side screw axes."""
from pathlib import Path
import json,numpy as np,trimesh
HERE=Path(__file__).resolve().parent
frame=trimesh.load(HERE.parent/'Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl',force='mesh')
rows=[]
for x in (24.5,25,25.5,26,26.5,27):
 for z in np.arange(-4,-31,-2):
  c=trimesh.creation.cylinder(radius=1.15,height=10,sections=48)
  c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
  c.apply_translation((x,-39,z))
  q=trimesh.boolean.intersection([frame,c],engine='manifold')
  rows.append({'x':x,'z':float(z),'cut_volume_mm3':round(q.volume,3)})
rows.sort(key=lambda v:v['cut_volume_mm3'],reverse=True)
(HERE/'frame_screw_site_scan.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows[:30],indent=2))
