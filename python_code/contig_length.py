import sys

file=open(sys.argv[1])
dic={}
for line in file.readlines():
    if(line[0]==">"):
        tmp=line.rstrip('\n').split()[0][1:]
        dic[tmp]=""
    else:
        dic[tmp]=dic[tmp]+line.rstrip("\n")
        
for k,v in dic.items():
    print(str(k)+"\t"+str(len(v)))
