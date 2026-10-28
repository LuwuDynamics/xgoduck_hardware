# Cece happy revision — experimental parts

- Centered, decorative antenna; no electrical function.
- Four body vertical corners rounded to nominal 5 mm radius. The shape is not
  validated against internal servos and electronics.
- Three mouth LEDs use raised corners and a lower center to suggest a smile;
  ultrasonic openings remain clear, and the two outer LEDs remain in place.
- Separate left and right 45-degree outward arms with larger rounded hands.
  Each arm remains passively hinged about the original side pin axis.
- Each STL is watertight and has one connected component. At -90, -45, 0, 45,
  90 degrees, boolean intersections of each installed arm with head/body were
  zero. This excludes legs, internal components, flex, cables and clearances;
  it does not test whether the snap pin will survive printing or installation.
- Charge socket and 2S balance charging are not selected or incorporated;
  OLED, sensor, board and battery fit remain unverified. Do not use as final
  printable assembly without fit trials.
- Use happy base OLED frame/cover and original legs/feet with these files.
  The head and matching happy faceplate replace both older versions together.

Regenerate by running design/build_happy_base.py then design/build_happy_cece.py;
requires numpy, trimesh and manifold3d. Attribution is in the project README.
