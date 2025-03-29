import os

def combine_txt_files(input_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Iterate over all files in the folder
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Add a new line between files

# Specify the folder containing the .txt files and the output file
input_folder = '2ch_nios'  # Replace with your folder path
output_file = 'combined_output.txt'

combine_txt_files(input_folder, output_file)
