"""Orthographic rear illustration of the speaker pod candidate STLs."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
CECE = HERE.parents[1]
sys.path.insert(0, str(HERE.parents[4] / "cece_mesh_deps"))
import trimesh

head = trimesh.load(HERE / "cece_head_with_speaker_mount_CANDIDATE.stl", force="mesh")
pod = trimesh.load(HERE / "speaker_pod_tray.stl", force="mesh")
grille = trimesh.load(HERE / "speaker_retaining_grille.stl", force="mesh")
body = trimesh.load(CECE / "packaging_study/charger_cassette" /
                    "cece_body_with_charger_posts_CANDIDATE.stl", force="mesh")
charger = trimesh.load(CECE / "packaging_study/charger_cassette" /
                       "removable_tray.stl", force="mesh")
name = trimesh.load(CECE / "parts_adafruit_draft" /
                    "Cece_Name_Back_Visual_Overlay.stl", force="mesh")

img = Image.new("RGB", (1100, 830), "#f7fafc")
draw = ImageDraw.Draw(img)
title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 25)
small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
draw.text((28, 18), "Cece rear 28 mm speaker pod: candidate packaging", font=title, fill="#182a3c")
draw.text((28, 56), "Grey head/body • blue speaker pod • orange grille • green charger cassette", font=small, fill="#344b5e")

u = np.array([-0.8, -0.6, 0.0]); u /= np.linalg.norm(u)
v = np.array([0.25, -0.35, 0.9]); v /= np.linalg.norm(v)
depth = np.cross(u, v)
center = np.array([0, 20, 0])
tris = []
for mesh, col in ((head, (171, 184, 195)), (body, (171, 184, 195)),
                  (name, (54, 75, 90)), (charger, (105, 166, 103)),
                  (pod, (45, 139, 203)), (grille, (237, 158, 63))):
    for tri in mesh.triangles:
        pts = tri - center
        xy = np.column_stack((pts @ u, pts @ v)) * 5.7
        xy[:, 0] += 550
        xy[:, 1] = 420 - xy[:, 1]
        n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
        norm = np.linalg.norm(n)
        light = 0.76 + 0.24 * abs(float(n @ np.array([0.3, 0.6, 0.7])) / norm) if norm else 0.76
        tris.append((float((pts @ depth).mean()), xy, tuple(int(c * light) for c in col)))
for _, xy, col in sorted(tris, key=lambda row: row[0]):
    draw.polygon([tuple(p) for p in xy], fill=col)

draw.rounded_rectangle((18, 742, 1082, 815), radius=8, fill="#e9f0f5")
draw.text((32, 755), "Exact printed meshes show no solid clashes in this position; speaker terminals and wiring are unknown.",
          font=small, fill="#263c4e")
draw.text((32, 784), "The pod requires a replacement head and two M3 screws; grille takes two M2 screws.",
          font=small, fill="#263c4e")
img.save(HERE / "speaker_pod_preview.png")
