"""Otto original STL visual meshes on a simplified five-joint physics rig.

The STL geometry is used for appearance; simple proxy boxes still determine
mass and collisions. Head yaw is a conceptual added joint, not a printable
servo mount. Original Otto files are not modified.
"""
import argparse, json, struct, os, xml.etree.ElementTree as ET
from pathlib import Path
import otto_head_walk as sim

ROOT=Path(__file__).resolve().parent
ASSET=ROOT/'otto_actual_stl_simulation'/'assets'
ASSET.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'otto_reference'/'3Dprint'

def mirror_stl(source,destination):
    data=source.read_bytes();count=struct.unpack_from('<I',data,80)[0]
    if len(data)!=84+50*count:raise ValueError('Expected binary STL')
    with open(destination,'wb') as f:
        f.write(data[:84])
        for i in range(count):
            v=list(struct.unpack_from('<12fH',data,84+50*i))
            v[0]*=-1
            for j in (3,6,9):v[j]*=-1
            v[6:9],v[9:12]=v[9:12],v[6:9]
            f.write(struct.pack('<12fH',*v))

leg=SOURCE/'OttoDIY_Leg_V9.stl';foot=SOURCE/'OttoDIY_foot_V9.stl'
mirror_stl(leg,ASSET/'leg_mirror.stl');mirror_stl(foot,ASSET/'foot_mirror.stl')
root=ET.fromstring(sim.XML)
root.set('model','Otto STL - corrected head alignment')
# The v09 meshes are saved in the original assembled coordinates: their shared
# torso/head seam is at z=0. Place the yaw pivot at that seam instead of 11 mm
# above it. This aligns the visuals; it does not engineer a real swivel joint.
root.find('.//body[@name="head"]').set('pos','0 0 .039')
assets=ET.Element('asset');root.insert(1,assets)
paths={'otto_body':SOURCE/'OttoDIY_body_V9.stl',
       'otto_head':SOURCE/'OttoDIY_head_V9.stl',
       'otto_leg_l':leg,'otto_leg_r':ASSET/'leg_mirror.stl',
       'otto_foot_l':foot,'otto_foot_r':ASSET/'foot_mirror.stl'}
for name,path in paths.items():
    ET.SubElement(assets,'mesh',name=name,file=str(path.resolve()).replace('\\','/'),scale='.001 .001 .001')
for geom in root.findall('.//worldbody//geom'):
    if geom.get('name')!='floor':
        rgba=geom.get('rgba','0.3 0.3 0.3 1').split();rgba[-1]='0';geom.set('rgba',' '.join(rgba))
for name,asset,pos in [
    ('torso','otto_body','0 0 .039'),('head','otto_head','0 0 0'),
    ('left_leg','otto_leg_l','0 -.024 .039'),('right_leg','otto_leg_r','0 .024 .039'),
    ('left_foot','otto_foot_l','0 -.0345 .079'),('right_foot','otto_foot_r','0 .0345 .079')]:
    body=root.find('.//body[@name="%s"]'%name)
    ET.SubElement(body,'geom',name='visual_'+name,type='mesh',mesh=asset,euler='0 0 90',pos=pos,
                  mass='0',contype='0',conaffinity='0',rgba='.4 .78 .3 1')
sim.XML=ET.tostring(root,encoding='unicode')
sim.OUT=ASSET.parent
# Keep the archived XML portable, while the live simulation uses absolute
# paths from this checkout to avoid depending on the caller's working directory.
portable=ET.fromstring(sim.XML)
for item in portable.findall('./asset/mesh'):
    item.set('file',os.path.relpath(item.get('file'),str(sim.OUT)).replace('\\','/'))
(sim.OUT/'otto_actual_stl_model.xml').write_text(ET.tostring(portable,encoding='unicode'))
cfg={'hz':1.,'hip':30,'ankle':20,'hipsign':-1,'anklesign':1}
p=argparse.ArgumentParser();p.add_argument('--live',action='store_true');p.add_argument('--video',action='store_true');a=p.parse_args()
result,trace=sim.run(cfg,video=a.video,live=a.live)
result['visual_geometry']='Actual OttoDIY v09 STL meshes; two leg and foot meshes mirrored for opposite side'
result['limitations'][0]='Original Otto STL visuals at corrected seam; simplified collision boxes do not test head/body mesh interference'
(sim.OUT/'result.json').write_text(json.dumps(result,indent=2))
(sim.OUT/'trace.json').write_text(json.dumps(trace,indent=2))
print(json.dumps(result,indent=2))
