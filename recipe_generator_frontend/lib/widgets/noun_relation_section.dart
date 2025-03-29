import 'package:flutter/material.dart';
import 'relation_components.dart';
import 'relation_utils.dart';
import 'modifier_wizard.dart';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';




class NounRelationSection extends StatefulWidget {
  final List<Map<String, dynamic>> instructions;
  final List<String> nouns;
  final List<String> relations;
  final List<String> modifiers;
  final List<String>intensifiers;
  final List<String> measurements;
  final List<String> dquantities;
  final Function(List<Map<String, dynamic>>) onUpdate;

  const NounRelationSection({
    Key? key,
    required this.instructions,
    required this.nouns,
    required this.relations,
    required this.modifiers,
    required this.intensifiers,
    required this.measurements,
    required this.dquantities,
    required this.onUpdate,
  }) : super(key: key);

  @override
  _NounRelationSectionState createState() => _NounRelationSectionState();
}


class _NounRelationSectionState extends State<NounRelationSection> {
  String _searchQuery = '';
  void _handleUpdate(Map<String, dynamic> updatedNounRelation) {
  final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);

  // Get the noun from updatedNounRelation
  final String? targetNoun = updatedNounRelation['selectedNouns']?.first;
  
  // Find the nounRelation to update
  final nounRelationIndex = updatedInstructions.indexWhere((instruction) =>
      instruction['nounRelations'] != null &&
      instruction['nounRelations']
          .any((relation) => relation == updatedNounRelation));

  if (nounRelationIndex >= 0 && targetNoun != null) {
    final relationIndex = updatedInstructions[nounRelationIndex]['nounRelations']
        .indexOf(updatedNounRelation);

    // Extract complexType from measureTypes and add it to the update
    final measureTypes = updatedNounRelation['measureTypes'] as Map<String, String>?;
    final complexType = measureTypes?[targetNoun];

    updatedInstructions[nounRelationIndex]['nounRelations'][relationIndex] = {
      ...updatedNounRelation,
      'complexType': complexType ?? 'simple',  // Fallback to 'simple' if not found
    };

    widget.onUpdate(updatedInstructions);  // Notify parent about updated instructions
  }
}


  void addNounRelationPair(int instructionIndex) {
  final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
  var currentInstruction = updatedInstructions[instructionIndex];
  
  if (currentInstruction['nounRelations'] == null) {
    currentInstruction['nounRelations'] = <Map<String, dynamic>>[];
  }
  
  currentInstruction['nounRelations'].add({
    'noun': null,
    'relation': null,
    'relationType': null,
    'complexTypeSelection': null, // Added for storing the complex type selection
    'modifier': null,
    'measurement': null,
    'quantity': null,
    'dquantity': <String, List<String>>{},
    'selectedNouns': <String>[],
    'nounModifiers': <String, List<String>>{},
    'nounIntensifiers': <String, List<String>>{},
    'measurements': <String, String>{},
    'quantities': <String, double>{},
    'unitEveryMeasurements': <String, String>{},
    'unitEveryQuantities': <String, double>{},
    'unitValueMeasurements': <String, String>{},
    'unitValueQuantities': <String, double>{},
  });
  
  widget.onUpdate(updatedInstructions);
}

  void clearRelationField(Map<String, dynamic> nounRelation, String field) {
    setState(() {
      nounRelation[field] = null;
    });
  }

Future<void> addCustomOptionToDB(String category,
    {String? subcategory, required String option}) async {
  const String url = 'http://127.0.0.1:2000/add-option';
  final payload = {
    "category": category,
    "option": option,
    if (subcategory != null) "subcategory": subcategory,
  };
  try {
    final response = await http.post(Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(payload));
    final message = response.statusCode == 200
        ? '$option added successfully!'
        : 'Failed to add custom option.';
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(message)));
  } catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Error adding custom option.')),
    );
  }
}




Widget _buildSelectedModifiersAndMeasurements(
    Map<String, dynamic> nounRelation, String targetNoun) {
  // Retrieve modifiers and intensifiers for the target noun.
  final modifiers = (nounRelation['nounModifiers'] as Map<String, List<String>>?)
          ?[targetNoun] ??
      [];
  final intensifiers =
      (nounRelation['nounIntensifiers'] as Map<String, List<String>>?)
              ?[targetNoun] ??
          [];
  // Determine the measurement type; default is 'simple'
  final measureType =
      (nounRelation['measureTypes'] as Map<String, String>?)?[targetNoun] ??
          'simple';

  // For cleaner structure, use a switch-like conditional.
  if (measureType == 'complex') {
    // Complex measurements: show start and end values.
    final startMeasurement =
        (nounRelation['startMeasurements'] as Map<String, String>?)
            ?[targetNoun];
    final startQuantity =
        (nounRelation['startQuantities'] as Map<String, double>?)
            ?[targetNoun]
            ?.toString();
    final endMeasurement =
        (nounRelation['endMeasurements'] as Map<String, String>?)
            ?[targetNoun];
    final endQuantity =
        (nounRelation['endQuantities'] as Map<String, double>?)
            ?[targetNoun]
            ?.toString();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('$targetNoun:',
            style:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        if (modifiers.isNotEmpty)
          _buildExpandableRow('Modifiers', modifiers.join(', ')),
        if (intensifiers.isNotEmpty)
          _buildExpandableRow('Intensifiers', intensifiers.join(', ')),
        if (startMeasurement != null && startQuantity != null)
          _buildExpandableRow('Start', '$startQuantity $startMeasurement'),
        if (endMeasurement != null && endQuantity != null)
          _buildExpandableRow('End', '$endQuantity $endMeasurement'),
        const SizedBox(height: 10),
      ],
    );
  } else if (measureType == 'rate') {
    // Rate measurements: show details for "unit every" and "unit value".
    final unitEveryMeasurement =
        (nounRelation['unitEveryMeasurements'] as Map<String, String>?)
            ?[targetNoun];
    final unitEveryQuantity =
        (nounRelation['unitEveryQuantities'] as Map<String, double>?)
            ?[targetNoun]
            ?.toString();
    final unitValueMeasurement =
        (nounRelation['unitValueMeasurements'] as Map<String, String>?)
            ?[targetNoun];
    final unitValueQuantity =
        (nounRelation['unitValueQuantities'] as Map<String, double>?)
            ?[targetNoun]
            ?.toString();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('$targetNoun:',
            style:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        if (modifiers.isNotEmpty)
          _buildExpandableRow('Modifiers', modifiers.join(', ')),
        if (intensifiers.isNotEmpty)
          _buildExpandableRow('Intensifiers', intensifiers.join(', ')),
        if (unitEveryMeasurement != null && unitEveryQuantity != null)
          _buildExpandableRow(
              'Unit Every', '$unitEveryQuantity $unitEveryMeasurement'),
        if (unitValueMeasurement != null && unitValueQuantity != null)
          _buildExpandableRow(
              'Unit Value', '$unitValueQuantity $unitValueMeasurement'),
        const SizedBox(height: 10),
      ],
    );
  } else {
    // Simple measurement branch.
    final measurement =
        (nounRelation['measurements'] as Map<String, String>?)?[targetNoun];
    final savedQuantity =
        (nounRelation['quantities'] as Map<String, double>?)?[targetNoun];

    // Additional simple fields.
    final number =
        (nounRelation['number'] as Map<String, String>?)?[targetNoun];
    
    final Quantity =
        (nounRelation['quantity'] as Map<String, dynamic>?)
            ?[targetNoun];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('$targetNoun:',
            style:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        if (modifiers.isNotEmpty)
          _buildExpandableRow('Modifiers', modifiers.join(', ')),
        if (intensifiers.isNotEmpty)
          _buildExpandableRow('Intensifiers', intensifiers.join(', ')),
        if (measurement != null && savedQuantity != null) ...[
          _buildExpandableRow('Measurement', measurement),
          _buildExpandableRow('Quantity', savedQuantity.toString()),
        ],
        if (number != null)
          _buildExpandableRow('Number', number.toString()),
        
        if (Quantity != null)
          _buildExpandableRow('Quantity', Quantity.toString()),
        const SizedBox(height: 10),
      ],
    );
  }
}


 Widget _buildMultipleNounsModifiersAndMeasurements(Map<String, dynamic> nounRelation) {
    final selectedNouns = nounRelation['selectedNouns'] as List<String>? ?? [];
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: selectedNouns.map<Widget>((noun) {
        return _buildSelectedModifiersAndMeasurements(nounRelation, noun);
      }).toList(),
    );
  }
  
Widget _buildExpandableRow(String label, String value) {
  return Padding(
    padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 4.0),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 100,
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
              color: Colors.grey,
            ),
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(fontSize: 14),
          ),
        ),
      ],
    ),
  );
}


  void removeNounRelationPair(int instructionIndex, int relationIndex) {
    final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
    updatedInstructions[instructionIndex]['nounRelations'].removeAt(relationIndex);
    widget.onUpdate(updatedInstructions);
  }


 
 @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: widget.instructions.length,
      itemBuilder: (context, index) {
        final instruction = widget.instructions[index];
        instruction['nounRelations'] ??= [];

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
         children: [
  _buildSectionHeader(index),
  ...instruction['nounRelations'].asMap().entries.map((e) => _buildRelationCard(e, index)),
  // Add a button at the bottom of the list
  if (instruction['nounRelations'].isNotEmpty)
    _buildAddButtonRow(index),
],
        );
      },
    );
  }

  Widget _buildSectionHeader(int index) {
    final instruction = widget.instructions[index];
    // Only show the top "+" button if there are no relations yet
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        const Text('Noun-Relation Pairs:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        if (instruction['nounRelations']?.isEmpty ?? true)
          IconButton(
            icon: const Icon(Icons.add_circle),
            onPressed: () => addNounRelationPair(index),
            color: Colors.blue,
          ),
      ],
    );
  }


Widget _buildAddButtonRow(int index) {
  return Align(
    alignment: Alignment.centerRight, // Align to the right side
    child: Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: ElevatedButton.icon(
        icon: const Icon(Icons.add_circle),
        label: const Text('Add Noun-Relation Pair'),
        onPressed: () => addNounRelationPair(index),
        style: ElevatedButton.styleFrom(
          foregroundColor: Colors.white,
          backgroundColor: Colors.blue,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        ),
      ),
    ),
  );
}




 
  
    Widget _buildRelationCard(MapEntry<int, dynamic> entry, int instructionIndex) {
    final nounRelIndex = entry.key;
    final nounRelation = entry.value;

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Stack(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Select Noun Concept Type:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                // Simplified radio buttons - just SimpleConcept and ComplexConcept
                ...buildRadioButtons(
                  nounRelation,
                  ['SimpleConcept', 'ComplexConcept'],
                  2,
                  (v) {
                    setState(() {
                      // When switching to SimpleConcept, clear any complex concept selection
                      if (v == 'SimpleConcept') {
                        nounRelation['complexTypeSelection'] = null;
                      }
                      nounRelation['relationType'] = v;
                    });
                  },
                ),
                // If ComplexConcept is selected, show complex type selection
                if (nounRelation['relationType'] == 'ComplexConcept') ...[
                  const SizedBox(height: 10),
                  const Text('Select Complex Concept Type:', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w500)),
                  ...buildRadioButtons(
                    {'relationType': nounRelation['complexTypeSelection']},
                    ['Conjoined', 'Disjoined', 'Span', 'Rate', 'Location', 'Calendar', 'Temporal'],
                    3,
                    (v) {
                      setState(() {
                        nounRelation['complexTypeSelection'] = v;
                        // Also update relationType to maintain compatibility with existing code
                        nounRelation['relationType'] = v;
                      });
                    },
                  ),
                ],
                _buildRelationContent(nounRelation, instructionIndex, nounRelIndex),
              ],
            ),
          ),
          Positioned(
            top: -3,
            right: -3,
            child: IconButton(
              icon: const Icon(Icons.remove_circle),
              onPressed: () => removeNounRelationPair(instructionIndex, nounRelIndex),
              color: Colors.red,
            ),
          ),
        ],
      ),
    );
  }
  


  // Update in _NounRelationSectionState class
Widget _buildRelationContent(Map<String, dynamic> nounRelation, int instructionIndex, int nounRelIndex) {
  return Column(
    children: [
      if (nounRelation['relationType'] == 'SimpleConcept') ...[
        SimpleRelationFields(
          nouns: widget.nouns,
          modifiers: widget.modifiers,
          intensifiers:widget.intensifiers,
           relations: widget.relations,
          measurements: widget.measurements,
          dquantities: widget.dquantities,
          nounRelation: nounRelation,
          onClearField: clearRelationField,
          onRelationChanged: (updatedRelation) {
            setState(() {
              // Update the specific nounRelation in the instructions
              final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
              updatedInstructions[instructionIndex]['nounRelations'][nounRelIndex] = updatedRelation;
              widget.onUpdate(updatedInstructions);
            });
          },
        ),
        const SizedBox(height: 10),
      ],
       if (nounRelation['relationType'] == 'Span') ...[
        const Text('Select Start and End Nouns:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        // Start Noun Dropdown
     Autocomplete<String>(
  initialValue: TextEditingValue(
    text: nounRelation['startNoun'] ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.nouns;
    }
    return widget.nouns.where((noun) =>
        noun.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
      nounRelation['startNoun'] = selection;
      // Ensure selectedNouns is initialized and contains unique values.
      nounRelation['selectedNouns'] ??= [];
      if (!nounRelation['selectedNouns'].contains(selection)) {
        nounRelation['selectedNouns'].add(selection);
      }
    });
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: InputDecoration(
        labelText: 'Start Noun',
        border: const OutlineInputBorder(),
        suffixIcon: textEditingController.text.isNotEmpty
            ? IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () {
                  setState(() {
                    textEditingController.clear();
                    nounRelation['startNoun'] = '';
                  });
                },
              )
            : null,
      ),
      onChanged: (value) {
        setState(() {
          nounRelation['startNoun'] = value;
          nounRelation['selectedNouns'].add(value);
        });
      },
      onSubmitted: (value) {
        setState(() {
          nounRelation['startNoun'] = value;
          nounRelation['selectedNouns'].add(value);
          // Ensure selectedNouns is initialized and add the value if not already present.
          
          // nounRelation['selectedNouns'] ??= [];
          // if (value.isNotEmpty && !nounRelation['selectedNouns'].contains(value)) {
          //   nounRelation['selectedNouns'].add(value);
          // }
        });
      },
    );
  },
),


        const SizedBox(height: 16),
        // End Noun Dropdown
      Autocomplete<String>(
  initialValue: TextEditingValue(
    text: nounRelation['endNoun'] ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.nouns;
    }
    return widget.nouns.where((noun) =>
        noun.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
      nounRelation['endNoun'] = selection;
      // Ensure selectedNouns is initialized and contains unique values.
      nounRelation['selectedNouns'] ??= [];
      if (!nounRelation['selectedNouns'].contains(selection)) {
        nounRelation['selectedNouns'].add(selection);
      }
    });
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: InputDecoration(
        labelText: 'End Noun',
        border: const OutlineInputBorder(),
        suffixIcon: textEditingController.text.isNotEmpty
            ? IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () {
                  setState(() {
                    textEditingController.clear();
                    nounRelation['endNoun'] = '';
                  });
                },
              )
            : null,
      ),
      onChanged: (value) {
        setState(() {
          nounRelation['endNoun'] = value;
        });
      },
      onSubmitted: (value) {
        setState(() {
          nounRelation['endNoun'] = value;
          // Ensure selectedNouns is initialized and add the value if not already present.
         

          nounRelation['selectedNouns'] ??= [];
          if (value.isNotEmpty && !nounRelation['selectedNouns'].contains(value)) {
            nounRelation['selectedNouns'].add(value);
          }
        });
      },
    );
  },
),
        const SizedBox(height: 10),
       if (nounRelation['startNoun'] != null) ...[
  const SizedBox(height: 10),
  ElevatedButton.icon(
    icon: const Icon(Icons.edit),
    label: const Text('Edit Start Noun Properties'),
    onPressed: () => _showModifierWizard(nounRelation, nounRelation['startNoun']),
  ),
  const SizedBox(height: 10),
  _buildSelectedModifiersAndMeasurements(nounRelation, nounRelation['startNoun']), // Pass startNoun
],
if (nounRelation['endNoun'] != null) ...[
  const SizedBox(height: 10),
  ElevatedButton.icon(
    icon: const Icon(Icons.edit),
    label: const Text('Edit End Noun Properties'),
    onPressed: () => _showModifierWizard(nounRelation, nounRelation['endNoun']),
  ),
  const SizedBox(height: 10),
  _buildSelectedModifiersAndMeasurements(nounRelation, nounRelation['endNoun']), // Pass endNoun

         
        ],
      ],

      
      if (['Conjoined', 'Disjoined', 'Rate'].contains(nounRelation['relationType'])) ...[
  const Text('Select Noun(s):', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
  const SizedBox(height: 8),
  TextField(
    decoration: const InputDecoration(labelText: 'Search Nouns', prefixIcon: Icon(Icons.search)),
    onChanged: (v) => setState(() => _searchQuery = v.toLowerCase()),
  ),
  const SizedBox(height: 10),
  NounFilterChipList(
    nouns: widget.nouns,
    searchQuery: _searchQuery,
    selectedNouns: nounRelation['selectedNouns'] ?? [],
    onSelectionChanged: (noun, selected) => _handleNounSelection(nounRelation, noun, selected),
    onEditPressed: (noun) => _showModifierWizard(nounRelation, noun),
  ),
  const SizedBox(height: 10),
  _buildMultipleNounsModifiersAndMeasurements(nounRelation), 
],

RelationDropdown(
  relations: widget.relations,
  selectedRelation: nounRelation['relation'],
  onChanged: (value) => setState(() => nounRelation['relation'] = value),
  onClear: () => setState(() => nounRelation['relation'] = null),
),
    ],
  );
}

void _handleNounSelection(Map<String, dynamic> nounRelation, String noun, bool selected) {
  setState(() {
    if (selected) {
      nounRelation['selectedNouns'] ??= [];
      nounRelation['selectedNouns'].add(noun);

      // Initialize intensifiers map if it doesn't exist
      nounRelation['nounIntensifiers'] ??= <String, List<String>>{};

      // Call the function to add the noun to the database
      addCustomOptionToDB('nouns', option: noun);
    } else {
      nounRelation['selectedNouns']?.remove(noun);
      nounRelation['nounModifiers']?.remove(noun);
      nounRelation['nounIntensifiers']?.remove(noun); // Remove intensifiers when noun is deselected
    }
  });
}



  
 void _showModifierWizard(Map<String, dynamic> nounRelation, String noun) {
  // Get the actual type to pass to the wizard - if using complexTypeSelection, use that value
  String typeToPass = nounRelation['relationType'] == 'ComplexConcept' 
      ? nounRelation['complexTypeSelection'] ?? 'SimpleConcept'
      : nounRelation['relationType'];
      
  showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    builder: (context) => AdvancedModifierWizard(
      noun: noun,
      nounRelation: nounRelation,
      relationType: typeToPass, 
      modifiers: widget.modifiers,
      intensifiers: widget.intensifiers,
      measurements: widget.measurements,
      dquantities: widget.dquantities,
      onUpdate: _handleUpdate,
    ),
  );
}

}