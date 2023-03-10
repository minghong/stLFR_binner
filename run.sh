#!/bin/bash
OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)

      cat input_file/5000_2000_jaccard.txt |awk '{if($3>0.01) print($0)}' > 1.txt

        python "${DIR}"/python_code/infomap_python.py 1.txt> stag1_group.txt


       python "${DIR}"/python_code/merge.py $1  stag1_group.txt > input_file/stag1_merge.fa


        #bowtie2-build  -f input_file/stag1_merge.fa mm

        #bowtie2 -1 $2 -2 $3 -p $5 -x mm | samtools sort -O bam -@ 10 -o - > contig.bam

        #jgi_summarize_bam_contig_depths --outputDepth input_file/contig.depth.txt contig.bam

        #awk '{print $1"\t"$3}' input_file/contig.depth.txt > depth.txt

        checkm tetra -t $5 input_file/stag1_merge.fa  TDP.txt


#for i in {10..100}
	python "${DIR}"/python_code/k_means.py 37 > stag2_group.txt 
	
	python "${DIR}"/python_code/bins.py  $1 $4
	checkm lineage_wf -t 3 -x fa $4/ --nt --tab_table -f $4/37_bins_qa.txt checkout/ 
	rm -rf checkout

	rm *.txt



	#sed  "s/_/ /g" stag2_group.txt | awk '{print $1"\t"$3}' > name_module.txt

	#python /dellfsqd2/ST_OCEAN/USER/xuqi/final/run/jaccard_infomap/module_pre_count.py name_module.txt> tmp.txt

	#sort -k1n tmp.txt > module_pre_count.txt
	#python /dellfsqd2/ST_OCEAN/USER/xuqi/final/run/pic/method_plt.py  module_pre_count.txt 81 module.png
