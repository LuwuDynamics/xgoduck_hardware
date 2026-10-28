# Cece removable head-to-body four-screw joint — separate candidate

**Status: geometry candidate only; exclude from the current V3 print release until a physical coupon test.** This study preserves the current V3 side-speaker/faceplate head and V4 charger/OLED body. It exports replacement head and body STLs in this folder only.

## Files

- `Cece_head_V3_four_screw_joint_CANDIDATE.stl`: current integrated V3 head plus four internal descending tongues with blind screw pilots.
- `Cece_body_V4_four_screw_joint_CANDIDATE.stl`: current V4 body plus four shallow outside screw collars and clearance holes.
- `Cece_Head_Body_Four_Screw_Joint_CANDIDATE.FCStd`: FreeCAD inspection assembly with source-reference driver/OLED solids and screw envelopes.
- `build_and_check.py`, `mesh_validation.json`, `validate_freecad.py`, `freecad_validation.json`: regeneration and geometry evidence. `probe_joints.py`/`joint_probe.json` record the initial placement sweep.

## Joint geometry and assembly

Four candidate **M3 × 8 mm pan-head screws** enter from the left and right body sides at Y=±22.5, Z=−8 mm. The two screws on each side are at the front and rear of the torso; no screw approaches through the display or charger. A 1 mm high, Ø8 mm collar provides a seat on the outside of the existing 2 mm side wall. Body clearance holes are Ø3.3 mm. The head's internal tongues have Ø2.5 mm blind pilots; their nominal X range is ±26.5…±32.2 mm. At the screw positions, the body side wall occupies |X|≈32.5…34.5 mm, leaving **0.3 mm nominal clearance** to insert the tongues vertically before tightening. The pilots are 5.3 mm deep with a **0.5 mm minimum inner wall**, which is a thin feature requiring a real print-strength check.

Install all head wiring and the speaker lead first. Lower the head so all four tongues enter the body without forcing them. Align the four side holes and turn each screw by hand, alternately, until the head is seated; do not over-tighten printed PLA. The screws are intended to clamp the tongues against the inner body wall and allow later removal. Actual screw length, head style, torque and printed pilot sizing are unverified.

## What was checked

Both output STLs reimport as watertight single components; FreeCAD converts both to valid one-solid BReps. Head/body solid intersection is zero. Static mesh checks find zero solid intersection between either candidate and the current speaker pod/grille, UC2 tray/bezel, V3 heart frame, faceplate, arms, antenna, legs/feet and the provisional battery, UBEC, ESP, amp, mic, ultrasonic PCB and hip-servo boxes. The broad rectangular driver envelope overlaps the head by 6.511 mm³, **the same overlap inherited from the source V3 head**; FreeCAD checks the detailed partial PiicoDev STEP at the selected placement and finds zero overlap with head and body. The official Adafruit 4741 STEP likewise has zero overlap. Four Ø2 mm screw-core probes, Ø6 mm screw-head envelopes and Ø6.4 mm screwdriver approaches clear the relevant printed paths/other parts. The supplier PiicoDev STEP omits its physical USB-C/JST-SH connectors and mating cables.

## Remaining go/no-go test

Print a short full-circumference head-rim/body-top test set containing the four tongues and side walls at the final printer orientation. Use actual M3×8 screws. Confirm all tongues insert freely, all four holes align, and the screws seat without bottoming, stripping or cracking the 0.5 mm pilot web. Then attach a representative measured head/pod mass and repeat assembly/removal and pull/rock tests. Do not infer pull-out strength from the zero-clash CAD result. A true full-body print still needs the separate OLED/frame, sensor/LED, servo/horn and charging checks in `../ASSEMBLY_JOINT_AUDIT.md`.
