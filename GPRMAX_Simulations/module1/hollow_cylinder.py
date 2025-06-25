import os
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import mpl_plot
import matplotlib.pyplot as plt
import shutil
import glob  # 用于遍历文件

dmax = r"E:\GPRMAX_Simulations"  # 项目根目录

# 获取所有以 "hollowCylinder_" 开头的 .in 文件并排序
in_files = sorted(glob.glob(os.path.join(dmax, "module1", "sources", "hollowCylinder_*.in")),
                 key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[1]))

for in_file in in_files:
    # 提取文件名（不含路径和扩展名）
    sim_name = os.path.splitext(os.path.basename(in_file))[0]
    print(f"正在处理文件: {sim_name}")

    # (1) 运行仿真（120个A扫）
    api(in_file, n=120, gpu={0})

    # (2) 合并A扫为B扫
    output_dir = os.path.join(dmax, "module1", "sources")
    merge_files(
        os.path.join(output_dir, sim_name),  # 输入文件前缀（不含.out）
        removefiles=True  # 删除A扫
    )

    # (3) 准备目标目录
    out_files_dir = os.path.join(dmax, "module1", "results", "outFiles")
    os.makedirs(out_files_dir, exist_ok=True)

    # (4) 移动合并的.out文件
    src_merged_file = os.path.join(output_dir, f"{sim_name}_merged.out")
    dst_merged_file = os.path.join(out_files_dir, f"{sim_name}_merged.out")

    if os.path.exists(src_merged_file):
        shutil.move(src_merged_file, dst_merged_file)
        print(f"已移动合并文件到: {dst_merged_file}")
    else:
        raise FileNotFoundError(f"合并文件未生成: {src_merged_file}")

    # (5) 读取合并后的B扫数据（从新位置）
    rxnumber = 1
    rxcomponent = 'Ez'
    outputdata, dt = get_output_data(dst_merged_file, rxnumber, rxcomponent)

    # (6) 保存为txt
    txt_file_path = os.path.join(out_files_dir, f"{sim_name}.txt")
    np.savetxt(txt_file_path, outputdata, delimiter=' ')

    # (7) 绘制B扫描图像
    plt = mpl_plot(dst_merged_file, outputdata, dt * 1e9, rxnumber, rxcomponent)
    plt.ylabel('Time [ns]')

    # (8) 保存图片文件
    output_pic_dir = os.path.join(dmax, "module1", "results", "outPictures")
    os.makedirs(output_pic_dir, exist_ok=True)

    existing_files = [f for f in os.listdir(output_pic_dir)
                      if f.startswith('hollowCylinder_') and f.endswith('.png')]
    i = len(existing_files) + 1

    output_filename = os.path.join(output_pic_dir, f'hollowCylinder_{i}.png')
    plt.savefig(output_filename)