
OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)

sed  "s/_/ /2" $1 > tmp.fa
nohup checkm lineage_wf -t 1 -x fa ./ --tab_table -f checkm_2.txt checkout/  &
#bowtie2-build -f tmp.fa index

#bowtie2 -p $5 -x  index -1 $2 -2 $3 -S contig.sam 

minimap2 -d  minimap.min tmp.fa

minimap2 -ax sr  minimap.min  $2 $3 -t $5>contig.sam

mkdir $4

mkdir input_file



flag=$(cat contig.sam |wc -l)
time split -a 3 -l $(($flag/$5)) -d contig.sam example

echo "contig_barcode_read"
python "${DIR}"/python_code/contig_length.py tmp.fa > input_file/contig_length.txt
for i in example*
do
nohup  time python "${DIR}"/python_code/contig_barcode_read.py  "${i}" > tmp_"${i}".tmp &
done

a=-1
while [ $a -ne 0 ]
do
cat *.tmp > hhh
flag=$(cat hhh | wc -l)
b=$(find . -name "*.tmp" | wc -l )
a=$(($flag-$b))
done

cat input_file/*.out > input_file/contig_barcode_read.txt
cat input_file/contig_barcode_read.txt | awk NF > input_file/contig_barcode_read.txt_2



sort -V -k1 input_file/contig_barcode_read.txt_2 > input_file/sort_contig_barcode_read.txt
echo "contig_barcode_read_read.py"
time python "${DIR}"/python_code/contig_barcode_read_read.py input_file/sort_contig_barcode_read.txt input_file/contig_barcode_read_read.txt

rm input_file/sort_contig_barcode_read.txt


cat input_file/contig_barcode_read_read.txt | awk '{print $2"\t"$1"\t"$3}' >input_file/barcode_contig_read_read.txt

time python  "${DIR}"/python_code/tmp.py 


time python "${DIR}"/python_code/tmp_1.py 
rm example*
rm *.tmp
rm input_file/*.out


