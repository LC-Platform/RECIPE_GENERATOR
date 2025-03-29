def convert_vert_to_csv(input_text):
    # Split the input text into segments based on the closing </segment_id> tag
    segments = input_text.strip().split('</segment_id>')
    
    # Initialize lists to store segment outputs and segment IDs
    all_output = []
    segment_ids = []
    
    # Process each segment individually
    for segment in segments:
        # Skip empty segments
        if not segment.strip():
            continue
        
        # Split each segment into lines and remove any empty lines
        lines = segment.strip().splitlines()
        
        # Extract the first line (segment_id)
        segment_id = lines[0].strip()
        if "<segment_id=" in segment_id:  # Extract sentence id
            segment_id = segment_id.split('=')[1].strip('>')  # Extract everything after '=' and remove '>'
            segment_ids.append(segment_id)  # Store the segment ID
        
        # Extract the second line (sentence)
        sentence = lines[1].strip()
        
        # Initialize lists to store the columns
        words, indices, entities, extra_column1, extra_column2, extra_column3, extra_column4, extra_column5, extra_column6 = ([] for _ in range(9))
        
        # Process each line of the table data (ignore the first two and last lines)
        for line in lines[2:-1]:
            columns = line.split()
            words.append(columns[0])  # word
            indices.append(columns[1])  # index
            entities.append(columns[2] if columns[2] != '-' else '')  # entity
            
            # Check each extra column and replace '-' with an empty string
            extra_column1.append(columns[3] if columns[3] != '-' else '')
            extra_column2.append(columns[4] if columns[4] != '-' else '')
            extra_column3.append(columns[5] if columns[5] != '-' else '')
            extra_column4.append(columns[6] if columns[6] != '-' else '')
            extra_column5.append(columns[7] if columns[7] != '-' else '')
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
        
        # Add the result to the final output
        all_output.append(output)
    # print(all_output)
    # print(segment_ids)    # Return both the segment outputs and the segment IDs as separate lists
    return all_output, segment_ids

# Example input with multiple segments
input_text = """<segment_id=Test_1_0004>
#जीव समाज आतंकित है ।
jIva_1  1       -       -       -       -       -       -       5:mod
samAja_1        2       -       -       -       -       -       -       5:head
AwaMkiwa_1      3       -       -       4:k1s   -       -       -       -
hE_1-pres       4       -       -       0:main  -       -       -       -
[6-tat_1]       5       -       -       4:k1    -       -       -       -
%affirmative
</segment_id>

<segment_id=Test_1_0005>
#जीव समाज आतंकित है ।
jIva_1  1       -       -       -       -       -       -       5:mod
samAja_1        2       -       -       -       -       -       -       5:head
AwaMkiwa_1      3       -       -       4:k1s   -       -       -       -
hE_1-pres       4       -       -       0:main  -       -       -       -
[6-tat_1]       5       -       -       4:k1    -       -       -       -
%affirmative
</segment_id>

<segment_id=Test_1_0006>
#जीव समाज आतंकित है ।
jIva_1  1       -       -       -       -       -       -       5:mod
samAja_1        2       -       -       -       -       -       -       5:head
AwaMkiwa_1      3       -       -       4:k1s   -       -       -       -
hE_1-pres       4       -       -       0:main  -       -       -       -
[6-tat_1]       5       -       -       4:k1    -       -       -       -
%affirmative
</segment_id>"""

# Call the function and print the result for each segment
outputs, segment_ids = convert_vert_to_csv(input_text)

for segment_output, segment_id in zip(outputs, segment_ids):
    print(f"Segment ID: {segment_id}")
    for line in segment_output:
        print(line)
    print()
