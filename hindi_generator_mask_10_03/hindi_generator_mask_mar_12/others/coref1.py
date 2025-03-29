import json

def process_coreferences(data):
    # Dictionary to keep track of coref words and their assigned IDs
    coref_dict = {}
    coref_counter = 1

    # Read data from the input file
    # with open(input_file, 'r', encoding='utf-8') as infile:
    #     data = json.load(infile)
    with open('output2.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    
    # Process each story and token
    for story in data:
        for token in story.get("tokens", []):
            if "discourse_head" in token and "discourse_rel" in token and token["discourse_rel"] == "coref":
                discourse_head = token["discourse_head"]

                if '.' in discourse_head:
                    referenced_story, referenced_index = discourse_head.split('.')
                    referenced_index = int(referenced_index)

                    # Find the coref_word in the referenced story
                    coref_word = None
                    for ref_story in data:
                        if ref_story["usr_id"] == referenced_story:
                            for ref_token in ref_story.get("tokens", []):
                                if ref_token["index"] == referenced_index:
                                    coref_word = ref_token.get("concept")
                                    break
                            break

                    # Assign or retrieve the coref_id
                    if coref_word:
                        if coref_word not in coref_dict:
                            coref_dict[coref_word] = coref_counter
                            coref_counter += 1

                        token["coref_id"] = coref_dict[coref_word]
                        token["coref_word"] = coref_word

                else:
                    # Handle case where discourse_head is an index within the same story
                    referenced_index = int(discourse_head)
                    coref_word = None
                    for ref_token in story.get("tokens", []):
                        if ref_token["index"] == referenced_index:
                            coref_word = ref_token.get("concept")
                            break

                    # Assign or retrieve the coref_id
                    if coref_word:
                        if coref_word not in coref_dict:
                            coref_dict[coref_word] = coref_counter
                            coref_counter += 1

                        token["coref_id"] = coref_dict[coref_word]
                        token["coref_word"] = coref_word
    # print(coref_dict)

    # Write the updated data to the output file
    with open('output2.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    return json.dumps(data, ensure_ascii=False, indent=4), coref_dict

# Example usage
# print(process_coreferences('output.json', 'output2.json'))
