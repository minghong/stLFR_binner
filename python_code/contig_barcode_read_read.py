
import sys


out=open(sys.argv[2],"w")

infile = open(sys.argv[1], 'r')

a=0;b=0;dic={}
for lines in infile.readlines():
    if(lines==""):
        continue
    tmp=lines.split()
    if(a==0 and b==0):
        a=tmp[0];b=tmp[1]
    if(a==tmp[0] and b==tmp[1]):
        dic.setdefault(tmp[1],[]).append(tmp[2])
    else:       
        for j in dic.keys():
            out.write(a+"\t"+b+'\t')
            for h in range(0,len(dic[j])):
                if(h==0):
                    out.write(str(dic[j][h]))
                else:
                    out.write(":"+str(dic[j][h]))
            out.write('\n')
        a=tmp[0];b=tmp[1];dic={}
        dic.setdefault(tmp[1],[]).append(tmp[2])

out.close()

