import json

def transform_data(input_file):
    """
    Reads JSON data from a file, filters and transforms it based on the given conditions,
    and returns the transformed JSON data.
    
    :param input_file: Path to the input JSON file
    :return: Transformed JSON data
    """
    # Read data from the file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Initialize a list for the transformed data
    transformed_data = []
    
    # Process each entry in the data
    for entry in data:
        usr_id = entry["usr_id"]
        for token in entry["tokens"]:
            if token.get("discourse_rel") and token["discourse_rel"] != "coref":
                # Process discourse_head field
                discourse_head = token.get("discourse_head")
                if discourse_head and '.' in discourse_head:
                    discourse_head_sent_id, discourse_head_index = discourse_head.split('.')
                else:
                    discourse_head_sent_id, discourse_head_index = None, None
                
                # Create a new dictionary with the required fields
                new_entry = {
                    "usr_id": usr_id,
                    "discourse_head":discourse_head,
                    "discourse_head_sent_id": discourse_head_sent_id,
                    "discourse_head_index": discourse_head_index,
                    "discourse_rel": token.get("discourse_rel"),
                    "speaker_view": token.get("speaker_view", None)
                }
                transformed_data.append(new_entry)
    
    return transformed_data

# Example usage:
if __name__ == "__main__":
    input_file = "output.json"  # Replace with the path to your input file
    output_file = "discource.json"  # Path to save the transformed data
    
    # Transform the data
    result = transform_data(input_file)
    
    # Save the result to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    
    print(f"Transformed data saved to {output_file}")
