def process_dependencies(data, final_filtered_ids, node_info, verb_tam_index):
    dependencies = []
    node_id_to_label = {node['id']: node['attributes']['label'] for node in data['nodes']}
    label_to_id = {node['attributes']['label']: node['id'] for node in data['nodes']}
    
    # Map relations to their connected nodes
    relation_connections = {}
    connector_relations = {}
    noun_span_connections = {}
    
    # First pass: Build connection maps
    for edge in data['edges']:
        source_node = next((node for node in data['nodes'] if node['id'] == edge['source']), None)
        target_node = next((node for node in data['nodes'] if node['id'] == edge['target']), None)
        
        if source_node and target_node:
            source_label = source_node['attributes']['label']
            target_label = target_node['attributes']['label']
            source_type = source_node['attributes']['node_type']
            target_type = target_node['attributes']['node_type']
            
            # Map relations to conj/span connections
            if source_type == 'relation':
                if target_type in ['conj', 'span_dynamic']:
                    relation_connections[target_label] = source_label
                    
            # Map conj to relations
            elif source_type in ['conj', 'span_dynamic']:
                if target_type == 'relation':
                    connector_relations[source_label] = target_label
                    
            # Map spans to nouns (via start/end)
            elif source_type == 'span_dynamic':
                if target_type == 'noun':
                    edge_type = edge.get('type', '')  # 'start' or 'end'
                    if edge_type in ['start', 'end']:
                        if source_label not in noun_span_connections:
                            noun_span_connections[source_label] = {}
                        noun_span_connections[source_label][edge_type] = target_label

    # Process dependencies for each node
    for i, node_label in enumerate(final_filtered_ids):
        node_label_clean = node_label.strip('[]')
        node_type = node_info[node_label_clean]['type']
        node_index = str(i + 1)
        
        if node_type == 'conj':
            # Check if conj is connected to a relation that connects to another conj
            if node_label_clean in connector_relations:
                relation = connector_relations[node_label_clean]
                dependencies.append(f"{verb_tam_index}:{relation}")
            else:
                dependencies.append(f"{verb_tam_index}:conj")
                
        elif node_type == 'span_dynamic':
            # Check if span is connected to a relation
            if node_label_clean in relation_connections:
                dependencies.append(f"{verb_tam_index}:{relation_connections[node_label_clean]}")
            else:
                dependencies.append('-')
                
        elif node_type == 'noun':
            # Find if noun is connected to any span
            connected_span = None
            for span, connections in noun_span_connections.items():
                if node_label_clean in connections.values():
                    connected_span = span
                    break
            
            if connected_span:
                # Check if connected to meas_ through the span
                has_meas = False
                span_id = label_to_id.get(connected_span)
                if span_id:
                    meas_edges = [edge for edge in data['edges'] 
                                if edge['source'] == span_id and 
                                node_id_to_label.get(edge['target'], '').startswith('meas_')]
                    has_meas = bool(meas_edges)
                
                if has_meas:
                    dependencies.append(f"{node_index}:rmeas")
                else:
                    dependencies.append('-')
            else:
                dependencies.append('-')
        else:
            dependencies.append('-')
    
    return dependencies