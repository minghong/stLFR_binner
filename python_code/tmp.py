import sys
from collections import Counter
import time

def add_two_dim_dict(out_dict, key_a, key_b, val ):
    if key_a in out_dict:
        out_dict[key_a].update({key_b: val})
    else:
        out_dict.update({key_a:{key_b:val}})

def load_dict(filename):
    tmp_dict = {}
    infile = open_input(filename)
    line = infile.readline()
    while line:
        split_line = line.split()
        key_a = split_line[0]
        key_b = split_line[1]
        val_list = split_line[2].split(":")
        add_two_dim_dict(tmp_dict, key_a, key_b, val_list)

        line = infile.readline()

    return tmp_dict

def open_input(filename):
    infile = open(filename, 'r')

    return infile
def barcode(contig_list, contig_dict, barcode_dict, thresh1, thresh2, weight_index):
    for contig1 in contig_list:  #contig是所有的，都要遍历一遍
        if(contig1[0] in contig_dict.keys()):
            contig1_bin = ContigBin(contig1[0], contig1[1])  #计算1的bin
            contig1_name =contig1[0] #
            binsize = contig1_bin.binsize #1的binsize
            start1 = contig1_bin.get_head()#开始位置
            contig1_barcode_dict = get_bin_barcodeset(contig1_name,binsize, start1, contig_dict )
            
            dic_1[contig1[0]]=contig1_barcode_dict
            start1 = contig1_bin.get_tail()
            contig1_barcode_dict = get_bin_barcodeset(contig1_name,binsize, start1, contig_dict )
                
            dic_2[contig1[0]]=(contig1_barcode_dict)
            
            
def candidate (contig_list, contig_dict, barcode_dict, thresh1, thresh2, weight_index):
    for contig1 in contig_list:  #contig是所有的，都要遍历一遍
        if(contig1[0] in contig_dict.keys()):
            candidate_contig_dict[contig1[0]]=get_candidate_contig(contig1[0], contig_dict, barcode_dict, thresh1, thresh2)



def cal_all_correlation(contig_list, contig_dict_keys,thresh1, thresh2, weight_index):
    corr_map = []
			
    for contig1 in contig_list:  #contig是所有的，都要遍历一遍
        if(contig1[0] in contig_dict_keys):
       	    print(contig1[1])
            contig1_index = contig_list.index(contig1)    
            
            for contig2 in contig_list[contig1_index+1:]:
                
                if(contig2[0] in candidate_contig_dict[contig1[0]]):
                        tmp_corr = cal_a_correlation(contig1, contig2, weight_index)
                   
                        corr_map.append([contig1[0], contig2[0], tmp_corr])
        
    return corr_map
    
def get_candidate_contig(contig_name, contig_dict, barcode_dict, thresh1, thresh2):
    effect_barcode_list = get_effect_barcode(contig_name, contig_dict, thresh1)
    candidate_contig_dict = get_effect_contig(effect_barcode_list, barcode_dict, thresh1, thresh2)
    return candidate_contig_dict
    
    
def get_effect_barcode(contig_name, contig_dict, thresh1):#得到有barcode

        effect_barcode_list =[]
        for barcode in contig_dict[contig_name].keys():
            if len(contig_dict[contig_name][barcode]) >= thresh1:  #contig的barcode的条数大于阈值，则认为是合法的
                #print(contig_name,barcode,contig_dict[contig_name][barcode])
                effect_barcode_list.append(barcode)
                #存的是scaffold对应的barcode
        return effect_barcode_list
def get_effect_contig(effect_barcode_list, barcode_dict, thresh1, thresh2):


#得到的barcode大于thresh1，得到的contig大于thresh2
    effect_contig_dict = {}
    effect_contig_list = []
    for barcode in effect_barcode_list:
        try:
            for contig in barcode_dict[barcode].keys():
                if len(barcode_dict[barcode][contig]) >= thresh1:#表达的意思相同？
                    #print(contig,barcode,barcode_dict[barcode][contig])
                    effect_contig_list.append(contig)

        except KeyError:
            print ("there exist errors in barcode name.")
            sys.exit(-1)

    tmp_contig_dict = list_to_dict(effect_contig_list)  #得到scffold的总条数
    #print(tmp_contig_dict)
    for contig in tmp_contig_dict.keys():
        if tmp_contig_dict[contig] >= thresh2:
            effect_contig_dict[contig] = tmp_contig_dict[contig]
    #print(effect_contig_dict)

    return effect_contig_dict
        

    
    
def cal_a_correlation(contig1, contig2, weight_index):

    tmp_corr =[]
    head_to_head = cal_corr_ht(contig1, contig2, 1, 1, weight_index)
    tmp_corr.append(head_to_head)
    head_to_tail = cal_corr_ht(contig1, contig2, 1, 0, weight_index)
    tmp_corr.append(head_to_tail)
    tail_to_head = cal_corr_ht(contig1, contig2, 0,1, weight_index)
    tmp_corr.append(tail_to_head)
    tail_to_tail = cal_corr_ht(contig1, contig2, 0, 0 , weight_index)
    tmp_corr.append(tail_to_tail)

    max_corr = max(tmp_corr)
    return max_corr
  
def cal_corr_ht(contig1, contig2, ht_index1, ht_index2, weight_index):
    """
    contig1 and contig2 are lists including contig's name and length for using ContigBin Class
    """
    corr = 0 
    if ht_index1==1 and ht_index2==1:
	
        corr = cal_jaccard(dic_1[contig1[0]], dic_1[contig2[0]], weight_index)
		
    elif ht_index1 ==1 and ht_index2==0:
	
        corr = cal_jaccard(dic_1[contig1[0]], dic_2[contig2[0]], weight_index)
        
    elif ht_index1 == 0 and ht_index2 ==1:
	
        corr = cal_jaccard(dic_2[contig1[0]], dic_1[contig2[0]], weight_index)

    elif ht_index1 == 0 and ht_index2 == 0:

        corr = cal_jaccard(dic_2[contig1[0]], dic_2[contig2[0]], weight_index)
        
    else:
        print ("Errors in setting the ht_index.")
        exit(-1)

    return corr
    
    
def get_bin_barcodeset(contig, binsize, start, contig_dict):

    bin_barcode_dict = {}
    end = start + binsize -1

    for barcode in contig_dict[contig].keys():
        verify_index, effective_num = get_barcode_by_pos(start, end, contig_dict[contig][barcode])
        if verify_index == 1:
            bin_barcode_dict[barcode] = effective_num
    return bin_barcode_dict
    
    

def open_output(filename):  #输出
    outfile = open(filename, 'w')
    return outfile


def list_to_dict(t_list):
    t_dict = Counter(t_list)
    return t_dict


def whether_exist(t_key, t_dict):#判断是不是在里面存在，
    if t_key in t_dict:
        return True
    else:
        return False



class ContigBin:
    
    def __init__(self, contig, contig_len):
        self.conitg = contig
        self.contig_len = contig_len
        self.binsize = 2000
        self.offset = 10
        self.bins = []
        self.tot_bin_num = 0
        self.bin_gap = 100
        self.center = int(contig_len/2)
        
        left_bin_count, left_bin_start_list = self._chop_forward()
        right_bin_count, right_bin_start_list = self._chop_reverse()

        self.tot_bin_num = left_bin_count + right_bin_count
        self.bins = left_bin_start_list + right_bin_start_list

    
    def _chop_forward(self):
        bin_start_list = []
        bin_dist = self.binsize + self.bin_gap
        bin_start = self.offset
        tmp_dist = self.center - bin_start
        bin_count = 0

        while bin_start < self.center and tmp_dist > self.binsize/2 :
            bin_count = bin_count+1
            bin_start_list.append(bin_start)

            bin_start = self.offset + bin_count * bin_dist
        return bin_count, bin_start_list
        

    def _chop_reverse(self):
        bin_start_list = []
        bin_dist = self.binsize + self.bin_gap
        bin_start = self.contig_len - self.offset - self.binsize
        bin_count =0

        while bin_start >self.center :
            bin_count = bin_count +1 
            bin_start_list.append(bin_start)

            bin_start = self.contig_len - self.offset - (bin_count+1)*bin_dist
        
        bin_start_list.sort()
        return bin_count, bin_start_list 
       

    def get_head(self):
        head = 0
        head_order = 0
        if self.tot_bin_num ==0:
            print ("there exist contig shorter than binsize")
            exit(-1) 
        else:
            head = self.bins[head_order]

        return head

    
    def get_tail(self):
        tail = 0
        tail_order = self.tot_bin_num - 1
        if self.tot_bin_num ==0:
            print ("there exist contig shorter than binsize")
            exit(-1)
        else:
            tail = self.bins[tail_order]

        return tail
                

def cal_jaccard(dict1, dict2, weight_index):    #计算jaccard系数
    if weight_index == 1:
        intersect_num = cal_intersect_1(dict1, dict2)
        union_num = cal_union_1(dict1, dict2)
        if(union_num==0):
            jaccard = 0
        else:
            jaccard = (1.0 * intersect_num) / (1.0* union_num)
    else:
        intersect_num = cal_intersect_0(dict1, dict2)
        union_num = cal_union_0(dict1, dict2)
        if(union_num==0):
            jaccard = 0

    return jaccard


def get_barcode_by_pos(start, end, barcode_pos_list):
    verify_index = 0
    effective_num =0
    for pos in barcode_pos_list :
        if int(pos) >= start and int(pos) <= end :   #如果起始位置大于开始小于结束，就加一
            effective_num = effective_num +1
    
    if effective_num >=2:#如果有效个数大于等于2，则认为是有效的
        verify_index = 1

    return verify_index, effective_num

def cal_intersect_1(dict1, dict2):
    list1 = dict1.keys()
    list2 = dict2.keys()

    intersect_num = 0
    intersect = list(set(list1).intersection(set(list2)))

    for barcode in intersect:
        intersect_num = intersect_num + min(dict1[barcode], dict2[barcode])

    return intersect_num


def cal_union_1(dict1, dict2):
    list1 = dict1.keys()
    list2 = dict2.keys()

    union_num = 0
    t_union = list(set(list1).union(set(list2)))

    for barcode in t_union:
        if barcode in list1 and barcode in list2:
            union_num = union_num + max(dict1[barcode], dict2[barcode])
        elif barcode in list1 and barcode not in list2:
            union_num = union_num + dict1[barcode]
        else:
            union_num = union_num + dict2[barcode]

    return union_num

def get_seed_contig_info(contig_info, len_thresh):#返回符合条件的barcode列表
    infile = open_input(contig_info)
    contig_list = []
    line = infile.readline()
    while line:
        split_line = line.split()
        if int(split_line[1]) > len_thresh:   #如果contig长度的大于预设值,则记录
            contig_list.append([split_line[0],int(split_line[1])])

        line = infile.readline()

    return contig_list


def output_corr_map(corr_map_list, filename):
    outfile = open(filename,"w")
    for k,v in corr_map_list.items():
        for a,b in v.items():
            outfile.write(str(k)+"\t"+str(a)+"\t"+str(b)+"\n")
    
    outfile.close()
file="input_file/contig_length.txt"
len_thresh=5000
contig_list =get_seed_contig_info(file,len_thresh )

tmp_contig_list = []

for i in range(0,len(contig_list)):

    tmp_contig_list.append(contig_list[i])
        
dic_1={} 
dic_2={}
               
contig_dict_file = "input_file/contig_barcode_read_read.txt"
contig_dict = load_dict(contig_dict_file)

barcode_dict_file = "input_file/barcode_contig_read_read.txt"
barcode_dict = load_dict(barcode_dict_file)

thresh1 = 2
thresh2 = 2
weight_index = 1
corr_map_file_1="input_file/dic_1.txt"
corr_map_file_2="input_file/dic_2.txt"
corr_map_file_3="input_file/candidate_contig_dict.txt"

barcode(tmp_contig_list, contig_dict, barcode_dict, thresh1, thresh2, weight_index)
contig_dict_keys=contig_dict.keys()

candidate_contig_dict={}
candidate(tmp_contig_list, contig_dict, barcode_dict, thresh1, thresh2, weight_index)


output_corr_map(dic_1, corr_map_file_1)
output_corr_map(dic_2, corr_map_file_2)
output_corr_map(candidate_contig_dict, corr_map_file_3)

out=open("input_file/contig_keys.txt","w")
for i in contig_dict.keys():
    out.write(i+"\n")
out.close()

