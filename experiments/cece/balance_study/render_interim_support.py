"""Draw the actual STL sole polygons and included-item COM scenario as SVG."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input', type=Path, default=HERE/'interim_relocated_results.json')
parser.add_argument('--output', type=Path, default=HERE/'interim_relocated_support.svg')
args = parser.parse_args()
data = json.loads(args.input.read_text(encoding='utf-8'))
W, H = 960, 565
scale = 3.05
panels = ({'baseline': 240, 'wider': 720}
          if len(data['cases']) == 2 else {next(iter(data['cases'])): 480})
cy = 285

def xy(x, y, cx):
    return cx + scale*x, cy - scale*y

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<rect width="100%" height="100%" fill="#ffffff"/>',
    '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#172033}.title{font-size:24px;font-weight:700}.head{font-size:19px;font-weight:700}.label{font-size:14px}.small{font-size:12px;fill:#48566b}</style>',
    '<text x="30" y="40" class="title">Cece: ideal flat-foot support in neutral pose</text>',
    '<text x="30" y="66" class="label">Actual STL sole outlines; COM includes nominal solid shells and the hardware masses listed in the scenario.</text>',
]
for variant, cx in panels.items():
    case = data['cases'][variant]
    label = 'Existing feet' if variant == 'baseline' else 'Wider candidate feet'
    parts.append(f'<text x="{cx}" y="106" class="head" text-anchor="middle">{label}</text>')
    parts.append(f'<line x1="{cx}" y1="145" x2="{cx}" y2="399" stroke="#b9c3d3" stroke-width="1" stroke-dasharray="5 5"/>')
    parts.append(f'<line x1="{cx-195}" y1="{cy}" x2="{cx+195}" y2="{cy}" stroke="#b9c3d3" stroke-width="1" stroke-dasharray="5 5"/>')
    for side in ('left_foot','right_foot'):
        polygon = case['support_polygon_xy_mm'][side]
        points = ' '.join(f'{xy(x,y,cx)[0]:.2f},{xy(x,y,cx)[1]:.2f}' for x,y in polygon)
        fill = '#bbd8f0' if side == 'left_foot' else '#d2e9c9'
        parts.append(f'<polygon points="{points}" fill="{fill}" stroke="#23374f" stroke-width="2"/>')
        footx = -36 if side == 'left_foot' else 36
        fx, fy = xy(footx, 0, cx)
        parts.append(f'<text x="{fx:.1f}" y="{fy+5:.1f}" class="label" text-anchor="middle">{side.split("_")[0]}</text>')
    com = case['included_combined_center_mm']
    ox, oy = xy(com[0], com[1], cx)
    parts.append(f'<circle cx="{ox:.2f}" cy="{oy:.2f}" r="7" fill="#d14646" stroke="white" stroke-width="2"/>')
    parts.append(f'<text x="{cx}" y="421" class="label" text-anchor="middle">COM above floor: {case["combined_center_height_above_floor_mm"]:.1f} mm</text>')
    left = case['lateral_COM_shift_for_5mm_single_foot_margin_mm']['left_foot']
    right = case['lateral_COM_shift_for_5mm_single_foot_margin_mm']['right_foot']
    parts.append(f'<text x="{cx}" y="447" class="label" text-anchor="middle">Shift COM for 5 mm one-foot reserve:</text>')
    parts.append(f'<text x="{cx}" y="470" class="label" text-anchor="middle">{left:.1f} mm left / {right:.1f} mm right</text>')
    parts.append(f'<text x="{cx}" y="493" class="small" text-anchor="middle">One-foot margins: {case["signed_support_margin_mm"]["left_foot"]:.1f} / {case["signed_support_margin_mm"]["right_foot"]:.1f} mm</text>')

warning = ('Known component box collision in this layout.'
           if any(v>0 for v in data['candidate_box_pair_overlap_mm3'].values())
           else 'Candidate boxes clear; charger, other payload and print masses remain unverified.')
parts += [
    '<circle cx="35" cy="526" r="7" fill="#d14646" stroke="white" stroke-width="2"/>',
    '<text x="52" y="531" class="small">Included-item COM projection; outside either sole in this pose</text>',
    f'<text x="950" y="551" text-anchor="end" class="small">Interim only: {warning}</text>',
    '</svg>',
]
args.output.write_text('\n'.join(parts),encoding='utf-8')
print(args.output)
