def update_morph_dict(json_data, morph_dict):
    # Iterate through morph_dict
    for usr_id in morph_dict:
        # Iterate through json_data for each usr_id
        for entry in json_data:
            coref_id = entry["coref_id"]
            coref_index = entry["index"]
            coref_word_sent_id = entry["coref_word_sent_id"]
            coref_word_index = int(entry["coref_word_index"])

            if usr_id == coref_word_sent_id:
                # Iterate through the entries in morph_dict for the given usr_id
                for i, (index, word, *rest) in enumerate(morph_dict[usr_id]):
                    # If the index matches coref_word_index
                    if index == coref_word_index:
                        # Check if the word has multiple tokens (e.g., "उसमें से")
                        tokens = word.split()
                        if len(tokens) > 1:
                            # Append coref_id to the first token if not already added
                            if f"({coref_id})" not in tokens[0]:
                                tokens[0] = f"{tokens[0]}({coref_id})"
                            # Reassemble the word with the updated tokens
                            word = " ".join(tokens)
                        else:
                            # Append coref_id to the word if not already added
                            if f"({coref_id})" not in word:
                                word = f"{word}({coref_id})"
                        # Update the morph_dict entry
                        morph_dict[usr_id][i] = (index, word, *rest)
            

            if entry["usr_id"] == usr_id:
                # Iterate through the entries in morph_dict for the given usr_id
                for i, (index, word, *rest) in enumerate(morph_dict[usr_id]):
                    # If the index matches coref_index
                    if index == coref_index:
                        # Check if the word has multiple tokens (e.g., "उसमें से")
                        tokens = word.split()
                        if len(tokens) > 1:
                            # Append coref_id to the first token if not already added
                            if f"({coref_id})" not in tokens[0]:
                                tokens[0] = f"{tokens[0]}({coref_id})"
                            # Reassemble the word with the updated tokens
                            word = " ".join(tokens)
                        else:
                            # Append coref_id to the word if not already added
                            if f"({coref_id})" not in word:
                                word = f"{word}({coref_id})"
                        # Update the morph_dict entry
                        morph_dict[usr_id][i] = (index, word, *rest)
    # print(morph_dict)
    return morph_dict

# # Sample input data
# json_data = [
#     {
#         "usr_id": "gold_data_095",
#         "index": 3,
#         "coref_id": 1,
#         "coref_word": "hiMxa",
#         "morpho_sem": None,
#         "discourse_head": "1",
#         "coref_word_sent_id": "gold_data_095",
#         "coref_word_index": "1"
#     },
#     {
#         "usr_id": "gold_data_096",
#         "index": 5,
#         "coref_id": 2,
#         "coref_word": "rAma",
#         "morpho_sem": None,
#         "discourse_head": "1",
#         "coref_word_sent_id": "gold_data_096",
#         "coref_word_index": "1"
#     }
# ]

# morph_dict = {
#     'gold_data_095': [(1, 'hiMxa', 'n', 'd', 'm', 's', 'a', 'proper', None), (2, 'mahAsAgara', 'n', 'd', 'm', 's', 'a', 'common', None), (3, 'jo', 'p', 'd', 'm', 's', 'a', 0, None), (4, 'yUropIya', 'adj', 'd', 'm', 'p'), (5, 'xeSa Ora', 'n', 'd', 'm', 'p', 'a', 'common', None), (6, '#eSiyAI', 'adj', 'd', 'm', 'p'), (7, 'xeSa', 'n', 'd', 'm', 'p', 'a', 'common', None), (8, 'milAwA', 'v', 'm', 's', 'a', 'wA', 'o', 'main'), (8.1, 'hE', 'v', 'm', 's', 'a', 'hE', 'o', 'auxiliary'), (14, 'conj', 'n', 'd', 'm', 's', 'a', 'common', None), (9, 'BArawa ko', 'n', 'o', 'm', 's', 'a', 'proper', 'ko'), (10, 'keMxrIya', 'adj', 'd', 'm', 's'), (11, '*swiwi', 'n', 'd', 'm', 's', 'a', 'common', None), (12, 'praxAna', 'n', 'd', 'm', 's', 'a', 'common', None), (15, 'karawA', 'v', 'm', 's', 'a', 'wA', 'o', 'main'), (15.1, 'hE', 'v', 'm', 's', 'a', 'hE', 'o', 'auxiliary'), (13, 'cp', 'n', 'd', 'm', 's', 'a', 'common', None)],
#     'gold_data_096': [(1, 'rAma', 'n', 'd', 'm', 's', 'a', 'proper', None), (12, 'eka', 'n', 'd', 'm', 's', 'a', 'common', None), (2, 'isa', 'p', 'o', 'm', 's', 'a', 0, None), (3, 'prakAra kA', 'n', 'o', 'm', 's', 'a', 'common', 'kA'), (4, 'ladakA', 'n', 'd', 'm', 's', 'a', 'common', None), (11, 'hE', 'v', 'm', 's', 'a', 'hE', 'o', 'main'), (5, 'jo', 'p', 'd', 'm', 's', 'a', 0, None), (6, 'jyAxA', 'adj', 'd', 'f', 's'), (7, 'mehanawa', 'n', 'd', 'f', 's', 'a', 'common', None), (10, 'karawA', 'v', 'm', 's', 'a', 'wA', 'o', 'main'), (10.1, 'hE', 'v', 'm', 's', 'a', 'hE', 'o', 'auxiliary')]
# }

# # Call the function to update the morph_dict
# updated_morph_dict = update_morph_dict(json_data, morph_dict)

# # Output the updated morph_dict
# print(updated_morph_dict)