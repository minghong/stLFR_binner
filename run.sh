OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)



cat input_file/jaccard.txt |awk '{if($3>=0.039) print($0)}' > 1.txt

python "${DIR}"/python_code/infomap_no2.py 1.txt> stag1_group.txt

python "${DIR}"/python_code/merge.py tmp.fa  stag1_group.txt > input_file/stag1_merge.fa

checkm tetra -t $5 input_file/stag1_merge.fa  TDP.txt
rm -rf checkout
k=$(tail -1 checkm_2.txt|awk '{print $14}')
python "${DIR}"/python_code/k_means.py $k >stag2_group.txt

echo $k
rm -rf $4/*
python "${DIR}"/python_code/bins.py tmp.fa $4

cd  $4
checkm lineage_wf --pplacer_threads 10 -t 10 -x fa ./ --tab_table -f checkm_2.txt checkout/

