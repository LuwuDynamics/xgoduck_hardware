# Cece heart frame V4 — design candidate

The updated front fascia has rounded lobes, a centre notch and a pointed lower end, with a 30.2 mm square OLED window preserved from V3. It is a single watertight part, about 72.7 mm wide and 49.5 mm tall. The wider fascia adds approximately 3.12 g of solid PLA relative to the V3 frame (actual printed weight depends on slicer settings).

`Cece_Heart_V4_Assembly.FCStd` is the full existing candidate assembly with the new heart substituted. `Cece_Heart_Frame_V4_TEST_ONLY.stl` is the heart frame only, not a complete robot. `Cece_Heart_V4_Front.png` shows the CAD assembly. Open `show_heart_v4.FCMacro` in FreeCAD for the coloured front view.

The FreeCAD solid intersection test found no overlaps above 0.01 mm³ between the heart and the other modeled objects in the neutral pose. An independent mesh test against four leg and foot solids found no overlaps above 0.01 mm³ in 800 samples of the existing 20 Hz gait trajectory. That trajectory was generated for the earlier frame and does not incorporate this frame's additional mass. The checks do not establish continuous clearance, walking reliability, real-part tolerances, hardware or cable fit. Display retention and attachment to the body also remain to be validated. Do not treat this candidate as a complete print-ready design.

`build_heart.py` generates the mesh; `check_and_assemble.py` performs the neutral CAD check and exports the assembly; `../bullet_gait/check_heart_trajectory.py` runs the sampled leg-clearance check. JSON files record the measured results.
