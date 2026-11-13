# Printing inventory

[Project](../readme.md) · [Build guide](BUILD_GUIDE.md)

For complete pre-arranged 3MF projects, use [V5 audio/video or V2 original downloads and the plate guide](../3DManufacturingFormat/README.md) ([简体中文](../3DManufacturingFormat/README_CN.md)). Open the matching project in Bambu Studio, confirm the printer and filaments, then slice before printing.

## Choose the STL set for your kit

| Kit | Folder and instructions | STL files | Filename prefix |
| --- | --- | ---: | --- |
| V2 standard kit, without audio/video | [English](../structure/V2_STANDARD_/) · [简体中文](../structure/V2_STANDARD_/README.zh-CN.md) | 47 | `V2_STANDARD_` |
| V5 audio/video kit | [English](../structure/V5_AUDIO_VIDEO_/) · [简体中文](../structure/V5_AUDIO_VIDEO_/README.zh-CN.md) | 50 | `V5_AUDIO_VIDEO_` |

These sets were exported in millimetres from the corresponding nine-plate 3MF projects. Numbered files already represent separate instances: print each selected file once, without multiplying it again by a retained `2x` or `4x` label. Do not mix parts across robot versions. Each set includes optional roller-skate parts and alternative backpack enclosures; choose one enclosure for your V1 or V1.1 board using the [plate guide](../3DManufacturingFormat/README.md).

The [structure/](../structure/) directory contains only `V2_STANDARD_/` and `V5_AUDIO_VIDEO_/`. Use the matching version folder and its guide for the complete file inventory.

## Optional roller skates

The files below are already included in each version's STL count. For the roller skates, print each numbered file once from your chosen version. They also require 4 additional M2 × 6 countersunk, flat-end self-tapping screws and 8 additional 10 × 15 × 3 mm bearings, included in the totals in [BOM.md](../BOM.md). Confirm the material and slicing profile for these parts.

| Part | Files per version | V2 standard | V5 audio/video |
| --- | ---: | --- | --- |
| Tire supports | 2 | [01](../structure/V2_STANDARD_/V2_STANDARD_2x_tire_support_01.stl), [02](../structure/V2_STANDARD_/V2_STANDARD_2x_tire_support_02.stl) | [01](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_2x_tire_support_01.stl), [02](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_2x_tire_support_02.stl) |
| Tires | 4 | [01](../structure/V2_STANDARD_/V2_STANDARD_TIRE_01.stl), [02](../structure/V2_STANDARD_/V2_STANDARD_TIRE_02.stl), [03](../structure/V2_STANDARD_/V2_STANDARD_TIRE_03.stl), [04](../structure/V2_STANDARD_/V2_STANDARD_TIRE_04.stl) | [01](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_TIRE_01.stl), [02](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_TIRE_02.stl), [03](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_TIRE_03.stl), [04](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_TIRE_04.stl) |
| Tire axes | 4 | [01](../structure/V2_STANDARD_/V2_STANDARD_4x_tire_axis_01.stl), [02](../structure/V2_STANDARD_/V2_STANDARD_4x_tire_axis_02.stl), [03](../structure/V2_STANDARD_/V2_STANDARD_4x_tire_axis_03.stl), [04](../structure/V2_STANDARD_/V2_STANDARD_4x_tire_axis_04.stl) | [01](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_4x_tire_axis_01.stl), [02](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_4x_tire_axis_02.stl), [03](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_4x_tire_axis_03.stl), [04](../structure/V5_AUDIO_VIDEO_/V5_AUDIO_VIDEO_4x_tire_axis_04.stl) |

## Print profile still required

The release needs tested values for material brand/type, nozzle, layer height, walls, infill, supports, orientation, scale and tolerances, with finished-part photographs. TPU hardness is also unspecified. No recommended print time or filament mass has been measured here.

Before a full print, check one servo mount and one bearing seat, inspect left/right orientation and verify cable clearance. Record your settings and report fit results with the part filename. A slicer project from a different revision is not a verified profile for these STLs.
