OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)

#:<<EOF
sed  "s/_/ /" $1 >tmp.fa
bowtie2-build -f tmp.fa index

bowtie2 -p $5 -x  index -1 $2 -2 $3 -S contig.sam 

rm -rf $4

rm -rf input_file

mkdir $4

mkdir input_file

OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)

python "${DIR}"/python_code/contig_length.py tmp.fa > input_file/contig_length.txt
echo "contig_barcode_read"
time python "${DIR}"/python_code/contig_barcode_read.py    

sed -i '/^$/d' input_file/contig_barcode_read.txt 


sort -V -k1 input_file/contig_barcode_read.txt > input_file/sort_contig_barcode_read.txt
echo "contig_barcode_read_read.py"
time python "${DIR}"/python_code/contig_barcode_read_read.py input_file/sort_contig_barcode_read.txt input_file/contig_barcode_read_read.txt

rm input_file/sort_contig_barcode_read.txt


cat input_file/contig_barcode_read_read.txt | awk '{print $2"\t"$1"\t"$3}' >input_file/barcode_contig_read_read.txt


time python  "${DIR}"/python_code/tmp.py 

#EOF

time python "${DIR}"/python_code/tmp_1.py 



