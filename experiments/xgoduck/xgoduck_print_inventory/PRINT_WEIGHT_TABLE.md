# XGO-Duck printed-parts weight estimate

100% solid; PLA 1.24 g/cm3, TPU 1.21 g/cm3; no supports, waste or electrical parts.
STL volume × assumed density. This is a fully solid material estimate, not a slicer result.
Actual infill, wall thickness, density, supports and waste change the result.

| STL part | Quantity | Material | Each (g) | Total (g) | Mesh closed? |
|---|---:|---|---:|---:|---|
| 2x_ankle_axis.STL | 2 | PLA | 0.27 | 0.54 | yes |
| 2x_foot_bottom_tpu.stl | 2 | TPU | 14.09 | 28.18 | yes |
| 2x_hip_rol_output.stl | 2 | PLA | 6.41 | 12.81 | yes |
| 2x_hip_rol_shell.stl | 2 | PLA | 1.20 | 2.41 | yes |
| 2x_hip_yaw2rol.STL | 2 | PLA | 4.36 | 8.73 | yes |
| 2x_neck.stl | 2 | PLA | 0.47 | 0.93 | yes |
| 2x_shank.stl | 2 | PLA | 5.32 | 10.63 | yes |
| 2x_thigh_support.stl | 2 | PLA | 1.97 | 3.94 | yes |
| battery.stl | 1 | PLA | 15.59 | 15.59 | yes |
| body.stl | 1 | PLA | 10.16 | 10.16 | yes |
| body_left_shell.stl | 1 | PLA | 15.16 | 15.16 | yes |
| body_right_shell.stl | 1 | PLA | 15.32 | 15.32 | yes |
| eye.stl | 1 | PLA | 0.95 | 0.95 | yes |
| eye_shell.stl | 1 | PLA | 5.70 | 5.70 | yes |
| head.stl | 1 | PLA | 53.25 | 53.25 | yes |
| head_pitch.stl | 1 | PLA | 4.97 | 4.97 | yes |
| head_servo_support.stl | 1 | PLA | 13.90 | 13.90 | yes |
| head_shell.stl | 1 | PLA | 50.95 | 50.95 | yes |
| head_yaw.STL | 1 | PLA | 4.72 | 4.72 | yes |
| hip_yaw_support.STL | 1 | PLA | 1.99 | 1.99 | yes |
| jaw.stl | 1 | PLA | 19.50 | 19.50 | yes |
| left_foot.stl | 1 | PLA | 21.16 | 21.16 | yes |
| mouth_buttom_tpu.stl | 1 | TPU | 16.73 | 16.73 | yes |
| mouth_up_tpu.stl | 1 | TPU | 4.32 | 4.32 | yes |
| right_foot.stl | 1 | PLA | 21.14 | 21.14 | yes |
| thigh_left_shell.stl | 1 | PLA | 8.84 | 8.84 | yes |
| thigh_right_shell.stl | 1 | PLA | 8.83 | 8.83 | yes |
| **TOTAL** | **35** | | | **361.35** | |

PLA: 312.12 g; TPU: 49.23 g.

Optional roller skate pieces are excluded. Two flexible foot soles and both mouth parts are TPU according to upstream filenames.

**Quantity conflict:** the upstream folder contains `2x_hip_yaw2rol.STL` but its print inventory refers to `hip_yaw2rol.STL` with quantity one. This report follows the actual filename prefix (two); confirm against the illustrated assembly guide before printing.

Source: https://github.com/LuwuDynamics/xgoduck_hardware/tree/106186e1beda690c28f485a754538d6f41b5d025/structure
Upstream inventory: https://github.com/LuwuDynamics/xgoduck_hardware/blob/106186e1beda690c28f485a754538d6f41b5d025/docs/PRINTING.md
