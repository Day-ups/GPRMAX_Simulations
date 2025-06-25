import os
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files

dmax = r"E:\GPRMAX_Simulations"  # 项目目录
filename = os.path.join(dmax, 'iofiles\ex1.in')  # 获得输入文件

# 正演获得3次A扫
api(filename, n=3)
merge_files(r".\iofiles\ex1", removefiles=False)  # 将A扫合成B扫，在合成后不删除原文件（removefiles=False）
# r".\gprmax\gpr"代表该位置中的以gpr.in为输入文件的输出的一系列A扫文件（如gpr1.out、gpr2.out…）

# 获取B扫数据
filename = os.path.join(dmax, ".\iofiles\ex1_merged.out")  # 获取生成的B扫文件
rxnumber = 1  # 1个发射天线
rxcomponent = 'Ez'  # 获得Ez向数据
outputdata, dt = get_output_data(filename, rxnumber, rxcomponent)  # B扫数据传给outputdata，时间分辨率传给dt

# 保存为.txt文件
np.savetxt('Bscan.txt', outputdata, delimiter=' ')

# 画出B扫图像
from tools.plot_Bscan import mpl_plot

plt = mpl_plot(filename, outputdata, dt * 1e9, rxnumber, rxcomponent)  # 时间转换为ns
plt.ylabel('Time [ns]')
plt.show()