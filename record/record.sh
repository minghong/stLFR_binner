#!/bin/bash

 
pid=`ps -ef | grep $1 | grep -v grep | grep -v '/bin/bash' | head  -n 1 | awk '{printf $2}'`
 
tmpfile=${pid}.tmp
 
if [ -e $tmpfile ]
then 
    rm -rf $tmpfile
fi
 
echo 'timestamp    cpu%' >> $tmpfile

flag=1
result=1
while [ "$flag" -eq 1 ]
do
    time=`date +%T`
    cpu=`top -b -n 1 -c | grep -E $1 | grep -v grep | awk '{ sum_cpu+=$9; } END { printf ("%8.2f%", sum_cpu) }'`
    
    pid2=`ps -ef | grep $1 | grep -v grep | grep -v '/bin/bash' | head  -n 1 | awk '{printf $2}'`
    sleep 1s
    VmHWM=`cat /proc/$1/status |grep VmHWM `
    echo $time'    '$cpu'     '$VmHWM  >> $tmpfile
    if [ -z "$pid2" ]; then
    flag=0
    fi
done

