from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
import os
import json
import datetime
from dotenv import load_dotenv # Import load_dotenv
from verticalformat import graphtousr
from graphfunctions import create_graph_from_instruction, generate_graph_image, generate_hindi_sentence, GraphDataManager, clear_graph_data

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb://127.0.0.1:27017")  # Use your MongoDB URI if different
db = client["recipe_db"]
selections_collection = db["selections"]
usr_collection = db["usrs"]  # This is the collection where the recipe data is stored
collection = db['options']
sentences_collection = db["sentences"]
usrs = db["only_usrs"]
recipe_options = db['recipe_opt']

# Load paths from environment variables
GRAPH_DATA_PATH = os.getenv('GRAPH_DATA_PATH')
DEPENDENCY_ROW_PATH = os.getenv('DEPENDENCY_ROW_PATH')
VERTICAL_FORMAT_PATH = os.getenv('VERTICAL_FORMAT_PATH')

#insert option data into db
# Run this once to insert initial data
if collection.count_documents({}) == 0:
    collection.insert_one({
        "verbs": ["बना", "गर्म+कर", "डाल", "भून", "चला", "पका", "देख", "बन", "रख", "तैयार+कर", "ले", "हो", "मिल", "चटक", "चला"],
        
        "tams": [
            "imperative",
            "habitual_pres",
            "habitual_past",
            "progressive_pres",
            "progressive_past",
            "simple_past",
            "simple_future",
            "simple_present_copula",
            "perfective_pres",
            "perfective_past"
        ],

        "relations": [
            "क्या-कर्ता", "क्या-कर्म", "कौन-कर्ता", "कौन-कर्म", "क्या", "कौन", "कब", "कहां", "कैसे", 
            "कब तक", "कहां पर", "कहां से", "किस लिए", "किस में", "किस के कारण", "किस से अधिक", 
            "किस के समान", "किस का", "किसके तुलना में"
        ],

        "nouns": ["मिर्च", "चटनी", "पैन", "तेल", "लहसुन", "काली+मिर्च", "अब", "आंच", "धब्बे", "धनिया", "करी+पत्ता", "साइड", "मसाला+पाउडर", "चना+दाल", "उड़द+दाल", "जीरा", "मेथी", "सरसों", "सामग्री", "मसाला", "गेंद", "इमली", "नमक", "पेस्ट", "तड़का", "मिर्च", "हिंग", "मिक्सी+जार"],

        "measurements": ["मिनट", "घंटा", "रुपए", "चम्मच"],

        "modifiers": ["हरा", "मसालेदार", "मध्यम", "भूरा", "खुशबूदार", "सुनहरा", "महीन", "स्वादानुसार", "चिकना", "सूखी", "बारीक", "छोटी-सी", "लाल", "ठंडा"],

        "dquantities": ["सभी", "कुछ"],

        "intensifiers": ["बहुत", "अत्यधिक", "बहुत अधिक", "काफ़ी", "थोड़ा", "अत्यंत"]
    })


# Validate that paths are set
if not all([GRAPH_DATA_PATH, DEPENDENCY_ROW_PATH, VERTICAL_FORMAT_PATH]):
    raise ValueError("Please ensure all required environment variables (GRAPH_DATA_PATH, DEPENDENCY_ROW_PATH, VERTICAL_FORMAT_PATH) are set in the .env file.")

# Sample recipes and categories (you could dynamically load these from the database)

if recipe_options.count_documents({}) == 0:
    recipe_options.insert_one({
        "recipes": ["हरा मिर्च की चटनी"],
        "ingredients": {
            "सब्जियां": ["हरा मिर्च", "काली मिर्च", "मसालेदार मिर्च", "हरा धनिया", "करी पत्ता"],
            "दालें और अनाज": ["चना दाल", "उड़द दाल"],
            "मसाले": ["जीरा", "मेथी", "सरसों", "सुखी लाल मिर्च", "हींग"],
            "मसाला पदार्थ": ["इमली", "नमक"],
            "तेल": ["तेल"]
        }
    })

# Endpoint to get recipes and categories
@app.route('/recipes', methods=['GET'])
def get_recipes():
    # Fetch data from MongoDB and exclude the '_id' field
    data = recipe_options.find_one({}, {'_id': 0})
    
    # Check if data exists in the collection
    if data:
        return jsonify(data), 200  # Added status code 200 for success
    else:
        return jsonify({"message": "No data found"}), 404

# Endpoint to get dropdown options (verbs and tams)
@app.route('/get-options', methods=['GET'])
def get_options():
    data = collection.find_one({}, {'_id': 0})  # Fetch without the _id field
    return jsonify(data)



@app.route('/add-option', methods=['POST'])
def add_option():
    data = request.json  # Expecting JSON: {"category": "verbs", "option": "नई क्रिया"}
    category = data.get("category")
    option = data.get("option")
    subcategory = data.get("subcategory")

    if category and option:
        if category == 'recipes':
            recipe_options.update_one({}, {'$push': {category: option}})
        elif category == "ingredients":
            recipe_options.update_one({}, {'$push': {f"{category}.{subcategory}": option}})

            collection.update_one({},{'$push': {"nouns":option}})
            
        else:

            collection.update_one({}, {'$push': {category: option}})
        
        return jsonify({"message": "Option added successfully!"})
    else:
        return jsonify({"message": "Invalid data!"}), 400


@app.route('/save-selection', methods=['POST'])
def save_selection():
    data = request.json
    recipe_id = data.get("recipe_id")
    recipe = data.get("recipe")
    ingredients = data.get("ingredients")

    if not recipe or not ingredients:
        return jsonify({"message": "Recipe and ingredients are required!"}), 400

    # Save the selected combination in MongoDB
    selection_data = {
        "recipe_id": recipe_id,
        "recipe": recipe,
        "ingredients": ingredients
    }
    
    selections_collection.insert_one(selection_data)  # Save the data to MongoDB
    
    return jsonify({"message": "Selection saved successfully!"})

@app.route('/recipe/<recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    # Query the database for the recipe by recipe_id
    recipe_data = selections_collection.find_one({"recipe_id": recipe_id})

    if recipe_data is None:
        return jsonify({"message": "Recipe not found!"}), 404

    # Ensure 'ingredients' is a list
    ingredients = recipe_data.get("ingredients")
    if not isinstance(ingredients, list):
        ingredients = []  # If not a list, provide an empty list or handle as needed

    # Return the recipe details
    return jsonify({
        "recipe_id": recipe_data.get("recipe_id"),
        "recipe": recipe_data.get("recipe"),
        "ingredients": ingredients
    })

@app.route('/create-graph', methods=['POST'])
def create_graph():
    try:
        instruction_data = request.json
        recipe_id = instruction_data.get('recipe_id')
        
        if not recipe_id:
            return jsonify({'error': 'recipe_id is required'}), 400
        
        # Initialize graph manager with recipe_id
        graph_manager = GraphDataManager(recipe_id)
        
        # Create the graph using NetworkX
        G = create_graph_from_instruction(instruction_data, graph_manager)
        
        # Generate the graph image
        graph_image = generate_graph_image(G)
        
        # Generate Hindi sentence
        hindi_sentence = generate_hindi_sentence(G)
        
        return jsonify({
            'status': 'success',
            'graph_image': f"data:image/png;base64,{graph_image}",
            'hindi_sentence': hindi_sentence
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/reset-graph', methods=['POST'])
def reset_graph():
    try:
        data = request.json
        recipe_id = data.get('recipe_id')
        
        if not recipe_id:
            return jsonify({'error': 'recipe_id is required'}), 400
        
        # Initialize graph manager with recipe_id
        graph_manager = GraphDataManager(recipe_id)
        
        # Clear the graph data
        graph_manager.clear_data()
        
        return jsonify({'message': 'Graph reset successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/graphtousr', methods=['POST'])
def graphtousr_api():
    try:
        data = request.get_json()
        recipe_id = data.get('recipe_id')
        
        if not recipe_id:
            return jsonify({'error': 'recipe_id is required'}), 400
        
        # Query the selections collection to find the record
        selection = selections_collection.find_one({"recipe_id": recipe_id})
        
        if not selection:
            return jsonify({'error': 'No matching selection found'}), 404
        
        # Load the graph data from MongoDB
        graph_manager = GraphDataManager(recipe_id)
        G = graph_manager.current_graph
        
        # Convert the graph to USR format and store in database
        result = graphtousr(G, DEPENDENCY_ROW_PATH, recipe_id, db)
        
        return jsonify({
            'message': 'USR data stored successfully', 
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to process graph: {e}'}), 500

# Update the add-sentence route to work with the database
# @app.route('/add-sentence', methods=['POST'])
# def add_sentence():
#     try:
#         data = request.json
#         recipe_id = data.get('recipe_id')
#         sentence = data.get('sentence')

#         if not recipe_id or not sentence:
#             return jsonify({'error': 'Recipe ID and sentence are required'}), 400

#         # Add the sentence to the sentences collection
#         result = sentences_collection.insert_one({
#             'recipe_id': recipe_id,
#             'sentence': sentence,
#             'created_at': datetime.datetime.utcnow()
#         })

#         if result.inserted_id:
#             # Get the USR data for the recipe
#             usr_data = db.usr_collection.find_one({'recipe_id': recipe_id})
#             if usr_data:
#                 # Archive the USR data
#                 db.usr_archive.insert_one({
#                     'recipe_id': recipe_id,
#                     'usr_data': usr_data,
#                     'archived_at': datetime.datetime.utcnow()
#                 })
                
#                 # Clear current USR data
#                 db.usr_collection.delete_one({'recipe_id': recipe_id})

#             return jsonify({'message': 'Sentence added successfully'})

#         return jsonify({'error': 'Failed to add sentence'}), 500

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
@app.route('/get-sentences/<recipe_id>', methods=['GET'])
def get_sentences(recipe_id):
    try:
        # Query all sentences for the given recipe_id
        cursor = sentences_collection.find({'recipe_id': recipe_id})
        sentences = [doc['sentence'] for doc in cursor]
        return jsonify({'sentences': sentences})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/add-sentence', methods=['POST'])
def add_sentence():
    try:
        data = request.json
        recipe_id = data.get('recipe_id')
        sentence = data.get('sentence')
        usr = data.get('usr')

        if not recipe_id or not sentence:
            return jsonify({'error': 'Recipe ID and sentence are required'}), 400

        # Add the sentence to the sentences collection
        result = sentences_collection.insert_one({
            'recipe_id': recipe_id,
            'sentence': sentence,
            'created_at': datetime.datetime.utcnow()
        })
        usrs.insert_one({
                    'recipe_id': recipe_id,
                    'usr':usr,
                    'created_at': datetime.datetime.utcnow()
                })

        if result.inserted_id:
            # Get the usr for the given recipe_id from selections_collection
            usr_data = selections_collection.find_one({'recipe_id': recipe_id}, {'usr': 1})
            if usr_data and 'usr' in usr_data:
                # Insert into the usr_collection
                usr_collection.insert_one({
                    'recipe_id': recipe_id,
                    'usr': usr_data['usr'],
                    'created_at': datetime.datetime.utcnow()
                })
                # Insert into the usrs collection with proper syntax
            
           
            # Unset usr and sentence in selections_collection
            selections_collection.update_one(
                {'recipe_id': recipe_id},
                {'$unset': {'usr': "", 'sentence': ""}}
            )
           
            # Clear the files
            files_to_clear = [
                os.getenv('GRAPH_DATA_PATH'),
                os.getenv('VERTICAL_FORMAT_PATH')
            ]

            for file_path in files_to_clear:
                if file_path and os.path.exists(file_path):
                    if file_path.endswith('.json'):
                        with open(file_path, 'w') as f:
                            json.dump({}, f)
                    else:
                        open(file_path, 'w').close()

            return jsonify({'message': 'Sentence added successfully'})

        return jsonify({'error': 'Failed to add sentence'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# In your Flask app, update the remove_sentences route:



@app.route('/remove-sentences', methods=['POST'])
def remove_sentences():
    try:
        data = request.json
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({'error': 'Recipe ID is required'}), 400

        # Remove all sentences for the given recipe_id
        # result = sentences_collection.delete_many({'recipe_id': recipe_id})
        
        # Clear USR and other related data
        selections_collection.update_one(
            {'recipe_id': recipe_id},
            {'$unset': {'usr': "", 'sentence': ""}}
        )

        # Clear the files
        files_to_clear = [
            os.getenv('GRAPH_DATA_PATH'),
            os.getenv('VERTICAL_FORMAT_PATH')
        ]

        for file_path in files_to_clear:
            if os.path.exists(file_path):
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump({}, f)
                else:
                    open(file_path, 'w').close()

        return jsonify({'message': 'Sentences removed successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



@app.route('/usrs', methods=['GET'])
def get_usrs():
    recipe_id = request.args.get('recipe_id')
    if not recipe_id:
        return jsonify({"error": "recipe_id is required"}), 400
    try:
        # Query the 'only_usrs' collection with the given recipe_id
        cursor = usrs.find({"recipe_id": recipe_id}, {"_id": 0, "usr": 1})
        usr_list = [doc.get('usr', '') for doc in cursor]
        return jsonify(usr_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/sentences', methods=['GET'])
def get_sentenecs():
    recipe_id = request.args.get('recipe_id')
    
    if not recipe_id:
        return jsonify({"error": "recipe_id is required"}), 400

    # Query USRs with the given recipe_id
    sentences= sentences_collection.find({"recipe_id": recipe_id}, {"_id": 0, "sentence": 1})

    # Extract 'usr' values
    sentences_list = [sentence['sentence'] for sentence in sentences]

    return jsonify(sentences_list)
    
if __name__ == '__main__':
   app.run(host="0.0.0.0",debug=True,port=2000)
