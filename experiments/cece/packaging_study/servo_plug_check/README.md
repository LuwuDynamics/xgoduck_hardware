# Cece servo-plug packaging study

Status: **CAD candidate, not physical-fit certified.** The selected placement below uses the available hardware and keeps the decorative antenna centered. It includes a new printable head with an internal cable hood. Servo connector housings, USB-C/JST-SH mating plugs and cable bends remain dimensional proxies because the purchased SG90 and PiicoDev STEP do not provide those complete CAD shapes.

## Installed coordinates (mm, original Cece assembly axes)

| Item | Center | Envelope / orientation |
|---|---|---|
| PiicoDev CE09181 | (+1,+13,+13) | Official partial STEP, upright in XZ, servo pins facing head front (−Y) |
| ESP32-C3 SuperMini | (0,+24,+10) | 28×8×21 allowance, upright in rear head |
| Audio amp | (+17,−5,+24) | 22×22×6 allowance |
| Microphone board | (−14,−5,+24) | 16×16×6 allowance |
| Hobbywing UBEC | (+2.3,0,−8) | 21×56×14 rotated clearance envelope |
| Dualsky battery | (0,+3,−24) | 35×56×16 rotated clearance envelope |

Four PiicoDev 3-pin header centers after the transform lie at x≈+0.956, y≈+6.85, z≈+5.38,+10.46,+15.54,+20.62. The front-facing mated servo plug proxy has nominal footprint 9.6×3.2 mm and 18.15 mm straight depth (deliberately conservative). All four proxies clear the modified head and its centered antenna.

Use one lower USB-C socket for servo power and one upper PiicoDev JST-SH socket for I2C. The other duplicated sockets can remain unplugged. The lower USB-C straight-service proxy clears the shifted UBEC. The upper JST-SH proxy needs an upward route through the modified head's raised roof duct. The roof duct runs x=7.8..20.8, y=7..31, z=27..40 mm, with a 9×20 mm internal channel that lets the wire turn rearward toward the ESP. The centered antenna base at x,y≈0 does not intersect it.

## Files

- `Cece_head_vertical_driver_hood_CANDIDATE.stl` — valid watertight, one-piece print candidate, 24,292.392 mm³ solid volume.
- `Cece_Vertical_Driver_Service_Hood_CANDIDATE.FCStd` — editable FreeCAD study.
- `build_service_hood.py` — generates both files in FreeCAD Python 1.1.
- `refined_candidate.py` and `validate_final_integration.py` — BRep checks. The final V4 body, head, speaker pod and grille, antenna, OLED frame, driver STEP, selected connector corridors, SG90 plug proxies, ESP, battery, UBEC, amp, mic and front ultrasonic PCB gave **zero volume overlaps** at this pose. See `final_integration_results.json`.
- `check_freecad.py` — shows why the previous horizontal ESP position failed: it intersects three mated servo-plug proxies.

## Sources and limitations

The PiicoDev PCB/partial STEP derives from [Core Electronics' hardware source](https://github.com/CoreElectronics/CE-PiicoDev-Servo-Driver); `../reference/README.md` records the revision and model gaps. [Core's setup guide](https://core-electronics.com.au/guides/piicodev/piicodev-servo-driver-pca9685-getting-started-guide/) describes connecting power through one USB-C connector. A separately sold [Futaba 3-pin female housing](https://www.mg-modellbau.de/Allgemeines-Zubehoer/Servokabel/Futaba-Servo-Buchse-Stecker---female--Pin-3-St-Basic-014-035-mm%C2%B2-Bausatz.html) is 14×9.6×2.7 mm; that is only a proxy for the actual SG90 plug. The purchased Rapid Robotics servo page specifies the motor but not the plug's shape or USB-C/JST-SH mated dimensions.

A zero-volume intersection can mean touching. There are no finished mounting posts for PiicoDev, ESP, amp or microphone; the 0.5–1.5 mm gaps near some electronic modules are not mounting allowance. Horns, fasteners, module cables, wire bend radius, heat, battery service, controller USB access and movement have not been physically tested. This is a first packaging candidate, not a release-ready print set.

## Clearance follow-up (frozen hood and V4 body)

`clearance_sweep.py` and `driver_forward_probe.py` probe small position changes. Rearward ESP travel from y=24 to y=24.5, 25, 26 mm increases driver gap from 0.85 to 1.35, 1.85, 2.85 mm, but overlaps the exact hooded head by 4.035, 24.211, 64.563 mm³ respectively. Moving the driver forward from y=13 to y=11.8 raises the driver–ESP gap to 2.05 mm, while the upper JST-SH 10 mm service box intersects the fixed hood roof by 58.568 mm³. With the current hood, no tested simple Y translation gives both ≥2 mm driver–ESP gap and zero roof overlap.

Moving UBEC down 1 mm makes its driver gap 2.3 mm but leaves no gap to the battery. Moving the battery down 0.5/1 mm intrudes into two 1 mm-wide structural side rails in the V4 body by 56/112 mm³. With the original conservative clearance envelopes and fixed body, the current battery–UBEC and UBEC–driver 1.0/1.3 mm gaps cannot both be improved to 2 mm by Z translation alone. Modifying these rails or the head cable hood would be a separate CAD revision and must be assessed for structure and physical assembly.

## V2 roof duct and improved driver spacing

`Cece_head_vertical_driver_hood_V2_CANDIDATE.stl` is a separate CAD candidate; the earlier V1 head remains unchanged. V2 extends the outer hood 1.2 mm forward (Y front 5.8 mm) and its inner cable channel to Y=7.8 mm while preserving a 2 mm front wall. This permits the PiicoDev STEP to move from Y=13 to **Y=11.8 mm**. With ESP vertical at (0,24,10) and amp moved to (17,−6,24), `validate_v2.py` reports zero volume intersection against the V4 body, hooded head, speaker pod/grille, antenna, OLED frame, sensor PCB, driver, ESP/amp/mic envelopes, battery, UBEC, all four servo plug proxies and selected power/I2C service corridors. Driver–ESP distance improves to **2.05 mm** and driver–amp to **2.33 mm**. The existing 1.0–1.3 mm power-module gaps remain.

The V2 hood head still contains the earlier **4 mm speaker wire opening**. It must not be paired with `speaker_pod/plug_passage_v2` as though the enlarged speaker connector passage were already present. Merge the speaker passage and this roof hood into one head model, then rerun geometry and physical tests. Neither printed head candidate is ready for final production.
