from pathlib import Path
import FreeCAD as App,Part
V=App.Vector;p=Path('xgoduck_project_repo/experiments/cece/packaging_study/reference/piicodev_ce09181.step');s=Part.read(str(p))
ub=Part.makeBox(21,56,14,V(-10.5,-28,-15))
def ov(a,b):return a.common(b).Volume
for x,z in [(0,9),(-1,8),(-2,8),(-1,7)]:
 r=App.Rotation(V(1,0,0),90).multiply(App.Rotation(V(0,0,1),-90));a=s.copy();a.Placement=App.Placement(V(x,13,z)-r.multVec(V(97.282,-88.046,4.8)),r);print(x,z,'UBEC',ov(a,ub))
