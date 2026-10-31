# Cece on Otto: consolidated prototype

**Want to run the current Windows simulation?** Start with
[the step-by-step ROS 2, Gazebo and voice guide](START_HERE.md).
The sections below include older historical studies and may describe
superseded firmware or appearance.

## Current engineering state — 29 October 2026

The newest mechanical/electronics candidate is in [`packaging_study/`](packaging_study/README.md). It has a replacement body for the chosen Adafruit 4741 OLED and proposed charge passage, a replacement head with a vertical PiicoDev servo-driver cable hood and rear speaker pod, a rear candidate USB-C balance-charger cassette, the SG90 ankle V2 joint, and wider feet. The full FreeCAD neutral-pose scene reports **zero modeled solid intersections** for its selected printed parts and explicitly sized electronic/connector envelopes. The neutral static balance result has an ideal two-foot margin but still requires a lateral weight shift for one-foot walking. **This does not establish actual part, plug, fastener, electrical or moving fit. Do not release the full print or charge the battery in the robot yet.** See the packaging and [latest balance](balance_study/LATEST_BALANCE.md) reports.

The older sections below document the path to that candidate and contain superseded parts and simulations. The MuJoCo viewer is for appearance/motion illustration only; the latest FreeCAD assembly and physical dry-fit procedure govern the current prototype.

## SG90 ankle V2 FreeCAD study

`ankle_v2/` contains revised left/right legs and feet, separate bearing washers,
optional servo shims, an editable FreeCAD assembly, and its exact-solid
interference results. It keeps the four purchased SG90 servos: two hips and two
ankles. The foot uses the supplied SG90 horn as the drive and a screw-retained
bearing on the opposite side. FreeCAD checks the printed parts and servo
envelopes at 5-degree intervals from -45 to +45 degrees. This is a mechanical
prototype: the actual horn, screws, case tolerances and powered movement still
need a one-ankle physical check before a final Cece print.

**Status: DEVELOPMENT ONLY. Not ready for final printing or battery operation.**

The goal is a fixed-head four-servo Otto with HC-SR04, LED face, 128x32 OLED,
INMP441 microphone, MAX98357 amplifier, 28 mm speaker, ESP32-C3 Super Mini,
PiicoDev 4-channel servo board and 2S LiPo. This folder supersedes the unrelated
Cece and Otto variants only for this experiment; it does not replace them.

1. `parts/`: candidate STL components for test fitting. Head uses ultrasonic
   openings and two relocated LED holes. Body has the OLED opening. Faceplate,
   body, legs, feet, and OLED frame are separate. The generic frame and speaker
   mount are not proven to fit the selected boards and cable connectors.
   STL geometry uses original OttoDIY v09 as source. The regenerated head and
   body are derived from https://github.com/Open-Hardware-Leaders/OttoDIY at
   commit 8cf3e784c734981c50143cfddde18a68685bcea3; see upstream LICENSE and
   attribution/redistribution requirements, especially before commercial use.
2. `simulation/cece_four_servo.gif` and `result.json`: new 10-second physics
   simulation with four actuators and fixed head. Visual shell is the modified
   head/body. Simplified boxes set contacts and mass; electronics, faceplate,
   battery, wires, actual servo force and physical fit are not represented.
   Upright simulation is not physical walking validation. Run with Python 3,
   numpy, mujoco and Pillow: `python simulation/simulate_cece.py`.
3. `electronics/WIRING_DRAFT.md`: proposed net connections, pin budget and
   component status; not an electrical sign-off.
4. `firmware/CeceBench/CeceBench.ino`: incomplete bench diagnostic draft,
   servo control is not implemented; disconnect servo power for tests. Audio remains
   unimplemented; board and pinout must be confirmed and code compiled/tested.

## Hard blockers to a finished build

- The current [installed-part CAD study](packaging_study/README.md) checks nominal printed shells, published component clearance boxes and the official OLED and partial servo-driver CAD. The real LiPo/servo/plugs, terminals, switch and moving wires are not yet dry-fitted.
- A rear-cassette ISDT UC2 balance-charger **candidate** and USB-C opening now exist in CAD. Its exact plugs, switch, load isolation, protection and wiring need physical verification; no charging USB cable may be connected to the pack except through a verified 2S balance charger with the robot off.
- No final fit, thermal, current, print tolerance, gait or hardware tests.
- ESP32-C3 board is generic: printed pin labels, boot pins, USB/5V backfeed,
  I2S/firmware and OLED connector must be checked on the actual items.
- No complete assembly or production-ready PCB schematic has been verified.

See `electronics/WIRING_DRAFT.md`. STL closed-mesh checks do not mean parts fit.


## Current cosmetic revision

`parts_passive_arms_draft/` contains a newer **test-only** head and body with
Cece name, two unpowered swinging arms and a decorative antenna. It supersedes
only the corresponding older shell candidates in `parts/`. The old simulation
still uses the previous shell and does not display these new parts. Its snap
pins and head joint require fit testing. No charging socket or charge circuit
has yet been finalized. Refer to that folder's README before printing.

Interactive viewer: install the dependencies in `simulation/requirements.txt`,
then run `python simulation/view_cece_live.py`. It displays the newer draft
body, antenna, faceplate, OLED frame and free-moving arms. The arms use assumed
joint parameters, contain no collision contacts, and are not physically tested.
The viewer automatically resets after 10 seconds or a fall; close it to stop.
The old recorded GIF and numeric result are from the previous shell revision.

## Happy-face update

`parts_happy_draft/` is the newest prototype: centered antenna, rounded body,
smiling three-LED face and separate outward 45-degree passive arms with round
hands. Use its head and faceplate together. The live MuJoCo viewer shows this
revision and uses colored placeholder shapes for LEDs, sensor and display;
it does not simulate the electronics or prove real-world motion. See the
folder README for measured CAD checks and unresolved fit/charging work.

## Heart-front revision

`parts_heart_draft/` is the latest appearance: five mouth LEDs, heart-shaped
frame around the rectangular OLED, and raised Cece name on the back. The
front and back previews are `simulation/cece_heart_front.png` and
`simulation/cece_heart_back.png`. The heart is a colored preview; print color
requires filament choice or painting. All electronic mounting, charger and
physical fit cautions still apply; see that folder's README.

## Display selection change — 28 October 2026

Core cart now contains Adafruit 4741, 1.5-inch 128x128 grayscale SSD1327 OLED,
instead of the previously selected 0.91-inch SSD1306. The current heart bezel,
body window, screen placeholder and OLED firmware are STILL FOR THE OLD 0.91
INCH SCREEN. They do not fit or support the new display and are not ready for
printing or use. A new mounting layout must establish the actual 4741 board,
active window, connector and fastener geometry and check battery/servos.
The display uses I2C STEMMA QT and needs an SSD1327-compatible Arduino library;
the existing SSD1306 sketch is not compatible. Current rear name is lowercase
`cece`. Preview at `simulation/cece_lowercase_back.png`.

## Waveshare square OLED concept

The cheaper candidate is Waveshare WS-13992 1.5-inch SSD1327 (Little Bird
cart). `parts_waveshare_draft/` contains an unverified external heart frame and
body opening for it; see its README and fit report. The latest live preview
shows this concept. It does not show all electronic parts or confirm fit.
The module ships in SPI mode; I2C configuration needs SMD rework, so it does
not currently satisfy the simple, no-SMD-rework wiring goal. Wiring/firmware
and charger are unresolved.

## Adafruit prototype and wiring review

The Core cart selection is Adafruit 4741. `parts_adafruit_draft/` is the
latest geometry concept, includes URL-cleaned feet and a preliminary mass and
battery-envelope check. It is not fit-confirmed or ready for final printing.
See `parts_adafruit_draft/README.md`, its JSON reports, and
`electronics/ADAFRUIT_CONNECTION_SCHEDULE_DRAFT.md` for the current wiring
proposal. The earlier `WIRING_DRAFT.md` and Waveshare folders are historical.
