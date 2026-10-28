# Cece UC2 rear charger cassette — front-to-back candidate

The [ISDT UC2 charger](https://www.isdt.co/uc2-2.html?lang=en) measures **39.6 × 19.8 × 9.5 mm** and has its battery XH balance socket and USB-C input at opposite short ends, as shown in [ISDT's product photograph](https://www.isdt.co/wp-content/uploads/2023/11/UC2-2.png). This candidate puts its 39.6 mm axis along Cece's rearward **Y axis**, with the XH end facing a body passage and the USB-C end exposed through a rear bezel. The exact positions and shapes of both sockets and the user's plugs have not been measured, so the openings are provisional.

## Printable files

- `cece_body_with_charger_posts_CANDIDATE.stl` — replacement V3 Adafruit 4741 body with four integral mounting posts and a reinforced balance-lead duct. The source V3 body is untouched.
- `removable_tray.stl` — charger cradle, X = ±13.9 mm, Y = 39.5–85.1 mm, Z = −32.75…−15.25 mm before its mounting ears.
- `retaining_bezel.stl` — rear module retainer at Y = 85.1–87.1 mm, with a **16 × 7.5 mm provisional USB-C access window**.

`Cece_UC2_charger_cassette_candidate.FCStd` includes the body reference, replacement body mesh, FreeCAD solids for posts/duct, tray and bezel, and a rectangular charger envelope. `build_freecad.py` builds the solids with FreeCAD 1.1; `validate_meshes.py` fuses/cuts the replacement body and writes `mesh_validation.json`. Re-run `build_freecad.py` after validation so the FreeCAD project includes the newest replacement body mesh.

## Cable and fastener path

The assumed charger body lies at X = ±9.9, Y = 43.5–83.1, Z = −28.75…−19.25 mm. Its cavity is X = ±11.9, Y = 41.5–85.1, Z = −30.75…−17.25 mm: **at least 2 mm beyond each module face**. The rear USB-C bezel does not enter that allowance. A 14 × 12 mm opening runs through the V3 body wall and the tray front at X = ±7, Z = −30…−18 mm; a 2 mm wall surrounds the passage through the 5 mm stand-off gap. The battery balance lead can in principle reach the charger's front end, but the actual XH connector and its cable bend still require a fit check.

Four M3 × 10 screws attach the tray to blind Ø2.5 mm pilot holes in the replacement body posts at X = ±18 and Z = −30 or −18 mm. The ears are accessible from behind along the sides of the narrow tray. Two M2 × 5 screws fasten the rear bezel to separate rear tabs at X = ±18, Z = −24 mm. These screw dimensions are provisional for printed PLA: test pilots on a scrap piece, and do not drive a screw through the body wall. Remove the bezel to access the charger body. The old wide, sideways tray is superseded by these files.

## Geometric results and remaining gates

`mesh_validation.json` records exact mesh Boolean tests. The replacement body, tray and bezel are each watertight single solids. The charger rectangle, body-to-cassette lead passage, rear USB opening, four mounting screw cores, screw-tool approaches and two bezel screw cores have no solid interference with their printed paths. The tray has no solid overlap with the V3 body, head, speaker pod/grille, rear `cece` name, neutral legs or feet. A sampled estimated hip sweep from −45° to +45° in 5° increments also found no tray/leg volume overlap. That is not a load test or a guarantee of positive clearance at every intermediate position.

The 45.6 mm long cantilever behind the body and the added charger mass shift the robot's weight rearward. Real battery connector fit, USB-C plug access, strain relief, charging isolation from the running robot, post strength, thermal behavior, print tolerances and walking balance still need physical checks before powered charging in the robot. The UC2 specifies a fixed 0.8 A charging current; check that the actual battery permits this rate.
