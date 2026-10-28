"""Probe internal head tongues in the current V3 head and V4 body."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;CECE=HERE.parents[1]
sys.path.insert(0,str(HERE.parents[4]/'cece_mesh_deps'))
import trimesh
def load(p):return trimesh.load(p,force='mesh')
def box(s,c):
 m=trimesh.creation.box(extents=s);m.apply_translation(c);return m
def cyl_x(r,x0,x1,y,z):
 return trimesh.creation.cylinder(radius=r,segment=[[x0,y,z],[x1,y,z]],sections=96)
def ov(a,b):return round(abs(float(trimesh.boolean.intersection([a,b],engine='manifold').volume)),3)
head=load(CECE/'packaging_study/speaker_pod/side_route_v3/Cece_head_V2_hood_side_speaker_face_boss_V3_CANDIDATE.stl')
body=load(CECE/'packaging_study/Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl')
modules={
 'hip_right':box((12.2,23,22),(25.5,-5.5,-24)),
 'battery':box((35,56,16),(0,3,-24)),
 'UBEC':box((21,56,14),(2.3,0,-8)),
 'driver_gross':box((52,12.3,25.4),(1,11.8,13)),
 'ESP':box((28,8,21),(0,24,10)),
}
rows=[]
for y in (-26,-24,-22,-20,-18,18,20,22,24,26):
 for x0,x1 in ((25.5,31.5),(26,31),(27,32),(27.5,32.5),(28,33)):
  tongue=box((x1-x0,8,13),((x0+x1)/2,y,-6.5)) # z-13..0
  bridge=box((34-x0,8,7),((34+x0)/2,y,3.5)) # z0..7
  rows.append({'y':y,'tongue_x':[x0,x1],'tongue_body':ov(tongue,body),
               'bridge_head':ov(bridge,head),'bridge_body':ov(bridge,body),
               'tongue_modules':{k:ov(tongue,v) for k,v in modules.items()}})
(HERE/'joint_probe.json').write_text(json.dumps(rows,indent=2))
for r in rows:
 if r['bridge_head']>0 and r['tongue_body']<100:
  print(r)
print('Screw-axis body shell intersections')
for side in (-1,1):
 for y in (-24,24):
  a,b=(30,40) if side>0 else (-40,-30)
  screw=cyl_x(1.6,a,b,y,-8)
  print(side,y,'whole',ov(screw,body))
  slabs=[]
  for x in [30+i*.5 for i in range(20)]:
   q=box((.5,4,4),(side*(x+.25),y,-8))
   v=ov(q,body)
   if v>.001:slabs.append((round(side*(x+.25),2),v))
  print('occupied x slices',slabs)
