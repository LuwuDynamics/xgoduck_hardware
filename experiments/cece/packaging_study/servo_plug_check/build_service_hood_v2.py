"""V2 one-piece upper JST-SH hood with 1.2mm more front cable clearance."""
import json
from pathlib import Path
import FreeCAD as App,Part,Mesh
V=App.Vector;O=Path(__file__).resolve().parent;P=O.parent
src=P/'speaker_pod/cece_head_with_speaker_mount_CANDIDATE.stl'
m=Mesh.Mesh(str(src));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);head=Part.makeSolid(s.Shells[0])
# Top JST service channel centered (14.3,13), 9x8mm cable envelope.
# Add 2mm walls and continue the roof channel rearward above the vertically
# mounted ESP board, so the cable can bend after the 10mm straight section
# and return into the head cavity. The antenna at x=0 remains separate.
outer=Part.makeBox(13,25.2,13,V(7.8,5.8,27))
inner=Part.makeBox(9,21.2,11,V(9.8,7.8,27))
hood=head.fuse(outer).cut(inner).removeSplitter()
assert hood.isValid(), 'invalid BRep'
assert len(hood.Solids)==1,'hood not one printable solid'
service=Part.makeBox(9,8,10,V(9.8,7.8,22.423))
assert hood.common(service).Volume<.01,'service space blocked'
# Retain original centered antenna as a distinct print part.
antm=Mesh.Mesh(str(P.parent/'parts_adafruit_draft/Cece_Antenna_DRAFT.stl'));a=Part.Shape();a.makeShapeFromMesh(antm.Topology,0.01);ant=Part.makeSolid(a.Shells[0]);ant.translate(V(0,0,27))
assert hood.common(ant).Volume<.01,'antenna clash'
doc=App.newDocument('Cece_Vertical_Driver_Service_Hood_V2');ob=doc.addObject('PartDesign::Feature','HeadWithCableHoodV2');ob.Shape=hood;doc.recompute();doc.saveAs(str(O/'Cece_Vertical_Driver_Service_Hood_V2_CANDIDATE.FCStd'))
Mesh.export([ob],str(O/'Cece_head_vertical_driver_hood_V2_CANDIDATE.stl'))
report={'status':'candidate only; electrical connectors and actual plug dimensions not physically verified','source_head':str(src),'outer_hood_bounds_mm':[[7.8,5.8,27],[20.8,31,40]],'inner_channel_bounds_mm':[[9.8,7.8,27],[18.8,29,38]],'head_height_increase_mm':10,'service_overlap_mm3':hood.common(service).Volume,'antenna_overlap_mm3':hood.common(ant).Volume,'valid':hood.isValid(),'solid_count':len(hood.Solids),'limits':['V2 opens 1.2mm more space in front for driver center Y=11.8mm; connector and cable shapes remain provisional.','Hood wall and roof are nominally 2mm; print strength and water/impact protection untested.','Confirm antenna, head/body joining and screw access with whole-assembly CAD and physical trial.']}
(O/'hood_v2_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
