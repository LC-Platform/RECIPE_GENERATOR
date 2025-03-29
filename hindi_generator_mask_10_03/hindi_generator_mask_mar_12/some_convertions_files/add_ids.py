import json
def process_sentence(segment_ids,sentences, all_output):
    # Create a dictionary to hold the output
    if len(segment_ids)>1 and len(segment_ids)==len(all_output):
        for segment_id, output in zip(segment_ids, all_output):
            if segment_id and output:
                    sentences.append({
                        "segment_id": segment_id,
                        "text": output
                    })
            # current_segment_id = None
            # current_text = None
        output = {
            "bulk": sentences
        }
    else:
        output = {
            "sentence_id": segment_ids,
            "text": all_output
        }
    # ##print the JSON output
    # ##print(json.dumps(output, ensure_ascii=False, indent=2))
    # Convert the dictionary to a JSON string
    json_output = json.dumps(output, ensure_ascii=False)
    # process_and_write_json(json_output, output_file="./formatted_output.txt")
    return json_output

if __name__=="__main__":
    segment_ids=['1', '2', '3a', '3b', '4a', '4b', '4c', '5', '6', '7a', '7b', '8', '9']
    all_output=[
        "एक गाँव में 4 लडके रहते थे।",
        "वह (लडका) बहुत घनिष्ठ मित्र था।",
        "उसमें (लडका) 2 लडके बहुत आज्ञाकारी थे।",
        "विपरीत/इसके विपरीत/परंतु/किंतु/लेकिन 2 लडके बहुत शरारती #चंचल थे।",
        "यदि गाँव में #कुछ भी #गलत होती थी।",
        "तो सब लोग यह सोचता था।",
        "वह *दोनों लडका किया है।",
        "इस कारण/इसी कारण/इसके परिणामस्वरूप/अतः/इसलिए/इसीलिए उसकी (लडका) माता पिता बहुत #परेशान थी।",
        "जबकि अन्य 2 लडकों का परिवार बहुत खुश था।",
        "वे (लडका) आज्ञाकारी ही थे।",
        "बल्कि वे (लडका) बहुत समझदार भी थे भी।",
        "इसके बावज़ूद/फिर भी/हालाँकि/तथापि उस 4 का *स्वभाव बहुत अनोखा था।",
        "यद्यपि वे (लडका) बहुत घनिष्ठ मित्र थे।"
    ]
    sentences=[]
    output_json= process_sentence(segment_ids,sentences, all_output)
    # Print the formatted output
    # print(output)
    output = json.loads(output_json)

# Access the 'bulk' key and print formatted output
    for item in output['bulk']:
        print(f"{item['segment_id']}\t{item['text']}")

    # output.load()
    