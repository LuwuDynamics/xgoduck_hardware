# XGO-Duck V5 · 音视频套件适配版

[English](README.md) · 简体中文

本目录提供适配 XGO-Duck 音视频套件的 3D 打印零件。该版本包含面部外壳，以及摄像头、灯光和飞行时间（ToF）传感器各自对应的面部零件。

## STL 文件

目录内有 **50 个独立 STL 文件**，从 [`xgoduckV5.3mf`](../../3DManufacturingFormat/xgoduckV5.3mf) 导出。所有文件名均以 `V5_AUDIO_VIDEO_` 开头，`_01`、`_02` 等后缀用于区分原打印工程中分别摆放的同名件。

| 文件 | 零件 |
| --- | --- |
| [`V5_AUDIO_VIDEO_FACE.stl`](V5_AUDIO_VIDEO_FACE.stl) | 面部外壳 |
| [`V5_AUDIO_VIDEO_FACE_CAMERA.stl`](V5_AUDIO_VIDEO_FACE_CAMERA.stl) | 摄像头对应的面部零件 |
| [`V5_AUDIO_VIDEO_FACE_LIGHT.stl`](V5_AUDIO_VIDEO_FACE_LIGHT.stl) | 灯光对应的面部零件 |
| [`V5_AUDIO_VIDEO_FACE_TOF.stl`](V5_AUDIO_VIDEO_FACE_TOF.stl) | ToF 传感器对应的面部零件 |

目录中还有机身、腿部、脚部和喙部零件，其中脚垫和柔性喙部零件有对应的 TPU 文件。

## 打印和组装

每个带序号的 STL 对应原工程中的一个零件实例。选中的文件各打印一份，不要再按保留的 `2x` 或 `4x` 标记倍增数量。上述文件总数包含可选轮滑套件及两种备选背包外壳；请按 V1 或 V1.1 板卡版本，参考 [3MF 分盘指南](../../3DManufacturingFormat/README_CN.md)选择一种外壳。

1. 将所需 STL 以毫米为单位、按 100% 比例导入切片软件。每个零件保留原工程的打印朝向，并已单独贴底。
2. 文件名含 `TPU` 的零件使用 TPU 耗材。[3MF 分盘指南](../../3DManufacturingFormat/README_CN.md)可用于查看 9 个打印盘和各零件的切片参数。整套打印前，请核对面部零件与套件硬件的配合尺寸。
3. 音视频模块的安装、接线和软件配置以对应套件的说明为准。机器人本体可参考官方硬件文档。[组装指南](../../Assembly_Guide.pdf) · [物料清单](../../BOM.md)

## 项目来源

XGO-Duck 由陆吾智能（Luwu Dynamics）基于 Pollen Robotics 的 Microduck 项目改编。[XGO-Duck 硬件项目](https://github.com/LuwuDynamics/xgoduck_hardware)
