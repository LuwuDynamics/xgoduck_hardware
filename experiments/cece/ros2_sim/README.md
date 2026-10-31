# Cece ROS 2 and Gazebo study

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
colliders and approximate box inertias. It has four passive revolute joints;
there is no motor controller or walking gait in this Gazebo model yet. A
100-step headless launch was checked; this is not a walking test. The existing
`../bullet_gait` experiment has separate assumed motor parameters, contact
and inertias; its gait has not been ported or validated in Gazebo.
The OpenAI bridge and ESP32/Wokwi circuit are not connected to this world.
This world cannot establish physical walking, obstacle detection, real-world
mapping, servo fit or electrical safety. Camera hardware and actual room data
are still needed for a real reconstruction.

## Intended connections

The ESP32 remains responsible for its real sensor and motor firmware. It will
send audio or commands over Wi-Fi to a PC service rather than running the
large language model locally. The PC service can use AtBots and the user's
own authorized ChatGPT plan for text; weather comes from a weather service.
ROS 2 will coordinate robot state and commands, and Gazebo will model the
robot, sensors and room. A Wokwi-to-ROS bridge still has to be written and
tested. ChatGPT plan OAuth does not by itself provide simulated I2S audio,
and its preview route does not support audio or transcription; speech needs
an additional supported speech path.
