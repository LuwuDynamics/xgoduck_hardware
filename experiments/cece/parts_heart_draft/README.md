# Cece heart-front revision — prototype

This is the latest appearance revision. The heart-shaped OLED frame is a
separate piece, not a screen shaped like a heart: the selected rectangular
0.91-inch OLED shows through its rectangular central window. Its prior frame
and board slot were retained beneath the new front fascia; lower corners of
that backing are visible. Connector, screw and physical board fit remain
untested. Name lettering is fused to the back of the body; the visual-overlay
STL is for the MuJoCo color preview and is not an extra part to print.

The head and faceplate have five 3 mm mouth LED holes in a lower scattered
smile; the two ultrasonic openings and two outer 5 mm LED holes remain. Use
this head and its matching faceplate together. Wiring for the extra LEDs and
GPIO/driver budget must be revised before assembly.

Seven printable parts in this folder are each one watertight component. At the
nominal frame location, the body and heart frame had zero intersection volume.
This is a static mesh check; it does not establish clearance for screws,
sensor, screen connector, battery, servo motion, wiring, charger or assembly.
No charging socket or 2S charging circuit is designed. No complete fit or
physical tests have been performed; these files are prototypes.

Regenerate with design/build_heart_base.py followed by
 design/build_heart_cece.py (numpy, trimesh and manifold3d required).
