HAS_CONSTRUCTION_DATA = False
HAS_SPKVIEW_DATA = False
HAS_MORPHO_SEMANTIC_DATA = False
HAS_DISCOURSE_DATA = False
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
has_changes = False
flag_temporal_spatial = False

# TAM_DICT_FILE = 'tam_mapping.dat'
TAM_DICT_FILE = './repository/tam_mapping_new.dat'
AUX_MAP_FILE = './repository/auxillary_mapping.txt'
CAUSATIVE_MAP_FILE='./repository/causative_mapping.txt'

# data lists
INDECLINABLE_WORDS = [
        'eKana','waWA','Ara','paranwu','kinwu','evaM','waWApi','kiCu',
        'wo','yaxi','wabe','awaH','kAraNa','kenanA','yeBAbe',
        'waKana','waKani','bA', 'nAhale','anyaWA', 'yaKana', 'naile',
        'yAwe','yaxi', 'aWabA','Aja','nA', 'yawa', 'wawa', 'yA','nahIM',]

UNITS = ['semI', 'kimI', 'mItara', 'lItara', 'kilomItara', 'kilolItara']

kriyAmUla=['viswqwa','prawIkRA','varNana']

# NON_FINITE_VERB_DEPENDENCY = ['rpk', 'rsk','rbk', 'rvks', 'rbks', 'rblpk', 'rblsk']
NON_FINITE_VERB_DEPENDENCY = ['rpk', 'rsk','rbk']
ADJECTIVE_DEPENDENCY = ['card', 'mod','meas', 'ord', 'intf','rvks','rbks']
# VERBAL_ADJECTIVE = ['rvks','rbks']
PRONOUN_TERMS = ['addressee', 'speaker', 'kyA', 'Apa','wyax', 'jo', 'koI', 'kOna', 'mEM','merA', 'saba', 'vaha', 'wU', 'wuma', 'yaha', 'kim','ve','ye','yax']
# NOMINAL_VERB_DEPENDENCY = ['rt', 'rh', 'k7p', 'k7t', 'k2']
NOMINAL_VERB_DEPENDENCY = ['rt', 'rh', 'k7p','k7', 'k7t', 'k2','rblpk','rblsk','rblak','k1s']
# constants.py
# pass_list=['pass-affirmative','pass-interrogative','pass-negative sentence']
pass_list=['pass-affirmative','pass-interrogative','pass-negative']
k7_postposition_list=['पर', 'को', 'में']
noun_attribute = dict()
USR_row_info = [
    'root_words', 'index_data', 'seman_data', 'gnp_data', 'depend_data',
    'discourse_data', 'spkview_data', 'scope_data'
]
nA_list = [
    'nA_paDa', 'nA_padZA', 'nA_padA', 'nA_hE', 'nA_WA', 'nA_hogA', 'nA_cAhie',
    'nA_cAhiye','cAhiye'
]

morpho_seman = ['compermore','comperless','comper_more', 'comper-more', 'comper_less', 'comper-less', 'superl', 'mawupa', 'mawup','dviwva']

spkview_list_b = [
    'jI', 'lagAwAra', 'kevala' ,'karIba','TIka','mAwra','basa','sirPa',
]
spkview_list_a = [
    'hI', 'BI', 'jI', 'wo','sI','ki','waka', 'lagaBaga', 'lagAwAra'
]
kisase_k2g_verbs = ['bola', 'pUCa', 'kaha', 'nikAla', 'mAzga']
reciprocal_verbs = ['mila', 'pyAra']
kisase_k5_verbs = ['dara', 'baca', 'rakSA']
kahAz_k5_verbs = ['A', 'uga', 'gira']

discourse_dict = {
    'samuccaya': ['Ora', 'evaM', 'waWA'],
    'AvaSyakawApariNAma': 'wo',
    'kAryakAraNa': ['kyoMki', 'cUzki', 'cUMki'],
    'pariNAma': ['isIlie', 'isalie', 'awaH', 'isake pariNAmasvarUpa', 'isI kAraNa', 'isa kAraNa'],
    'viroXI_xyowaka': 'jabaki',
    'vyaBicAra': ['waWApi', 'hAlAzki', 'Pira BI','isake bAvajZUxa'],
    'viroXI': ['lekina', 'kiMwu', 'paraMwu', 'isake viparIwa', 'viparIwa'],
    'anyawra': ['yA', 'aWavA'],
    'samuccaya x': ['isake alAvA', 'isake awirikwa', 'isake sAWa-sAWa', 'isake sAWa sAWa'],
    'arWAwa':['arWAwa','xUsre SabxoM meM'],
    'uwwarakAla':['bAxa meM', 'isake bAxa meM'],
    'kAryaxyowaka':'wAki',
    'uxaharaNasvarUpa':'uxAharaNa ke lie',
}

spkview_list = ['BI_1', 'samAveSI', 'alAvA', 'awirikwa']
discourse_list = ['samuccaya', 'AvaSyakawApariNAma', 'kAryakAraNa', 'pariNAma', 'viroXIxyowaka', 'vyaBicAra', 
                  'viroXI', 'anyawra', 'samuccaya x', 'arWAwa', 'uwwarkAla', 'kAryaxyowaka', 'uxaharaNasvarUpa']

# Create a dictionary to map short categories to descriptive forms
category_mapping = {
    'n': 'noun',
    'p': 'pronoun',
    'adj': 'adjective',
    'v': 'verb',
    'adv': 'adverb',
    'indec': 'indeclinable',
    # Add more mappings as needed
}

construction_list =['cp', 'conj','temporal', 'disjunct', 'span','meas', 'widthmeas', 'depthmeas','volumemeas','nc', 'distmeas', 'rate', 'timemeas', 'waw', 'calender', 'massmeas', 'heightmeas', 'spatial','xvanxva','compound','ne']
complex_concepts = {
    "conj_1": ["op1", "op2", "op3", "op4", "op5"],
    "disjunct_1": ["op1", "op2", "op3", "op4", "op5"],
    "span_1": ["start", "end"],
    "nc_1": ["mod", "head"],
    "time_meas_1": ["count", "unit"],
    "dist_meas_1": ["count", "unit"],
    "weight_meas_1": ["count", "unit"],
    "length_meas_1": ["count", "unit"],
    "temp_meas_1": ["count", "unit"],
    "width_meas_1": ["count", "unit"],
    "depth_meas_1": ["count", "unit"],
    "height_meas_1": ["count", "unit"],
    "volume_meas_1": ["count", "unit"],
    "rate_1": ["unit_value", "unit_every"],
    "calender_1": ["component1", "component2", "component3", "component4", "component5", "component6"],
    "spatial_1": ["whole", "part"],
    "temporal_1": ["whole", "part"],
    "cp_1": ["kriyAmUla", "verbalizer"],
    "xvanxva_1": ["op1", "op2"],
    "ne_1": ["begin", "inside"]
}
# spkview_list_for_discource=['BI_1','samAveSI','alAvA','awirikwa']
exception_no_tam_sentence_type = ["fragment","term","title","heading"]
aux_exception_case = ['sakawA']
relations = ["card","cxnpart","dem","dur","extent","freq","intf","jk1","k1","k1s","k2","k2g","k2p","k2s","k3","k4","k4a","k5","k5prk","k7","k7a","k7p","k7t","krvn","main",
"mk1","mod","neg","ord","pk1","quant","quantless","quantmore","rad","rbks","rblak","rblpk","rblsk","rcdelim","rcelab","rcloc","rcsamAnakAla","rd",
"re","rh","rhh","rk","rn","rp","r6","rpk","rs","rsma","rsm","rsk","rt","ru","rv","rvks","vIpsA","vkvn"]

ordering_dep_list = ['card','dem','intf','mod','ord','quant','rn','rs','r6','ru','rv','rmeas']
