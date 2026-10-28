from pathlib import Path
import FreeCAD,Mesh,Part
p=Path(__file__).resolve().parent
for n in ['Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl','Cece_Body_4741_WindowV3_CANDIDATE.stl']:
 m=Mesh.Mesh(str(p/n));s=Part.Shape();s.makeShapeFromMesh(m.Topology,.01)
 solid=Part.makeSolid(s.Shells[0]) if len(s.Shells)==1 else None
 print(n,'facets',m.CountFacets,'components',m.countComponents(),'isSolid',m.isSolid(),'nonManifold',m.hasNonManifolds(),'selfIntersections',m.hasSelfIntersections(),'shells',len(s.Shells),'brepValid',solid.isValid() if solid else None,'solids',len(solid.Solids) if solid else None,flush=True)
