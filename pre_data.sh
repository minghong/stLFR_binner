
bowtie2-build -f $1  index
bowtie2 -p $5 -x  index -1 $2 -2 $3 -S contig.sam 
rm -rf $4
rm -rf input_file
mkdir $4
mkdir input_file
OUT=$(command -v test.py)
DIR=$(cd $(dirname $OUT); pwd)
echo "run contig_barcode_read"
python "${DIR}"/python_code/contig_barcode_read.py  contig.sam input_file/contig_barcode_read.txt 
sed -i '/^$/d' input_file/contig_barcode_read.txt 
echo "run contig_barcode_read_read"
sort -V -k1 input_file/contig_barcode_read.txt > input_file/sort_contig_barcode_read.txt

python "${DIR}"/python_code/contig_barcode_read_read.py input_file/sort_contig_barcode_read.txt input_file/contig_barcode_read_read.txt
rm input_file/sort_contig_barcode_read.txt
echo "run barcode_contig_read_read"
cat input_file/contig_barcode_read_read.txt | awk '{print $2"\t"$1"\t"$3}' >input_file/barcode_contig_read_read.txt


python "${DIR}"/python_code/contig_length.py $1 > input_file/contig_length.txt

python "${DIR}"/python_code/tmp_2.py  input_file/contig_length.txt input_file/contig_barcode_read_read.txt input_file/barcode_contig_read_read.txt  input_file/5000_2000_jaccard.txt



