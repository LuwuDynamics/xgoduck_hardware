# Printing inventory

[Project](../readme.md) · [Build guide](BUILD_GUIDE.md)

For complete pre-arranged 3MF projects, use [V5 audio/video or V2 original downloads and the plate guide](../3DManufacturingFormat/README.md) ([简体中文](../3DManufacturingFormat/README_CN.md)). Open the matching project in Bambu Studio, confirm the printer and filaments, then slice before printing.

## Choose the STL set for your kit

| Kit | Folder and instructions | STL files | Filename prefix |
| --- | --- | ---: | --- |
| V2 standard kit, without audio/video | [English](../structure/v2/) · [简体中文](../structure/v2/README.zh-CN.md) | 47 | `V2_STANDARD_` |
| V5 audio/video kit | [English](../structure/v5/) · [简体中文](../structure/v5/README.zh-CN.md) | 50 | `V5_AUDIO_VIDEO_` |

These sets were exported in millimetres from the corresponding nine-plate 3MF projects. Numbered files already represent separate instances: print each selected file once, without multiplying it again by a retained `2x` or `4x` label. Do not mix parts across robot versions. Each set includes optional roller-skate parts and alternative backpack enclosures; choose one enclosure for your V1 or V1.1 board using the [plate guide](../3DManufacturingFormat/README.md).

## Existing files directly under structure/

The following tables describe the existing files directly under `structure/`, retained for earlier links and builds. Their copy counts do not apply to the numbered files in `structure/v2/` or `structure/v5/`.

For these existing files, `2x_` means two copies and `4x_` means four copies; other files default to one for planning and require confirmation against the assembly. Left/right files are distinct. Original filenames, including `mouth_buttom_tpu.stl`, are preserved. Choose one backpack enclosure for your board: [V1](../structure/ENCLOSURE_FOR_V1.stl) or [V1.1](../structure/ENCLOSURE_FOR_V1P1.stl).

| File | Planned copies | Material note |
| --- | ---: | --- |
| [2x_ankle_axis.STL](../structure/2x_ankle_axis.STL) | 2 | Rigid material: confirm profile |
| [2x_foot_bottom_tpu.stl](../structure/2x_foot_bottom_tpu.stl) | 2 | TPU indicated by filename |
| [2x_hip_rol_output.stl](../structure/2x_hip_rol_output.stl) | 2 | Rigid material: confirm profile |
| [2x_hip_rol_shell.stl](../structure/2x_hip_rol_shell.stl) | 2 | Rigid material: confirm profile |
| [2x_neck.stl](../structure/2x_neck.stl) | 2 | Rigid material: confirm profile |
| [2x_shank.stl](../structure/2x_shank.stl) | 2 | Rigid material: confirm profile |
| [2x_thigh_support.stl](../structure/2x_thigh_support.stl) | 2 | Rigid material: confirm profile |
| [battery.stl](../structure/battery.stl) | 1 | Rigid material: confirm profile |
| [body.stl](../structure/body.stl) | 1 | Rigid material: confirm profile |
| [body_left_shell.stl](../structure/body_left_shell.stl) | 1 | Rigid material: confirm profile |
| [body_right_shell.stl](../structure/body_right_shell.stl) | 1 | Rigid material: confirm profile |
| [eye.stl](../structure/eye.stl) | 1 | Rigid material: confirm profile |
| [FACE.stl](../structure/FACE.stl) | 1 | Audio/video face part |
| [FACE_CAMERA.stl](../structure/FACE_CAMERA.stl) | 1 | Audio/video face part |
| [FACE_LIGHT.stl](../structure/FACE_LIGHT.stl) | 1 | Audio/video face part |
| [FACE_TOF.stl](../structure/FACE_TOF.stl) | 1 | Audio/video face part |
| [head.stl](../structure/head.stl) | 1 | Rigid material: confirm profile |
| [head_pitch.stl](../structure/head_pitch.stl) | 1 | Rigid material: confirm profile |
| [head_servo_support.stl](../structure/head_servo_support.stl) | 1 | Rigid material: confirm profile |
| [head_shell.stl](../structure/head_shell.stl) | 1 | Rigid material: confirm profile |
| [head_yaw.STL](../structure/head_yaw.STL) | 1 | Rigid material: confirm profile |
| [2x_hip_yaw2rol.STL](../structure/2x_hip_yaw2rol.STL) | 2 | Rigid material: confirm profile |
| [hip_yaw_support.STL](../structure/hip_yaw_support.STL) | 1 | Rigid material: confirm profile |
| [jaw.stl](../structure/jaw.stl) | 1 | Rigid material: confirm profile |
| [left_foot.stl](../structure/left_foot.stl) | 1 | Rigid material: confirm profile |
| [mouth_buttom_tpu.stl](../structure/mouth_buttom_tpu.stl) | 1 | TPU indicated by filename |
| [mouth_up_tpu.stl](../structure/mouth_up_tpu.stl) | 1 | TPU indicated by filename |
| [right_foot.stl](../structure/right_foot.stl) | 1 | Rigid material: confirm profile |
| [thigh_left_shell.stl](../structure/thigh_left_shell.stl) | 1 | Rigid material: confirm profile |
| [thigh_right_shell.stl](../structure/thigh_right_shell.stl) | 1 | Rigid material: confirm profile |

### Optional roller skates — existing files

Print these additional parts for the roller skates. They also require 4 additional M2 × 6 countersunk, flat-end self-tapping screws and 8 additional 10 × 15 × 3 mm bearings, included in the totals in [BOM.md](../BOM.md).

| File | Planned copies | Material note |
| --- | ---: | --- |
| [2x_tire_support.STL](../structure/2x_tire_support.STL) | 2 | Material/profile to be confirmed |
| [4x_tire.STL](../structure/4x_tire.STL) | 4 | Material/profile to be confirmed |
| [4x_tire_axis.STL](../structure/4x_tire_axis.STL) | 4 | Material/profile to be confirmed |

## Print profile still required

The release needs tested values for material brand/type, nozzle, layer height, walls, infill, supports, orientation, scale and tolerances, with finished-part photographs. TPU hardness is also unspecified. No recommended print time or filament mass has been measured here.

Before a full print, check one servo mount and one bearing seat, inspect left/right orientation and verify cable clearance. Record your settings and report fit results with the part filename. A slicer project from a different revision is not a verified profile for these STLs.
