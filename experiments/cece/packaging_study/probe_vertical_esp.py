"""Probe rear vertical ESP envelope against the speaker-pod head shell."""
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;root=Path(__file__).resolve().parent
m=Mesh.Mesh(str(root/'speaker_pod'/'cece_head_with_speaker_mount_CANDIDATE.stl'))
s=Part.Shape();s.makeShapeFromMesh(m.Topology,.01);head=Part.makeSolid(s.Shells[0])
def box(sz,c):return Part.makeBox(*sz,V(*[c[i]-sz[i]/2 for i in range(3)]))
driver=box((56,30,16),(0,0,8));ubec=box((21,56,14),(0,0,-8))
amp=box((22,22,6),(10,17,24));mic=box((16,16,6),(-14,17,24))
for y in (20,21,22,23):
 for z in (9,10,11):
  esp=box((28,8,21),(0,y,z))
  print(y,z,'head',round(esp.common(head).Volume,3),'driver',round(esp.common(driver).Volume,3),'ubec',round(esp.common(ubec).Volume,3),'amp',round(esp.common(amp).Volume,3),'mic',round(esp.common(mic).Volume,3),flush=True)
