import sys
from collections import Counter
import time
from thread_1 import *
from thread_2 import *
from thread_3 import *
from thread_4 import *
from thread_5 import *
from thread_6 import *
from multiprocessing import *

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
        val_list = int(split_line[2])
        add_two_dim_dict(tmp_dict, key_a, key_b, val_list)

        line = infile.readline()

    return tmp_dict

def open_input(filename):
    infile = open(filename, 'r')

    return infile

            


def cal_all_correlation(contig_list, contig_dict_keys,thresh1, thresh2, weight_index):
    corr_map = []
			
    for contig1 in contig_list:  #contig是所有的，都要遍历一遍
        if(contig1[0] in contig_dict_keys):
            contig1_index = contig_list.index(contig1)    
            for contig2 in contig_list:
                if(contig1_index<contig_list.index(contig2)):
                    if(contig2[0] in candidate_contig_dict[contig1[0]]):
                            tmp_corr = cal_a_correlation(contig1, contig2, weight_index)
                       
                            corr_map.append([contig1[0], contig2[0], tmp_corr])
                            
        
    return corr_map
    
    
    
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
        try:
            corr = cal_jaccard(dic_1[contig1[0]], dic_1[contig2[0]], weight_index)
        except:
            pass
    elif ht_index1 ==1 and ht_index2==0:
        try:
            corr = cal_jaccard(dic_1[contig1[0]], dic_2[contig2[0]], weight_index)
        except:
            pass    
    elif ht_index1 == 0 and ht_index2 ==1:
        try:
            corr = cal_jaccard(dic_2[contig1[0]], dic_1[contig2[0]], weight_index)
        except:
            pass
    elif ht_index1 == 0 and ht_index2 == 0:
        try:
            corr = cal_jaccard(dic_2[contig1[0]], dic_2[contig2[0]], weight_index)
        except:
            pass    
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
    outfile = open(filename,"a")
    for i in corr_map_list:
        contig1 = i[0]
        contig2 = i[1]
        correlation = round(i[2],3)
        correlation = str(correlation)
        outfile.write(contig1+"\t"+contig2+"\t"+correlation+"\n")
    
    outfile.close()


file="input_file/contig_length.txt"
len_thresh=5000
contig_list =get_seed_contig_info(file,len_thresh )

tmp_contig_list = []

for i in range(0,len(contig_list)):

    tmp_contig_list.append(contig_list[i])
    
m = Manager()    

corr_map_6=m.list()
corr_map_5=m.list()
corr_map_4=m.list()
corr_map_3=m.list()
corr_map_2=m.list()
corr_map_1=m.list()

dic_1_file = "input_file/dic_1.txt"
dic_1 = load_dict(dic_1_file)
thresh1 = 2
thresh2 = 2
weight_index = 1
dic_2_file = "input_file/dic_2.txt"
dic_2 = load_dict(dic_2_file)
conda_file = "input_file/candidate_contig_dict.txt"
candidate_contig_dict = load_dict(conda_file)
contig_keys=[]
contig_keys_file=open("input_file/contig_keys.txt")
for i in contig_keys_file.readlines():
    contig_keys.append(i.rstrip("\n"))
    

t1 = Process(target=cal_all_correlation_1, args=(dic_1,dic_2,contig_list,contig_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_1))
t1.start()
t2 = Process(target=cal_all_correlation_2, args=(dic_1,dic_2,contig_list,contig_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_2))
t2.start()
t3 = Process(target=cal_all_correlation_3, args=(dic_1,dic_2,contig_list,contig_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_3))
t3.start()
t4 = Process(target=cal_all_correlation_4, args=(dic_1,dic_2,contig_list,contig_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_4))
t4.start()
t5 = Process(target=cal_all_correlation_5, args=(dic_1,dic_2,contig_list,contig_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_5))
t5.start()
t6 = Process(target=cal_all_correlation_6, args=(dic_1,dic_2,contig_list,contig_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_6))
t6.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()


output_corr_map(corr_map_1,"input_file/jaccard.txt")
output_corr_map(corr_map_2,"input_file/jaccard.txt")
output_corr_map(corr_map_3,"input_file/jaccard.txt")
output_corr_map(corr_map_4,"input_file/jaccard.txt")
output_corr_map(corr_map_5,"input_file/jaccard.txt")
output_corr_map(corr_map_6,"input_file/jaccard.txt")


