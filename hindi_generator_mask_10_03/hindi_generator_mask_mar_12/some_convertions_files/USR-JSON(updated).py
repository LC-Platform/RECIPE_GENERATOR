import os
import json
import re

class SentenceParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.current_sentence = {}
        self.current_tokens = []
        self.default_usr_id = "Geo_ncert_-"
        self.usr_id = self.default_usr_id

    def parse_input_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()

                if line.startswith("Geo_") or line.startswith(" Geo_"):
                    continue  

                if line.startswith("<sent_id="):
                    self.usr_id = self.extract_usr_id(line)
                elif line.startswith("#") or line.startswith("%"):
                    self.process_sentence_metadata(line)
                elif line.startswith("</sent_id>"):
                    self.finalize_sentence()
                elif line:
                    try:
                        token = self.process_token_info(line)
                        self.current_tokens.append(token)
                    except (IndexError, ValueError) as e:
                        print(f"Error in file: {self.file_path}, Sentence ID: {self.usr_id}")
                        print(f"Error processing line: {line}")
                        print(f"Exception: {e}")
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
        # Resets for the next sentence
        self.current_sentence = {}
        self.current_tokens = []
        self.usr_id = self.default_usr_id

    def process_token_info(self, line):
        token_info = re.split(r'\s+', line)
        token = {}

        token["index"] = self.extract_token_index(token_info)
        token["concept"], token["tam"], token["is_combined_tam"], token["type"] = self.process_concept(token_info[0])
        token["dep_rel"], token["dep_head"] = self.process_dependency(token_info[4])
        
        self.extract_sem_cat(token, token_info[2])
        self.process_morpho_sem(token, token_info[3])
        self.process_discourse_info(token, token_info[5])
        self.process_speaker_view_or_key_value(token, token_info[6])
        self.process_construct_info(token, token_info[8])
        self.process_special_types(token, token_info[0])

        if token["tam"] is None:
            del token["tam"]
            del token["is_combined_tam"]

        if token["type"] is None:
            del token["type"]

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

        # Only split if the concept is not inside square brackets
        if "-" in concept and not concept.startswith("[") and not concept.endswith("]"):
            concept_parts = concept.split("-", 1)
            tam = concept_parts[1] if concept_parts[1] else None
            concept_name = concept_parts[0]

            if tam:
                return concept_name, tam, True, type
            else:
                return concept_name, None, False, type
        return concept, None, False, type

    # def process_dependency(self, dep_info_row):
    #     dep_info = dep_info_row.split(':')
    #     dep_rel = dep_info[1] if len(dep_info) > 1 else "-"
    #     dep_head = dep_info[0] if dep_info[0] != "-" else "-"
    #     return dep_rel, dep_head
    def process_dependency(self, dep_info_row):
        dep_info = dep_info_row.split(':')
        dep_rel = dep_info[1] if len(dep_info) > 1 else "-"
        
        # Convert dep_head to an integer if it's not "-"
        dep_head = dep_info[0]
        if dep_head != "-":
            try:
                dep_head = int(dep_head)  
            except ValueError:
                dep_head = "-"  

        return dep_rel, dep_head

    
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

def process_all_files_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace('.txt', '.json'))

            parser = SentenceParser(input_file_path)
            try:
                parsed_data = parser.parse_input_file()
                parser.save_to_json(output_file_path)
                print(f"Processed {filename} and saved to {output_file_path}")
            except Exception as e:
                print(f"Failed to process {filename}. Error: {e}")

input_folder = 'updated/resolved_chapters' 
output_folder = 'updated/check_outputs' 

process_all_files_in_folder(input_folder, output_folder)
