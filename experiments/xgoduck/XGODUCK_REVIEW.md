# XGO-Duck hardware review for the CeCe robot

Reviewed on 27 October 2026. This is a source review, not a build or independent
walking verification. Links below are pinned to the revisions reviewed.

## What XGO-Duck actually uses

The [hardware overview](https://github.com/LuwuDynamics/xgoduck_hardware/blob/106186e1beda690c28f485a754538d6f41b5d025/readme.md)
describes 15 Feetech 1910 serial servos: ten for the two legs, four for the
head/neck and one for the mouth. It uses an Arduino UNO Q, a custom expansion
board and a QMI8658A six-axis IMU. The 14-joint motion policy excludes the
mouth servo.

The corresponding [MuJoCo walking model](https://github.com/LuwuDynamics/xgoduck_rl/blob/fa621fc77ad9a05d69da13270e86118bdd3603fe/src/mjlab_microduck/robot/xgoduck/robot_walk.xml)
defines five independently actuated joints on each leg: hip yaw, hip roll,
hip pitch, knee and ankle. It supplies joint limits, collision geometry,
inertial parameters, actuator placeholders, and IMU-related sensors. The
model's coordinates and mass properties describe XGO-Duck, not CeCe.

Hip roll gives the controller a way to alter lateral stance; hip pitch and
knee can swing and lift a leg; the ankle lets it change foot orientation.
These are interpretations of the joint arrangement, not claims that any one
joint alone guarantees stability. The build guide calls for calibrated servo
IDs and IMU feedback before supported motion tests.

The [runtime repository](https://github.com/LuwuDynamics/xgoduck_runtime_arduino/tree/8837d5a3bc7cf3746f6da2b55c7b9191026b9838)
provides onboard policy execution, servo setup and walk/get-up/pick policies;
the [RL repository](https://github.com/LuwuDynamics/xgoduck_rl/tree/fa621fc77ad9a05d69da13270e86118bdd3603fe)
contains simulation and training material. The published policies depend on
the project's joint layout, model, actuators, observations, calibration and
runtime. They must not be assumed to work on an altered robot or on an ESP32-C3.

## Comparison with our current model

- CeCe has two proposed leg motor axes with no motor mounts, shaft coupling,
  angle sensors, knees, ankle joints or weight-shifting hip axis. It does not
  reproduce the XGO-Duck leg mechanism and has not demonstrated walking.
- CeCe's two AA cells are not the XGO-Duck power system. Its [BOM](https://github.com/LuwuDynamics/xgoduck_hardware/blob/106186e1beda690c28f485a754538d6f41b5d025/BOM.md)
  lists an 8.4 V 18650 battery pack with >3500 mAh and >3C. The maintainers
  note that exact pack configuration, connector polarity and compatibility
  still require confirmation. Do not power the XGO hardware directly from
  two AAs or assume its motor performance at an unspecified supply.
- The Super Mini is not a drop-in replacement for UNO Q's Linux host and MCU
  combination. A stripped-down controller or different robot may be possible,
  but it needs its own implementation and measured performance.
- The hardware [print inventory](https://github.com/LuwuDynamics/xgoduck_hardware/blob/106186e1beda690c28f485a754538d6f41b5d025/docs/PRINTING.md)
  marks the soles as TPU and says a complete validated print profile is still
  missing. PLA may suit rigid shells after fit testing; PLA alone does not
  reproduce its flexible soles.

## Practical route

For the most direct reference to a demonstrated platform, study the complete
XGO-Duck leg joint geometry and its matching control and power system before
redesigning the enclosure. Keep the leg joint chain, actuator capability, IMU
placement, mass distribution, foot friction and control model consistent at
first. The green CeCe head/body/OLED could then be developed as a lightweight
enclosure around that mechanism, with recalculated mass and retesting.

If two AA cells, a much smaller body and ESP32-C3 are hard requirements, this
becomes a different robot. It needs appropriately sized position-controlled
actuators, at least a worked-out sideways weight-transfer and forward-swing
mechanism, a power budget, and an independently designed and tested gait.
Fewer joints might be feasible, but no minimum joint count has been validated.
Do not transplant XGO's trained policy and claim that the result walks.

The project is adapted from Pollen Robotics' Microduck. Consult the hardware
repository's [licensing notes](https://github.com/LuwuDynamics/xgoduck_hardware/blob/106186e1beda690c28f485a754538d6f41b5d025/LICENSING.md)
and applicable upstream/file-level rights before distributing or reusing
their CAD. The notes say the hardware repository lacks a top-level finalized
licence; don't assume the hardware has the same terms as the RL code.
