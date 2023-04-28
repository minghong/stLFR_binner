import sys

file=open(sys.argv[1])
dic={}
for line in file.readlines():
    if(line[0]==">"):
        tmp=line.split()
        h=tmp[0][1:]
        dic[h]=""
    else:
        dic[h]=dic[h]+line.rstrip("\n")
new={};m=0
file=open(sys.argv[2])

for line in file.readlines():
    tmp=line.split()
    ll=tmp[0].split("_")
    #new[tmp[0]]=ll[0]+"_"+tmp[1]
    new[tmp[0]]=tmp[1]

x={};lis=[]
for k,v in new.items():
    lis.append(k)
    if(v not in x.keys()):
        x[v]=dic[k];
    else:
        
        x[v]=x[v]+"NNNN"+dic[k]

for k,v in x.items():

        print(">"+k)
        print(v)

for k,v in dic.items():
    if (k not in lis and len(v)>=10000):
        print(">"+k)
        print(v)

