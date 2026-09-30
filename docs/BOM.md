# Bill of materials and component specifications

[Project](../readme.md) · [Purchasing list](../BOM.md) · [Build guide](BUILD_GUIDE.md) · [Print inventory](PRINTING.md)

Quantities are transcribed from [the robot purchasing list](../BOM.md), items 1–10. They are purchasing quantities, not a verified installed-fastener count. Component specifications below are source-backed; unresolved purchasing details are identified rather than replaced with generic substitutes.

## Robot purchasing list

| Item | Quantity | Specification supported by available sources | Purchasing check |
| --- | ---: | --- | --- |
| Arduino Uno Q | 1 | Qualcomm QRB2210 Linux host + STM32U585 MCU; Arduino App environment | 2 GB and 4 GB variants both confirmed by the maintainer; record which variant your build uses |
| XGO-Duck expansion board | 1 | Drawing envelope 68.55 × 53.38 mm; QMI8658A IMU; servo/power interfaces | Use the matching Luwu board revision; thickness and fabrication stackup are not specified |
| Feetech 1910 serial servo | 15 | Confirmed model: HD-1910-C001 / HD1910M; 34 × 20 × 23 mm; 21 ± 2 g; 4–8.4 V | Maintainer confirms this supplier model; preserve matching firmware/protocol when purchasing replacements |
| Servo cable | 15 | Supplier reference: AMP2.0-3P, 3 positions, 2.0 mm pitch; PVC; 150 ± 5 mm | Verify mating housing, pin orientation and wiring; wire gauge is not supplied |
| Battery pack | 1 | Original BOM: “18650 battery 8.4V”; capacity >2,500 mAh; discharge rating >3C; XH2.54 connector | Pack model, chemistry, nominal voltage, cell arrangement, polarity and charger still need confirmation |
| M2 × 6 countersunk screws | 200 | 2 mm nominal thread diameter × 6 mm length; countersunk head | Source purchasing quantity; thread form/pitch, drive and material are unspecified |
| M2.5 × 6 screws | 6 | 2.5 mm nominal thread diameter × 6 mm length; supplier specifies M2.5 × 6 for the servo output-shaft screw | Confirm head/drive and required quantities for the actual assembly |
| M3 × 16 screws | 4 | 3 mm nominal thread diameter × 16 mm length | Head type, thread pitch, drive and material are unspecified |
| Bearing, 10 × 15 × 3 mm | 2 | 10 mm bore × 15 mm outside diameter × 3 mm width | Confirm shield/seal, flange, clearance and supplier part number |
| Bearing, 16 × 22 × 4 mm | 11 | 16 mm bore × 22 mm outside diameter × 4 mm width | Confirm shield/seal, flange, clearance and supplier part number |

The [PCBA BOM](../PCBA/BOM.xlsx) is for manufacturing the expansion board. Do not count its components again when buying a finished board. Charger, USB data cable, assembly tools, filament and adhesive are not separate entries in the original ten-row robot BOM; account for them when planning the build.

## Controller

The [official Arduino Uno Q documentation](https://docs.arduino.cc/hardware/uno-q/) identifies a Qualcomm QRB2210 MPU with four Cortex-A53 cores at 2.0 GHz, plus an STM32U585 Cortex-M33 MCU up to 160 MHz. The board runs Debian Linux and Arduino sketches over Zephyr. The maintainer confirms that the project uses both 2 GB and 4 GB variants. Record the RAM variant and board SKU in your build report; no comparative performance result is claimed.

Use an Uno Q rather than treating another UNO-family board as interchangeable. Board power-input specifications and the expansion-board battery path are separate interfaces; the servo's 8.4 V maximum is not a voltage recommendation for a logic or USB power pin.

## Servo: supplier specification and runtime configuration

Source: supplied Feetech **HD-1910-C001**, edition **A/0**, dated **2026-09-07**. The cover identifies **HD1910M**. Values below describe that supplier variant. The maintainer confirms that the abbreviated “Feetech 1910” BOM entry refers to this supplied HD-1910-C001 / HD1910M variant. The simulation retains an HLS1910-labelled actuator model; that internal name is not an alternate purchasing SKU.

### Mechanical and interface data

| Parameter | Supplier specification |
| --- | --- |
| Body dimensions | 34 × 20 × 23 mm; use the supplier drawing for shaft and mounting details |
| Mass | 21 ± 2 g per servo |
| Motor / gears | Coreless motor / metal gears |
| Case | PA66 + GF43% |
| Position sensor | 12-bit magnetic encoder |
| Output spline | 25 teeth; 4.95 mm outside diameter |
| Gear ratio | 1:320 |
| Backlash | ≤0.5° |
| Output-shaft screw | M2.5 × 6 |
| Connector / cable | AMP2.0-3P; PVC; 150 ± 5 mm |
| Communication | TTL half-duplex asynchronous serial, 8 data bits, 1 stop bit, no parity |
| Baud range | 38,400 bit/s to 1 Mbit/s; supplier default 1 Mbit/s |
| ID range | 0–253; supplier default ID 1 |
| Encoder range / resolution | 0–4095 over 360°; approximately 0.088° per step |
| Operating temperature | −20 to +60 °C, supplier component rating |

### Electrical data by supply voltage

The working-voltage range is **4–8.4 V**. Typical-voltage columns in the supplier specification are shown separately so torque/current values are not mixed across voltages.

| Parameter | 4.8 V | 6.0 V | 7.4 V |
| --- | ---: | ---: | ---: |
| No-load speed, seconds per 60° | 0.137 | 0.109 | 0.088 |
| No-load current | ≤160 mA | ≤180 mA | ≤210 mA |
| Stall torque | 9 kgf·cm | 12 kgf·cm | 15 kgf·cm |
| Stall current | 1.2 A | 1.6 A | 2.0 A |
| Idle current | 20 mA | 20 mA | 20 mA |
| Rated torque | 2.2 kgf·cm | 3.0 kgf·cm | 3.7 kgf·cm |
| Rated current | 500 mA | 690 mA | 900 mA |

The sheet specifies ±10% for no-load speed, stall torque and stall current. Stall torque is not continuous usable torque or robot lifting capacity. Do not size the full robot supply from one servo's no-load current. No whole-robot current measurement is available here.

### Cable pin definition

| Pin number in supplier connector drawing | Function |
| --- | --- |
| 1 | TTL signal |
| 2 | VCC |
| 3 | GND |

All three conductors are described as black. Identify pin numbers using the supplier's connector view; do not infer left/right orientation from this table or identify polarity by wire color. The mating harness part number, wire gauge and allowable harness current remain unconfirmed.

### Values used by XGO-Duck

| Setting | Current runtime |
| --- | --- |
| Servo bus | 1 Mbit/s, Serial1 |
| IDs | 10–14, 20–24, 30–34 |
| Setup centering position | Raw 2047; supplier neutral is stated as 2048 |
| Run temporary gains | KP 6 / KD 20; mouth KP 10 |
| Setup stored-gain defaults | KP 5 / KD 20 |
| Calibration temporary gains | KP 3 / KD 0 |

These are software settings, not additional purchase specifications. Use the [runtime setup instructions](https://github.com/LuwuDynamics/xgoduck_runtime_arduino); do not change calibration based on a one-count difference in the supplier's neutral label.

## Expansion board

The dimensioned [PCB drawing](../PCBA/ArduinoUnoQ.pdf) gives a **68.55 × 53.38 mm** envelope. It is a board layout/outline drawing, not a rendered circuit schematic. Electrical design source is [ArduinoUnoQ.SchDoc](../PCBA/ArduinoUnoQ.SchDoc); PCB source is [ArduinoUnoQ.PcbDoc](../PCBA/ArduinoUnoQ.PcbDoc).

| Component / interface | Board quantity | Identifier and known parameter |
| --- | ---: | --- |
| IMU | 1 | U1: QMI8658A, 6-axis; runtime I²C at 400 kHz, probes 0x6A then 0x6B |
| 5 V regulator | 1 | U2: h7651-50pr, as listed in PCBA BOM |
| 3.3 V regulator | 1 | Q2: AMS1117-3.3V, as listed; verify exact orderable part/package against footprint |
| Serial buffers | 2 | SN1: SN74LVC1G126; SN2: SN74LVC1G125 |
| 2.0 mm 3-position headers | 3 | U3–U5: TE 292253-3, right-angle through-hole AMP CT |
| 1.25 mm 3-position headers | 3 | P1–P3: MX 1.25-WI-3P footprint; full manufacturer SKU absent |
| Battery connector | 1 | CN1: ZX-XH2.54-2PWZ; verify actual mating connector and polarity |
| DC socket | 1 | DC1: kh-dc-007b-2.1g; plug drawing and polarity require confirmation |
| Power switch | 1 | SW1: SS-12D06L5 |

The [TE manufacturer listing](https://www.te.com/en/product-292253-3.html) confirms the header's part number, three positions, 2 mm pitch and right-angle mounting. It does not establish that every generic “AMP 3-pin” cable mates correctly.

The original PCBA workbook retains garbled description fields and incomplete sourcing data. Regulator names and connector labels are not a validated continuous-current specification for the assembled board. Fabrication layer stack, thickness, trace/load limits, battery polarity and a board bring-up record still need release documentation.

## Fasteners and bearings

Use the dimensions in the purchasing table; no bearing series code is assigned from dimensions alone. Shields, seals and flanges affect fit and friction. Screw thread type, head profile and drive must match the actual part; do not silently replace a self-tapping fastener with a machine screw or vice versa.

The servo sheet specifies an M2.5 × 6 output-shaft screw, while the whole-robot BOM lists only six screws of that size. The available documents do not reconcile shaft retention, included accessories and total installed counts. Keep the original quantity and request the assembly-specific fastener map rather than multiplying by fifteen.

## Battery and charger: specification still to be finalized

Confirmed from the original BOM: one pack described as **18650 / 8.4 V**, **capacity >2,500 mAh**, **discharge rating >3C**, with an **XH2.54** connector reference.

The entry does not establish chemistry, nominal versus charge-limit voltage, series/parallel configuration, BMS/protection, dimensions, wire size or connector polarity. A 2-series lithium-ion pack is a possible interpretation, not a verified specification. No charger model, charge current or charging interface is provided. Do not order a charger solely by the “8.4 V” label.

The maintainer must identify the actual pack and compatible charger, then verify mechanical fit and the complete power path under load. The approximately one-hour battery-life target remains an estimate.

## Printed materials and workshop items

The local beta 3MF saves PLA presets for rigid parts on an A1 with a 0.4 mm nozzle and 0.2 mm layer height. That is a saved configuration, not a completed print-validation result. Explicit `_tpu` parts require a separately matched TPU setup; grade/hardness and material quantities are not yet provided. See [PRINTING.md](PRINTING.md).

For assembly, prepare screwdrivers matching the confirmed drives, a multimeter, a stable robot support and a USB data cable suitable for your Uno Q setup. The assembly guide includes an adhesive step; adhesive type and quantity must be selected for the actual printed materials and validated joint. These are preparation requirements, not additions with invented quantities to the source BOM.

## Budget and source record

The maintainer estimates **approximately US$400** per build. No itemized quote is validated. Record supplier, exact SKU, quantity, unit price, currency/date, shipping, taxes, filament, tools and spares for a reproducible budget.

- Robot purchasing list: `BOM.md`, items 1–10; transcribed from the review workbook.
- Maintainer confirmation in this documentation session: both Uno Q 2 GB and 4 GB variants are used; the supplied HD-1910-C001 / HD1910M specification identifies the project servo.
- Supplier servo document: HD-1910-C001 A/0, 2026-09-07; printed pages 2/7 and 3/7 (PDF pages 3 and 4) for the ratings above. Local original SHA-256: `aafd3b6a03f4902f74164bf49091d88c01418b12ddf7d5f8118cbc763f03f9a9`.
- Expansion-board components: `PCBA/BOM.xlsx`, ArduinoUnoQ sheet; dimensions visually checked in `PCBA/ArduinoUnoQ.pdf`.
- Software settings: runtime `sketch/duck_config.h` and documented setup procedure.
- Controller and connector manufacturer references linked above, checked on 2026-09-26.
