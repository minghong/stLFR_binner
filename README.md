# stLFR_binner

you can use it as fllows:

wget https://github.com/minghong/stLFR_binner/archive/refs/heads/main.zip

unzip main.zip

conda activate binner  #创建新的虚拟环境

pip install networkx #安装依赖

pip install infomap

binner -i contig.fa -1 1.fastq -2 2.fastq -o out_dir -t 10


