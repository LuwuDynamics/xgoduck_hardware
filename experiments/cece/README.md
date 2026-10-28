# Cece on Otto: consolidated prototype

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

- No installed-part CAD fit check exists for the LiPo, driver, four servos,
  UBEC, speaker, microphone, amplifier, wires, terminals or charging hardware.
- 2S balance charging, port location, isolation, protection and connections
  are not designed. No charging USB connector may be connected to the battery.
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
