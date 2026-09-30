# Build and first-power workflow

[Project](../readme.md) · [BOM](BOM.md) · [Print inventory](PRINTING.md) · [Troubleshooting](TROUBLESHOOTING.md)

Use this guide alongside the [25-page assembly PDF](../Assembly_Guide.pdf). The PDF's photographs determine orientations and cable routing. The sequence below adds preparation and inspection checkpoints; it does not invent missing torque values, connector polarity or mechanical-zero drawings.

## 1. Establish a matched build

Record the hardware, runtime and RL revisions you use. Inventory the BOM, identify every printed part and check the actuator model. Obtain the battery/power details in [BOM.md](BOM.md) before powering the board. Keep a multimeter, the appropriate screwdrivers, cable labels and a stable robot support available. Choose print settings only after validating fit on a representative bearing/servo interface.

## 2. Prepare the board and individual servos

Inspect the assembled expansion board against `PCBA/ArduinoUnoQ.pdf`, including component orientation and shorts. PCB fabrication settings and a tested board bring-up procedure are not yet supplied; have the board reviewed before connecting the controller or servos.

Deploy the [runtime](https://github.com/LuwuDynamics/xgoduck_runtime_arduino) on Uno Q before configuring servos. Connect **one servo at a time**. In Servo setup, assign unique IDs 10–14, 20–24 and 30–34, center at raw 2047, then write stored gains according to the runtime guide. Label each servo. Duplicate IDs can receive the same write.

## 3. Follow the assembly drawings

| PDF pages | Focus and checks |
| --- | --- |
| 1 | Servo ID placement. Match physical labels to the photos before installing. |
| 2 | Secondary shafts: retain on IDs 30 and 31. Removal on 10, 20 and 32 is optional per the guide. Do not remove the output shafts. |
| 3–5 | Initial structure and cable routing. Page 3 explicitly delays screw installation. Follow the pictured sequence. |
| 6–10 | Leg assembly. Connect cables before the indicated joints become enclosed; left/right orientations differ on page 8. |
| 11–15 | Feet and sole assembly. Page 11 calls out the 10 × 15 × 3 bearing and M2.5 × 6 screw; page 14 also calls out M2.5 × 6. Check the TPU sole direction on page 15. |
| 16–20 | Head/neck mechanism around IDs 32–34. Connect the bottom cables before closing the assembly on page 17. |
| 21 | Adhesive operation shown in the drawing. Adhesive type/cure time are not specified; confirm material compatibility. |
| 22–23 | IDs 30/31 and the M3 × 16 screw locations. |
| 24–25 | Follow final pictured assembly and inspect the completed routing. |

Before closing each section, check that the harness cannot be pinched and has slack through the intended movement. Compare mirrored parts to the photos; do not assume left and right mountings are identical. Do not force printed bearing seats or infer tightening torque from screw size.

## 4. Inspect before enabling motion

- All 15 unique IDs answer; the mouth is ID 34.
- Mechanical assembly matches the PDF and cables clear the joints.
- Polarity and supply limits have been confirmed from the matched hardware revision.
- The robot is supported with joints clear of hands and obstructions.
- The runtime reports fresh MCU feedback and a working IMU.

## 5. Calibrate, then test in stages

Use the runtime calibration procedure. Starting calibration commands the servos to raw 2047 and can move them. Factory zero values are a reference from another assembly, not a substitute for calibrating your robot. A per-joint mechanical-zero photo set is still needed for unambiguous first-time reproduction; obtain it before completing zero calibration.

Back up `data/zero_pos.json` privately. Start with inference only, then a supported default-pose test, then low-command walking on a clear level surface. Check torque-off behavior before testing pick or recovery. A torque-off robot can collapse; use a support. Stop on unexpected direction, binding, heat or unstable feedback and diagnose before retrying.

## Record your build

Record printer/material/profile, board revision, servo supplier/firmware, power pack, three repository commits, policy hashes, calibration date and motion-test observations. These details make a useful issue report and let another maker repeat your result.
