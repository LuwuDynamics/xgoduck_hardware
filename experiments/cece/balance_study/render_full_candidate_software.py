"""Software-render front/rear previews of the current exact Cece CAD study.

Run with FreeCAD 1.1 bundled Python. It reads the existing FCStd Part shapes,
triangulates them and uses Pillow's CPU rasterizer. No OpenGL window or scene
geometry changes are needed. The FCStd is opened read-only and never saved.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import FreeCAD as App
import Mesh
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PACKAGING = HERE.parent / 'packaging_study'
SOURCE = PACKAGING / 'Cece_Electronics_Packaging_Study.FCStd'
WIDTH, HEIGHT = 1500, 1050
CX, CY, SCALE = 500, 435, 5.5
SNAPSHOT_LABEL = 'V3 combined head snapshot'

PLASTIC = {
    'Body': (221, 228, 233), 'Head': (211, 225, 239),
    'Heart_Frame_V3': (219, 85, 117), 'Faceplate': (240, 245, 248),
    'Antenna': (246, 188, 91),
    'Left_Arm': (161, 192, 218), 'Right_Arm': (161, 192, 218),
    'Left_Leg': (164, 181, 201), 'Right_Leg': (164, 181, 201),
    'Left_Foot': (105, 137, 174), 'Right_Foot': (105, 137, 174),
    'Left_Washer': (99, 116, 141), 'Right_Washer': (99, 116, 141),
    'Charger_Tray': (60, 155, 177), 'Charger_Bezel': (31, 114, 145),
    'Speaker_Pod': (86, 137, 199), 'Speaker_Grille': (40, 88, 149),
}
ELECTRONICS = {
    'Battery_Clearance': (106, 177, 78),
    'UBEC_Clearance': (237, 174, 66),
    'Charger_UC2_Physical_Candidate': (240, 112, 58),
    'OLED_Adafruit4741_Official_CAD': (61, 79, 106),
    'HC_SR04_PCB': (49, 143, 159),
    'HC_SR04_Left_Can': (64, 175, 199),
    'HC_SR04_Right_Can': (64, 175, 199),
    'Speaker_COM21311_Clearance': (202, 65, 112),
    'PiicoDev_Driver_Official_Partial_STEP': (134, 88, 205),
    'ESP32_C3_Board_Envelope': (78, 184, 145),
    'DFR0954_Amp_Envelope': (204, 129, 190),
    'INMP441_Breakout_Envelope': (105, 176, 209),
    'Left_Hip_SG90_Proxy': (229, 130, 75),
    'Right_Hip_SG90_Proxy': (229, 130, 75),
    'Left_Ankle_SG90_Proxy': (229, 130, 75),
    'Right_Ankle_SG90_Proxy': (229, 130, 75),
}
GHOST_SHELLS = {'Body', 'Head', 'Charger_Tray', 'Charger_Bezel',
                'Speaker_Pod', 'Speaker_Grille'}
NAME_HIGHLIGHT = 'Existing_Fused_Rear_Name_Visual_Highlight'
NAME_OVERLAY_STL = HERE.parent / 'parts_adafruit_draft' / 'Cece_Name_Back_Visual_Overlay.stl'


def font(size, bold=False):
    path = (r'C:\Windows\Fonts\arialbd.ttf' if bold
            else r'C:\Windows\Fonts\arial.ttf')
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def geometry(doc):
    out = {}
    for name in list(PLASTIC)+list(ELECTRONICS):
        obj = doc.getObject(name)
        if obj is None or obj.Shape.isNull():
            raise ValueError(f'Missing CAD object {name}')
        verts, faces = obj.Shape.tessellate(0.8)
        out[name] = (np.array([[v.x,v.y,v.z] for v in verts], dtype=np.float64),
                     np.array(faces, dtype=np.int32))
    # This is the source glyph mesh already fused into the printed body. It is
    # loaded only to colour the existing letters in the rear preview.
    mesh = Mesh.Mesh(str(NAME_OVERLAY_STL))
    verts, faces = mesh.Topology
    out[NAME_HIGHLIGHT] = (
        np.array([[v.x,v.y,v.z] for v in verts],dtype=np.float64),
        np.array(faces,dtype=np.int32))
    return out


def project(vertices, side):
    # Exact orthographic X/Z views; rear is mirrored as seen looking at the back.
    if side == 'front':
        x, depth, light = vertices[:,0], -vertices[:,1], np.array([-.4,-.6,.7])
    else:
        x, depth, light = -vertices[:,0], vertices[:,1], np.array([.4,.6,.7])
    pts = np.column_stack((CX+SCALE*x, CY-SCALE*vertices[:,2], depth))
    return pts, light/np.linalg.norm(light)


def shaded(base, unit_normal, light):
    factor = 0.70 + 0.30*max(0.0, float(np.dot(unit_normal, light)))
    return tuple(max(0, min(255, int(c*factor))) for c in base)


def collect_triangles(meshes, side, selected):
    tris = []
    for name in selected:
        vertices, faces = meshes[name]
        if len(faces) == 0:
            continue
        pts, light = project(vertices, side)
        base = PLASTIC.get(name, ELECTRONICS.get(name, (250,209,80)))
        xyz_faces = vertices[faces]
        normals = np.cross(xyz_faces[:,1]-xyz_faces[:,0],
                           xyz_faces[:,2]-xyz_faces[:,0])
        lengths = np.linalg.norm(normals, axis=1)
        lengths[lengths == 0] = 1.0
        normals /= lengths[:,None]
        projected = pts[faces]
        # Very small facets are omitted only from the raster; source CAD stays exact.
        dx1 = projected[:,1,0]-projected[:,0,0]
        dy1 = projected[:,1,1]-projected[:,0,1]
        dx2 = projected[:,2,0]-projected[:,0,0]
        dy2 = projected[:,2,1]-projected[:,0,1]
        visible_area = np.abs(dx1*dy2-dy1*dx2)*.5
        for i in np.flatnonzero(visible_area >= 0.18):
            xy = [(float(projected[i,j,0]),float(projected[i,j,1]))
                  for j in range(3)]
            depth = float(projected[i,:,2].mean())
            color = shaded(base, normals[i], light)
            tris.append((depth, xy, color))
    tris.sort(key=lambda t: t[0])  # far to near; opaque CAD preview
    return tris


def draw_scene(meshes, side, mode):
    image = Image.new('RGB',(WIDTH,HEIGHT),(249,251,253))
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((35,94,975,940), radius=25,
                        fill=(238,243,247), outline=(216,225,234), width=2)
    if mode == 'exterior':
        selected = list(PLASTIC)+list(ELECTRONICS)
    else:
        selected = [n for n in PLASTIC if n not in GHOST_SHELLS]+list(ELECTRONICS)
    for _, xy, color in collect_triangles(meshes, side, selected):
        d.polygon(xy, fill=color)
    if mode == 'electronics':
        mask = Image.new('L',(WIDTH,HEIGHT),0)
        md = ImageDraw.Draw(mask)
        for name in ('Body','Head','Charger_Tray','Speaker_Pod'):
            vertices, faces = meshes[name]
            pts,_ = project(vertices,side)
            for f in faces:
                md.polygon([(float(pts[i,0]),float(pts[i,1])) for i in f],
                           fill=255)
        # The pale overlay and outline are exact projected shell silhouettes.
        tint = Image.new('RGB',(WIDTH,HEIGHT),(214,226,234))
        alpha = mask.point(lambda p: 29 if p else 0)
        image = Image.composite(tint,image,alpha)
        edge = ImageChops.difference(mask.filter(ImageFilter.MaxFilter(7)),
                                     mask.filter(ImageFilter.MinFilter(7)))
        edge = edge.point(lambda p: 130 if p>70 else 0)
        image.paste((96,124,148),mask=edge)
    if side == 'rear':
        name_mask = Image.new('L',(WIDTH,HEIGHT),0)
        nd = ImageDraw.Draw(name_mask)
        verts, faces = meshes[NAME_HIGHLIGHT]
        pts,_ = project(verts,side)
        for f in faces:
            nd.polygon([(float(pts[i,0]),float(pts[i,1])) for i in f],fill=255)
        # Paint the same fused letter silhouette with contrast for inspection.
        border = name_mask.filter(ImageFilter.MaxFilter(5))
        image.paste((91,58,35),mask=border)
        image.paste((252,213,87),mask=name_mask)
    return image


def label(image, side, mode, source_hash):
    d = ImageDraw.Draw(image)
    title = (f"Cece CAD candidate ({SNAPSHOT_LABEL}) — {side.title()} "
             f"{'exterior' if mode=='exterior' else 'electronics view'}")
    d.text((45,28),title,font=font(34,True),fill=(29,51,76))
    d.text((45,68),"Exact study shapes in their assembled positions; colours identify parts and envelopes.",
           font=font(17),fill=(67,85,105))
    d.rounded_rectangle((1000,94,1465,940),radius=24,fill=(255,255,255),
                        outline=(217,226,234),width=2)
    x,y=1025,120
    d.text((x,y),'PRINTED PLASTIC',font=font(20,True),fill=(29,51,76));y+=38
    for label_text,key in [
        ('Body and head','Body'),('Heart frame','Heart_Frame_V3'),
        ('Legs and feet','Left_Foot'),('Charger cassette','Charger_Tray'),
        ('Speaker pod','Speaker_Pod')]:
        d.rounded_rectangle((x,y+4,x+22,y+22),radius=4,fill=PLASTIC[key]);
        d.text((x+34,y),label_text,font=font(18),fill=(50,68,89));y+=38
    d.rounded_rectangle((x,y+4,x+22,y+22),radius=4,fill=(252,213,87));
    d.text((x+34,y),'Existing cece lettering*',font=font(18),fill=(50,68,89));y+=42
    y+=8
    d.text((x,y),'ELECTRONICS / ENVELOPES',font=font(20,True),fill=(29,51,76));y+=39
    for label_text,key in [
        ('Battery clearance','Battery_Clearance'),('UBEC clearance','UBEC_Clearance'),
        ('UC2 charger candidate','Charger_UC2_Physical_Candidate'),
        ('OLED official CAD','OLED_Adafruit4741_Official_CAD'),
        ('Ultrasonic proxy','HC_SR04_Left_Can'),
        ('Servo driver partial STEP','PiicoDev_Driver_Official_Partial_STEP'),
        ('ESP32-C3 envelope','ESP32_C3_Board_Envelope'),
        ('SG90 case proxies','Left_Hip_SG90_Proxy'),
        ('Speaker envelope','Speaker_COM21311_Clearance'),
        ('Amp and microphone','DFR0954_Amp_Envelope'),
    ]:
        d.rounded_rectangle((x,y+4,x+22,y+22),radius=4,fill=ELECTRONICS[key]);
        d.text((x+34,y),label_text,font=font(18),fill=(50,68,89));y+=34
    d.text((1025,865),'*Rendering highlight of fused rear name;',font=font(14),fill=(94,112,129))
    d.text((1025,886),'not an added printed part.',font=font(14),fill=(94,112,129))
    d.text((1025,910),'Grey outlines: hidden shells.',font=font(14),fill=(94,112,129))
    d.rounded_rectangle((35,964,1465,1026),radius=15,fill=(255,235,226),
                        outline=(242,166,140),width=2)
    d.text((55,976),'CAD candidate, not physical fit verified',
           font=font(24,True),fill=(144,58,41))
    d.text((800,985),f'Source FCStd SHA-256 {source_hash[:12]} · orthographic {side} view',
           font=font(15),fill=(117,68,55))
    return image


def main():
    doc = App.openDocument(str(SOURCE))
    meshes = geometry(doc)
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    for side in ('front','rear'):
        for mode in ('exterior','electronics'):
            im = draw_scene(meshes,side,mode)
            im = label(im,side,mode,source_hash)
            out = PACKAGING / f'Cece_CAD_{side}_{mode}.png'
            im.save(out,optimize=True)
            print(out,flush=True)
    App.closeDocument(doc.Name)


if __name__ == '__main__':
    main()
