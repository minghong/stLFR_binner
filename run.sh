#!/bin/bash
OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)

cat input_file/jaccard.txt |awk '{if($3>=0.02) print($0)}' > 1.txt

python "${DIR}"/python_code/infomap_no2.py 1.txt> stag1_group.txt


python "${DIR}"/python_code/merge.py tmp.fa  stag1_group.txt > input_file/stag1_merge.fa

checkm tetra -t $5 input_file/stag1_merge.fa  TDP.txt

python "${DIR}"/python_code/k_means.py $6 >stag2_group.txt
rm $4/*.fa
python "${DIR}"/python_code/bins.py tmp.fa $4

rm -rf checkout
checkm lineage_wf -t 20 -x fa $4/ --tab_table -f checkm.txt checkout/  
