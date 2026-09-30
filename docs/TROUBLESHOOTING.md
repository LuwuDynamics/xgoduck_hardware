# Hardware troubleshooting

[Build guide](BUILD_GUIDE.md)

Disable motion and support the robot before inspecting mechanics. Disconnect power before changing connectors.

| Symptom | Inspect first | Next action |
| --- | --- | --- |
| Two servos respond together | Duplicate IDs | Disconnect the shared bus and configure one servo at a time |
| One servo is missing | ID label, connector seating, harness continuity | Test it separately with confirmed compatible power and protocol |
| Joint moves the wrong way | ID location, left/right installation, zero calibration | Compare PDF and runtime mapping; do not compensate by changing policy order |
| Bearing or servo does not fit | Exact part number, print scale, orientation and tolerances | Validate one part before reprinting the whole set |
| Robot resets during movement | Supply voltage under load, connector and cable capacity | Stop and verify the complete power path; do not keep retrying with a hotter supply |
| Default pose binds | Assembly orientation, joint zero, trapped cable | Release torque with the robot supported; correct the mechanical cause |
| Oscillation or heat | Calibration, gains, mechanical resistance | Stop motion; compare with the documented configuration before tuning |
| No IMU data | Board orientation, soldering, I²C connection | Inspect against the schematic and runtime IMU diagnostics |

For help, include the hardware revision, servo part/firmware, power-pack details, clear wiring photos and the runtime status capture. Avoid publishing Wi-Fi credentials, IP-sensitive logs or personal purchase information.
