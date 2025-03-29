import subprocess
from repository.constant import *

def generate_morph(processed_words):
    """Run Morph generator"""
    #print(processed_words,'pwsssss')
    morph_input = generate_input_for_morph_generator(processed_words)
    # print(morph_input,'morph_input')
    # mappings = parse_file("best_matches_output_uniq.txt")
    # morph_input1,replaced_words = update_list_with_index(morph_input, mappings)
    MORPH_INPUT = write_data(morph_input)
    OUTPUT_FILE1 = run_morph_generator(MORPH_INPUT)
    # print(OUTPUT_FILE1,'ooooooooo')
    # OUTPUT_FILE = replace_words_in_sentence_with_index(OUTPUT_FILE1, replaced_words)
    # OUTPUT_FILE = check_words_in_dict(OUTPUT_FILE)
    #print(OUTPUT_FILE,'output')
    return OUTPUT_FILE1

def generate_input_for_morph_generator(input_data):
    """Process the input and generate the input for morph generator"""
    morph_input_data = []
    for data in input_data:
        # if data[1] in construction_list:
        #     continue
        if data[2] == 'p':
            if data[8] != None and isinstance(data[8], str):
                morph_data = f'^{data[1]}<cat:{data[2]}><parsarg:{data[7]}><fnum:{data[8]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}><per:{data[6]}>$'
            else:
                morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><parsarg:{data[7]}><gen:{data[4]}><num:{data[5]}><per:{data[6]}>$'
        elif data[2] == 'n' and data[7] in ('proper', 'digit'):
            morph_data = f'{data[1]}'
        # elif data[2] == 'n' and data[7] == 'vn':
        #     morph_data = f'^{data[1]}<cat:{data[7]}><case:{data[3]}>$'
        elif data[2] == 'vn':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}>$'
        elif data[2] == 'n' and data[7] != 'proper':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}>$'
        elif data[2] == 'v' and data[8] in ('main','auxiliary'):
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><per:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'v' and data[6] == 'kara' and data[8] in ('nonfinite','adverb')     :
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><per:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'v' and data[6] != 'kara' and data[8] =='nonfinite':
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><case:{data[7]}><tam:{data[6]}>$'
        elif data[2] == 'adj':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}>$'
        elif data[2] == 'vj':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'indec':
            morph_data = f'{data[1]}'
        elif data[2] == 'other':
            morph_data = f'{data[1]}'
        else:
            morph_data = f'^{data[1]}$'
        morph_input_data.append(morph_data)
    #print(morph_input_data)
    print(morph_input_data)
    return morph_input_data

def write_data(writedata):
    """Return the Morph Input Data as a string instead of writing to a file."""
    final_input = " ".join(writedata)
    # Return the generated morph data as a string
    # ##print(final_input,'final')
    return final_input

def run_morph_generator(data):
    """ Pass the morph generator through the provided data and return the output."""
    # #print(data)
    # words = re.findall(r'\^([^\^<]+)<', data)
    command = [
        "lt-proc",
        "-g",
        "-c",
        "repository/hi.gen_LC.bin",
    ]

    # Run the command with input data piped directly
    result = subprocess.run(
        command,
        input=data,
        capture_output=True,
        text=True
    )
    
    # Optionally, handle errors
    if result.returncode != 0:
        raise RuntimeError(f"Error in morph generator: {result.stderr}")
    # #print(result.stdout)
    return result.stdout