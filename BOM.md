# XGO-Duck Bill of Materials

[Project overview](readme.md) · [Assembly guide](Assembly_Guide.pdf) · [Component specifications](docs/BOM.md)

Parts and purchasing quantities for one XGO-Duck build, transcribed from the robot BOM in Git commit `80be3e2`. Purchase links and battery requirements are preserved from the original workbook. A dash means no purchase link was supplied.

## Parts list

| No. | Part | Quantity | Purchase link | Specification / notes |
| ---: | --- | ---: | --- | --- |
| 1 | Arduino UNO Q (2 GB / 4 GB) | 1 | [Arduino Store](https://store.arduino.cc/) | — |
| 2 | Robot expansion board | 1 | [Luwu Dynamics Store](https://shop.xgorobot.com/products/robot-driver-board?variant=67594424713467) | See [PCBA design files](PCBA/). |
| 3 | AMP 3-pin cable | 15 | [Feetech servo kit](https://www.alibaba.com/product-detail/Microduck-Servo-Kit-Feetech-Low-Cost_1601942207064.html?spm=a2756.order-detail-bn.0.0.6b072fc22OPijK) | Shared purchase link with item 4 in the original workbook. |
| 4 | Feetech 1910 servo | 15 | [Feetech servo kit](https://www.alibaba.com/product-detail/Microduck-Servo-Kit-Feetech-Low-Cost_1601942207064.html?spm=a2756.order-detail-bn.0.0.6b072fc22OPijK) | Shared purchase link with item 3 in the original workbook. |
| 5 | 18650 battery pack, 8.4 V | 1 | — | XH2.54 connector; capacity **> 2,500 mAh**; discharge rating **> 3C**. |
| 6 | 8.4 V Li-ion battery charger | 1 | — | 5.5 × 2.1 mm DC barrel plug (DC5521). |
| 7 | Countersunk screw, M2 × 6 | 200 | — | — |
| 8 | Screw, M2.5 × 6 | 6 | — | — |
| 9 | Screw, M3 × 16 | 4 | — | — |
| 10 | Bearing, 10 × 15 × 3 mm | 2 | [Tmall](https://detail.tmall.com/item.htm?id=721793990910&skuId=6237461598360) | — |
| 11 | Bearing, 16 × 22 × 4 mm | 11 | [Tmall](https://detail.tmall.com/item.htm?id=721793990910&skuId=6237461598469) | — |

## Battery connector reference

<img src="media/bom/battery-reference.png" alt="Battery connector reference extracted from the original BOM, showing a white connector with red and black wires" width="230">

Original workbook image accompanying the battery entry. Confirm the mating connector and polarity against the actual board before connection. The image alone does not define a pinout.

## Build notes

- Quantities are the original purchasing quantities, including fasteners. Follow the [assembly guide](Assembly_Guide.pdf) for installation.
- The battery label and requirements above reproduce the source. Exact pack configuration, compatible charger and polarity require confirmation; see the [battery specification notes](docs/BOM.md#battery-and-charger-specification-still-to-be-finalized).
- Printed parts are available in [structure/](structure/), with a separate [printing inventory](docs/PRINTING.md).
- The [PCB manufacturing BOM](PCBA/BOM.xlsx) lists components for making the expansion board. Those components are already included when using a finished board.
