"""Exact V4-body right-hip fit coupon: no guessed SG90 spline or screw pattern."""
from pathlib import Path
import json
import FreeCAD as App,Part,Mesh
V=App.Vector;O=Path(__file__).resolve().parent;P=O.parent
source=P/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl'
m=Mesh.Mesh(str(source));s=Part.Shape();s.makeShapeFromMesh(m.Topology,0.01);body=Part.makeSolid(s.Shells[0])
# Crop retains both molded servo-ear pilot bores, output opening, nearby wall
# and sufficient depth to insert a complete servo before committing to a body.
crop=Part.makeBox(24,45,29,V(14,-29,-39)) # x14..38, y-29..16, z-39..-10
coupon=body.common(crop).removeSplitter()
assert coupon.isValid() and len(coupon.Solids)==1,'coupon must be one valid solid'
doc=App.newDocument('Cece_Right_Hip_Fit_Coupon');obj=doc.addObject('PartDesign::Feature','ExactV4HipPocket');obj.Shape=coupon;doc.recompute();doc.saveAs(str(O/'Cece_Right_Hip_Fit_Coupon.FCStd'))
Mesh.export([obj],str(O/'Cece_Right_Hip_Fit_Coupon.stl'))
report={'source':str(source),'crop_bounds_mm':[[14,-29,-39],[38,16,-10]],'coupon_volume_mm3':coupon.Volume,'valid':coupon.isValid(),'solid_count':len(coupon.Solids),'purpose':'Print and fit the purchased SG90, horns, and mounting screws into a small exact slice of the V4 body before full-body printing.'}
(O/'coupon_geometry.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
