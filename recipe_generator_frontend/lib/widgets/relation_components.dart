import 'package:flutter/material.dart';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../common/modifier_selector.dart';
import '../common/quantity_selector.dart';
import '../common/custom_measure_field.dart';
import '../common/custom_measurement_fields.dart';




class SimpleRelationFields extends StatefulWidget {
  final List<String> nouns;
  final List<String> modifiers;
  final List<String> intensifiers;
  final List<String> measurements;
  final Map<String, dynamic> nounRelation;
  final List<String> dquantities;
  final Function(Map<String, dynamic>, String) onClearField;
  final Function(Map<String, dynamic>) onRelationChanged;
  final List<String> relations;

  const SimpleRelationFields({
    Key? key,
    required this.nouns,
    required this.modifiers,
    required this.intensifiers,
    required this.measurements,
    required this.nounRelation,
    required this.dquantities,
    required this.onClearField,
    required this.onRelationChanged,
    required this.relations,
  }) : super(key: key);

  @override
  _SimpleRelationFieldsState createState() => _SimpleRelationFieldsState();
}


class _SimpleRelationFieldsState extends State<SimpleRelationFields> {
  late Map<String, dynamic> _localNounRelation;
  late TextEditingController _quantityController;
  late TextEditingController _startQuantityController;
  late TextEditingController _endQuantityController;
  late TextEditingController _everyCountController;
  late TextEditingController _valueCountController;
  late TextEditingController _numberController;
  Timer? _debounceTimer;
  bool _isUpdating = false;

  @override
  void initState() {
    super.initState();
    _localNounRelation = Map<String, dynamic>.from(widget.nounRelation);
    _initializeControllers();
  }

  void _initializeControllers() {
    _quantityController = TextEditingController(
      text: _localNounRelation['quantity']?.toString() ?? ''
    );
    _startQuantityController = TextEditingController(
      text: _localNounRelation['startQuantity']?.toString() ?? ''
    );
    _endQuantityController = TextEditingController(
      text: _localNounRelation['endQuantity']?.toString() ?? ''
    );
    _everyCountController = TextEditingController(
      text: _localNounRelation['every_count']?.toString() ?? ''
    );
    _valueCountController = TextEditingController(
      text: _localNounRelation['value_count']?.toString() ?? ''
    );
    _numberController = TextEditingController(
      text: _localNounRelation['number']?.toString() ?? ''
    );
  }

  void _updateRelation(String field, dynamic value) {
    if (_isUpdating) return;
    
    _isUpdating = true;
    
    // Update local state first
    if (_localNounRelation[field] != value) {
      _localNounRelation[field] = value;

      if (field == 'measureType') {
        _handleMeasureTypeChange(value);
      }

      // Use Future.microtask to defer the callback
      Future.microtask(() {
        if (mounted) {
          widget.onRelationChanged(_localNounRelation);
        }
        _isUpdating = false;
      });
    } else {
      _isUpdating = false;
    }
  }

  void _handleTextFieldChange(String field, String value) {
  _debounceTimer?.cancel();
  
  _debounceTimer = Timer(const Duration(milliseconds: 300), () { // Reduced from 500ms
    if (!mounted) return;
    final parsedValue = double.tryParse(value);
    if (_localNounRelation[field] != parsedValue) {
      _updateRelation(field, parsedValue);
    }
  });
}

  @override
  void didUpdateWidget(SimpleRelationFields oldWidget) {
    super.didUpdateWidget(oldWidget);
    
    if (widget.nounRelation != oldWidget.nounRelation && !_isUpdating) {
      _localNounRelation = Map<String, dynamic>.from(widget.nounRelation);
      _updateControllerValues();
    }
  }

  void _updateControllerValues() {
  if (_isUpdating) return;

  _isUpdating = true;

  WidgetsBinding.instance.addPostFrameCallback((_) {
    if (mounted) {
      // Update each controller only if the value has changed
      final newQuantity = _localNounRelation['quantity']?.toString() ?? '';
      if (_quantityController.text != newQuantity) {
        _quantityController.text = newQuantity;
      }

      final newStartQuantity = _localNounRelation['startQuantity']?.toString() ?? '';
      if (_startQuantityController.text != newStartQuantity) {
        _startQuantityController.text = newStartQuantity;
      }

      final newEndQuantity = _localNounRelation['endQuantity']?.toString() ?? '';
      if (_endQuantityController.text != newEndQuantity) {
        _endQuantityController.text = newEndQuantity;
      }

      final newEveryCount = _localNounRelation['every_count']?.toString() ?? '';
      if (_everyCountController.text != newEveryCount) {
        _everyCountController.text = newEveryCount;
      }

      final newValueCount = _localNounRelation['value_count']?.toString() ?? '';
      if (_valueCountController.text != newValueCount) {
        _valueCountController.text = newValueCount;
      }
    


      _isUpdating = false;
    }
  });
}

  @override
  void dispose() {
    _debounceTimer?.cancel();
    _quantityController.dispose();
    _startQuantityController.dispose();
    _endQuantityController.dispose();
    _everyCountController.dispose();
    _valueCountController.dispose();
    _numberController.dispose();
    super.dispose();
  }


  

  
  void _handleMeasureTypeChange(String value) {
    if (value == 'complex') {
      _localNounRelation['complexType'] = 'span';
    } else {
      _localNounRelation
        ..remove('complexType')
        ..remove('startMeasurement')
        ..remove('endMeasurement')
        ..remove('startQuantity')
        ..remove('endQuantity')
        ..remove('unit_every')
        ..remove('unit_value')
        ..remove('every_count')
        ..remove('value_count');

      _startQuantityController.clear();
      _endQuantityController.clear();
      _everyCountController.clear();
      _valueCountController.clear();
    }
  }

  
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          _buildNounSection(),
           _buildModifierAndMeasurementSection(),
          // _buildModifierSection(),
          // _buildMeasureTypeSection(),
          _buildTypeSpecificFields(),
        ],
      ),
    );
  }

 

 Widget _buildNounSection() {
  bool isCustomNoun = _localNounRelation['noun'] != null &&
      !widget.nouns.contains(_localNounRelation['noun']);
  final TextEditingController customNounController = TextEditingController(
    text: isCustomNoun ? _localNounRelation['noun'] : '',
  );
  final FocusNode customNounFocusNode = FocusNode();

  return StatefulBuilder(
    builder: (context, setState) {
      void toggleCustomNounMode() {
        setState(() {
          isCustomNoun = !isCustomNoun;
          if (isCustomNoun) {
            customNounController.text = _localNounRelation['noun'] ?? '';
            Future.delayed(Duration.zero, customNounFocusNode.requestFocus);
          } else {
            if (_localNounRelation['noun'] != null &&
                !widget.nouns.contains(_localNounRelation['noun']) &&
                widget.nouns.isNotEmpty) {
              _updateRelation('noun', widget.nouns.first);
            }
          }
        });
      }

      return Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Select Noun',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              isCustomNoun
                  ? Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: customNounController,
                            focusNode: customNounFocusNode,
                            decoration: _inputDecoration('Enter Custom Noun', 'noun'),
                            onChanged: (value) => _updateRelation('noun', value),
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.save),
                          tooltip: 'Save custom noun',
                          onPressed: () {
                            final customNoun = customNounController.text.trim();
                            if (customNoun.isNotEmpty) {
                              addCustomOptionToDB('nouns', option: customNoun);
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Please enter a custom noun first.')),
                              );
                            }
                          },
                        ),
                      ],
                    )
                  : Autocomplete<String>(
                      initialValue: TextEditingValue(text: _localNounRelation['noun'] ?? ''),
                      optionsBuilder: (TextEditingValue textEditingValue) {
                        return textEditingValue.text.isEmpty
                            ? widget.nouns
                            : widget.nouns
                                .where((noun) => noun.toLowerCase().contains(textEditingValue.text.toLowerCase()))
                                .toList();
                      },
                      onSelected: (String selection) => _updateRelation('noun', selection),
                      fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
                        return TextField(
                          controller: textEditingController,
                          focusNode: focusNode,
                          decoration: _inputDecoration('Select Noun', 'noun'),
                          onChanged: (value) => _updateRelation('noun', value),
                        );
                      },
                    ),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton.icon(
                  icon: Icon(isCustomNoun ? Icons.list : Icons.edit),
                  label: Text(isCustomNoun ? 'Use predefined nouns' : 'Add custom noun'),
                  onPressed: toggleCustomNounMode,
                ),
              ),
            ],
          ),
        ),
      );
    },
  );
}

// State variables to track checkbox selections
bool _showModifier = false;
bool _showMeasurement = false;

Widget _buildModifierAndMeasurementSection() {
  return Card(
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Select Options',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              // Checkbox for Modifier
              Checkbox(
                value: _showModifier,
                onChanged: (value) {
                  setState(() {
                    _showModifier = value ?? false;
                  });
                },
              ),
              const Text('Modifier'),
              const SizedBox(width: 16),
              
              // Checkbox for Measurement
              Checkbox(
                value: _showMeasurement,
                onChanged: (value) {
                  setState(() {
                    _showMeasurement = value ?? false;
                  });
                },
              ),
              const Text('Measurement'),
            ],
          ),
          const SizedBox(height: 16),

          // Conditionally show modifier widget
          if (_showModifier) _buildModifierSection(),
          const SizedBox(height: 16),

          // Conditionally show measurement widget
          if (_showMeasurement) _buildMeasureTypeSection(),
        ],
      ),
    ),
  );
}
  Widget _buildModifierSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Select Modifier Type',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                _buildRadioOption('simple', 'Simple'),
                _buildRadioOption('complex', 'Complex'),
              ],
            ),
            const SizedBox(height: 16),
            if (_localNounRelation['modifierType'] == 'simple')
              ModifierSelector(
                predefinedModifiers: widget.modifiers,
                predefinedIntensifiers: widget.intensifiers,
                currentModifier: _localNounRelation['modifier'],
                onModifierChanged: (value) => _updateRelation('modifier', value),
                onIntensifierChanged: (_) {}, // Not used in simple mode
                isComplex: false,
              ),
            if (_localNounRelation['modifierType'] == 'complex')
              ModifierSelector(
                predefinedModifiers: widget.modifiers,
                predefinedIntensifiers: widget.intensifiers,
                currentModifier: _localNounRelation['modifier'],
                currentIntensifier: _localNounRelation['intensifier'],
                onModifierChanged: (value) => _updateRelation('modifier', value),
                onIntensifierChanged: (value) => _updateRelation('intensifier', value),
                isComplex: true,
              ),
          ],
        ),
      ),
    );
  }


Widget _buildRadioOption(String value, String label) {
  return Row(
    children: [
      Radio<String>(
        value: value,
        groupValue: _localNounRelation['modifierType'],
        onChanged: (v) => _updateRelation('modifierType', v),
      ),
      Text(label),
      const SizedBox(width: 16),
    ],
  );
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
  Widget _buildMeasureTypeSection() {
  return Card(
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Select Measure Type',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              _buildMeasureRadioOption('simple', 'Simple'),
              _buildMeasureRadioOption('complex', 'Complex'),
            ],
          ),
        ],
      ),
    ),
  );
}

Widget _buildMeasureRadioOption(String value, String label) {
  return Row(
    children: [
      Radio<String>(
        value: value,
        groupValue: _localNounRelation['measureType'],
        onChanged: (v) => _updateRelation('measureType', v),
      ),
      Text(label),
      const SizedBox(width: 16),
    ],
  );
}



 Widget _buildTypeSpecificFields() {
    if (_localNounRelation['measureType'] == 'simple') {
      return _buildSimpleFields();
    } else if (_localNounRelation['measureType'] == 'complex') {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Complex Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: _localNounRelation['complexType'] ?? 'span',
                decoration: _inputDecoration('Select Complex Type', 'complexType'),
                items: const [
                  DropdownMenuItem(value: 'span', child: Text('Span')),
                  DropdownMenuItem(value: 'rate', child: Text('Rate')),
                ],
                onChanged: (value) {
                  _updateRelation('complexType', value);
                },
              ),
              const SizedBox(height: 16),
              if (_localNounRelation['complexType'] == 'span') _buildSpanFields(),
              if (_localNounRelation['complexType'] == 'rate') _buildRateFields(),
            ],
          ),
        ),
      );
    }
    return Container();
  }

Widget _buildSimpleFields() {
  return Card(
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Simple Type Fields',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),

          // Dropdown to select field type
          DropdownButtonFormField<String>(
            value: _localNounRelation['fieldType'] ?? 'number',
            decoration: _inputDecoration('Select Field Type', 'fieldType'),
            items: const [
              DropdownMenuItem(value: 'number', child: Text('Number')),
              DropdownMenuItem(value: 'quantity', child: Text('Quantity')),
              DropdownMenuItem(value: 'measure', child: Text('Measure')),
            ],
            onChanged: (value) {
              setState(() => _updateRelation('fieldType', value));
            },
          ),
          const SizedBox(height: 16),

          // Number input field
          if (_localNounRelation['fieldType'] == 'number')
            TextField(
              controller: _numberController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Enter Number',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.confirmation_number),
              ),
              onChanged: (v) => _updateRelation('number', int.tryParse(v)),
            ),

          // Quantity selection
          if (_localNounRelation['fieldType'] == 'quantity') _buildQuantityField(),

          // Measure selection
          if (_localNounRelation['fieldType'] == 'measure') _buildMeasureField(),
        ],
      ),
    ),
  );
}
Widget _buildQuantityField() {
  return QuantitySelector(
    localNounRelation: _localNounRelation,
    dquantities: widget.dquantities,
    updateRelation: (_, value) {
      _updateRelation('dquantity', value);
    },
    addCustomOptionToDB: addCustomOptionToDB,
  );
}




Widget _buildMeasureField() {
  return MeasurementInputField(
    nounRelation: _localNounRelation,
    predefinedMeasurements: widget.measurements,
    onMeasurementChanged: (value) {
      // Update your _localNounRelation or call setState as needed.
      _updateRelation('measurement', value);
    },
    onQuantityChanged: (value) {
      // Update the quantity as a double.
      _updateRelation('quantity', value);
    },
  );
}



  /// Builds the rate fields using the custom measurement helper.
Widget _buildRateFields() {
  return Card(
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Unit Every field with count
          _buildCustomMeasurementField(
            measurementKey: 'unit_every',
            customFlagKey: 'isCustomUnitEvery',
            fieldLabel: 'Unit Every',
            selectLabel: 'Select Unit Every',
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _everyCountController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Count',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.numbers),
            ),
            onChanged: (v) => _updateRelation('every_count', double.tryParse(v)),
          ),
          const SizedBox(height: 20),
          // Unit Value field with count
          _buildCustomMeasurementField(
            measurementKey: 'unit_value',
            customFlagKey: 'isCustomUnitValue',
            fieldLabel: 'Unit Value',
            selectLabel: 'Select Unit Value',
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _valueCountController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Count',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.numbers),
            ),
            onChanged: (v) => _updateRelation('value_count', double.tryParse(v)),
          ),
        ],
      ),
    ),
  );
}
 /// Helper widget to build a custom measurement field.
/// [measurementKey] – key in _localNounRelation for the measurement value.
/// [customFlagKey] – key in _localNounRelation for the custom mode flag.
/// [fieldLabel] – label for the input field.
/// [selectLabel] – placeholder for the autocomplete field.
Widget _buildCustomMeasurementField({
  required String measurementKey,
  required String customFlagKey,
  required String fieldLabel,
  required String selectLabel,
}) {
  // Initialize flag if not already set.
  if (_localNounRelation[customFlagKey] == null) {
    _localNounRelation[customFlagKey] =
        _localNounRelation[measurementKey] != null &&
        !widget.measurements.contains(_localNounRelation[measurementKey]);
  }
  return StatefulBuilder(
    builder: (context, setState) {
      bool isCustom = _localNounRelation[customFlagKey] ?? false;
      TextEditingController controller = TextEditingController(
        text: isCustom ? _localNounRelation[measurementKey] : '',
      );
      FocusNode focusNode = FocusNode();

      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          isCustom
              ? Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: controller,
                        focusNode: focusNode,
                        decoration: _inputDecoration('Enter Custom $fieldLabel', measurementKey),
                        onChanged: (value) => _updateRelation(measurementKey, value),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.save),
                      tooltip: 'Save custom $fieldLabel',
                      onPressed: () {
                        final customValue = controller.text.trim();
                        if (customValue.isNotEmpty) {
                          addCustomOptionToDB('measurements', option: customValue)
                              .then((_) {
                            _updateRelation(measurementKey, customValue);
                          });
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Please enter a custom $fieldLabel first.')),
                          );
                        }
                      },
                    ),
                  ],
                )
              : Autocomplete<String>(
                  initialValue: TextEditingValue(
                    text: _localNounRelation[measurementKey] ?? '',
                  ),
                  optionsBuilder: (textEditingValue) {
                    if (textEditingValue.text.isEmpty) {
                      return widget.measurements;
                    }
                    return widget.measurements.where((m) =>
                        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                  },
                  onSelected: (selection) => _updateRelation(measurementKey, selection),
                  fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
                    return TextField(
                      controller: textEditingController,
                      focusNode: focusNode,
                      decoration: _inputDecoration(selectLabel, measurementKey),
                      onChanged: (value) => _updateRelation(measurementKey, value),
                    );
                  },
                ),
          Align(
            alignment: Alignment.centerRight,
            child: TextButton.icon(
              icon: Icon(isCustom ? Icons.list : Icons.edit),
              label: Text(isCustom ? 'Use predefined' : 'Add custom'),
              onPressed: () {
                setState(() {
                  _localNounRelation[customFlagKey] = !isCustom;
                  if (_localNounRelation[customFlagKey]) {
                    controller.text = _localNounRelation[measurementKey] ?? '';
                    Future.delayed(Duration.zero, () => focusNode.requestFocus());
                  } else if (_localNounRelation[measurementKey] != null &&
                      !widget.measurements.contains(_localNounRelation[measurementKey]) &&
                      widget.measurements.isNotEmpty) {
                    _updateRelation(measurementKey, widget.measurements.first);
                  }
                });
              },
            ),
          ),
        ],
      );
    },
  );
}

Widget _buildSpanFields() {
  return buildSpanFields(
    localNounRelation: _localNounRelation,
    predefinedMeasurements: widget.measurements,
    startQuantityController: _startQuantityController,
    endQuantityController: _endQuantityController,
    updateRelation: _updateRelation,
    addCustomOptionToDB: addCustomOptionToDB,
  );
}
  InputDecoration _inputDecoration(String label, String field) {
    return InputDecoration(
      labelText: label,
      border: const OutlineInputBorder(),
      suffixIcon: _localNounRelation[field] != null
          ? IconButton(
              icon: const Icon(Icons.clear),
              onPressed: () {
                widget.onClearField(_localNounRelation, field);
                setState(() {
                  _localNounRelation[field] = null;
                });
              },
            )
          : null,
    );
  }
}





class NounFilterChipList extends StatelessWidget {
  final List<String> nouns;
  final String searchQuery;
  final List<String> selectedNouns;
  final Function(String, bool) onSelectionChanged;
  final Function(String) onEditPressed;

  const NounFilterChipList({
    Key? key,
    required this.nouns,
    required this.searchQuery,
    required this.selectedNouns,
    required this.onSelectionChanged,
    required this.onEditPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Filter existing nouns based on the search query.
    final filteredNouns = nouns
        .where((noun) => noun.toLowerCase().contains(searchQuery.toLowerCase()))
        .toList();

    // Determine if the search query (custom value) should be added as a chip.
    final bool showAddChip = searchQuery.isNotEmpty &&
        !nouns.any((noun) => noun.toLowerCase() == searchQuery.toLowerCase());

    // Build a list of chip items.
    final List<_ChipItem> chipItems = [];
    if (showAddChip) {
      chipItems.add(_ChipItem(value: searchQuery, isCustom: true));
    }
    chipItems.addAll(filteredNouns.map((noun) => _ChipItem(value: noun, isCustom: false)));

    return SizedBox(
      height: 50,
      child: Scrollbar(
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemCount: chipItems.length,
          itemBuilder: (context, index) {
            final chipItem = chipItems[index];
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4.0),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  FilterChip(
                    label: Text(chipItem.isCustom
                        ? "Add '${chipItem.value}'"
                        : chipItem.value),
                    selected: selectedNouns.contains(chipItem.value),
                    onSelected: (selected) {
                      // Pass the chip's value (custom or from the list) to your callback.
                      onSelectionChanged(chipItem.value, selected);
                    },
                  ),
                  // Show the edit icon for any chip that is selected, regardless of its origin.
                  if (selectedNouns.contains(chipItem.value))
                    IconButton(
                      icon: const Icon(Icons.edit, size: 20),
                      color: Colors.blue,
                      onPressed: () => onEditPressed(chipItem.value),
                    ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}

// A helper class to distinguish between custom (entered) values and list items.
class _ChipItem {
  final String value;
  final bool isCustom;

  _ChipItem({required this.value, required this.isCustom});
}



class RelationDropdown extends StatelessWidget {
  final List<String> relations;
  final String? selectedRelation;
  final ValueChanged<String?> onChanged;
  final VoidCallback onClear;

  const RelationDropdown({
    Key? key,
    required this.relations,
    required this.selectedRelation,
    required this.onChanged,
    required this.onClear,
  }) : super(key: key);

  @override
 Widget build(BuildContext context) {
  return Autocomplete<String>(
    // Set the initial value from selectedRelation or an empty string.
    initialValue: TextEditingValue(text: selectedRelation ?? ''),
    optionsBuilder: (TextEditingValue textEditingValue) {
      // When the field is empty, show all relations.
      if (textEditingValue.text.isEmpty) {
        return relations;
      }
      // Filter the list based on the user's input (case insensitive).
      return relations.where((relation) =>
          relation.toLowerCase().contains(textEditingValue.text.toLowerCase()));
    },
    onSelected: (String selection) {
      // Call the onChanged callback when a relation is selected.
      onChanged(selection);
    },
    fieldViewBuilder: (BuildContext context,
        TextEditingController textEditingController,
        FocusNode focusNode,
        VoidCallback onFieldSubmitted) {
      return TextField(
        controller: textEditingController,
        focusNode: focusNode,
        decoration: InputDecoration(
          labelText: 'Select Relation',
          border: const OutlineInputBorder(),
          // Show a clear icon if a relation is selected.
          suffixIcon: textEditingController.text.isNotEmpty
              ? IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () {
                    textEditingController.clear();
                    onClear(); // Clear the selected relation
                  },
                )
              : null,
        ),
        onChanged: (String value) {
          // Update the selected relation as the user types.
          onChanged(value);
        },
        onSubmitted: (String value) {
          // Ensure the last entered value is saved.
          onChanged(value);
        },
      );
    },
  );
}
}