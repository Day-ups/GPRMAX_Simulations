import os

# 本程序用于对文件夹进行排序
# 指定文件夹路径
folder_path = r"D:\\桌面\\renameFiles\\生成的图片"

# 获取所有子文件夹
subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

# 按名称排序
subfolders_sorted = sorted(subfolders)

# 打印排序结果
print("排序后的子文件夹：")
for i, folder in enumerate(subfolders_sorted, 1):
    print(f"{i}. {folder}")

# 如果需要重命名这些文件夹以反映排序顺序，可以取消下面的注释

# for i, folder in enumerate(subfolders_sorted, 1):
#     old_path = os.path.join(folder_path, folder)
#     new_name = f"{i:03d}_{folder}"  # 在前面添加序号，如"001_原文件夹名"
#     new_path = os.path.join(folder_path, new_name)
#     os.rename(old_path, new_path)
#     print(f"重命名: {folder} -> {new_name}")
