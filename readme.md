# XGO Duck 硬件

XGO Duck 是基于 [Arduino Uno Q](https://docs.arduino.cc/hardware/uno-q/) 的双足鸭子机器人。本仓库给出把它做出来所需的结构件、扩展板和物料，包括可打印零件、电路工程、整机清单和装配说明。

行走、起立和拾取策略，以及 Uno Q 上的固件和网页控制，在配套仓库 [xgoduck_runtime_arduino](https://github.com/LuwuDynamics/xgoduck_runtime_arduino)。

## 声明与引用

XGO Duck 的鸭子外形、15 个舵机的关节布置，以及策略所沿用的关节顺序，来自 [Pollen Robotics](https://pollen-robotics.com/microduck/) 的 [Microduck](https://github.com/pollen-robotics/microduck)。

Microduck 约 25 cm 高、不到 800 g，由 15 个舵机驱动，神经网络策略以 50 Hz 运行。它的机载软件以 [Apache License 2.0](https://github.com/pollen-robotics/microduck/blob/main/LICENSE) 发布。强化学习、仿真模型和三维网格在 [microduck_rl](https://github.com/pollen-robotics/microduck_rl)。该仓库说明：软件为 Apache 2.0，三维模型文件以 Creative Commons BY-NC-SA 授权（原文写作 BY-SA-NC）。

本仓库是 Luwu Dynamics 面向 Arduino Uno Q 的硬件实现，相对 Microduck 做了这些改动：

- 主控改为 Arduino Uno Q，一侧是 Qualcomm Linux，一侧是 STM32
- 舵机改为飞特 1910，共 15 只
- 扩展板自行设计，板上有 QMI8658 惯性传感器、电源和舵机总线

Pollen Robotics 未公开量产结构与电路。使用或再分发本仓库时，请保留对 Microduck 与 Pollen Robotics 的署名。若某件几何取自 [microduck_rl](https://github.com/pollen-robotics/microduck_rl) 的公开模型，该几何还须遵守 Creative Commons BY-NC-SA：署名、以相同方式共享、非商业使用。

## 仓库结构

```text
readme.md                         本说明
Assembly_Guide.pdf                装配说明
bom.xlsx                          整机物料
PCBA/                             Arduino Uno Q 扩展板
  ArduinoUnoQ.SchDoc              Altium 原理图
  ArduinoUnoQ.PcbDoc              Altium PCB
  ArduinoUnoQ.pdf                 原理图与 PCB 图
  ArduinoUnoQ.DWG                 板框
  ArduinoUnoQ.step                板级三维
  BOM.xlsx                        贴片物料
  Pick Place for ArduinoUnoQ.csv  贴片坐标
structure/                        可打印结构件（STL）
```

| 路径 | 用途 |
| --- | --- |
| `structure/` | 打印躯干、腿、头颈和软胶件，再按装配说明安装 |
| `PCBA/` | 制作叠在 Arduino Uno Q 上的扩展板：原理图、PCB、三维、贴片 BOM 和坐标 |
| `bom.xlsx` | 整机采购清单：主控、扩展板、舵机、线材、电池、螺丝和轴承 |
| `Assembly_Guide.pdf` | 按图装配 |

`structure/` 里以 `2x_` 开头的文件各打印两份。左右件分成两个文件，例如 `left_foot.stl` 和 `right_foot.stl`。文件名中带 `tpu` 的零件用软料打印，包括脚底和嘴巴。

### 结构件

- 躯干：`body.stl`、`body_left_shell.stl`、`body_right_shell.stl`、`battery.stl`
- 腿：`thigh_left_shell.stl`、`thigh_right_shell.stl`、`2x_thigh_support.stl`、`2x_shank.stl`、`hip_yaw_support.STL`、`hip_yaw2rol.STL`、`2x_hip_rol_shell.stl`、`2x_hip_rol_output.stl`、`2x_ankle_axis.STL`、`left_foot.stl`、`right_foot.stl`、`2x_foot_bottom_tpu.stl`
- 头颈：`2x_neck.stl`、`head.stl`、`head_shell.stl`、`head_pitch.stl`、`head_yaw.STL`、`head_servo_support.stl`、`eye.stl`、`eye_shell.stl`、`jaw.stl`、`mouth_up_tpu.stl`、`mouth_buttom_tpu.stl`

### 扩展板

扩展板叠在 Arduino Uno Q 上，给舵机和传感器供电，并引出舵机总线。板上主要器件：

- QMI8658A 六轴惯性传感器
- 5 V 稳压（H7651）和 AMS1117-3.3
- 舵机座：TE 292253-3 三只，MX1.25 三针三只
- 串口缓冲 SN74LVC1G125、SN74LVC1G126
- 电源开关、DC 座和 XH2.54 电池接口

运行时把舵机总线接在 D0/D1（`Serial1`，1 Mbps），QMI8658 接在 D20/D21（`Wire`）。舵机 ID 与 Microduck 相同：10–14 和 20–24 是两条腿，30–33 是颈和头，34 是嘴。

## 整机物料

数量以 `bom.xlsx` 为准。

| 物料 | 数量 |
| --- | --- |
| Arduino Uno Q | 1 |
| 机器人扩展板 | 1 |
| AMP 三针线 | 15 |
| 飞特 1910 | 15 |
| 18650 电池 | 1 |
| 沉头螺钉 M2×6 | 200 |
| 螺钉 M2.5×6 | 6 |
| 螺钉 M3×16 | 4 |
| 轴承 10×15×3 | 2 |
| 轴承 16×22×4 | 11 |

## 相关链接

- [xgoduck_runtime_arduino](https://github.com/LuwuDynamics/xgoduck_runtime_arduino)：Arduino Uno Q 上的策略、固件和网页控制
- [Microduck](https://github.com/pollen-robotics/microduck)：Pollen Robotics 的机载软件
- [microduck_rl](https://github.com/pollen-robotics/microduck_rl)：策略训练与仿真模型
- [Microduck 产品页](https://pollen-robotics.com/microduck/)
