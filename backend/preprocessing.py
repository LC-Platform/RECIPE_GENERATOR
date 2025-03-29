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
                    highest_index = max(highest_index, index)
                except ValueError:
                    continue
    return highest_index

def process_lines_nc(output_format):
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
                value_after_plus = parts[1].split('_')[0]
                if value_after_plus not in {'ho', 'kara', 'le', 'xe', 'laga', 'lagA', 'dAla', 'raha', 'karanA', 'raKa', 'xenA', 'A', 'honA', 'lenA', 'laganA', 'lagAnA', 'dAlanA', 'rahanA', 'rakanA', 'kIjie', 'kA'}:
                    try:
                        cp_part = line.split('\t')  
                        if len(cp_part) > 7:
                            spk_info = cp_part[6]
                            processed_lines.append(f"{parts[0]}\t{cp_index}\t-\t-\t-\t-\t-\t-\t{cp_part[1]}:mod\n")
                            processed_lines.append(f"{parts[1].split('_')[0]}\t{cp_index + 1}\t-\t-\t-\t-\t{spk_info}\t-\t{cp_part[1]}:head\n")
                            processed_lines.append(f"[nc_{cp_counter}]\t" + "\t".join(cp_part[1:]) + "\n")  
                            cp_counter += 1
                            cp_index += 2  
                            continue
                    except IndexError:
                        print(f"Skipping line due to missing data: {line}")
                        continue
        processed_lines.append(line + '\n')
    
    return "".join(processed_lines)

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
                    highest_index = max(highest_index, index)
                except ValueError:
                    continue
    return highest_index

def process_lines_cp(output_format):
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
                value_after_plus = parts[1].split('_')[0]
                if value_after_plus in {'ho', 'kara', 'le', 'xe', 'laga', 'lagA', 'dAla', 'raha', 'karanA', 'raKa', 'xenA', 'A', 'honA', 'lenA', 'laganA', 'lagAnA', 'dAlanA', 'rahanA', 'rakanA', 'kIjie', 'kA'}:
                    try:
                        cp_part = parts[1].strip('').split('\t')
                        spk_info = cp_part[6] if len(cp_part) > 6 else '-'
                        
                        if len(cp_part) > 1:
                            cp_inx = cp_part[1]
                            processed_lines.append(f"{parts[0]}_1\t{cp_index}\t-\t-\t-\t-\t-\t-\t{cp_inx}:kriyAmUla\n")
                            processed_lines.append(f"{cp_part[0]}\t{cp_index + 1}\t-\t-\t-\t-\t{spk_info}\t-\t{cp_inx}:verbalizer\n")
                            processed_lines.append(f"[cp_{cp_counter}]\t" + "\t".join(cp_part[1:]) + "\n")
                            cp_counter += 1
                            cp_index += 2  
                            continue
                    except IndexError:
                        print(f"Skipping line due to missing data: {line}")
                        continue
        processed_lines.append(line + '\n')
    
    return "".join(processed_lines)


