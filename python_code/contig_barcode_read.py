import sys
import time
def get_seed_contig_info(contig_info, len_thresh):#返回符合条件的barcode列表
    infile = open_input(contig_info)
    contig_list = []
    line = infile.readline()
    while line:
        split_line = line.split()
        if int(split_line[1]) > len_thresh:   #如果contig长度的大于预设值,则记录
            contig_list.append(split_line[0])

        line = infile.readline()

    return contig_list
def parse_allline(filename):
    infile = open_input(filename)
    line = infile.readline()
    all_maplist = []
    while line:
        if line[0] != "@":
            maplist = parse_oneline(line)
            if maplist != "" and maplist!=None:
                all_maplist.append(maplist)
        line = infile.readline()
    
    return all_maplist

def open_input(filename):    #输入
    infile = open(filename, 'r')
    return infile


def parse_oneline(line):
    """
    parse one alignment for get a list containing readname, barcode, contigname, read's position;
    the aligment with forward direction is considered in this process.
    """
    
    maplist = []
    split_line = line.split()
    if(split_line[2] in tmp_contig_list):
        flag_index = parse_flag(split_line[1])
        proper_flag_index = flag_index[0]
        proper_map_index = parse_map_qual(int(split_line[4]), split_line[5])
        forward_index = flag_index[1]
        if proper_flag_index == 1 and proper_map_index ==1 and forward_index ==1 :
            tmp_readname = split_line[0] 
            split_name = tmp_readname.split("#")
            barcode = split_name[1]
            readname = split_name[0]
            if barcode != "0_0_0":
                
                contig = split_line[2]
                maplist.append(contig)
                maplist.append(barcode)
                pos = get_pos_pe(split_line[3], split_line[7]) 
                maplist.append(pos)

            return maplist
    

def get_pos_pe(read1_pos, read2_pos):
    """
    get the left-most position of a pair-end reads from the alignment of the forward read.
    """
    pos_list = []
    read1_left = int(read1_pos)
    read1_right = int(read1_pos) + 100
    read2_left = int(read2_pos)
    read2_right = int(read2_pos) + 100

    pos_list.append(read1_left)
    pos_list.append(read1_right)
    pos_list.append(read2_left)
    pos_list.append(read2_right)

    pos = min(pos_list)
    return pos

def parse_map_qual(mapQ, cigar_str):
    proper_map_index = 1
    if mapQ < 20:
        proper_map_index = 0

    len_match = count_cigar("M", cigar_str)
    if len_match < 50:
        proper_map_index = 0

    return proper_map_index

def count_cigar(char1, cigar_str):
    tmp_cigar_str = cigar_str
    cigar_str_len = len(tmp_cigar_str)
    tot_num = 0
    while cigar_str_len >0 :
        head_cigar_info = get_head_cigar(tmp_cigar_str)
        if head_cigar_info[0] == char1:
            tot_num = tot_num + head_cigar_info[1]

        tmp_cigar_str = head_cigar_info[2]
        cigar_str_len = len(tmp_cigar_str)

    return  tot_num

def get_head_cigar(cigar_str):
    cigar_list = ["M","I","D","N","S","H","P", "=", "X"]
    cigar_str_len = len(cigar_str)
    tmp_cigar_c= ""
    tmp_num = 0
    new_cigar_str = ""
    for i in range(cigar_str_len):
        if cigar_str[i] in cigar_list:
            tmp_cigar_c = cigar_str[i]
            tmp_num = int(cigar_str[0:i])
            if i+1 < cigar_str_len:
                new_cigar_str = cigar_str[i+1:]
            else:
                new_cigar_str = ""
            break

    return (tmp_cigar_c, tmp_num, new_cigar_str)

def parse_flag(sam_flag):
    flag = str(bin(int(sam_flag)))
    flag_string = flag[2:]
    flag_list = list(flag_string)
    flag_list.reverse()

    if len(flag_list) < 12:
        begin = len(flag_list)
        end = 12
        for i in range(begin,end):
            flag_list.append(0)
    proper_index = 1 
    forward_index = 1
    return (proper_index, forward_index)

    if flag_list[1]=="0":
        proper_index = 0
    if flag_list[8]=="1":
        proper_index = 0
    if flag_list[9]=="1" or flag_list[10]=="1" or flag_list[11]=="1":
        proper_index = 0

    if flag_list[4]=="1":
        forward_index = 0
    
    return (proper_index, forward_index)


file="input_file/contig_length.txt"
len_thresh=5000
contig_list =get_seed_contig_info(file,len_thresh )

tmp_contig_list = []

for i in range(0,len(contig_list)):

    tmp_contig_list.append(contig_list[i])
    
out=open("input_file/"+sys.argv[1]+".out","w")
all_maplist = parse_allline(sys.argv[1])     #input是10x_bowtie.sam
for j in range(0,len(all_maplist)):
    for h in range(0,len(all_maplist[j])):
        out.write(str(all_maplist[j][h])+'\t')
    out.write('\n')
out.close()


print(1)