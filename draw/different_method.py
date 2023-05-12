import sys
import matplotlib.pyplot as plt
import sys
from networkx.algorithms.community import *
import networkx as nx
import networkx as nx
import numpy as np
from infomap import Infomap
from communities.algorithms import *

file=open(sys.argv[1])

list1=[]

for lines in file.readlines():
    line=lines.split("\t")
    list1.append(line[0])
    list1.append(line[1])   #把所有contig存下来
    
list_new = list(set(list1))  
list_new.sort()      
dic_1={};dic_2={}
for i in range(0,len(list_new)):  #去重，映射为数字
    dic_1[list_new[i]]=i    
    dic_2[i]=list_new[i]
    
matrix1 = [[0 for j in range(len(list_new))] for i in range(len(list_new))]

file=open(sys.argv[1])

for lines in file.readlines():
    tmp=lines.split()
    tmp[2]=tmp[2].rstrip("\n")
    matrix1[dic_1[tmp[0]]][dic_1[tmp[1]]]=float(tmp[2])
    matrix1[dic_1[tmp[1]]][dic_1[tmp[0]]]=float(tmp[2])

adj_matrix = np.array(matrix1)
'''
spectral_clustering algorithms

print("spectral_clustering")
out=open("/dellfsqd2/ST_OCEAN/USER/xuqi/task/final/process/bacteria_split_sam/10xdata/data/jaccard/different_method/spectral_clustering.txt","w")
communities1 = spectral_clustering(adj_matrix,k=10)
m=0
for i in range(len(communities1)):
    for value in communities1[i]:
        out.write(dic_2[value]+"\t"+str(m)+"\n")
    m=m+1

out.close()
'''    
'''
louvain_method algorithms
'''

try:
    communities1, _ = louvain_method(adj_matrix)
    module=0
    for i in range(len(communities1)):
        for value in communities1[i]:
            print(dic_2[value],module)
        module=module+1
except:
    print("wrong")


#girvan_newman algorithms
'''
try:
    communities1, _ = girvan_newman(adj_matrix)
    module=0
    for i in range(len(communities1)):
        for value in communities1[i]:
            print(dic_2[value],module)
        module=module+1

except:
    print("wrong")
    
'''