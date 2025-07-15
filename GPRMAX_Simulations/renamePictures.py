import os
from natsort import natsorted  # 更自然的排序（如 1, 2, 10 而不是 1, 10, 2）

# 设置路径
base_dir = r"D:\桌面\renameFiles\生成的图片"
output_dir = r"D:\桌面\生成的图片_重命名"  # 新文件夹（保持原结构）

# 创建输出目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取所有子文件夹（按名称排序）
subfolders = natsorted([
    f for f in os.listdir(base_dir)
    if os.path.isdir(os.path.join(base_dir, f))
])

global_counter = 1  # 全局计数器

for folder in subfolders:
    folder_path = os.path.join(base_dir, folder)
    output_subfolder = os.path.join(output_dir, folder)  # 对应的新子文件夹

    # 创建子文件夹（如果不存在）
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    # 获取文件夹内所有图片（按名称排序）
    images = natsorted([
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and
           f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    ])

    # 重命名并复制图片
    for img in images:
        old_path = os.path.join(folder_path, img)
        file_ext = os.path.splitext(img)[1]  # 保留原扩展名
        new_name = f"({global_counter}){file_ext}"
        new_path = os.path.join(output_subfolder, new_name)

        # 复制文件（保留原文件）
        with open(old_path, 'rb') as f_in:
            with open(new_path, 'wb') as f_out:
                f_out.write(f_in.read())

        print(f"重命名: {folder}/{img} → {folder}/{new_name}")
        global_counter += 1

print(f"完成！共处理 {global_counter - 1} 张图片。输出目录：{output_dir}")