# Cece CAD candidate previews

The four PNGs below are orthographic projections of the **exact Part shapes** in `Cece_Electronics_Packaging_Study.FCStd`. The plastic colours identify printable STL-derived solids. Electronics colours identify the official OLED/partial PiicoDev CAD or the placement envelopes already in that study. The body, head, charger cassette and speaker pod are shown as pale outlines in the electronics views so their internal positions can be seen. These outlines are projections of their CAD shapes. The gold rear `cece` is a rendering highlight of the name mesh already fused into the printed body, aligned at its existing CAD coordinates; it is **not an extra printed part**.

| View | Exterior | Electronics with ghosted shells |
|---|---|---|
| Front | [Cece_CAD_front_exterior.png](Cece_CAD_front_exterior.png) | [Cece_CAD_front_electronics.png](Cece_CAD_front_electronics.png) |
| Rear | [Cece_CAD_rear_exterior.png](Cece_CAD_rear_exterior.png) | [Cece_CAD_rear_electronics.png](Cece_CAD_rear_electronics.png) |

Each image is marked **“CAD candidate, not physical fit verified”** and records the first 12 characters of the source FCStd SHA-256. The current images are a **V3 combined-head snapshot** with the V2 driver hood, enlarged speaker side route, V3 retained faceplate and side-notched speaker pod; regenerate them if any assembly geometry changes. Run `C:\Program Files\FreeCAD 1.1\bin\python.exe experiments/cece/balance_study/render_full_candidate_software.py` from the repository root. The script reads the FCStd without saving it and writes the four PNGs here. It uses FreeCAD shape tessellation and a CPU rasterizer because Qt's offscreen OpenGL widget is unavailable on this PC.

The renderer uses a far-to-near triangle draw order; small occlusion or edge artifacts are possible. The images show a **neutral CAD pose** and envelopes, not a measured assembly, print tolerance check, electrical verification or motion simulation. Review the dimensioned and interference reports separately before changing the print set.
