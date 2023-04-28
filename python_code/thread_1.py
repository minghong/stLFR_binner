from collections import Counter


def cal_all_correlation_1(dic_1,dic_2,contig_list, contig_dict_keys,thresh1, thresh2, weight_index,candidate_contig_dict,corr_map_1):
		
    for contig1 in contig_list:  #contig是所有的，都要遍历一遍
        if(contig_list.index(contig1) % 6==0):
            if(contig1[0] in contig_dict_keys):
                contig1_index = contig_list.index(contig1)    
                for contig2 in contig_list[contig1_index+1:]:
                    try:

                            if(candidate_contig_dict[contig1[0]][contig2[0]]):
                                    tmp_corr = cal_a_correlation_1(contig1, contig2, weight_index,dic_1,dic_2)
                               
                                    corr_map_1.append([contig1[0], contig2[0], tmp_corr])
                            
                    except Exception as e:
                            pass              
    
def cal_a_correlation_1(contig1, contig2, weight_index,dic_1,dic_2):

    tmp_corr =[]
    head_to_head = cal_corr_ht_1(contig1, contig2, 1, 1, weight_index,dic_1,dic_2)
    tmp_corr.append(head_to_head)
    head_to_tail = cal_corr_ht_1(contig1, contig2, 1, 0,  weight_index,dic_1,dic_2)
    tmp_corr.append(head_to_tail)
    tail_to_head = cal_corr_ht_1(contig1, contig2, 0,1,  weight_index,dic_1,dic_2)
    tmp_corr.append(tail_to_head)
    tail_to_tail = cal_corr_ht_1(contig1, contig2, 0, 0 , weight_index,dic_1,dic_2)
    tmp_corr.append(tail_to_tail)

    max_corr = max(tmp_corr)
    return max_corr
  
def cal_corr_ht_1(contig1, contig2, ht_index1, ht_index2, weight_index,dic_1,dic_2):
    """
    contig1 and contig2 are lists including contig's name and length for using ContigBin Class
    """
    corr = 0 
    if ht_index1==1 and ht_index2==1:
        try:
            corr = cal_jaccard_1(dic_1[contig1[0]], dic_1[contig2[0]], weight_index)
        except:
            pass 
    elif ht_index1 ==1 and ht_index2==0:
        try:
            corr = cal_jaccard_1(dic_1[contig1[0]], dic_2[contig2[0]], weight_index)
        except:
            pass    
    elif ht_index1 == 0 and ht_index2 ==1:
        try:
            corr = cal_jaccard_1(dic_2[contig1[0]], dic_1[contig2[0]], weight_index)
        except:
            pass
    elif ht_index1 == 0 and ht_index2 == 0:
        try:
            corr = cal_jaccard_1(dic_2[contig1[0]], dic_2[contig2[0]], weight_index)
        except:
            pass    
    else:
        print ("Errors in setting the ht_index.")
        exit(-1)

    return corr
             

def cal_jaccard_1(dict1, dict2, weight_index):    #计算jaccard系数

    intersect_num = cal_intersect_1(dict1, dict2)
    union_num = cal_union_1(dict1, dict2)
    if(union_num==0):
        jaccard = 0
    else:
        jaccard = (1.0 * intersect_num) / (1.0* union_num)

    return jaccard


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


    
def list_to_dict_1(t_list):
    t_dict = Counter(t_list)
    return t_dict