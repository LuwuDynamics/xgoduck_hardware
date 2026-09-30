# Origins and adaptations

[Project](readme.md) · [Licensing](LICENSING.md)

XGO-Duck is a substantial adaptation of the Microduck ecosystem, not an independently originated robot concept. The maintainer has confirmed extensive reference to Microduck materials. The XGO-Duck repository descriptions also identify that lineage. This page records the architectural relationship; it is not a completed file-by-file copyright audit.

## Credit the foundation

- [Microduck, Pollen Robotics](https://pollen-robotics.com/microduck/): the robot concept and upstream project.
- [Microduck runtime](https://github.com/pollen-robotics/microduck): upstream onboard software and system reference.
- [microduck_rl](https://github.com/pollen-robotics/microduck_rl): upstream learning environments and sim-to-real approach.
- [mjlab](https://github.com/mujocolab/mjlab): training framework.
- [BAM, Rhoban](https://github.com/Rhoban/bam): actuator modelling.

## What follows upstream and what is adapted

| Area | Inherited or referenced foundation | XGO-Duck adaptation documented in its source |
| --- | --- | --- |
| Robot form | Duck-shaped biped with articulated legs, neck, head and mouth | Printable XGO-Duck structure and assembly drawings |
| Joint layout | Fifteen servos and retained policy ordering | Feetech 1910 bus integration and per-robot encoder calibration |
| Learning | Microduck task recipes and PPO/ONNX workflow | XGO-Duck geometry/inertias and HLS1910 BAM parameters |
| Control interface | Shared policy conventions and motion concepts | Linux policy host plus STM32 control on Uno Q |
| Electronics | Reference robot architecture | Luwu expansion board with QMI8658A, power and servo interfaces |

“Adaptation” here describes the engineering work visible in the XGO-Duck source. It does not establish exclusive ownership of every file. The exact upstream base revision, copied paths, original design sources and permissions must still be recorded.

## Compatibility is a separate question

Use the XGO-Duck task IDs, dependencies and deployment instructions in these repositories. Do not substitute an upstream policy solely because its tensors have the same dimensions. Actuator dynamics, geometry, calibration, command meaning and runtime behavior must also agree.

Upstream commands such as `robotctl` belong to a different runtime. They are not XGO-Duck Uno Q installation instructions. Features demonstrated on an upstream robot are not evidence that this hardware variant supports them.

## Model and design rights need their own record

The current [upstream RL README](https://github.com/pollen-robotics/microduck_rl) distinguishes its code license from a noncommercial, share-alike statement for 3D models. Preserve the applicable terms for the actual inherited files and versions; obtain the precise license text and provenance before redistributing derivatives. A code LICENSE alone is insufficient evidence for model rights.

The official [Microduck press kit](https://pollen-robotics.com/microduck/press-kit/) also limits its open-source statement to software. Do not infer design-file permissions from product marketing. These observations were reviewed on 2026-09-26 and are not a finding that any specific XGO-Duck file is unauthorized.

## Attribution for articles and demonstrations

Suggested credit: **“XGO-Duck by Luwu Dynamics, based on Microduck and microduck_rl by Pollen Robotics.”** Add mjlab and Rhoban BAM when discussing training. Preserve file-level copyright and license notices in source distributions. This project does not claim endorsement by Pollen Robotics, Hugging Face, Rhoban or Arduino.
