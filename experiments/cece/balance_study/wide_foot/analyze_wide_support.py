"""Static shell-only reference with optional widened Cece feet."""
import json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from balance_study import PARTS,read_binary_stl,polygon_hull,signed_margin_mm,DENSITY_G_CM3,G,RESERVE_MM,round_list
rows=[]; soles={};feet=[];ground_levels=[]
for name,path,offset in PARTS:
    if name in ('left_foot','right_foot'):
        path=HERE/f'Cece_{name.split("_")[0]}_wide_foot.stl'
    data=read_binary_stl(path)
    mass=data['volume_mm3']*.001*DENSITY_G_CM3
    center=[data['center_local_mm'][i]+offset[i] for i in range(3)]
    rows.append((name,mass,center))
    if name in ('left_foot','right_foot'):
        floor=min(v[2] for v in data['vertices']);ground_levels.append(floor);points=[(v[0],v[1]) for v in data['vertices'] if v[2]<=floor+.1]
        soles[name]=polygon_hull(points);feet.extend(points)
M=sum(m for _,m,_ in rows);com=[sum(m*c[i] for _,m,c in rows)/M for i in range(3)];ground=min(ground_levels)
h=com[2]-ground
margins={name:signed_margin_mm(com[:2],poly) for name,poly in soles.items()}
report={'status':'SHELL_GEOMETRY_ONLY; FULL_HARDWARE_UNVERIFIED','nominal_solid_PLA_mass_g':round(M,3),'nominal_shell_center_mm':round_list(com),'height_above_floor_mm':round(h,3),'single_foot_signed_margin_mm':{k:round(v,3) for k,v in margins.items()},'lateral_shift_for_5mm_reserve_mm':{k:round(RESERVE_MM-v,3) for k,v in margins.items()},'equivalent_rigid_tilt_deg':{k:round(math.degrees(math.atan2(RESERVE_MM-v,h)),2) for k,v in margins.items()},'dynamic_outward_acceleration_budget_at_5mm_margin_m_s2':round(G*RESERVE_MM/h,3),'both_feet_margin_mm':round(signed_margin_mm(com[:2],polygon_hull(feet)),3),'methods':'CAD source STL exact volumes/centroids at nominal 1.24 g/cm3, documented local-part assembly transforms, true wide-foot sole vertices. Electronics/battery/servos absent.'}
(HERE/'wide_balance_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
