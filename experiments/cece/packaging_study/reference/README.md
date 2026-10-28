# Reference CAD for Cece packaging study

## Adafruit 4741 grayscale 1.5-inch OLED

Files: `adafruit_4741.step`, `adafruit_4741.stl`.

Manufacturer source: [Adafruit_CAD_Parts, 4741 OLED 1.5in](https://github.com/adafruit/Adafruit_CAD_Parts/tree/a2f8a3e7d394cf145eca41e85944c38268646c94/4741%20OLED%201.5in), commit `a2f8a3e7d394cf145eca41e85944c38268646c94` (17 February 2021). Downloaded 29 October 2026. These are the manufacturer CAD model, not a scan of the purchased unit.

Adafruit's MIT license is copied in `adafruit_cad_parts_LICENSE.txt`.

The STL mesh spans x = 0 to 35.56 mm, y = -5.08 to 41.91 mm, and z = -1.10 to 4.53 mm: **35.56 × 46.99 × 5.63 mm**. The PCB lies around z = 0 to 1.6 mm. The **OLED viewing face points toward negative z**; rear connectors and components extend toward positive z. The modeled front active square spans approximately x = 4.477 to 31.337 mm and y = 8.659 to 35.519 mm (26.86 × 26.86 mm). The active-area center is x = 17.907, y = 22.089 mm; it is about 3.67 mm toward the top of the board from the board center. Mounting holes in the [official Eagle PCB](https://github.com/adafruit/Adafruit-Grayscale-1.5-inch-128x128-OLED-PCB) have 2.5 mm drills and center pitches 30.48 × 41.91 mm. The two STEMMA QT/JST-SH sockets are at the long side edges near y = 18.415 mm; the eight-position through-hole header is along the top edge.

The 3D model is nominal. [Adafruit's support note](https://forums.adafruit.com/viewtopic.php?t=197630) says the real OLED glass placement can vary relative to the PCB. Measure the delivered board and leave front-window clearance before releasing the print.

## Core Electronics CE09181 PiicoDev four-channel servo driver

File: `piicodev_ce09181.step`.

Generated 29 October 2026 with KiCad 8.0.5 `kicad-cli pcb export step --subst-models` from the [manufacturer's PCB source](https://github.com/CoreElectronics/CE-PiicoDev-Servo-Driver/blob/066cbc34496e92cc33a281020ff38091f38a951c/PCB/CE-PiicoDev-Servo-Driver.kicad_pcb), source commit `066cbc34496e92cc33a281020ff38091f38a951c` (2 December 2022). The KiCad exporter used a 1.6 mm board stackup and included the available component models, including the servo output headers. **This STEP is an incomplete physical model:** KiCad could not resolve both JST-SH PiicoDev connector models (J1/J2) or either USB-C servo-power socket model (J8/J9). The PCB footprint positions are still present in the source, but their mating plugs and cable bends are absent from this 3D export. Do not use this STEP alone as evidence of connector clearance.

Core Electronics' source hardware license information is copied in `piicodev_servo_driver_LICENSE.md`. This generated STEP is attributed to Core Electronics and derived from its PCB source; any redistribution or adaptation should follow the hardware license stated there.

The source PCB outline is 25.4 × 52.0 mm. M2.5 mounting-hole center pitch is approximately 19.40 × 46.00 mm. The USB-C sockets face the long sides near 11.29 mm from one short end; four 3-pin servo headers lie across the board near 26.04 mm from that end; and two PiicoDev JST-SH sockets face the long sides near 39.30 mm from that end. Reserve additional space at those edges for plugs and cable bends.
