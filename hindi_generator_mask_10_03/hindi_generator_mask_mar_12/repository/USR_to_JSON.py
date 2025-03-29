import json
import re

class USR_to_json:
    def __init__(self, input_text):
        self.input_text = input_text
        self.data = []
        self.current_sentence = {}
        self.current_tokens = []
        self.default_usr_id = "Geo_ncert_-"
        self.usr_id = self.default_usr_id

    def parse_input_text(self):
        lines = self.input_text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("Geo_") or line.startswith(" Geo_"):
                continue  

            if line.startswith("<segment_id=") or line.startswith("<sent_id="):
                self.usr_id = self.extract_usr_id(line)
            elif line.startswith("#") or line.startswith("%"):
                self.process_sentence_metadata(line)
            elif line.startswith("</segment_id>") or line.startswith("</id>"):  # Corrected closing tag check
                self.finalize_sentence()
            elif line:
                try:
                    token = self.process_token_info(line)
                    self.current_tokens.append(token)
                except (IndexError, ValueError) as e:
                    raise  

        if self.current_sentence:
            self.finalize_sentence()

        return self.data

    def extract_usr_id(self, line):
        return line.split('=')[1].strip('>').replace('\t', ' ')

    def process_sentence_metadata(self, line):
        if line.startswith("#"):
            self.current_sentence["text"] = self.extract_sentence_text(line)
            self.current_sentence["usr_id"] = self.usr_id
        elif line.startswith("%"):
            self.current_sentence["sent_type"] = self.extract_sentence_type(line)

    def extract_sentence_text(self, line):
        return line[1:].strip().replace('\t', ' ')  

    def extract_sentence_type(self, line):
        return line.strip('%')

    def finalize_sentence(self):
        self.current_sentence["tokens"] = self.current_tokens
        self.data.append(self.current_sentence)
        self.current_sentence = {}
        self.current_tokens = []
        self.usr_id = self.default_usr_id

    def process_token_info(self, line):
        token_info = re.split(r'\s+', line)
        token = {}
        token["index"] = self.extract_token_index(token_info)
        token["concept"], token["tam"], token["is_combined_tam"], token["type"] = self.process_concept(token_info[0])
        token["dep_rel"], token["dep_head"] = self.process_dependency_data(token,token_info[4])
        token["constr_value"], token["constr_concept_index"] = self.process_construction(token_info[8])
        
        self.extract_sem_cat(token, token_info[2])
        self.process_morpho_sem(token, token_info[3])
        self.process_discourse_info(token, token_info[5])
        self.process_speaker_view_or_key_value(token, token_info[6])
        self.process_construct_info(token, token_info[8])
        self.process_special_types(token, token_info[0])

        if "cxn_construct" in token_info[8]:
            token["cxn_construct"], token["construct_head"] = token_info[8].split(':')
            token["construct_head"] = int(token["construct_head"])
        return token

    def extract_token_index(self, token_info):
        try:
            return int(token_info[1])  
        except ValueError:
            raise ValueError(f"Invalid token index: {token_info[1]}")

    def process_concept(self, concept):
        type = None
        if concept.startswith("$"):
            concept = concept[0:] 
            type = "pron"    

        if "-" in concept and not concept.startswith("[") and not concept.endswith("]"):
            concept_parts = concept.split("-", 1)
            tam = concept_parts[1] if concept_parts[1] else None
            concept_name = concept_parts[0]

            if tam:
                return concept_name, tam, True, type
            else:
                return concept_name, None, False, type
        return concept, None, False, type

    def process_construction(self, constr_info_row):
        dep_info = constr_info_row.split(':')
        constr_value = dep_info[1] if len(dep_info) > 1 else "-"
        
        constr_concept_index = dep_info[0]
        if constr_concept_index != "-":
            try:
                constr_concept_index = int(constr_concept_index)  
            except ValueError:
                constr_concept_index = "-"  
        return constr_value, constr_concept_index
    
    def process_dependency_data(self,token, dependency_row ):
        if ':' in dependency_row:
            dep_info = dependency_row.split(':')
            dep_rel = dep_info[1] if len(dep_info) > 1 else "-"
            dep_head = dep_info[0]
            if dep_head:
                try:
                    dep_head = int(dep_head)  
                except ValueError:
                    dep_head = "-"  
            return dep_rel, dep_head
        else:
            return dependency_row, "-"
    
    def extract_sem_cat(self, token, sem_cat_row):
        if sem_cat_row != "-":
            token["sem_category"] = sem_cat_row

    def process_morpho_sem(self, token, morpho_sem_info):
        if morpho_sem_info != "-":
            token["morpho_sem"] = morpho_sem_info

    def process_discourse_info(self, token, discourse_info):
        if discourse_info != "-":
            discourse_parts = discourse_info.split(":")
            token["discourse_head"] = discourse_parts[0] if discourse_parts[0] != "-" else "-"
            token["discourse_rel"] = discourse_parts[1] if len(discourse_parts) > 1 else "-"

    def process_speaker_view_or_key_value(self, token, speaker_view_info):
        if speaker_view_info.startswith("[") and speaker_view_info.endswith("]"):
            bracket_content = speaker_view_info.strip("[]")
            if ":" in bracket_content:
                key, value = bracket_content.split(":", 1)
                token[key] = value
        else:
            if speaker_view_info != "-":
                token["speaker_view"] = speaker_view_info

    def process_construct_info(self, token, construct_info_raw):
        if len(construct_info_raw) > 1:
            construct_info = construct_info_raw.split(':')
            if construct_info[0] != "-":
                token["cxn_construct"] = construct_info[1]
                token["construct_head"] = int(construct_info[0]) if construct_info[0] != "-" else "-"

    def process_special_types(self, token, concept):
        if "conj" in concept:
            token["type"] = "conjunction"
        elif "rate" in concept:
            token["type"] = "rate"
        elif "dist_meas" in concept:
            token["type"] = "distance_measurement"

    def save_to_json(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_json_output(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)

# Example usage:
input_text = '''<segment_id=Test_1_0008>
# बड़ा पैन 1 चुटकी धनिया 2 करी पत्ता भून ।
BUna_1-o_1	1	-	-	0:main	-	-	-	-
pEna_1	2	-	-	1:k2p	-	-	-	-
badZA_1	3	-	-	2:mod	-	-	-	-
XaniyA_1	4	-	-	-	-	-	-	11:op1
[meas_1]	5	-	-	4:rmeas	-	-	-	-
cutakI_1	6	-	-	-	-	-	-	5:unit
1	7	-	-	-	-	-	-	5:count
karI+pawwA_1	8	-	-	-	-	-	-	11:op2
[meas_2]	9	-	-	8:rmeas	-	-	-	-
2	10	-	-	-	-	-	-	9:count
[conj_1]	11	-	-	1:k2	-	-	-	-
%imperative
</segment_id>
'''

parser = USR_to_json(input_text)
parsed_data = parser.parse_input_text()
parser.save_to_json('output.json')
# print(json.dumps(parsed_data, indent=4, ensure_ascii=False))