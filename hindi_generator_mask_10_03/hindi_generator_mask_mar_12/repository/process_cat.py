from repository.common_v4 import *
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def process_all_cat(categorized_words_list,index_data,gnp_data,seman_data,depend_data,spkview_data,sentence_type,words_info,k1_not_need,has_changes):

    # foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = identify_cat(
    #         words_info,sentence_type)
    foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = categorized_words_list
    
    processed_foreign_words = process_foreign_word(index_data,foreign_words_data,words_info,verbs_data)
    processed_indeclinables = process_indeclinables(indeclinables_data)
    processed_nouns = process_nouns(index_data,seman_data,nouns_data, words_info, verbs_data)
    # #print(processed_nouns)
    processed_pronouns = process_pronouns(index_data,pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
    processed_others = process_others(others_data)
    process_nominal_form = process_nominal_verb(index_data,nominal_forms_data, processed_nouns, words_info, verbs_data)
    processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data,processed_nouns, processed_pronouns,index_data, words_info,k1_not_need, False)
    # processed_adjectives = process_verbal_adjective(verbal_adjectives,processed_nouns, words_info, verbs_data)
    processed_adjectives = process_adjectives(adjectives_data,gnp_data,index_data, processed_nouns, processed_verbs)
    process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
    postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info)
    # Every word is collected into one and sorted by index number.
    processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
                                                processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)
    
    return processed_foreign_words,processed_indeclinables,processed_nouns,processed_pronouns,processed_others,process_nominal_form,processed_verbs, processed_auxverbs,processed_adjectives,processed_words


def process_change(rules_info,categorized_words_list,words_info,processed_nouns,processed_pronouns,processed_others,processed_foreign_words,processed_indeclinables):

    (src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, 
 discourse_data, spkview_data, scope_data, construction_data, sentence_type) = rules_info
    index_data = [int(x) for x in index_data]

    foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = categorized_words_list
    
    processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, words_info, True)
    processed_adjectives = process_adjectives(adjectives_data,gnp_data,index_data, processed_nouns, processed_verbs)
    process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)
    processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns, processed_nouns,  processed_adjectives, processed_verbs,processed_auxverbs,processed_indeclinables,processed_others)
    return processed_words


# def check_main_verb(depend_data):
    # flag=False
    # for dep in list(depend_data):
    #     if dep:
    #         dep1=dep.strip().split(':')[1]
    #         if dep1== 'main' or dep1=='rcelab' or dep1=='rcdelim':
    #             flag=True
    #             break
    # if flag==False:
    #     return(log('USR error. Main verb not identified. Check the USR.'))
        # sys.exit()
def get_main_verb(relation_head, verbs_data, flag, main_verb):
    """
    Process construction data based on relation_head and verbs_data.
    
    Parameters:
        relation_head (str): The head of the relation being processed.
        verbs_data (list): A list of verbs data, each represented as a list.
        flag (bool): A flag indicating if a matching verb has been found.
        main_verb (list): The main verb object to be updated.
    
    Returns:
        tuple: Updated main_verb and flag.
    """
    # Iterate through the verbs data
    for verb in verbs_data:
        # Check if the verbalizer matches the relation head
        # verbalizer_match = f"{relation_head}:verbalizer" == verb[8]
        if 'verbalizer' in verb[8] and verb[4] == '0:main':
            main_verb = verb
            flag = True
            break
        elif verb[4] == '0:main':
            main_verb = verb

        # Check if the relation_head matches verb[0] (as an integer)
        # elif int(relation_head) == verb[0]:
        #     main_verb = verb
        #     break
        # else:
        #     main_verb = verb
    
    # If no match is found, return the original main_verb and flag
    return main_verb, flag

def convert_to_devanagari(text):
    # Convert English text to Devanagari script
    devanagari_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    return devanagari_text

def process_foreign_word(index_data,foreign_words_data,words_info,verbs_data):
    # for verb in verbs_data:
    #    if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
    #         main_verb = verb
    #         break
    processed_foreign_words=[]
    flag=False
    for i,foreign_word in enumerate(foreign_words_data):
        index=foreign_word[0]
        gender, number, person, case = get_default_GNP()
        category='n'
        type=''
        main_verb = ''
        foreign_list = list(foreign_word)
        # for main verb
        relation_head = foreign_word[4].strip().split(':')[0]
        relation = foreign_word[4].strip().split(':')[1]
        # if int(relation_head) in index_data and relation=='k1':
        main_verb,flag=get_main_verb(relation_head,verbs_data,flag,main_verb)
        # for verb in verbs_data:
        #     # if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
        #     v = relation_head + ':verbalizer'
        #     if v == verb[8]:
        #         # id = construction_data.index(v)
        #         main_verb=verb
        #         break
        #     elif int(relation_head)==verb[0]:
        #         main_verb=verb
        #         break
        # else:
        #     main_verb=verb
        
        foreign_list[1] = foreign_list[1].replace('^','')
        # if '_' in foreign_list[1]:
        foreign_list[1]=clean(foreign_list[1])
        foreign_list[1]=convert_to_devanagari(foreign_list[1])
        # foreign_list[1]=convert_to_hindi(foreign_list[1])
        foreign_word = tuple(foreign_list)
        case,postposition = preprocess_postposition_new('noun', foreign_word, words_info, main_verb,index_data)
        # if flag:
        #     del processed_postpositions_dict[float(index)]
        processed_foreign_words.append((index,foreign_word[1],category,case,gender,number,person,type,postposition))
        
    return processed_foreign_words

def process_nominal_verb(index_data,nominal_verbs_data, processed_noun, words_info, verbs_data):

   nominal_verbs = []
   flag=False
#    for verb in verbs_data:
#        if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
#             main_verb = verb
#             break
    
   for nominal_verb in nominal_verbs_data:
        index = nominal_verb[0]
        term = clean(nominal_verb[1])
        gender = 'm'
        number = 's'
        person = 'a'
        # category = 'n'
        noun_type = 'common'
        case = 'o'
        postposition = ''
        main_verb=''

        log_msg = f'{term} identified as nominal, re-identified as other word and processed as common noun with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'

        relation = ''
        if nominal_verb[4] != '':
            relation = nominal_verb[4].strip().split(':')[1]

        relation_head = nominal_verb[4].strip().split(':')[0]
        # relation = nominal_verb[4].strip().split(':')[1]
        # if int(relation_head) in index_data and relation=='k1':
        main_verb,flag = get_main_verb(relation_head,verbs_data,flag,main_verb)

        case, postposition = preprocess_postposition_new('noun', nominal_verb, words_info, main_verb, index_data)
        # ##print(processed_postpositions_dict,index,flag,'klllll')
        # if flag:
        #     del processed_postpositions_dict[float(index)]
        # tags = find_tags_from_dix_as_list(term)
        # for tag in tags:
        #     if (tag[0] == 'cat' and tag[1] == 'v'):
        noun_type = 'vn'
        category='vn'
        if relation in ('k2', 'rt', 'rh','rblpk','rblak','rblsk'):
            term = term + 'nA'
            log_msg = f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'
            noun = (index, term, category, case, gender, number, person, noun_type, postposition)
            processed_noun.append(noun)
            log(log_msg)
            # break
        elif relation in ('k1'):
            case='d'
            term = term + 'nA'
            log_msg = f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'
            noun = (index, term, category, case, gender, number, person, noun_type, postposition)
            processed_noun.append(noun)
            log(log_msg)
            # break
        else:
            noun = (index, term, category, case, gender, number, person, noun_type, postposition)
            processed_noun.append(noun)
        # nominal_verbs.append(noun)
        
   return processed_noun

def process_adverb_as_noun(concept, processed_nouns):
    index, term, *_ = concept
    case = 'd' if ('+se_') not in term else 'o'
    term = clean(term.split('+')[0])
    category, gender, number, person, noun_type, postposition = 'n', 'm', 'p', 'a', 'abstract', 'se'
    processed_postpositions_dict[index] = postposition
    noun = (index, term, category, case, gender, number, person, noun_type, postposition)
    processed_nouns.append(noun)
    log(f' Adverb {term} processed as an abstract noun with index {index} gen:{gender} num:{number} case:{case},noun_type:{noun_type} and postposition:{postposition}')
    return

def process_adverb_as_verb(concept, processed_verbs):
    index, term, *_ = concept
    term = clean(term)
    gender, number, person, category, type, case = 'm', 's', 'a', 'v', 'adverb', 'd'
    tags = find_tags_from_dix_as_list(term)
    # ##print(tags,'tags5')
    for tag in tags:
        if tag['cat']== 'v':
            tam = 'kara'
            adverb = (index, term, category, gender, number, person, tam, case, type)
            processed_verbs.append(adverb)
            log(f'{term} adverb processed as a verb with index {index} gen:{gender} num:{number} person:{person}, and tam:{tam}')
            return

def process_adverbs(adverbs, processed_nouns, processed_verbs, processed_indeclinables, reprocessing):
    for adverb in adverbs:
        term = clean(adverb[1])
        if '+se_' in term or adverb[2] == 'abs':  # for adverbs like jora+se
            if not reprocessing:
                process_adverb_as_noun(adverb, processed_nouns)
        else:  # check morph tags
            tags = find_tags_from_dix_as_list(term)
            for tag in tags:
                if tag['cat'] == 'v':  # term type is verb in morph dix
                    return process_adverb_as_verb(adverb, processed_verbs)
                elif tag['cat'] == 'adj':  # term type is adjective in morph dix
                    term += 'rUpa_se'
                    new_entry = (adverb[0], term, 'indec')
                    if new_entry not in processed_indeclinables:
                        processed_indeclinables.append(new_entry)
                        log(f'adverb {adverb[1]} processed indeclinable with form {term}')
                    return
            else:
                for processed in processed_indeclinables:
                    if term == processed[1]:
                        log(f'adverb {adverb[1]} already processed indeclinable, no processing done')
                        return
                processed_indeclinables.append((adverb[0], term, 'indec'))  # to be updated, when cases arise.
                log(f'adverb {adverb[1]} processed indeclinable with form {term}, no processing done')
                return

def process_indeclinables(indeclinables):
    '''
    Functionality:
        1. They do not require any furthur processing
        2. Make a tuple with - index, term, type(indec)

    Parameters:
        indeclinables: List of indeclinable data

    Returns:
        list of tuples.

    for eg.     :
        indeclinables: [(2, 'Aja_1', '', '', '3:k7t', '', '', '')]

    Result:
       processed_indeclinables: [(2, 'Aja', 'indec')]
    '''

    processed_indeclinables = []
    for indec in indeclinables:
        clean_indec = clean(indec[1])
        processed_indeclinables.append((indec[0], clean_indec, 'indec'))
    return processed_indeclinables

def process_nouns(index_data,seman_data,nouns, words_info, verbs_data):
    '''
    Functionality:
        1. Make a noun tuple
        2. We update update_additional_words_dict(index, 'before', 'eka'), if number == 's' and noun[6] == 'some'

    Parameters:
        1. nouns - List of noun data
        2. words_info - List of USR info word wise
        3. verbs_data - List of verbs data

    Returns:
        processed_nouns = List of noun tuples where each tuple looks like - (index, word, category, case, gender, number, proper/noun type= proper, common, NC, nominal_verb, CP_noun or digit, postposition)

    For eg.:
        rAma,xo_1,rotI_1,xAla_1,KA_1-yA_1
        1,2,3,4,5,6
        male per,,,,
        sg,,sg,sg,
        6:k1,3:card,6:k2,6:k2,0:main
        ,,,,,
        ,,,,,
        ,,,,,
        affirmative
        conj:[3,4]

        nouns     : [(1, 'rAma', 'male per', 'sg', '6:k1', '', '', ''), (3, 'rotI_1', '', 'sg', '6:k2', '', '', ''), (4, 'xAla_1', '', 'sg', '6:k2', '', '', '')]
        words_info     : [(1, 'rAma', 'male per', 'sg', '6:k1', '', '', ''), (2, 'xo_1', '', '', '3:card', '', '', ''), (3, 'rotI_1', '', 'sg', '6:k2', '', '', ''), (4, 'xAla_1', '', 'sg', '6:k2', '', '', ''), (5, 'KA_1-yA_1', '', '', '0:main', '', '', '')]
        verbs_data     : [(5, 'KA_1-yA_1', '', '', '0:main', '', '', '')]

    Result:
        processed_nouns     : [(1, 'rAma', 'n', 'o', 'm', 's', 'a', 'proper', 'ne'), (3, 'rotI', 'n', 'd', 'f', 's', 'a', 'common', None), (4, 'xAla', 'n', 'd', 'f', 's', 'a', 'common', None)]
    '''

    processed_nouns = []
    main_verb = ''
    flag=False
    # for verb in verbs_data:
    #     if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
    #         main_verb = verb
    #         ##print(main_verb,'vbb')
            # break
    # if not len(main_verb):
    #     log('USR error. Main verb not identified. Check the USR.')
    #     sys.exit()
        # return None

    for noun in nouns:
        category = 'n'
        index = noun[0]
        # dependency = noun[4].strip().split(':')[1]
        gender, number, person = extract_gnp_noun(noun)
        # ##print(noun)
        relation_head = noun[4].strip().split(':')[0]
        # relation = noun[4].strip().split(':')[1]
        # if int(relation_head) in index_data and relation=='k1':
        
        main_verb,flag = get_main_verb(relation_head,verbs_data,flag,main_verb)
        

        if noun[6] == 'respect': # respect for nouns
            number = 'p'
        noun_type = 'common' if '_' in noun[1] else 'proper'

        # if 'kriyAmUla' in noun[8]:
        if clean(noun[8]) in ('start','end','whole','kriyAmUla','mod','count','avayavI'):
            case='d'
            postposition=None
        else:
            case, postposition = preprocess_postposition_new('noun', noun, words_info, main_verb, index_data)

        if '+' in noun[1]:
            processed_nouns = handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition)

        else:
            term = noun[1]
            if check_is_digit(term):
                if '_' in term:
                    clean_noun = term.strip().split('_')[0]
                else:
                    clean_noun = term
                noun_type = 'digit'
            else:
                clean_noun = clean(noun[1])

            if 'era' == noun[2]:
                clean_noun = clean_noun.replace('00','')
                clean_noun=clean_noun +'_vIM_saxI'
            # print(seman_data)
            # print(noun[2],'iiii')
            # if 'mod' in noun[8]:
            #     postposition=None
            #     processed_postpositions_dict[index] = postposition
            #     case='d'

            if any(condition for condition in [
                ('era' in seman_data and noun[2] in ('dom', 'moy', 'yoc')),
                ('yoc' in seman_data and noun[2] in ('dom', 'moy')),
                ('moy' in seman_data and noun[2] == 'dom')
            ]):
                postposition = None
                processed_postpositions_dict[index] = postposition
                case = 'd'
            elif all(item not in seman_data for item in ('era', 'moy', 'yoc')) and noun[2] == 'dom':
                clean_noun = clean_noun+ '_wArIKa'
            if noun[2]=='clocktime':
                clean_noun = clean_noun + '_baje'
            
            if clean(noun[1]) in repository.constant.construction_list:
                postposition=None
                if index in processed_postpositions_dict:
                    del processed_postpositions_dict[index]
                
            processed_nouns.append((noun[0], clean_noun, category, case, gender, number, person, noun_type, postposition))
        log(f'{noun[1]} processed as noun with case:{case} gen:{gender} num:{number} noun_type:{noun_type} postposition: {postposition}.')
    return processed_nouns

def process_pronouns(index_data,pronouns, processed_nouns, processed_indeclinables, words_info, verbs_data):
    '''
        Functionality:
            1. Make a pronoun tuple
            2. If the term is kim, there is separate handling
            3. If term is yahAz or vahAz along with discourse data as 'emphasis' we convert it to yahIM, vahIM and treat them as indeclinables which do not require furthur processing
            4. If dependency is r6, then use the dependency_head to fetch the related noun data, and pick fnum, gender and case of this pronoun term same as related noun.
            5. Except for r6 relation, fnum is by default None

        Parameters:
            1. pronouns - List of pronoun data
            2. processed_nouns - List of processed noun data
            3. processed_indeclinables - List of processed indeclinable data
            2. words_info - List of USR info word wise
            3. verbs_data - List of verbs data

        Returns:
            processed_pronouns = List of pronoun tuples where each tuple looks like - (index, word, category, case, gender, number, person, parsarg, fnum)

        For eg.:
            yaha_1,aBiprAya_8,yaha_1,hE_1-pres
            1,2,3,4
            ,,,
            ,,sg,
            2:r6,4:k1,4:k1s,0:main
            ,,Geo_ncert_6stnd_4ch_0031d:coref,
            ,,,
            ,,,
            affirmative

            pronouns     : [(1, 'yaha_1', '', '', '2:r6', '', '', ''), (3, 'yaha_1', '', 'sg', '4:k1s', 'Geo_ncert_6stnd_4ch_0031d:coref', '', '')]
            words_info     : [(1, 'yaha_1', '', '', '2:r6', '', '', ''), (2, 'aBiprAya_8', '', '', '4:k1', '', '', ''), (3, 'yaha_1', '', 'sg', '4:k1s', 'Geo_ncert_6stnd_4ch_0031d:coref', '', ''), (4, 'hE_1-pres', '', '', '0:main', '', '', '')]
            verbs_data     : [(4, 'hE_1-pres', '', '', '0:main', '', '', '')]

        Result:
            processed_nouns     : [(1, 'yaha', 'p', 'd', 'm', 's', 'a', 'kA', 's'), (3, 'yaha', 'p', 'd', 'm', 's', 'a', 0, None)]
        '''

    processed_pronouns = []
    flag=False
    # for verb in verbs_data:
    #     if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
    #         main_verb = verb
    #         break

    for pronoun in pronouns:
        index = pronoun[0]
        main_verb=''
        term = clean(pronoun[1])
        anim = pronoun[2]
        gnp = pronoun[3]
        relation_head = pronoun[4].strip().split(':')[0]
        relation = pronoun[4].strip().split(':')[1]
        spkview_data = pronoun[6]
        main_verb,flag=get_main_verb(relation_head,verbs_data,flag,main_verb)
        
        if is_kim(term):
            gender, number, person, case = get_default_GNP()
            
            # gender, number, person = extract_gnp(pronoun)
            processed_pronouns, processed_indeclinables = process_kim(index, index_data, relation, anim, gnp,case, pronoun, words_info,
                                                                      main_verb, processed_pronouns, processed_indeclinables, processed_nouns)
        elif is_yax(term):
            gender, number, person, case = get_default_GNP()
            processed_pronouns, processed_indeclinables = process_yax(index, index_data, relation, anim, gnp,case, pronoun, words_info,
                                                                      main_verb, processed_pronouns, processed_indeclinables, processed_nouns)

        else:
            category = 'p'
            case = 'o'
            parsarg = 0

            if term in ['yahAz', 'vahAz'] and spkview_data == 'emphasis':
                term = term.replace('Az', 'IM')
                category = 'indec'
                processed_indeclinables.append((index, term, category))
                break

            case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb, index_data)
            
            if postposition != '':
                parsarg = postposition

            fnum = None
            gender, number, person = extract_gnp(pronoun)
            # ##print(gender,'ggg')
            if term == 'addressee':
                addr_map = {'respect': 'Apa', 'informal': 'wU', '': 'wU'}
                pronoun_per = {'respect': 'm', 'informal': 'm', '': 'm_h1'}
                pronoun_number = {'respect': 'p', 'informal': 's', '': 'p'}
                word = addr_map.get(spkview_data.strip().lower(), 'wU')
                person = pronoun_per.get(spkview_data.strip().lower(), 'm_h1')
                number = pronoun_number.get(spkview_data.strip(), 'p')
            elif term == 'speaker':
                # ##print(number,'ggg')
                word = 'mEM'
            elif term == 'wyax':
                # nn_data = is_next_word_noun(index+1, processed_nouns)
                if '/' in spkview_data:
                    spkview_data = spkview_data.split('/')[0]
                if spkview_data=="proximal" and relation=='k2p':
                    word='yahAz'
                elif spkview_data=="proximal" and relation=='k7p':
                    word='yahAz'
                elif spkview_data=='distal' and relation=='k7p':
                    word='vahAz'
                elif spkview_data=="proximal" and relation=='k7t':
                    word='aba'
                elif spkview_data=='distal' and relation=='k7t':
                    word='waba'
                # if spkview_data == "proximal" and relation=='dem':
                #     word = 'ye'
                #     case='o'
                elif spkview_data == "proximal" and relation=='dem':
                    fnoun = int(relation_head)
                    fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
                    if fnoun_data:
                        case = fnoun_data[3]
                    word = 'yaha'
                    # case='o' #changed for 10a example
                # elif spkview_data == "distal" and relation=='dem':
                #     word = 've'
                #     case='o'
                elif spkview_data == "distal" and relation=='dem':
                    fnoun = int(relation_head)
                    fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
                    if fnoun_data:
                        case = fnoun_data[3]
                        number = fnoun_data[5]
                    word = 'vaha'
                    # case='o'
                elif spkview_data == "distal" and number=='s':
                    word = 'vaha'
                elif spkview_data == "distal" and number=='p':
                    word='vaha'
                elif spkview_data == "proximal":
                    word = 'yaha'
                # elif spkview_data == "proximal" :
                #     word = 'yaha'
                else:
                    word = term
            
            else:
                word = term

            if relation == "r6":
                fnoun = int(relation_head)
                fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
                if fnoun_data:
                    gender = fnoun_data[4]  # To-ask
                    # fnum = number = fnoun_data[5]
                    fnum = fnoun_data[5]
                    case = fnoun_data[3]
                if term == 'apanA':
                    parsarg = '0'
            # ##print(word,)
            # if flag:
            #     del processed_postpositions_dict[float(index)]
            processed_pronouns.append((index, word, category, case, gender, number, person, parsarg, fnum))
            log(f'{term} processed as pronoun with case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    return processed_pronouns

def process_others(other_words):
    '''Process other words. Right now being processed as noun with default gnp'''
    processed_others = []
    for word in other_words:
        gender = 'm'
        number = 's'
        person = 'a'
        processed_others.append((word[0], clean(word[1]), 'other', gender, number, person))
    return processed_others

def process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, words_info,k1_not_need, reprocess=False):
    '''
    Functionality:
        1. In the list of verbs data, identify
            a) if it is complex predicate - it is appended in processed_nouns
            b) if verb_type == 'nonfinite': - process the concept and append in processed_verbs
            c) otherwise process main verb and auxilliary verbs and append in respective lists
    Parameters:
         verbs_data: List of verbs data
         seman_data: Semantic data row of USR
         depend_data: Dependency data row of USR
         sentence_type: Sentence type
         spkview_data: Speaker's view data row of USR
         processed_nouns: List of processed_nouns
         processed_pronouns: List of processed_pronouns
         words_info: List of USR info word wise
         reprocess: for first time processing, it is False. In case of changes, it is made True and sent as parameter
        :Returns:
        List of processed_verbs and processed_auxverbs
    '''
    processed_verbs = []
    processed_auxverbs = []
    # ##print(words_info,'words info')
    for concept in verbs_data:

        concept = Concept(index=concept[0], term=concept[1], dependency=concept[4])
        verb_type = identify_verb_type(concept)
        if verb_type == 'nonfinite':
            verb = process_nonfinite_verb(concept, seman_data, gnp_data,depend_data, sentence_type, processed_nouns, processed_pronouns,index_data, words_info,k1_not_need)
            processed_verbs.append(to_tuple(verb))
        else:
            # if process_verb(concept, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocess):
            verb, aux_verbs = process_verb(concept, seman_data, gnp_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, reprocess,k1_not_need)
            processed_verbs.append(to_tuple(verb))
            log(f'{verb.term} processed as main verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
            processed_auxverbs.extend([to_tuple(aux_verb) for aux_verb in aux_verbs])
    return processed_verbs, processed_auxverbs

def process_auxiliary_verbs(verb: Verb, index_data, concept, spkview_data,sentence_type) -> [Verb]:
    """
    >>> [to_tuple(aux) for aux in process_auxiliary_verbs(Verb(index=4, term = 'kara', gender='m', number='s', person='a', tam='hE', type= 'auxiliary'), concept_term='kara_17-0_sakawA_hE_1')]
    [(4.1, 'saka', 'v', 'm', 's', 'a', 'wA', 'auxiliary'), (4.2, 'hE', 'v', 'm', 's', 'a', 'hE',''auxiliary'')]
    """
    concept_term = concept.term
    concept_index = concept.index
    HAS_SHADE_DATA = False
    auxiliary_term_tam = []
    auxiliary_verb_terms = ''
    for i,data in enumerate(spkview_data):
        # shade_index = 1
        if data != '':
            data = data.strip().strip('][')
            if 'shade' in data and concept_index == index_data[i]:
                term = clean(data.split(':')[1])
                tam = identify_default_tam_for_main_verb(concept_term)
                HAS_SHADE_DATA = True
                break
        # shade_index = shade_index + 1
    # ind1=index_data.index(concept_index)
    # if 'shade' in spkview_data[ind1]:
    #     data1 = spkview_data[concept_index].strip().strip('][')
    #     term = clean(data1.split(':')[1])
    #     tam = identify_default_tam_for_main_verb(concept_term)
    #     HAS_SHADE_DATA = True

    if HAS_SHADE_DATA:
        if term == 'jA' and tam == 'yA':
            tam = 'yA1'   # to generate gayA from jA-yA
        # else:
        temp = (term, tam)
        auxiliary_term_tam.append(temp)
        # ##print(auxiliary_term_tam,'auxxxx')
        verb = set_main_verb_tam_zero(verb)
    if sentence_type[1:] not in ("fragment","title","heading","term") and '-' in concept_term:
        auxiliary_verb_terms = identify_auxiliary_verb_terms(concept_term)
    if len(auxiliary_verb_terms)>2 and 'pass' in sentence_type and auxiliary_verb_terms[1] not in repository.constant.aux_exception_case:
        ''' verb is in below cases
           1. pA-yA_jA_wA_hE
           2. pA-yA_jA_yA_hE
        '''
        combined = auxiliary_verb_terms[0] + auxiliary_verb_terms[1]
        auxiliary_verb_terms = [combined] + auxiliary_verb_terms[2:]

    for v in auxiliary_verb_terms:
        term, tam = auxmap_hin(v)
        temp = (term, tam)
        auxiliary_term_tam.append(temp)

    return [create_auxiliary_verb(index, pair[0], pair[1], verb) for index, pair in enumerate(auxiliary_term_tam)]

def process_dep_rbks(concept, words_info, processed_nouns, processed_pronouns):
    finalData = []
    k1_exists, k1_index = find_match_with_same_head(concept.index, 'k1', words_info, index=4)
    k3_exists, k3_index = find_match_with_same_head(concept.index, 'k3', words_info, index=4)
    if k1_exists:
        case = 'o'
        ppost = 'ke xvArA'

        for i in range(len(processed_nouns)):
            data = processed_nouns[i]
            data_index = data[0]
            if data_index == k1_index:
                temp = list(data)
                temp[3] = case
                temp[8] = ppost
                processed_nouns[i] = tuple(temp)
                update_ppost_dict(data_index, ppost)

    elif k3_exists:
        case = 'o'
        ppost = 'ke xvArA'

        for i in range(len(processed_nouns)):
            data = processed_nouns[i]
            data_index = data[0]
            if data_index == k3_index:
                temp = list(data)
                temp[3] = case
                temp[8] = ppost
                processed_nouns[i] = tuple(temp)
                update_ppost_dict(data_index, ppost)

def process_verb(concept: Concept, seman_data, gnp_data, dependency_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, reprocessing,k1_not_need):
    """
    concept pattern: 'main_verb' - 'TAM for main verb' _Aux_verb+tam...
    Example 1:
    kara_1-wA_hE_1
    main verb - kara,  main verb tam: wA, Aux -hE with TAM hE (identified from tam mapping file)

    Example 2:
    kara_1-yA_1
    main verb - kara,  main verb tam: yA,

    Example 3:
    kara_1-0_rahA_hE_1
    main verb - kara,  main verb tam: 0, Aux verb -rahA with TAM hE, Aux -hE with TAM hE (identified from tam mapping file)

    Example 4:
    kara_1-0_sakawA_hE_1
    main verb - kara,  main verb tam: 0, Aux verb -saka with TAM wA, Aux -hE with TAM hE (identified from tam mapping file)

    *Aux root and Aux TAM identified from auxiliary mapping File
    """
    # if process_main_verb(concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns, reprocessing):
    verb = process_main_verb(concept, seman_data, gnp_data, dependency_data, sentence_type, processed_nouns, processed_pronouns,index_data, reprocessing,k1_not_need)
    auxiliary_verbs = process_auxiliary_verbs(verb,index_data, concept, spkview_data,sentence_type)
    return verb, auxiliary_verbs
    # else:
    #     return None

def process_nonfinite_verb(concept, seman_data,gnp_data, depend_data, sentence_type, processed_nouns, processed_pronouns,index_data, words_info,k1_not_need):
    '''
    >>process_nonfinite_verb([], [()],[()])
    '''
    gender = 'm'
    number = 's'
    person = 'a'
    verb = Verb()
    verb.index = concept.index
    # is_cp = is_CP(concept.term)
    # if is_cp: #only CP_head as nonfinite verb
    #     draft_concept = concept.term.split('+')[1]
    #     verb.term  = clean(draft_concept)
    # else:
    verb.term = clean(concept.term)
    ind=index_data.index(verb.index)
    verb.type = 'nonfinite'
    verb.tam = ''
    relation = concept.dependency.strip().split(':')[1]
    if relation == 'rbks':
        process_dep_rbks(concept, words_info, processed_nouns, processed_pronouns)
    if 'causative' in gnp_data[ind] and verb.term[-1]=='a':
        verb.term = verb.term[:-1] + 'A'

    verb.tam = set_tam_for_nonfinite(relation)
    full_tam = verb.tam
    # if getVerbGNP_new(verb.term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns):
    gender, number, person = getVerbGNP_new(verb.term, full_tam,verb.index, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns,index_data,k1_not_need)
    verb.gender = gender
    verb.number = number
    verb.person = person
    verb.case = 'o' # to be updated - agreement with following noun
    log(f'{verb.term} processed as nonfinite verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
    return verb
    # else:
    #     return None

def process_main_verb(concept: Concept, seman_data, gnp_data, dependency_data, sentence_type, processed_nouns, processed_pronouns,index_data, reprocessing,k1_not_need):
    """
    >>> to_tuple(process_main_verb(Concept(index=2, term='varRA+ho_1-gA_1', dependency='0:main'), ['2:k7t', '0:main'], [(1, 'kala', 'n', 'o', 'm', 's', 'a', 'common', None)], [], False))
    [OK]     : varRA processed as noun with index 1.9 case:d gen:f num:s per:a, noun_type:CP_noun, default postposition:None.
    (2, 'ho', 'v', 'f', 's', 'a', 'gA')
    >>> to_tuple(process_main_verb(Concept(index=2, term='varRA+ho_1-gA_1', dependency='0:main'), ['2:k7t', '0:main'], [(1, 'kala', 'n', 'o', 'm', 's', 'a', 'common', None)], [], True))
    [OK]     : ho reprocessed as verb with index 2 gen:f num:s per:a in agreement with CP
    (2, 'ho', 'v', 'f', 's', 'a', 'gA')
    >>>
    """
    verb = Verb()
    verb.type = "main"
    verb.index = concept.index
    verb.term = identify_main_verb(concept.term)
    full_tam=''
    # ##print(verb.term,gnp_data,'vtt')
    if sentence_type[1:] not in ("fragment","title","heading","term"):

        full_tam = identify_complete_tam_for_verb(concept.term)
        verb.tam = identify_default_tam_for_main_verb(concept.term)
        if verb.term == 'hE' and verb.tam in ('pres', 'past'):  # process TAM
            alt_tam = {'pres': 'hE', 'past': 'WA'}
            alt_root = {'pres': 'hE', 'past': 'WA'}
            verb.term = alt_root[verb.tam]  # handling past tense by passing correct root WA
            verb.tam = alt_tam[verb.tam]
        if verb.term == 'jA' and verb.tam == 'yA':
            verb.tam = 'yA1'
        # ##print(index_data)
        ind=index_data.index(verb.index)

        if gnp_data[ind] in ('causative','doublecausative'):
            verb.term=identify_causative(verb.term,gnp_data,ind)
    # else:

    # is_cp = is_CP(concept.term)
    # if getVerbGNP_new(concept.term, full_tam, is_cp, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns):
    verb.gender, verb.number, verb.person = getVerbGNP_new(concept.term, full_tam,verb.index, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns,index_data,k1_not_need)
    return verb
    # else:
    #     return None
def identify_causative(verb,gnp_data,ind):
    with open(repository.constant.CAUSATIVE_MAP_FILE, 'r') as file:
        for line in file.readlines():
            # ##print(line,'lll')
            causative_mapping = line.strip().split(',')
            if causative_mapping[0] == verb and causative_mapping[1]==gnp_data[ind]:
                return causative_mapping[2]
            # else:

    # log(f'"{aux_verb}" not found in auxiliary mapping.', 'WARNING')

def create_auxiliary_verb(index, term, tam, main_verb: Verb):
    verb = Verb()
    verb.index = main_verb.index + (index + 1)/10
    verb.gender, verb.number, verb.person = main_verb.gender, main_verb.number, main_verb.person
    verb.term = term
    verb.tam = tam
    if verb.term == 'cAha':
        verb.person = 'm_h'
    verb.type = 'auxiliary'
    log(f'{verb.term} processed as auxiliary verb with index {verb.index} gen:{verb.gender} num:{verb.number} and tam:{verb.tam}')
    return verb

def process_adjectives(adjectives, gnp_data1, index_data, processed_nouns, processed_verbs):
    """
    Process adjectives as tuples with grammatical attributes.

    Args:
        adjectives (list): List of adjectives as tuples (index, word, category, case, gender, number, relation).
        gnp_data1 (list): GNP-related data.
        index_data (list): Index mapping data.
        processed_nouns (list): Processed noun data.
        processed_verbs (list): Processed verb data.

    Returns:
        list: Processed adjectives with updated attributes.
    """
    processed_adjectives = []
    default_gender, default_number, default_person, default_case = get_default_GNP()

    # Determine the index of 'kqwpft' if it exists
    ind_kqwpft = gnp_data1.index('kqwpft') if 'kqwpft' in gnp_data1 else None

    for adjective in adjectives:
        index = adjective[0]
        adj = clean(adjective[1])
        category = 'adj'
        tam = ''
        rel_concept = int(adjective[4].strip().split(':')[0])  # Related noun/verb
        relation = adjective[4].strip().split(':')[1]

        # Determine associated concept data based on relation type
        if relation == 'k1s':
            if adj == 'kim':
                adj = 'kEsA'
            rel_concept_data = getDataByIndex(rel_concept, processed_verbs)
        else:
            rel_concept_data = getDataByIndex(rel_concept, processed_nouns)

        # Extract GNP case attributes
        if not rel_concept_data:
            log(f'Associated noun/verb not found for adjective {adjective[1]}. Using default values.')
            gender, number, person, case = default_gender, default_number, default_person, default_case
        else:
            gender, number, person, case = get_gnpcase_from_concept(rel_concept_data)
            if relation == 'k1s':
                case = 'd'

        # Special case for 'kim' with 'krvn' relation
        if adj == 'kim' and relation == 'krvn':
            adj = 'kEsA'

        # Find tags and process based on category
        tags = find_tags_from_dix_as_list(adj)
        for tag in tags:
            if tag['cat'] == 'v':
                if relation in ('rvks', 'rbks'):
                    category = 'vj'
                    tam = 'adj_yA_huA' if relation == 'rbks' else 'adj_wA_huA'
                if ind_kqwpft is not None and index == index_data[ind_kqwpft]:
                    category = 'vj'
                    tam = 'adj_yA_huA'
                break

        # Append processed adjective with or without TAM
        if tam:
            adjective = (index, adj, category, case, gender, number, tam)
            processed_adjectives.append(adjective)
            log(f'{adjective[1]} processed as adjective with case:{case}, gender:{gender}, number:{number}, tam:{tam}')
        else:
            adjective = (index, adj, category, case, gender, number)
            processed_adjectives.append(adjective)
            log(f'{adjective[1]} processed as adjective with case:{case}, gender:{gender}, number:{number}')

    return processed_adjectives


def process_kim(index, index_data, relation, anim, gnp,case, pronoun, words_info, main_verb, processed_pronouns, processed_indeclinables, processed_nouns):

    term = get_root_for_kim(relation, anim,gnp,case,)
    if term == 'kyoM':
        processed_indeclinables.append((index, term, 'indec'))
    else:
        category = 'p'
        case = 'o'
        parsarg = 0
        case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb, index_data)
        if postposition != '':
            parsarg = postposition

        fnum = None
        gender, number, person = extract_gnp(pronoun)

        if "r6" in pronoun[4]:
            fnoun = int(pronoun[4][0])
            fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
            gender = fnoun_data[4]  # To-ask
            fnum = number = fnoun_data[5]
            case = fnoun_data[3]
            if term == 'apanA':
                parsarg = '0'

        if term in ('kahAz'):
            parsarg = 0
        processed_pronouns.append((pronoun[0], term, category, case, gender, number, person, parsarg, fnum))
        log(f'kim processed as pronoun with term: {term} case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    return processed_pronouns, processed_indeclinables

def get_root_for_kim(relation, anim, gnp,case):
    # kOna is root for - kisakA, kisakI, kisake, kinakA, kinake, kinakI, kOna, kisa, kisane, kise, kisako,
    # kisase, kisake, kisameM, kisameM_se, isapara, kina, inhoMne, kinheM, kinako, kinase, kinpara, kinake, kinameM, kinameM_se, kisI, kisa
    # if gnp=='pl':
    #     number='p'
    # else:
    #     number='s'
    animate = ['anim', 'per']
    if relation in ('k2p', 'k7p'):
        return 'kahAz'
    elif relation == 'k5' :
        return 'kahAz'
    elif relation == 'k7t':
        return 'kaba'
    elif relation == 'rh' :
        return 'kyoM'
    elif relation == 'rt' : #generate kisa
        return 'kOna'
    elif relation == 'krvn': #generate kEse
        return 'kEsA'
    elif relation == 'k1s':
        return 'kEsA'
    elif relation=='dem' and gnp=='' and case=='o':
        return 'kis'
    elif relation=='dem' and gnp=='pl' and case=='o':
        return 'kin'
    elif anim not in animate:
        return 'kyA'
    elif anim in animate:
        return 'kOna'
    elif relation =='k1' or relation =='k2':
        return 'kyA'
    else:
        return 'kim'

def process_yax(index1, index_data, relation, anim, gnp,case, pronoun, words_info, main_verb, processed_pronouns, processed_indeclinables, processed_nouns):
                
    term = get_root_for_yax(relation, anim,gnp,case,)
    # if term == 'kyoM':
    #     processed_indeclinables.append((index, term, 'indec'))
    # else:
    category = 'p'
    case = 'o'
    parsarg = 0
    case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb, index_data)
    if postposition != '':
        parsarg = postposition

    fnum = None
    gender, number, person = extract_gnp(pronoun)

    if "r6" in pronoun[4]:
        fnoun = int(pronoun[4][0])
        fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
        gender = fnoun_data[4]  # To-ask
        fnum = number = fnoun_data[5]
        case = fnoun_data[3]
        if term == 'apanA':
            parsarg = '0'

    if term in ('jahAz'):
        parsarg = 0
    processed_pronouns.append((pronoun[0], term, category, case, gender, number, person, parsarg, fnum))
    log(f'yax processed as pronoun with term: {term} case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    return processed_pronouns, processed_indeclinables

def get_root_for_yax(relation, anim, gnp,case):
    # kOna is root for - kisakA, kisakI, kisake, kinakA, kinake, kinakI, kOna, kisa, kisane, kise, kisako,
    # kisase, kisake, kisameM, kisameM_se, isapara, kina, inhoMne, kinheM, kinako, kinase, kinpara, kinake, kinameM, kinameM_se, kisI, kisa
    # if gnp=='pl':
    #     number='p'
    # else:
    #     number='s'
    animate = ['anim', 'per']
    if relation in ('k2p', 'k7p'):
        return 'jahAz'
    elif relation == 'k5' :
        return 'jahAz'
    elif relation == 'k7t':
        return 'jaba'
    # elif relation == 'rh' :
    #     return 'kyoM'
    elif relation == 'rt' : #generate kisa
        return 'jo'
    # elif relation == 'krvn': #generate kEse
    #     return 'kEsA'
    # elif relation == 'k1s':
    #     return 'kEsA'
    elif relation=='dem' and gnp=='' and case=='o':
        return 'jisa'
    elif relation=='dem' and gnp=='pl' and case=='o':
        return 'jina'
    elif anim not in animate:
        return 'jo'
    elif anim in animate:
        return 'jo'
    elif relation =='k1' or relation =='k2':
        return 'jo'
    else:
        return 'jo'