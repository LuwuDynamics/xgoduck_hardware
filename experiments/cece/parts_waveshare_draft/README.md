# cece square OLED concept: Waveshare WS-13992

Status: **concept only; NOT an assembly-ready print**. This revision uses a
27.8 x 27.8 mm window and a nominal 45.5 x 38 x 6.8 mm pocket for the
Waveshare 1.5 inch display. Published board envelope 44.5 x 37 mm and active
area 26.86 x 26.86 mm; location on board, module thickness and clearance are
assumptions. Heart shape and larger OLED window were updated in the STL. At
nominal assembly position, the frame and body had zero intersection volume.
Both are single watertight meshes. This is not a hardware fit check.

There is **no designed frame attachment, display retainer, cable route or
connector clearance**. Existing servo mounting material may be affected by
the enlarged opening: no check of installed servos and wiring was done. Also
no 2S charging socket, charging circuit or battery fit validation. Do not
print this as the final robot until these are resolved and test-fitted.

Waveshare 13992 ships in SPI mode according to manufacturer documentation.
To use I2C, the module requires a surface-mount configuration change; confirm
actual revision and soldering work before proceeding. The supplied cable is
7-pin PH2.0, not the 4-pin PiicoDev/STEMMA QT cable. The robot wiring and
firmware are not updated; ESP32-C3 pin budget and exact SSD1327 mode require
validation. Do not assume it is plug-and-play or use old SSD1306 firmware.
https://docs.waveshare.com/ESP32-Arduino-Tutorials/I2C-Communication

Little Bird cart currently has this OLED; Core cart retains the other parts.
Sources: https://littlebirdelectronics.com.au/products/128x128-general-1-5inch-oled-display-module
https://zaitronics.com.au/products/1-5inch-oled-display-module-128x128

Run ../design/build_waveshare_concept.py with numpy, trimesh and manifold3d
to regenerate; it uses the previous `parts_heart_draft` as input. Overlay STL
for the rear name is visual-only, not an additional print. Use corresponding
head, faceplate, arms and antenna candidates from this folder; original legs,
feet and prior prototype cautions apply.
