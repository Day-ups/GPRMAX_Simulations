import os
import re

# 配置变量
dmax = "E:\\GPRMAX_Simulations"  # 新的顶层目录路径
old_dmax1 = "D:\\disk_f\\cxcy_gpr\\GPRMAX_Simulations"  # 需要替换的第一处旧路径
old_dmax2 = "D:\\disk_f\\cxcy_gprGPRMAX_Simulations"  # 需要替换的第二处旧路径(注意这里没有斜杠)
input_dir = os.path.join(dmax, "module1", "autoMakeFiles", "results_of_in_files")

# 遍历目录中的所有.in文件
for filename in os.listdir(input_dir):
    if filename.startswith("hollowCylinder_") and filename.endswith(".in"):
        filepath = os.path.join(input_dir, filename)

        # 读取文件内容
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换两处路径
        new_content = content.replace(old_dmax1, dmax)  # 替换第一处
        new_content = new_content.replace(old_dmax2, dmax)  # 替换第二处

        # 如果内容有变化，则写入文件
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已更新文件: {filename}")
        else:
            print(f"无需修改: {filename}")

print("所有文件处理完成！")