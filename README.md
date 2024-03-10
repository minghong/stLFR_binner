# stLFR_binner

you can use it as fllows:

wget https://github.com/minghong/stLFR_binner/archive/refs/heads/main.zip

unzip main.zip


cd stLFR_binner-main

chmod 755 *

conda create --name binner python=3.6

conda install -c bioconda checkm-genome #安装checkm

conda activate binner  #创建新的虚拟环境

bash rely.sh

binner -i contig.fa -1 1.fastq -2 2.fastq -o out_dir -t 10

If you have any question,please contact me: xuqi@seu.edu.cn
