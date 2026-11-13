# XGO-Duck reference and simulation

- `xgoduck_freecad_reference/XGO_Duck_Standing_Reference.FCStd`: a static
  assembled view of the upstream simulation meshes, not printable parts or a
  moving FreeCAD assembly. The printable files are in `../../3d/` and
  `../../structure/`.
- `xgoduck_walk_output/walking.gif` and `result.json`: the recorded simulation
  and measurements. The run used the upstream walking policy with simplified
  MuJoCo position actuators. It is not a physical or build validation.
- `xgoduck_print_inventory/`: per-part weight calculations at 100% solid
  assumptions; not a slicer estimate.
- `XGODUCK_REVIEW.md`: hardware, power, gait and provenance review.

## Recreate the walking run

The scripts expect the following two upstream repositories cloned **inside
this directory** at the revisions used in the experiment:

```text
git clone https://github.com/LuwuDynamics/xgoduck_rl.git xgoduck_rl_reference
git -C xgoduck_rl_reference checkout fa621fc77ad9a05d69da13270e86118bdd3603fe
git clone https://github.com/LuwuDynamics/xgoduck_runtime_arduino.git xgoduck_runtime_reference
git -C xgoduck_runtime_reference checkout 8837d5a3bc7cf3746f6da2b55c7b9191026b9838
python -m pip install mujoco==3.17.0 numpy pillow onnxruntime
python xgoduck_walk_simulation.py --seconds 8 --speed 0.3 --video
```

The cloned reference repositories and Python dependencies are intentionally
not included in this archive. The policy and model revisions, sensor inputs,
approximations and simulation output are documented in `result.json`.
`xgoduck_print_weights.py` reads the repository's `structure/` folder and
requires FreeCAD's Python with the `FreeCAD` and `Mesh` modules.

The XGO-Duck hardware project and its upstream designs are credited in the
repository's `UPSTREAM.md` and `LICENSING.md`. Review applicable terms before
reusing or distributing any hardware or model asset.
