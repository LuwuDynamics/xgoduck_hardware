"""Fill the identified sole lettering from both inherited Otto feet.
Keep attribution in documentation. Output is not print-orientation aligned.
"""
from pathlib import Path
import trimesh
p=Path(__file__).resolve().parents[1];src=p/'parts';out=p/'parts_adafruit_draft';out.mkdir(exist_ok=True)
for f,side in [('OttoDIY_foot_V9.stl',1),('foot_mirror.stl',-1)]:
 m=trimesh.load(src/f,force='mesh')
 fill=trimesh.creation.box([9.8,55,.52]);fill.apply_translation([side*47.2,0,-88.76])
 m=trimesh.boolean.union([m,fill],engine='manifold')
 if not m.is_watertight or len(m.split())!=1:raise ValueError('invalid '+f)
 check=(abs(m.face_normals[:,2])>.999)&(abs(m.triangles_center[:,2]+88.6)<.03)
 if check.any():raise ValueError('letter depth still exists: '+f)
 m.export(out/('cece_foot_right_clean.stl' if side>0 else 'cece_foot_left_clean.stl'))
 print(f,'cleaned; watertight and 1 component')
