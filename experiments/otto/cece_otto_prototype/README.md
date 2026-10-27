# Cece on Otto — prototype parts

Open `Cece_Otto_Prototype.FCStd` in FreeCAD 1.1. This local prototype uses
the actual OttoDIY v09 head, body, leg and foot meshes from
https://github.com/Open-Hardware-Leaders/OttoDIY at commit
`8cf3e784c734981c50143cfddde18a68685bcea3`; see that project's licensing
and attribution requirements before redistributing any adapted files.

## Created so far

- Modified Otto torso with a belly OLED opening, four retainer screw holes,
  a small wire pass-through, and two provisional AA-holder support ledges.
- A **separate external OLED frame** and rear-cover test part, sized around
  the Adafruit 4440 board's published 35 × 20 × 4 mm envelope. The frame is
  mounted outside the torso because an internal position overlapped Otto's
  existing structure. Connector and solder clearance remain unverified.
  The rear cover is a separate bench/retention concept; it is not shown in the
  assembled preview and must not be assumed to fit between frame and torso.
- Modified Otto head and a separate faceplate. Two nominal 5 mm eye LEDs fit
  the faceplate over Otto's original eye openings. Three nominal 3 mm mouth
  LEDs and a microphone sound hole have matching head openings. Locator rings
  sit in the eye holes; actual LED bodies, lips and tolerances must be tested.
  A rear grille and inner locating rim are sized for an Adafruit 1890 28 mm
  speaker; the rim needs a separate retainer to hold the speaker.
- Raised `Cece` lettering, separately exported as four disconnected letters.
- The original mirrored leg and foot meshes retained for visual context.

The 2-AA holder ledges assume the [Pololu 1150](https://www.pololu.com/product/1150/)
59 × 32 × 15 mm holder. A simple holder envelope, the faceplate, and the
externally positioned display frame were checked for volume intersections
with their corresponding shell. These are static envelope checks only. The
holder has no retaining strap and no cable or contact access check. A holder
shape that clears the shell can still collide with a servo or its wire. A
28 × 4.5 mm speaker envelope clears its proposed position in the head, but
the speaker terminals and fastener are not modelled.

## Incomplete — do not print as a finished build

There is no completed fifth-servo mount, rotating head bearing, head coupling
or flexible wire loop. Original Otto head tabs may conflict with head rotation.
The ESP32-C3, amplifier, power converters and switch do not have
verified mounts, openings or wiring paths. LEDs have no wiring/firmware yet.
No motor, installed-board, servo-sweep, cable bend, screw fit, power-current,
balance or walking validation has been done for this revision.

The colours on the preview show visual LED and OLED placeholders, not
purchased components. M2 clearance holes in the torso and nominal M2 pilot
holes in the frame are starting sizes, not tested thread specifications.
The original torso mounts for four Otto leg servos remain in the source mesh,
but they have not been checked against the chosen servo or new battery ledges.

`geometry_checks.json` reports watertightness only. `Cece_Name_Letters.stl`
contains four separate shapes. `build_cece_otto.py` regenerates modified mesh
parts; `open_cece_otto.FCMacro` builds the FreeCAD visual assembly. Board
dimensions are assumptions based on the cited model and need measurement.
