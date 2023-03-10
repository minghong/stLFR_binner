#!/bin/bash
for i in {12..50}
do

     cat 5000_2000_jaccard.txt |awk '{if($3>0.02) print($0)}' > 1.txt

        python python_code/infomap_python.py 1.txt> stag1_group.txt


       python python_code/merge.py Mock10.STLFR_CLOUDSPADES.fa  stag1_group.txt > input_file/stag1_merge.fa


        bowtie2-build  -f input_file/stag1_merge.fa mm

        bowtie2 -1 1.fastq -2 2.fastq -p 8 -x mm | samtools sort -O bam -@ 10 -o - > contig.bam

        jgi_summarize_bam_contig_depths --outputDepth input_file/contig.depth.txt contig.bam

        awk '{print $1"\t"$3}' input_file/contig.depth.txt > depth.txt

        checkm tetra -t 10 input_file/stag1_merge.fa  TDP.txt




	python python_code/k_means.py "$i" > stag2_group.txt 
	
	python python_code/bins.py
	find $4/*.fa -size -10000c -exec rm {} \;
	checkm lineage_wf -t 15 -x fa bins/ --nt --tab_table -f kmeans_result/0.02_"$i"_bins_qa.txt checkout/ 
	rm -rf checkout

done




	#sed  "s/_/ /g" stag2_group.txt | awk '{print $1"\t"$3}' > name_module.txt

	#python /dellfsqd2/ST_OCEAN/USER/xuqi/final/run/jaccard_infomap/module_pre_count.py name_module.txt> tmp.txt

	#sort -k1n tmp.txt > module_pre_count.txt
	#python /dellfsqd2/ST_OCEAN/USER/xuqi/final/run/pic/method_plt.py  module_pre_count.txt 81 module.png
