from transformers import AutoModelForMaskedLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
import torch
import time
import re
import sys
# from extract_restore import *
sys.path.append('/home/user/varsh/hindi_generator_mask/updated/repository')
import repository.constant
# from huggingface_hub import login
# token = "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"
# login(token=token, add_to_git_credential=True)
# Load the base masked language model
model = AutoModelForMaskedLM.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")
# model = AutoModelForMaskedLM.from_pretrained("/home/varshith/Downloads/new_gen_example/updated/repository/hindi_fine_tuned_model1")
# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/IndicBERTv2-MLM-only")
# tokenizer = AutoModelForMaskedLM.from_pretrained("/home/varshith/Downloads/new_gen_example/updated/repository/IndicBERTv2-MLM-only")
# Define LoRA configuration
# lora_config = LoraConfig(
#     r=8,               # Low-rank matrix dimension
#     lora_alpha=16,     # Scaling factor for LoRA
#     target_modules=["query", "value"],  # Apply LoRA on attention layers (query, value)
#     lora_dropout=0.1,  # Dropout rate for LoRA layers
#     bias="none",       # No bias terms in LoRA layers
#     task_type="CAUSAL_LM"  # Task type
# )

# # Apply LoRA to the model
# model = get_peft_model(model, lora_config)
# Function to remove special characters but keep mask tokens intact
# Function to remove special characters but keep mask tokens intact
# def clean_sentence(sentence):
#     # Remove all special characters except [MASK] and words
#     return re.sub(r'[^a-zA-Z0-9[\]MASK\s]', '', sentence)

# Function to generate output using the Masked Language Model
# def gen_op(sentence):
#     # Clean the sentence before prediction (remove special characters)
#     # cleaned_sentence = clean_sentence(sentence)
    
#     # Clean the sentence before prediction (remove special characters)
#     # cleaned_sentence = clean_sentence(sentence)
#     model.eval()
#     inputs = tokenizer(sentence, return_tensors="pt")
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits
#         masked_index = (inputs['input_ids'] == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
#         predicted_tokens = logits[0, masked_index].argmax(dim=-1)
#         predicted_words = tokenizer.decode(predicted_tokens)
#         return predicted_words
# Function to generate output using the Masked Language Model
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

def gen_op(sentence):
    model.eval()
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        masked_index = (inputs['input_ids'] == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
        probabilities = torch.softmax(logits[0, masked_index], dim=-1)
        max_probs, predicted_tokens = probabilities.max(dim=-1)
        predicted_words = tokenizer.decode(predicted_tokens)
        return predicted_words, max_probs

# Function to substitute the masked tokens with predictions
# def gen_sen(sentence, op_tokens):
#     sent_list = sentence.strip().split()
#     count = 0
#     op_tok_list = op_tokens.split()
#     for word_inx in range(len(sent_list)):
#         if sent_list[word_inx] == "[MASK]":
#             print(op_tok_list[count],'kkkkkkkk')
#             # if op_tok_list[count] in repository.constant.k7_postposition_list:
#             sent_list[word_inx] = op_tok_list[count]
#             # else:
#             #     sent_list[word_inx] = ''
#             count += 1
#     return " ".join(sent_list)
def gen_sen(sentence, op_tokens, max_probs):
    sent_list = sentence.strip().split()
    count = 0
    op_tok_list = op_tokens.split()
    max_probs_list = max_probs.tolist()
    # print(max_probs_list,'prob')
    for word_inx in range(len(sent_list)):
        if sent_list[word_inx] == "[MASK]":
            if max_probs_list[count] > 0.50:
                sent_list[word_inx] = op_tok_list[count]
            else:
                sent_list[word_inx] = ''  # Remove the mask if probability < 80%
            count += 1

    return " ".join(sent_list).strip()

# Function to handle vibhakti prediction based on masks
# def gen_vibhakti_prediction(sentence):
#     if "[MASK]" in sentence:
#         print(sentence,'sentttt')
#         op = gen_op(sentence.strip())
#         print(op,'opppp')
#         op = gen_sen(sentence, op)
#         return op
#     else:
#         print(sentence,'sentttt1')
#         return sentence
def gen_vibhakti_prediction(sentence):
    if "[MASK]" in sentence:
        print(sentence, 'sentttt')
        op, max_probs = gen_op(sentence.strip())
        print(op,'opppp')
        print(max_probs, 'prob')
        op = gen_sen(sentence, op, max_probs)
        return op
    else:
        print(sentence, 'sentttt1')
        return sentence

# Function to process multiple sentences and measure execution time
def process_masked_multiple_sentences(sentences):
    results = []
    modified_sentence_str, special_words = find_special_words(sentences)
    start_time = time.time()
    
    for sentence in modified_sentence_str:
        
        result = gen_vibhakti_prediction(sentence)
        # print(result,'resulttttttttt')
        results.append(result)
    # print(sentences,'senttttt')
    restored_sentence_str = restore_sentences(results, special_words)
    end_time = time.time()
    execution_time = end_time - start_time
    
    return restored_sentence_str

# if __name__=='__main__':
#     sentences = ["एक *गांव [MASK] चार लडके रहते थे।"]
#     results1= process_masked_multiple_sentences(sentences)
#     print(results1,'results1')