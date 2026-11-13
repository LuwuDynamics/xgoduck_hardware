# XGO-Duck V2 · Standard Kit

English · [简体中文](README.zh-CN.md)

These 3D-printable parts are for the standard XGO-Duck kit without audio or video hardware.

## STL files

This folder contains **47 individual STL files** exported from [`XGO_duckV2.3mf`](../../3DManufacturingFormat/XGO_duckV2.3mf). Every file starts with `V2_STANDARD_`. Suffixes such as `_01` and `_02` distinguish separate instances from the original print project.

| Part group | Example files |
| --- | --- |
| Head and beak | [Head cover](V2_STANDARD_HEAD_COVER.stl), [head pitch part](V2_STANDARD_HEAD_PITCH.stl), [head servo support](V2_STANDARD_HEAD_SERVO_SUPPORT.stl), [jaw](V2_STANDARD_JAW.stl) |
| Body and legs | [Body](V2_STANDARD_BODY.stl), [left foot](V2_STANDARD_LEFT_FOOT.stl), [right foot](V2_STANDARD_RIGHT_FOOT.stl) |
| Flexible parts | [Upper beak](V2_STANDARD_MOUTH_UP_TPU.stl), [lower beak](V2_STANDARD_MOUTH_BOTTOM_TPU.stl), [foot pad](V2_STANDARD_2x_FOOT_BOTTOM_TPU_01.stl) |

## Printing and assembly

Each numbered STL represents one instance from the source project. Print each selected file once; do not multiply it again by a retained `2x` or `4x` label. The file count includes the optional roller-skate parts and alternative backpack enclosures. Choose the enclosure for your V1 or V1.1 board using the [3MF plate guide](../../3DManufacturingFormat/README.md).

1. Import the required STLs into your slicer in millimeters at 100% scale. Each part retains its orientation from the source project and has been positioned individually on the build plane.
2. Use TPU for parts marked `TPU`. Refer to the [3MF plate guide](../../3DManufacturingFormat/README.md) for the nine build plates and any part-specific slicing settings.
3. For standard kit assembly and parts sourcing, use the official hardware references. [Assembly guide](../../Assembly_Guide.pdf) · [Bill of materials](../../BOM.md)

## Credits

XGO-Duck was adapted from Pollen Robotics’ Microduck by Luwu Dynamics. [XGO-Duck hardware project](https://github.com/LuwuDynamics/xgoduck_hardware)
