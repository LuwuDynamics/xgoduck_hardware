# Cece provisional static balance scenarios

Run `python experiments/cece/balance_study/interim_static.py` from the repository root for the first, blocked layout. It reads `interim_inputs.json` and writes `interim_static_results.json`. Run `python experiments/cece/balance_study/interim_static.py --input experiments/cece/balance_study/interim_relocated_inputs.json --output experiments/cece/balance_study/interim_relocated_results.json` for the rotated battery/UBEC layout. Both use the current candidate STL shells, ankle V2 parts and optional wider feet. The sole support polygons come from the actual bottom STL vertices; plastic mass and centroid come from exact STL tetrahedron volume with nominal 1.24 g/cm³ solid PLA.

The first layout is **a mathematical mass scenario, not a physically possible assembled layout**. The battery clearance box at `(0, -3, -24)` mm overlaps **each hip servo case envelope by 3164.8 mm³**; its UBEC box overlaps each hip case by **60.2 mm³**. These values are calculated from the recorded box dimensions and centres when the script runs. The hip servo centres are inferred from body geometry and have not been fitted with the purchased servos.

The calculation includes the V2 heart frame and six purchased items: 35 g Dualsky battery, 21 g Hobbywing UBEC and four 9 g SG90s. These are supplier-listed masses carried in the repository, not individually weighed. Battery and UBEC candidate centres are `(0, -3, -24)` and `(0, 13, -8)` mm. The two ankle SG90 case proxies are centred at `(±25.5, -3.5, -62)` mm in `ankle_v2/freecad_fit_results.json`; the hip case proxies are `(±25.5, -5.5, -24)` mm, inferred from the underside body pockets in `packaging_study/hip_servo_probe.py`. A box centre is not necessarily the motor's true mass centre.

| First layout, neutral pose | Existing feet | Wider candidate feet |
|---|---:|---:|
| Nominal fully solid printed shells with V2 frame | 129.061 g | 136.429 g |
| Shells plus the six listed purchased items | 221.061 g | 228.429 g |
| Included-item COM, X/Y/Z | (0.129, -0.025, -32.784) mm | (0.125, -0.024, -34.515) mm |
| COM height above sole | 56.236 mm | 54.505 mm |
| Minimum two-foot support margin | +31.975 mm | +31.976 mm |
| Left-foot-only support margin | -15.129 mm | -4.125 mm |
| Right-foot-only support margin | -14.871 mm | -3.875 mm |
| Lateral COM shift for 5 mm reserve on left foot | 20.129 mm | 9.125 mm |
| Lateral COM shift for 5 mm reserve on right foot | 19.871 mm | 8.875 mm |

The second layout rotates the battery clearance box to 35 × 56 × 16 mm at `(0, +3, -24)` mm and the UBEC clearance box to 21 × 56 × 14 mm at `(0, 0, -8)` mm. Its ideal battery, UBEC and hip-servo boxes have **zero mutual intersection**. This removes the first layout's specific clash, but does not establish fit for the selected charger, other boards, connectors or wires. The shell mass and X/Z balance are unchanged because the same masses remain at the same X/Z coordinates; moving battery and UBEC in Y changes the included COM Y to `-0.310` mm with existing feet and `-0.300` mm with wider feet. The two-foot margins become `+31.690` and `+31.700` mm. One-foot margins and required lateral shifts remain the values in the table. The rotated boxes still need exact shell and accessory clearance checks and a physical fit test.

Positive support margin means the COM's vertical projection lies inside the ideal flat sole polygon; negative means it lies outside. Thus both foot options have a theoretical neutral two-foot support area, but neither can hold a **motionless neutral-pose** one-foot stance with the included mass scenario. Wider soles reduce the required lateral shift by about 11 mm. The 5 mm reserve is an analysis criterion, not a validated safe margin. The listed shifts are projected-COM translations, not joint angles or proven servo commands. For illustration only, rigidly tilting a body of the reported COM height would require about 19.5–19.8° with existing feet, or 9.3–9.5° with wider feet. The four-joint robot can shift its COM differently and may lack clearance or torque for such poses.

At the centred one-foot pose the simple quasi-static model gives **zero outward lateral acceleration budget** because the COM is already outside the planted foot. This says nothing about actual walking speed. A dynamic proof needs the time-varying body and joint poses, active ground contact, acceleration, angular momentum, floor friction, voltage under load and measured SG90 torque/current. The existing MuJoCo proxy animation does not establish these.

The charger, ESP32-C3, servo driver, OLED, HC-SR04, microphone, amplifier, speaker, LEDs/resistors, switch, connectors, wires, fasteners and mount features are **not included** in the 221/228 g totals. The candidate charger estimate of 6 g is intentionally excluded because the part is unpurchased/unselected. Actual sliced or weighed print masses are also missing; 100%-solid geometric mass is not FDM filament consumption. For a real assembled COM, replace every nominal mass and provisional centre with weighed parts and their measured or final CAD locations, then rerun the static calculation at every gait pose and test the hardware.

## Third scenario: V3 body, charger cassette and wider feet

Run `python experiments/cece/balance_study/interim_static.py --input experiments/cece/balance_study/interim_cassette_inputs.json --output experiments/cece/balance_study/interim_cassette_results.json`. This scenario replaces the older body with `packaging_study/charger_cassette/cece_body_with_charger_posts_CANDIDATE.stl` and the V2 heart frame with `packaging_study/Cece_Heart_Frame_4741_WindowV3_CANDIDATE.stl`. The V3 frame is already in assembled coordinates; it is **not** translated a second time. The `removable_tray.stl` and `retaining_bezel.stl` are included as additional printed solids at their native assembled coordinates. Only the wider-foot STLs are used.

The same 35 g battery, 21 g UBEC and four 9 g SG90 masses remain at the rotated candidate centres. A **6 g estimated, unpurchased ISDT UC2 charger** is added at `(0, 48.25, -24.2)` mm, the centre of the cassette's rectangular charger envelope. The script computes zero overlap among the battery, UBEC, charger and hip-servo **boxes**; the cassette's separate mesh check reports zero nominal intersections with body/head/neutral legs and its charger envelope. Neither check establishes USB-C or battery balance-lead access, actual charger mass, printed clearance, fastener strength, heat, retention or a complete mounted assembly.

| V3 cassette scenario, neutral pose, wider feet | Calculated value |
|---|---:|
| Nominal 100%-solid printed plastic, including V3 body/frame and tray/bezel | 150.858 g |
| Listed battery + UBEC + four SG90s | 92 g |
| UC2 candidate mass estimate | 6 g |
| Included total, **not final robot mass** | 248.858 g |
| Included-item COM, X/Y/Z | (0.066, 3.589, -33.671) mm |
| COM height above sole plane | 55.349 mm |
| Minimum ideal two-foot support margin | +28.411 mm |
| Left-foot-only neutral margin | -4.066 mm |
| Right-foot-only neutral margin | -3.934 mm |
| Lateral COM shift for 5 mm reserve, left/right planted | 9.066 / 8.934 mm |

The rear tray, bezel and charger move the neutral COM rearward relative to the second wide-foot scenario, but it remains within the ideal two-foot polygon at rest. The centred COM still lies outside either individual sole. The equivalent *rigid-body* tilt to shift the COM projection to a 5 mm single-foot reserve is about 9.30° left or 9.17° right; those angles are geometric illustrations, **not** a validated four-servo gait. The ESP32-C3, servo driver, OLED, ultrasonic board, microphone, amplifier, speaker, LEDs/resistors, switch, wires/connectors, screws, charging leads and actual FDM print masses are still missing from the 248.858 g calculation. In particular, the charger mass and its USB/balance-lead routing must be replaced with measured hardware data before a complete balance or walking assessment.
