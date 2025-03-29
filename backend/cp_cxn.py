import os

def extract_highest_index(lines):
    highest_index = -1  

    for line in lines:
        line = line.rstrip()  
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) > 1:
                try:
                    index = int(parts[1])  
                    if index > highest_index:
                        highest_index = index
                except ValueError:
                    continue  
    
    return highest_index

def process_file_cp(output_format):
    lines = output_format.split('\n')
    highest_index = extract_highest_index(lines)

    processed_lines = []
    cp_counter = 1
    cp_index = highest_index + 1  

    for line in lines:
        line = line.rstrip()
        if '+' in line and '#' not in line:
            parts = line.split('+')
            if len(parts) > 1:
                full_word = parts[1].split('_')[0]  # Extract full word (e.g., "kara-o_1" → "kara")
                base_word = full_word.split('-')[0]  # Extract base word before "-"

                if base_word in {'ho', 'kara', 'le', 'xe', 'laga', 'lagA', 'dAla', 'raha', 'karanA', 'raKa', 'xenA', 'A', 'honA', 'lenA', 'laganA', 'lagAnA', 'dAlanA', 'rahanA', 'rakanA', 'kIjie', 'kA'}:
                    try:
                        cp_part = parts[1].strip().split('\t')
                        spk_info = cp_part[6] if len(cp_part) > 6 else '-'
                        
                        if len(cp_part) > 1:
                            cp_inx = cp_part[1]
                            processed_lines.append(f"{parts[0]}_1\t{cp_index}\t-\t-\t-\t-\t-\t-\t{cp_inx}:kriyAmUla\n")
                            processed_lines.append(f"{cp_part[0]}\t{cp_index + 1}\t-\t-\t-\t-\t{spk_info}\t-\t{cp_inx}:verbalizer\n")
                            processed_lines.append(f"[cp_{cp_counter}]\t{cp_part[1]}\t{cp_part[2]}\t{cp_part[3]}\t{cp_part[4]}\t{cp_part[5]}\t-\t{cp_part[7]}\t-\n")
                            cp_counter += 1
                            cp_index += 2
                            continue
                    except IndexError:
                        print(f"Skipping line due to missing data: {line}")
                        continue
        
        processed_lines.append(line + '\n')

    return "".join(processed_lines)  

# # Sample Input
# output_format = """
# <sent_id=834ba>
# गर्म+कर-o आंच चिकना
# garma+kara-o_1  1       -       -    0:main   -       -       -       -
# AMca    2       -       -       1:k2p--       -       -
# cikanA  3       -       -       2:mod--       -       -
# %imperative
# </sent_id>
# """

# print("Original Output Format:")
# print(output_format)

# output_format = process_file_cp(output_format)

# print("\nProcessed Output Format:")
# print(output_format)
