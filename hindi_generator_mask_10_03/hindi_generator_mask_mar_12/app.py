from pymongo import MongoClient
from flask import jsonify, request
from flask_cors import cross_origin
import re,json
from hindi_gen import hindi_generation
from flask import Flask, request, jsonify
import traceback
from flask_cors import CORS
from flask_cors import cross_origin
from my_masking_model import *
import requests





app = Flask(__name__)

@app.route('/hindi-generation', methods=['POST'])
@cross_origin()
def process_hindi():
    try:
        # Get the data from the POST request body
        data = request.json

        if not data or 'result' not in data:
            return jsonify({"error": "No data or result provided"}), 400

        # Extract result content
        sentence_data = data['result']

        # Extract the sent_id from the result text
        sent_id_match = re.search(r"<sent_id=(.*?)>", sentence_data)
        if not sent_id_match:
            return jsonify({"error": "sent_id not found in result"}), 400

        sent_id = sent_id_match.group(1)

        # Connect to MongoDB
        client = MongoClient('mongodb://10.4.16.167:27017')
        db = client["recipe_db"]
        usr_collection = db["usr_collection"]

        # Get the result from the hindi_generation function
        print("Received sentence data:", sentence_data)
        main_result = hindi_generation(sentence_data)

        # Ensure main_result is a valid dictionary
        if isinstance(main_result, str):
            main_result = json.loads(main_result)

        # Check if main_result has 'bulk' key
        if not isinstance(main_result, dict) or 'bulk' not in main_result:
            return jsonify({"error": "Invalid response format from hindi_generation function"}), 500

        # Extract text and segment_id
        gen_text = []
        for item in main_result['bulk']:
            text = item.get('text')
            segment_id = item.get('segment_id')
            if text and segment_id:
                gen_text.append((segment_id, text))
            else:
                return jsonify({"error": "Missing text or segment_id in main_result"}), 500

        # Define the URL for the mask model
        url = "http://10.4.16.167:8000/mask_model"

        # Create the payload dynamically
        payload = {
            "sentences": [text for segment_id, text in gen_text]  # Extract all texts
        }

        # Send POST request
        response = requests.post(url, json=payload)
        MASK_LIST = []

        # Check the response
        if response.status_code == 200:
            response_data = response.json()
            if 'results' in response_data:
                MASK_LIST = response_data['results']
                for mask in MASK_LIST:
                    print("Masked text received:", mask)
            else:
                return jsonify({"error": "Invalid response format from mask model"}), 500
        else:
            return jsonify({"error": f"Mask model request failed with status code {response.status_code}"}), 500

        # Search for the document with the matching sent_id
        existing_doc = usr_collection.find_one({
            "usr_format": {"$regex": f"<sent_id={re.escape(segment_id)}>"}
        })

        if not existing_doc:
            return jsonify({"error": f"Document with sent_id {segment_id} not found"}), 404

        # Update the document with the new masked sentence
        update_result = usr_collection.update_one(
            {"_id": existing_doc["_id"]},
            {"$set": {"sentence": MASK_LIST[0] if MASK_LIST else ""}}
        )

        if update_result.matched_count == 0:
            return jsonify({"error": "No document updated"}), 500

        return jsonify({"message": "Result stored successfully", "result": MASK_LIST[0] if MASK_LIST else ""})

    except Exception as e:
        print(f"Error: {str(e)}")  # Print error for debugging
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
