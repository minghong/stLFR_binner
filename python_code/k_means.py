import pandas as pd
import time
import sys
import pandas as pd
import numpy as np
from sklearn import decomposition
from scipy.stats import pearsonr
import numpy as np  
import matplotlib.pyplot as plt  
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs   #生成数据函数  
from sklearn import metrics
import math
def eucliDist(X,Y):
    return math.sqrt(sum([(x - y)**2 for (x,y) in zip(X,Y)]))

#--------------------------------------------最小-最大规范化--------------------------------------------
def MinMax_Normalize(data):
    text=(data - data.min())/(data.max() - data.min())          #最小-最大规范化
    return text

#--------------------------------------------零-均值规范化--------------------------------------------
def ZeroAvg_Normalize(data):
    text=(data - data.mean())/data.std() 
    return text

#--------------------------------------------小数定标规范化--------------------------------------------
def Float_Normalize(data):
    text=data/10**np.ceil(np.log10(data.abs().max())) 
    return (text)

#--------------------------------------------pca降维代码--------------------------------------------

def PCA(data,n):
#调用sklearn库实现PCA:
    pca = decomposition.PCA()
    pca.fit(data)                                         #X_arr是原始数据集，一行表示一个样本，一列表示一个feature
    pca.n_components = n              #降为1维
    X_reduced = pca.fit_transform(data) #X_reduced是降维后的数据集

    return(X_reduced)

if __name__ == '__main__':
    #读取excel文件：
    start=time.time()
    file=open("TDP.txt")
    dic={}
    for line in file.readlines():
        tmp=line.split()
        if(tmp[0]!="Sequence"):
            for i in range(1,len(tmp)):
                dic.setdefault(tmp[0], []).append(float(tmp[i]))
          
        
    s_key = list(dic.keys())
     
    for k_s in s_key:
         if(len(dic[k_s])==0):
             del dic[k_s]  
        

    data=pd.DataFrame.from_dict(dic).T
    M=MinMax_Normalize(data) 
    F=Float_Normalize(data)
    Z=ZeroAvg_Normalize(data)
    #PCA降维：
    
    model = KMeans(n_clusters=int(int(float(sys.argv[1])*0.01+1)*1.5))

# Note I'm scaling the data to normalize it! Important for good results.
    model = model.fit(data)
     
    # We can look at the clusters each data point was assigned to
    for i in range(len(model.labels_)):
        print(data.index[i],model.labels_[i])
        
    




