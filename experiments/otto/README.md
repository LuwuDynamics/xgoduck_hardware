# Otto and Cece experiments

This archive is separate from the XGO-Duck print set. It contains:

- `otto_reference/3Dprint/`: the four upstream Otto v09 STL types (head,
  body, leg, foot; print two legs and two feet). The original STEP and SCAD
  source are in `otto_reference/CAD/`.
- `otto_freecad_reference/Otto_Four_Servo_Print_Parts.FCStd`: the original
  print parts arranged for inspection.
- `cece_otto_prototype/`: our modified body, head, OLED frame, LED faceplate,
  lettering, FreeCAD view and notes. This is a **prototype**, not a completed
  physical robot. The head-turning mount, wiring and some electronics fittings
  are incomplete; see its README.
- `otto_head_walk.py` and `otto_actual_stl_sim.py`: simplified MuJoCo studies
  of four leg servos plus a head-yaw joint. `otto_actual_stl_simulation/`
  contains the STL-visual result and recording; the collision shapes are
  simplified and the head/body interference is not modelled.

## Run the simulation

From this directory, use Python 3.10+ and install `mujoco`, `numpy`, and
`Pillow`. Run `python otto_actual_stl_sim.py --video` to regenerate the
10-second recording, or `python otto_actual_stl_sim.py --live` for the live
viewer. The simulation uses approximate inertia, proxy ground contact and
generic torque-limited motors; it does not prove a physical build will walk.

For the editable prototype, open the saved `.FCStd` file in FreeCAD. The
`build_cece_otto.py` mesh generator additionally needs `trimesh`, `manifold3d`
and NumPy. `open_cece_otto.FCMacro` is a FreeCAD macro and expects the Otto
reference STL files and the mirrored simulation assets in this archive.

## Attribution and rights

Otto DIY is by [Otto DIY](https://www.ottodiy.com/). The reference files are
from [Open-Hardware-Leaders/OttoDIY](https://github.com/Open-Hardware-Leaders/OttoDIY)
commit `8cf3e784c734981c50143cfddde18a68685bcea3`. The upstream README is
preserved at `otto_reference/README.md`; it states applicable open-hardware,
software and documentation terms and attribution requirements. Check those
terms and any referenced licenses when sharing or modifying the material.
