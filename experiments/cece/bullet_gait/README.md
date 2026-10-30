# Cece Bullet walking experiment

This is a **rigid-body dynamics experiment**, not a verified physical walking
robot. It uses [Bullet/PyBullet](https://github.com/bulletphysics/bullet3),
gravity, ground contact, four revolute joints, servo position controllers and
motor limits. The pictured exterior is exported from the current FreeCAD
study. The robot, its servo horns and electronics have not yet been fully
assembled or measured.

## Results

A step is counted here when a commanded swing foot is at least 1 mm above the
physics collider and not touching the floor for at least 0.05 seconds, and it
is in contact at the end of the half-step. Forward travel is the base centre of
mass displacement in the programmed forward direction. A fall is defined as a
body tilt over 55° or base COM below 18 mm. These are simulation criteria,
not physical acceptance tests.

| Experiment | Mass | Motor cap | Solver | Lift-and-land events | Forward | Result |
|---|---:|---:|---:|---:|---:|---|
| Nominal | 339.2 g | 0.08 N·m | 240 Hz | 10/10 | 84.9 mm | Upright; maximum 12.1° body tilt |
| Smaller time step | 339.2 g | 0.08 N·m | 480 Hz | 10/10 | 87.8 mm | Upright; peak simulated motor moment changes from 0.0689 to 0.0777 N·m |
| Lower floor friction | 339.2 g | 0.08 N·m | 240 Hz | 10/10 | 85.7 mm | Upright in this contact model |
| Weaker motors | 339.2 g | 0.04 N·m | 240 Hz | 0/10 | 85.5 mm | No detected lifts; forward displacement alone is not walking |
| Additional assumed 60 g payload | 399.2 g | 0.08 N·m | 240 Hz | 10/10 | 84.8 mm | Upright in the model; not a real payload rating |
| 1 N sideways push | 339.2 g | 0.08 N·m | 240 Hz | 10/10 | 85.0 mm | Remained upright in the model |
| 2 N sideways push | 339.2 g | 0.08 N·m | 240 Hz | 1 completed | 11.1 mm | **Fell at 6.15 s**, during second step |

Pushes last 0.15 s, starting at 6 s, 40 mm above the modeled base COM.
The nominal friction coefficient is 0.8 on each surface; Bullet's default
contact combiner multiplies them, giving a nominal effective coefficient of
0.64. The lower-friction experiment uses 0.4 on each surface, yielding 0.16.
These coefficients were **not measured** on the actual feet or floor. Bullet's
[contact-combining source](https://raw.githubusercontent.com/bulletphysics/bullet3/master/src/BulletCollision/CollisionDispatch/btManifoldResult.cpp)
documents the multiplication.

The nominal supporting-foot link moved at most 0.29 mm horizontally during
the lift, swing and landing phases. It remained in contact under the model's
contact rules. The weak-motor case is reported as a failure because neither
foot completed the lift criterion even though the body moved forward.

The video `bullet_cece_4step_final.mp4` is a **recording of the simulated
physics state**, showing four of these slow modeled steps over 16 seconds.
It does not show a physical robot and is not the older decorative animation.
The corresponding machine-readable results contain motor targets, joint
positions, contact links, torques and body position over time.

## How the model was built

- The hip and ankle axes come from the existing CAD study. Initial Bullet joint
  positions were checked against those assumed CAD axes, within 0.00001 mm.
  That numerical agreement does not verify the real SG90 shaft locations.
- Each foot's ground collision is the convex hull of the actual CAD sole
  polygon, extruded 5.02 mm. The body, head and legs use bounding boxes; the
  physics engine's **self-collision is disabled**. The floor is flat and rigid.
- The visible shell and legs use FreeCAD geometry. Solid PLA parts use exact
  solid geometry mass properties at assumed 1.24 g/cm³; real sliced infill and
  supports differ. Other hardware is represented as uniform boxes and some
  mass values are guessed. The 339.2 g total includes the nominal battery,
  UBEC, four servos, candidate charger and explicitly listed estimated parts.
- Joint control is open loop. A nominal 0.08 N·m torque cap and a **hypothetical
  linear** drop to zero at 500°/s are modeled. The [SG90 seller](https://rapidroboticsaustralia.com.au/products/sg90-micro-servo)
  quotes 1.8 kg·cm holding torque at 4.8 V and 0.12 s/60° no-load speed, but
  does not provide the actual continuous torque/speed curve for these units.
  The model does not include motor current, power supply sag, backlash, servo
  internal control, temperature or gearbox wear.
- `check_cad_trajectory.py` independently tests ten selected printed body,
  leg and foot pairs using manifold mesh intersections at 20 Hz along the
  nominal Bullet run. The result is in `cad_trajectory_clearance_results.json`.
  This check remains discrete, and excludes horns, screws, wiring, speaker and
  other components. It does not add self-collision forces to the physics run.

## Reproduce

The environment used locally is `cece_bullet_env`, with conda-forge
`python=3.12`, `pybullet=3.25`, `numpy=2.2.3`, `scipy=1.18.1` and Pillow.
The Python user site supplied the imported NumPy 2.2.3 during these runs;
ensure that version is selected explicitly when reproducing the results.
The mesh tools are in the workspace's `cece_mesh_deps` directory: install
`trimesh==5.2.0` and `manifold3d==3.5.4` there with pip `--target` and
`--no-deps`. Run
`export_visuals.py` and `export_plastic_mass_properties.py` with FreeCAD 1.1
Python after any CAD change; then run `simulate_bullet.py` with the Bullet
environment. For the trajectory check use `--steps 10 --geometry-trace
--trace-hz 20 --name geometry_trace`, then run `check_cad_trajectory.py`.
Use `--video --steps 4 --name cece_4step_final --ffmpeg PATH` to render the
video. The result JSON files contain source hashes and all assumptions.

## Remaining gates

The actual servo body, shaft, mounting ears, horns and screws need measurement
and fit tests. Finish the hip/ankle clamps, board mounts, charger, power and
wiring; weigh the built components; measure actual motor behavior, rail sag and
foot friction; repeat the simulations and then run the restrained physical
test described in [the walking acceptance protocol](../hip_drive_study/WALKING_PROOF_STATUS.md).
Only a physical test of the built robot can establish how that robot walks.
