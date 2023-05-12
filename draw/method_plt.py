import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math

from random import choice
import matplotlib.pyplot as plt
 
 
class RandomWalk():
    """一个生成随机漫步数据的类"""
    def __init__(self):
        """初始化随机漫步的属性"""
        # 所有随机漫步都始于(0, 0)
        self.x_values = [0]
        self.y_values = [0]
 
    def fill_walk(self,n):
        """计算随机漫步包含的所有点"""
 
        # 不断漫步， 直到列表达到指定的长度
        while len(self.x_values) < n:
            # 决定前进方向以及沿这个方向前进的距离
            x_direction = choice([1, -1])
            x_distance = choice([0, 1, 2, 3, 4])
            x_step = x_direction * x_distance
 
            y_direction = choice([1, -1])
            y_distance = choice([0, 1, 2, 3, 4])
            y_step = y_direction * y_distance
 
            # 拒绝原地踏步
            if x_step == 0 and y_step == 0:
                continue
 
            # 计算下一个点的x和y值
            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step
 
            self.x_values.append(next_x)
            self.y_values.append(next_y)
start =1
file=open(sys.argv[1])

color_dict = { '1613':'red', '1280':'darkblue', '1351':'black', '1639':'green','1423':'purple',
              '4932':'peru', '287':'brown', '5207':'aqua', '562':'orange','28901':'maroon'}
              
if(int(sys.argv[2])>81):
    m=int(math.sqrt(int(sys.argv[2])))+1
else:
    m=int(math.sqrt(81))+1
fig,ax = plt.subplots(m+1,m)

for i in range(m+1):
   for j in range(m):
       ax[i,j].axis('off')

list=[]
for key in color_dict.keys():
    list.append(key)

for j in range(10):
    ax[0,j].set_xlim(-1,1)  
    ax[0,j].scatter(-0.4,0, color=color_dict[list[j]],s=7)
    ax[0,j].text(0,-0.01,list[j],size=7)


k=-1
for line in file.readlines():
    
    tmp=line.split()
    
    rw = RandomWalk()
    rw.fill_walk(int(tmp[2]))
    i=int((int(tmp[0])-start)/m)
    j=int((int(tmp[0])-start)-m*i)
    ax[i+1,j].scatter(rw.x_values, rw.y_values, s=4,color=color_dict[tmp[1]])
    ax[i+1,j].axis('on')
    ax[i+1,j].get_xaxis().set_visible(False)
    ax[i+1,j].get_yaxis().set_visible(False)

    if(k==tmp[0]):
        ax[i+1,j].spines['bottom'].set_linewidth(3)
        ax[i+1,j].spines['bottom'].set_color('green')
    k=tmp[0]
fig.suptitle('girvan_newman',fontweight ="bold",size=10)
plt.savefig(sys.argv[3])

        
