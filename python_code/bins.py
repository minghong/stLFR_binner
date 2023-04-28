# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 08:57:29 2023

@author: 阿布拉卡达布拉
"""
import os

import sys
dic={}
mock=open(sys.argv[1])
for line in mock.readlines():
    if(line[0]==">"):
        tmp=line.rstrip("\n").split()
        dic[tmp[0][1:]]=""
    else:
        dic[tmp[0][1:]]=dic[tmp[0][1:]]+line
mock.close()        
        
group_1={}
group=open("stag1_group.txt")
for line in group.readlines():
    tmp=line.strip('\n').split()
    group_1.setdefault(tmp[1],[]).append(tmp[0])
group.close()
    
group_2={}
group=open("stag2_group.txt")
for line in group.readlines():
    tmp=line.strip('\n').split()
    group_2[tmp[0]]=tmp[1]
    
group.close()
for k,v in group_2.items():
    
    out=open(sys.argv[2]+"/bin"+v+".fa","a")
    if(k in group_1.keys()):
        for i in range(len(group_1[k])):
        
            out.write(">"+group_1[k][i]+"\n"+dic[group_1[k][i]])

    else:
        out.write(">"+k+"\n"+dic[k])

    out.close()
    
    
    
