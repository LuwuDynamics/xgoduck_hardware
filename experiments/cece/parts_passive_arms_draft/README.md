# Cece cosmetic and passive-arm revision — prototype only

Files in this folder are in original assembled coordinates, not oriented or
arranged on a slicer plate. Use these two shell files in place of the earlier
head and body, and print one antenna and two identical arms for fit trials.
The remaining leg, foot, faceplate and OLED frame candidates remain in ../parts.
No final assembled print plate has been generated.

- Body: raised Cece lettering fused on front above the display; slotted pegs
  on the sides are candidate snap retention for freely swinging arms.
- Arm: 3.7 mm nominal hole around a 3.2 mm pin and a 4.2 mm end lip.
  Force, clearance, PLA flexibility, printing orientation and durability are
  untested. Arms swing freely due to gravity/inertia; no servo or linkage
  moves them. Their motion is not guaranteed when the robot walks.
- Antenna: decorative removable peg; 3.3 mm nominal opening on head, 2.9 mm
  peg. It is not a wireless antenna. Orientation and press fit need testing.
- Original URL glyphs were detected on the inside of the head crown and the
  outside of the torso rear. They were filled. The measured old glyph-level
  planar triangles are no longer present. Other components were not subjected
  to exhaustive optical text detection; no universal no-URL guarantee is made.
  Source and attribution remain in the project documentation.
- Head-to-body uses the inherited Otto retaining features; these have not been
  mechanically validated as a reusable snap joint. Feet attach to servo horns;
  moving joints cannot simply be snapped together without those servo parts.
- No charge connector cutout has been made. The ordered 2S LiPo requires a
  compatible 2S balance charging system; until its actual module/connector and
  location are selected, no dimensions or safe charging wiring can be final.
- Ultrasonic, microphone, OLED, speaker and board mounts remain unverified.
  Do not fabricate as final hardware or claim full electronic clearance.

`../design/build_passive_arms.py` regenerates the draft from ../parts. Requires
trimesh, numpy, manifold3d and the input name STL. `report.json` is a mesh
report, not an assembly or safety certification.

CAD check: with each arm centred at x = +/-37.2 mm, y = 0, z = -15 mm,
boolean intersections with the current head and body were zero at -90, -45,
0, 45 and 90 degrees about X. This omits legs, cables, sensor, electronics,
installation, flex, printer tolerance and dynamic movement; it is not a fit
or walking validation.
