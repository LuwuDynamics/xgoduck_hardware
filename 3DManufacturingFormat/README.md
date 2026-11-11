# XGO-Duck — Complete 3MF Print Projects

**English** · [简体中文](README_CN.md)

Choose **V5 for the audio/video design** or **V2 for the original design**. These projects bundle the model parts, prepared plate layouts, and saved print settings, so you do not need to download and arrange individual STL files.

## Download the matching version

| Robot version | Project file | Direct download | Saved setup |
| --- | --- | --- | --- |
| **V5 — Audio/video design** | `xgoduckV5.3mf` | [Download V5 3MF](https://raw.githubusercontent.com/LuwuDynamics/xgoduck_hardware/master/3DManufacturingFormat/xgoduckV5.3mf) | P1P · 0.4 mm nozzle · 9 plates |
| **V2 — Original design** | `XGO_duckV2.3mf` | [Download V2 3MF](https://raw.githubusercontent.com/LuwuDynamics/xgoduck_hardware/master/3DManufacturingFormat/XGO_duckV2.3mf) | P1P · 0.4 mm nozzle · 9 plates |

For individual models, use the [current V5 STL set](../structure/) or the [original V2 STL set](https://github.com/LuwuDynamics/xgoduck_hardware/tree/9a97c3dac11d445691c228ccd9f1ecaa8eec28c9/structure). Keep the parts for your chosen robot version together; do not mix head parts across versions.

## Open, check, slice and print

1. Download the 3MF for your robot version and open it **as a project in Bambu Studio** to retain the saved plate layout and settings.
2. Confirm your actual printer, nozzle, build plate and filament assignments. Both files save a **Bambu Lab P1P, 0.4 mm nozzle, 0.20 mm layer height** profile with **PLA and TPU** filament settings. If you use another printer or material, select the matching settings before slicing.
3. Review the selected plates and preserve the prepared part orientations. Check the original project preview before rearranging anything.
4. Use the appropriate PLA or TPU filament for each part. Select **one backpack enclosure** for your board revision, and include the roller-skate plates only if you need that accessory.
5. Slice the selected plates, inspect the toolpath preview, then send the print job or export the sliced file supported by your printer.

**These downloads are editable 3MF projects, not pre-sliced G-code. They need to be sliced for your printer before printing. Saved settings do not establish a validated profile for every printer and filament.**

## Plate guide

Each project has nine saved plates. The two enclosure plates are alternatives, not two different robot versions.

### V5 — Audio/video design

| Plate | Saved label / purpose |
| --- | --- |
| 1–3 | PLA parts |
| 4 | TPU parts; saved label: `TPU90-95` |
| 5 | Backpack enclosure for the V1 board |
| 6 | Backpack enclosure for the V1.1 board |
| 7 | PLA parts |
| 8 | Optional roller-skate kit |
| 9 | Exterior parts |

### V2 — Original design

| Plate | Saved label / purpose |
| --- | --- |
| 1 | TPU parts |
| 2 | Yellow PLA parts |
| 3 | Black PLA parts |
| 4–6 | Model parts; these plates have no saved names, so check their previews and filament assignments |
| 7 | Backpack enclosure for the V1 board |
| 8 | Backpack enclosure for the V1.1 board |
| 9 | Optional roller-skate kit |

**V2 and V5 identify robot structure versions. V1 and V1.1 in the enclosure labels identify PCB revisions.** Choose the enclosure that matches your [board](../PCBA/); you do not need to print both enclosure plates.

See the [printing inventory](../docs/PRINTING.md) for individual parts and the [assembly guide](../Assembly_Guide.pdf) for assembly.
