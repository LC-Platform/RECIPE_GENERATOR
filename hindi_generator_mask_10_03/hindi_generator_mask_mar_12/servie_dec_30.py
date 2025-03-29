# from flask import Flask, request, jsonify
import sys
from repository.common_v4 import *
#from common_v2 import *
from repository.USR_to_JSON import USR_to_json
from repository.coref_discourse import *
import json
from repository.constant import *


# from repository.my_masking_model import *
# Global flags
HAS_CONSTRUCTION_DATA = False
HAS_SPKVIEW_DATA = False
ADD_MORPHO_SEMANTIC_DATA = False
HAS_DISCOURSE_DATA = False
HAS_ADDITIONAL_WORDS = False
HAS_COREF = False
flag_conj = False
flag_disjunct = False
flag_span = False
flag_cp = False
flag_meas = False
flag_rate = False
flag_spatial = False
flag_waw = False
flag_cal = False
flag_xvanxva = False
flag_temporal = False
k1_not_need = False
# Import all the required functions from your other modules
# Example:
# from common_v3 import (read_file, generate_rulesinfo, process_verbs, etc.)
# from Json_format import Json_format
# from extract_json_data import *
# Main function that handles the core processing logic
def process_file_data(input_data,segment_id,json_output):
    global HAS_CONSTRUCTION_DATA, HAS_SPKVIEW_DATA, ADD_MORPHO_SEMANTIC_DATA, HAS_DISCOURSE_DATA, HAS_ADDITIONAL_WORDS, HAS_COREF
    global flag_conj, flag_disjunct, flag_span, flag_cp, flag_meas, flag_rate, flag_spatial, flag_waw, flag_cal, flag_xvanxva, flag_temporal, k1_not_need

    # Initialize flags and output data list
    output_data_list = []
    coref_list=[]
    pass_list=['pass-affirmative','pass-interrogative','pass-negative']
    # output_text,sentence_id=convert_vert_to_csv(input_data)
    # Read the input file
    # file_data= read_file(output_text)
    # ##print(output_text,'hhh')
    # Extract rules info
    try:
        reset_global_dicts()
        rules_info = generate_rulesinfo(input_data) #Extracting Rules from each row of USR
        print('rules_info')
        # Extracting Information
        src_sentence = rules_info[0]
        print('src_sentence:',src_sentence)
        root_words = rules_info[1]
        print('root_words:',root_words)
        # print(root_words,'root_words')
        index_data = [int(x) for x in rules_info[2]]
        print('index_data:',index_data)
        # print(index_data,'index_data')
        seman_data = rules_info[3]
        print('seman_data:',seman_data)
        # print(seman_data,'seman_data')
        gnp_data = rules_info[4]
        print('gnp_data:',gnp_data)
        # print(gnp_data,'gnp_data')
        #print(gnp_data,'rulesss')
        depend_data = rules_info[5]
        print('depend_data:',depend_data)
        # print(depend_data,'depend_data')
        discourse_data = rules_info[6]
        print('discourse_data:',discourse_data)
        # print(discourse_data,'discourse_data')
        spkview_data = rules_info[7]
        print('spkview_data:',spkview_data)
        # print(spkview_data,'spkview_data')
        scope_data = rules_info[8]
        print('scope_data:',scope_data)
        # print(scope_data,'scope_data')
        construction_data = rules_info[9]
        print('construction_data:',construction_data)
        # print(construction_data,'construction_data')
        # ##print(construction_data,'cd')
        sentence_type = rules_info[10]
        print('sentence_type:',sentence_type)
        # print(sentence_type,'sentence_type')
        ##print(sentence_type[1:],'sentencesssss')
        if sentence_type[1:] in pass_list:
            k1_not_need=True
        # ##print(k1_not_need)
        # ##print(depend_data,'dp')
        # ##print(depend_data,'dp')
        construction=['conj','span']
        conj_concept=[]
        span_concept=[]
        conj_concept=root_words
        span_concept=root_words

        # ##print(span_concept,'cc')

        for i, concept in enumerate(root_words):
            if 'conj' in concept :
                flag_conj=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'disjunct' in concept :
                flag_disjunct=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'span' in concept :
                flag_span=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_span(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'cp' in concept:
                flag_cp=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_cp(i,construction_data,depend_data,index_data,spkview_data)
            elif 'meas' in concept:
                flag_meas=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_meas(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'rate' in concept:
                flag_rate=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_meas(i,construction_data,depend_data,index_data)
            elif 'waw' in concept:
                flag_waw=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_waw(i,construction_data,depend_data,index_data)
            elif clean(concept) in ('compound','waw'):
                flag_waw=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_waw(i,construction_data,depend_data,index_data)
            elif 'calender' in concept:
                flag_cal=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_calender(i,construction_data,depend_data,index_data)
            elif 'spatial' in concept:
                flag_spatial=True
                HAS_CONSTRUCTION_DATA = True
                depend_data= construction_row_spatial(i,construction_data,depend_data,index_data)
            elif 'xvanxva' in concept:
                flag_xvanxva=True
                HAS_CONSTRUCTION_DATA = True
                depend_data= construction_row(i,construction_data,depend_data,index_data)
            elif 'temporal' in concept:
                flag_temporal=True
                HAS_CONSTRUCTION_DATA = True
                depend_data= construction_row_temporal(i,construction_data,depend_data,index_data)
            
        check_main_verb(depend_data)
        # if len(rules_info) > 10 and rules_info[10] != '':
        #     if 'speaker not found in dictionary' in rules_info[10]:
        #         construction_data = ''
        #     else:
        #         HAS_CONSTRUCTION_DATA = True
        #only when construction data is not nil
        # if flag_conj or flag_span:
        #     # construction_data = rules_info[10]
        #     HAS_CONSTRUCTION_DATA = True

        # if len(rules_info) > 10 and rules_info[10]!='*nil':
        #     construction_data = rules_info[10]
        #     HAS_CONSTRUCTION_DATA = True

        if spkview_data != [] or len(spkview_data) > 0:
            HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data,index_data)
            #returns true or false
        if discourse_data != [] or len(discourse_data) > 0:
            # HAS_DISCOURSE_DATA = populate_disc(discourse_data)
            HAS_DISCOURSE_DATA = True

        if any('coref' in item for item in discourse_data):
            HAS_COREF = True

        
        # Making a collection of words and its rules as a list of tuples.
        words_info = generate_wordinfo(root_words, index_data, seman_data,
                                    gnp_data, depend_data, discourse_data, spkview_data,scope_data,construction_data)
        print('words_info')
        print(words_info)
        # ##print(words_info,'cccccccccccc')
        # Categorising words as Nouns/Pronouns/Adjectives/..etc.
        foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = identify_cat(
            words_info,sentence_type)
        print('identify cat')
        print(foreign_words_data,'foreign_words_data')
        print(indeclinables_data,'indeclinables_data')
        print(pronouns_data,'pronouns_data')
        print(nouns_data,'nouns_data')
        print(verbal_adjectives,'verbal_adjectives')
        print(adjectives_data,'adjectives_data')
        print(verbs_data,'verbs_data')
        print(adverbs_data,'adverbs_data')
        print(others_data,'others_data')
        print(nominal_forms_data,'nominal_forms_data')

        # ##print(verbs_data,'vd')

        #  Processing Stage
        processed_foreign_words = process_foreign_word(index_data,foreign_words_data,words_info,verbs_data)
        print('processed_foreign_words:',processed_foreign_words)
        processed_indeclinables = process_indeclinables(indeclinables_data)
        print('processed_indeclinables:',processed_indeclinables)
        processed_nouns = process_nouns(index_data,seman_data,nouns_data, words_info, verbs_data)
        print('processed_nouns:',processed_nouns)
        # ##print(processed_nouns)
        processed_pronouns = process_pronouns(index_data,pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
        print('processed_pronouns:',processed_pronouns)
        processed_others = process_others(others_data)
        print('processed_others:',processed_others)
        process_nominal_form = process_nominal_verb(index_data,nominal_forms_data, processed_nouns, words_info, verbs_data)
        print('process_nominal_form:',process_nominal_form)
        processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data,processed_nouns, processed_pronouns,index_data, words_info,k1_not_need, False)
        print('processed_verbs:',processed_verbs)
        print('processed_auxverbs:',processed_auxverbs)
        # processed_adjectives = process_verbal_adjective(verbal_adjectives,processed_nouns, words_info, verbs_data)
        processed_adjectives = process_adjectives(adjectives_data,gnp_data,index_data, processed_nouns, processed_verbs)
        print('processed_adjectives:',processed_adjectives)
        process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
        print('adverbs_data:',adverbs_data)
        postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info)
        print('postposition_finalization:',processed_nouns)
        if len(additional_words_dict) > 0:
            # ##print(additional_words_dict,'jjjjjjjjjjj')
            HAS_ADDITIONAL_WORDS = True
        # ##print(processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
                                                # processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)

        # Every word is collected into one and sorted by index number.
        processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
                                                processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)
        print('collect_processed_data:',processed_words)
        # ##print(processed_words,'pw')
        # processed_words = if_morph_kqwpft(processed_words,gnp_data)
        #print(processed_words,'pww')
        # calculating postpositions for words if applicable.
        # processed_words, processed_postpositions = preprocess_postposition_new(processed_words, words_info,processed_verbs)
        if HAS_CONSTRUCTION_DATA:
            if flag_conj or flag_disjunct:
                processed_words = process_construction(processed_words,root_words, construction_data, depend_data, gnp_data, index_data,conj_concept)
                flag_conj,flag_disjunct=False,False
            if flag_span:
                processed_words = process_construction_span(processed_words, construction_data,index_data)
                flag_span=False
            if flag_rate:
                processed_words = process_construction_rate(processed_words, construction_data,index_data)
                flag_rate=False
            if flag_spatial:
                processed_words = process_construction_spatial(processed_words, construction_data,index_data)
                flag_spatial=False
            if flag_xvanxva:
                processed_words = process_construction_xvanxva(processed_words, construction_data,index_data)
                flag_xvanxva=False
            # if flag_temporal:


        # Input for morph generator is generated and fed into it.
        # Generator outputs the result in a file named morph_input.txt-out.txt
        outputData = generate_morph(processed_words)
        print('generate_morph:',outputData)
        outputData = check_words_in_dict(outputData,processed_words)

        # Create a new list to store the data from the output file
        # outputData = read_output_data(OUTPUT_FILE)
        # Check for any non-generated words (mainly noun) & change the gender for non-generated words
        # has_changes, reprocess_list, processed_nouns = handle_unprocessed_all(outputData, processed_nouns)
        # ##print(reprocess_list)
        has_changes, processed_nouns = handle_unprocessed(index_data,depend_data,outputData, processed_nouns)

        # handle unprocessed_verbs also with verb agreement
        # If any changes is done in gender for any word.
        # Adjectives and verbs are re-processed as they might be dependent on it.
        if has_changes:
            # Reprocessing adjectives and verbs based on new noun info
            processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, words_info, True)
            processed_adjectives = process_adjectives(adjectives_data,gnp_data,index_data, processed_nouns, processed_verbs)
            process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)
            # Sentence is generated again
            processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns, processed_nouns,  processed_adjectives, processed_verbs,processed_auxverbs,processed_indeclinables,processed_others)
            if HAS_CONSTRUCTION_DATA:
                if flag_conj or flag_disjunct:
                    processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data,index_data,conj_concept)
                if flag_span:
                    processed_words = process_construction_span(processed_words, construction_data, index_data)
                if flag_rate:
                    processed_words = process_construction_rate(processed_words, construction_data,index_data)
                if flag_spatial:
                    processed_words = process_construction_spatial(processed_words, construction_data,index_data)

            outputData = generate_morph(processed_words)
            print('generate_morph 2:',outputData)
        #print(processed_words,'pwp')
        # outputData = check_words_in_dict(outputData,processed_words)
        # #print(outputData,'ooooooo')
        # Post-Processing Stage
        # outputData = read_output_data(OUTPUT_FILE)
        # generated words and word-info data is combined #pp data not yet added
        transformed_data = analyse_output_data(outputData, processed_words)
        print('analyse_output_data:',transformed_data)

        # compound words and post-positions are joined.
        transformed_data = join_compounds(transformed_data, construction_data)
        print('join_compounds:',transformed_data)
        # transformed_data = rs_fun(index_data,depend_data,transformed_data)
        #post-positions are joined.
        
        PP_fulldata = add_postposition(transformed_data,index_data,depend_data, processed_postpositions_dict)
        print('add_postposition:',PP_fulldata)
        # masked_pup_list = masked_postposition(processed_words, words_info, processed_verbs)
        # ##print(masked_pup_list,'masked1')
        # PP_fulldata = add_postposition(transformed_data,index_data, depend_data, masked_pup_list)
        # ##print(PP_fulldata,'masked2')
        #construction data is joined
        if HAS_CONSTRUCTION_DATA:
            PP_fulldata = add_construction(PP_fulldata, construction_dict)
            print('add_construction:',PP_fulldata)

        if HAS_SPKVIEW_DATA:
            PP_fulldata = add_spkview(PP_fulldata, spkview_dict)
            print('add_spkview:',PP_fulldata)

        ADD_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(index_data,gnp_data, PP_fulldata,words_info)
        if ADD_MORPHO_SEMANTIC_DATA:
            PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)
            print('add_MORPHO_SEMANTIC:',PP_fulldata)

        if HAS_ADDITIONAL_WORDS:
            PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)
            print('add_additional_words:',PP_fulldata)
        # ##print(input_data,discourse_data,HAS_COREF,'inpp')
        if HAS_COREF:
            coref_list=process_coref(segment_id,index_data,processed_words,json_output,discourse_data,coref_list)
            print('coref_list:',coref_list)
        # POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata,coref_list)  # reaarange by index number
        POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata,coref_list)
        print('POST_PROCESS_OUTPUT:',POST_PROCESS_OUTPUT)
        ##print(POST_PROCESS_OUTPUT,'ppo')
        POST_PROCESS_OUTPUT=POST_PROCESS_OUTPUT.split()
        # ##print(POST_PROCESS_OUTPUT)
        # allowed_values = ('cp', 'conj', 'disjunct', 'span', 'widthmeas', 'depthmeas', 'distmeas', 'rate', 'timemeas', 'waw', 'calender', 'massmeas', 'heightmeas', 'spatial')
        POST_PROCESS_OUTPUT = [word for word in POST_PROCESS_OUTPUT if clean(word) not in repository.constant.construction_list]

        for i in range(len(processed_foreign_words)):
            n=processed_foreign_words[i][0]
            POST_PROCESS_OUTPUT[n-1] = processed_foreign_words[i][1].replace('+',' ')
        POST_PROCESS_OUTPUT=' '.join(POST_PROCESS_OUTPUT)

        if HAS_DISCOURSE_DATA:
            # POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
            # fp = 'output.json'
            discourse,sp_data = extract_discourse_values(json_output,segment_id)
            # ##print(sp_data)
            relation = ['AvaSyakawApariNAma','vyaBicAra']
            if discourse and discourse in relation:
                POST_PROCESS_OUTPUT = add_discourse_elements(discourse,spkview_data,sp_data, POST_PROCESS_OUTPUT)
                print('add_discourse_elements:',POST_PROCESS_OUTPUT)
            else:
                for i in discourse_data:
                    if i and i.split(':')[1] not in relation and 'coref' not in i:
                        POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data,sp_data, POST_PROCESS_OUTPUT)
                        print('add_discourse_elements:',POST_PROCESS_OUTPUT)
                
        POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT,sentence_type)
        print('has_ques_mark:',POST_PROCESS_OUTPUT)
        # if 'BI_1' in spkview_data:
        POST_PROCESS_OUTPUT=extract_spkview_values(json_output,segment_id,POST_PROCESS_OUTPUT)
        print('extract_spkview_values:',POST_PROCESS_OUTPUT)
        for i in discourse_data:
            if 'AvaSyakawApariNAma' in i and 'nahIM' not in spkview_data:
                POST_PROCESS_OUTPUT = 'yaxi ' + POST_PROCESS_OUTPUT
                # break
            elif 'vyaBicAra' in i:
                POST_PROCESS_OUTPUT = 'yaxyapi ' + POST_PROCESS_OUTPUT
        masked_hindi_data=collect_hindi_output(POST_PROCESS_OUTPUT)
        print('hindi_data:',masked_hindi_data)
        return masked_hindi_data
    except Exception as e:
            # Return the last line of the error message
        return str(e).splitlines()[-1]
    
def hindi_genration(input_text):
    sentences=[]
    input_text = input_text.replace('</segment_id>', '</id>').replace('</sent_id>', '</id>')

    # Now split the text based on the common identifier </id>
    segments = input_text.strip().split('</id>')
    # Normalize newlines: replace multiple newlines with a single one
    # input_text_normalized = re.sub(r'\n+', '\n\n', input_text.strip())
    # Create a list of lists for each sentence block
    list_of_lists = []
    current_block = []

    for line in input_text:
        current_block.append(line)
        if line.strip() == '</id>':  # End of a block
            list_of_lists.append(current_block)
            current_block = []
    # Initialize lists to store segment outputs and segment IDs
    all_output = []
    segment_ids = []
    parser = USR_to_json(segments)  # Create an instance of SentenceParser
    parser.parse_input_text()  # Parse the input text
    json_output = parser.get_json_output()
    #print(json_output,'json otp')
    # Process each segment individually
    for segment in segments:
        # Skip empty segments
        if not segment.strip():
            continue
        
        # Split each segment into lines and remove any empty lines
        lines = segment.strip().splitlines()
        
        # Extract the first line (segment_id)
        segment_id = lines[0].strip()
        if "<segment_id=" in segment_id or "<sent_id=" in segment_id:  # Extract sentence id
            segment_id1 = segment_id.split('=')[1].strip('>')  # Extract everything after '=' and remove '>'
            ##print(segment_id1,'sgmntttttt')
            segment_ids.append(segment_id1)  # Store the segment ID
        
        # Extract the second line (sentence)
        sentence = lines[1].strip()
        # Initialize lists to store the columns
        words, indices, entities, extra_column1, extra_column2, extra_column3, extra_column4, extra_column5, extra_column6 = ([] for _ in range(9))
        
        # Process each line of the table data (ignore the first two and last lines)
        try:
            for line in lines[2:-1]:
                # Extract columns from the line
                columns = line.split()
                
                words.append(columns[0])  # word
                indices.append(columns[1])  # index
                entities.append(columns[2] if columns[2] != '-' else '')  # entity
                
                # Check each extra column and replace '-' with an empty string
                extra_column1.append(columns[3] if len(columns) > 3 and columns[3] != '-' else '')
                extra_column2.append(columns[4] if len(columns) > 4 and columns[4] != '-' else '')
                extra_column3.append(columns[5] if len(columns) > 5 and columns[5] != '-' else '')
                extra_column4.append(columns[6] if len(columns) > 6 and columns[6] != '-' else '')
                extra_column5.append(columns[7] if len(columns) > 7 and columns[7] != '-' else '')
                extra_column6.append(columns[8] if len(columns) > 8 and columns[8] != '-' else '')

            # Extract the last line (marker)
            last_line_marker = lines[-1].strip()

            # Create the output for this segment
            output = [
                sentence,
                ','.join(words),
                ','.join(indices),
                ','.join(entities),
                ','.join(extra_column1),
                ','.join(extra_column2),
                ','.join(extra_column3),
                ','.join(extra_column4),
                ','.join(extra_column5),
                ','.join(extra_column6),
                last_line_marker,
            ]

        except IndexError as e:
            #print(f"IndexError encountered: {e}")
            # Handle missing or incomplete columns gracefully
            output = ["Error: Missing or incomplete data in input lines"]

        # except Exception as e:
        #     #print(f"An unexpected error occurred: {e}")
        #     # Handle other unexpected errors
        #     output = ["Error: An unexpected error occurred while processing the lines"]

        # Add the result to the final output
        # ##print(output,'oppp')
        try:
            #print(segment_id1)
            print(output,'csv')
            output1=process_file_data(output,segment_id1,json_output)
            all_output.append(output1)
        except Exception as e:
            # Capture the last line of the error and append it to results
            all_output.append(f"Error processing {segment_id1}: {str(e).splitlines()[-1]}")
    # all_output=process_masked_multiple_sentences(all_output)
    # ##print(segment_ids)    # Return both the segment outputs and the segment IDs as separate lists
    # for segment_id, output in zip(segment_ids, all_output):
    last_output=process_sentence(segment_ids,sentences,all_output)
    #print(last_output)
    #print(global_starred_words, 'Global starred words with categories')
    
    return last_output


if __name__=='__main__':
    input_data = '''<sent_id= gold_data_155a>
#राम घर गया ।
rAma 1 per/male - 3:k1 - - - -
Gara_1 2 - - 3:k2p - - - -
jA_1-yA_1 3 - - 0:main - - - -
%affirmative
</sent_id>
'''
# Specify the file path
    # file_path = '/home/varshith/Downloads/hindi_generator_mask/updated/repository/health_usrs.txt'

    # # # Open the file in read mode
    # with open(file_path, 'r') as file:
    #     # Read the entire content of the file and store it in a string
    #     input_data = file.read()

    # #print the content
    # #print(str(file_content))

# अन्य आकाशीय #पिण्ड जैसी पृथ्वी का आकृति भी गोलाकार है।

# ["अन्य आकाशीय *पिण्ड जैसी पृथ्वी का आकृति भी गोलाकार है।"]
# ["यह जीवन के लिये हानिकारक/तीनों पराबैंगनी किरणें रोक और जीवन के लिये अनुकूल तापमान बनकर राख में सहायक है।"]

    hindi_genration(input_data)
