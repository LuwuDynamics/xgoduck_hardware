# Cece rounded head and camera — engineering study

**Status: incomplete; do not print this as the finished robot.** This is the first
mechanical step toward the approved rounded concept, not a complete redesign or
proof of a working robot. The existing body, legs, feet, display frame and rear
charger cassette are still the earlier engineering candidates. No new robot STL
set is released by this study.

## What changed

- A rounded 84 × 79 × 55 mm head and separate rear cover replace the old head,
  faceplate and external speaker pod in the CAD study. The speaker volume moves
  inside the head behind a perforated rear cover. Shell thickness is 1.6 mm.
- The front has openings for the two existing ultrasonic cans, a trial centre
  camera lens and five LED positions. The existing antenna is moved to a
  centred roof hole. Four screw tongues match the separate body-joint study;
  four rear-cover pilot posts are included as provisional features.
- The 21 × 17.8 × 15 mm XIAO ESP32-S3 Sense published stack dimensions are
  represented by a **23 × 17 × 19.8 mm bounding box**, with the 15 mm dimension
  oriented front to back. The lens position, its ribbon, antenna and connector
  spaces are unknown. [Seeed's documentation](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)
  identifies different camera revisions; verify the exact one before ordering
  or making a mount. It is an additional controller and is not yet purchased.

## Checks and results

`build_study.py` reconstructs the model using FreeCAD 1.1, the previously
modeled parts and the provisional camera box. Its results are in
`camera_fit_results.json`. Shell and rear cover are valid single solids;
the explicitly modeled shell/component and camera/component pairs have no
volume overlap in the neutral pose. Rear-cover and body screw-core probes,
and rear screwdriver approach proxies, have no detected solid overlap. These
are geometry checks of the modeled shapes, not proof of screw grip or access
with actual tools. Existing component-to-component checks apply only to the
previously tested placement. The relocated speaker box also has no overlap
with the tested modules; it is only **1 mm** from the ESP32-C3 envelope, with
speaker terminals and cables unmodeled.

`analyze_balance.py` uses the existing measured sole polygons and original
nominal battery, UBEC, charger and four-servo masses. It substitutes the new
head, cover and modified body volumes and their exact solid centroids, assuming
all plastic is solid PLA (1.24 g/cm³). A sensitivity case adds an **assumed**
10 g camera and **assumed** 12 g speaker. See `balance_sensitivity.json`.
This case produces an incomplete 290.2 g subtotal, and neutral centre of mass
approximately 4 mm outside either individual foot. A lateral shift of around
9 mm gives a chosen 5 mm single-foot margin. This is static geometry, not a
walking simulation; board masses, wiring, mounts, supports and fasteners are
missing. PLA weight must eventually be determined using the actual slicer.

## Remaining work before release

1. Design the rounded torso and integrate the charger and power switch, while
   preserving access to the battery and the four existing SG90 servos. The
   purchased battery plugs and a compatible 2S balance charger remain to be
   identified and verified. The UBEC is not a charger.
2. Measure the actual SG90 cases, supplied horn and screws. Complete hip and
   ankle drive and retention; check motion, insertion, bending, print tolerance
   and load. The existing ankle sweep used simplified servo proxies.
3. Measure the chosen camera and its lens offset; add a retained mount and
   connector, ribbon and antenna clearances. Retain the sensor PCB, OLED, LED,
   speaker, driver, ESP, amplifier and microphone; model all actual cables.
4. Reduce head weight and check its walls and attachment against assembly and
   walking loads. The rear-cover and head/body printed pilots and the antenna
   peg need fit and strength tests. Determine print orientation and support
   requirements with the actual Bambu profile and sliced files.
5. Complete the power/wiring design and firmware, check the measured centre of
   mass throughout the gait, servo torque and current, 5 V voltage sag and
   stability. Then physically test an assembled prototype. No analysis currently
   proves that this robot walks or that the complete electronics fit.

The front preview is generated from the CAD shapes, not from the approved
photorealistic concept. It depicts provisional geometry with the old torso and
legs; it is a way to inspect the study, not a final aesthetic rendering.
