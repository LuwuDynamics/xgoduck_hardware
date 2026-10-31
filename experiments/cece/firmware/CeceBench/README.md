# Cece ESP32-C3 simulator and bench firmware

This project builds real Arduino ESP32-C3 firmware. It is currently a component diagnostic, not a complete walking or voice controller. No physical board, wiring, power system or motion has been verified.

## Checked so far

- Wokwi runs the compiled C3 firmware and shows a modeled HC-SR04 range reading of about 25 cm. An I2C scan detects the modeled PCA9685 servo driver at 0x44. This is functional simulation, not electrical or mechanical certification.
- An SSD1327 custom-chip model is included as work in progress. Its first version appeared in the diagram but did not respond to the firmware's I2C scan. A revised WebAssembly build has not yet been verified. Do not treat the OLED as tested yet.
- The PC bridge forwards text to a local Ollama model. An actual request from the PC returned a model response; the simulated ESP32-to-PC connection has not been validated. Tests with a mock backend also pass.
- Wokwi does not emulate the ESP32-C3 I2S peripheral. The firmware contains hardware I2S `mic` and `beep` diagnostics, but the microphone, amplifier and speaker have not been emulated or tested on hardware. Camera, speech transcription, speech playback and full walking software remain to be implemented. The camera interface and model are not selected.

## Wiring

Pin assignments are provisional, not a build-ready schematic. See `../../electronics/WIRING_DRAFT.md`. SDA GPIO0 and SCL GPIO1 connect to the SSD1327 (default 0x3D) and PiicoDev PCA9685 (0x44); HC-SR04 TRIG GPIO7 and ECHO GPIO10 require a verified 3.3 V-safe echo interface. PiicoDev sockets 1, 2, 3, 4 map to PCA channels 3, 2, 1, 0. Servo power is separate from logic with common ground; assess power, polarity and current on the actual system. Never connect a 5 V echo directly to an ESP32 pin.

The firmware sends no servo commands at boot, but a separately powered PCA9685 can retain earlier outputs. Remove servo power before checking connections; start with a restrained individual servo and conservative limits. `release` requests all four signals off, but cannot establish physical safety.

## Run

Install the ESP32 Arduino core and Adafruit SSD1327/GFX libraries, then run `arduino-cli compile --fqbn esp32:esp32:esp32c3 --output-dir build .`. Open this folder in VS Code with the Wokwi extension, then run `Wokwi: Start Simulator`. The generated binary and ELF under `build/` are not committed.

At 115200 baud the bench serial commands include `scan`, `status`, `wifi Wokwi-GUEST -`, `servo 1 90`, `release`, `mic`, `beep` and `ask <http://PC-IP:8765/ask> <message>`. I2S commands are physical-device diagnostics and are not modeled by Wokwi.

For the optional bridge use `python pc_bridge/server.py`; it listens on localhost by default. To accept requests from a real ESP32 on a trusted LAN, explicitly choose the PC's LAN address with `--listen <PC-LAN-IP>`. Prototype HTTP is unauthenticated and unencrypted; do not expose it on the public internet or untrusted networks.

The PCA9685 Wokwi model is from https://github.com/bonnyr/wokwi-pca9685-custom-chip (MIT; license included). The SSD1327 model implements only a subset of the controller and remains unverified. References: https://learn.adafruit.com/adafruit-grayscale-1-5-128x128-oled-display ; https://github.com/CoreElectronics/CE-PiicoDev-PyPI/blob/main/src/PiicoDev_Servo.py ; https://docs.wokwi.com/guides/esp32 .
