import networkx as nx
import graphviz
import json
import os
import io
import base64
from typing import Dict, Optional, Tuple
import uuid
import itertools
from rate import handle_rate_measurement

import networkx as nx
import json
import os
from typing import Dict, Optional, Tuple
import datetime
from pymongo import MongoClient
import networkx as nx
import json
from typing import Dict, Optional, Tuple

class GraphDataManager:
    """Manages graph data storage and manipulation using MongoDB."""
    
    def __init__(self, recipe_id: str):
        """
        Initialize the graph data manager.
        
        Args:
            recipe_id: ID of the recipe being processed
        """
        self.client = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.client["recipe_db"]
        self.graphs_collection = self.db["graphs"]
        self.recipe_id = recipe_id
        self.current_graph = self.load_data()
    
    def load_data(self) -> nx.DiGraph:
        """
        Load existing graph data from MongoDB.
        
        Returns:
            NetworkX DiGraph object
        """
        try:
            graph_data = self.graphs_collection.find_one({"recipe_id": self.recipe_id})
            
            if graph_data and 'graph_data' in graph_data:
                data = graph_data['graph_data']
                G = nx.DiGraph()
                
                # Add nodes with their attributes including shape
                for node in data.get('nodes', []):
                    shape = node.get('shape', 'ellipse')
                    G.add_node(node['id'], shape=shape, **node.get('attributes', {}))
                
                # Add edges with their attributes
                for edge in data.get('edges', []):
                    G.add_edge(edge['source'], edge['target'], **edge.get('attributes', {}))
                
                return G
            return nx.DiGraph()
            
        except Exception as e:
            print(f"Error loading graph data: {e}")
            return nx.DiGraph()
    
    def save_data(self) -> bool:
        """
        Save current graph data to MongoDB.
        
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Create a custom dictionary representation of the graph
            data = {
                'nodes': [],
                'edges': []
            }
            
            # Add nodes and their attributes
            for node, attrs in self.current_graph.nodes(data=True):
                node_data = {
                    'id': node,
                    'shape': attrs.get('shape', 'ellipse'),
                    'attributes': {key: value for key, value in attrs.items() if key != 'shape'}
                }
                data['nodes'].append(node_data)
            
            # Add edges and their attributes
            for source, target, attrs in self.current_graph.edges(data=True):
                edge_data = {
                    'source': source,
                    'target': target,
                    'attributes': attrs
                }
                data['edges'].append(edge_data)
            
            # Update or insert the graph data
            self.graphs_collection.update_one(
                {"recipe_id": self.recipe_id},
                {
                    "$set": {
                        "graph_data": data,
                        "last_updated": datetime.datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
            
        except Exception as e:
            print(f"Error saving graph data: {e}")
            return False
    
    def clear_data(self) -> None:
        """Clear all existing graph data for this recipe."""
        self.current_graph = nx.DiGraph()
        self.graphs_collection.delete_one({"recipe_id": self.recipe_id})


# Rest of the code remains the same...


def create_measurement_subgraph(G: nx.DiGraph, parent_node: str, 
                              measurement: str = "", quantity: str = "") -> None:
    global_measurement_counter = 1
    """
    Create measurement-related nodes and edges for a given parent node.
    
    Args:
        G: NetworkX DiGraph object
        parent_node: Node to attach measurements to
        measurement: Measurement unit value
        quantity: Quantity value
    """
    if not (measurement or quantity):
        return
        
    mod_measure_node = f"mod_measure_{parent_node}"
    measure_node = f"[meas_1_{parent_node}]"
    if measurement and quantity:
        G.add_node(mod_measure_node, node_type='mod_measure', label="mod_")
        G.add_node(measure_node, node_type='measure', label=f"[measure_{global_measurement_counter}]")
        G.add_edge(parent_node, mod_measure_node)
        G.add_edge(mod_measure_node, measure_node)
    
        if measurement:
            unit_node = f"unit_{measurement}"
            G.add_node(unit_node, node_type='unit', label=measurement)
            G.add_edge(measure_node, unit_node)
            
            value_node = str(measurement)
            G.add_node(value_node, node_type='unit_value', label=measurement)
            G.add_edge(unit_node, value_node)
            
        if quantity:
            quantity_node = f"count_{quantity}"
            G.add_node(quantity_node, node_type='quantity', label=quantity)
            G.add_edge(measure_node, quantity_node)
            
            value_node = str(quantity)
            G.add_node(value_node, node_type='quantity_value', label=quantity)
            G.add_edge(quantity_node, value_node)
    


def handle_span_relationship(G, relation_node, noun_rel, root_node):
    """
    Handle span relationship in the graph structure for cooking instructions.
    Includes support for noun intensifiers.
    
    Args:
        G: NetworkX DiGraph object
        relation_node: String identifier for the relation node
        noun_rel: Dictionary containing noun relationship data
        root_node: String identifier for the root verb+tam node
    """
    global_measurement_counter = 1
    global_span_counter = 1
    
    # Create span node
    span_node = f"span_dynamic_1_{uuid.uuid4().hex[:6]}"
    G.add_node(span_node, node_type='span_dynamic', label=f"[span_{global_span_counter}]")
    G.add_edge(relation_node, span_node)
    
    def add_modifier_with_intensifier(G, noun_node, noun, noun_rel):
        """Helper function to add modifier and intensifier nodes for a noun"""
        if noun not in noun_rel['nounModifiers']:
            return
            
        modifiers = noun_rel['nounModifiers'][noun]
        intensifiers = noun_rel.get('nounIntensifiers', {}).get(noun, [])
        
        # Zip modifiers with intensifiers, padding shorter list with None
        for idx, modifier in enumerate(modifiers):
            mod_node = f"mod_{noun}_{uuid.uuid4().hex[:6]}"
            G.add_node(mod_node, node_type='mod', label="mod")
            G.add_edge(noun_node, mod_node)

            modifier_node = f"modifier_{modifier}_{uuid.uuid4().hex[:6]}"
            G.add_node(modifier_node, node_type='modifier', label=modifier)

            # Connect mod -> modifier
            G.add_edge(mod_node, modifier_node)

            # Add intensifier if available
            if idx < len(intensifiers) and intensifiers[idx]:
                intensifier = intensifiers[idx]
                intf_node = f"intf_{uuid.uuid4().hex[:6]}"  # Intermediate intf node
                intensifier_node = f"intensifier_{intensifier}_{uuid.uuid4().hex[:6]}"

                G.add_node(intf_node, node_type='intf', label="intf")
                G.add_node(intensifier_node, node_type='intensifier', label=intensifier)

                # Connect modifier -> intf -> intensifier
                G.add_edge(modifier_node, intf_node)
                G.add_edge(intf_node, intensifier_node)
    
    def add_measurements(G, noun_node, noun, noun_rel, counter):
        """Helper function to add measurement and quantity nodes for a noun"""
        if noun not in noun_rel['measurements'] and noun not in noun_rel['quantities']:
            return counter  # Return unchanged counter if no measurements to add
            
        mod_measure_node = f"mod_measure_{noun}_{uuid.uuid4().hex[:6]}"
        G.add_node(mod_measure_node, node_type='mod_measure', label="mod")
        G.add_edge(noun_node, mod_measure_node)
        
        measure_node = f"[measure_1_{noun}_{uuid.uuid4().hex[:6]}]"
        G.add_node(measure_node, node_type='measure', label=f"[meas_{counter}]")
        G.add_edge(mod_measure_node, measure_node)
        
        if noun in noun_rel['measurements']:
            unit_node = f"unit_{noun}_{uuid.uuid4().hex[:6]}"
            G.add_node(unit_node, node_type='unit', label="unit")
            G.add_edge(measure_node, unit_node)
            
            unit_value = noun_rel['measurements'][noun]
            unit_value_node = f"unit_value_{unit_value}_{uuid.uuid4().hex[:6]}"
            G.add_node(unit_value_node, node_type='unit_value', label=unit_value)
            G.add_edge(unit_node, unit_value_node)
        
        if noun in noun_rel['quantities']:
            quantity_node = f"count_{noun}_{uuid.uuid4().hex[:6]}"
            G.add_node(quantity_node, node_type='quantity', label="quantity")
            G.add_edge(measure_node, quantity_node)
            
            quantity_value = str(noun_rel['quantities'][noun])
            quantity_value_node = f"quantity_value_{quantity_value}_{uuid.uuid4().hex[:6]}"
            G.add_node(quantity_value_node, node_type='quantity_value', label=quantity_value)
            G.add_edge(quantity_node, quantity_value_node)
        
        return counter + 1  # Return incremented counter
    
    # Handle start node and its components
    start_node = f"start_{uuid.uuid4().hex[:6]}"
    G.add_node(start_node, node_type='start', label="start")
    G.add_edge(span_node, start_node)
    
    start_noun = noun_rel['startNoun']
    start_noun_node = f"noun_start_{start_noun}_{uuid.uuid4().hex[:6]}"
    G.add_node(start_noun_node, node_type='noun', label=start_noun)
    G.add_edge(start_node, start_noun_node)
    
    # Add modifiers and intensifiers for start noun
    add_modifier_with_intensifier(G, start_noun_node, start_noun, noun_rel)
    
    # Add measurements for start noun
    global_measurement_counter = add_measurements(G, start_noun_node, start_noun, noun_rel, global_measurement_counter)
    
    # Handle end node and its components
    end_node = f"end_{uuid.uuid4().hex[:6]}"
    G.add_node(end_node, node_type='end', label="end")
    G.add_edge(span_node, end_node)
    
    end_noun = noun_rel['endNoun']
    end_noun_node = f"noun_end_{end_noun}_{uuid.uuid4().hex[:6]}"
    G.add_node(end_noun_node, node_type='noun', label=end_noun)
    G.add_edge(end_node, end_noun_node)
    
    # Add modifiers and intensifiers for end noun
    add_modifier_with_intensifier(G, end_noun_node, end_noun, noun_rel)
    
    # Add measurements for end noun
    global_measurement_counter = add_measurements(G, end_noun_node, end_noun, noun_rel, global_measurement_counter)
def create_graph_from_instruction(
    instruction_data: Dict,
    graph_manager: Optional[GraphDataManager] = None
) -> nx.DiGraph:
    """
    Create or update a tree-like graph from instruction data with proper string handling.
    Skips creation of nodes when values are empty and prevents displaying None values.

    Args:
        instruction_data: Dictionary containing instruction components
        graph_manager: Optional GraphDataManager instance

    Returns:
        NetworkX DiGraph object
    """
    # Initialize counters as function attributes instead of globals
    counters = {
        'span': 1,
        'conjunction': 1,
        'measurement': 1,
         'rate': 1 
    }
    
    if graph_manager is None:
        graph_manager = GraphDataManager()

    G = graph_manager.current_graph.copy() if graph_manager.current_graph else nx.DiGraph()

    # Find existing verb+TAM node
    existing_verb_tam = next(
        (node for node, attrs in G.nodes(data=True)
         if attrs.get('node_type') == 'verb_tam'),
        None
    )

    # Process verb and TAM
    verb = str(instruction_data.get('verb', '')) if instruction_data.get('verb') is not None else ''
    tam = str(instruction_data.get('tam', '')) if instruction_data.get('tam') is not None else ''

    # Set root node
    root_node = None
    if verb and tam:
        verb_tam_node = f"verb_tam_{verb}_{tam}_{uuid.uuid4().hex[:6]}"
        G.add_node(verb_tam_node, node_type='verb_tam', label=f"{verb}-{tam}")
        root_node = verb_tam_node
        counters['conjunction'] = 1
    else:
        root_node = existing_verb_tam

    if not root_node:
        return G
    


    def add_measurement_nodes(G, parent_node, measurement, quantity, prefix, counters):
        """Helper function to add measurement and quantity nodes"""
        if not measurement and not quantity:
            return

        # Create measure node if parent_node contains "start" or "end"
        if "start" in parent_node or "end" in parent_node:
            meas_node = f"measure_{prefix}_{counters['measurement']}_{uuid.uuid4().hex[:6]}"
            G.add_node(meas_node, node_type='measure', label=f"[meas_{counters['measurement']}]")
            G.add_edge(parent_node, meas_node)
            counters['measurement'] += 1
        else:
        # Create rmeas node and connect it to measure node
            meas_node = f"measure_{prefix}_{counters['measurement']}_{uuid.uuid4().hex[:6]}"
            rmeas_node = f"rmeas__{uuid.uuid4().hex[:6]}"
            G.add_node(rmeas_node, node_type='rmeas', label="rmeas")
            G.add_node(meas_node, node_type='measure', label=f"[meas_{counters['measurement']}]")
            G.add_edge(parent_node, rmeas_node)
            G.add_edge(rmeas_node, meas_node)
            counters['measurement'] += 1

        # Create quantity and quantity_value nodes if quantity is provided
        if quantity is not None:
            quantity_node = f"count_{prefix}_{uuid.uuid4().hex[:6]}"
            G.add_node(quantity_node, node_type='quantity', label="quantity")
            G.add_edge(meas_node, quantity_node)

            quantity_value = f"quantity_value_{prefix}_{uuid.uuid4().hex[:6]}"
            G.add_node(quantity_value, node_type='quantity_value', label=str(quantity))
            G.add_edge(quantity_node, quantity_value)

        # Create unit and unit_value nodes if measurement is provided
        if measurement:
            unit_node = f"unit_{prefix}_{uuid.uuid4().hex[:6]}"
            G.add_node(unit_node, node_type='unit', label="unit")
            G.add_edge(meas_node, unit_node)

            unit_value = f"unit_value_{prefix}_{uuid.uuid4().hex[:6]}"
            G.add_node(unit_value, node_type='unit_value', label=str(measurement))
            G.add_edge(unit_node, unit_value)

    def add_modifier_nodes(G, noun_node, modifier, intensifier=None):
  
        if not modifier:
            return
        
        mod_node = f"mod_{uuid.uuid4().hex[:6]}"
        
        G.add_node(mod_node, node_type="mod", label="mod")
        G.add_edge(noun_node, mod_node)

        modifier_node = f"modifier_{modifier}_{uuid.uuid4().hex[:6]}"
        G.add_node(modifier_node, node_type="modifier", label=modifier)

        # Connect mod → modifier
        G.add_edge(mod_node, modifier_node)

        if intensifier:
            intf_node = f"intf_{uuid.uuid4().hex[:6]}"  # Intermediate intf node
            intensifier_node = f"intensifier_{intensifier}_{uuid.uuid4().hex[:6]}"

            G.add_node(intf_node, node_type="intf", label="intf")
            G.add_node(intensifier_node, node_type="intensifier", label=intensifier)

            # Connect modifier → intf → intensifier
            G.add_edge(modifier_node, intf_node)
            G.add_edge(intf_node, intensifier_node)


    def handle_span_measurement(G, parent_node, measurement_data, prefix, counters):
        """Helper function to handle span measurements"""
        start_measurement = measurement_data.get(f'start{prefix}Measurement')
        start_quantity = measurement_data.get(f'start{prefix}Quantity')
        end_measurement = measurement_data.get(f'end{prefix}Measurement')
        end_quantity = measurement_data.get(f'end{prefix}Quantity')
        
        # Create start and end nodes
        start_node = f"start_{uuid.uuid4().hex[:6]}"
        end_node = f"end_{uuid.uuid4().hex[:6]}"
        G.add_node(start_node, node_type='start', label="start")
        G.add_node(end_node, node_type='end', label="end")
        G.add_edge(parent_node, start_node)
        G.add_edge(parent_node, end_node)
        
        # Add measurements
        add_measurement_nodes(G, start_node, start_measurement, start_quantity, 'start', counters)
        add_measurement_nodes(G, end_node, end_measurement, end_quantity, 'end', counters)

    # Process noun relations
    for idx, noun_rel in enumerate(instruction_data.get('nounRelations', [])):
        relation = str(noun_rel.get('relation', '')) if noun_rel.get('relation') is not None else ''
        if not relation:
            continue

        relation_node = f"relation_{relation}_{idx}_{uuid.uuid4().hex[:6]}"
        G.add_node(relation_node, node_type='relation', label=relation)
        G.add_edge(root_node, relation_node)

        relation_type = noun_rel.get('relationType')
        
        if relation_type == 'SimpleConcept':
            noun = str(noun_rel.get('noun', ''))
            if not noun:
                continue
                
            noun_node = f"noun_{relation}_{noun}_{uuid.uuid4().hex[:6]}"
            G.add_node(noun_node, node_type='noun', label=noun)
            G.add_edge(relation_node, noun_node)
            number = str(noun_rel.get('number', ''))
            number_node = f"number_{number}_{uuid.uuid4().hex[:6]}"
            num_node = f"num__{uuid.uuid4().hex[:6]}"
            if number:
                G.add_node(num_node, node_type='card',label=f"card")
                G.add_node(number_node,node_type='number',label=number)
                G.add_edge(noun_node, num_node)
                G.add_edge(num_node,number_node)

            quantity = str(noun_rel.get('quantity',''))
    
            quantity_node = f"quantity_{quantity}_{uuid.uuid4().hex[:6]}"
            quant_node = f"quantity__{uuid.uuid4().hex[:6]}"
            measurement = noun_rel.get('measurement', None)
            measurements = noun_rel.get('measurements', {})

            if quantity and quantity != 'None' and measurement is None and not measurements:  
                G.add_node(quant_node,node_type='quant_label',label=f'quant')
                G.add_node(quantity_node,node_type='quant',label=quantity)
                G.add_edge(noun_node,quant_node)
                G.add_edge(quant_node,quantity_node)

            add_modifier_nodes(G, noun_node, noun_rel.get('modifier'), noun_rel.get('intensifier'))
            
            if noun_rel.get('complexType') == 'span':
                span_node = f"span_dynamic_{counters['span']}_{uuid.uuid4().hex[:6]}"
                rmeas_node = f"rmeas__{uuid.uuid4().hex[:6]}"
                G.add_node(span_node, node_type='span_dynamic', label=f"[span_{counters['span']}]")
                G.add_node(rmeas_node, node_type='rmeas',label=f"rmeas")
                G.add_edge(noun_node, rmeas_node)
                G.add_edge(rmeas_node,span_node)
                counters['span'] += 1
                
                handle_span_measurement(G, span_node, noun_rel, '', counters)

            elif noun_rel.get('complexType') == 'rate':
                rate_node = f"rate_dynamic_{counters['rate']}_{uuid.uuid4().hex[:6]}"
                rmeas_node = f"rmeas__{uuid.uuid4().hex[:6]}"
                G.add_node(rate_node, node_type='rate_dynamic', label=f"[rate_{counters['rate']}]")
                G.add_node(rmeas_node, node_type='rmeas', label="rmeas")
                G.add_edge(noun_node, rmeas_node)
                G.add_edge(rmeas_node, rate_node)
                counters['rate'] += 1
                # print(noun_rel)
                handle_rate_measurement(G, rate_node, noun_rel, '', counters)
            else:
                add_measurement_nodes(G, noun_node, 
                                   noun_rel.get('measurement'),
                                   noun_rel.get('quantity'),
                                   'simple',
                                   counters)
                
        elif relation_type in ['Conjoined', 'Disjoined']:
            connector_type = 'conj' if relation_type == 'Conjoined' else 'disj'
            connector_node = f"{connector_type}_{counters['conjunction']}_{uuid.uuid4().hex[:6]}"
            G.add_node(connector_node, node_type=connector_type, 
                      label=f"[{connector_type}_{counters['conjunction']}]")
            G.add_edge(relation_node, connector_node)
            counters['conjunction'] += 1
            
            for noun_idx, noun in enumerate(noun_rel.get('selectedNouns', []), 1):
                if not noun:
                    continue
                    
                opt_node = f"op_{noun_idx}_{uuid.uuid4().hex[:6]}"
                G.add_node(opt_node, node_type='option', label=f"op{noun_idx}")
                G.add_edge(connector_node, opt_node)
                
                noun_node = f"noun_{relation}_{noun}_{noun_idx}_{uuid.uuid4().hex[:6]}"
                G.add_node(noun_node, node_type='noun', label=noun)
                G.add_edge(opt_node, noun_node)
                
                # Handle modifiers and intensifiers
                modifiers = noun_rel.get('nounModifiers', {}).get(noun, [])
                intensifiers = noun_rel.get('nounIntensifiers', {}).get(noun, [])
                
                # Zip modifiers with intensifiers, padding shorter list with None
                mod_int_pairs = itertools.zip_longest(modifiers, intensifiers)
                
                for modifier, intensifier in mod_int_pairs:
                    if isinstance(modifier, dict):
                        # Handle case where modifier is a dictionary
                        add_modifier_nodes(G, noun_node, 
                                        modifier.get('modifier'), 
                                        modifier.get('intensifier'))
                    elif modifier:
                        # Handle case where modifier is a string
                        add_modifier_nodes(G, noun_node, modifier, intensifier)
                
                # Handle measurements
                if noun_rel.get('measureTypes', {}).get(noun) == 'complex':
                   
                    span_node = f"span_dynamic_{counters['span']}_{uuid.uuid4().hex[:6]}"
                    rmeas_node = f"rmeas__{uuid.uuid4().hex[:6]}"
            
                    G.add_node(rmeas_node, node_type='rmeas',label=f"rmeas")
                    G.add_edge(noun_node, rmeas_node)
                    G.add_node(span_node, node_type='span_dynamic', 
                             label=f"[span_{counters['span']}]")
                    G.add_edge(rmeas_node, span_node)
                    counters['span'] += 1
                    
                    measurement_data = {
                        'startMeasurement': noun_rel.get('startMeasurements', {}).get(noun),
                        'startQuantity': noun_rel.get('startQuantities', {}).get(noun),
                        'endMeasurement': noun_rel.get('endMeasurements', {}).get(noun),
                        'endQuantity': noun_rel.get('endQuantities', {}).get(noun)
                    }
                    handle_span_measurement(G, span_node, measurement_data, '', counters)
                
                elif noun_rel.get('measureTypes', {}).get(noun) == 'rate':
                   
                    rate_node = f"rate_dynamic_{counters['rate']}_{uuid.uuid4().hex[:6]}"
                    rmeas_node = f"rmeas__{uuid.uuid4().hex[:6]}"
            
                    G.add_node(rmeas_node, node_type='rmeas',label=f"rmeas")
                    G.add_edge(noun_node, rmeas_node)
                    G.add_node(rate_node, node_type='rate_dynamic', 
                             label=f"[rate_{counters['rate']}]")
                    G.add_edge(rmeas_node, rate_node)
                    counters['rate'] += 1
                    
                    rate_data = {
                        'unit_every': noun_rel.get('unitEveryMeasurements', {}).get(noun),
                        'every_count': noun_rel.get('unitEveryQuantities', {}).get(noun),
                        'unit_value': noun_rel.get('unitValueMeasurements', {}).get(noun),
                        'value_count': noun_rel.get('unitValueQuantities', {}).get(noun)
                    }
                    handle_rate_measurement(G, rate_node, rate_data, '', counters)
                elif noun_rel.get('measureTypes', {}).get(noun) == 'simple':
                        measurements = noun_rel.get('measurements', {})
                        quantities = noun_rel.get('quantities', {})

                        # Handle missing 'number' gracefully
                        final_number = (noun_rel.get('number') or {}).get(noun, None)
                        if final_number:
                            number_node = f"number_{final_number}_{uuid.uuid4().hex[:6]}"
                            num_node = f"num__{uuid.uuid4().hex[:6]}"
                            G.add_node(num_node, node_type='card', label="card")
                            G.add_node(number_node, node_type='number', label=final_number)
                            G.add_edge(noun_node, num_node)
                            G.add_edge(num_node, number_node)

                        # Safely handle 'quantity'
                        quantity_data = noun_rel.get('quantity') or {}
                        quantity = str(quantity_data.get(noun, ""))
                        quantity_node = f"quantity_{quantity}_{uuid.uuid4().hex[:6]}"
                        quant_node = f"quantity__{uuid.uuid4().hex[:6]}"
                        measurement = noun_rel.get('measurement', None)

                        if quantity and measurement is None and not measurements:
                            G.add_node(quant_node, node_type='quant_label', label='quant')
                            G.add_node(quantity_node, node_type='quant', label=quantity)
                            G.add_edge(noun_node, quant_node)
                            G.add_edge(quant_node, quantity_node)


                        if noun in measurements or noun in quantities:
                            add_measurement_nodes(G, noun_node,
                                                measurements.get(noun, ""),
                                                quantities.get(noun, ""),
                                                'conj',
                                                counters)

        elif noun_rel.get('relationType') in ['Span']:
            
                # Process span relationship using dedicated function
                handle_span_relationship(G, relation_node, noun_rel, root_node)
        

    graph_manager.current_graph = G
    graph_manager.save_data()
    return G
def generate_graph_image(G: nx.DiGraph) -> str:
    """
    Generate visualization of the graph using Graphviz with a focus on displaying labels.
    
    Args:
        G: NetworkX DiGraph object
        
    Returns:
        Base64 encoded string of the graph image
    """
    dot = graphviz.Digraph(format='png', engine='dot')
    
    NODE_COLORS = {
        'verb_tam': '#80C7FF',  
        'noun': '#FF7F7F',      
        'relation': '#A3F7BF',  # Lightened
        'ingredient': '#F9E470',
        'modifier': '#BFA6FF',  # Lightened
        'quantity_value': '#FFB6D1',  
        'unit_value': '#B2D8F7',  
        'instruction': '#A3F7BF',  # Lightened
        'conj': '#FFD599',  # Lightened
        'measuring_unit': '#C2DCFF',  # Lightened
        'measurements': '#A3F7BF',  # Lightened
        'mod': '#A3F7BF',  # Lightened
        'card':'#A3F7BF',
        'mod_measure': '#A3F7BF',
        'measure': '#FFD599',  # Lightened
        'quantity': '#F8C2FF',  # Lightened
        'unit': '#F7E09A',  # Lightened
        'intensifier': '#FFA588',  # Lightened
        'span_dynamic': '#66FF80',  # Lightened
        'intf': '#A3F7BF',  # Lightened
        'rmeas': '#A3F7BF',  # Lightened
        'rate_dynamic': '#E5FFE9',  # Lightened
        'unit_every': '#FFD699',  # Added with a light shade
        'quant_label':'#A3F7BF',
    }


    
    ELLIPSE_NODES = {'unit', 'relation', 'quantity', 'mod_measure', 'mod','option' ,'start','end','intf','rmeas','unit_every','unit_label','num','quant_label','card'}
    
    # Add nodes with labels
    for node, attr in G.nodes(data=True):
        node_type = attr.get('node_type', '')
        if node_type=='quantity':
            label='count'
        else:
            label = attr.get('label', node)  # Use 'label' if available, fallback to node ID
        shape = 'ellipse' if node_type in ELLIPSE_NODES else 'rectangle'
        color = NODE_COLORS.get(node_type, '#34A853')
        
        dot.node(
            node, 
            label,  # Display label on the node
            style='filled',
            fillcolor=color,
            shape=shape,
            fontsize='12'  # Font size for better visibility
        )
    
    # Add edges with labels (if any)
    for u, v, edge_attr in G.edges(data=True):
        edge_label = edge_attr.get('label', '')  # Use 'label' if available
        u_type = G.nodes[u].get('node_type', '')
        v_type = G.nodes[v].get('node_type', '')
        
        if u_type == 'option' and v_type == 'noun'  or u_type == 'start' and v_type == 'measure' or u_type == 'end' and v_type == 'measure' or u_type=="unit" and v_type=='unit_value' or u_type=='quantity' and v_type=="quantity_value" or u_type=="unit_every" and v_type=="measure" or u_type=="unit_label" and v_type=="measure" or u_type=="num" and v_type=="number":
            dot.edge(u, v, arrowhead='box', label=edge_label, fontsize='12')  # Square arrowhead
        elif u_type in {'relation', 'mod', 'mod_measure','intf','rmeas','quant_label'} or v_type in {'noun', 'span_dynamic','modifier', 'meas_1','intensifier','rate_dynamic','quant','card'}:
            dot.edge(u, v, arrowhead='normal', label=edge_label, fontsize='12')  # Normal arrowhead
        else:
            dot.edge(u, v, dir='none', label=edge_label, fontsize='12')  # No arrowhead
    
    # Render and return base64 encoded image
    buf = io.BytesIO()
    buf.write(dot.pipe())
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

def generate_hindi_sentence(G: nx.DiGraph) -> str:
    """
    Generate Hindi sentence from the graph structure.
    
    Args:
        G: NetworkX DiGraph object
        
    Returns:
        str: Generated Hindi sentence
    """
    sentence_parts = []
    
    # Find verb+TAM node
    verb_tam_node = next(
        (node for node in G.nodes() if 'क्रिया+काल' in node),
        None
    )
    
    if not verb_tam_node:
        return ""
        
    # Process relations
    for relation_node in G.successors(verb_tam_node):
        if 'संबंध' not in relation_node:
            continue
            
        relation = relation_node.split(':\n')[1]
        
        for connected_node in G.successors(relation_node):
            if 'संज्ञा' in connected_node:
                noun = connected_node.split(': ')[1]
                sentence_parts.append(f"{noun} के साथ {relation}")
            elif 'सामग्री' in connected_node:
                ingredient = connected_node.split(': ')[1]
                if not sentence_parts:
                    sentence_parts.append(f"{ingredient} का उपयोग करके")
                else:
                    sentence_parts.append(f"और {ingredient} का उपयोग")
    
    # Add verb+TAM
    verb_tam_text = verb_tam_node.split(': ')[1]
    sentence_parts.append(verb_tam_text)
    
    return ' '.join(sentence_parts)

def clear_graph_data(graph_manager):
    """Clear all existing graph data"""
    graph_manager.current_graph = nx.DiGraph()
    graph_manager.save_data()
