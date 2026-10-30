"""Render the exact FreeCAD shapes; not a photoreal concept or motion test."""
from pathlib import Path
import FreeCAD as App
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
HERE=Path(__file__).resolve().parent
doc=App.openDocument(str(HERE/'Cece_Heart_V4_Assembly.FCStd'))
colors={'Rounded_Head_Study':(0.88,0.92,0.96),'Rear_Cover_Study':(.76,.85,.93),
 'Body':(.85,.89,.94),'Heart_Frame_V3':(.88,.30,.45),'Left_Arm':(.56,.72,.84),'Right_Arm':(.56,.72,.84),
 'Left_Leg':(.58,.71,.83),'Right_Leg':(.58,.71,.83),'Left_Foot':(.36,.52,.69),'Right_Foot':(.36,.52,.69),
 'HC_SR04_Left_Can':(.28,.68,.76),'HC_SR04_Right_Can':(.28,.68,.76),
 'OLED_Adafruit4741_Official_CAD':(.12,.18,.25),'Left_Washer':(.35,.43,.51),'Right_Washer':(.35,.43,.51),
 'Antenna':(.96,.7,.32),
 'Charger_Tray':(.6,.73,.8),'Charger_Bezel':(.45,.57,.67),
 'Camera_Lens_Corridor_Provisional':(.08,.1,.12)}
ren=vtk.vtkRenderer();ren.SetBackground(.91,.95,.98)
win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1000,800);win.AddRenderer(ren)
for name,color in colors.items():
    shape=doc.getObject(name).Shape; verts,faces=shape.tessellate(.6)
    xyz=np.array([[v.x,v.y,v.z] for v in verts],dtype=float);f=np.asarray(faces,dtype=np.int64)
    cells=np.column_stack((np.full(len(f),3,dtype=np.int64),f)).ravel()
    points=vtk.vtkPoints();points.SetData(numpy_to_vtk(xyz,deep=True))
    polys=vtk.vtkCellArray();polys.SetCells(len(f),numpy_to_vtkIdTypeArray(cells,deep=True))
    data=vtk.vtkPolyData();data.SetPoints(points);data.SetPolys(polys)
    normals=vtk.vtkPolyDataNormals();normals.SetInputData(data);normals.ConsistencyOn();normals.SplittingOff()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*color);actor.GetProperty().SetAmbient(.35);actor.GetProperty().SetDiffuse(.65);ren.AddActor(actor)
camera=ren.GetActiveCamera();camera.SetPosition(0,-500,-15);camera.SetFocalPoint(0,0,-15);camera.SetViewUp(0,0,1);camera.ParallelProjectionOn();camera.SetParallelScale(105)
title=vtk.vtkTextActor();title.SetInput('CECE  |  HEART FRAME CANDIDATE');title.SetPosition(30,750);title.GetTextProperty().SetFontSize(23);title.GetTextProperty().SetColor(.18,.28,.39);ren.AddActor2D(title)
warning=vtk.vtkTextActor();warning.SetInput('CAD feasibility study - not print-ready');warning.SetPosition(30,24);warning.GetTextProperty().SetFontSize(17);warning.GetTextProperty().SetColor(.5,.25,.2);ren.AddActor2D(warning)
win.Render();w=vtk.vtkWindowToImageFilter();w.SetInput(win);w.Update();writer=vtk.vtkPNGWriter();writer.SetFileName(str(HERE/'Cece_Heart_V4_Front.png'));writer.SetInputConnection(w.GetOutputPort());writer.Write()
win.Finalize();App.closeDocument(doc.Name)

