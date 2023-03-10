import pandas as pd
import time
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import decomposition
from scipy.stats import pearsonr
import numpy as np  
import matplotlib.pyplot as plt  
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs   #生成数据函数  
from sklearn import metrics
import math

if __name__ == '__main__':
    #读取excel文件：
    file=open("stag1_merge.fa")
    
    clusters=int(sys.argv[1])
    dic={}
    for line in file.readlines():
        if(line[0]==">"):
            tmp=line[1:].strip("\n")
        else:
            dic[tmp]=len(line)
            
    new_dic=sorted(dic.items(), key=lambda x: x[1],reverse=True)
    
    for i in range(clusters):
        print(new_dic[i][0])
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

    #PCA降维：
    f=[]
    for i in range(clusters):
        f.append(str(new_dic[i][0]))

        
    model = KMeans(n_clusters=clusters,init=data.loc[f])

# Note I'm scaling the data to normalize it! Important for good results.
    model = model.fit(data)
     
    # We can look at the clusters each data point was assigned to
    for i in range(len(model.labels_)):
        print(data.index[i],model.labels_[i])
        
    




