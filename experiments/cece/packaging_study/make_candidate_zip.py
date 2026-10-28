"""Package the current V3 Cece CAD candidate STL inventory with a warning."""
from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
files=[
 'experiments/cece/packaging_study/Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl',
 'experiments/cece/packaging_study/speaker_pod/side_route_v3/Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl',
 'experiments/cece/packaging_study/Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl',
 'experiments/cece/packaging_study/speaker_pod/side_route_v3/Cece_faceplate_M2_retained_V3_CANDIDATE.stl',
 'experiments/cece/parts_adafruit_draft/Cece_Antenna_DRAFT.stl',
 'experiments/cece/parts_adafruit_draft/Cece_Left_Arm_45_DRAFT.stl',
 'experiments/cece/parts_adafruit_draft/Cece_Right_Arm_45_DRAFT.stl',
 'experiments/cece/ankle_v2/Cece_left_leg_SG90_v2.stl',
 'experiments/cece/ankle_v2/Cece_right_leg_SG90_v2.stl',
 'experiments/cece/balance_study/wide_foot/Cece_left_wide_foot.stl',
 'experiments/cece/balance_study/wide_foot/Cece_right_wide_foot.stl',
 'experiments/cece/ankle_v2/Cece_left_bearing_washer.stl',
 'experiments/cece/ankle_v2/Cece_right_bearing_washer.stl',
 'experiments/cece/packaging_study/charger_cassette/removable_tray.stl',
 'experiments/cece/packaging_study/charger_cassette/retaining_bezel.stl',
 'experiments/cece/packaging_study/speaker_pod/side_route_v3/speaker_pod_side_wire_notch_V3_CANDIDATE.stl',
 'experiments/cece/packaging_study/speaker_pod/speaker_retaining_grille.stl',
]
archive=OUT/'Cece_V3_CAD_CANDIDATE_NOT_FINAL_STLs.zip'
manifest=[]
for name in files:
    path=ROOT/name
    if not path.is_file():raise FileNotFoundError(path)
    manifest.append({'file':Path(name).name,'source':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
if len({item['file'] for item in manifest})!=len(manifest):raise ValueError('duplicate STL basename')
read_first=(
 'CECE V3 CAD CANDIDATE — NOT A FINAL WORKING ROBOT PRINT SET\n\n'
 'The exact FreeCAD neutral-pose study reports no modeled solid intersections,\n'
 'but actual SG90 horns, plugs, the display mounting, head/body joint, sensor\n'
 'and LED retention, electrical/charge behavior and walking are NOT verified.\n'
 'Print and test one ankle joint first. Do not install/charge the LiPo in the\n'
 'robot based on this archive alone.\n\n'
 'See experiments/cece/packaging_study/README.md and\n'
 'experiments/cece/packaging_study/ASSEMBLY_JOINT_AUDIT.md in the repository.\n'
 'The body and head derive from OttoDIY v09; see repository attribution/license.\n'
)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('READ_FIRST.txt',read_first)
    z.writestr('manifest.json',json.dumps({'status':'CAD candidate, not physical fit verified','parts':manifest},indent=2))
    for item in manifest:z.write(ROOT/item['source'],'STLs/'+item['file'])
print(json.dumps({'archive':str(archive),'stl_count':len(manifest),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
