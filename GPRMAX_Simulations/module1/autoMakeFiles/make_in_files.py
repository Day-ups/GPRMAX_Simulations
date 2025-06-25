import os
import numpy as np

# 配置路径
output_dir = r"E:\GPRMAX_Simulations\module1\autoMakeFiles\results_of_in_files"
os.makedirs(output_dir, exist_ok=True)

# 基础工程模板（精确匹配您提供的模板）
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
#cylinder: 0.600 0.200 0 0.600 0.200 0.002 0.060 water
#geometry_objects_read: 0.520 0.120 0 E:\\GPRMAX_Simulations\\module1\\sources\\hollow_cylinder.h5 E:\\GPRMAX_Simulations\\module1\\sources\\PVC.txt
#cylinder: {water_x} {water_y} 0 {water_x} {water_y} 0.002 0.060 water
#geometry_objects_read: {x_pos} {y_pos} 0 E:\\GPRMAX_Simulations\\module1\\sources\\hollow_cylinder.h5 E:\\GPRMAX_Simulations\\module1\\sources\\pec.txt
"""

# 几何参数（根据您的最新说明修正）
pvc_outer_radius = 0.08  # PVC外径
water_radius = 0.06  # 水柱半径
pvc_inner_radius = 0.06  # PVC内径（计算用）
offset = pvc_outer_radius  # 几何体原点偏移量

# 固定参数
metal_cylinder_x = 0.500
metal_radius = 0.020
src_start_x = 0.040
src_step_x = 0.025
src_steps = 120
src_max_x = src_start_x + (src_steps - 1) * src_step_x
y_max = 0.500  # 根据模板保持y_max=0.5

# 用户选择方向
print("请选择移动方向:")
print("1. x方向 (从左到右)")
print("2. y方向 (从下到上)")
choice = input("请输入选项(1-2): ")

if choice == "1":
    # x方向移动参数
    start_x = pvc_outer_radius + 0.8 + 0.6 # 从金属圆筒1右侧安全距离0.5m开始
    end_x = min(src_max_x, 3.0) - pvc_outer_radius - 0.56  # 到信号源最大距离结束

    # 生成文件
    i = 1
    for x_base in np.arange(start_x, end_x + 0.001, 0.02):  # 步长0.02m
        x_pos = x_base - offset  # 转换为几何体原点坐标
        water_x = x_base  # 水柱中心x坐标

        content = template.format(
            x_pos=x_pos,
            y_pos=0.120,  # y固定
            water_x=water_x,
            water_y=0.200  # 水柱y中心坐标
        )

        filename = os.path.join(output_dir, f"hollowCylinder_{i}.in")
        with open(filename, "w") as f:
            f.write(content)
        print(f"已生成: {filename} - PVC原点: ({x_pos:.3f}, {0.120 - offset:.3f}) 水柱中心: ({water_x:.3f}, 0.120)")
        i += 1

elif choice == "2":
    # y方向移动参数
    start_y = water_radius + 0.7  # 从最下方安全距离0.7m开始
    end_y = y_max - pvc_outer_radius - 0.7  # 到domain上限结束

    # 生成文件
    i = 1
    for y_base in np.arange(start_y, end_y + 0.001, 0.02):  # 步长0.02m
        y_pos = y_base - offset  # 转换为几何体原点坐标
        water_y = y_base  # 水柱中心y坐标

        content = template.format(
            x_pos=1.720,  # x固定
            y_pos=y_pos,
            water_x=1.800,  # 水柱x中心坐标
            water_y=water_y
        )

        filename = os.path.join(output_dir, f"hollowCylinder_{i}.in")
        with open(filename, "w") as f:
            f.write(content)
        print(f"已生成: {filename} - PVC原点: ({1.720 - offset:.3f}, {y_pos:.3f}) 水柱中心: (1.720, {water_y:.3f})")
        i += 1

else:
    print("无效输入!")
    exit()

print(f"\n共生成 {i - 1} 个.in文件")
print(f"移动范围: {start_x:.3f}-{end_x:.3f}m (x)" if choice == "1" else f"移动范围: {start_y:.3f}-{end_y:.3f}m (y)")