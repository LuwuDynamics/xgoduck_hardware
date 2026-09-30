# XGO Duck Hardware

XGO Duck is a biped duck robot built on the [Arduino Uno Q](https://docs.arduino.cc/hardware/uno-q/). This repository contains the parts needed to build it: printable structure, the expansion board, the bill of materials, and the assembly guide.

Walking, get-up, and pick policies, plus the Uno Q firmware and web UI, live in [xgoduck_runtime_arduino](https://github.com/LuwuDynamics/xgoduck_runtime_arduino).

## Notice

The duck shape, the 15-servo joint layout, and the joint order used by the policies come from [Microduck](https://github.com/pollen-robotics/microduck) by [Pollen Robotics](https://pollen-robotics.com/microduck/).

This repository is Luwu Dynamics' hardware for Arduino Uno Q. Relative to Microduck, it makes these changes:

- The controller is an Arduino Uno Q: Qualcomm Linux on one side, an STM32 on the other.
- The actuators are fifteen Feetech 1910 servos.
- The expansion board is our own design. It carries a QMI8658 IMU, power, and the servo bus.


## Repository layout

```text
readme.md                         This file
Assembly_Guide.pdf                Assembly guide
bom.xlsx                          Robot bill of materials
PCBA/                             Arduino Uno Q expansion board
  ArduinoUnoQ.SchDoc              Altium schematic
  ArduinoUnoQ.PcbDoc              Altium PCB
  ArduinoUnoQ.pdf                 Schematic and PCB print
  ArduinoUnoQ.DWG                 Board outline
  ArduinoUnoQ.step                Board 3D model
  BOM.xlsx                        SMT bill of materials
  Pick Place for ArduinoUnoQ.csv  Pick-and-place coordinates
structure/                        Printable parts (STL)
```

| Path | Purpose |
| --- | --- |
| `structure/` | Print the body, legs, head, neck, and soft parts, then assemble them from the guide |
| `PCBA/` | Build the board that stacks on the Arduino Uno Q: schematic, PCB, 3D model, SMT BOM, and pick-and-place file |
| `bom.xlsx` | Buy list for the whole robot: controller, expansion board, servos, cables, battery, screws, and bearings |
| `Assembly_Guide.pdf` | Assembly drawings |

Files in `structure/` whose names start with `2x_` are printed twice. Left and right parts are separate files, for example `left_foot.stl` and `right_foot.stl`. Names that contain `tpu` are soft parts: the foot soles and the mouth.

### Expansion board

The expansion board stacks on the Arduino Uno Q. It powers the servos and the sensor and brings out the servo bus. The main parts on the board are:

- QMI8658A 6-axis IMU
- 5 V regulator (H7651) and AMS1117-3.3
- Servo connectors: three TE 292253-3 and three MX1.25 3-pin headers
- Serial buffers SN74LVC1G125 and SN74LVC1G126
- Power switch, DC jack, and an XH2.54 battery connector

## Bill of materials

Quantities come from `bom.xlsx`.

| Part | Quantity |
| --- | --- |
| Arduino Uno Q | 1 |
| Robot expansion board | 1 |
| AMP 3-pin cable | 15 |
| Feetech 1910 | 15 |
| 18650 battery | 1 |
| Countersunk screw M2×6 | 200 |
| Screw M2.5×6 | 6 |
| Screw M3×16 | 4 |
| Bearing 10×15×3 | 2 |
| Bearing 16×22×4 | 11 |

## Related links

- [xgoduck_runtime_arduino](https://github.com/LuwuDynamics/xgoduck_runtime_arduino): policies, firmware, and the web UI on the Arduino Uno Q
- [Microduck](https://github.com/pollen-robotics/microduck): onboard software by Pollen Robotics
- [microduck_rl](https://github.com/pollen-robotics/microduck_rl): policy training and simulation models
- [Microduck product page](https://pollen-robotics.com/microduck/)
