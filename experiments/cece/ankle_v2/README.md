# Cece SG90 ankle V2 — FreeCAD mechanical revision

This revision uses the four SG90 servos already bought: two hip servos and two ankle servos. No additional servos are needed. The source geometry is the Cece/Otto V9 leg and the Cece URL-cleaned feet. The supplied plastic servo horn remains the drive coupling; the printed pin on the other side is a bearing.

## Changes

- Enlarged the servo insertion corridor to allow 0.8 mm nominal clearance on each X side, 0.5 mm on each Y side and 0.8 mm on each Z side around the **assumed case body** (12.2 × 22.5 × 23 mm). The seller publishes only overall servo size (23 × 12.2 × 29 mm); this case split and shaft position are provisional.
- Replaced the tapered molded bearing peg with a 4.7 mm straight bearing. The matching foot bore is 5.4 mm. These diameters give 0.35 mm nominal radial space before print error.
- Added a 0.5 mm thrust collar at the leg side and a separate 8.8 mm OD retaining washer at the outside of the foot, leaving nominal 0.25 mm inner and 0.30 mm outer axial gaps. The washer screws into the pilot hole in the peg. This makes the bearing captive.
- Added two shallow tie grooves above the foot, for narrow nylon cable ties that clamp the servo case to the leg. Optional 0.6/0.8 mm flat shims can take up case width variation. The tie shapes in FreeCAD are clearance envelopes; actual ties are installed by hand.

## Print inventory for one robot

- `Cece_left_leg_SG90_v2.stl` and `Cece_right_leg_SG90_v2.stl`: one each.
- `Cece_left_foot_bearing_v2.stl` and `Cece_right_foot_bearing_v2.stl`: one each; these replace the earlier feet.
- `Cece_left_bearing_washer.stl` and `Cece_right_bearing_washer.stl`: one each, plus a spare of each recommended.
- `SG90_Shimming_Strip_0p6.stl` and `SG90_Shimming_Strip_0p8.stl`: optional; print only the thickness needed after checking the actual servo.

Four SG90 servos total: two in the ankles and two at the hips. Use their supplied horns and the proper horn retaining/fixing screws. The captive bearing design also needs one **suitable M2 × 8 mm pointed screw per ankle**; confirm that the servo accessories include two of these. It also uses two narrow nylon cable ties per ankle. If those fasteners/ties are not on hand they are required hardware, not extra servos.

## FreeCAD check

`Cece_SG90_Ankle_V2.FCStd` is the inspection assembly, with exact STL-derived leg/foot solids, a body/shaft/turret envelope, washer and tie clearance shapes. `build_and_check.py` regenerates it in FreeCAD 1.1. `freecad_fit_results.json` records all checks. The left and right printable legs and feet are each valid single solids; all exported STLs are watertight single components. At the neutral pose, the exact printed parts and servo proxies have zero overlap. FreeCAD swept the leg, servo body, turret, shaft, washer and tie clearance envelopes against each foot at 5° steps from -45° to +45° with zero volume overlap at every sampled angle.

The output is a geometry check, **not a working-robot guarantee**. It does not prove the actual Rapid Robotics SG90 case, supplied horn, screw lengths, screw pull-out, case clamping, print shrinkage, full robot balance, or walking under load. The Otto V9 manual specifically uses SG90 servos and screw-mounted horns in this ankle geometry, which supports this design approach. The exact Rapid Robotics horn still needs a dry physical assembly before installing the whole robot.

## First physical verification before full assembly

1. Print one revised leg, one matching revised foot and one washer. Confirm the SG90 case slides in with its shaft toward positive Y and can be held firmly by two ties and any needed shims.
2. Centre the servo electronically at 90° without the horn. Fit the supplied horn, then follow the Otto guide's foot horn screw pattern. Confirm the horn seats and the central retaining screw does not bottom out.
3. Fit the opposite bearing and washer with a suitable M2 screw. The washer should retain the foot without clamping it. The leg should swing freely by hand without appreciable wobble or pull-out.
4. Power one servo from a correctly rated 5 V supply and move slowly through ±20°, checking for binding, loose case, cracked pin, and horn slip. Increase motion only if the joint stays sound.

The body/head electronics and full walking gait are separate unresolved Cece design checks. Do not treat this ankle package as a final full-robot print plate.

Sources: https://rapidroboticsaustralia.com.au/products/sg90-micro-servo and the Otto V9 manual at https://www.laskakit.cz/user/related_files/ottodiy_instructionsmanual_v09.pdf .
