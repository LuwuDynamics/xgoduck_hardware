# cece Adafruit 4741 concept — NOT FINAL PRINT FILES

This folder contains the latest conceptual shell/heart screen mount and two
clean-foot candidates. The body is 69 mm square and 39 mm tall before pins;
the nominal pose including feet, arms, antenna, front display frame and rear
name measures approximately 120.4 x 79.2 x 139.0 mm (width x depth x height).
The feet, head, torso, heart frame and antenna are only one geometry pose; an
actuated movement envelope has not been checked.

The new concept allows a rotated 47.0 x 35.56 mm Adafruit 4741 PCB envelope,
with 48 x 36.56 x 6.8 mm pocket assumed and 30.2 mm square viewing opening.
Board outline is derived from Adafruit's published Eagle board; the named
OLED package footprint has a 29 x 26.85 mm dashed rectangle, whose center is
not at the board center. Consequently this simple centered window may clip the
active panel; the proposed 90-degree orientation and software rotation,
connector clearance and a board retainer require engineering and real parts.
Frame-to-body mesh intersection is zero at the nominal placement, but there
are no finished frame latches or physical mounting method. The extra opening
removes about 174 mm³ of material behind the nominal front wall, which may
include servo support. Servo mounts must be checked before this body is printed.

`geometry_mass_report.json` calculates mesh dimensions and solid plastic
volumes. At a nominal PLA density of 1.24 g/cm³ the *100%-solid geometric*
mass of the 11 listed components is 130.85 g. This is not the required
filament mass: walls, infill, support, brim, purge, filament density and
slicer settings all affect the result. No slicer estimate was obtained.
All listed meshes were watertight single components at this check.

The 53 x 32 x 13 mm battery test box clears the printed body at some sampled
positions, but only shell material was checked. Motors, wiring, screen,
controller board, UBEC, fasteners and charging hardware were not included.
No whole-assembly fit or center-of-mass/stability confirmation is possible.

A 10-second MuJoCo run in `../simulation/adafruit_proxy_motion_result.json`
did not fall in a simplified proxy model with an assumed 215.2 g mass. Battery,
actual electronics, measured servo characteristics and detailed collision
geometry are absent, so this does not prove real cece will balance or walk.

Website glyphs were identified and filled on the two foot soles, inside the
head and on the body rear. Cleaned foot STLs are in this folder; source Otto
STLs and earlier Bambu projects are unchanged and may retain old markings.
No exhaustive optical scan of every tiny feature was completed. Keep upstream
attribution in documentation.

Print inventory for trials: body 1, head 1, faceplate 1, heart frame 1,
antenna 1, left arm 1, right arm 1, original mirrored and unmirrored legs 1
each from ../parts, cleaned feet 1 each. Name overlay is preview-only. The
snap pins, head latch, fastener strategy, charger and display retainer remain
untested/unfinished. Do not use the old Otto Simple Bambu project as the cece
final print plate.
