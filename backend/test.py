# import matplotlib.pyplot as plt
# from matplotlib import font_manager as fm

# # Font path
# hindi_font_path = "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Medium.ttf"
# hindi_font = fm.FontProperties(fname=hindi_font_path)

# # Sample text
# plt.figure()
# plt.text(0.5, 0.5, "धनिया और तेल", fontproperties=hindi_font, fontsize=20, ha='center')
# plt.savefig("test_font_render.png")
# plt.close()

import json
import pandas as pd
from wxconv import WXC
from langdetect import detect
import re
import uuid

def graphtousr(input_file_path, relations_file_path, output_file_path):
    try:
        # Load and process files
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            data = json.loads(infile.read())
            print("===== Input Data =====")
            print(json.dumps(data, indent=2))

        with open(relations_file_path, 'r', encoding='utf-8') as relfile:
            relations_data = json.loads(relfile.read())
            print("\n===== Relations Data =====")
            print(json.dumps(relations_data, indent=2))

        # Initialize variables
        A_list = []  # Final list of processed elements
        B_list = []  # Temporary list for storing connectors
        verb_processed = False
        connector_list = []  # Store both conj and disjunct
        connector_ids = []   # Store connector IDs for final filtered list
        node_info = {}      # For storing node details based on node label
        verb_tam_index = None
        tam = None

        # Process each node in the data
        print("\n===== Processing Nodes =====")
        for node in data['nodes']:
            node_type = node['attributes'].get('node_type')
            node_label = node['attributes'].get('label')

            # Save node information for later use
            node_info[node_label] = {'type': node_type}

            # Step 1: Process verb+TAM first
            if not verb_processed and node_type == 'verb_tam':
                A_list.append(node_label)
                verb_processed = True
                verb_tam_index = len(A_list)
                print(f"Verb+TAM node found: {node_label} (Index: {verb_tam_index})")

            # Step 2: Handle both conj and disjunct nodes dynamically
            if node_type in ['conj', 'disjunct' ,'span_dynamic'] and (node_label.startswith('conj_') or node_label.startswith('disjunct_') or node_label.startswith('span_')):
                print("true")
                if connector_list:
                    A_list.append(connector_list.pop())
                connector_list.append(node_label)
                connector_ids.append(node_label)
                print(f"Connector node found: {node_label}")

            # Step 3: Handle nouns, ingredients, and modifiers
            if node_type in ['noun', 'ingredient', 'modifier']:
                A_list.append(node_label)
                print(f"Noun/Ingredient/Modifier node found: {node_label}")

            # Step 4: Handle measurements and quantities
            if node_type in ['measure', 'unit_value', 'quantity_value']:
                A_list.append(node_label)
                print(f"Measurement/Quantity node found: {node_label}")

        # Step 5: Add remaining connectors to A_list
        if connector_list:
            A_list.extend(connector_list)
            print(f"\nRemaining connectors added to A_list: {connector_list}")

        final_filtered_ids = []
        current_connector = None
        last_non_connector = None

        # Step 6: Filter nodes into final list
        print("\n===== Filtering Nodes into Final List =====")
        for node_label in A_list:
            node_label_clean = node_label.strip('[]')
            node_type = node_info[node_label_clean]['type']
            
            if node_type in ['conj', 'disjunct', 'measure','span_dynamic']:
                final_filtered_ids.append(f"[{node_label}]")
            else:
                final_filtered_ids.append(node_label)

        # Split the first element and handle TAM
        first_element = final_filtered_ids[0]
        split_parts = first_element.split('-')
        if len(split_parts) == 2:
            verb_base = split_parts[0]
            tam = split_parts[1]
            
            if tam == "imperative":
                final_filtered_ids[0] = f"{verb_base}-o_1"
            else:
                final_filtered_ids[0] = verb_base
                
            original_node_label = f"{verb_base}-{tam}"
            if original_node_label in node_info:
                if tam == "imperative":
                    node_info[f"{verb_base}-o_1"] = node_info[original_node_label]
                node_info[verb_base] = node_info[original_node_label]
                node_info[tam] = {"type": "verb_tam_suffix" if node_info[original_node_label]["type"] == "verb_tam" else "other"}

        print(f"TAM part: {tam}")
        print("\n===== Final Filtered IDs =====")
        print(final_filtered_ids)

        # Generate dependencies
        dependencies = []
        last_verb_index = None
        last_noun_index = None

        # Create mappings
        relation_to_dep = {rel['relation']: rel['dependency_relation'] for rel in relations_data['relations']}
        print("\n===== Relation to Dependency Mapping =====")
        print(relation_to_dep)

       
        print("\n===== Processing Edges =====")
        # Initialize a dictionary to store connector-to-relation mappings
        connector_to_relation = {}

        for edge in data['edges']:
            # Case 1: Handle edges where the target starts with 'conj_' or 'disjunct_'
            if edge['target'].startswith(('conj_', 'disjunct_')):
                source_node_id = edge['source']
                source_node = next((node for node in data['nodes'] if node['id'] == source_node_id), None)
          
        # Create mapping for nouns connected to relations
        noun_relation_deps = {}
        node_id_to_label = {node['id']: node['attributes']['label'] for node in data['nodes']}

       
        span_connections = {}  # {span_label: {'relation': relation_label, 'measures': [measure_labels], 'noun_index': None}}
        noun_measures = {}  # {noun_label: [measure_labels]}
        span_noun_map = {}  # {span_label: noun_index}

        for edge in data['edges']:
            source_node = next(n for n in data['nodes'] if n['id'] == edge['source'])
            target_node = next(n for n in data['nodes'] if n['id'] == edge['target'])

            # Track span connections
            if target_node['attributes']['node_type'] == 'span_dynamic':
                span_label = target_node['attributes']['label']

                # Connection from relation to span
                if source_node['attributes']['node_type'] == 'relation':
                    span_connections.setdefault(span_label, {'relation': None, 'measures': [], 'noun_index': None})
                    span_connections[span_label]['relation'] = source_node['attributes']['label']

                # Connection from noun to span
                elif source_node['attributes']['node_type'] == 'noun':
                    noun_index = source_node['attributes'].get('index')  # Returns None if 'index' key is missing
 # Assuming the noun has an 'index' attribute
                    span_noun_map[span_label] = noun_index  # Map span to noun index

                # Check if span is connected to a measure through 'start' or 'end'
                for measure_edge in data['edges']:
                    if measure_edge['source'] == target_node['id']:
                        measure_node = next(n for n in data['nodes'] if n['id'] == measure_edge['target'])
                        
                        if measure_node['attributes']['node_type'] == 'measure' and measure_edge['relation'] in ['start', 'end']:
                            span_connections.setdefault(span_label, {'relation': None, 'measures': [], 'noun_index': None})
                            span_connections[span_label]['measures'].append(measure_node['attributes']['label'])

        # Update span dependencies
        for span_label, details in span_connections.items():
            if details['measures'] and span_label in span_noun_map:
                noun_index = span_noun_map[span_label]
                print(f"[{span_label}]\t{noun_index}:rmeas")
            else:
                print(f"[{span_label}]\t-")  # Keep it as span if no measure connection through start/end
            

        # Create label to index mapping
        label_to_index = {label.strip('[]'): idx+1 for idx, label in enumerate(final_filtered_ids)}

        # Enhanced dependency generation
        print("\n===== Generating Dependencies =====")
        for i, node_label in enumerate(final_filtered_ids):
            node_label_clean = node_label.strip('[]')
            node_type = node_info[node_label_clean]['type']
            node_index = str(i + 1)

            if node_type == 'verb_tam':
                dependencies.append("0:main")
                last_verb_index = node_index
                print(f"Verb+TAM node: {node_label} (Index: {node_index}, Dependency: 0:main)")
            elif node_type == 'noun':
                dependency = '-'
                
                # Check if noun is connected to a relation
                noun_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label_clean)
                source_edges = [edge for edge in data['edges'] if edge['target'] == noun_id]
                
                for edge in source_edges:
                    source_node = next(n for n in data['nodes'] if n['id'] == edge['source'])
                    if source_node['attributes']['node_type'] == 'relation':
                        relation_label = source_node['attributes']['label']
                        dep_rel = relation_to_dep.get(relation_label, 'rel')
                        dependency = f"{verb_tam_index}:{dep_rel}"
                        break  # Take the first found relation

                dependencies.append(dependency)
                print(f"Noun node: {node_label} (Dependency: {dependency})")


            elif node_type in ['conj', 'disjunct']:
                # Handle conjunctions with relation connections
                relation_label = connector_to_relation.get(node_label_clean)
                if relation_label:
                    dep_rel = relation_to_dep.get(relation_label, 'rel')
                    dependencies.append(f"{verb_tam_index}:{dep_rel}")
                else:
                    dependencies.append(f"{verb_tam_index}:{node_type}")
                print(f"Connector node: {node_label} (Dependency: {dependencies[-1]})")

            elif node_type == 'span_dynamic':
                print(f"Processing Span: {node_label_clean}")  # Debugging
            

                if span_connections.get(node_label_clean, {}).get('relation'):
                    # Case: Span is connected to a relation
                 
                    relation_label = span_connections[node_label_clean]['relation']
                    dep_rel = relation_to_dep.get(relation_label, 'rel')
                    dependencies.append(f"{verb_tam_index}:{dep_rel}")

                else:
                    # Check if the span is connected to a noun directly
                    connected_noun = None
                    for edge in data['edges']:
                        if edge['target'] == node_label_clean:
                            source_node = next(n for n in data['nodes'] if n['id'] == edge['source'])
                            if source_node['attributes']['node_type'] == 'noun':
                                connected_noun = source_node['attributes']['label']
                                break
                    
                    print(f"Connected Noun: {connected_noun}")  # Debugging

                    if connected_noun:
                        noun_index = label_to_index.get(connected_noun, '-')
                        # Check if this noun is linked to a measure
                        if connected_noun in noun_measures:
                            dependencies.append(f"{noun_index}:rmeas")
                            dependencies.append('-')  # For rmeas itself
                        else:
                            dependencies.append(f"{noun_index}:rel")  # Generic relation if no measure
                    else:
                        dependencies.append('-')

                print(f"Span node: {node_label} (Dependency: {dependencies[-1]})")


            elif node_type == 'measure':
                # Find connected noun through span
                connected_noun = next((noun for noun, measures in noun_measures.items() 
                                    if node_label_clean in measures), None)
                if connected_noun:
                    noun_idx = label_to_index.get(connected_noun)
                    dependencies.append(f"{noun_idx}:rmeas" if noun_idx else '-')
                else:
                    dependencies.append('-')
                print(f"Measure node: {node_label} (Dependency: {dependencies[-1]})")

            elif node_type in ['modifier']:
                if last_noun_index:
                    dependencies.append(f"{last_noun_index}:mod")
                else:
                    dependencies.append('-')
                print(f"Modifier node: {node_label} (Dependency: {dependencies[-1]})")

            else:
                dependencies.append('-')
                print(f"Other node: {node_label} (Dependency: -)")

# ... [Remaining code stays the same] ...
        # Process component values
        label_to_index = {label: idx + 1 for idx, label in enumerate(final_filtered_ids)}
        component_values = ['-'] * len(final_filtered_ids)

        # Process components for nouns and values
        for idx, node_label in enumerate(final_filtered_ids):
            node_label_clean = node_label.strip('[]')
            node_type = node_info[node_label_clean]['type']
            
            if node_type == 'noun':
                noun_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label_clean)
                source_edges = [edge for edge in data['edges'] if edge['target'] == noun_id]
                
                if source_edges:
                    source_id = source_edges[0]['source']
                    source_label = node_id_to_label.get(source_id)
                    
                    if source_label:
                        conj_edges = [edge for edge in data['edges'] if edge['target'] == source_id]
                        
                        if conj_edges:
                            conj_id = conj_edges[0]['source']
                            conj_label = node_id_to_label.get(conj_id)
                            
                            if conj_label and (conj_label.startswith('conj_') or conj_label.startswith('disjunct_')):
                                conj_index = label_to_index.get(f"[{conj_label}]")
                                if conj_index:
                                    component_values[idx] = f"{conj_index}:{source_label}"

            elif node_type == 'quantity_value':
                quantity_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label_clean)
                source_edges = [edge for edge in data['edges'] if edge['target'] == quantity_id]
                
                if source_edges:
                    source_id = source_edges[0]['source']
                    source_label = node_id_to_label.get(source_id)
                    
                    if source_label:
                        measure_edges = [edge for edge in data['edges'] if edge['target'] == source_id]
                        
                        if measure_edges:
                            measure_id = measure_edges[0]['source']
                            measure_label = node_id_to_label.get(measure_id)
                            
                            if measure_label:
                                measure_index = label_to_index.get(f"[{measure_label}]")
                                if measure_index:
                                    component_values[idx] = f"{measure_index}:count"

            elif node_type == 'unit_value':
                unit_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label_clean)
                source_edges = [edge for edge in data['edges'] if edge['target'] == unit_id]
                
                if source_edges:
                    source_id = source_edges[0]['source']
                    source_label = node_id_to_label.get(source_id)
                    
                    if source_label:
                        measure_edges = [edge for edge in data['edges'] if edge['target'] == source_id]
                        
                        if measure_edges:
                            measure_id = measure_edges[0]['source']
                            measure_label = node_id_to_label.get(measure_id)
                            
                            if measure_label:
                                measure_index = label_to_index.get(f"[{measure_label}]")
                                if measure_index:
                                    component_values[idx] = f"{measure_index}:unit"
        sentence = " ".join(final_filtered_ids)

# Remove "_1" and any content inside square brackets
        sentence = re.sub(r'\[.*?\]', '', sentence)  # Remove content inside square brackets

        sentence = sentence.replace('_1', '')  # Remove "_1"
        sentence = re.sub(r'\d+', '', sentence)  # Remove any numbers

        # Print the cleaned sentence
        print("\n===== Constructed Sentence =====")
        print(sentence)
        # Convert to Hindi if needed
        def convert_to_hindi(final_filtered_ids):
            wx = WXC(order='wx2utf', lang='hin')
            wx1 = WXC(order='utf2wx', lang='hin')
            
            hindi_text_list = [
                wx1.convert(word) if not (word.startswith('[meas') or word.startswith('[conj') or word.startswith('[disjunct') or word.startswith('[span')) else word
                for word in final_filtered_ids
            ]
            return hindi_text_list

        final_filtered_ids = convert_to_hindi(final_filtered_ids)

        # Create DataFrame
        df = pd.DataFrame({
            'concept_data': final_filtered_ids,
            'index_data': [str(i) for i in range(1, len(final_filtered_ids) + 1)],
            'semantic_data': ['-'] * len(final_filtered_ids),
            'gnp_data': ['-'] * len(final_filtered_ids),
            'dependency_data': dependencies,
            'discourse_data': ['-'] * len(final_filtered_ids),
            'skpview_data': ['-'] * len(final_filtered_ids),
            'scope_data': ['-'] * len(final_filtered_ids),
            'construction_data': component_values,
        })

        # Add TAM row if present
        if tam:
            tam_row = pd.DataFrame({
                'concept_data': [f"%{tam}"],
                'index_data': [''],
                'semantic_data': [''],
                'gnp_data': [''],
                'dependency_data': [''],
                'discourse_data': [''],
                'skpview_data': [''],
                'scope_data': [''],
                'construction_data': [''],
            })
            df = pd.concat([df, tam_row], ignore_index=True)

        # Save to TSV file
        df.to_csv(output_file_path, sep='\t', index=False)

        # Save to file
        df.to_csv(output_file_path, sep='\t', index=False)
        print(f"\nFile saved successfully at {output_file_path}")

        # Generate the desired format
     

        def generate_sent_id():
            unique_id = uuid.uuid4().hex[:4]  # Generate a short unique id (first 4 characters)
            return f"<sent_id={unique_id}a>\n"

        # Generate a dynamic sent_id and assign it to output_format
        output_format = generate_sent_id()
        output_format += f"#{sentence}\n"
        for index, row in df.iterrows():
            output_format += f"{row['concept_data']}\t{row['index_data']}\t{row['semantic_data']}\t{row['gnp_data']}\t{row['dependency_data']}\t{row['discourse_data']}\t{row['skpview_data']}\t{row['scope_data']}\t{row['construction_data']}\n"
        output_format += "</sent_id>"

        # Write the formatted output to a file
        
        with open(output_file_path.replace('.tsv', '.txt'), 'w', encoding='utf-8') as f:
            f.write(output_format)
        return output_format

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
graphtousr('/home/praveen/Desktop/main_project/backend/graph_data.json', '/home/praveen/Desktop/main_project/backend/usr_writing/dependency_row.json', '/home/praveen/Desktop/main_project/backend/usr_writing/vertical_format.tsv')



    
       
