"""Make a labeled snapshot from the CAD packaging study; envelopes are proxies."""
from pathlib import Path
import FreeCAD as App
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
doc=App.openDocument(str(HERE/'Cece_Full_Electronics_Study.FCStd'))
colors={
 'Rounded_Head_Study':((.79,.85,.91),.14),'Rear_Cover_Study':((.79,.85,.91),.14),
 'Body':((.79,.85,.91),.14),'Heart_Frame_V3':((.93,.34,.48),.30),
 'Left_Arm':((.55,.73,.86),.5),'Right_Arm':((.55,.73,.86),.5),
 'Left_Leg':((.57,.72,.85),.18),'Right_Leg':((.57,.72,.85),.18),
 'Left_Foot':((.36,.53,.72),.35),'Right_Foot':((.36,.53,.72),.35),
 'Antenna':((1.,.75,.30),1.),'Charger_Tray':((.55,.75,.80),.2),'Charger_Bezel':((.36,.65,.70),.2),
 'Charger_UC2_Unpurchased_Proxy':((1.,.42,.1),1.),'Battery_Clearance':((.3,.76,.35),1.),
 'UBEC_Clearance':((1.,.71,.15),1.),'OLED_Adafruit4741_Official_CAD':((.08,.2,.34),1.),
 'HC_SR04_PCB':((.13,.58,.56),1.),'HC_SR04_Left_Can':((.30,.80,.85),1.),'HC_SR04_Right_Can':((.30,.80,.85),1.),
 'Speaker_COM21311_Clearance':((.89,.22,.48),1.),'PiicoDev_Driver_Official_Partial_STEP':((.63,.36,.85),1.),
 'ESP32_C3_Board_Envelope':((.19,.66,.48),1.),'DFR0954_Amp_Envelope':((.95,.55,.27),1.),
 'INMP441_Breakout_Envelope':((.27,.58,.92),1.),'Camera_Stack_Clearance_Provisional':((.18,.75,.50),1.),
 'Camera_Lens_Corridor_Provisional':((.08,.10,.13),1.),'Perfboard_Provisional_30x20':((.52,.32,.13),1.),
 'Left_Hip_SG90_Proxy':((.22,.43,.9),1.),'Right_Hip_SG90_Proxy':((.22,.43,.9),1.),
 'Left_Ankle_SG90_Proxy':((.22,.43,.9),1.),'Right_Ankle_SG90_Proxy':((.22,.43,.9),1.)}
for side in ('Left','Right'):
 for joint in ('Hip','Ankle'):
  colors[f'{side}_{joint}_Turret_Proxy']=((.18,.38,.8),1.)
  colors[f'{side}_{joint}_Output_Shaft_Proxy']=((1.,.35,.08),1.)
for i in range(1,6):colors[f'LED_{i}_Body_Proxy']=((1.,.78,.1),1.)
ren=vtk.vtkRenderer();ren.SetBackground(.93,.96,.98);ren.SetUseDepthPeeling(True)
win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(960,900);win.SetAlphaBitPlanes(1);win.SetMultiSamples(0);win.AddRenderer(ren)
for name,(color,opacity) in colors.items():
 shape=doc.getObject(name).Shape;v,f=shape.tessellate(.8)
 pts=np.array([[p.x,p.y,p.z] for p in v],dtype=float);faces=np.asarray(f,dtype=np.int64)
 cells=np.column_stack((np.full(len(faces),3,dtype=np.int64),faces)).ravel()
 points=vtk.vtkPoints();points.SetData(numpy_to_vtk(pts,deep=True))
 polys=vtk.vtkCellArray();polys.SetCells(len(faces),numpy_to_vtkIdTypeArray(cells,deep=True))
 data=vtk.vtkPolyData();data.SetPoints(points);data.SetPolys(polys)
 normals=vtk.vtkPolyDataNormals();normals.SetInputData(data);normals.ConsistencyOn();normals.SplittingOff()
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
 a=vtk.vtkActor();a.SetMapper(mapper);a.GetProperty().SetColor(*color);a.GetProperty().SetOpacity(opacity);a.GetProperty().SetAmbient(.45);a.GetProperty().SetDiffuse(.55);ren.AddActor(a)
camera=ren.GetActiveCamera();camera.SetPosition(230,-440,125);camera.SetFocalPoint(0,8,-18);camera.SetViewUp(0,0,1);camera.ParallelProjectionOn();camera.SetParallelScale(110)
win.Render();capture=vtk.vtkWindowToImageFilter();capture.SetInput(win);capture.Update();writer=vtk.vtkPNGWriter();temp=HERE/'electronics_render_tmp.png';writer.SetFileName(str(temp));writer.SetInputConnection(capture.GetOutputPort());writer.Write();win.Finalize();App.closeDocument(doc.Name)
canvas=Image.new('RGB',(1400,900),'white');canvas.paste(Image.open(temp).convert('RGB'),(0,0));temp.unlink()
d=ImageDraw.Draw(canvas);fontpath=r'C:\Windows\Fonts\arial.ttf';boldpath=r'C:\Windows\Fonts\arialbd.ttf'
f=ImageFont.truetype(fontpath,20);b=ImageFont.truetype(boldpath,23)
d.text((980,35),'CECE ELECTRONICS',font=b,fill='#243b54')
legend=[('4 servo case proxies',(56,110,230)),('Output shaft proxies',(255,89,20)),('Battery envelope',(76,194,89)),('UBEC envelope',(255,181,38)),('Servo driver',(160,92,217)),('Ultrasonic sensor',(77,204,217)),('OLED display',(20,51,87)),('Speaker envelope',(227,56,122)),('Camera envelope',(46,191,128)),('Microphone envelope',(69,148,235)),('Amplifier envelope',(242,140,69)),('Perfboard placeholder',(133,82,33)),('Charger candidate',(255,107,26))]
for i,(label,c) in enumerate(legend):
 y=86+i*45;d.rounded_rectangle((980,y,1002,y+22),radius=4,fill=c);d.text((1015,y),label,font=f,fill='#344a61')
d.text((980,715),'Transparent shell shows',font=f,fill='#344a61');d.text((980,742),'approximate placements.',font=f,fill='#344a61')
d.text((980,795),'CAD STUDY ONLY',font=b,fill='#a04b32');d.text((980,827),'Wiring and mounts unfinished',font=f,fill='#a04b32')
canvas.save(HERE/'Cece_Electronics_Overview.png',optimize=True)
