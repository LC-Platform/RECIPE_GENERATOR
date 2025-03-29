import os
import sys
import re
import subprocess
import repository.constant
import tempfile
from mapping_paradigm import *
# from googletrans import Translator
# from indic_transliteration import sanscript
from repository.coref_discourse import *
from repository.verb import Verb
from repository.concept import Concept
from wxconv import WXC
import json
import tempfile
# from googletrans import Translator
# from generate_input_modularize_new import additional_words_dict,spkview_dict
# from Table import store_data
from repository.verb import Verb
from repository.concept import Concept
from some_convertions_files.json_to_txt import process_and_write_json
additional_words_dict = {}
processed_postpositions_dict = {}
construction_dict = {}
spkview_dict = {}
MORPHO_SEMANTIC_DICT = {}
data_case_for_k4=[]
construction_dict_to_leave={}
# Global dictionary to store words prefixed with '*' along with their category
global_starred_words = {}
#pre processing

def read_file(file_path):
    """
    Read and return the content of a file.
    """
    with open(file_path, 'r') as file:
        return file.read()

# def read_file(file_path):
#     """
#     Functionality: To read the file from mentioned file_path.
#     Exception: If file_path is incorrect raise an exception - "No such File found." and exit the program.
#     Parameters:
#         file_path - path of file to be read.
#     Returns:
#         Returns array of lines for data given in file.
#     """
#     log(f'File ~ {file_path}')
#     try:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             if len(lines) > 10 and lines[10].strip() == '':
#                 lines = lines[:10]
#         log('File data read.')
#     except FileNotFoundError:
#         log('No such File found.', 'ERROR')
#         sys.exit()
#     return lines

def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'log : [{logtype}]:{mssg}')
    if logtype == 'ERROR':
        path = sys.argv[1]
        write_hindi_test(' ', 'Error', mssg, 'test.csv', path)


def write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path):
    """Append the hindi text into the file"""
    OUTPUT_FILE = 'TestResults.csv'# temporary for presenting
    str = path.strip('lion_story/')
    if str == '1':
        with open(OUTPUT_FILE, 'w') as file:
            file.write("")

    with open(OUTPUT_FILE, 'a') as file:
        file.write(path.strip('../hindi_gen/lion_story') + '\t')
        file.write(src_sentence.strip('"').strip('\n').strip('#') + '\t')
        file.write(POST_PROCESS_OUTPUT + '\t')
        file.write(hindi_output + '\t')
        file.write('\n')
        # log('Output data write successfully')
    return "Output data write successfully"


# def masked_postposition(processed_words, words_info, processed_verbs):
#     '''Calculates masked postposition to words wherever applicable according to rules.'''
#     masked_PPdata = {}

#     for data in processed_words:
#         if data[2] not in ('p', 'n', 'other'):
#             continue
#         data_info = getDataByIndex(data[0], words_info)
#         try:
#             data_case = False if data_info == False else data_info[4].split(':')[1].strip()
#         except IndexError:
#             data_case = False
#         ppost = ''
#         ppost_value = '<>'
#         # if data_case in ('k1', 'pk1'):
#         #     if findValue('yA', processed_verbs, index=6)[0]:  # has TAM "yA"
#         #         if findValue('k2', words_info, index=4)[0]: # or findExactMatch('k2p', words_info, index=4)[0]:
#         #             ppost = ppost_value
#         # if data_case in ('r6', 'k3', 'k5', 'k5prk', 'k4', 'k4a', 'k7t', 'jk1','k7', 'k7p','k2g', 'k2','rsk', 'ru' ):
#         #     ppost = ppost_value
#         if data_case in ('k7','k7t','k7p','k2p'):
#             ppost = ppost_value
#         elif data_case == 'krvn' and data_info[2] == 'abs':  #abstract noun as adverb
#             ppost = ppost_value
#         elif data_case in ('k2g', 'k2') and data_info[2] in ("anim", "per"):
#             ppost = ppost_value #'ko'
#         elif data_case in ('rsm', 'rsma','k7a'):
#             ppost = ppost_value+ ' ' + ppost_value #ke pAsa
#         elif data_case == 'rt':
#             # ppost = ppost_value+ ' ' + ppost_value #'ke lie'
#             ppost = ppost_value
#         elif 'rask' in data_case:
#             # ppost = ppost_value+ ' ' + ppost_value #ke sath
#             ppost = ppost_value
#         elif data_case == 'rv':
#             ppost = ppost_value+ ' ' + ppost_value + ' ' + ppost_value#'kI tulanA meM'
#         elif data_case == 'r6':
#             ppost = ppost_value # 'kI' if data[4] == 'f' else 'kA'
#             nn_data = nextNounData(data[0], words_info)
#             if nn_data != False:
#                 if nn_data[4].split(':')[1] in ('k3', 'k4', 'k5', 'k7', 'k7p', 'k7t', 'mk1', 'jk1', 'rt'):
#                     ppost = ppost_value
#                 elif nn_data[3][1] != 'f' and nn_data[3][3] == 'p':
#                     ppost = ppost_value#'ke'
#                 else:
#                     pass
#         else:
#             pass
#         if data[2] == 'p':
#             temp = list(data)
#             temp[7] = ppost if ppost != '' else 0
#             data = tuple(temp)
#         if data[2] == 'n' or data[2] == 'other':
#             temp = list(data)
#             temp[8] = ppost if ppost != '' else None
#             data = tuple(temp)
#             masked_PPdata[data[0]] = ppost
#     # ##print(masked_PPdata,'mppp')
#     return masked_PPdata
def clean(word, inplace=''):
    """
    Clean concept words by removing numbers and special characters from it using regex.
    >>> clean("kara_1-yA_1")
    'karayA'
    >>> clean("kara_1")
    'kara'
    >>> clean("padZa_1")
    'pada'
    >>> clean("caDZa_1")
    'caDa'
    """
    # Replace specific patterns
    word = word.replace('dZ', 'd').replace('jZ', 'j').replace('DZ', 'D')
    # Remove numbers and special characters
    return re.sub(r'[^a-zA-Z]+', inplace, word)

def process_sentence(filtered_data, sentences):
    # Check if filtered_data is not empty
    if filtered_data:
        for segment_id, text_list in filtered_data.items():
            for text in text_list:
                sentences.append({
                    "segment_id": segment_id,
                    "text": text
                })
        # Prepare output in the required format
        output = {
            "bulk": sentences
        }
    else:
        output = {
            "sentence_id": list(filtered_data.keys()),
            "text": list(filtered_data.values())
        }
    
    # Convert the dictionary to a JSON string
    json_output = json.dumps(output, ensure_ascii=False)
    
    # Process and write the JSON output to a file
    process_and_write_json(json_output, output_file="./formatted_output.txt")
    
    return json_output

def check_main_verb(depend_data):
    for dep in depend_data:
        if dep:  # Check if dep is not empty
            dep_type = dep.strip().split(':')[1]  # Extract the type after splitting
            if dep_type in ('main', 'rcelab', 'rcdelim'):  # Check for main verb types
                return True  # Return immediately if a main verb is found

    # Log the error if no main verb was identified
    log('USR error. Main verb not identified. Check the USR.')
    
    return False

def generate_rulesinfo(file_data):
    '''
    Functionality: Extract all rows of USR, remove spaces from Running and end and break the entire row on the basis of comma and convert into list of strings.
    Exception: If length of file_data array is less than 10 raise an exception - Invalid USR. USR does not contain 10 lines.' and exit the program.
    Parameters:
        file_data - This is an array of lines read from input file.
    Returns:
        Return list of rows of USR as list of lists.
    '''

    if len(file_data) < 10:
        log('Invalid USR. USR does not contain 10 lines.', 'ERROR')
        sys.exit()

    src_sentence = file_data[0]
    root_words = file_data[1].strip().split(',')
    index_data = file_data[2].strip().split(',')
    seman_data = file_data[3].strip().split(',')
    gnp_data = file_data[4].strip().split(',')
    depend_data = file_data[5].strip().split(',')
    discourse_data = file_data[6].strip().split(',')
    spkview_data = file_data[7].strip().split(',')
    scope_data = file_data[8].strip().split(',')
    construction_data=file_data[9].strip().split(',')
    sentence_type = file_data[10].strip()
    # construction_data = ''
    # if len(file_data) > 10:
    #     construction_data = file_data[10].strip()

    log('Rules Info extracted succesfully fom USR.')
    # ##print('generate_rulesinfo : ',[src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
            # scope_data, sentence_type, construction_data])
    return [src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
            scope_data, construction_data,sentence_type]

def populate_spkview_dict(spkview_info,discourse_data,index_data):
    populate_spk_dict = False
    a = 'after'
    b = 'before'
    for i, info in enumerate(spkview_info):
        clean_spk_info = info.rstrip('_1234567890')
        # print(discourse_data)
        if '/' in clean_spk_info :
            clean_spk_info = clean_spk_info.split('/')[1]
        if clean_spk_info in repository.constant.spkview_list_b or clean_spk_info in repository.constant.spkview_list_a or clean_spk_info == 'result':
            populate_spk_dict = True
            if clean_spk_info in repository.constant.spkview_list_a:
                if not discourse_data[i]:
                    temp = (a, clean_spk_info)
                    spkview_dict[index_data[i]] = [temp]
            else:
                temp = (b, clean_spk_info)
                spkview_dict[index_data[i]] = [temp]
    return populate_spk_dict

def preprocess_postposition_new(concept_type, np_data, words_info, verb_data, index_data):
    '''Calculates postposition to words wherever applicable according to rules.'''
    cp_verb_list = ['prayApreprsa+kara','sahAyawA+kara']
    
    if len(verb_data) > 0:
        verb_term = verb_data[1]
        if len(verb_term) > 0:
            root_main = verb_term.strip().split('-')[0].split('_')[0]
    if np_data != ():
        data_case = np_data[4].strip().split(':')[1]
        data_case_for_k4.append(np_data[4])
        data_head = np_data[4].strip().split(':')[0]
        data_index = np_data[0]
        ind_in_index_data = index_data.index(data_index)
        data_seman = np_data[2]
    ppost = ''
    new_case = 'o'
    # ##print(np_data,'nnnn')
    if data_case in ('k1', 'pk1'):
        if is_tam_ya(verb_data,data_head): # has TAM "yA" or "yA_hE" or "yA_WA" marA WA
            # print(data_head,verb_data,'headd')
            k2exists, k2_index = find_match_with_same_head(data_head, 'k2', words_info, index=4) # or if CP_present, then also ne - add #get exact k2, not k2x
            # vk2exists, vk2_index = find_match_with_same_head(data_head, 'vk2', words_info, index=4)
            if k2exists:
                ppost = 'ne'
            else:
                ppost = ''
                log('Karma k2 not found. Output may be incorrect')

        elif identify_complete_tam_for_verb(verb_term) in repository.constant.nA_list:
            ppost = 'ko'
        else:
            log('inside tam ya else')

    elif data_case=='mod' and data_seman=='season':
        ppost = 'kA'
        nn_data = nextNounData(data_head, words_info)
        # ##print(nn_data,'nndl')
        if nn_data != False:
            if nn_data[4].split(':')[1] in ('k3', 'k4', 'k5', 'k7', 'k7p', 'k7t', 'r6', 'mk1', 'jk1', 'rt'):
                ppost = 'ke'
                if nn_data[3] == 's':#agreement with gnp
                    if nn_data[3] == 'f':
                        ppost = 'kI'
                    else:
                        ppost = 'kA'
                else:
                    pass
    elif data_case == 'k2g':
        ppost = process_dep_k2g(data_case, verb_data)
    elif data_case == 'k2': #if CP present, and if concept is k2 for verb of CP, and the verb is not in specific list, then kA
        if data_seman and data_seman!=''and data_seman.split()[0] in ("anim", "per"):
            check_k4=data_head+':k4'
            # check_k7t=data_head+':k7t'
            if clean(root_main) in repository.constant.reciprocal_verbs:
                ppost = 'se'
            elif check_k4 not in data_case_for_k4:
                ppost = 'ko'
        else:
            new_case = 'd'

    # elif data_case in ('k2p','k7','k7p','k7t'):
    #     # ppost = '' 
    #     ppost = '<>'
    # elif data_case == 'rt':
    #     ppost = '<>' +  ' ' + '<>'
    elif data_case in ('k2p'):
        ppost = '' # modified from meM 22/06
    elif data_case in ('k3', 'k5', 'k5prk'):
        ppost = 'se'
    elif data_case in ('k4', 'k4a', 'jk1'):
        ppost = 'ko'
    elif data_case == 'k7t' and np_data[2]=='timex':
        ppost = 'para'
    elif data_case == 'k7t' and clean(np_data[1]) not in ['kala','subaha','Aja','aBI','pahale']:
        ppost = 'ko'
    elif data_case == 'k7':
        ppost = 'meM'
    elif data_case =='k7p':
        ppost = 'para'
    elif data_case =='k7a':
        ppost = 'ke anusAra'
    elif data_case == 'krvn' and data_seman == 'abs':
        ppost = 'se'
    elif data_case == 'rt':
        ppost = 'ke liye'
    elif data_case == 'rblak':
        ppost = 'ke bAxa'
    elif data_case == 'rblsk':
        ppost = 'we samaya'
    # elif data_case == 'rblsk':
    #     ppost = 'we samaya'
    elif data_case == 'rblpk':
        ppost = 'se pahale'
    elif data_case in ('rsm', 'rsma'):
        ppost = 'ke pAsa'
    elif data_case == 'rhh':
        ppost = 'ke'
    elif data_case == 'rsk':
        ppost = 'hue'
    elif data_case == 'rn':
        ppost = 'meM_se'
    elif data_case == 'rib':
        ppost = 'se'
    elif data_case == 'rasneg':
        ppost = 'ke binA'
    elif data_case == 'ru':
        ppost = 'jEsI'
    elif data_case == 'rkl':
        next_word = fetchNextWord(ind_in_index_data + 1,index_data, words_info)
        if next_word == 'bAxa':
            ppost = 'ke'
        elif next_word == 'pahale':
            ppost = 'se'

    elif data_case == 'rdl':
        next_word = fetchNextWord(ind_in_index_data + 1,index_data, words_info)
        if next_word in ('anxara', 'bAhara', 'Age', 'sAmane', 'pICe', 'Upara', 'nIce', 'xAyeM',
                         'bAyeM', 'cAroM ora', 'bIca', 'pAsa','uparI'):
            ppost = 'ke'
        elif next_word == 'xUra':
            ppost = 'se'

    elif data_case == 'rv':
        ppost = 'se'
    elif data_case == 'mk1':
        ppost = 'se'
    elif data_case == 'rh':
        ppost = 'ke_kAraNa'
    elif data_case == 'rd':
        ppost = 'kI ora'
    elif data_case == 'rp':
        ppost = 'se hokara'
    # elif 'rask7' in data_case:
    #     ppost = 'sahiwa'
    elif data_case in ('rask1','rask2','rask3','rask4','rask5','k1as','k2as','k3as','k4as','k5as','k7as'):
        ppost = 'ke sAWa'
    elif data_case == 'r6':
        ppost = 'kA' #if data[4] == 'f' else 'kA'
        
    elif data_case == 'quantless':
        ppost = 'se kama'
    elif data_case == 'quantmore':
        ppost = 'se aXika'
    else:
        pass
    if ppost == '':
        new_case = 'd'
    if concept_type == 'noun':
        if ppost == '':
            ppost = None
        processed_postpositions_dict[data_index] = ppost

    if concept_type == 'pronoun':
        if ppost == '':
            ppost = 0
        processed_postpositions_dict[data_index] = ppost
    return new_case, ppost

def generate_wordinfo(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
                      scope_data,construction_data):
    '''
    Functionality:
        1. To check USR format
        2. Combine each concept with its corresponding information at the same index in all rows in tuples. Group all these tuples as word_info list.

    Parameters:
        1. root_words - second row of USR. Contains all concepts/ root words
        2. index_data - third row of USR. Contains indexing of concepts from 1, 2, 3 and onwards
        3. seman_data - fourth row of USR. Contains semantic information about all concepts
        4. gnp_data - fifth row of USR. Contains number information of the concept
        5. depend_data - sixth row of USR. Contains dependency information of the concept
        6. discourse_data - seventh row of USR. Contains discourse information of the concept
        7. spkview_data - eighth row of USR. Contains speaker's view information of the concept
        8. scope_data - ninth row of USR. Contains scope information of the concept

    Returns:
        Generates an array of tuples containing word and its USR info i.e USR info word wise.
        '''
    return list(
        zip(index_data, root_words, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data,construction_data))
    # return check_USR_format(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data)

def check_USR_format(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
                      scope_data):
    '''
    Functionality:
    1. To check if root words and their indices are in order
    2. To ensure that all the tuples of the USR have same number of enteries

    Returns:
        Corrected USR as an array of tuples containing word and its USR info (corresponding value on same index in each row) i.e USR info word wise.
    '''
    data = [root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data]
    len_root = len(root_words)
    len_index = len(index_data)

    if len_root > len_index:
        diff = len_root - len_index
        while diff:
            index_data.append(0)
            diff = diff - 1
            log(f'{repository.constant.USR_row_info[1]} has lesser enteries as compared to {repository.constant.USR_row_info[0]}')

    elif len_root < len_index:
        diff = len_index - len_root
        while diff:
            index_data.pop()
            diff = diff - 1
            log(f'{repository.constant.USR_row_info[1]} has more enteries as compared to {repository.constant.USR_row_info[0]}')

    #once the lengths of root_words and index_data are equal check value of each index
    len_root = len(root_words)
    len_index = len(index_data)
    if len_root == len_index:
        for i in range(1, len_root + 1):
            if index_data[i - 1] == i:
                continue
            else:
                index_data[i - 1] = i
                log(f'{repository.constant.USR_row_info[1]} has wrong entry at position {i}')

    #Checking all tuples have same number of enteries
    max_col = max(index_data)
    i = 0
    for ele in data:
        length = len(ele)
        if length < max_col:
            diff = max_col - length
            while diff:
                ele.append('')
                log(f'Added one entry at the end of {repository.constant.USR_row_info[i]}')
                diff = diff - 1
        elif length > max_col:
            diff = length - max_col
            while diff:
                ele.pop()
                log(f'Removed one entry from the end of {repository.constant.USR_row_info[i]}')
                diff = diff - 1
        i = i + 1

    #Removing spaces if any,before/ after each ele for all rows in USR
    for row in data:
        for i in range(0, len(row)):
            if type(row[i]) != int and row[i] != '':
                temp = row[i].strip()
                row[i] = temp

    return list(
        zip(index_data, root_words, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data))

            

# def translate_to_hindi(text):
#     translator = Translator()
#     translated = translator.translate(text, src='en', dest='hi')
#     return translated.text

def convert_to_hindi(word):
    # wx = WXC(order='wx2utf', lang='hin')
    wx1 = WXC(order='utf2wx', lang='hin')
    hindi_text_list = wx1.convert(word)
    return hindi_text_list

def new_to_old_convert_construction_conj_dis(index_data, construction_data, conj_concept):
    result = {}

    for i, concept in enumerate(conj_concept):
        if 'conj' in concept or 'disjunct' in concept:  # Check if the concept contains 'conj'
            ind = index_data[i]
            op_indices = []

            for j, text in enumerate(construction_data):
                if text and 'op' in text:
                    txt_index = int(text.split(':')[0])
                    if txt_index == ind:
                        op_indices.append((index_data[j], text.split(':')[1]))  # Store as a tuple (index in construction_data, opX)

            if op_indices:
                result[ind] = op_indices

    return result

# def new_to_old_convert_construction_conj_dis(index_data,construction_data,conj_concept):
#     # op_index=[]
#     op_sub_ind=[]
#     construction_data1=''
#     print(index_data,construction_data,conj_concept,'ll')
#     for i, concept in enumerate(conj_concept):
        
#         if 'conj' in concept :
#             ind=index_data[i]
#             for j, text in enumerate(construction_data):
#                 # if text!='':
#                 txt=text.split(':')[0]
#                 if 'op' in text and ind==int(txt):
#                         op_sub_ind.append(str(index_data[j]))
                        
#             # op_index.append(str(op_sub_ind))

#             # for j,value in enumerate(op_index):
#             #     if j==0:
#             #         construction_data1='*conj:'+ value.replace(' ','')
#             #     else:
#             #         construction_data1=' conj:'+ value.replace(' ','')
#         elif 'disjunct' in concept :
#             ind=index_data[i]
#             for j, text in enumerate(construction_data):
#                 # if text!='':
#                 txt=text.split(':')[0]
#                 if 'op' in text and ind==int(txt):
#                         op_sub_ind.append(str(index_data[j]))
                        
#             # op_index.append(str(op_sub_ind))

#             # for j,value in enumerate(op_index):
#             #     if j==0:
#             #         construction_data1='*disjunct:'+ value.replace(' ','')
#             #     else:
#             #         construction_data1=' disjunct:'+ value.replace(' ','')
#     return op_sub_ind

def process_dep_k2g(data_case, main_verb):
    verb = identify_main_verb(main_verb[1])
    if verb in repository.constant.kisase_k2g_verbs:
        ppost = 'se'
    else:
        ppost = 'ko'
    return ppost

def get_all_form(morph_forms):
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>'
    """
    morph=morph_forms.split("$")[1]
    return morph

def get_first_form(morph_forms):
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>'
    """
    morph=morph_forms.split("/")[1]
    return morph

def get_default_GNP():
    gender,number,person,case = 'm','s','a','o'
    
    return gender, number, person, case

def get_gnpcase_from_concept(concept): #computes GNP values from noun or

    if concept[2] == 'v':
        gender = concept[3]
        number= concept[4]
        person = concept[5]
        case =  concept[7]

    elif concept[2] == 'vn':
        gender = concept[4]
        number= concept[5]
        person = concept[6]
        case =  concept[3]

    elif concept[2] in ('n', 'p'):
        gender = concept[4]
        number= concept[5]
        person = concept[6]
        case = concept[3]
    else:
        gender, number, person, case = get_default_GNP()
    return gender, number, person, case

# def get_TAM(term, tam):
#     """
#     >>> get_TAM('hE', 'pres')
#     'hE'
#     >>> get_TAM('hE', 'past')
#     'WA'
#     >>> get_TAM('asdf', 'gA')
#     'gA'
#     """
#     if term == 'hE' and tam in ('pres', 'past'):
#         alt_tam = {'pres': 'hE', 'past': 'WA'}
#         return alt_tam[tam]
#     else:
#         if term == 'jA':
#             tam = 'yA1'
#             return tam
#     return tam

# def get_main_verb(term):
#     ''' return main verb from a term'''

#     pass

def getDataByIndex(value: int, searchList: list, index=0):
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.
        Return False when index not found.'''
    try:
        res = False
        for dataele in searchList:
            # dataele=list(dataele)
            # if (dataele[(index)]) == value and dataele[7]=='vn':
            #     dataele[3]='d'
            #     res = tuple(dataele)
            if (dataele[(index)]) == value:
                # res = tuple(dataele)
                res = dataele
                break
        return res
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return False
    

# def getComplexPredicateGNP(term):
#     CP_term = clean(term.split('+')[0])
#     gender = 'm'
#     number = 's'
#     person = 'a'

#     tags = find_tags_from_dix(CP_term)  # getting tags from morph analyzer to assign gender and number for agreement
#     if '*' not in tags['form']:
#         gender = tags['gen']
#         number = tags['num']
#     return gender, number, person

def getGNP_using_k2(k2exists, searchList):
    casedata = getDataByIndex(k2exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb.', 'ERROR')
        sys.exit()
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
    return verb_gender, verb_number, verb_person[0]
        
def getGNP_using_k1(k1exists, searchList):
    # for k1 in k1exists:
    casedata = getDataByIndex(k1exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb k1 is missing.', 'ERROR')
        sys.exit()
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
    return verb_gender, verb_number, verb_person

def getVerbGNP_new(concept_term, full_tam,index, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns,index_data,k1_not_need):
    '''
    '''
    #for imperative sentences
    if sentence_type in ('Imperative','imperative') or 'o' in full_tam:
        verb_gender = 'm'
        verb_number = 's'
        verb_person = 'm'
        return verb_gender, verb_number, verb_person

    #for non-imperative sentences
    # For non-imperative sentences
    k1exists = False
    k2exists = False
    k1_case = ''
    k2_case = ''
    verb_gender, verb_number, verb_person, case = get_default_GNP()
    # if process_nominal_form:
    #     searchList = processed_nouns + processed_pronouns 
    # else:
    searchList = processed_nouns + processed_pronouns

    for dep in depend_data:
        # head_index=dep.split(':')[0]
        
        if dep == '':
            continue
        else:
            dep_val=dep.split(':')[1]
        # elif (case=='k1' or case=='pk1') and head_index==str(index):
        if (dep_val=='k1' or dep_val=='pk1'):
            k1exists_index = depend_data.index(dep)
            k1exists = index_data[k1exists_index]
            
        # elif dep[-2:]=='k2' and head_index==index:
        elif dep[-2:]=='k2':
            k2exists_index = depend_data.index(dep)
            k2exists = index_data[k2exists_index]

    if k1exists:
        casedata = getDataByIndex(k1exists, searchList)
        if (casedata == False):
            log('Something went wrong. Cannot determine case for k1.', 'ERROR')
        else:
            k1_case = casedata[3]
   
    if k2exists:
        casedata = getDataByIndex(k2exists, searchList)
        if (casedata == False):
            log('Something went wrong. Cannot determine case for k2.', 'ERROR')
        else:
            k2_case = casedata[3]
    
#     if is_cp:
#         cp_term = concept_term.split('+')[0]
#         if not k1exists and not k2exists:
#             verb_gender, verb_number, verb_person = getComplexPredicateGNP(cp_term)
#         elif k1exists and k1_case == 'd':
#             verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
#         elif k1exists and k1_case == 'o' and k2exists and k2_case == 'o':
#             verb_gender, verb_number, verb_person = getComplexPredicateGNP(cp_term)
#         return verb_gender, verb_number, verb_person[0]

    if 'yA' in full_tam:
        if k1exists and k1_case == 'd':
            verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'd':
            verb_gender, verb_number, verb_person = getGNP_using_k2(k2exists, searchList)
        return verb_gender, verb_number, verb_person[0]

    if full_tam in repository.constant.nA_list:
        return verb_gender, verb_number, verb_person[0]

    #tam - gA
    elif k1exists:
        verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        return verb_gender, verb_number, verb_person[0]
    else:
        return verb_gender, verb_number, verb_person[0]

def is_tam_ya(verbs_data,data_head):
    ya_tam = '-yA_'
    if len(verbs_data) > 0 and verbs_data != ():
        if verbs_data[0]==int(data_head):
            term = verbs_data[1]
            if ya_tam in term:
                return True
    return False

def is_kim(term):
    if term == 'kim':
        return True

    return False
def is_yax(term):
    if term == 'yax':
        return True

    return False

# def is_complex_predicate(concept):
#     return "+" in concept

# def is_CP(term):
#     """
#     >>> is_CP('varRA+ho_1-gA_1')
#     True
#     >>> is_CP("kara_1-wA_hE_1")
#     False
#     """
#     if "+" in term:
#         return True
#     else:
#         return False

def is_update_index_NC(i, processed_words):
    for data in processed_words:
        temp = tuple(data)
        if len(temp) > 7 and float(i) == temp[0] and temp[7] == 'NC':
            return True
    return False

def is_nonfinite_verb(concept):
    return concept.type == 'nonfinite'

def has_tam_ya():
    '''Check if USR has verb with TAM "yA".
        It sets the global variable HAS_TAM to true
    '''
    global HAS_TAM
    if HAS_TAM == True:
        return True
    else:
        return False

def has_GNP(gnp_info):
    if len(gnp_info) and ('sg', 'pl') in gnp_info:
        return True
    return False

def has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
    # interrogative_lst = ["yn_interrogative", "yn_interrogative_negative", "pass-yn_interrogative", "interrogative",
    #                      "Interrogative", "pass-interrogative"]
    if sentence_type in ("yn_interrogative", "yn_interrogative_negative", "pass-yn_interrogative", "interrogative",
                        "Interrogative", "pass-interrogative"):
        return POST_PROCESS_OUTPUT + ' ?'
    elif sentence_type in ('pass_affirmative','affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative',"fragment","term","title","heading"):
        return POST_PROCESS_OUTPUT + ' ।'
    else:
        return POST_PROCESS_OUTPUT

# def identify_case(verb, dependency_data, processed_nouns, processed_pronouns,index_data):
#     return getVerbGNP_new(verb.term, verb.tam, dependency_data, processed_nouns, processed_pronouns,index_data)

def identify_main_verb(concept_term):
    """
    >>> identify_main_verb("kara_1-wA_hE_1")
    'kara'
    >>> identify_main_verb("varRA+ho_1-gA_1")
    'ho'
    """
    if ("+" in concept_term):
        concept_term = concept_term.split("+")[1]
    con=clean(concept_term.split("-")[0])
    # ##print(con,'main verb')
    return con

def identify_default_tam_for_main_verb(concept_term):
    """
    >>> identify_default_tam_for_main_verb("kara_1-wA_hE_1")
    'wA'
    >>> identify_default_tam_for_main_verb("kara_1-0_rahA_hE_1")
    '0'
    """
    # con=concept_term.split("-")[1].split("_")[0]
    if '-' in concept_term:
        con=concept_term.split("-")[1]
        if '_' in con:
            con=con.split("_")[0]
            return con
        else:
            return con
    else:
        return concept_term
    return con

def identify_complete_tam_for_verb(concept_term):
    """
    >>> identify_complete_tam_for_verb("kara_1-wA_hE_1")
    'wA_hE'
    >>> identify_complete_tam_for_verb("kara_1-0_rahA_hE_1")
    'rahA_hE'
    >>> identify_complete_tam_for_verb("kara_1-nA_howA_hE_1")
    'nA_howA_hE'
    >>> identify_complete_tam_for_verb("kara_o")
    'o'
    """
    if 'cAha_1-e_1' in concept_term:
        return 'cAhiye'
    elif "-" not in concept_term:
        return concept_term.split("_")[1]
    tmp = concept_term.split("-")[1]
    tokens = tmp.split("_")
    non_digits = filter(lambda x: not x.isdigit(), tokens)
    tam_v="_".join(non_digits)

    return tam_v

def identify_auxiliary_verb_terms(term):
    """
    >>> identify_auxiliary_verb_terms("kara_1-wA_hE_1")
    ['hE']
    >>> identify_auxiliary_verb_terms("kara_1-0_rahA_hE_1")
    ['rahA', 'hE']
    """
    # ##print(term,'ee')
    aux_verb_terms = term.split("-")[1].split("_")[1:]
    # ##print(aux_verb_terms,'ee')
    cleaned_terms = map(clean, aux_verb_terms)
    # ##print(cleaned_terms,'clt')
    aux_list=list(filter(lambda x: x != '', cleaned_terms))
    # ##print(el)
    return aux_list            # Remove empty strings after cleaning

def identify_verb_type(verb_concept):
    '''
    >>identify_verb_type([])
    '''
    #dep_rel = verb_concept[4].strip().split(':')[1] #if using with non-OO program
    dependency = verb_concept.dependency
    dep_rel=''
    if dependency!='-':
        dep_rel = dependency.strip().split(':')[1]
    v_type = ''
    if dep_rel == 'main':
        v_type = "main"
    # elif dep_rel in ('rpk', 'rbk', 'rvks', 'rbks', 'rsk', 'rblpk','rblak','rblsk'):
    #     v_type = "nonfinite"
    elif dep_rel in ('rpk', 'rsk','rbk'):
        v_type = "nonfinite"
    # elif dep_rel in ('rvks'):
    #     v_type = "verbal adjective"
    # elif dep_rel in ('rblpk','rblak','rblsk'):
    #     v_type = "nominal_verb"
    else:
        v_type = "main"
    return v_type

def find_tags_from_dix(word):
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac repository/hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    # ##print(morph_forms,'dixxxxxxxx')
    p_m=parse_morph_tags(morph_forms)
    return p_m

def find_tags_from_dix_as_list(word):
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac repository/hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags_as_list(morph_forms)
    # ##print(p_m,'pmmmmmmmmm')
    return p_m

def find_exact_dep_info_exists(index, dep_rel, words_info):
    for word in words_info:
        dep = word[4]
        dep_head = word[4].strip().split(':')[0]
        dep_val = word[4].strip().split(':')[1]
        if dep_val == dep_rel and int(dep_head) == index:
            return True

    return False

def find_match_with_same_head(data_head, term, words_info, index):
    #  k2exists, k2_index = find_match_with_same_head(data_head, 'k2', words_info, index=4)
     for dataele in words_info:
        dataele_index = dataele[0]
        dep_head = dataele[index].strip().split(':')[0]
        dep_value = dataele[index].strip().split(':')[1]
        if str(data_head) == dep_head and term == dep_value:
            return True, dataele_index
     return False, -1

def parse_morph_tags(morph_form):
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = {match[0]: match[1] for match in matches}
    result["form"] = form
    return result

# def parse_morph_tags_as_list(morph_form):
#     """
#     >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
#     {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
#     """
#     ##print(morph_form,'form')
#     form = morph_form.split("<")[0]
#     ##print(form,'mmmm')
#     matches = re.findall("<(.*?):(.*?)>", morph_form)
#     result = [(match[0], match[1]) for match in matches]
#     result.append(('form',form))
#     ##print(result,'res')
#     return result

def parse_morph_tags_as_list(morph_form):
    """
    Extracts the word and its corresponding morphological tags from the given morph-form string.

    Example:
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    [{'form': 'mA', 'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p'}]
    """
    # Split the morph-form by '/' to get individual word segments
    word = morph_form.split('/')[0].replace('^','')
    segments = morph_form.split('/')
    
    result = []
    # Iterate over each segment
    for segment in segments:
        form = segment.split("<")[0]  # Extract the word (before the first '<')
        if word==form:
            matches = re.findall("<(.*?):(.*?)>", segment)  # Find all morphological tags
            tag_dict = {match[0]: match[1] for match in matches}  # Convert matches to a dictionary
            tag_dict['form'] = form  # Add the word under the 'form' key
            result.append(tag_dict)  # Add the dictionary to the result list
    # ##print(result,'result')
    return result

def if_morph_kqwpft(processed_words, gnp_data):
    # Check if 'kqwpft' is present in gnp_data
    if 'kqwpft' in gnp_data:
        # Find the index of 'kqwpft' in gnp_data
        index = gnp_data.index('kqwpft')
        
        # Ensure the index is valid for processed_words
        if index < len(processed_words):
            # Modify the corresponding element in processed_words
            word_entry = processed_words[index]
            modified_entry = (
                word_entry[0],  # Keep the first element (ID) unchanged
                word_entry[1],  # Keep the second element (word) unchanged
                'vj',           # Change the third element to 'vj'
                *word_entry[3:6],  # Keep the next two elements unchanged
                'adj_yA_huA',   # Change the 6th element
                *word_entry[7:]  # Keep the rest of the elements unchanged
            )
            processed_words[index] = modified_entry
    return processed_words


# def check_words_in_dict(words,processed_words):
#     """
#     Check if each word in the list is present in the file using shell commands.
#     If a word starts with '#', remove '#', check if the word is present in the file, 
#     then replace '#' with '*' if not found, or leave as is if found.
#     This ensures that only whole words are matched, and matching is case-sensitive.
#     """
#     global global_starred_words  # Declare the global variable
#     words = words.split(' ')
    
#     file_path = "repository/hi_expanded_LC"
#     processed_concepts = []
    
#     for word in words:
#         original_word = word
#         if word.startswith('#'):
#             word_to_check = word[1:]  # Remove '#' for checking
#         else:
#             word_to_check = word  # If there's no '#', use the word as is
        
#         # Use the -w flag to match whole words only and make sure it's case-sensitive
#         command = f"grep -qw '{word_to_check}' {file_path}"
        
#         # Run the grep command
#         result = subprocess.run(command, shell=True)
        
#         # If grep returns a non-zero exit status, the word is not found
#         if result.returncode != 0:
#             if original_word.startswith('#'):
#                 starred_word = f"*{word_to_check}"
#                 processed_concepts.append(starred_word)  # Add * in front if not found
#                 global_starred_words.append(starred_word)  # Store in the global list
#             else:
#                 processed_concepts.append(word_to_check)  # Leave the word as is if not found and doesn't have #
#         else:
#             processed_concepts.append(original_word)  # Keep the original word if found
#     #print(processed_concepts, 'Processed concepts')
#     # #print(global_starred_words, 'Global starred words')
#     return processed_concepts


import subprocess

# Global dictionary to store words prefixed with '*' along with their category
global_starred_words = {}

def check_is_digit(num):
    if num.isdigit():
        return True
    else:
        try:
            float_value = float(num)
            return True
        except ValueError:
            return False
    return False

def check_words_in_dict(words, processed_words):
    """
    Check if each word in the list is present in a .txt file.
    If a word starts with '#', remove '#', check if the word is present in the file, 
    then replace '#' with '*' if not found, or leave as is if found.
    Also, store the word along with its descriptive category in the global list.
    """
    global global_starred_words  # Declare the global variable
    words = words.split(' ')

    file_path = "repository/extracted_words.txt"
    processed_concepts = []

    # Create a dictionary for word categories from `processed_words`
    word_categories = {entry[1]: entry[2] for entry in processed_words if len(entry) > 2}

    # Load the .txt file into a set for fast lookups
    with open(file_path, 'r', encoding='utf-8') as file:
        file_words = set(file.read().splitlines())

    for word in words:
        original_word = word
        if word.startswith('#'):
            word_to_check = word[1:]  # Remove '#' for checking
        else:
            word_to_check = word  # If there's no '#', use the word as is

        # Check if the word is in the loaded set
        if word_to_check not in file_words:
            # Handle starred word case
            if original_word.startswith('#') and word_to_check not in repository.constant.construction_list:
                starred_word = f"*{word_to_check}"
                processed_concepts.append(starred_word)  # Add * in front if not found
                
                # Map the category to its descriptive form
                category = word_categories.get(word_to_check, "unknown")
                descriptive_category = repository.constant.category_mapping.get(category, "unknown")
                
                # Add to global dictionary
                global_starred_words[starred_word.replace('*', '')] = descriptive_category
            else:
                processed_concepts.append(word_to_check)  # Leave the word as is if not found or is excluded
        else:
            processed_concepts.append(original_word)  # Keep the original word if found

    #print(processed_concepts, 'Processed concepts')
    #print(global_starred_words, 'Global starred words with descriptive categories')
    return processed_concepts

def read_output_data(output_file):
    """Check the output file data for post processing"""

    with open(output_file, 'r') as file:
        data = file.read()
    return data

def analyse_output_data(output_data, morph_input):
    if isinstance(output_data, str):
        output_data = output_data.strip().split(" ")

    combine_data = []
    for i in range(len(output_data)):
        morph_input_list = list(morph_input[i])
        morph_input_list[1] = output_data[i]
        combine_data.append(tuple(morph_input_list))
    return combine_data

def handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition):
    dnouns = noun[1].split('+')
    # ##print(dnouns,'dns')
    for k in range(len(dnouns)):
        index = noun[0] + (k * 0.1)
        noun_type = 'NC'
        clean_dnouns = clean(dnouns[k])
        if k == len(dnouns) - 1:
            noun_type = 'NC_head'
            dict_index = index
            processed_nouns.append(
                (index, clean_dnouns, category, case, gender, number, person, noun_type, postposition))
        else:
            processed_nouns.append((index, clean_dnouns, category, case, gender, number, person, noun_type, ''))

    if noun[0] in processed_postpositions_dict:
        processed_postpositions_dict[dict_index] = processed_postpositions_dict.pop(noun[0])
    # if clean(noun[1]) in ('cp', 'conj', 'disjunct', 'span', 'widthmeas', 'depthmeas', 'distmeas', 'rate', 'timemeas', 'waw', 'calender', 'massmeas', 'heightmeas', 'spatial'):
    #     del processed_postpositions_dict[index]
    return processed_nouns

def handle_unprocessed_all(outputData, processed_nouns):
    """swapping gender info that does not exist in dictionary."""
    output_data = outputData.strip().split(" ")
    has_changes = False
    reprocess_list = []
    dataIndex = 0  # temporary [to know index value of generated word from sentence]
    for data in output_data:
        dataIndex = dataIndex + 1
        if data[0] == '#':
            for i in range(len(processed_nouns)):
                if round(processed_nouns[i][0]) == dataIndex:
                        if processed_nouns[i][7] != 'proper':
                            temp = list(processed_nouns[i])
                            temp[4] = change_gender(processed_nouns[i][4])
                            #temp[4] = 'f' if processed_nouns[i][4] == 'm' else 'm'
                            reprocess_list.append(['n', i, processed_nouns[i][0],temp[4], temp[7]])
                            processed_nouns[i] = tuple(temp)
                            has_changes = True
                            log(f'{temp[1]} reprocessed as noun with new gen:{temp[4]}.')
    return has_changes, reprocess_list, processed_nouns

# def handle_unprocessed(index_data,depend_data,output_data, processed_nouns):
#     """swapping gender info that does not exist in dictionary."""
#     # output_data = outputData.strip().split(" ")
#     has_changes = False
#     # dataIndex = 0  # temporary [to know index value of generated word from sentence]
#     for dataIndex,data in enumerate(output_data):
#         # ##print(data,output_data,'df')
#         if data[0] == '#':
#             for i in range(len(processed_nouns)):
#                 # ##print(processed_nouns[i][0],'dff')
#                 # if dataIndex in index_data:
#                     # ind = index_data.index(dataIndex-1)
#                 ind = index_data[dataIndex]
#                 if round(processed_nouns[i][0]) == ind:
#                     # ##print(processed_nouns[i][2],depend_data[i].split(':')[1],'klm')
#                     if depend_data[i] and processed_nouns[i][2]=='n' and depend_data[i].split(':')[1]=='k1s':
#                         # ##print('klm')
#                         has_changes = True
#                         temp = list(processed_nouns[i])
#                         temp[2] = 'adj'
#                         # temp[4] = 'f' if processed_nouns[i][4] == 'm' else 'm'
#                         processed_nouns[i] = tuple(temp)
#                     if processed_nouns[i][7] not in ('proper','NC','CP_noun', 'abs', 'vn'):
#                     #if not processed_nouns[i][7] == 'proper' and not processed_nouns[i][7] == 'NC' and not processed_nouns[i][7] == 'CP_noun':
#                         has_changes = True
#                         temp = list(processed_nouns[i])
#                         temp[4] = 'f' if processed_nouns[i][4] == 'm' else 'm'
#                         processed_nouns[i] = tuple(temp)
#                         log(f'{temp[1]} reprocessed as noun with gen:{temp[4]}.')
#                     else:
#                         break
#     # ##print(processed_nouns,'nn')
#     return has_changes, processed_nouns
def handle_unprocessed(index_data, depend_data, output_data, processed_nouns, construction_data):
    """
    Swaps gender info for nouns that do not exist in the dictionary.
    
    Args:
        index_data (list): Maps indices of `output_data` to corresponding indices in `processed_nouns`.
        depend_data (list): Dependency information for each word.
        output_data (list): Processed words from the sentence.
        processed_nouns (list): List of tuples representing processed nouns.
        
    Returns:
        tuple: A tuple containing a boolean indicating if changes were made and the updated `processed_nouns`.
    """
    has_changes = False

    # Ensure index_data is a list
    if not isinstance(index_data, list):
        raise ValueError("index_data must be a list mapping indices.")

    for dataIndex, data in enumerate(output_data):
        # Check if the current word starts with '#'
        if data.startswith('#'):
            # Get the corresponding index in processed_nouns
            if dataIndex >= len(index_data):
                continue  # Skip if index_data does not have a mapping for this dataIndex
            noun_index = index_data[dataIndex]

            # Find the matching noun in processed_nouns
            for i, noun in enumerate(processed_nouns):
                if round(noun[0]) == noun_index and len(noun) > 2 and noun[2] == 'n':
                    print(construction_data[i].split(':')[1] if ':' in construction_data[i] else "No ':' found")
                    
                    # Check if depend_data[i] exists and contains ':'
                    depend_check = depend_data[i] and isinstance(depend_data[i], str) and ':' in depend_data[i]
                    construction_check = construction_data[i] and isinstance(construction_data[i], str) and ':' in construction_data[i]

                    # Get dependency tags safely
                    depend_tag = depend_data[i].split(':')[1] if depend_check else ""
                    construction_tag = construction_data[i].split(':')[1] if construction_check else ""

                    # If either condition matches, update noun POS tag
                    if depend_tag == 'k1s' or construction_tag == 'kriyAmUla':
                        temp = list(noun)
                        temp[2] = 'adj'
                        processed_nouns[i] = tuple(temp)
                        has_changes = True
                        break  # Exit loop after first match

                    # Swap gender if the noun is not a proper noun or special type
                    if noun[7] not in ('proper', 'NC', 'CP_noun', 'abs', 'vn'):
                        temp = list(noun)
                        temp[4] = 'f' if noun[4] == 'm' else 'm'
                        processed_nouns[i] = tuple(temp)
                        has_changes = True
                        print(f'{temp[1]} reprocessed as noun with gen:{temp[4]}.')
                    break  # Stop searching once the noun is found
    print(processed_nouns,'pn')
    return has_changes, processed_nouns

def nextNounData_fromFullData(fromIndex, PP_FullData):
    index = fromIndex
    # ##print(index,'ind',PP_FullData)
    for data in PP_FullData:
        if data[0]==index and data[2] == 'n':
            return data

    return ()
def is_next_word_noun(index,processed_nouns):
    for data in processed_nouns:
        if data[0]==index and data[2]=='n':
            return data
            # return data
    else:
        return False

def nextNounData(fromIndex, word_info):
    #for NC go till NC_head and return that tuple
    # index = fromIndex
    # for i in range(len(word_info)):
    #     for data in word_info:
    #         if index == data[0]:
    #             if data[3] != '' and index != fromIndex:
    #                 return data
    index = fromIndex
    # ##print(index,'indx')
    for data in word_info:
        # if index == data[0] and data[3] != '':
        data=list(data)
        if index == str(data[0]):
            if 'female' in data[2]:
                data[2]='f'
            elif 'male' in data[2]:
                data[2]='m'
            if 'pl' in data[3]:
                data[3]='p'
            elif data[3]!='':
                data[3]='s'
            data=tuple(data)
            return data
                # if ':' in data[4]:
                #     index = int(data[4][0])
    return False

def fetchNextWord(index,index_data, words_info):
    next_word = ''
    idx = index_data[index]
    for data in words_info:
        if idx == data[0]:
            next_word = clean(data[1])
            break
    return next_word

def change_gender(current_gender):
    """
    >>> change_gender('m')
    'f'
    >>> change_gender('f')
    'm'
    """
    return 'f' if current_gender == 'm' else 'm'

def set_gender_make_plural(processed_words, g, num):
    process_data = []
    # for all k1s and main verb change gender to female and number to plural
    for i in range(len(processed_words)):
        word_list = list(processed_words[i])
        if word_list[2] == 'adj':
            # 4th index - gender, 5th index - number
            word_list[4] = g
            word_list[5] = num
        elif word_list[2] == 'v':
            # 3rd index - gender, 4th index - number
            word_list[3] = g
            word_list[4] = num
        process_data.append(tuple(word_list))
    return process_data

def set_main_verb_tam_zero(verb: Verb):
    verb.tam = 0
    return verb

def set_tam_for_nonfinite(dependency):
    '''
    Sets the TAM (Tense-Aspect-Mood) for non-finite verb forms based on the given dependency code.

    Parameters:
        dependency (str): The dependency code indicating the type of non-finite form.

    Returns:
        str: The TAM code for the given non-finite form.

    Examples:
        >>> set_tam_for_nonfinite('rvks')
        'adj_wA_huA'
        >>> set_tam_for_nonfinite('rbks')
        'yA_huA'
        >>> set_tam_for_nonfinite('rsk')
        'wA_huA'
        >>> set_tam_for_nonfinite('rpk')
        'kara'
    '''
    tam = {
        # 'rvks': 'adj_wA_huA',
        'rpk': 'kara',
        'rsk': 'adj_wA_huA',
        # 'rbks': 'adj_yA_huA',
        # 'rblpk': 'nA',
        # 'rbk': 'yA_gayA',
    }.get(dependency, '')
    return tam

def update_ppost_dict(data_index, param):
    # whether entry exists or not, param is updated in ppost_dict
    processed_postpositions_dict[data_index] = param

def extract_tamdict_hin():
    extract_tamdict = []
    try:
        with open(repository.constant.TAM_DICT_FILE, 'r') as tamfile:
            for line in tamfile.readlines():
                hin_tam = line.strip()
                if hin_tam:  # Ensure the line is not empty
                    extract_tamdict.append(hin_tam)
        # ##print(extract_tamdict)
        return extract_tamdict
    except FileNotFoundError:
        log('TAM Dictionary File not found.', 'ERROR')
        sys.exit()

def extract_gnp_noun(noun_data):
    gender = 'm'
    number = 's'
    person = 'a'

    if len(noun_data):
        noun_term = noun_data[1]
        if check_is_digit(noun_term):
            noun_term = noun_term
        elif '+' in noun_term:
            cn_terms = noun_term.strip().split('+')
            for i in range(len(cn_terms)):
                if i == len(cn_terms) - 1:
                    noun_term = clean(cn_terms[i])
        else:
            noun_term = clean(noun_term)

        #Setting gender
        seman_data = noun_data[2].strip()
        #seman_info_lst = seman_data.split()
        if len(seman_data) > 0:
            if 'female' in seman_data:
                gender = 'f'
            elif 'male' in seman_data:
                gender = 'm'
        else:
            tags = find_tags_from_dix(noun_term)
            # ##print(tags,'tags2')
            if '*' not in tags['form']:
                gender = tags['gen']

        #Setting number
        if len(noun_data[3]):
            # number = noun_data[3].strip()[0]
            if noun_data[3] =='':
                number = 's'
            elif noun_data[3]=='pl':
                number = 'p'
            # number = noun_data[3].strip()[3]

        #Setting person
        if noun_term == 'speaker':
            person = 'u'
        elif noun_term == 'addressee':
            person = 'm'
        else:
            person = 'a'
    return gender, number, person

def extract_gnp(data):
    gender = 'm'
    number = 's'
    person = 'a'

    if len(data):
        term = clean(data[1])

        # Setting gender
        seman_data = data[2].strip()
        # seman_info_lst = seman_data.split()
        if len(seman_data) > 0:
            if 'female' in seman_data:
                gender = 'f'
            elif 'male' in seman_data:
                gender = 'm'

        # Setting number
        if len(data[3]):
            if data[3]=='pl':
                number = 'p'
            else:
                number = 's'

        # Setting person
        if term == 'speaker':
            person = 'u'
        elif term == 'addressee':
            person = 'm'
        else:
            person = 'a'
    # ##print(number,'gl')
    return gender, number, person

def add_postposition(transformed_fulldata,index_data,depend_data, processed_postpositions):
    '''Adds postposition to words wherever applicable according to rules.'''
    PPFulldata = []
    # ##print(depend_data,'dpdd')
    for i, ele in enumerate(depend_data):
        if 'rs' in ele:
            # ##print(index_data,i)
            ind0, ind1 = index_data[i-1], index_data[i]
            if ind0 in processed_postpositions_dict:
                processed_postpositions_dict[ind1] = processed_postpositions_dict.pop(ind0)
    
    # ##print(processed_postpositions,'psp')
    for data in transformed_fulldata:
        index = data[0]
        if index in processed_postpositions:
            temp = list(data)
            ppost = processed_postpositions[index]
            if ppost != None and (temp[2] == 'n'or temp[2] == 'vn'):
                temp[1] = temp[1] + ' ' + str(ppost)
            data = tuple(temp)
        PPFulldata.append(data)
    return PPFulldata


def add_adj_to_noun_attribute(key, value):
    if key is not None:
        if key in repository.constant.noun_attribute:
            repository.constant.noun_attribute[key][0].append(value)
        else:
            repository.constant.noun_attribute[key] = [[],[]]

def add_verb_to_noun_attribute(key, value):
    if key is not None:
        if key in repository.constant.noun_attribute:
            repository.constant.noun_attribute[key][1].append(value)
        else:
            repository.constant.noun_attribute[key] = [[], []]

def add_spkview(full_data, spkview_dict):
    transformed_data = []
    for data in full_data:
        index = data[0]
        if index in spkview_dict:
            temp = list(data)
            spkview_info = spkview_dict[index]
            for info in spkview_info:
                tag = info[0]
                val = info[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                elif tag == 'after':
                    temp[1] = temp[1] + ' ' + val
                data = tuple(temp)
        transformed_data.append(data)
    return transformed_data

def add_MORPHO_SEMANTIC(full_data, MORPHO_SEMANTIC_DICT):
    transformed_data = []
    for data in full_data:
        index = data[0]
        if index in MORPHO_SEMANTIC_DICT:
            temp = list(data)
            term = MORPHO_SEMANTIC_DICT[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    temp[1] = temp[1] + ' ' + val
            data = tuple(temp)
        transformed_data.append(data)
    return transformed_data

def add_construction(transformed_data, construction_dict):
    Constructdata = []
    dependency_check=['k7p','k7t']
    add_words_list=['meM','ko','ke','kI','kA']
    depend_data1=''
    for data in transformed_data:
        index = data[0]
        if len(data)==9:
            depend_data1=data[8]
        if index in construction_dict:
            temp = list(data)
            term = construction_dict[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    if val == ',':
                        temp[1] = temp[1] + val
                    elif val == '-':
                        temp[1] = temp[1] + val
                    else:
                        if depend_data1!='' and depend_data1 in add_words_list and depend_data1 in temp[1]:
                            temp[1] = temp[1].split()[0] + ' ' +val
                        else:
                            temp[1] = temp[1] + ' ' +val
            # if clean(temp[1]) not in ('cp','conj','disjunct','span','widthmeas','depthmeas','distmeas','rate','timemeas','waw','calender','massmeas','heightmeas','spatial'):
            #     # del(temp)
            data = tuple(temp)
        Constructdata.append(data)
        
    return Constructdata

def add_additional_words(additional_words_dict, processed_data):
    additionalData = []
    for data in processed_data:
        index = data[0]
        if index in additional_words_dict:
            temp = list(data)
            term = additional_words_dict[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    temp1=temp[1].split()
                    if len(temp1)>=2 and temp1[1]=='ko':
                        temp1[1] = val
                        temp[1] = ' '.join(temp1)
                    else:
                        temp[1] = temp[1] + ' ' + val
            data = tuple(temp)
        additionalData.append(data)
    return additionalData

# post_process_utils.py

def add_coreferences(segment_id, index_data, words_info, json_output, discourse_data, coref_list):
    """
    Process coreferences and return the updated coref list.
    """
    # sub_coref_list=[]
    # if 'coref' in discourse_data[i]:  # No '.' in discourse_head, simpler case
    #     sub_coref_list.append(index_data[i])
    #     indx=int(discourse_data[i].split(':')[0])
    #     for processed_word in processed_words:
    #         if processed_word[0]==indx:  # Check if indx is composed entirely of digits
    #             coref_word = processed_word[1]
    #             # morpho_sem = processed_word[3]
    #             sub_coref_list.append(coref_word)

    #             break

    # if sub_coref_list:  # Append to coref_list if there's any coreference info
    #     coref_list.append(sub_coref_list)
    return process_coref(segment_id, index_data, words_info, json_output, discourse_data, coref_list)

def clean_post_process_output(post_process_output, processed_foreign_words):
    """
    Clean and update the post-process output with foreign words.
    """
    for i in range(len(processed_foreign_words)):
        n = processed_foreign_words[i][0]
        post_process_output[n - 1] = processed_foreign_words[i][1].replace('+', ' ')
    return ' '.join(post_process_output)

def add_discourse_elements_to_output(discourse_data,discourse, spkview_data, sp_data, post_process_output):
    """
    Add discourse elements to the output based on given data.
    """
    if not discourse_data:  # Check if discourse_data is None or empty
        return post_process_output
    relation = ['AvaSyakawApariNAma', 'vyaBicAra']
    if discourse and discourse in relation:
        return add_discourse_elements(discourse, spkview_data, sp_data, post_process_output)
    for i in discourse_data:
        if i and i.split(':')[1] not in relation and 'coref' not in i:
            post_process_output = add_discourse_elements(discourse_data, spkview_data, sp_data, post_process_output)
    return post_process_output

def check_special_conditions(discourse_data, spkview_data, post_process_output):
    """
    Modify the post-process output based on specific conditions.
    """
    for i in discourse_data:
        if 'AvaSyakawApariNAma' in i and 'nahIM' not in spkview_data:
            return 'yaxi ' + post_process_output
        elif 'vyaBicAra' in i:
            return 'yaxyapi ' + post_process_output
    return post_process_output


def fetch_NC_head(i, processed_words):
    for data in processed_words:
        temp = tuple(data)
        if int(temp[0]) == int(i) and temp[7] == 'NC_head':
            return temp[0]

def auxmap_hin(aux_verb):
    """
    Finds auxiliary verb in auxiliary mapping file. Returns its root and tam.
    >>> auxmap_hin('sakawA')
    ('saka', 'wA')
    """
    # ##print(aux_verb)
    # try:
    with open(repository.constant.AUX_MAP_FILE, 'r') as tamfile:
        for line in tamfile.readlines():
            # ##print(line,'lll')
            aux_mapping = line.strip().split(',')
            if aux_mapping[0] == aux_verb:
                return aux_mapping[1], aux_mapping[2]
    log(f'"{aux_verb}" not found in auxiliary mapping.', 'WARNING')
    #     return None, None       # TODO Figure out the fallback
    # except FileNotFoundError:
    #     log('auxiliary Mapping File not found.', 'ERROR')
    #     sys.exit()

def update_additional_words_dict(index, tag, add_word):
    value = (tag, add_word)
    value_found = False
    if index in additional_words_dict:
        value_list = additional_words_dict[index]
        for data in value_list:
            if data[0] == tag and data[1] == add_word:
                value_found = True
        if not value_found:
            additional_words_dict[index].append(value)
    else:
        additional_words_dict[index] = [value]

def to_tuple(verb: Verb):
    return (verb.index, verb.term, verb.category, verb.gender, verb.number, verb.person, verb.tam, verb.case, verb.type)

def postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info):
    for data in words_info:
        data_index = data[0]
        dep = data[4]
        # head = data[4].strip().split(':')[0]

        if 'r6' in dep:
            dep = data[4].strip().split(':')[1]
            head = data[4].strip().split(':')[0]
            for noun in processed_nouns:
                index = noun[0]
                case = noun[3]
                if head == str(index) and case == 'o':
                    update_ppost_dict(data_index, 'ke')

            for pronoun in processed_pronouns:
                index = pronoun[0]
                case = pronoun[3]
                if head == str(index) and case == 'o':
                    update_ppost_dict(data_index, 'ke')

            # for nominal_v in process_nominal_form:
            #     index = nominal_v[0]
            #     case = nominal_v[3]
            #     if head == str(index) and case == 'o':
            #         update_ppost_dict(data_index, 'ke')
            # for f_word in processed_foreign_words:
            #     index = f_word[0]
            #     case = f_word[3]
            #     if head == str(index) and case == 'o':
            #         update_ppost_dict(data_index, 'ke')

def collect_processed_data(index_data,processed_foreign_words,processed_pronouns, processed_nouns, processed_adjectives, processed_verbs,
                           processed_auxverbs, processed_indeclinables, processed_others):
    """collect sort and return processed data."""
    # sorted_data=sorted(processed_foreign_words+processed_pronouns + processed_nouns + processed_adjectives + processed_verbs + processed_auxverbs + processed_indeclinables + processed_others)
    combined_data = sorted(processed_foreign_words + processed_pronouns + processed_nouns + processed_adjectives +
                     processed_verbs + processed_auxverbs + processed_indeclinables + processed_others)

    # Initialize an empty list to hold the sorted data
    sorted_data = []

    # Create a set from index_data for quick lookup
    # index_set = set(map(float, index_data))  # Convert indices to float for comparison

    # Filter and sort combined data based on the order in index_data
    for index in index_data:
        # index = int(index)
        sorted_data.extend([item for item in combined_data if int(item[0]) == index])
    return sorted_data
    # return sorted_data

def join_compounds(transformed_data, construction_data):
    '''joins compound words without spaces'''
    resultant_data = []
    prevword = ''
    previndex = -1

    for data in transformed_data:
        if (data[0]) == previndex and data[2] == 'n':
            temp = list(data)
            temp[1] = prevword + ' ' + temp[1]
            data = tuple(temp)
            resultant_data.pop()
        resultant_data.append(data)
        previndex = data[0]
        prevword = data[1]
    return resultant_data

def populate_morpho_semantic_dict(index_data,gnp_info, PPfull_data,words_info):
    populate_morpho_semantic_dict = False
    a = 'after'
    b = 'before'
    
    for i,term in enumerate(gnp_info):
        input_string = gnp_info[i]
        # matches = re.findall(r'\[(.*?)\]', input_string)
        # strings = [s.strip() for s in matches]

        # for term in strings:
        # ##print(morpho_seman)
        if term in repository.constant.morpho_seman:
            populate_morpho_semantic_dict = True
            if term == 'superl':
                temp = (b, 'sabase')

            elif term in ('compermore','comper_more', 'comper-more'):
                # ##print('var')
                temp = (b, 'aXika')
            # elif term in ('quantless'):
            #     # ##print('var')
            #     temp = (a, 'se kama')
            # elif term in ('quantmore'):
            #     # ##print('var')
            #     temp = (a, 'se aXika')
            elif term in ('comperless','comper_less', 'comper-less'):
                temp = (b, 'kama')
            # elif term == 'dviwva':
            #     dup_word = clean(words_info[i][1])
            #     # ##print(dup_word,'dupw')
            #     if dup_word in PPfull_data[i][1]:  # Check membership in tuple
            #         if '<>' in PPfull_data[i][1]:
            #             dup_word1= dup_word +'-'+ dup_word + ' <>'
            #             PPfull_data[i] = (PPfull_data[i][0], dup_word1)  # Replace the tuple
            #             temp = (a, '')
            #         else:
            #             dup_word = '-' + dup_word
            #             temp = (a, dup_word)
            elif term == 'dviwva':
                dup_word = clean(words_info[i][1])
                # #print(dup_word,'dupw')
                if dup_word in PPfull_data[i][1]:  # Check membership in tuple
                    if 'para' in PPfull_data[i][1]:
                        dup_word1= dup_word +'-'+ dup_word + ' para'
                        PPfull_data[i] = (PPfull_data[i][0], dup_word1)  # Replace the tuple
                        temp = (a, '')
                    else:
                        dup_word = '-' + dup_word
                        temp = (a, dup_word)
            else:
                # fetch GNP of next noun
                # curr_index = 
                # ##print(index_data[i+1],i,'ndd')
                # ##print(PPfull_data)
                noun_data = nextNounData_fromFullData(index_data[i+1], PPfull_data)
                # ##print(noun_data)
                if noun_data != ():
                    g = noun_data[4]
                    n = noun_data[5]
                    p = noun_data[6]
                    if g == 'f':
                        temp = (a, 'vAlI')
                    elif n == 'p':
                        temp = (a, 'vAle')
                    elif n == 's':
                        temp = (a, 'vAlA')
            if index_data[i] in MORPHO_SEMANTIC_DICT:
                MORPHO_SEMANTIC_DICT[index_data[i]].append(temp)
            else:
                MORPHO_SEMANTIC_DICT[index_data[i]] = [temp]
    return populate_morpho_semantic_dict,PPfull_data

def join_indeclinables(transformed_data, processed_indeclinables, processed_others):

    """Joins Indeclinable data with transformed data and sort it by index number."""
    return transformed_data + processed_indeclinables + processed_others

# def rearrange_sentence(fulldata,coref_list):
#     '''Function comments'''
#     finalData = fulldata
#     final_words = [x[1].strip() for x in finalData]
#     r_s=" ".join(final_words)
#     return r_s

# def filter_and_concat_data(data, sentence_type_dict):
#     print('data:',data)
#     filtered_data = {}

#     for key, values in data.items():
#         concatenated = []
#         for item in values:
#             word = item[1]
#             # Only add the word if it's not in the construction_list
#             if word not in repository.constant.construction_list:
#                 concatenated.append(word)

#         # Check if the key exists in sentence_type_dict
#         if key in sentence_type_dict:
#             # Call has_ques_mark with concatenated words and sentence type
#             concatenated_data = has_ques_mark(' '.join(concatenated), sentence_type_dict[key])

#         # Store the concatenated result in the filtered data dictionary
#         filtered_data[key] = [concatenated_data]
#     print(filtered_data)
#     return filtered_data
def filter_and_concat_data(data, sentence_type_dict):
    print('data:', data)
    filtered_data = {}

    for key, values in data.items():
        # Check if the value is a list of tuples
        if isinstance(values, list) and all(isinstance(item, tuple) for item in values):
            concatenated = []
            for item in values:
                word = item[1]
                # Only add the word if it's not in the construction_list
                if word not in repository.constant.construction_list:
                    concatenated.append(word)

            # Check if the key exists in sentence_type_dict
            if key in sentence_type_dict:
                # Call has_ques_mark with concatenated words and sentence type
                concatenated_data = has_ques_mark(' '.join(concatenated), sentence_type_dict[key])
            else:
                concatenated_data = ' '.join(concatenated)

            # Store the concatenated result in the filtered data dictionary
            filtered_data[key] = [concatenated_data]

        # If the value is a string, return it unchanged
        elif isinstance(values, str):
            filtered_data[key] = ["ERROR: " + values]

        # Handle unexpected types (optional)
        else:
            filtered_data[key] = ["Unexpected data format"]
    print('filtered',filtered_data)
    return filtered_data

def rearrange_sentence(fulldata, index_data):
    '''Function to rearrange sentence based on coreference list'''
    # Create a dictionary for quick lookup from coref_list
    # coref_dict = {item[0]: item[1] for item in coref_list}
    # coref_dict = {index: value for index, value in coref_list}
    finalData = []
    # Join the words for the final rearranged sentence
    # final_words = [x[1].strip() for x in finalData]
    # r_s = " ".join(final_words)
    final_words = []
    for i in range(len(finalData)):
        word = finalData[i][1].strip()
        
        # If the word ends with a hyphen, join without space
        if i > 0 and final_words[-1].endswith('-'):
            final_words[-1] = final_words[-1] + word
        else:
            final_words.append(word)
    
    r_s = " ".join(final_words)
    ##print(r_s,'rsss')
    return r_s

# def collect_hindi_output(source_text):
#     """Take the output text and find the hindi text from it."""
#     hindi_format = WXC(order="wx2utf", lang="hin")
#     if source_text and '_' in source_text:
#         source_text = source_text.replace('_', ' ')

#     generate_hindi_text = hindi_format.convert(source_text)
#     return generate_hindi_text

def collect_hindi_output(filtered_data):
    """Take the filtered data and convert the Hindi text found in it."""
    hindi_format = WXC(order="wx2utf", lang="hin")
    
    # Create a dictionary to store the converted text
    converted_data = {}
    
    for key, values in filtered_data.items():
        # Iterate through the list of values for each key
        converted_values = []
        for value in values:
            if value.startswith("ERROR:"):
                # Append the value as-is without conversion
                converted_values.append(value)
            else:
            # Replace underscores with spaces if applicable
                words = value.split()
    # Filter and join words
                value = ' '.join(v for v in words if v[1:] not in repository.constant.construction_list)
                value = value.replace('_', ' ')
                # Convert the Hindi text using the WXC converter
                generate_hindi_text = hindi_format.convert(value)
                #mask tag
                if '<>' in generate_hindi_text:
                    print(generate_hindi_text,'oppp')
                    generate_hindi_text = generate_hindi_text.replace('<>','[MASK]')
                converted_values.append(generate_hindi_text)
            # Store the converted values in the dictionary
        converted_data[key] = converted_values
    
    return converted_data


def parse_segments(input_text):
    """
    Split the input text into segments based on </id>.
    """
    return input_text.strip().split('</id>')

def reset_global_dicts():
    global additional_words_dict, processed_postpositions_dict, construction_dict, spkview_dict, MORPHO_SEMANTIC_DICT
    additional_words_dict.clear()
    processed_postpositions_dict.clear()
    construction_dict.clear()
    spkview_dict.clear()
    MORPHO_SEMANTIC_DICT.clear()

# def convert_sentences_to_json(sentences):
#     """
#     Converts a list of sentences into the required JSON format.
    
#     Args:
#         sentences (list): A list of sentences.
    
#     Returns:
#         str: A JSON string with the sentences in the specified format.
#     """
#     # Prepare the output structure
#     output = {
#         "sentences": sentences
#     }
    
#     # Convert the dictionary to JSON
#     output_json = json.dumps(output, ensure_ascii=False, indent=4)
#     return output_json    


# from repository.common_v4 import *
# def multi_construction():

if __name__ == '__main__':
    import doctest
    doctest.run_docstring_examples(identify_complete_tam_for_verb, globals())

# ==============================================