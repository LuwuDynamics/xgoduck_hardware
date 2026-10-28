"""Make a conservative 1x8 rear-header service passage in the Cece body.

This only proves a nominal routing envelope. It does not define a connector BOM
or display mounting. The opening is hidden by the front heart frame.
"""
from pathlib import Path
import json
import trimesh

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'charger_cassette'/'cece_body_with_charger_posts_CANDIDATE.stl'
OUT=ROOT/'Cece_Body_4741_HeaderRouteV4_CANDIDATE.stl'

body=trimesh.load(SOURCE,force='mesh')
# PTH row world X≈20.96, Z≈-17.7. This keeps 0.7 mm around a conservative
# 5×17×22 mm mating housing and its initial rearward egress.
cut=trimesh.creation.box(extents=(6.5,25.25,23.5))
cut.apply_translation((20.96,-29.375,-17.7)) # X17.71..24.21, Y-42..-16.75
candidate=trimesh.boolean.difference([body,cut],engine='manifold')
reloaded=None
if not candidate.is_watertight or len(candidate.split())!=1 or not candidate.is_winding_consistent:
    raise ValueError('V4 body must be one watertight, consistent component')
candidate.export(OUT)
reloaded=trimesh.load(OUT,force='mesh')
if not reloaded.is_watertight or len(reloaded.split())!=1 or not reloaded.is_winding_consistent:
    raise ValueError('V4 STL roundtrip invalid')
report={
 'status':'candidate through-hole OLED header route, exact connector and retention unverified',
 'source':str(SOURCE.relative_to(ROOT)),
 'output':OUT.name,
 'passage_bounds_mm':{'x':[17.71,24.21],'y':[-42,-16.75],'z':[-29.45,-5.95]},
 'nominal_housing_envelope_mm':{'size':[5,17,22],'center':[20.96,-26,-17.7]},
 'watertight':True,'single_component':True,
 'original_volume_mm3':round(body.volume,3),
 'candidate_volume_mm3':round(candidate.volume,3),
 'removed_volume_mm3':round(body.volume-candidate.volume,3),
 'limits':['Exact 1x8 header/housing, orientation key and wiring not selected.','OLED mounting and heart frame retention not tested.','Body strength after cut and physical cable bend need test.'],
}
(ROOT/'oled_header_route_v4_mesh_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
