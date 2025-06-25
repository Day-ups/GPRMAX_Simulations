import os
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data

dmax = r"E:\GPRMAX_Simulations"  # 项目目录
filename = os.path.join(dmax, "iofiles/ex1.in")  # 组合得到gprmax位置下的输入文件gpr.in
# 正演
# 输入文件（filename），生成扫描次数（n），使用第0块GPU加速（gpu={0}）
api(filename, n=3, gpu={0})
# 如果有gpu加速，就是api(filename, n=3, gpu={0})

# 获取回波数据
filename = os.path.join(dmax, "iofiles\ex11.out")  # 获取当前目录下第一次扫描输出的文件（获取哪一次A扫数据后面就是画哪一次图像）
rxnumber = 1  # 发射天线数量
rxcomponent = 'Ez'  # 接收Ez向数据
outputdata, dt = get_output_data(filename, rxnumber, rxcomponent)  # 获得回波数据(outputdata)和时间分辨率（dt）

# 保存为.txt类型数据
np.savetxt("gpr_Ascan1.txt", outputdata, delimiter=' ')

# 画A扫波形图
from tools.plot_Ascan import mpl_plot
from gprMax.receivers import Rx

outputs = Rx.defaultoutputs
outputs = ['Ez']
print(outputs)
plt = mpl_plot(filename, outputs)
plt.show()