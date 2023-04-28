
import sys

import networkx as nx

from infomap import Infomap

file1=open(sys.argv[1])

list1=[]
for lines in file1.readlines():
    line=lines.split()
    list1.append(line[0])
    list1.append(line[1])   #把所有contig存下来
    
list_new = list(set(list1))  
dic_1={};dic_2={}
for i in range(0,len(list_new)):  #去重，映射为数字
    dic_1[list_new[i]]=i    
    dic_2[i]=list_new[i]
    

im = Infomap(silent=True,num_trials=20)
G = nx.Graph()
# 添加对应的边和点
file1.close()

file=open(sys.argv[1])

for lines in file.readlines():
    tmp=lines.split()
    #a=int(tmp[0]);b=int(tmp[1]);c=float(tmp[2])
    a=dic_1[tmp[0]];b=dic_1[tmp[1]];c=float(tmp[2])
    if (c>0):
        im.add_link(a,b,c)

im.run()
file.close()
for node, module in im.modules:
    print(dic_2[node], module)



