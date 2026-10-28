"""Illustrative turntable animation of the V3 FreeCAD study, not a physics test."""
import math
import os
import shutil
import subprocess
from pathlib import Path

import FreeCAD as App
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'Cece_Electronics_Packaging_Study.FCStd'
OUTPUT = ROOT / 'Cece_V3_Colour_Concept.mp4'
FFMPEG = os.environ.get('CECE_FFMPEG') or shutil.which('ffmpeg')
if not FFMPEG:
    raise RuntimeError('Set CECE_FFMPEG to an ffmpeg executable, or add ffmpeg to PATH')
W, H, FPS, SECONDS = 960, 720, 24, 12

colors = {
    'Body': '#e4edf4', 'Head': '#e9f1f7', 'Heart_Frame_V3': '#ed5884',
    'Faceplate': '#f9fbff', 'Antenna': '#ffc65c',
    'Left_Arm': '#82b6db', 'Right_Arm': '#82b6db',
    'Left_Leg': '#a8c8df', 'Right_Leg': '#a8c8df',
    'Left_Foot': '#547fb0', 'Right_Foot': '#547fb0',
    'Left_Washer': '#496584', 'Right_Washer': '#496584',
    'Charger_Tray': '#d4e4ec', 'Charger_Bezel': '#7798a6',
    'Speaker_Pod': '#a5c6df', 'Speaker_Grille': '#537dab',
    'OLED_Adafruit4741_Official_CAD': '#1b304c',
    'HC_SR04_Left_Can': '#58c9db', 'HC_SR04_Right_Can': '#58c9db',
}

def rgb(h):
    return tuple(int(h[i:i+2], 16)/255 for i in (1,3,5))

def actor_for_shape(shape, color):
    vertices, faces = shape.tessellate(0.6)
    pts = np.array([[p.x,p.y,p.z] for p in vertices], dtype=np.float64)
    faces = np.asarray(faces, dtype=np.int64)
    cells = np.column_stack((np.full(len(faces),3,dtype=np.int64),faces)).ravel()
    points = vtk.vtkPoints(); points.SetData(numpy_to_vtk(pts, deep=True))
    polys = vtk.vtkCellArray(); polys.SetCells(len(faces), numpy_to_vtkIdTypeArray(cells, deep=True))
    data = vtk.vtkPolyData(); data.SetPoints(points); data.SetPolys(polys)
    normals = vtk.vtkPolyDataNormals(); normals.SetInputData(data); normals.ConsistencyOn(); normals.SplittingOff(); normals.Update()
    mapper = vtk.vtkPolyDataMapper(); mapper.SetInputConnection(normals.GetOutputPort())
    actor = vtk.vtkActor(); actor.SetMapper(mapper)
    prop=actor.GetProperty(); prop.SetColor(*rgb(color)); prop.SetAmbient(.27); prop.SetDiffuse(.68); prop.SetSpecular(.25); prop.SetSpecularPower(30)
    return actor

def sphere(center, radius, color):
    s=vtk.vtkSphereSource(); s.SetCenter(*center); s.SetRadius(radius); s.SetThetaResolution(18); s.SetPhiResolution(12)
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*rgb(color)); a.GetProperty().SetAmbient(.6); a.GetProperty().SetSpecular(.4)
    return a

def line(points, color, width=3):
    p=vtk.vtkPoints(); [p.InsertNextPoint(*point) for point in points]
    path=vtk.vtkPolyLine(); path.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)): path.GetPointIds().SetId(i,i)
    ca=vtk.vtkCellArray(); ca.InsertNextCell(path)
    data=vtk.vtkPolyData(); data.SetPoints(p); data.SetLines(ca)
    tube=vtk.vtkTubeFilter(); tube.SetInputData(data); tube.SetRadius(width/2); tube.SetNumberOfSides(10)
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(tube.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*rgb(color)); a.GetProperty().SetAmbient(.8)
    return a

doc=App.openDocument(str(SOURCE))
ren=vtk.vtkRenderer(); ren.SetBackground(.90,.94,.98); ren.SetBackground2(.98,.985,1); ren.GradientBackgroundOn()
window=vtk.vtkRenderWindow(); window.SetOffScreenRendering(1); window.SetSize(W,H); window.SetMultiSamples(4); window.AddRenderer(ren)
actors={}
for name,color in colors.items():
    o=doc.getObject(name)
    if o is None or o.Shape.isNull(): raise RuntimeError('Missing '+name)
    actors[name]=actor_for_shape(o.Shape,color); ren.AddActor(actors[name])

# The display graphics and LED colours are artistic overlays; they are not CAD hardware.
for x in (-6,6): ren.AddActor(sphere((x,-43.8,-16),1.5,'#8df4ff'))
smile=[(x,-43.85,-23+0.045*x*x) for x in np.linspace(-8,8,25)]
ren.AddActor(line(smile,'#8df4ff',.8))
for x,z in [(-8,5),(-4,3.8),(0,3.2),(4,3.8),(8,5)]:
    ren.AddActor(sphere((x,-34.6,z),1.1,'#ffbb5a'))

floor=vtk.vtkPlaneSource(); floor.SetOrigin(-500,-500,-89.2); floor.SetPoint1(500,-500,-89.2); floor.SetPoint2(-500,500,-89.2)
fm=vtk.vtkPolyDataMapper(); fm.SetInputConnection(floor.GetOutputPort()); fa=vtk.vtkActor(); fa.SetMapper(fm); fa.GetProperty().SetColor(.83,.88,.93); fa.GetProperty().SetAmbient(.65); ren.AddActor(fa)

def text_label(value,x,y,size,color):
    a=vtk.vtkTextActor(); a.SetInput(value); a.SetPosition(x,y); p=a.GetTextProperty(); p.SetFontFamilyToArial(); p.SetFontSize(size); p.SetColor(*rgb(color)); p.SetBold(True); ren.AddActor2D(a)
text_label('cece',40,654,42,'#355675')
text_label('COLOUR CONCEPT  |  CAD CANDIDATE',42,626,15,'#5d7892')
text_label('Illustrative animation - fit and walking are not verified',42,28,16,'#596e83')

camera=ren.GetActiveCamera(); camera.SetViewUp(0,0,1); camera.SetFocalPoint(0,4,-20); camera.ParallelProjectionOn(); camera.SetParallelScale(100)
writer=subprocess.Popen([FFMPEG,'-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(OUTPUT)],stdin=subprocess.PIPE)
grab=vtk.vtkWindowToImageFilter(); grab.SetInput(window); grab.SetInputBufferTypeToRGB(); grab.ReadFrontBufferOff()
try:
    for i in range(FPS*SECONDS):
        t=i/FPS
        # Front view holds briefly, then circles to the rear and back.
        progress=max(0,min(1,(t-1)/10))
        angle=2*math.pi*(progress-math.sin(2*math.pi*progress)/(2*math.pi))
        camera.SetPosition(300*math.sin(angle),-300*math.cos(angle),95)
        for name,sign in [('Left_Arm',1),('Right_Arm',-1)]:
            pivot=(-39 if name=='Left_Arm' else 39,0,-12)
            transform=vtk.vtkTransform(); transform.PostMultiply(); transform.Translate(-pivot[0],-pivot[1],-pivot[2]); transform.RotateY(sign*5*math.sin(2*math.pi*t/2.5)); transform.Translate(*pivot); actors[name].SetUserTransform(transform)
        window.Render(); grab.Modified(); grab.Update()
        a=vtk_to_numpy(grab.GetOutput().GetPointData().GetScalars()).reshape(H,W,3)
        writer.stdin.write(np.flipud(a).tobytes())
        if i%48==0: print(f'frame {i}/{FPS*SECONDS}',flush=True)
finally:
    writer.stdin.close(); status=writer.wait(); window.Finalize(); App.closeDocument(doc.Name)
if status: raise RuntimeError(f'ffmpeg exited {status}')
print('Wrote',OUTPUT,flush=True)
