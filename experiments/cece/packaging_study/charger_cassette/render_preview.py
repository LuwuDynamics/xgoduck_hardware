"""Simple orthographic illustration of the exact exported candidate STLs."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "cece_mesh_deps"))
import trimesh

body = trimesh.load(HERE / "cece_body_with_charger_posts_CANDIDATE.stl", force="mesh")
tray = trimesh.load(HERE / "removable_tray.stl", force="mesh")
lid = trimesh.load(HERE / "retaining_bezel.stl", force="mesh")
name = trimesh.load(HERE.parents[1] / "parts_adafruit_draft" / "Cece_Name_Back_Visual_Overlay.stl", force="mesh")

img = Image.new("RGB", (950, 760), "#f7fafc")
draw = ImageDraw.Draw(img)
title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
label_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
draw.text((25, 18), "Cece UC2 front-to-back charger cassette", font=title_font, fill="#192937")
draw.text((25, 56), "XH balance end faces body • USB-C end faces rear bezel", font=label_font, fill="#32495c")

u = np.array([-0.8, -0.6, 0.0]); u /= np.linalg.norm(u)
v = np.array([0.25, -0.35, 0.9]); v /= np.linalg.norm(v)
d = np.cross(u, v)
center = np.array([0.0, 20.0, -22.0])
triangles = []
for mesh, color in ((body, (164, 180, 193)), (name, (54, 75, 90)),
                    (tray, (47, 142, 205)), (lid, (237, 158, 63))):
    for tri in mesh.triangles:
        t = tri - center
        xy = np.column_stack((t @ u, t @ v)) * 7.2
        xy[:, 0] += 475
        xy[:, 1] = 380 - xy[:, 1]
        n = np.cross(t[1] - t[0], t[2] - t[0])
        norm = np.linalg.norm(n)
        light = 0.77 + 0.23 * abs(float(n @ np.array([0.3, 0.6, 0.7])) / norm) if norm else 0.77
        triangles.append((float((t @ d).mean()), xy, tuple(int(c * light) for c in color)))
for _, xy, color in sorted(triangles, key=lambda x: x[0]):
    draw.polygon([tuple(p) for p in xy], fill=color)

draw.rounded_rectangle((18, 670, 932, 745), radius=8, fill="#eaf1f5")
draw.text((32, 684), "Envelope fit and printed-part interference checked; exact plug positions are unknown.",
          font=label_font, fill="#253b4d")
draw.text((32, 712), "Mount requires four M3 screws; rear bezel takes two M2 screws.",
          font=label_font, fill="#253b4d")
img.save(HERE / "cassette_preview.png")
