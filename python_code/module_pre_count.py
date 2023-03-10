import sys


dic={}
with open(sys.argv[1]) as f:
    for line in f.readlines():
        tmp=line.split()
        try:
            dic[tmp[1]][tmp[0]]=dic[tmp[1]][tmp[0]]+1
            
        except:
            try:
                dic[tmp[1]][tmp[0]]=1
            except:
                dic[tmp[1]]={}
                dic[tmp[1]][tmp[0]]=1


for id, info in dic.items():
    for key in info:
        print(id,key,info[key])  

