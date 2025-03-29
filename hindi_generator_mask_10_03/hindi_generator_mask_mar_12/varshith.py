from flask import Flask, request, jsonify
from flask_cors import cross_origin
import re
import json
import requests
from hindi_gen import hindi_generation

app = Flask(__name__)

@app.route('/hindi-generation', methods=['POST'])
@cross_origin()
def process_hindi():
    try:
        # Get the data from the POST request body as a string
        data = request.get_data(as_text=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract sent_id from the input string
        sent_id_match = re.search(r"<sent_id=(.*?)>", data)
        if not sent_id_match:
            return jsonify({"error": "sent_id not found in input data"}), 400

        sent_id = sent_id_match.group(1)

        # Process the input string using hindi_generation function
        print("Received sentence data:", data)
        main_result = hindi_generation(data)

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

        # Return the masked result directly
        return jsonify({
            "message": "Result processed successfully",
            "result": MASK_LIST[0] if MASK_LIST else ""
        })

    except Exception as e:
        print(f"Error: {str(e)}")  # Print error for debugging
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)