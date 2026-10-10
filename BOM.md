# XGO-Duck Bill of Materials

[Project overview](readme.md) · [Assembly guide](Assembly_Guide.pdf) · [Component specifications](docs/BOM.md)

Parts and purchasing quantities for one XGO-Duck build, initially transcribed from the robot BOM in Git commit `80be3e2`. The maintainer corrected the fastener descriptions for items 7–9 on 2026-10-10; their quantities are unchanged. Other purchase links and battery requirements are preserved from the original workbook. A dash means no purchase link was supplied.

## Parts list

| No. | Part | Quantity | Purchase link | Specification / notes |
| ---: | --- | ---: | --- | --- |
| 1 | Arduino UNO Q (2 GB / 4 GB) | 1 | [Arduino Store](https://store.arduino.cc/) | — |
| 2 | Robot expansion board | 1 | [Luwu Dynamics Store](https://shop.xgorobot.com/products/robot-driver-board?variant=67594424713467) | See [PCBA design files](PCBA/). |
| 3 | AMP 3-pin cable | 15 | [Feetech servo kit](https://www.alibaba.com/product-detail/Microduck-Servo-Kit-Feetech-Low-Cost_1601942207064.html?spm=a2756.order-detail-bn.0.0.6b072fc22OPijK) | Shared purchase link with item 4 in the original workbook. |
| 4 | Feetech 1910 servo | 15 | [Feetech servo kit](https://www.alibaba.com/product-detail/Microduck-Servo-Kit-Feetech-Low-Cost_1601942207064.html?spm=a2756.order-detail-bn.0.0.6b072fc22OPijK) | Shared purchase link with item 3 in the original workbook. |
| 5 | 18650 battery pack, 8.4 V | 1 | — | XH2.54 connector; capacity **> 2,500 mAh**; discharge rating **> 3C**. |
| 6 | 8.4 V Li-ion battery charger | 1 | — | 5.5 × 2.1 mm DC barrel plug (DC5521). |
| 7 | M2 × 6 countersunk, flat-end self-tapping screw | 200 | — | [Shape and photo reference](#fastener-identification) |
| 8 | M2.3 × 8 flat-top round-head, flat-end self-tapping screw | 6 | — | [Shape and photo reference](#fastener-identification) |
| 9 | M3 × 16 round-head machine screw | 4 | — | [Shape and photo reference](#fastener-identification) |
| 10 | Bearing, 10 × 15 × 3 mm | 2 | [Tmall](https://detail.tmall.com/item.htm?id=721793990910&skuId=6237461598360) | — |
| 11 | Bearing, 16 × 22 × 4 mm | 11 | [Tmall](https://detail.tmall.com/item.htm?id=721793990910&skuId=6237461598469) | — |

## Fastener identification

<img src="media/bom/fastener-shapes.svg" alt="Side-view shape guide for BOM item 7 M2 by 6 countersunk flat-end self-tapping screw, item 8 M2.3 by 8 flat-top round-head flat-end self-tapping screw, and item 9 M3 by 16 domed round-head machine screw" width="900">

The illustrations distinguish the three head and thread types; they are **not dimensioned drawings or product photos**. Seller pages below show actual fasteners with the matching size option. Select that option and check head, flat end where specified, thread type, drive, material and finish against your build before ordering. These links are photo references, not validated suppliers for this project.

<img src="media/bom/round-head-reference.jpg" alt="User-supplied reference photo showing the intended low, gently domed round screw head" width="280">

**Round-head style reference for item 9 only.** This supplied photo clarifies its shallow, domed head profile. Item 8 keeps the **same rounded side profile**, but its **top surface is flat**. The photo does not establish item 9's diameter, length or thread type; use the specifications in the parts list for those details.

| Item | Product photo / size reference |
| ---: | --- |
| 7 | [M2 × 6 countersunk flat-end self-tapping screw](https://www.rakuten.com.tw/shop/longteng010/product/zzc0d6xyk/) — select **M2*6**. |
| 8 | [M2.3 × 8 flat-end self-tapping listing](https://i-item.jd.com/10131153225220.html) — select **M2.3*8**. This is a size/thread reference; its head profile has not been confirmed against the shape guide. |
| 9 | [M3 × 16 round-head machine screw](https://www.partco.fi/en/mechanics/screwsnutswashers/metal-screwsnutwashers/9369-m-ru-m3x16.html). |

## Battery connector reference

<img src="media/bom/battery-reference.png" alt="Battery connector reference extracted from the original BOM, showing a white connector with red and black wires" width="230">

Original workbook image accompanying the battery entry. Confirm the mating connector and polarity against the actual board before connection. The image alone does not define a pinout.

## Build notes

- Quantities are the original purchasing quantities, including fasteners. The item 7–9 descriptions reflect the maintainer's 2026-10-10 correction. Follow the [assembly guide](Assembly_Guide.pdf) for installation.
- The battery label and requirements above reproduce the source. Exact pack configuration, compatible charger and polarity require confirmation; see the [battery specification notes](docs/BOM.md#battery-and-charger-specification-still-to-be-finalized).
- Printed parts are available in [structure/](structure/), with a separate [printing inventory](docs/PRINTING.md).
- The [PCB manufacturing BOM](PCBA/BOM.xlsx) lists components for making the expansion board. Those components are already included when using a finished board.
