from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;P=Path('xgoduck_project_repo/experiments/cece/packaging_study');m=Mesh.Mesh(str(P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl'));h=Part.Shape();h.makeShapeFromMesh(m.Topology,0.01);h=Part.makeSolid(h.Shells[0]);src=Part.read(str(P/'reference/piicodev_ce09181.step'));r=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90))
for y in [10,11,12,13,14]:
 d=src.copy();d.Placement=App.Placement(V(-1,y,13)-r.multVec(V(97.282,-88.046,4.8)),r);i=d.common(h);print(y,i.Volume)
