# Cece ROS 2 and Gazebo study

For the complete Windows start-up sequence, including Wokwi, voice and AtBots,
see [Start Cece's simulation](../START_HERE.md).

The starter world is a 4 m by 4 m virtual room with a floor, four walls and a
box obstacle. It is invented geometry, not a scan or measurement of a real
room. The XML can be inspected with any SDF-compatible tool.

On Ubuntu 24.04 with ROS 2 Jazzy and Gazebo Harmonic installed:

```bash
source /opt/ros/jazzy/setup.bash
gz sim -r worlds/starter_room.sdf
```

To generate and view the provisional Cece model in the room:

```bash
python3 build_prototype_world.py
gz sim generated/starter_cece.sdf
```

The model uses existing CAD visuals, estimated component masses, simple box
colliders and approximate box inertias. Four Gazebo position controllers and
an experimental gait are provided:

```bash
source /opt/ros/jazzy/setup.bash
python3 walk_controller.py --steps 20
python3 evaluate_gait.py
```

Each requested step corresponds to one alternating commanded half-step.
If no count is specified, motion continues until a stop request. The PC bridge
accepts requests such as “move forward twenty steps” without a fixed maximum;
say “stop” to request a stop. It responds once the request has been launched,
not when motion finishes. The stop request applies to the Gazebo gait only.

The evaluation measured all four joints moving and roughly 15 mm of body
displacement in one run. Reported foot-frame vertical ranges were under
0.001 mm: this does not demonstrate foot lift and suggests sliding. The
script does not measure ground contact or landing, and cannot establish
walking. The previous
`../bullet_gait` study uses different contact geometry and assumptions.
The PC bridge can explicitly enable a simulation-only gait in response to a
request from the ESP32; it launches the Gazebo controller directly. This is
not a simulation of the ESP32's PCA9685 outputs driving Gazebo joints.
This world cannot establish physical walking, obstacle detection, real-world
mapping, servo fit or electrical safety. Camera hardware and actual room data
are still needed for a real reconstruction.

## Intended connections

The ESP32 remains responsible for its real sensor and motor firmware. It will
send audio or commands over Wi-Fi to a PC service rather than running the
large language model locally. The PC service can use AtBots and the user's
own authorized ChatGPT plan for text; weather comes from a weather service.
ROS 2 will coordinate robot state and commands, and Gazebo will model the
robot, sensors and room. A direct Wokwi servo-output-to-ROS bridge still has
to be written and tested. ChatGPT plan OAuth does not provide simulated I2S audio,
and its preview route does not support audio or transcription; speech needs
an additional supported speech path.
