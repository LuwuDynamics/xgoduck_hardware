"""Diagnose STL manifold export around the Cece body display cut."""
from pathlib import Path
import tempfile
import trimesh
root=Path(__file__).resolve().parent.parent
src=trimesh.load(root/'parts_heart_draft'/'Cece_Body_Rounded_DRAFT.stl',force='mesh')
for x in (2.9,3.0,3.1,3.3):
 for y,size_y in ((-33.8,10),(-36,8),(-36.5,7),(-35.5,7)):
  tool=trimesh.creation.box(extents=(30.2,size_y,30.2));tool.apply_translation((x,y,-19))
  out=trimesh.boolean.difference([src,tool],engine='manifold')
  with tempfile.NamedTemporaryFile(suffix='.stl',delete=False) as f:p=Path(f.name)
  out.export(p)
  roundtrip=trimesh.load(p,force='mesh');p.unlink()
  print(x,y,size_y,'memory',out.is_watertight,'roundtrip',roundtrip.is_watertight,'components',len(roundtrip.split()),flush=True)
