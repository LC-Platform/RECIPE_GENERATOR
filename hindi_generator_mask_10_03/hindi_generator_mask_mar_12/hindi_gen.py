import sys
import json
from repository.common_v4 import *
from repository.USR_to_JSON import USR_to_json
from repository.coref_discourse import *
from repository.constant import *
from repository.construction import *
from repository.reorder import rearrange_tuples,arrange_by_index_order
from repository.morph_gen import generate_morph
from repository.preprocessing import process_segment,preprocess_id
from repository.identify_cat import identify_cat
from repository.process_cat import process_all_cat,process_change
from my_masking_model import *

# Main function that handles the core processing logic
def process_file_data(input_data,segment_id):
    global HAS_CONSTRUCTION_DATA, HAS_SPKVIEW_DATA, HAS_MORPHO_SEMANTIC_DATA, HAS_DISCOURSE_DATA, HAS_COREF
    global flag_conj, flag_disjunct, flag_span, flag_cp, flag_meas, flag_rate, flag_spatial, flag_waw, flag_cal, flag_xvanxva, flag_temporal_spatial, k1_not_need, has_changes

    # Initialize flags and output data list
    try:
        reset_global_dicts()
        rules_info = generate_rulesinfo(input_data) #Extracting Rules from each row of USR
        
        # Extracting Information
        src_sentence = rules_info[0]
        root_words = rules_info[1]
        index_data = [int(x) for x in rules_info[2]]
        seman_data = rules_info[3]
        gnp_data = rules_info[4]
        depend_data = rules_info[5]
        discourse_data = rules_info[6]
        spkview_data = rules_info[7]
        scope_data = rules_info[8]
        construction_data = rules_info[9]
        sentence_type = rules_info[10]

        if sentence_type[1:] in pass_list:
            k1_not_need=True
        
        # check_main_verb(depend_data)
        # try:
            # if sentence_type[1:] not in 
        check_main_verb(depend_data)
        #     if not has_main_verb:
        #         raise Exception("Main verb is missing in the dependency data")
        # except Exception as e:
        #     print('ERROR_1:',e)
        #     PP_fulldata_dict_with_id = create_dict_with_ids(segment_id, str(e).splitlines()[-1])
        #     return PP_fulldata_dict_with_id
        
        depend_data, HAS_CONSTRUCTION_DATA, flags = identify_and_assign_dep(root_words, construction_data, depend_data, index_data, spkview_data)

        if spkview_data != [] or len(spkview_data) > 0:
            HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data,discourse_data,index_data)
        if any(discourse_data):
            HAS_DISCOURSE_DATA = True
        if any('coref' in item for item in discourse_data):
            HAS_COREF = True

        # Making a collection of words and its rules as a list of tuples.
        words_info = generate_wordinfo(root_words, index_data, seman_data,
                                    gnp_data, depend_data, discourse_data, spkview_data,scope_data,construction_data)
        
        print(words_info,'wf')
        # index_order,words_info = rearrange_tuples(words_info)
        # foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data 
        categorized_words_list= identify_cat(words_info,sentence_type)

        #  Processing Stage - identify the cat and proces each cat
        processed_foreign_words,processed_indeclinables,processed_nouns,processed_pronouns,processed_others,process_nominal_form,processed_verbs, processed_auxverbs,processed_adjectives,processed_words= process_all_cat(
            categorized_words_list,index_data,gnp_data,seman_data,depend_data,spkview_data,sentence_type,words_info,k1_not_need,has_changes)
        
        print('processed_words:',processed_words)
        # processed_words = arrange_by_index_order(processed_words, index_order)
        
        if HAS_CONSTRUCTION_DATA:
            processed_words, flags = process_construction(processed_words, root_words, construction_data, depend_data, 
                                gnp_data, index_data, flags)

        # Input for morph generator is generated and fed into it.
        # Generator outputs the result in a file named morph_input.txt-out.txt
        outputData = generate_morph(processed_words)
        outputData = check_words_in_dict(outputData,processed_words)
        
        # Check for any non-generated words (mainly noun) & change the gender for non-generated words
    
        # # -> is for the concept which is in dict but its morph data is not found
        # * -> then the conept is not found in dict
        # has_changes, processed_nouns = handle_unprocessed(index_order,depend_data,outputData, processed_nouns, construction_data)
        has_changes, processed_nouns = handle_unprocessed(index_data,depend_data,outputData, processed_nouns, construction_data)
        # handle unprocessed_verbs also with verb agreement
        # If any changes is done in gender for any word.
        # Adjectives and verbs are re-processed as they might be dependent on it.
        if has_changes:
            # Reprocessing adjectives and verbs based on new noun info
            # processed_foreign_words,processed_indeclinables,processed_nouns,processed_pronouns,processed_others,process_nominal_form,processed_verbs, processed_auxverbs,processed_adjectives,processed_words= identify_and_process_all_cat(index_data,gnp_data,seman_data,depend_data,spkview_data,sentence_type,words_info,k1_not_need,has_changes)
            processed_words = process_change(rules_info,categorized_words_list,words_info,processed_nouns,processed_pronouns,processed_others,processed_foreign_words,processed_indeclinables)
            # Sentence is generated again
            if HAS_CONSTRUCTION_DATA:
                processed_words, flags = process_construction(processed_words, root_words, construction_data, depend_data, 
                                gnp_data, index_data, flags)

            outputData = generate_morph(processed_words)
        # outputData = check_words_in_dict(outputData,processed_words)
        # Post-Processing Stage
        # generated words and word-info data is combined #pp data not yet added
        transformed_data = analyse_output_data(outputData, processed_words)

        PP_fulldata = add_postposition(transformed_data,index_data,depend_data, processed_postpositions_dict)
        
        #construction data is joined
        if HAS_CONSTRUCTION_DATA:
            PP_fulldata = add_construction(PP_fulldata, construction_dict)
        
        if HAS_SPKVIEW_DATA:
            PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

        HAS_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(index_data,gnp_data, PP_fulldata,words_info)
        if HAS_MORPHO_SEMANTIC_DATA:
            PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

        # if HAS_ADDITIONAL_WORDS:
        #     PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)
        # print(PP_fulldata,'lkl')
        # print(PP_fulldata_dict_with_id,'kkk')
        PP_fulldata_dict_with_id = create_dict_with_ids(segment_id, PP_fulldata)
        
        return PP_fulldata_dict_with_id
    
    except Exception as e:
            # Return the last line of the error message
        print('ERROR_2:',e)
        error = create_dict_with_ids(segment_id, str(e))
        # return str(e).splitlines()[-1]
        return error
    
def hindi_generation(input_text):
    """
    Process Hindi text input, extracting sentences, segment IDs, and generating structured output.
    """
    PP_fulldata_dict_with_ids = {}
    input_text = preprocess_id(input_text)
    segments = parse_segments(input_text)

    sentences, all_output, segment_ids = [], [], []
    parser = USR_to_json(input_text)
    parser.parse_input_text()
    construction_json = generate_construction_json(parser.parse_input_text())
    coref_json,coref_dict,sentence_type_dict = process_coreferences(parser.parse_input_text())
    disource_json=transform_data(parser.parse_input_text())

    with open('construction.json', 'w', encoding='utf-8') as f:
        json.dump(construction_json, f, ensure_ascii=False, indent=2)
    with open("discource.json", "w") as file:
        json.dump(disource_json, file, indent=4)
    with open("output.json", "w") as file:
        json.dump(parser.parse_input_text(), file, indent=4)

    for segment in segments:
        segment_id, sentence, output = process_segment(segment)
        if segment_id:
            segment_ids.append(segment_id)
        if output:
            try:
                output1=process_file_data(output,segment_id)
                print(output1,'o1')
                # below comented are for mask 
                # if '<>' in output1:
                #     print(output1,'oppp')
                #     output1 = output1.replace('<>','[MASK]')
                # # print(output1,'oppp')
                PP_fulldata_dict_with_ids.update(output1)
            except Exception as e:
                print('ERROR_3:',e)
                all_output.append(f"Error processing {segment_id}: {str(e).splitlines()[-1]}")
    
    PP_fulldata_dict_with_ids = update_morph_dict_coref(coref_json, PP_fulldata_dict_with_ids)
    
    filtered_data = filter_and_concat_data(PP_fulldata_dict_with_ids,sentence_type_dict)
    
    with open('generated_data.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    filtered_data = update_discourse_sentences(disource_json, filtered_data)
    
    masked_hindi_data=collect_hindi_output(filtered_data)
    # below comented fun are for mask 
    # json_output1 = convert_sentences_to_json(all_output)
    # all_output=process_masked_multiple_sentences(json_output1)
    last_output = process_sentence(masked_hindi_data, sentences)
    print(last_output)
    print(global_starred_words, 'Global starred words with categories')

    return last_output

if __name__ == '__main__':
    input_data='''<segment_id=sept-7-2022ICF-HD_source_hin_032a>
#यदि हमारे अध्ययन से कोई उपचार निकलता है ।
$speaker	1	anim	pl	2:r6	-	-	-	-
aXyayana_1	2	-	-	5:k5	-	-	-	-
koI_1	3	-	-	4:quant	-	-	-	-
upacAra_7	4	-	-	5:k1	-	-	-	-
nikala_2-wA_hE_1	5	-	-	0:main	sept-7-2022ICF-HD_source_hin_032b.6:AvaSyakawApariNAma	-	-	-
%affirmative
</segment_id>

<segment_id=sept-7-2022ICF-HD_source_hin_032b>
#तो आपसे संपर्क किया जाएगा।
$addressee	1	-	-	6:k2	-	-	-	-
saMparka_1	2	-	-	-	-	-	-	6:kriyAmUla
kara_17-yA_jA_gA_1	3	-	-	-	-	-	-	6:verbalizer
[cp_1]	6	-	-	0:main	-	-	-	-
%affirmative
</segment_id>

<segment_id=sept-7-2022ICF-HD_source_hin_022>
#इस अध्ययन में भाग लेने के लिए क्या करना होगा?
$wyax	1	-	-	2:dem	-	proximal	-	-
aXyayana_1	2	-	-	8:k7	-	-	-	-
BAga_2	3	-	-	-	-	-	-	8:kriyAmUla
le_1	4	-	-	-	-	-	-	8:verbalizer
$speaker	5	anim	pl	7:k1	-	-	-	-
$kim	6	-	-	7:k2	-	-	-	-
kara_17-nA_hogA_1	7	-	-	0:main	-	-	-	-
[cp_1]	8	-	-	7:rt	-	-	-	-
%interrogative
</segment_id>

<segment_id=sept-7-2022ICF-HD_source_hin_017>
#बीटा थैलेसीमिया एक रक्त विकार है जो हीमोग्लोबिन के उत्पादन को कम करता है।
bItA	1	-	-	-	-	-	-	3:begin
WElesImiyA	2	-	-	-	-	-	-	3:inside
[ne_1]	3	-	-	7:k1	-	-	-	-
rakwa_1	5	-	-	-	-	-	-	14:mod
vikAra_4	6	-	-	-	-	-	-	14:head
hE_1-pres	7	-	-	0:main	-	-	-	-
$yax	8	-	-	15:k1	1:k1	-	-	-
hImoglobina	9	-	-	-	-	-	-	10:begin
[ne_2]	10	-	-	11:r6	-	-	-	-
uwpAxana_1	11	-	-	15:k2	-	-	-	-
kara_17-wA_hE_1	13	-	-	-	-	-	-	15:verbalizer
[nc_1]	14	-	-	7:k1s	-	-	-	-
[cp_1]	15	-	-	3:rcelab	-	-	-	-
eka_2	4	-	-	14:quant	-	-	-	-
kama_8	12	-	-	-	-	-	-	15:kriyAmUla
%affirmative
</segment_id>
'''
    # file_path = './concatenated_output.txt'
    
    
    # # Read input data from the file
    # input_data = read_file(file_path)
    
    hindi_generation(input_data)
# [{"segment_id": "7a", "text": "ना केवल वे आज्ञाकारी ही थे।"}, {"segment_id": "7b", "text": "बल्कि वे बहुत समझदार भी थे भी।"}]}
