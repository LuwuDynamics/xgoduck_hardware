"""Render exact STL sections around the existing right hip/ankle drive pockets."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'cece_mesh_deps'))
import trimesh
HERE=Path(__file__).resolve().parent
leg=trimesh.load(HERE/'Cece_right_leg_SG90_v2.stl',force='mesh')
foot=trimesh.load(HERE.parent/'balance_study/wide_foot/Cece_right_wide_foot.stl',force='mesh')
scale=10; W,H=380,320
def px(x,y):return (int(W/2+(x-25.5)*scale),int(H/2-y*scale))
def render(mesh,normal,offsets,label):
    im=Image.new('RGB',(W*len(offsets),H+46),'white'); draw=ImageDraw.Draw(im)
    for i,off in enumerate(offsets):
        if normal=='z': origin=[0,0,off];n=[0,0,1]
        else: origin=[0,off,0];n=[0,1,0]
        seg=trimesh.intersections.mesh_plane(mesh,n,origin)
        for a,b in seg:
            if normal=='z':a2=px(a[0],a[1]);b2=px(b[0],b[1])
            else:a2=px(a[0],a[2]+71.5);b2=px(b[0],b[2]+71.5)
            draw.line([(a2[0]+i*W,a2[1]),(b2[0]+i*W,b2[1])],fill=(18,62,96),width=2)
        draw.text((i*W+8,8),f'{label}: {normal}={off} mm',fill='black')
        draw.line((i*W+W//2,20,i*W+W//2,H-10),fill=(210,210,210))
        draw.line((i*W+20,H//2,i*W+W-10,H//2),fill=(210,210,210))
    im.save(HERE/f'joint_sections_{label}.png')
render(leg,'z',[-40.5,-41.5,-42.5,-43.5,-44.5,-45.5],'hip_leg')
render(foot,'y',[17,18,19,20,21,22,23,24,25],'ankle_foot')
