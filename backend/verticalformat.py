import json
import pandas as pd
from wxconv import WXC
from langdetect import detect
import re
import uuid,datetime
import os 
from cp_cxn import process_file_cp
from nc import process_file_nc

def graphtousr(input_graph, relations_file_path, recipe_id, db):
    """
    Convert graph data to USR format and store in MongoDB
    
    Parameters:
    input_graph: NetworkX graph object
    relations_file_path: Path to relations JSON file
    recipe_id: Recipe identifier
    db: MongoDB database connection
    """
    try:
        # 1. Input validation
        if not recipe_id:
            raise ValueError("Recipe ID must be provided")
        if not input_graph:
            raise ValueError("Input graph must be provided")
        if not relations_file_path:
            raise ValueError("Relations file path must be provided")

        # 2. File validation for relations
        if not os.path.exists(relations_file_path):
            raise FileNotFoundError(f"File not found: {relations_file_path}")
        
        with open(relations_file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                raise ValueError(f"Empty file: {relations_file_path}")
            try:
                relations_data = json.loads(content)
                if not relations_data.get('relations'):
                    raise ValueError("Relations data must contain 'relations' array")
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in file: {relations_file_path}")

        # Convert NetworkX graph to required format
        data = {
            'nodes': [],
            'edges': []
        }
        
        # Add nodes
        for node, attrs in input_graph.nodes(data=True):
            data['nodes'].append({
                'id': node,
                'attributes': attrs
            })
            
        # Add edges
        for source, target, attrs in input_graph.edges(data=True):
            data['edges'].append({
                'source': source,
                'target': target,
                'attributes': attrs
            })

        # Initialize variables
        A_list = []  # Final list of processed elements
        B_list = []  # Temporary list for storing connectors
        verb_processed = False
        connector_list = []  # Store both conj and disj
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

            # Step 2: Handle both conj and disj nodes dynamically
            print(node_type)
            if node_type in ['conj', 'disj' ,'span_dynamic','rate_dynamic'] or (node_label.startswith('[conj_') or node_label.startswith('[disj_') or node_label.startswith('[span_')):
               
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
            if node_type in ['intensifier','measure', 'unit_value', 'quantity_value','number','quant']:
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
            node_type = node_info[node_label]['type']
            
            if node_type in ['conj', 'disj', 'measure','span_dynamic','rate_dynamic']:
                print(node_type)
                final_filtered_ids.append(f"{node_label}")
            else:
                final_filtered_ids.append(node_label)

        # Split the first element and handle TAM
       

        # Generate dependencies
        dependencies = []
        last_verb_index = None
        last_noun_index = None
        last_mod_index = None

        # Create mappings
        relation_to_dep = {rel['relation']: rel['dependency_relation'] for rel in relations_data['relations']}
        print("\n===== Relation to Dependency Mapping =====")
        print(relation_to_dep)

       
        print("\n===== Processing Edges =====")
        # Initialize a dictionary to store connector-to-relation mappings
        connector_to_relation = {}

        for edge in data['edges']:
            # Case 1: Handle edges where the target starts with 'conj_' or 'disj_'
            if edge['target'].startswith(('[conj_', '[disj_')):
                source_node_id = edge['source']
                source_node = next((node for node in data['nodes'] if node['id'] == source_node_id), None)
          
        # Create mapping for nouns connected to relations
        noun_relation_deps = {}
        node_id_to_label = {node['id']: node['attributes']['label'] for node in data['nodes']}

        # First pass: identify nouns connected to relations, excluding those with spans
        # ... [Previous code remains the same until edge processing] ...

# Enhanced edge processing for relations and spans
        span_connections = {}  # {span_label: {'relation': relation_label, 'measures': [measure_labels]}}
        noun_measures = {}     # {noun_label: [measure_labels]}

        for edge in data['edges']:
            source_node = next(n for n in data['nodes'] if n['id'] == edge['source'])
            target_node = next(n for n in data['nodes'] if n['id'] == edge['target'])
            
            # Track relations connected to connectors/spans
            if source_node['attributes']['node_type'] == 'relation':
                if target_node['attributes']['node_type'] in ['conj', 'disj', 'span_dynamic']:
                    connector_to_relation[target_node['attributes']['label']] = source_node['attributes']['label']
            
            # Track span connections
            if target_node['attributes']['node_type'] == 'span_dynamic' or 'rate_dynamic':
                span_label = target_node['attributes']['label']
                
                # Connection from relation to span
                if source_node['attributes']['node_type'] == 'relation':
                    span_connections.setdefault(span_label, {'relation': None, 'measures': []})
                    span_connections[span_label]['relation'] = source_node['attributes']['label']
                
                # Connection from noun to span
                elif source_node['attributes']['node_type'] == 'noun':
                  
                    for measure_edge in data['edges']:
                        if measure_edge['source'] == target_node['id']:
                            measure_node = next(n for n in data['nodes'] if n['id'] == measure_edge['target'])
                            print(measure_node['attributes']['node_type'])
                            if measure_node['attributes']['node_type'] == 'measure':

                                noun_measures.setdefault(source_node['attributes']['label'], []).append(measure_node['attributes']['label'])
                                

        # Create label to index mapping
        label_to_index = {label.strip('[]'): idx+1 for idx, label in enumerate(final_filtered_ids)}

        # Enhanced dependency generation
        print("\n===== Generating Dependencies =====")
        for i, node_label in enumerate(final_filtered_ids):
            node_label_clean = node_label.strip('[]')
            # node_label_clean = node_label_clean.strip('[]')
            node_type = node_info[node_label]['type']
            node_index = str(i + 1)
            mod_index= str(i+1)
            print(node_type)

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
                        print(relation_label)
                        dep_rel = relation_to_dep.get(relation_label, 'rel')
                        print(dep_rel)
                        dependency = f"{verb_tam_index}:{dep_rel}"
                        break  # Take the first found relation

                dependencies.append(dependency)
                last_noun_index = node_index
                print(f"Noun node: {node_label} (Dependency: {dependency})")


            elif node_type in ['conj', 'disj']:
                # Handle conjunctions with relation connections
                relation_label = connector_to_relation.get(node_label)
                if relation_label:
                    dep_rel = relation_to_dep.get(relation_label, 'rel')
                    dependencies.append(f"{verb_tam_index}:{dep_rel}")
                else:
                    dependencies.append(f"{verb_tam_index}:{node_type}")
                print(f"Connector node: {node_label} (Dependency: {dependencies[-1]})")

            elif node_type == 'span_dynamic' or node_type == 'rate_dynamic':
    # Initialize dependency
                source_node_label = None
                
                # First, find the edge where target starts with 'span_dynamic'
                for edge in data['edges']:
                    if edge['target'].startswith("span_dynamic") or edge['target'].startswith("rate_dynamic"):
                        source_node = next(n for n in data['nodes'] if n['id'] == edge['source'])
                        source_node_label = source_node['attributes']['label']
                        # Find the span_dynamic node's outgoing connections
                        span_node_id = edge['target']
                        
                        # Now find where this span_dynamic node connects to
                        for next_edge in data['edges']:
                            if next_edge['source'] == span_node_id:
                                intermediate_target = next_edge['target']
                                print(f"First level target: {intermediate_target}")
                                
                                # Look for the next connection using intermediate_target as source
                                final_target = None
                                for second_edge in data['edges']:
                                    if second_edge['source'] == intermediate_target:
                                        final_target = second_edge['target']
                                        print(f"Final target found: {final_target}")
                                        break
                                
                                # If no second level connection found, use intermediate_target as final_target
                                if final_target is None:
                                    final_target = intermediate_target
                                    print(f"No second level connection found, using intermediate as final: {final_target}")
                                
                                # Process the final target
                                if final_target.startswith('measure_'):
                                    dep_rel = 'rmeas'
                                    print(f"Found measurement connection: {span_node_id} -> {final_target}")
                                else:
                                    # If not connected to measurement, use default logic
                                    if node_label_clean in span_connections:
                                        relation_label = span_connections[node_label_clean].get('relation')
                                        dep_rel = relation_to_dep.get(relation_label, 'rel') if relation_label else 'rel'
                                        print(f"Using relation from span_connections: {dep_rel}")
                                    else:
                                        dep_rel = 'meas'
                                        print(f"No measurement or specific relation found, defaulting to 'mod'")
                                break
                        break
                
                if source_node_label:
                    # Find the index of the source node label in label_to_index
                    source_index = label_to_index.get(source_node_label, '-')
                    print(source_index)
                    if source_index != '-':
                        dependencies.append(f"{source_index}:{dep_rel}")
                    else:
                        dependencies.append(f"{verb_tam_index}:{dep_rel}")
                    print(f"Final dependency for {source_node_label}: {dependencies[-1]}")
           
                else:
                    dependencies.append('-')
                    print("No source node found for span_dynamic")
            
            elif node_type == 'measure':
                # Find connected noun through span
                print(data['edges'])
                print(node_label_clean)
                measure_source = next(
        (edge['source'] for edge in data['edges'] if edge['target'].startswith('rmeas')), 
        None
    )
    
                
                connected_noun = next((noun for noun, measures in noun_measures.items() 
                                    if node_label_clean in measures), None)
            
                if connected_noun:
                    noun_idx = label_to_index.get(connected_noun)
                    dependencies.append(f"{noun_idx}:rmeas" if noun_idx else '-')
                print(measure_source)
                if measure_source:
        # Find the corresponding node in data['nodes']
                    source_node = next((node for node in data['nodes'] if node['id'] == measure_source), None)
                    print(source_node)
                    
                    # if source_node and source_node['attributes']['label'].startswith('noun'):
                    noun_label = source_node['attributes']['label']
                    noun_idx = label_to_index.get(noun_label)
                    
                    if noun_idx:
                        dependencies.append(f"{noun_idx}:rmeas")
                    
            
                else:
                    dependencies.append('-')
                print(f"Measure node: {node_label} (Dependency: {dependencies[-1]})")
            elif node_type == 'number':
                # Find connected noun through span
                print(data['edges'])
                print(node_label_clean)
                measure_source = next(
        (edge['source'] for edge in data['edges'] if edge['target'].startswith('num')), 
        None
    )
    
                
                connected_noun = next((noun for noun, measures in noun_measures.items() 
                                    if node_label_clean in measures), None)
            
                if connected_noun:
                    noun_idx = label_to_index.get(connected_noun)
                    dependencies.append(f"{noun_idx}:card" if noun_idx else '-')
                print(measure_source)
                if measure_source:
        # Find the corresponding node in data['nodes']
                    source_node = next((node for node in data['nodes'] if node['id'] == measure_source), None)
                    print(source_node)
                    
                    # if source_node and source_node['attributes']['label'].startswith('noun'):
                    noun_label = source_node['attributes']['label']
                    noun_idx = label_to_index.get(noun_label)
                    
                    if noun_idx:
                        dependencies.append(f"{noun_idx}:card")
                    
            
                else:
                    dependencies.append('-')
                print(f"Measure node: {node_label} (Dependency: {dependencies[-1]})")

            elif node_type == 'quant':
                # Find connected noun through span
                print(data['edges'])
                print(node_label_clean)
                measure_source = next(
        (edge['source'] for edge in data['edges'] if edge['target'].startswith('quan')), 
        None
    )
    
                
                connected_noun = next((noun for noun, measures in noun_measures.items() 
                                    if node_label_clean in measures), None)
            
                if connected_noun:
                    noun_idx = label_to_index.get(connected_noun)
                    dependencies.append(f"{noun_idx}:quant" if noun_idx else '-')
                print(measure_source)
                if measure_source:
        # Find the corresponding node in data['nodes']
                    source_node = next((node for node in data['nodes'] if node['id'] == measure_source), None)
                    print(source_node)
                    
                    # if source_node and source_node['attributes']['label'].startswith('noun'):
                    noun_label = source_node['attributes']['label']
                    noun_idx = label_to_index.get(noun_label)
                    
                    if noun_idx:
                        dependencies.append(f"{noun_idx}:quant")
                    
            
                else:
                    dependencies.append('-')
                print(f"Measure node: {node_label} (Dependency: {dependencies[-1]})")



            elif node_type == 'modifier':
            
                if last_noun_index:
                    dependencies.append(f"{last_noun_index}:mod")
                else:
                    dependencies.append('-')
                print(f"Modifier node: {node_label} (Dependency: {dependencies[-1]})")
                last_mod_index = mod_index
            elif node_type == "intensifier":
                if last_mod_index:
                    dependencies.append(f"{last_mod_index}:intf")
                else:
                    dependencies.apped('-')
                print("intensidier node:{node_label} (Dependency: -)")

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
            node_type = node_info[node_label]['type']
            
            if node_type == 'noun':
                noun_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label_clean)
                source_edges = [edge for edge in data['edges'] if edge['target'] == noun_id]
                
                if source_edges:
                    source_id = source_edges[0]['source']
                    source_label = node_id_to_label.get(source_id)
                    print("sr",source_label)
                    
                    if source_label:
                        conj_edges = [edge for edge in data['edges'] if edge['target'] == source_id]
                        # print(conj_edges)
                        
                        if conj_edges:
                            conj_id = conj_edges[0]['source']
                            conj_label = node_id_to_label.get(conj_id)
                            print(conj_label)
                            
                            if  (conj_label.startswith('[conj_') or conj_label.startswith('[disj_')) or (conj_label.startswith('[span_')):
                                conj_index = label_to_index.get(f"{conj_label}")
                                # print(conj_index)
                                if conj_index:
                                    component_values[idx] = f"{conj_index}:{source_label}"
                        

            elif node_type == 'quantity_value':
                quantity_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label_clean)
                source_edges = [edge for edge in data['edges'] if edge['target'] == quantity_id]
                print("qi",quantity_id)
                print(source_edges)
                
                if source_edges:
                    source_id = source_edges[0]['source']
                    source_label = node_id_to_label.get(source_id)
                    print(source_id)
                    print(source_label)
                   
                    
                    if source_label:
                        measure_edges = [edge for edge in data['edges'] if edge['target'] == source_id]
                        print(measure_edges)
                        
                        if measure_edges:
                            measure_id = measure_edges[0]['source']
                            measure_label = node_id_to_label.get(measure_id)
                           
                            
                            if measure_label:
                                measure_index = label_to_index.get(f"{measure_label}")
    
                                if measure_index:
                                    component_values[idx] = f"{measure_index}:count"

            elif node_type == 'unit_value':
                unit_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label)
                source_edges = [edge for edge in data['edges'] if edge['target'] == unit_id]
                
                if source_edges:
                    # Find the nearest preceding measurement node
                    current_idx = idx
                    nearest_meas_index = None
                    
                    # Search backwards through the sequence until we find a measurement
                    while current_idx >= 0:
                        prev_label = final_filtered_ids[current_idx]
                        if prev_label.startswith('[meas_'):
                            nearest_meas_index = label_to_index.get(prev_label)
                            break
                        current_idx -= 1
                    
                    if nearest_meas_index is not None:
                        component_values[idx] = f"{nearest_meas_index}:unit"
            elif node_type == 'measure':
                    
                    measure_id = next(node['id'] for node in data['nodes'] if node['attributes']['label'] == node_label)
                    
                    # Find edges targeting this measure node
                    incoming_edges = [edge for edge in data['edges'] if edge['target'] == measure_id]
                    
                    if incoming_edges:
                        source_id = incoming_edges[0]['source']
                        source_label = node_id_to_label.get(source_id)
                        
                        if source_label:
                            # Find what this start/end node is connected to
                            parent_edges = [edge for edge in data['edges'] if edge['target'] == source_id]
                            
                            if parent_edges:
                                parent_id = parent_edges[0]['source']
                                parent_label = node_id_to_label.get(parent_id)
                                
                                if parent_label:
                                    parent_index = label_to_index.get(f"{parent_label}")
                                    print(parent_index)
                                    print(parent_label)
                                    print(source_label)
                                    
                                    # Check if source is start or end node
                                    if 'start' in source_label.lower():
                                        component_values[idx] = f"{parent_index}:start"
                                    elif 'end' in source_label.lower():
                                        component_values[idx] = f"{parent_index}:end"
                                    elif 'unit_every' in source_label.lower():
                                        component_values[idx] = f"{parent_index}:unit_every"
                                    elif 'unit_value' in source_label.lower():
                                        component_values[idx] = f"{parent_index}:unit_value"

        print(component_values)
        sentence = " ".join(final_filtered_ids)
        sentence = re.sub(r'\[.*?\]', '', sentence)
        sentence = sentence.replace('_1', '')
        sentence = re.sub(r'\d+', '', sentence)

        # Convert to Hindi if needed
        def convert_to_hindi(final_filtered_ids):
            wx = WXC(order='wx2utf', lang='hin')
            wx1 = WXC(order='utf2wx', lang='hin')

            hindi_text_list = []
            for word in final_filtered_ids:
                fixed_prefixes = ('[meas', '[conj', '[disj', '[span', '[rate')
                numeric_prefixes = tuple(str(i) for i in range(10))
                if word.startswith(fixed_prefixes + numeric_prefixes):
    # your code here

                    hindi_text_list.append(word)
                else:
                    parts = word.split('-', 1)  # Split only at the first occurrence of '-'
                    if len(parts) == 2:
                        converted_left = wx1.convert(parts[0])  # Convert only the left part
                        hindi_text_list.append(f"{converted_left}_1-{parts[1]}")
                    else:
                        hindi_text_list.append(wx1.convert(word)+"_1")

            return hindi_text_list
        first_element = final_filtered_ids[0]
        split_parts = first_element.split('-')
        if len(split_parts) == 2:
            verb_base = split_parts[0]
            tam = split_parts[1]
            
            if tam == "imperative":
                final_filtered_ids[0] = f"{verb_base}-imper_1"
            elif tam == "habitual_pres":
                final_filtered_ids[0] = f"{verb_base}-wA_hE_1"
            elif tam == "habitual_past":
                final_filtered_ids[0] = f"{verb_base}-wA_WA_1"
            elif tam == "progressive_pres":
                final_filtered_ids[0] = f"{verb_base}-0_rahA_hE_1"
            elif tam == "progressive_past":
                final_filtered_ids[0] = f"{verb_base}-0_rahA_WA_1"
            elif tam == "simple_past":
                final_filtered_ids[0] = f"{verb_base}-yA_1"
            elif tam == "simple_future":
                final_filtered_ids[0] = f"{verb_base}-gA_1"
            elif tam == "simple_present_copula":
                final_filtered_ids[0] = f"{verb_base}-hE_1-pres"
            elif tam == "perfective_pres":
                final_filtered_ids[0] = f"{verb_base}-0_cukA_hE_1"
            elif tam == "perfective_past":
                final_filtered_ids[0] = f"{verb_base}-0_cukA_wA_1"
            else:
                final_filtered_ids[0] = verb_base

                
            original_node_label = f"{verb_base}-{tam}"
            if original_node_label in node_info:
                if tam == "imperative":
                    node_info[f"{verb_base}-imper_1"] = node_info[original_node_label]
                node_info[verb_base] = node_info[original_node_label]
                node_info[tam] = {"type": "verb_tam_suffix" if node_info[original_node_label]["type"] == "verb_tam" else "other"}

        print(f"TAM part: {tam}")
        print("\n===== Final Filtered IDs =====")
        print(final_filtered_ids)
        

        final_filtered_ids = convert_to_hindi(final_filtered_ids)
        print("cp",final_filtered_ids)
        print(dependencies)
        print(component_values)

       
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
                'concept_data': [f"%affirmative"],
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

        # Generate output format
        def generate_sent_id():
            return f"<sent_id={uuid.uuid4().hex[:4]}a>\n"

        output_format = generate_sent_id()
        output_format += f"#{sentence}\n"
        
        for index, row in df.iterrows():
            output_format += f"{row['concept_data']}\t{row['index_data']}\t"\
                           f"{row['semantic_data']}\t{row['gnp_data']}\t"\
                           f"{row['dependency_data']}\t{row['discourse_data']}\t"\
                           f"{row['skpview_data']}\t{row['scope_data']}\t"\
                           f"{row['construction_data']}\n"
        
        output_format += "</sent_id>"

        print(output_format)
        output_format = process_file_cp(output_format)
        output_format = process_file_nc(output_format)
        print(output_format)
    
       




        # Save outputs
        usr_data = {
            'recipe_id': recipe_id,
            'usr_format': output_format,
            'dataframe': df.to_dict('records'),
            'created_at': datetime.datetime.utcnow()
        }
        
        # Update or insert USR data using the db parameter directly
        db.usr_collection.update_one(
            {'recipe_id': recipe_id},
            {'$set': usr_data},
            upsert=True
        )

        return output_format

    except Exception as e:
        print(f"An error occurred in graphtousr: {str(e)}")
        raise
