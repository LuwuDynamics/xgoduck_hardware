"""Measure exact nearest-shell gaps in the saved FreeCAD packaging scene."""
from pathlib import Path
import json
import FreeCAD as App
ROOT=Path(__file__).resolve().parent
doc=App.openDocument(str(ROOT/'Cece_Electronics_Packaging_Study.FCStd'))
pairs=[('Battery_Clearance','Body'),('UBEC_Clearance','Body'),('PiicoDev_Driver_Envelope','Head'),('ESP32_C3_Board_Envelope','Head'),('Charger_UC2_Physical_Candidate','Charger_Tray'),('Speaker_COM21311_Clearance','Head')]
result={a+'__'+b:round(doc.getObject(a).Shape.distToShape(doc.getObject(b).Shape)[0],3) for a,b in pairs}
(ROOT/'internal_gaps_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
