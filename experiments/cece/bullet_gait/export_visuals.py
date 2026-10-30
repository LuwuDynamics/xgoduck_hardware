"""Export actual FreeCAD shapes for Bullet visualization only, not collision."""
from pathlib import Path
import FreeCAD as App,Mesh
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hip_drive_study'/'Cece_Full_Electronics_Study.FCStd'
ASSETS=HERE/'cad_visuals';ASSETS.mkdir(exist_ok=True)
doc=App.openDocument(str(SOURCE))
names=['Body','Rounded_Head_Study','Rear_Cover_Study','Heart_Frame_V3','Antenna',
       'Left_Arm','Right_Arm','Left_Leg','Right_Leg','Left_Foot','Right_Foot',
       'OLED_Adafruit4741_Official_CAD','HC_SR04_Left_Can','HC_SR04_Right_Can',
       'Camera_Lens_Corridor_Provisional','Charger_Tray','Charger_Bezel']
for name in names:
    obj=doc.getObject(name)
    if obj is None or obj.Shape.isNull():raise ValueError(name)
    Mesh.export([obj],str(ASSETS/f'{name}.stl'))
    print(name,flush=True)
App.closeDocument(doc.Name)
