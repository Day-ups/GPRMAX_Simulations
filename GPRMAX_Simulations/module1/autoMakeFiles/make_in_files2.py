import os
import numpy as np

# 配置路径
output_dir = r"E:\GPRMAX_Simulations\module1\autoMakeFiles\results_of_in_files"
os.makedirs(output_dir, exist_ok=True)

# 更新后的基础工程模板（固定PVC水柱在左侧，移动金属圆柱）
template = """#title: B-scan from a metal cylinder and a PVC hollow cylinder buried in a dielectric half-space
#domain: 3.000 0.500 0.002
#dx_dy_dz: 0.002 0.002 0.002
#time_window: 9e-9

#material: 6 0 1 0 half_space
#material: 81 0.01 1 0 water
#material: 3.3 0 1 0 PVC

#waveform: ricker 1 1.5e9 my_ricker
#hertzian_dipole: z 0.040 0.400 0 my_ricker
#rx: 0 0.400 0
#src_steps: 0.025 0 0
#rx_steps: 0.0250 0 0

#box: 0 0 0 3.000 0.400 0.002 half_space
#cylinder: 0.580 0.200 0 0.580 0.200 0.002 0.060 water
#cylinder: {metal_x} {metal_y} 0 {metal_x} {metal_y} 0.002 0.020 pec
#geometry_objects_read: 0.500 0.120 0 E:\\GPRMAX_Simulations\\module1\\sources\\hollow_cylinder.h5 E:\\GPRMAX_Simulations\\module1\\sources\\PVC.txt
"""

# 几何参数
metal_radius = 0.020  # 金属圆柱半径
water_radius = 0.060  # 水柱半径
pvc_outer_radius = 0.08  # PVC外径

# 固定参数
src_start_x = 0.040
src_step_x = 0.025
src_steps = 120
src_max_x = src_start_x + (src_steps - 1) * src_step_x
y_max = 0.500  # y方向最大值

# 用户选择方向
print("请选择金属圆柱移动方向:")
print("1. x方向 (水平移动)")
print("2. y方向 (垂直移动)")
choice = input("请输入选项(1-2): ")

if choice == "1":
    # x方向移动参数
    start_x = 0.580 + water_radius + 1.0  # 从PVC水柱右侧安全距离0.7m开始
    end_x = min(src_max_x, 3.0) - metal_radius - 0.6  # 到右边界安全距离结束

    # 生成文件
    i = 1
    for metal_x in np.arange(start_x, end_x + 0.001, 0.02):  # 步长0.02m
        content = template.format(
            metal_x=metal_x,
            metal_y=0.120  # y固定
        )

        filename = os.path.join(output_dir, f"hollowCylinder_{i}.in")
        with open(filename, "w") as f:
            f.write(content)
        print(f"已生成: {filename} - 金属圆柱中心: ({metal_x:.3f}, 0.120)")
        i += 1

elif choice == "2":
    # y方向移动参数
    start_y = metal_radius + 0.1  # 从下边界安全距离开始
    end_y = y_max - metal_radius - 0.1  # 到上边界安全距离结束

    # 生成文件
    i = 1
    for metal_y in np.arange(start_y, end_y + 0.001, 0.02):  # 步长0.02m
        content = template.format(
            metal_x=1.720,  # x固定
            metal_y=metal_y
        )

        filename = os.path.join(output_dir, f"hollowCylinder_{i}.in")
        with open(filename, "w") as f:
            f.write(content)
        print(f"已生成: {filename} - 金属圆柱中心: (1.720, {metal_y:.3f})")
        i += 1

else:
    print("无效输入!")
    exit()

print(f"\n共生成 {i - 1} 个.in文件")
print(f"移动范围: {start_x:.3f}-{end_x:.3f}m (x)" if choice == "1" else f"移动范围: {start_y:.3f}-{end_y:.3f}m (y)")