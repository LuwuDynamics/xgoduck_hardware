# Cece whole-robot leg and balance study

**Status: research prototype, not a printable release and not a proven walking
robot.** The current FreeCAD assembly is `Cece_Whole_Robot_Leg_Study.FCStd`.
It combines the rounded head feasibility study with experimental revised legs
and feet, with the original battery, charger and electronics placeholders.
Run `show_whole_robot.FCMacro` in FreeCAD for a coloured exterior view. The
assembly includes no measured servo horn or servo screws.

The current force checks, explicit limits and proposed physical walking
acceptance test are recorded in [WALKING_PROOF_STATUS.md](WALKING_PROOF_STATUS.md).

## Electronics and four-actuator view

`Cece_Full_Electronics_Visible_v2_Study.FCStd` is the full packaging view with
transparent plastic and colored electronics already visible. In FreeCAD, use
the eye icons in the model tree to toggle individual parts; the `show_full_electronics.FCMacro`
also recreates this view from `Cece_Full_Electronics_Study.FCStd`.
`Cece_Electronics_Overview.png` and `Cece_Four_Servos_Overview.png` provide
labeled snapshots of the same modeled locations.

There are exactly four SG90 case proxies: left and right hips in the lower
torso, with assumed vertical output axes; and left and right ankles inside the
legs, with assumed fore/aft output axes. The newly added turret and output
shaft proxies have no modeled volume intersection with the corresponding body,
leg or foot in the neutral pose. These shapes and axes are assumptions from
the earlier studies, not accurate vendor CAD of the purchased parts. They omit
the actual supplied horns, mounting ears, screws, plugs and wires.

The model also shows battery and UBEC envelopes; the vendor's OLED and partial
servo-driver CAD; ultrasonic PCB/cans; microphone, amplifier and speaker
envelopes; C3 and unpurchased camera envelopes; five LED-body proxies; and the
unbought UC2 2S charger envelope in the external tray. A brown **30 × 20 mm**
perfboard placeholder and its **32 × 22 × 8 mm** component allowance were added
inside the head. This board size and component height have not been selected
or measured, and individual resistors, capacitors and a switch are not shown.
`full_electronics_fit_results.json` reports no detected volume overlaps for
these newly added selected shapes, not a complete full-assembly check. In
particular the relocated speaker is just **1 mm** from the ESP envelope, with
terminals and wires absent. Real connectors, routing, insertion, mount features,
insulation, charger access and all moving poses still require verification.

## Revised hip slot

The previous sample straight horn proxy was 3 × 15 × 2 mm, and the old leg
intersected it by 11.963 mm³. On each leg, `build_hip_drive.py` cuts a
3.7 × 16.2 × 3.2 mm trial pocket in the existing hip horn region. The proxy
then clears, and the exported test meshes are watertight single components.
Two Ø1.8 mm side pilots in each leg provide an experimental M2 screw clamp
against the horn arm to reduce the clearance. A Ø1.6 mm pilot-core probe and
Ø5 mm straight screwdriver-access envelope clear the leg, body and foot at
neutral pose (`clamp_access_results.json`). This does not check actual M2
screw length, force, horn damage, creep, friction or vibration. The supplied
central horn-to-servo screw is still needed.
The real horn, its spline, length, screw and installation remain unmeasured;
the 3 mm proxy is **not evidence** that the purchased horn will fit. A loose
slot can also cause backlash and concentrate load. No fatigue or pull-out
test has been performed. The horn must connect to the servo output and be
captured by the leg; the opposing ankle bearing is not the drive.

Selected ±45° ankle poses were checked for leg/foot solid overlap. This does
not model a real horn, case, wire, ties, screw, torque or wear. The old ankle
and hip packaging studies remain applicable only within their limitations.

## Foot interference and preliminary movement

The prior wide feet overlapped by 0.196 mm³ at a sampled single hip rotation
of 30° with the other hip fixed. `build_foot_clearance.py` moves each foot's
inner edge outward 1.5 mm to improve that case. Both test STL outputs reload
as watertight single components. A 169-pose grid covering each hip from -30°
to +30° in 5° increments with neutral ankles found **34 combinations with
foot overlap**, notably opposite large hip rotations. The subset from -15° to
+15° had no overlap at the tested grid points. This is not a continuous
clearance guarantee; see `foot_clearance_results.json`.

`stance_pose_check.py` puts one foot on a level floor, tilts the body 14° over
it and counter-rotates the swing ankle. For hip yaw -10°, 0°, +10°, the modeled
COM has approximately 7.2–7.7 mm margin within the planted sole, the swing
foot is approximately 10.9–12.3 mm above the floor, and selected tested
printed shapes do not intersect. The model includes 10 g camera and 12 g
speaker sensitivity assumptions and excludes several boards, wires and
fasteners; it is static and omits servo torque, friction and deformation.

**The initial weight-transfer sequence fails a quasi-static support check.**
In the simple pivot model the swing foot rises while the COM remains outside
the stance sole at small roll angles; for example, a 2° left roll gives a
1.78 mm foot lift and -3.98 mm stance margin. It crosses the stance edge
around 6–8° in this example. There is no verified transition, dynamic balance,
ground contact, acceleration, torque, current or gait controller. The robot
must not be described as walking successfully based on the lifted poses.

An alternate idealized transfer was then screened in
`edge_transfer_results.json`: a second ankle turns to keep an outer edge of
the unloaded foot in contact with the floor while the body tilts. Sampled
two-foot support polygons contain the projected partial-load COM; at 12° body
roll the opposite ankle would need about 34.25° relative rotation in this
geometry. `lift_transition_results.json` samples 12 steps from that edge
contact to a lifted foot on each side; the smallest modeled stance margin is
about 5.27 mm and selected printed meshes have no detected overlaps. Lifted
hip-yaw samples of -10°, 0° and +10° at 12° body roll also clear selected
geometry, with at least 9.4 mm modeled swing-foot floor clearance. These are
possible **stationary configurations**, not a demonstrated trajectory or
force-balanced gait. An edge of a hard printed foot can slip or rock; servo
torque, joint load, contact forces, timing, electronics mass and physical
parts must be checked before attempting an untethered walk.

`stride_pose_check.py` then rotates the torso around the planted hip while
counter-rotating the other hip. In the assumed mechanism this moves the
opposite ankle up to 8.856 mm forward. Twenty-two sampled one-foot positions
over ±10° yaw have at least 4.835 mm ideal sole-support margin and 10.442 mm
swing-foot floor clearance, and the selected printed mesh pairs do not
intersect. `touchdown_pose_check.py` checks 36 candidate landing and return
poses; the minimum modeled support margin is 4.835 mm with no sampled printed
mesh overlaps. `second_step_check.py` uses the first step's final displaced
foot placement and screens a second transfer, lift, swing, landing and return
to two-foot support. Its 48 samples have minimum modeled support margin
5.318 mm and no selected printed mesh overlap; the second ankle ends about
17.7 mm ahead of its starting position. These are static samples of assumed
joint transforms; they do not prove continuous clearance, force balance,
real servo travel, traction, commanded timing, electrical performance,
mechanical strength or repeatable walking.

For the modeled 12° single-support poses, the gravity moment of the included
mass above the stance ankle is approximately **0.041–0.043 N·m**. The
[purchased SG90 listing](https://rapidroboticsaustralia.com.au/products/sg90-micro-servo)
states 1.8 kg·cm holding torque at 4.8 V, approximately 0.1765 N·m. This
comparison is a screening calculation only: the model omits components and
dynamic torque, and the seller's holding rating is not a continuous operating
rating or a measured torque for the purchased servo. It does not establish
adequate reserve or acceptable current, temperature, gear wear, or voltage sag.

## Remaining work

1. Establish measured SG90 body, mounting-ear, horn, spline and screw geometry;
   finish both hip and ankle connections and test them with the real parts.
2. Solve weight transfer, foot clearances throughout a complete step, motion
   limits and recovery without assuming unverified friction or servo torque.
   Test with measured robot masses and a constrained initial hardware setup.
3. Design and fit the complete rounded torso, camera mount, electronics,
   fasteners, charger and cables. Check servo power and 5 V sag. No 2S charger
   is included in the purchased UBEC.
4. Slice the final parts for the actual printer; test coupons and full assembly
   before a powered walk. The `TEST_ONLY` STLs are engineering artifacts, not
   a recommendation to print a complete robot.
