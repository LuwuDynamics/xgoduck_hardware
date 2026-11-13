# XGO-Duck V2 · 普通版套件

[English](README.md) · 简体中文

本目录提供 XGO-Duck 普通版套件的 3D 打印零件，适用于无音频和视频硬件的配置。

## STL 文件

目录内有 **47 个独立 STL 文件**，从 [`XGO_duckV2.3mf`](../../3DManufacturingFormat/XGO_duckV2.3mf) 导出。所有文件名均以 `V2_STANDARD_` 开头，`_01`、`_02` 等后缀用于区分原打印工程中分别摆放的同名件。

| 零件类别 | 文件示例 |
| --- | --- |
| 头部和喙部 | [头盖](V2_STANDARD_HEAD_COVER.stl)、[头部俯仰件](V2_STANDARD_HEAD_PITCH.stl)、[头部舵机固定件](V2_STANDARD_HEAD_SERVO_SUPPORT.stl)、[下巴](V2_STANDARD_JAW.stl) |
| 机身和腿部 | [机身](V2_STANDARD_BODY.stl)、[左脚](V2_STANDARD_LEFT_FOOT.stl)、[右脚](V2_STANDARD_RIGHT_FOOT.stl) |
| 柔性件 | [上喙](V2_STANDARD_MOUTH_UP_TPU.stl)、[下喙](V2_STANDARD_MOUTH_BOTTOM_TPU.stl)、[脚垫](V2_STANDARD_2x_FOOT_BOTTOM_TPU_01.stl) |

## 打印和组装

每个带序号的 STL 对应原工程中的一个零件实例。选中的文件各打印一份，不要再按保留的 `2x` 或 `4x` 标记倍增数量。上述文件总数包含可选轮滑套件及两种备选背包外壳；请按 V1 或 V1.1 板卡版本，参考 [3MF 分盘指南](../../3DManufacturingFormat/README_CN.md)选择一种外壳。

1. 将所需 STL 以毫米为单位、按 100% 比例导入切片软件。每个零件保留原工程的打印朝向，并已单独贴底。
2. 文件名含 `TPU` 的零件使用 TPU 耗材。[3MF 分盘指南](../../3DManufacturingFormat/README_CN.md)可用于查看 9 个打印盘和各零件的切片参数。
3. 普通版套件的组装和备料可参考官方硬件文档。[组装指南](../../Assembly_Guide.pdf) · [物料清单](../../BOM.md)

## 项目来源

XGO-Duck 由陆吾智能（Luwu Dynamics）基于 Pollen Robotics 的 Microduck 项目改编。[XGO-Duck 硬件项目](https://github.com/LuwuDynamics/xgoduck_hardware)
