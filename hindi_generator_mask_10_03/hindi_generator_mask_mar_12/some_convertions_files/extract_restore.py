def find_special_words(strings):
    # Initialize an empty dictionary to store the results with indices
    special_words = {}
    # List to store sentences without * and # characters
    modified_sentences = []

    # Loop through each string in the list with its index
    for idx, string in enumerate(strings):
        modified_sentence = []
        # Split the string into words
        matches = string.split()
        
        # Loop through the matches and add them to the dictionary with their respective special character
        for match in matches:
            if '*' in match:
                word = match.lstrip('*')  # Remove the '*' character
                special_words[(word, idx)] = '*'  # Add to dictionary with index
            elif '#' in match:
                word = match.lstrip('#')  # Remove the '#' character
                special_words[(word, idx)] = '#'  # Add to dictionary with index
            else:
                word = match  # No special character, just the word
            modified_sentence.append(word)  # Append the modified word to the current sentence
        
        # Join the modified sentence and store it
        modified_sentences.append(' '.join(modified_sentence))
    
    return modified_sentences, special_words

def restore_sentences(modified_sentences, special_words):
    restored_sentences = []

    # Loop through each modified sentence with its index
    for idx, sentence in enumerate(modified_sentences):
        # Split the sentence into words
        words = sentence.split()
        
        # Rebuild the sentence with * and # based on the dictionary
        restored_sentence = []
        for word in words:
            if (word, idx) in special_words:
                restored_sentence.append(special_words[(word, idx)] + word)  # Add the special character back
            else:
                restored_sentence.append(word)  # No special character, just the word
        
        # Join the restored sentence and store it
        restored_sentences.append(' '.join(restored_sentence))
    
    return restored_sentences

# Example usage
strings = [
    "जीवन का ऐसाफेल्ट विकास *पहले #आरंभ हुआ।",
    "दिन समय #ऐसाफेल्ट से #बन सडकें #गर्म होतीं हैं।"
]
modified_sentences, result = find_special_words(strings)

print("Modified Sentences:", modified_sentences)
print("Dictionary:", result)

# Restoring the sentences
restored_sentences = restore_sentences(modified_sentences, result)
print("Restored Sentences:", restored_sentences)
