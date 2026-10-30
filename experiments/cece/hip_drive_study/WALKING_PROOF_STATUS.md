# Cece walking proof status

**Result: real walking is not proven.** Cece is an incomplete prototype; no
powered full robot, actual servo-to-horn measurements, finished wiring or
physical walking trial were available to this study. The model can only screen
whether the stated assumptions contain obvious geometric or static failures.

A later **Bullet dynamics experiment** with gravity, motor limits and floor
contact is documented in [the Bullet study](../bullet_gait/README.md). It
completes ten lift-and-land steps in its nominal assumed model, but a weak-motor
case fails to lift and a stronger side push tips the model. The assumptions
and missing real-part measurements mean it does not prove physical walking.

## Latest model checks

- The alternate weight transfer keeps an assumed foot edge in contact while
  leaning over the other foot. Sixteen sampled static positions have a
  nonnegative vertical contact-force solution. `edge_transfer_force_check.py`
  used a linear program to balance force and moment while minimizing the
  largest absolute joint moment; the largest optimum over the samples was
  **0.01806 N·m**. Solver equilibrium residual was below 9e-16 in the mixed
  force/moment equations. This is an ideal point-contact solution, not a
  measurement or a dynamic stability result.
- `static_gravity_torques.py` computes gravity moments around all four assumed
  joint axes for 22 single-support positions. Maximum absolute moments are
  **0.04413 N·m stance ankle, 0.00538 N·m stance hip, 0.00006 N·m swing hip,
  and 0.00113 N·m swing ankle**. The modeled total was 289.159 g, including
  assumed 10 g camera and 12 g speaker but excluding multiple boards, wiring,
  mounts and fasteners. The [purchased SG90 listing](https://rapidroboticsaustralia.com.au/products/sg90-micro-servo)
  specifies 1.8 kg·cm holding torque at 4.8 V (about 0.1765 N·m). A holding
  torque is not a continuous operating rating, and this comparison does not
  establish sufficient running torque or electrical capacity.
- `motor_motion_clearance.py` found no volume overlap among its selected motor
  case, turret, shaft and hip-horn **proxies** against selected printed shapes
  in 22 one-foot positions. `second_step_motor_clearance.py` found none in
  48 second-step positions. The supplied horn, spline, servo ears, screws,
  wiring and real shaft geometry were not modeled; motion between samples was
  not checked. See the machine-readable result files for the exact pairs.
- The earlier paired-hip grid found foot collisions at 34 of 169 sampled
  combinations; do not use unrestricted ±30° hip commands. The proposed step
  uses a smaller coordinated range, but no continuous contact or collision
  guarantee has been established.

## What these calculations cannot prove

The contact solver assumes a perfectly rigid, level floor and vertical point
reactions. It omits lateral forces, friction, acceleration, impacts, compliance,
motor speed/load behavior, servo control loops, power sag and moving cables.
It optimizes reaction forces but does not show a physical robot will achieve
those reactions. The design still has unmeasured horn and servo mounting
interfaces, a provisional clamp, incomplete electronics mounts and wiring, and
an unpurchased candidate camera/charger. There is no completed gait firmware.
The quoted values are not a guarantee or safety factor.

## Proposed physical acceptance test

1. Measure the purchased SG90 body, mounting ears, horn, shaft and supplied
   screws; confirm both hip and ankle drive paths and retest the CAD with those
   dimensions. Fit-test one joint before building the complete robot.
2. Complete the electrical design, safe 5 V servo supply, common grounds,
   actual cable routing and board/charger mounting. Weigh every installed item
   and printed part and repeat the mass, clearance and torque calculations.
3. With the robot supported so the feet cannot drive it off a bench, verify
   each servo's neutral, direction, commanded limits, current and joint motion
   separately, and check that the horn and bearing remain securely attached.
   Record voltage at the servo driver during motion. The retailer states a
   **4.8–5 V** operating range for these servos; stop for binding, unintended
   movement, slipping or voltage outside the specified range. Charging and
   power wiring require the separate reviewed design.
4. Install the finished walking code and test slow weight transfer, lift,
   swing and landing while the robot is restrained by a **loose safety tether**
   that does not provide balancing force. Inspect feet, horn fasteners and
   cables after each stage.
5. As a practical project acceptance target, on a level hard surface with the
   full intended payload installed, complete **three independent trials of at
   least 10 consecutive forward steps and 50 mm net progress per trial** without
   falling, manual balancing, foot entanglement, joint slippage or the servo
   supply dropping below its specified operating range. Record video, distance,
   rail voltage and any stall/binding; inspect gearboxes and printed joints.
   This target is a project test criterion, not an industry certification.

Results can only establish behavior for the tested build, floor, gait and
payload. Further reliability and fatigue testing is necessary for a robust
production design.
