"""Render four SG90 case and output envelopes in the full robot study."""
from pathlib import Path
import FreeCAD as App
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
doc=App.openDocument(str(HERE/'Cece_Full_Electronics_Study.FCStd'))
shells=['Body','Rounded_Head_Study','Rear_Cover_Study','Left_Leg','Right_Leg','Left_Foot','Right_Foot','Left_Arm','Right_Arm']
motors=[f'{s}_{j}_SG90_Proxy' for s in ('Left','Right') for j in ('Hip','Ankle')]
shafts=[f'{s}_{j}_Output_Shaft_Proxy' for s in ('Left','Right') for j in ('Hip','Ankle')]
ren=vtk.vtkRenderer();ren.SetBackground(.95,.97,.99);ren.SetUseDepthPeeling(True)
win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(900,850);win.SetAlphaBitPlanes(1);win.SetMultiSamples(0);win.AddRenderer(ren)
for name in shells+motors+shafts:
 shape=doc.getObject(name).Shape;v,f=shape.tessellate(.8)
 points=vtk.vtkPoints();points.SetData(numpy_to_vtk(np.array([[p.x,p.y,p.z] for p in v]),deep=True))
 faces=np.asarray(f,dtype=np.int64);cells=np.column_stack((np.full(len(faces),3,dtype=np.int64),faces)).ravel()
 polys=vtk.vtkCellArray();polys.SetCells(len(faces),numpy_to_vtkIdTypeArray(cells,deep=True))
 data=vtk.vtkPolyData();data.SetPoints(points);data.SetPolys(polys)
 m=vtk.vtkPolyDataMapper();m.SetInputData(data);a=vtk.vtkActor();a.SetMapper(m)
 if name in shells:a.GetProperty().SetColor(.6,.72,.82);a.GetProperty().SetOpacity(.12)
 elif name in motors:a.GetProperty().SetColor(.16,.39,.9);a.GetProperty().SetOpacity(.9)
 else:a.GetProperty().SetColor(1.,.35,.05);a.GetProperty().SetOpacity(1.)
 a.GetProperty().SetAmbient(.5);ren.AddActor(a)
cam=ren.GetActiveCamera();cam.SetPosition(0,-500,0);cam.SetFocalPoint(0,0,-20);cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(100)
win.Render();cap=vtk.vtkWindowToImageFilter();cap.SetInput(win);cap.Update();writer=vtk.vtkPNGWriter();temp=HERE/'actuator_render_tmp.png';writer.SetFileName(str(temp));writer.SetInputConnection(cap.GetOutputPort());writer.Write();win.Finalize();App.closeDocument(doc.Name)
image=Image.new('RGB',(1320,850),'white');image.paste(Image.open(temp).convert('RGB'),(0,0));temp.unlink();d=ImageDraw.Draw(image)
f=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',22);b=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',25)
d.text((920,35),'FOUR SG90 SERVOS',font=b,fill='#233c55')
for y,lines in [(105,['2 hip servos','Inside the lower body','Turn the legs']), (275,['2 ankle servos','One inside each leg','Tilt the feet'])]:
 d.rounded_rectangle((920,y,945,y+25),radius=4,fill='#2968e7')
 for i,line in enumerate(lines):d.text((960,y+31*i),line,font=b if i==0 else f,fill='#2e465e')
d.rounded_rectangle((920,445,945,470),radius=4,fill='#ff5910');d.text((960,445),'Output shaft proxies',font=f,fill='#2e465e')
d.text((920,610),'The blue shapes are',font=f,fill='#2e465e');d.text((920,640),'servo-sized placeholders.',font=f,fill='#2e465e')
d.text((920,705),'CAD STUDY ONLY',font=b,fill='#a04b32');d.text((920,740),'Actual horns and screws',font=f,fill='#a04b32');d.text((920,770),'still need fit testing.',font=f,fill='#a04b32')
image.save(HERE/'Cece_Four_Servos_Overview.png',optimize=True)
