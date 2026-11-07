"""Calculate 100%-solid material estimates directly from XGO-Duck STL meshes.

Run with FreeCAD's Python. This is not a slicer estimate; supports, waste,
filament variability and non-solid infill are not included.
"""
import FreeCAD, Mesh, os, json
from pathlib import Path

root=Path(__file__).resolve().parent
folder=root.parents[1]/'structure'
out=root/'xgoduck_print_inventory'
out.mkdir(exist_ok=True)
exclude={'2x_tire_support.stl','4x_tire.stl','4x_tire_axis.stl'}
rows=[]
for path in sorted(folder.iterdir(),key=lambda p:p.name.lower()):
    if path.suffix.lower()!='.stl' or path.name.lower() in exclude:continue
    mesh=Mesh.Mesh(str(path))
    quantity=2 if path.name.lower().startswith('2x_') else (4 if path.name.lower().startswith('4x_') else 1)
    material='TPU' if path.stem.lower().endswith('_tpu') else 'PLA'
    density=1.21 if material=='TPU' else 1.24
    volume=abs(float(mesh.Volume))
    mass=volume*density/1000
    rows.append({'file':path.name,'quantity':quantity,'material':material,'volume_mm3':round(volume,3),
                 'watertight':bool(mesh.isSolid()),'unit_weight_g':round(mass,3),'total_weight_g':round(mass*quantity,3)})
summary={'upstream_commit':'106186e1beda690c28f485a754538d6f41b5d025',
         'assumption':'100% solid; PLA 1.24 g/cm3, TPU 1.21 g/cm3; no supports, waste or electrical parts',
         'quantity_basis':'2x_ prefix = two, other files one; verify against assembly, especially 2x_hip_yaw2rol.STL',
         'rows':rows,'total_g':round(sum(r['total_weight_g'] for r in rows),2),
         'total_pla_g':round(sum(r['total_weight_g'] for r in rows if r['material']=='PLA'),2),
         'total_tpu_g':round(sum(r['total_weight_g'] for r in rows if r['material']=='TPU'),2)}
(out/'weight_estimates.json').write_text(json.dumps(summary,indent=2))
lines=['# XGO-Duck printed-parts weight estimate','',summary['assumption']+'.',
       'STL volume × assumed density. This is a fully solid material estimate, not a slicer result.',
       'Actual infill, wall thickness, density, supports and waste change the result.','',
       '| STL part | Quantity | Material | Each (g) | Total (g) | Mesh closed? |',
       '|---|---:|---|---:|---:|---|']
for r in rows:
    lines.append('| '+r['file']+' | '+str(r['quantity'])+' | '+r['material']+' | %.2f | %.2f | %s |'%(r['unit_weight_g'],r['total_weight_g'],'yes' if r['watertight'] else '**no**'))
lines+=['| **TOTAL** | **%d** | | | **%.2f** | |'%(sum(r['quantity'] for r in rows),summary['total_g']),
        '', 'PLA: %.2f g; TPU: %.2f g.'%(summary['total_pla_g'],summary['total_tpu_g']),
        '', 'Optional roller skate pieces are excluded. Two flexible foot soles and both mouth parts are TPU according to upstream filenames.',
        '', '**Quantity conflict:** the upstream folder contains `2x_hip_yaw2rol.STL` but its print inventory refers to `hip_yaw2rol.STL` with quantity one. This report follows the actual filename prefix (two); confirm against the illustrated assembly guide before printing.',
        '', 'Source: https://github.com/LuwuDynamics/xgoduck_hardware/tree/106186e1beda690c28f485a754538d6f41b5d025/structure',
        'Upstream inventory: https://github.com/LuwuDynamics/xgoduck_hardware/blob/106186e1beda690c28f485a754538d6f41b5d025/docs/PRINTING.md']
(out/'PRINT_WEIGHT_TABLE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
