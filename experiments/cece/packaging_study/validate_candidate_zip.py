"""Verify each packaged STL reloads as one printable closed mesh."""
from pathlib import Path
from io import BytesIO
import json,zipfile,trimesh

root=Path(__file__).resolve().parent
archive=root/'Cece_V3_CAD_CANDIDATE_NOT_FINAL_STLs.zip'
results=[]
with zipfile.ZipFile(archive) as z:
    manifest=json.loads(z.read('manifest.json'))
    for item in manifest['parts']:
        data=z.read('STLs/'+item['file'])
        mesh=trimesh.load(BytesIO(data),file_type='stl',force='mesh')
        valid=mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1 and mesh.volume>0
        results.append({'file':item['file'],'valid':bool(valid),'volume_mm3':round(float(mesh.volume),3)})
if not all(x['valid'] for x in results):raise ValueError([x for x in results if not x['valid']])
report={'archive':archive.name,'status':'17 closed one-component STL meshes; no physical fit approval','parts':results}
(root/'candidate_zip_mesh_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'count':len(results),'all_valid':True},indent=2))
