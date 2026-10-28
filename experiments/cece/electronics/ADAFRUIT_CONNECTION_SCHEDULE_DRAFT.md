# cece — connection schedule, REVISION DRAFT

**Not a checked or construction-ready schematic.** This schedule covers the
selected boards and proposed pin use, but the charge circuit, ESP32 power
isolation, exact connector pinouts, LED driver and installed fit are unresolved.
Read it as a review aid, not as authorization to connect a LiPo or order a PCB.

## Named supplies

- BAT2S = Dualsky 7.4 V nominal 2S lithium polymer pack, up to 8.4 V fully
  charged. The two-cell balance connector must be identified on the real pack.
- 5V = proposed 5 V UBEC output, measured before loading. UBEC input accepts
  the 2S pack; UBEC is not a charger. All signal-board grounds must share GND.
- 3V3 = ESP32-C3 Super Mini logic supply, but board-specific regulator current,
  5V input pin and USB-versus-external supply isolation must be verified.
- Charger, USB charging connector, 2S balancing, per-cell protection,
  reverse-polarity protection and load isolation are not designed. No wiring
  is specified for these until a compatible charger is selected and reviewed.
  Do not connect USB 5 V directly to either BAT2S or its balance lead.

```text
 BAT2S + / -  -->  2S protection & power switch TBD  -->  UBEC INPUT + / -
                                                        UBEC 5 V --> +5V rail
                                                        UBEC GND --> GND rail

 +5V rail --> PiicoDev SERVO SUPPLY (separate 5 V input; connector TBD)
 +5V rail --> HC-SR04 VCC
 +5V rail --> MAX98357 VCC
 +5V rail --> SN74AHCT125N pin 14 (proposed)
 +5V rail --> ESP32 5 V input ONLY after exact board / backfeed verification
 GND rail --> all modules and logic ground
 ESP32 3V3 --> INMP441 VDD; I2C servo-driver logic; OLED logic bus
```

The PiicoDev control bus is 3.3 V; it is separate from its servo 5 V supply.
Core specifies approximately 0.7 A per micro servo for budgeting; four may
therefore need about 2.8 A as a planning starting point, with transient/stall
behavior and actual SG90 current still unmeasured. UBEC rating alone does not
validate all wires, switches, connectors or peak rail voltage.

## Controller pin allocation (GPIO numbers, not physical header positions)

| ESP32-C3 GPIO | Proposed signal | Connects to |
|---|---|---|
| 0 | SDA | PiicoDev SDA and Adafruit 4741 SDA, 3.3 V I2C |
| 1 | SCL | PiicoDev SCL and Adafruit 4741 SCL, 3.3 V I2C |
| 3 | I2S bit clock | INMP441 SCK and MAX98357 BCLK |
| 4 | I2S word-select | INMP441 WS and MAX98357 LRC |
| 5 | I2S input | INMP441 SD |
| 6 | I2S output | MAX98357 DIN |
| 7 | ultrasonic trigger | AHCT125 input 1A pin 2; output pin 3 -> TRIG |
| 10 | ultrasonic echo | HC-SR04 ECHO via resistor divider below |
| 20 | LED control | grouped LED driver TBD, not directly seven LEDs |

Check the exact C3 Super Mini pin labels and that GPIO20/RX is actually exposed.
GPIO2, GPIO8 and GPIO9 are boot straps; GPIO18/19 are USB by default. GPIO20
may be UART RX; use USB programming and check reset behavior. All pin choices
are provisional until the exact board and prototype firmware are tested.

## Display and servo controller: I2C

- Connect the four signal lines **3V3, GND, SDA, SCL**, matching labels rather
  than wire colors, from ESP32 to the PiicoDev breakout or an adapter cable.
- Use the existing 4-pin PiicoDev cable between the second PiicoDev connector
  and the Adafruit 4741 STEMMA QT connector. Both carry 3.3 V I2C.
- PiicoDev logic device address is 0x44 by default. Adafruit 4741 address is
  **0x3D by default** (0x3C if its address jumper is set); scan before coding.
- Four standard servo plugs go on channels 0–3 with ground/5V/signal matching
  the driver silkscreen. Suggested labels: left hip, right hip, left ankle,
  right ankle. Calibrate servo neutral with horns detached. Channel directions
  are mechanical assumptions until tested.
- The separately powered servo input, adapter from the UBEC and barrel/USB-C
  power implementation must be checked on the real board. Do not feed 5 V
  into the 3V3 PiicoDev data connector.

## HC-SR04 level shifting

The sensor operates from 5 V; do not connect its ECHO directly to a 3.3 V GPIO.
Proposed conservative divider (through-hole 1/4 W resistors, values to buy):

```text
 HC-SR04 ECHO --- R1 2.2 kΩ ---+--- GPIO10
                                |
                              R2 3.3 kΩ
                                |
                               GND
```

At nominal 5 V echo, GPIO sees approximately 3.0 V. Confirm sensor high and
ESP32 voltage with a multimeter. HC-SR04 trigger may require 5 V logic; use
through-hole **SN74AHCT125N DIP-14**, not yet in the cart, as follows:

```text
 pin 14 -> +5V             pin 7 -> GND
 pin 1  -> GND (enable)    pin 2 -> GPIO7
 pin 3  -> sensor TRIG
 pins 4,10,13 -> +5V (disable unused gates)
 pins 5,9,12  -> GND (unused inputs)
 pins 6,8,11  -> no connection (unused outputs)
 100 nF ceramic from pin 14 to pin 7, physically close to chip
```

This buffer is a proposed through-hole addition; check the chip marking and
orientation against the TI datasheet before wiring. Resistances, chip and
housing are not yet accounted for in the cart or tested.

## Microphone and audio

- INMP441: VDD -> 3V3, GND -> GND, SCK -> GPIO3, WS -> GPIO4,
  SD -> GPIO5, L/R -> GND for left channel. Verify exact module labeling and
  any onboard configuration. Microphone power must not be connected to 5 V.
- MAX98357 DFR0954: VCC -> 5V, GND -> GND, BCLK -> GPIO3, LRC -> GPIO4,
  DIN -> GPIO6. Leave SD/GAIN per the module's documented defaults until
  firmware configures audio; check datasheet and silkscreen.
- Speaker wires across SPK+ and SPK− only. The output is bridged: never tie
  either speaker output to ground. Check 7-pin/2-pin connector types; the
  speaker connector and DFRobot PH2.0 socket compatibility is unverified.
- Shared I2S clocks can support input and output on ESP32-C3, but code, sample
  format and actual module interoperability have not been tested.

## Face LEDs and power details not yet finished

Five 3 mm mouth LEDs and two 5 mm LEDs need one correctly sized series resistor
per LED and a suitable driver; individual or grouped control is undecided.
Do not tie seven LEDs directly to one ESP32 pin or omit resistors. The cart has
330 Ω resistors, but LED colors, brightness, current budget and transistor/
MOSFET part have not been finalized. A bulk capacitor across 5V/GND near the
servo rail may help transients; value, voltage and wiring require measurement.

## References and checks

- https://www.ti.com/product/SN74AHCT125
- https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html
- https://learn.adafruit.com/adafruit-grayscale-1-5-128x128-oled-display/pinouts
- https://core-electronics.com.au/piicodev-servo-driver.html
- https://wiki.dfrobot.com/dfr0954/
- https://invensense.tdk.com/wp-content/uploads/2015/02/INMP441.pdf

Not checked: construction-level KiCad ERC, real board measurements and pinout,
servo stall current, power-rail and charge behavior, physical electronics,
firmware, enclosure clearances, balance or physical robot operation.
