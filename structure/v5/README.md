# XGO-Duck V5 · Audio and Video Kit

English · [简体中文](README.zh-CN.md)

These 3D-printable parts are for XGO-Duck builds that use the audio and video kit. This version includes the face shell and separate parts for the camera, light, and time-of-flight (ToF) sensor.

## STL files

This folder contains **50 individual STL files** exported from [`xgoduckV5.3mf`](../../3DManufacturingFormat/xgoduckV5.3mf). Every file starts with `V5_AUDIO_VIDEO_`. Suffixes such as `_01` and `_02` distinguish separate instances from the original print project.

| File | Part |
| --- | --- |
| [`V5_AUDIO_VIDEO_FACE.stl`](V5_AUDIO_VIDEO_FACE.stl) | Face shell |
| [`V5_AUDIO_VIDEO_FACE_CAMERA.stl`](V5_AUDIO_VIDEO_FACE_CAMERA.stl) | Camera-related face part |
| [`V5_AUDIO_VIDEO_FACE_LIGHT.stl`](V5_AUDIO_VIDEO_FACE_LIGHT.stl) | Light-related face part |
| [`V5_AUDIO_VIDEO_FACE_TOF.stl`](V5_AUDIO_VIDEO_FACE_TOF.stl) | ToF sensor-related face part |

The folder also includes body, leg, foot, and beak parts, including TPU files for the foot pads and flexible beak pieces.

## Printing and assembly

Each numbered STL represents one instance from the source project. Print each selected file once; do not multiply it again by a retained `2x` or `4x` label. The file count includes the optional roller-skate parts and alternative backpack enclosures. Choose the enclosure for your V1 or V1.1 board using the [3MF plate guide](../../3DManufacturingFormat/README.md).

1. Import the required STLs into your slicer in millimeters at 100% scale. Each part retains its orientation from the source project and has been positioned individually on the build plane.
2. Use TPU for parts marked `TPU`. Refer to the [3MF plate guide](../../3DManufacturingFormat/README.md) for the nine build plates and any part-specific slicing settings. Check the fit of the face parts against the hardware in your kit before printing the full set.
3. Follow your kit’s instructions for installing and wiring the audio and video modules and setting up their software. For the base robot, use the official hardware references. [Assembly guide](../../Assembly_Guide.pdf) · [Bill of materials](../../BOM.md)

## Credits

XGO-Duck was adapted from Pollen Robotics’ Microduck by Luwu Dynamics. [XGO-Duck hardware project](https://github.com/LuwuDynamics/xgoduck_hardware)
