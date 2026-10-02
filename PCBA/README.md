# ArduinoUnoQ connector correction — 2026-10-02

## 中文：已生产 PCB 的处理说明

**U3、U4、U5 舵机接口的 GND 与 SIGNAL 在旧版设计中接反。使用旧文件生产的 PCB，请先断电核对并处理，再连接舵机。U2 是稳压器，不属于此次换线范围。**

本次更新替换 `ArduinoUnoQ.SchDoc` 和 `ArduinoUnoQ.PcbDoc`。下面的旧版映射已在更新前的提交 [`703bfd2`](https://github.com/LuwuDynamics/xgoduck_hardware/tree/703bfd274071cb545b1ed6f512f3c81cf91e447b/PCBA) 中核实；更早批次请按实际网络测量确认，不能仅凭下载日期判断。

| 接口 | 引脚号 | 旧 PCB 网络 | 2026-10-02 修订文件网络 |
| --- | --- | --- | --- |
| U3 / U4 / U5 | 1 | GND | SIGNAL |
| U3 / U4 / U5 | 2 | VCC8.4V | VCC8.4V（不变） |
| U3 / U4 / U5 | 3 | SIGNAL | GND |

以上编号是工程内的焊盘编号，不代表从任意观察方向看到的左、中、右。确认插头朝向和焊盘编号，不要只凭线色或旧图纸判断。

### 已生产旧板：优先使用换线或专用转接线

1. 断开电池、USB 和其他电源，拔下舵机及外接线束。用旧版工程和万用表通断测量，确认实际板卡符合上表“旧 PCB 网络”。
2. 对每一路实际使用的 U3、U4、U5，在**板端插头这一端**交换 GND 与 SIGNAL 两根线的端子（对应 1、3 号位置），2 号电源线保持原位；也可制作专用交叉转接线。舵机端保留其原本正确的接线。不要把插头强行反插，也不要在同一线束两端都交换，否则会抵消修正。
3. 断电状态下逐线确认：板卡 GND 最终到舵机 GND、VCC8.4V 到舵机电源、SIGNAL 到舵机信号；确认电源与地没有短接，端子锁止可靠、没有裸露导体。
4. 确认线路后，在机器人可靠支撑、具有限流保护的条件下先做单个舵机通信测试，再逐路恢复。若不能可靠识别针位或测量结果不符，停止接线并联系 `hello@xgorobot.com`。
5. 给改过的线束标明“仅用于旧版 ArduinoUnoQ 板”。切换到修订 PCB 时，应恢复标准线束，不能继续使用这条交叉线。

该方法补偿旧 PCB 的接口顺序，不改变板上铜箔。若需把旧板改成标准线束可直接使用的版本，应由有经验的人员根据实际铜层连接制定割线、隔离及飞线方案，并验证断开和重连结果；这里未验证具体割线点位，不提供可直接照做的割线图。不要直接短接 GND 和 SIGNAL。

### 尚未生产的用户

使用此次修订的 `.SchDoc` 和 `.PcbDoc`，在 Altium 中检查原理图与 PCB 一致性，重新铺铜并运行 ERC/DRC，再重新生成 Gerber、钻孔及所需生产资料。此次未重新导出仓库内 PDF、DWG、STEP、BOM 或坐标文件；它们不能作为此次引脚修订已同步的证明，生产前须重新导出或核对。

### 验证范围

已读取新旧 PCB 的焊盘网络，确认三个接口 1、3 脚的网络互换，2 脚及三个接口的焊盘坐标保持一致；上传的两个工程文件与维护者提供的文件逐字节一致。未完成 Altium ERC/DRC、全部铜箔连通性检查或实物返修测试。换线方案基于已核实的网络映射，实施后仍需按上述步骤验证。

## English: notice for previously manufactured boards

**The old design reverses GND and SIGNAL on servo connectors U3, U4 and U5. Disconnect power and check affected boards before connecting servos. U2 is a regulator and is not part of this connector correction.**

The old PCB at commit `703bfd274071cb545b1ed6f512f3c81cf91e447b` has pin 1 = GND, pin 2 = VCC8.4V, pin 3 = SIGNAL. The supplied 2026-10-02 revision changes this to pin 1 = SIGNAL, pin 2 = VCC8.4V, pin 3 = GND. These are CAD pad numbers, not a left-to-right viewing convention. Verify other production batches by their actual connectivity.

For a confirmed old board, swap the GND and SIGNAL terminals **at the board end only** of each affected cable, or use a dedicated crossover adapter. Keep power on pin 2 and retain the correct servo-end wiring. Do not force a keyed plug backwards or swap both ends of the same cable. With all power removed, verify board GND reaches servo GND, power reaches servo power, and signal reaches servo signal; check for a power-to-ground short and secure the terminals. Start with one servo and current-limited power while supporting the robot. Label the modified cable for old-board use only; use normal wiring with the revised board. Contact `hello@xgorobot.com` if pin identification or continuity is uncertain.

This is a cable workaround, not a copper repair. No board cutting/jumper locations have been validated; do not bridge GND and SIGNAL. Board-level rework requires a separately verified isolation and reconnection plan.

For new production, use the revised schematic and PCB, check their consistency, repour copper, run ERC/DRC, and regenerate manufacturing outputs. Only the two Altium source files were replaced; existing PDF, DWG, STEP, BOM and placement exports were not regenerated for this correction and require review or regeneration.

Validation covers extracted PCB pad-net assignments and source-file byte equality, not a full copper-connectivity audit, Altium ERC/DRC or physical rework testing.
