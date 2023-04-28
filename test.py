import argparse
import os
def main(contig_name,paired1,paired2,output_name,threads):

    os.system('bash pre_data.sh '+contig_name+' '+paired1+' '+paired2+' '+output_name+' '+str(threads))
    
    os.system('bash run.sh '+contig_name+' '+paired1+' '+paired2+' '+output_name+' '+str(threads))




if __name__ == '__main__':


    parser=argparse.ArgumentParser(prog="testname", usage='''binner -i contig.fa -1 reads1.fastq -2 reads.fastq -o out_dir -t threads''',
    description='deal with fasta, get reads1、reads2', epilog='That\'s all')
    
    parser.add_argument('-i', '--input',nargs="+",type=str, metavar='',help='contig.fa',required=True)
    parser.add_argument('-1', '--paired1',nargs="+",type=str, metavar='',help='input reads1.fastq',required=True)
    parser.add_argument('-2', '--paired2',nargs="+",type=str, metavar='',help='input reads2.fastq',required=True)
    parser.add_argument('-o', '--out',nargs="+",type=str, metavar='',help='output dir',required=True)
    parser.add_argument('-t', '--threads',type=int, metavar='',help='threads number default:10',default=10)
    #parser.add_argument('-nn', '--Nnumber',type=int, metavar='',help='allow max contain N sizes default:0',default=0)
    args = parser.parse_args()


    main(args.input[0],args.paired1[0],args.paired2[0],args.out[0],args.threads)
