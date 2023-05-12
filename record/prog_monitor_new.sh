#!/bin/bash

if [[ $# -lt 4 ]]; then
    echo "Usage:this tool can monitor a programm at coarse grain resolution"
    echo "$0 pid step_size step_num outfile_prefix"
    exit 1
fi

pid=$1
size=$2
num=$3
logfile=$4

echo -e "PID\tUSER\tPR\tNI\tVIRT\tRES\tSHR\tState\tCPU\t%MEM\tTIME\tCommand" >> ${logfile}.log

count=0
while [ $count -le $num ]
do
    now_time=$(date)
    echo " the log time is $now_time" >>${logfile}.log
    pid_list=`pstree -p $pid  | grep -o '([0-9]*)' | grep -o  '[0-9]*'`
    #echo $pid_list
    #exit 1
    if [ ! -n "${pid_list}" ]; then
        echo "The process end" >> ${logfile}.log
        exit 1
    else 
        top -b -n 1 > tmp.top
        for tmp_pid in ${pid_list[@]}
        do
            #echo $tmp_pid
            out=`awk -v v1="${tmp_pid}" '{if($1==v1) print $0}' tmp.top`
            if [ ! -n "${out}" ]; then
                echo  -e "${tmp_pid}\thas not been captured" >> ${logfile}.log
            else
                echo "${out}" >> ${logfile}.log
                echo "${out}" >> tmp.frame
            fi
        done

        out2=`awk 'BEGIN{tot_cpu=0.0; tot_mem=0.0}{tot_cpu=tot_cpu+1.0*$9; tot_mem=tot_mem+1.0*$10}END{print tot_cpu, "\t", tot_mem}' tmp.frame`
        rm tmp.frame
        rm tmp.top
        echo -e "total_CPU_MEM\t${out2}" >> ${logfile}.log

        sleep ${size}
    fi

done

