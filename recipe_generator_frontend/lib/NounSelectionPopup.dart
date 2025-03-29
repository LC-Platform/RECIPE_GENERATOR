import 'package:flutter/material.dart';

class NounRelationSection extends StatefulWidget {
  final List<Map<String, dynamic>> instructions;
  final List<String> nouns;
  final List<String> relations;
  final List<String> modifiers;
  final List<String> measurements;
  final Function(List<Map<String, dynamic>>) onUpdate;

  const NounRelationSection({
    Key? key,
    required this.instructions,
    required this.nouns,
    required this.relations,
    required this.modifiers,
    required this.measurements,
    required this.onUpdate,
  }) : super(key: key);

  @override
  _NounRelationSectionState createState() => _NounRelationSectionState();
}

class _NounRelationSectionState extends State<NounRelationSection> {
  String _searchQuery = '';
  void addNounRelationPair(int instructionIndex) {
    final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
    var currentInstruction = updatedInstructions[instructionIndex];
   
    
    if (currentInstruction['nounRelations'] == null) {
      currentInstruction['nounRelations'] = <Map<String, dynamic>>[];
    }
    
    currentInstruction['nounRelations'].add({
      'noun': null,  // Changed to null since it's now a single string
      'relation': null,
      'relationType': null,
      
      'modifier': null,
      'measurement': null,
      'quantity': null,
      'selectedNouns': <String>[],
      'nounModifiers': <String, List<String>>{},
    });
    
    widget.onUpdate(updatedInstructions);
  }

  void removeNounRelationPair(int instructionIndex, int relationIndex) {
    final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
    updatedInstructions[instructionIndex]['nounRelations'].removeAt(relationIndex);
    widget.onUpdate(updatedInstructions);
  }

  void clearField(Map<String, dynamic> nounRelation, String field) {
    setState(() {
      nounRelation[field] = null;
      if (field == 'measurement') {
        nounRelation['quantity'] = null;
      }
    });
  }
Widget _buildSimpleRelationFields(Map<String, dynamic> nounRelation, int nounRelIndex) {
  return Column(
    children: [
      // Noun Dropdown
      DropdownButtonFormField<String>(
        value: nounRelation['noun'] as String?,
        items: widget.nouns.map<DropdownMenuItem<String>>((String noun) {
          return DropdownMenuItem<String>(
            value: noun,
            child: Text(noun),
          );
        }).toList(),
        onChanged: (value) {
          setState(() {
            nounRelation['noun'] = value;
          });
        },
        decoration: InputDecoration(
          labelText: 'Select Noun',
          border: const OutlineInputBorder(),
          suffixIcon: nounRelation['noun'] != null
              ? IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () => clearField(nounRelation, 'noun'),
                )
              : null,
        ),
      ),

      // Modifier Dropdown
     const SizedBox(height: 10),
DropdownButtonFormField<String>(
  value: nounRelation['modifier'],
  items: widget.modifiers.map<DropdownMenuItem<String>>((String modifier) {
    return DropdownMenuItem<String>(
      value: modifier,
      child: Text(modifier, style: const TextStyle(fontSize: 14)),
    );
  }).toList(),
  onChanged: (value) {
    setState(() {
      nounRelation['modifier'] = value;
    });
  },
  decoration: InputDecoration(
    labelText: 'Select Modifier (if any)',
    border: const OutlineInputBorder(),
    suffixIcon: nounRelation['modifier'] != null
        ? IconButton(
            icon: const Icon(Icons.clear),
            onPressed: () => clearField(nounRelation, 'modifier'),
          )
        : null,
  ),
),

const SizedBox(height: 10),

// Measurement Dropdown (Indent under Modifier)
Padding(
  padding: const EdgeInsets.only(left: 16.0), // Indentation
  child: DropdownButtonFormField<String>(
    value: nounRelation['measurement'] as String?,
    items: widget.measurements.map<DropdownMenuItem<String>>((String measurement) {
      return DropdownMenuItem<String>(
        value: measurement,
        child: Text(measurement),
      );
    }).toList(),
    onChanged: (value) {
      setState(() {
        nounRelation['measurement'] = value;
      });
    },
    decoration: InputDecoration(
      labelText: 'Measurement',
      border: OutlineInputBorder(),
      suffixIcon: nounRelation['measurement'] != null
          ? IconButton(
              icon: const Icon(Icons.clear),
              onPressed: () => clearField(nounRelation, 'measurement'),
            )
          : null,
    ),
  ),
),


      // Display Quantity field only when Measurement is selected (Indent under Measurement)
      if (nounRelation['measurement'] != null)
        Padding(
          padding: const EdgeInsets.only(left: 32.0), // Further Indentation
          child: Column(
            children: [
              const SizedBox(height: 10),
              TextField(
                controller: TextEditingController(text: nounRelation['quantity']?.toString() ?? ''),
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Quantity',
                  border: OutlineInputBorder(),
                ),
                onChanged: (value) {
                  setState(() {
                    nounRelation['quantity'] = double.tryParse(value);
                  });
                },
              ),
            ],
          ),
        ),

      const SizedBox(height: 10),

      // Display selected modifiers for the noun
      if (nounRelation['nounModifiers']?[nounRelation['noun']] != null)
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: Text(
            'Selected Modifiers: ${(nounRelation['nounModifiers'][nounRelation['noun']] as List<String>).join(', ')}',
            style: const TextStyle(
              fontSize: 14,
              fontStyle: FontStyle.italic,
            ),
          ),
        ),
        
    ],
  );
}



  List<Widget> buildRadioButtons(Map<String, dynamic> nounRelation, List<String> options, int maxInRow) {
    return [
      for (int i = 0; i < options.length; i += maxInRow)
        Row(
          children: [
            for (int j = i; j < i + maxInRow && j < options.length; j++)
              Expanded(
                child: Row(
                  children: [
                    Radio<String>(
                      value: options[j],
                      groupValue: nounRelation['relationType'] as String?,
                      onChanged: (String? value) {
                        setState(() {
                          nounRelation['relationType'] = value;
                          if (value != 'Conjoined' && value != 'Disjoined') {
                            nounRelation['selectedNouns'] = <String>[];
                            nounRelation['nounModifiers'] = <String, List<String>>{};
                          }
                        });
                      },
                    ),
                    Flexible(child: Text(options[j], overflow: TextOverflow.ellipsis)),
                  ],
                ),
              ),
          ],
        ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: widget.instructions.length,
      itemBuilder: (context, index) {
        final instruction = widget.instructions[index];
        if (instruction['nounRelations'] == null) {
          instruction['nounRelations'] = <Map<String, dynamic>>[];
        }

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Noun-Relation Pairs:',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.add_circle),
                  onPressed: () => addNounRelationPair(index),
                  color: Colors.blue,
                ),
              ],
            ),
            ...instruction['nounRelations'].asMap().entries.map((nounRelEntry) {
              final nounRelIndex = nounRelEntry.key;
              final nounRelation = nounRelEntry.value as Map<String, dynamic>;

              if (nounRelation['selectedNouns'] == null) {
                nounRelation['selectedNouns'] = <String>[];
              } else if (nounRelation['selectedNouns'] is List<dynamic>) {
                nounRelation['selectedNouns'] = List<String>.from(nounRelation['selectedNouns'] as List<dynamic>);
              }

              if (nounRelation['nounModifiers'] == null) {
                nounRelation['nounModifiers'] = <String, List<String>>{};
              } else {
                final Map<String, dynamic> originalModifiers = nounRelation['nounModifiers'] as Map<String, dynamic>;
                final Map<String, List<String>> convertedModifiers = {};
                originalModifiers.forEach((key, value) {
                  if (value is List<dynamic>) {
                    convertedModifiers[key] = List<String>.from(value);
                  } else if (value is List<String>) {
                    convertedModifiers[key] = value;
                  } else {
                    convertedModifiers[key] = <String>[];
                  }
                });
                nounRelation['nounModifiers'] = convertedModifiers;
              }

        return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Stack(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Select Noun Concept Type:',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                ...buildRadioButtons(
                  nounRelation,
                  [
                    'SimpleConcept',
                    'Conjoined',
                    'Disjoined',
                    'Span',
                    'Rate',
                    'Location',
                    'Calendar',
                    'Temporal',

                  ],
                  3,
                ),
                if (nounRelation['relationType'] == 'SimpleConcept') ...[
                  const SizedBox(height: 10),
                  _buildSimpleRelationFields(nounRelation, nounRelIndex),
                ],
                if (nounRelation['relationType'] == 'Conjoined' ||
                    nounRelation['relationType'] == 'Disjoined') ...[
                  const SizedBox(height: 10),
                  const Text(
                    'Select Noun(s) for Relation:',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    decoration: const InputDecoration(
                      labelText: 'Search Nouns',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.search),
                    ),
                    onChanged: (value) {
                      setState(() {
                        _searchQuery = value.toLowerCase();
                      });
                    },
                  ),
                  const SizedBox(height: 10),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: widget.nouns
                          .where((noun) =>
                              noun.toLowerCase().contains(_searchQuery))
                          .map((noun) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4.0),
                          child: Row(
                            children: [
                              FilterChip(
                                label: Text(noun),
                                selected: nounRelation['selectedNouns']
                                        ?.contains(noun) ??
                                    false,
                                onSelected: (bool selected) {
                                  setState(() {
                                    if (selected) {
                                      nounRelation['selectedNouns'] ??= [];
                                      nounRelation['selectedNouns'].add(noun);
                                    } else {
                                      nounRelation['selectedNouns']
                                          ?.remove(noun);
                                      nounRelation['nounModifiers']
                                          ?.remove(noun);
                                    }
                                  });
                                },
                              ),
                              if (nounRelation['selectedNouns']
                                      ?.contains(noun) ??
                                  false)
                                IconButton(
                                  icon: const Icon(Icons.edit, size: 20),
                                  color: Colors.blue,
                                  onPressed: () => _showAdvancedModifierWizard(
                                      context, noun, nounRelation),
                                ),
                            ],
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ],
                if (nounRelation['relationType'] == 'Span') ...[
  const SizedBox(height: 10),
  const Text(
    'Select Noun(s) for Span:',
    style: TextStyle(
      fontSize: 16,
      fontWeight: FontWeight.bold,
    ),
  ),
  const SizedBox(height: 8),
  TextField(
    decoration: const InputDecoration(
      labelText: 'Search Nouns',
      border: OutlineInputBorder(),
      prefixIcon: Icon(Icons.search),
    ),
    onChanged: (value) {
      setState(() {
        _searchQuery = value.toLowerCase();
      });
    },
  ),
  const SizedBox(height: 10),
  SingleChildScrollView(
    scrollDirection: Axis.horizontal,
    child: Row(
      children: widget.nouns
          .where((noun) => noun.toLowerCase().contains(_searchQuery))
          .map((noun) {
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 4.0),
          child: Row(
            children: [
              FilterChip(
                label: Text(noun),
                selected: nounRelation['selectedNouns']?.contains(noun) ?? false,
                onSelected: (bool selected) {
                  setState(() {
                    if (selected) {
                      nounRelation['selectedNouns'] ??= [];
                      nounRelation['selectedNouns'].add(noun);
                    } else {
                      nounRelation['selectedNouns']?.remove(noun);
                      nounRelation['nounModifiers']?.remove(noun);
                    }
                  });
                },
              ),
              if (nounRelation['selectedNouns']?.contains(noun) ?? false)
                IconButton(
                  icon: const Icon(Icons.edit, size: 20),
                  color: Colors.blue,
                  onPressed: () => _showAdvancedModifierWizard(
                      context, noun, nounRelation),
                ),
            ],
          ),
        );
      }).toList(),
    ),
  ),
],
const SizedBox(height: 10),
...widget.nouns.map((noun) {
  if (nounRelation['selectedNouns']?.contains(noun) ?? false) {
    return Padding(
      padding: const EdgeInsets.only(left: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Selected Modifiers for $noun: ${(nounRelation['nounModifiers']?[noun] ?? []).join(', ')}',
            style: const TextStyle(
              fontSize: 14,
              color: Colors.grey,
            ),
          ),
          // Measurement and quantity display
          if (nounRelation['relationType'] == 'Span') ...[
            // Check if start measurements or quantities exist for this noun
            if (nounRelation['startMeasurements']?[noun] != null ||
                nounRelation['startQuantities']?[noun] != null)
              Text(
                'Start Measurement: ${nounRelation['startMeasurements']?[noun] ?? 'None'}, '
                'Start Quantity: ${nounRelation['startQuantities']?[noun]?.toString() ?? 'None'}',
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                ),
              ),
            // Check if end measurements or quantities exist for this noun
            if (nounRelation['endMeasurements']?[noun] != null ||
                nounRelation['endQuantities']?[noun] != null)
              Text(
                'End Measurement: ${nounRelation['endMeasurements']?[noun] ?? 'None'}, '
                'End Quantity: ${nounRelation['endQuantities']?[noun]?.toString() ?? 'None'}',
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                ),
              ),
          ] else if (nounRelation['measurements']?[noun] != null ||
                     nounRelation['quantities']?[noun] != null)
            Text(
              'Measurement: ${nounRelation['measurements']?[noun] ?? 'None'}, '
              'Quantity: ${nounRelation['quantities']?[noun]?.toString() ?? 'None'}',
              style: const TextStyle(
                fontSize: 12,
                color: Colors.grey,
              ),
            ),
        ],
      ),
    );
  }
  
  return const SizedBox.shrink();
}).toList(),
     const SizedBox(height: 10),
                DropdownButtonFormField<String>(
                  value: nounRelation['relation'] as String?,
                  items: widget.relations
                      .map<DropdownMenuItem<String>>((String relation) {
                    return DropdownMenuItem<String>(
                      value: relation,
                      child: Text(relation),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      nounRelation['relation'] = value;
                    });
                  },
                  decoration: InputDecoration(
                    labelText: 'Select Relation',
                    border: const OutlineInputBorder(),
                    suffixIcon: nounRelation['relation'] != null
                        ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () => clearField(nounRelation, 'relation'),
                          )
                        : null,
                  ),
                ),
              ],
            ),
          ),
          Positioned(
            top: -3,
            right: -3,
            child: IconButton(
              icon: const Icon(Icons.remove_circle),
              onPressed: () => removeNounRelationPair(index, nounRelIndex),
              color: Colors.red,
            ),
          ),
        ],
      ),
    );
  

            }).toList(),
          ],
        );
      },
    );
  }
void _showAdvancedModifierWizard(BuildContext context, String noun, Map<String, dynamic> nounRelation) {
  nounRelation['nounModifiers'] ??= <String, List<String>>{};
  nounRelation['nounModifiers'][noun] ??= <String>[];

  nounRelation['measurements'] ??= <String, String>{};
  nounRelation['quantities'] ??= <String, double>{};

  nounRelation['startMeasurements'] ??= <String, String>{};
  nounRelation['startQuantities'] ??= <String, double>{};

  nounRelation['endMeasurements'] ??= <String, String>{};
  nounRelation['endQuantities'] ??= <String, double>{};

  Map<String, TextEditingController> quantityControllers = {};
  int currentStep = 0;
  bool isLoading = false;

  showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20.0)),
    ),
    builder: (BuildContext context) {
      return StatefulBuilder(
        builder: (BuildContext context, StateSetter setModalState) {
          List<String> selectedModifiers = List<String>.from(
            nounRelation['nounModifiers'][noun] ?? <String>[],
          );

          Future<void> _syncDataWithServer() async {
            setModalState(() {
              isLoading = true;
            });
            await Future.delayed(const Duration(seconds: 1));
            setModalState(() {
              isLoading = false;
            });
          }

          void goToNextStep() async {
            if (currentStep < 2) {
              if (currentStep == 1) await _syncDataWithServer();
              setModalState(() {
                currentStep++;
              });
            }
          }

          void goToPreviousStep() {
            setModalState(() {
              currentStep--;
            });
          }

          Widget buildStepContent() {
            switch (currentStep) {
              case 0: // Step 1: Select Modifiers
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Select Modifiers',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),
                    Wrap(
                      spacing: 8,
                      runSpacing: 4,
                      children: widget.modifiers.map((modifier) {
                        final isSelected = selectedModifiers.contains(modifier);
                        return FilterChip(
                          label: Text(modifier),
                          selected: isSelected,
                          onSelected: (selected) {
                            setModalState(() {
                              if (selected) {
                                selectedModifiers.add(modifier);
                              } else {
                                selectedModifiers.remove(modifier);
                              }
                              nounRelation['nounModifiers'][noun] = selectedModifiers;
                            });
                          },
                        );
                      }).toList(),
                    ),
                  ],
                );

              case 1: // Step 2: Set Measurement and Quantity
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Set Measurement and Quantity',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),

                    // **Handling SPAN relation type**
                    if (nounRelation['relationType'] == 'Span') ...[
                      // **Start Measurement & Quantity**
                      const Text("Start Measurement:", style: TextStyle(fontWeight: FontWeight.bold)),
                      DropdownButtonFormField<String>(
                        value: nounRelation['startMeasurements'][noun],
                        items: widget.measurements.map<DropdownMenuItem<String>>((String measurement) {
                          return DropdownMenuItem<String>(
                            value: measurement,
                            child: Text(measurement),
                          );
                        }).toList(),
                        onChanged: (value) {
                          setModalState(() {
                            nounRelation['startMeasurements'][noun] = value!;
                          });
                        },
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: "Select Start Measurement",
                        ),
                      ),
                      const SizedBox(height: 10),
                      TextField(
                        controller: TextEditingController(text: nounRelation['startQuantities'][noun]?.toString() ?? ''),
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Enter Start Quantity',
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          setModalState(() {
                            nounRelation['startQuantities'][noun] = double.tryParse(value);
                          });
                        },
                      ),
                      const SizedBox(height: 10),

                      // **End Measurement & Quantity**
                      const Text("End Measurement:", style: TextStyle(fontWeight: FontWeight.bold)),
                      DropdownButtonFormField<String>(
                        value: nounRelation['endMeasurements'][noun],
                        items: widget.measurements.map<DropdownMenuItem<String>>((String measurement) {
                          return DropdownMenuItem<String>(
                            value: measurement,
                            child: Text(measurement),
                          );
                        }).toList(),
                        onChanged: (value) {
                          setModalState(() {
                            nounRelation['endMeasurements'][noun] = value!;
                          });
                        },
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: "Select End Measurement",
                        ),
                      ),
                      const SizedBox(height: 10),
                      TextField(
                        controller: TextEditingController(text: nounRelation['endQuantities'][noun]?.toString() ?? ''),
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Enter End Quantity',
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          setModalState(() {
                            nounRelation['endQuantities'][noun] = double.tryParse(value);
                          });
                        },
                      ),
                    ] else ...[
                      // **Regular Measurement & Quantity Fields**
                      DropdownButtonFormField<String>(
                        value: nounRelation['measurements'][noun],
                        items: widget.measurements.map<DropdownMenuItem<String>>((String measurement) {
                          return DropdownMenuItem<String>(
                            value: measurement,
                            child: Text(measurement),
                          );
                        }).toList(),
                        decoration: const InputDecoration(
                          labelText: 'Select Measurement',
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          setModalState(() {
                            nounRelation['measurements'][noun] = value!;
                          });
                        },
                      ),
                      const SizedBox(height: 10),
                      TextField(
                        controller: quantityControllers.putIfAbsent(
                          noun,
                          () => TextEditingController(text: nounRelation['quantities'][noun]?.toString() ?? ''),
                        ),
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Enter Quantity',
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          setModalState(() {
                            nounRelation['quantities'][noun] = double.tryParse(value);
                          });
                        },
                      ),
                    ],
                  ],
                );

              default:
                return const SizedBox();
            }
          }

          return Padding(
            padding: EdgeInsets.only(
              top: 16.0,
              left: 16.0,
              right: 16.0,
              bottom: MediaQuery.of(context).viewInsets.bottom,
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                LinearProgressIndicator(
                  value: (currentStep + 1) / 3,
                  backgroundColor: Colors.grey[300],
                  valueColor: AlwaysStoppedAnimation(Theme.of(context).primaryColor),
                ),
                const SizedBox(height: 16),
                AnimatedSwitcher(
                  duration: const Duration(milliseconds: 300),
                  child: buildStepContent(),
                ),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    if (currentStep > 0)
                      ElevatedButton(onPressed: goToPreviousStep, child: const Text('Previous')),
                    if (currentStep < 1)
                      ElevatedButton(onPressed: goToNextStep, child: const Text('Next')),
                    if (currentStep == 1)
                      ElevatedButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('Save'),
                      ),
                  ],
                ),
              ],
            ),
          );
        },
      );
    },
  );
}
}