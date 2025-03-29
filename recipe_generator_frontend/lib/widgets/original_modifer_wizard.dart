// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
// import 'dart:convert';



// class AdvancedModifierWizard extends StatefulWidget {
//   final String noun;
//   final Map<String, dynamic> nounRelation;
//   final List<String> modifiers;
//   final List<String> intensifiers;
//   final String relationType;
//   final List<String> measurements;
//   final List<String> dquantities;
//   final Function(Map<String, dynamic>) onUpdate;

//   const AdvancedModifierWizard({
//     Key? key,
//     required this.noun,
//     required this.nounRelation,
//     required this.modifiers,
//     required this.intensifiers,
//     required this.relationType,
//     required this.measurements,
//     required this.dquantities,
//     required this.onUpdate,
//   }) : super(key: key);

//   @override
//   _AdvancedModifierWizardState createState() => _AdvancedModifierWizardState();
// }

// class _AdvancedModifierWizardState extends State<AdvancedModifierWizard> {
//   int _currentStep = 0;
//   late List<String> _selectedModifiers;
//   late List<String> _selectedIntensifiers;
//   String? _selectedmeasureType;
//   String? _selectedMeasurement;
//   String? _selectedNumber;
//   String? _selectedQuantity;
//   String _count = '';
//   String? _startMeasurement;
//   String _startcount = '';
//   String? _endMeasurement;
//   String _endcount = '';
//   String? _modifierType;

//   // Map to store intensifiers and their corresponding modifiers
//   Map<String, List<String>> intensifierModifiers = {};

//  @override
// void initState() {
//   super.initState();
//   final modifiers = (widget.nounRelation['nounModifiers'] as Map<String, List<String>>?) ?? {};
//   final intensifiers = (widget.nounRelation['nounIntensifiers'] as Map<String, List<String>>?) ?? {};
//   _selectedModifiers = List<String>.from(modifiers[widget.noun] ?? []);
//   _selectedIntensifiers = List<String>.from(intensifiers[widget.noun] ?? []);

//    final Quantities = (widget.nounRelation['quantity'] as Map<String, String>?) ?? {};
//   _selectedQuantity = Quantities[widget.noun];

//    final Number = (widget.nounRelation['number'] as Map<String, String>?) ?? {};
//   _selectedNumber = Number[widget.noun];
  
//   // Initialize rate measurements if they exist
//   final unitEveryMeasurements = (widget.nounRelation['unitEveryMeasurements'] as Map<String, String>?) ?? {};
//   final unitEveryQuantities = (widget.nounRelation['unitEveryQuantities'] as Map<String, double>?) ?? {};
//   final unitValueMeasurements = (widget.nounRelation['unitValueMeasurements'] as Map<String, String>?) ?? {};
//   final unitValueQuantities = (widget.nounRelation['unitValueQuantities'] as Map<String, double>?) ?? {};
  
//   _startMeasurement = unitEveryMeasurements[widget.noun];
//   _startcount = unitEveryQuantities[widget.noun]?.toString() ?? '';
//   _endMeasurement = unitValueMeasurements[widget.noun];
//   _endcount = unitValueQuantities[widget.noun]?.toString() ?? '';
// }

//   int get _totalSteps => widget.relationType == 'Span' ? 2 : 3;

//   @override
//   Widget build(BuildContext context) {
//     return Padding(
//       padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
//       child: Column(
//         mainAxisSize: MainAxisSize.min,
//         children: [
//           LinearProgressIndicator(
//             value: (_currentStep + 1) / _totalSteps,
//             backgroundColor: Colors.grey[300],
//             valueColor: AlwaysStoppedAnimation(Theme.of(context).primaryColor),
//           ),
//           const SizedBox(height: 16),
//           _buildStepContent(),
//           const SizedBox(height: 16),
//           _buildNavigationButtons(),
//         ],
//       ),
//     );
//   }
//   Future<void> addCustomOptionToDB(String category,
//     {String? subcategory, required String option}) async {
//   const String url = 'http://127.0.0.1:2000/add-option';
//   final payload = {
//     "category": category,
//     "option": option,
//     if (subcategory != null) "subcategory": subcategory,
//   };
//   try {
//     final response = await http.post(Uri.parse(url),
//         headers: {'Content-Type': 'application/json'},
//         body: json.encode(payload));
//     final message = response.statusCode == 200
//         ? '$option added successfully!'
//         : 'Failed to add custom option.';
//     ScaffoldMessenger.of(context)
//         .showSnackBar(SnackBar(content: Text(message)));
//   } catch (e) {
//     ScaffoldMessenger.of(context).showSnackBar(
//       const SnackBar(content: Text('Error adding custom option.')),
//     );
//   }
// }



//   Widget _buildStepContent() {
//     if (widget.relationType == 'Span') {
//       switch (_currentStep) {
//         case 0:
//           return _buildModifierTypeSelection();
//         case 1:
//           return _buildMeasurementInput();
//         default:
//           return const SizedBox();
//       }
//     } else {
//       switch (_currentStep) {
//         case 0:
//           return _buildModifierTypeSelection();
//         case 1:
//           return _buildmeasureTypeSelection();
//         case 2:
//           return _selectedmeasureType == 'span' ? _buildSpanMeasurementInput() : _buildMeasurementInput();
//         default:
//           return const SizedBox();
//       }
//     }
//   }

//     Widget _buildModifierTypeSelection() {
//     return Column(
//       crossAxisAlignment: CrossAxisAlignment.start,
//       children: [
//         const Text('Select Modifier Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//         const SizedBox(height: 10),
//         DropdownButtonFormField<String>(
//           value: _modifierType,
//           items: ['simple', 'complex']
//               .map((type) => DropdownMenuItem(value: type, child: Text(type)))
//               .toList(),
//           onChanged: (value) => setState(() {
//             _modifierType = value;
//             _selectedModifiers.clear();
//             _selectedIntensifiers.clear();
//           }),
//           decoration: const InputDecoration(
//             labelText: 'Modifier Type',
//             border: OutlineInputBorder(),
//           ),
//         ),
//         const SizedBox(height: 10),
//         if (_modifierType == 'simple') ...[
//           _buildModifierSelection(),
//           const SizedBox(height: 16),
//           // _buildIntensifierSelection(),
//         ],
//         if (_modifierType == 'complex') _buildComplexModifierSelection(),
//       ],
//     );
//   }
//   Widget _buildIntensifierSelection() {
//   // Merge predefined intensifiers with any custom ones already selected.
//   final List<String> allIntensifiers = [
//     ...widget.intensifiers,
//     ..._selectedIntensifiers.where((i) => !widget.intensifiers.contains(i))
//   ];
//   // Remove duplicates.
//   final uniqueIntensifiers = allIntensifiers.toSet().toList();

//   return Padding(
//     padding: const EdgeInsets.only(left: 16.0), // Adjust left padding as needed
//     child: Column(
//       crossAxisAlignment: CrossAxisAlignment.start,
//       children: [
//         const Text(
//           'Select Intensifiers',
//           style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
//         ),
//         const SizedBox(height: 10),
//         Wrap(
//           spacing: 8,
//           runSpacing: 4,
//           children: [
//             ...uniqueIntensifiers.map((intensifier) {
//               return Padding(
//                 padding: const EdgeInsets.symmetric(horizontal: 4.0),
//                 child: Row(
//                   mainAxisSize: MainAxisSize.min,
//                   children: [
//                     FilterChip(
//                       label: Text(intensifier),
//                       selected: _selectedIntensifiers.contains(intensifier),
//                       onSelected: (selected) => setState(() {
//                         if (selected) {
//                           _selectedIntensifiers.add(intensifier);
//                           addCustomOptionToDB('modifiers', option: intensifier);

//                         } else {
//                           _selectedIntensifiers.remove(intensifier);
//                         }
//                       }),
//                     ),
//                     if (_selectedIntensifiers.contains(intensifier))
//                       IconButton(
//                         icon: const Icon(Icons.edit, size: 20),
//                         color: Colors.blue,
//                         onPressed: () {
//                           // Add your edit functionality here (e.g., open an edit dialog).
//                         },
//                       ),
//                   ],
//                 ),
//               );
//             }).toList(),
//             // Custom chip for adding a new intensifier.
//             ActionChip(
//               label: const Text('Add Custom Intensifier'),
//               avatar: const Icon(Icons.add),
//               onPressed: () async {
//                 final customIntensifier = await _showCustommIntensifierDialog(context);
//                 if (customIntensifier != null && customIntensifier.trim().isNotEmpty) {
//                   setState(() {
//                     _selectedIntensifiers.add(customIntensifier.trim());
//                   });
//                 }
//               },
//             ),
//           ],
//         ),
//       ],
//     ),
//   );
// }

// /// Shows a dialog to allow the user to input a custom intensifier.
// Future<String?> _showCustommIntensifierDialog(BuildContext context) async {
//   final TextEditingController controller = TextEditingController();
//   return showDialog<String>(
//     context: context,
//     builder: (context) {
//       return AlertDialog(
//         title: const Text('Add Custom Intensifier'),
//         content: TextField(
//           controller: controller,
//           decoration: const InputDecoration(
//             hintText: 'Enter custom intensifier',
//           ),
//         ),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.of(context).pop(),
//             child: const Text('Cancel'),
//           ),
//           TextButton(
//             onPressed: () {
//               Navigator.of(context).pop(controller.text);
//             },
//             child: const Text('Add'),
//           ),
//         ],
//       );
//     },
//   );
// }

// Widget _buildModifierSelection() {
//   // Combine predefined modifiers with any custom-selected modifiers not in widget.modifiers.
//   final List<String> allModifiers = [
//     ...widget.modifiers,
//     ..._selectedModifiers.where((modifier) => !widget.modifiers.contains(modifier))
//   ];
//   // Remove duplicates if any.
//   final uniqueModifiers = allModifiers.toSet().toList();

//   return Column(
//     crossAxisAlignment: CrossAxisAlignment.start,
//     children: [
//       const Text(
//         'Select Modifiers',
//         style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
//       ),
//       const SizedBox(height: 10),
//       Wrap(
//         spacing: 8,
//         runSpacing: 4,
//         children: [
//           ...uniqueModifiers.map((modifier) {
//             return Padding(
//               padding: const EdgeInsets.symmetric(horizontal: 4.0),
//               child: Row(
//                 mainAxisSize: MainAxisSize.min,
//                 children: [
//                   FilterChip(
//                     label: Text(modifier),
//                     selected: _selectedModifiers.contains(modifier),
//                     onSelected: (selected) => setState(() {
//                       selected
//                           ? _selectedModifiers.add(modifier)
//                           : _selectedModifiers.remove(modifier);
//                     }),
//                   ),
//                   // Display the edit icon for any selected modifier.
//                   if (_selectedModifiers.contains(modifier))
//                     IconButton(
//                       icon: const Icon(Icons.edit, size: 20),
//                       color: Colors.blue,
//                       onPressed: () {
//                         // Trigger an edit callback or handle editing here.
//                         // For example, you could open a dialog to edit the modifier.
//                       },
//                     ),
//                 ],
//               ),
//             );
//           }).toList(),
//           // Add a custom chip to allow adding a custom modifier.
//           ActionChip(
//             label: const Text('Add Custom Modifier'),
//             avatar: const Icon(Icons.add),
//             onPressed: () async {
//               final customModifier = await _showCustomModifierDialog(context);
//               if (customModifier != null && customModifier.trim().isNotEmpty) {
//                 setState(() {
//                   _selectedModifiers.add(customModifier.trim());
//                    addCustomOptionToDB('modifiers', option: customModifier);
//                 });
//               }
//             },
//           ),
//         ],
//       ),
//     ],
//   );
// }

// /// Displays a dialog to input a custom modifier.
// Future<String?> _showCustomModifierDialog(BuildContext context) async {
//   final TextEditingController controller = TextEditingController();
//   return showDialog<String>(
//     context: context,
//     builder: (context) {
//       return AlertDialog(
//         title: const Text('Add Custom Modifier'),
//         content: TextField(
//           controller: controller,
//           decoration: const InputDecoration(
//             hintText: 'Enter custom modifier',
//           ),
//         ),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.of(context).pop(),
//             child: const Text('Cancel'),
//           ),
//           TextButton(
//             onPressed: () {
//               Navigator.of(context).pop(controller.text);
//             },
//             child: const Text('Add'),
//           ),
//         ],
//       );
//     },
//   );
// }


//     Widget _buildComplexModifierSelection() {
//     return Column(
//       crossAxisAlignment: CrossAxisAlignment.start,
//       children: [
//       //   const Text('Select Intensifiers and Modifiers',
//       //       style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//         const SizedBox(height: 10),
//         _buildModifierOptionsForIntensifiers(),
//         const SizedBox(height: 16),
//         _buildIntensifierSelection(),
        
//       ],
//     );
//   }
// Widget _buildModifierOptionsForIntensifiers() {
//   // Merge predefined modifiers with any custom-selected ones not in the list.
//   final List<String> allModifiers = [
//     ...widget.modifiers,
//     ..._selectedModifiers.where((modifier) => !widget.modifiers.contains(modifier))
//   ];
//   // Ensure uniqueness.
//   final uniqueModifiers = allModifiers.toSet().toList();

//   return Column(
//     crossAxisAlignment: CrossAxisAlignment.start,
//     children: [
//       const Text(
//         'Select Modifiers',
//         style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
//       ),
//       const SizedBox(height: 10),
//       Wrap(
//         spacing: 8,
//         runSpacing: 4,
//         children: [
//           ...uniqueModifiers.map((modifier) {
//             return Padding(
//               padding: const EdgeInsets.symmetric(horizontal: 4.0),
//               child: Row(
//                 mainAxisSize: MainAxisSize.min,
//                 children: [
//                   FilterChip(
//                     label: Text(modifier),
//                     selected: _selectedModifiers.contains(modifier),
//                     onSelected: (selected) => setState(() {
//                       if (selected) {
//                         _selectedModifiers.add(modifier);
//                         addCustomOptionToDB('modifiers', option: modifier);

//                       } else {
//                         _selectedModifiers.remove(modifier);
//                       }
//                     }),
//                   ),
//                   // Show edit icon for any chip that is selected.
//                   if (_selectedModifiers.contains(modifier))
//                     IconButton(
//                       icon: const Icon(Icons.edit, size: 20),
//                       color: Colors.blue,
//                       onPressed: () {
//                         // Add your edit functionality here.
//                         // For example, open a dialog to edit the modifier.
//                       },
//                     ),
//                 ],
//               ),
//             );
//           }).toList(),
//           // Custom chip for adding a new intensifier.
//           ActionChip(
//             label: const Text('Add Custom Modifier'),
//             avatar: const Icon(Icons.add),
//             onPressed: () async {
//               final customModifier = await _showCustomModifierDialog(context);
//               if (customModifier != null && customModifier.trim().isNotEmpty) {
//                 setState(() {
//                   _selectedModifiers.add(customModifier.trim());
//                 });
//               }
//             },
//           ),
//         ],
//       ),
//     ],
//   );
// }




// String? _selectedComplexType;
// String? _selectedSimpleType;

// Widget _buildmeasureTypeSelection() {
//   return Column(
//     crossAxisAlignment: CrossAxisAlignment.start,
//     children: [
//       const Text('Select Measure Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//       const SizedBox(height: 10),
//       DropdownButtonFormField<String>(
//         value: _selectedmeasureType,
//         items: ['simple', 'complex']
//             .map((type) => DropdownMenuItem(value: type, child: Text(type)))
//             .toList(),
//         onChanged: (value) {
//           setState(() {
//             _selectedmeasureType = value;
//             _selectedComplexType = null; // Reset complex selection
//             _selectedSimpleType = null; // Reset simple selection
//           });
//         },
//         decoration: const InputDecoration(
//           labelText: 'Measure Type',
//           border: OutlineInputBorder(),
//         ),
//       ),
//       if (_selectedmeasureType == 'simple') ...[
//         const SizedBox(height: 10),
//         const Text('Select Simple Type', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
//         DropdownButtonFormField<String>(
//           value: _selectedSimpleType,
//           items: ['number', 'quantity', 'measure']
//               .map((type) => DropdownMenuItem(value: type, child: Text(type)))
//               .toList(),
//           onChanged: (value) => setState(() => _selectedSimpleType = value),
//           decoration: const InputDecoration(
//             labelText: 'Simple Type',
//             border: OutlineInputBorder(),
//           ),
//         ),
//       ],
//       if (_selectedmeasureType == 'complex') ...[
//         const SizedBox(height: 10),
//         const Text('Select Complex Type', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
//         DropdownButtonFormField<String>(
//           value: _selectedComplexType,
//           items: ['span', 'rate']
//               .map((type) => DropdownMenuItem(value: type, child: Text(type)))
//               .toList(),
//           onChanged: (value) => setState(() => _selectedComplexType = value),
//           decoration: const InputDecoration(
//             labelText: 'Complex Type',
//             border: OutlineInputBorder(),
//           ),
//         ),
//       ],
//     ],
//   );
// }
// Widget _buildMeasurementInput() {
//   if (_selectedmeasureType == 'complex') {
//     if (_selectedComplexType == 'span') {
//       return _buildSpanMeasurementInput();
//     } else if (_selectedComplexType == 'rate') {
//       return _buildRateMeasurementInput();
//     }
//   } else if (_selectedmeasureType == 'simple') {
//     switch (_selectedSimpleType) {
//       case 'number':
//         return _buildNumberInput();
//       case 'quantity':
//         return _buildQuantityInput();
//       case 'measure':
//         return _buildMeasureInput();
//       default:
//         return const SizedBox(); // Empty widget if no type selected
//     }
//   }

//   return MeasurementInputSection(
//     noun: widget.noun,
//     nounRelation: widget.nounRelation,
//     measurements: widget.measurements,
//   );
// }

// Widget _buildNumberInput() {
//   return Column(
//     crossAxisAlignment: CrossAxisAlignment.start,
//     children: [
//       const Text('Enter Number', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//       const SizedBox(height: 10),
//       TextField(
//         keyboardType: TextInputType.number,
//         decoration: const InputDecoration(
//           labelText: 'Number Value',
//           border: OutlineInputBorder(),
//         ),
//         onChanged: (v) => setState(() => _selectedNumber = v),
//       ),
//     ],
//   );
// }

// Widget _buildQuantityInput() {
//   return Column(
//     crossAxisAlignment: CrossAxisAlignment.start,
//     children: [
//       const Text(
//         'Select Quantity',
//         style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
//       ),
//       const SizedBox(height: 10),
//       Autocomplete<String>(
//         initialValue: TextEditingValue(text: _selectedQuantity ?? ''),
//         optionsBuilder: (TextEditingValue textEditingValue) {
//           if (textEditingValue.text.isEmpty) {
//             return widget.dquantities;
//           }
//           return widget.dquantities.where(
//               (m) => m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//         },
//         onSelected: (value) {
//           setState(() {
//             _selectedQuantity = value;
//             print(_selectedQuantity);
//           });
//         },
//         fieldViewBuilder:
//             (context, textEditingController, focusNode, onFieldSubmitted) {
//           return TextField(
//             controller: textEditingController,
//             focusNode: focusNode,
//             decoration: const InputDecoration(
//               labelText: 'Quantity',
//               border: OutlineInputBorder(),
//             ),
//             onChanged: (value) {
//               // Update _selectedQuantity immediately when typing
//               setState(() {
//                 _selectedQuantity = value;
//               });
//             },
//           );
//         },
//       ),
//     ],
//   );
// }


// Widget _buildMeasureInput() {
//   return Column(
//     crossAxisAlignment: CrossAxisAlignment.start,
//     children: [
//       const Text('Select Measurement', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//       const SizedBox(height: 10),
//       Autocomplete<String>(
//   initialValue: TextEditingValue(text:   _selectedMeasurement ?? ''),
//   optionsBuilder: (TextEditingValue textEditingValue) {
//     if (textEditingValue.text.isEmpty) {
//       return widget.measurements;
//     }
//     return widget.measurements.where(
//         (m) => m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//   },
//   onSelected: (String selection) {
//     setState(() {
//        _selectedMeasurement  = selection;
//     });
//   },
//   fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
//     return TextField(
//       controller: textEditingController,
//       focusNode: focusNode,
//       decoration: const InputDecoration(
//         labelText: 'Start Measurement',
//         border: OutlineInputBorder(),
//       ),
//       onChanged: (value) {
//         // Update _selectedStartMeasurement immediately as the user types
//         setState(() {
//             _selectedMeasurement = value;
//         });
//       },
//     );
//   },
// ),

//       const SizedBox(height: 10),
//       TextField(
//         keyboardType: TextInputType.number,
//         decoration: const InputDecoration(
//           labelText: 'Value',
//           border: OutlineInputBorder(),
//         ),
//         onChanged: (v) => setState(() => _count = v),
//       ),
//     ],
//   );
// }




//   Widget _buildSpanMeasurementInput() {
//     return Column(
//       crossAxisAlignment: CrossAxisAlignment.start,
//       children: [
//         const Text('Set Start Measurement & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//     Autocomplete<String>(
//   initialValue: TextEditingValue(
//     text: _startMeasurement ?? '',
//   ),
//   optionsBuilder: (TextEditingValue textEditingValue) {
//     if (textEditingValue.text.isEmpty) {
//       return widget.measurements;
//     }
//     return widget.measurements.where((m) =>
//         m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//   },
//   onSelected: (String selection) {
//     setState(() {
//       _startMeasurement = selection;
//     });
//   },
//   fieldViewBuilder: (BuildContext context,
//       TextEditingController textEditingController,
//       FocusNode focusNode,
//       VoidCallback onFieldSubmitted) {
//     return TextField(
//       controller: textEditingController,
//       focusNode: focusNode,
//       decoration: const InputDecoration(
//         labelText: 'Start Measurement',
//         border: OutlineInputBorder(),
//       ),
//       onChanged: (value) {
//         // Update the value as the user types
//         setState(() {
//           _startMeasurement = value;
//         });
//       },
//     );
//   },
// ),

//         const SizedBox(height: 10),
//         TextField(
//           keyboardType: TextInputType.number,
//           decoration: const InputDecoration(labelText: 'Start count', border: OutlineInputBorder()),
//           onChanged: (v) => setState(() => _startcount = v),
//         ),
//         const SizedBox(height: 20),
//         const Text('Set End Measurement & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//      Autocomplete<String>(
//   initialValue: TextEditingValue(
//     text: _endMeasurement ?? '',
//   ),
//   optionsBuilder: (TextEditingValue textEditingValue) {
//     if (textEditingValue.text.isEmpty) {
//       return widget.measurements;
//     }
//     return widget.measurements.where((m) =>
//         m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//   },
//   onSelected: (String selection) {
//     setState(() {
//       _endMeasurement = selection;
//     });
//   },
//   fieldViewBuilder: (BuildContext context,
//       TextEditingController textEditingController,
//       FocusNode focusNode,
//       VoidCallback onFieldSubmitted) {
//     return TextField(
//       controller: textEditingController,
//       focusNode: focusNode,
//       decoration: const InputDecoration(
//         labelText: 'End Measurement',
//         border: OutlineInputBorder(),
//       ),
//       onChanged: (value) {
//         // Update immediately when user types
//         setState(() {
//           _endMeasurement = value;
//         });
//       },
//     );
//   },
// ),

//         const SizedBox(height: 10),
//         TextField(
//           keyboardType: TextInputType.number,
//           decoration: const InputDecoration(labelText: 'End count', border: OutlineInputBorder()),
//           onChanged: (v) => setState(() => _endcount = v),
//         ),
//       ],
//     );
//   }
  
//    Widget _buildRateMeasurementInput() {
//     return Column(
//       crossAxisAlignment: CrossAxisAlignment.start,
//       children: [
//         const Text('Set unit_every & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//      Autocomplete<String>(
//   initialValue: TextEditingValue(
//     text: _startMeasurement ?? '',
//   ),
//   optionsBuilder: (TextEditingValue textEditingValue) {
//     if (textEditingValue.text.isEmpty) {
//       return widget.measurements;
//     }
//     return widget.measurements.where((m) =>
//         m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//   },
//   onSelected: (String selection) {
//     setState(() {
//       _startMeasurement = selection;
//     });
//   },
//   fieldViewBuilder: (BuildContext context,
//       TextEditingController textEditingController,
//       FocusNode focusNode,
//       VoidCallback onFieldSubmitted) {
//     return TextField(
//       controller: textEditingController,
//       focusNode: focusNode,
//       decoration: const InputDecoration(
//         labelText: 'unit_every',
//         border: OutlineInputBorder(),
//       ),
//       onChanged: (value) {
//         // Save value immediately as user types
//         setState(() {
//           _startMeasurement = value;
//         });
//       },
//     );
//   },
// ),

//         const SizedBox(height: 10),
//         TextField(
//           keyboardType: TextInputType.number,
//           decoration: const InputDecoration(labelText: 'count', border: OutlineInputBorder()),
//           onChanged: (v) => setState(() => _startcount = v),
//         ),
//         const SizedBox(height: 20),
//         const Text('Set unit_value & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
//       Autocomplete<String>(
//   initialValue: TextEditingValue(
//     text: _endMeasurement ?? '',
//   ),
//   optionsBuilder: (TextEditingValue textEditingValue) {
//     if (textEditingValue.text.isEmpty) {
//       return widget.measurements;
//     }
//     return widget.measurements.where((m) =>
//         m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//   },
//   onSelected: (String selection) {
//     setState(() {
//       _endMeasurement = selection;
//     });
//   },
//   fieldViewBuilder: (BuildContext context,
//       TextEditingController textEditingController,
//       FocusNode focusNode,
//       VoidCallback onFieldSubmitted) {
//     return TextField(
//       controller: textEditingController,
//       focusNode: focusNode,
//       decoration: const InputDecoration(
//         labelText: 'unit_value',
//         border: OutlineInputBorder(),
//       ),
//       onChanged: (value) {
//         // Save value immediately as the user types
//         setState(() {
//           _endMeasurement = value;
//         });
//       },
//     );
//   },
// ),

//         const SizedBox(height: 10),
//         TextField(
//           keyboardType: TextInputType.number,
//           decoration: const InputDecoration(labelText: 'count', border: OutlineInputBorder()),
//           onChanged: (v) => setState(() => _endcount = v),
//         ),
//       ],
//     );
//   }

//   Widget _buildNavigationButtons() {
//     return Row(
//       mainAxisAlignment: MainAxisAlignment.spaceBetween,
//       children: [
//         if (_currentStep > 0)
//           TextButton(onPressed: () => setState(() => _currentStep--), child: const Text('Back')),
//         TextButton(
//           onPressed: () {
//             if (_currentStep < _totalSteps - 1) {
//               setState(() => _currentStep++);
//             } else {
//               _saveAndClose();
//             }
//           },
//           child: Text(_currentStep < _totalSteps - 1 ? 'Next' : 'Save'),
//         ),
//       ],
//     );
//   }
 
//    void _saveAndClose() {
//   // Save modifiers
//   widget.nounRelation['nounModifiers'] ??= <String, List<String>>{};
//   widget.nounRelation['nounModifiers'][widget.noun] = _selectedModifiers;

//   // Save intensifiers
//   widget.nounRelation['nounIntensifiers'] ??= <String, List<String>>{};
//   widget.nounRelation['nounIntensifiers'][widget.noun] = _selectedIntensifiers;

//   if (widget.relationType != 'Span') {
//     widget.nounRelation['measureTypes'] ??= <String, String>{};
//     widget.nounRelation['measureTypes'][widget.noun] = _selectedmeasureType ?? 'simple';
//   }

//   // Handle measurements based on type
//   if (_selectedmeasureType == 'complex') {
//     if (_selectedComplexType == 'rate') {
//       _saveRateMeasurements();
//     } else if (_selectedComplexType == 'span') {
//       _saveSpanMeasurements();
//     }
//   } else {
//     _saveSimpleMeasurements();
//   }

//   widget.onUpdate(widget.nounRelation);
//   Navigator.pop(context);
// }


   
//   void _saveSpanMeasurements() {
//     widget.nounRelation['startMeasurements'] ??= <String, String>{};
//     widget.nounRelation['startQuantities'] ??= <String, double>{};
//     widget.nounRelation['endMeasurements'] ??= <String, String>{};
//     widget.nounRelation['endQuantities'] ??= <String, double>{};

//     if (_startMeasurement != null && _startcount.isNotEmpty) {
//       widget.nounRelation['startMeasurements'][widget.noun] = _startMeasurement!;
//       widget.nounRelation['startQuantities'][widget.noun] = double.tryParse(_startcount) ?? 0.0;
//     }
//     if (_endMeasurement != null && _endcount.isNotEmpty) {
//       widget.nounRelation['endMeasurements'][widget.noun] = _endMeasurement!;
//       widget.nounRelation['endQuantities'][widget.noun] = double.tryParse(_endcount) ?? 0.0;
//     }
//   }
//   void _saveRateMeasurements() {
//   // Initialize rate-specific maps if they don't exist
//   widget.nounRelation['unitEveryMeasurements'] ??= <String, String>{};
//   widget.nounRelation['unitEveryQuantities'] ??= <String, double>{};
//   widget.nounRelation['unitValueMeasurements'] ??= <String, String>{};
//   widget.nounRelation['unitValueQuantities'] ??= <String, double>{};

//   // Save unit_every measurement and count
//   if (_startMeasurement != null && _startcount.isNotEmpty) {
//     widget.nounRelation['unitEveryMeasurements'][widget.noun] = _startMeasurement!;
//     widget.nounRelation['unitEveryQuantities'][widget.noun] = double.tryParse(_startcount) ?? 0.0;  // Fixed this line
//   }

//   // Save unit_value measurement and count
//   if (_endMeasurement != null && _endcount.isNotEmpty) {
//     widget.nounRelation['unitValueMeasurements'][widget.noun] = _endMeasurement!;
//     widget.nounRelation['unitValueQuantities'][widget.noun] = double.tryParse(_endcount) ?? 0.0;
//   }
  
//   // Save the measure type
//   widget.nounRelation['measureTypes'] ??= <String, String>{};
//   widget.nounRelation['measureTypes'][widget.noun] = 'rate';

//   // Print debug information
//   print('Saved unit_every: ${widget.nounRelation['unitEveryMeasurements'][widget.noun]} ${widget.nounRelation['unitEveryQuantities'][widget.noun]}');
//   print('Saved unit_value: ${widget.nounRelation['unitValueMeasurements'][widget.noun]} ${widget.nounRelation['unitValueQuantities'][widget.noun]}');
// }

//  void _saveSimpleMeasurements() {
//   widget.nounRelation['simpleValues'] ??= <String, dynamic>{};

//   switch (_selectedSimpleType) {
//     case 'number':
//        widget.nounRelation['number'] ??= <String, String>{};
      
//       if (_selectedNumber != null) {
//         // Store the selected quantity value
//         widget.nounRelation['number'][widget.noun] = _selectedNumber;
//         // Also store in simpleValues for compatibility
//         widget.nounRelation['simpleValues'][widget.noun] = _selectedNumber;
//       }
//       break;
//      case 'quantity':
//       // Initialize a separate map for discrete quantities
//       widget.nounRelation['quantity'] ??= <String, String>{};
      
//       if (_selectedQuantity != null) {
//         // Store the selected quantity value
//         widget.nounRelation['quantity'][widget.noun] = _selectedQuantity;
//         // Also store in simpleValues for compatibility
//         widget.nounRelation['simpleValues'][widget.noun] = _selectedQuantity;
//       }
//       break;
//     case 'measure':
//       widget.nounRelation['measurements'] ??= <String, String>{};
//       widget.nounRelation['quantities'] ??= <String, double>{};
//       if (_selectedMeasurement != null && _count.isNotEmpty) {
//         widget.nounRelation['measurements'][widget.noun] = _selectedMeasurement!;
//         widget.nounRelation['quantities'][widget.noun] =
//             double.tryParse(_count) ?? 0.0;
//       }
//       break;
//     default:
//       // Optionally handle unexpected types.
//       break;
//   }
  
//   // Print the updated nounRelation map for debugging purposes.
//   print(widget.nounRelation);
// }
// }
// class MeasurementInputSection extends StatelessWidget {
//   final String noun;
//   final Map<String, dynamic> nounRelation;
//   final List<String> measurements;

//   const MeasurementInputSection({
//     Key? key,
//     required this.noun,
//     required this.nounRelation,
//     required this.measurements,
//   }) : super(key: key);

//   @override
//   Widget build(BuildContext context) {
//     return Column(
//       children: [
//       Autocomplete<String>(
//   initialValue: TextEditingValue(
//     text: nounRelation['measurements']?[noun] ?? '',
//   ),
//   optionsBuilder: (TextEditingValue textEditingValue) {
//     if (textEditingValue.text.isEmpty) {
//       return measurements;
//     }
//     return measurements.where((m) =>
//         m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
//   },
//   onSelected: (String selection) {
//     nounRelation['measurements'][noun] = selection;
//   },
//   fieldViewBuilder: (BuildContext context,
//       TextEditingController textEditingController,
//       FocusNode focusNode,
//       VoidCallback onFieldSubmitted) {
//     return TextField(
//       controller: textEditingController,
//       focusNode: focusNode,
//       decoration: const InputDecoration(
//         labelText: 'Measurement',
//         border: OutlineInputBorder(),
//       ),
//       onChanged: (value) {
//         // Save value immediately as the user types
//         nounRelation['measurements'][noun] = value;
//       },
//     );
//   },
// ),

//         const SizedBox(height: 10),
//         TextField(
//           controller: TextEditingController(
//               text: nounRelation['quantities']?[noun]?.toString() ?? ''),
//           keyboardType: TextInputType.number,
//           decoration: const InputDecoration(
//             labelText: 'count',
//             border: OutlineInputBorder(),
//           ),
//           onChanged: (v) => nounRelation['quantities'][noun] = double.tryParse(v),
//         ),
//       ],
//     );
//   }
// }

// NEW CODE

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../common/modifier_selector.dart';


class AdvancedModifierWizard extends StatefulWidget {
  final String noun;
  final Map<String, dynamic> nounRelation;
  final List<String> modifiers;
  final List<String> intensifiers;
  final String relationType;
  final List<String> measurements;
  final List<String> dquantities;
  final Function(Map<String, dynamic>) onUpdate;

  const AdvancedModifierWizard({
    Key? key,
    required this.noun,
    required this.nounRelation,
    required this.modifiers,
    required this.intensifiers,
    required this.relationType,
    required this.measurements,
    required this.dquantities,
    required this.onUpdate,
  }) : super(key: key);

  @override
  _AdvancedModifierWizardState createState() => _AdvancedModifierWizardState();
}

class _AdvancedModifierWizardState extends State<AdvancedModifierWizard> {
  int _currentStep = 0;
  late List<String> _selectedModifiers;
  late List<String> _selectedIntensifiers;
  String? _selectedmeasureType;
  String? _selectedMeasurement;
  String? _selectedNumber;
  String? _selectedQuantity;
  String _count = '';
  String? _startMeasurement;
  String _startcount = '';
  String? _endMeasurement;
  String _endcount = '';
  String? _modifierType;
  String? _selectedModifier;
  String? _selectedIntensifier;

  // Map to store intensifiers and their corresponding modifiers
  Map<String, List<String>> intensifierModifiers = {};

 @override
void initState() {
  super.initState();
  final modifiers = (widget.nounRelation['nounModifiers'] as Map<String, List<String>>?) ?? {};
  final intensifiers = (widget.nounRelation['nounIntensifiers'] as Map<String, List<String>>?) ?? {};
  _selectedModifiers = List<String>.from(modifiers[widget.noun] ?? []);
  _selectedIntensifiers = List<String>.from(intensifiers[widget.noun] ?? []);

   final Quantities = (widget.nounRelation['quantity'] as Map<String, String>?) ?? {};
  _selectedQuantity = Quantities[widget.noun];

   final Number = (widget.nounRelation['number'] as Map<String, String>?) ?? {};
  _selectedNumber = Number[widget.noun];
  
  
  // Initialize rate measurements if they exist
  final unitEveryMeasurements = (widget.nounRelation['unitEveryMeasurements'] as Map<String, String>?) ?? {};
  final unitEveryQuantities = (widget.nounRelation['unitEveryQuantities'] as Map<String, double>?) ?? {};
  final unitValueMeasurements = (widget.nounRelation['unitValueMeasurements'] as Map<String, String>?) ?? {};
  final unitValueQuantities = (widget.nounRelation['unitValueQuantities'] as Map<String, double>?) ?? {};
  
  _startMeasurement = unitEveryMeasurements[widget.noun];
  _startcount = unitEveryQuantities[widget.noun]?.toString() ?? '';
  _endMeasurement = unitValueMeasurements[widget.noun];
  _endcount = unitValueQuantities[widget.noun]?.toString() ?? '';
}

  int get _totalSteps => widget.relationType == 'Span' ? 2 : 3;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          LinearProgressIndicator(
            value: (_currentStep + 1) / _totalSteps,
            backgroundColor: Colors.grey[300],
            valueColor: AlwaysStoppedAnimation(Theme.of(context).primaryColor),
          ),
          const SizedBox(height: 16),
          _buildStepContent(),
          const SizedBox(height: 16),
          _buildNavigationButtons(),
        ],
      ),
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



  Widget _buildStepContent() {
    if (widget.relationType == 'Span') {
      switch (_currentStep) {
        case 0:
          return _buildModifierTypeSelection();
        case 1:
          return _buildMeasurementInput();
        default:
          return const SizedBox();
      }
    } else {
      switch (_currentStep) {
        case 0:
          return _buildModifierTypeSelection();
        case 1:
          return _buildmeasureTypeSelection();
        case 2:
          return _selectedmeasureType == 'span' ? _buildSpanMeasurementInput() : _buildMeasurementInput();
        default:
          return const SizedBox();
      }
    }
  }

     Widget _buildModifierTypeSelection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Select Modifier Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 10),
        DropdownButtonFormField<String>(
          value: _modifierType,
          items: ['simple', 'complex']
              .map((type) => DropdownMenuItem(value: type, child: Text(type)))
              .toList(),
          onChanged: (value) => setState(() {
            _modifierType = value;
            _selectedModifier = null;
            _selectedIntensifier = null;
          }),
          decoration: const InputDecoration(
            labelText: 'Modifier Type',
            border: OutlineInputBorder(),
          ),
        ),
        const SizedBox(height: 10),
        if (_modifierType == 'simple')
          _buildSimpleModifierSelection()
        else if (_modifierType == 'complex')
          _buildComplexModifierSelection(),
      ],
    );
  }

 Widget _buildSimpleModifierSelection() {
  return ModifierSelector(
    predefinedModifiers: widget.modifiers,
    predefinedIntensifiers: [],
    currentModifier: _selectedModifiers.isNotEmpty ? _selectedModifiers.first : null, 
    isComplex: false,
    onModifierChanged: (value) => setState(() {
      if (value != null) {
        _selectedModifiers = [value];
      } else {
        _selectedModifiers = [];
      }
    }),
    onIntensifierChanged: (_) {},
  );
}

Widget _buildComplexModifierSelection() {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      ModifierSelector(
        predefinedModifiers: widget.modifiers,
        predefinedIntensifiers: widget.intensifiers,
        currentModifier: _selectedModifiers.isNotEmpty ? _selectedModifiers.first : null,
        currentIntensifier: _selectedIntensifiers.isNotEmpty ? _selectedIntensifiers.first : null,
        isComplex: true,
        onModifierChanged: (value) => setState(() {
          if (value != null) {
            _selectedModifiers = [value];
          } else {
            _selectedModifiers = [];
          }
        }),
        onIntensifierChanged: (value) => setState(() {
          if (value != null) {
            _selectedIntensifiers = [value];
          } else {
            _selectedIntensifiers = [];
          }
        }),
      ),
      const SizedBox(height: 10),
    ],
  );
}


String? _selectedComplexType;
String? _selectedSimpleType;

Widget _buildmeasureTypeSelection() {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Select Measure Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      DropdownButtonFormField<String>(
        value: _selectedmeasureType,
        items: ['simple', 'complex']
            .map((type) => DropdownMenuItem(value: type, child: Text(type)))
            .toList(),
        onChanged: (value) {
          setState(() {
            _selectedmeasureType = value;
            _selectedComplexType = null; // Reset complex selection
            _selectedSimpleType = null; // Reset simple selection
          });
        },
        decoration: const InputDecoration(
          labelText: 'Measure Type',
          border: OutlineInputBorder(),
        ),
      ),
      if (_selectedmeasureType == 'simple') ...[
        const SizedBox(height: 10),
        const Text('Select Simple Type', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
        DropdownButtonFormField<String>(
          value: _selectedSimpleType,
          items: ['number', 'quantity', 'measure']
              .map((type) => DropdownMenuItem(value: type, child: Text(type)))
              .toList(),
          onChanged: (value) => setState(() => _selectedSimpleType = value),
          decoration: const InputDecoration(
            labelText: 'Simple Type',
            border: OutlineInputBorder(),
          ),
        ),
      ],
      if (_selectedmeasureType == 'complex') ...[
        const SizedBox(height: 10),
        const Text('Select Complex Type', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
        DropdownButtonFormField<String>(
          value: _selectedComplexType,
          items: ['span', 'rate']
              .map((type) => DropdownMenuItem(value: type, child: Text(type)))
              .toList(),
          onChanged: (value) => setState(() => _selectedComplexType = value),
          decoration: const InputDecoration(
            labelText: 'Complex Type',
            border: OutlineInputBorder(),
          ),
        ),
      ],
    ],
  );
}
Widget _buildMeasurementInput() {
  if (_selectedmeasureType == 'complex') {
    if (_selectedComplexType == 'span') {
      return _buildSpanMeasurementInput();
    } else if (_selectedComplexType == 'rate') {
      return _buildRateMeasurementInput();
    }
  } else if (_selectedmeasureType == 'simple') {
    switch (_selectedSimpleType) {
      case 'number':
        return _buildNumberInput();
      case 'quantity':
        return _buildQuantityInput();
      case 'measure':
        return _buildMeasureInput();
      default:
        return const SizedBox(); // Empty widget if no type selected
    }
  }

  return MeasurementInputSection(
    noun: widget.noun,
    nounRelation: widget.nounRelation,
    measurements: widget.measurements,
  );
}

Widget _buildNumberInput() {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Enter Number', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      TextField(
        keyboardType: TextInputType.number,
        decoration: const InputDecoration(
          labelText: 'Number Value',
          border: OutlineInputBorder(),
        ),
        onChanged: (v) => setState(() => _selectedNumber = v),
      ),
    ],
  );
}

Widget _buildQuantityInput() {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text(
        'Select Quantity',
        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 10),
      Autocomplete<String>(
        initialValue: TextEditingValue(text: _selectedQuantity ?? ''),
        optionsBuilder: (TextEditingValue textEditingValue) {
          if (textEditingValue.text.isEmpty) {
            return widget.dquantities;
          }
          return widget.dquantities.where(
              (m) => m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
        },
        onSelected: (value) {
          setState(() {
            _selectedQuantity = value;
            print(_selectedQuantity);
          });
        },
        fieldViewBuilder:
            (context, textEditingController, focusNode, onFieldSubmitted) {
          return TextField(
            controller: textEditingController,
            focusNode: focusNode,
            decoration: const InputDecoration(
              labelText: 'Quantity',
              border: OutlineInputBorder(),
            ),
            onChanged: (value) {
              // Update _selectedQuantity immediately when typing
              setState(() {
                _selectedQuantity = value;
              });
            },
          );
        },
      ),
    ],
  );
}


Widget _buildMeasureInput() {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Select Measurement', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      Autocomplete<String>(
  initialValue: TextEditingValue(text:   _selectedMeasurement ?? ''),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.measurements;
    }
    return widget.measurements.where(
        (m) => m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
       _selectedMeasurement  = selection;
    });
  },
  fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: const InputDecoration(
        labelText: 'Start Measurement',
        border: OutlineInputBorder(),
      ),
      onChanged: (value) {
        // Update _selectedStartMeasurement immediately as the user types
        setState(() {
            _selectedMeasurement = value;
        });
      },
    );
  },
),

      const SizedBox(height: 10),
      TextField(
        keyboardType: TextInputType.number,
        decoration: const InputDecoration(
          labelText: 'Value',
          border: OutlineInputBorder(),
        ),
        onChanged: (v) => setState(() => _count = v),
      ),
    ],
  );
}




  Widget _buildSpanMeasurementInput() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Set Start Measurement & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
    Autocomplete<String>(
  initialValue: TextEditingValue(
    text: _startMeasurement ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.measurements;
    }
    return widget.measurements.where((m) =>
        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
      _startMeasurement = selection;
    });
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: const InputDecoration(
        labelText: 'Start Measurement',
        border: OutlineInputBorder(),
      ),
      onChanged: (value) {
        // Update the value as the user types
        setState(() {
          _startMeasurement = value;
        });
      },
    );
  },
),

        const SizedBox(height: 10),
        TextField(
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'Start count', border: OutlineInputBorder()),
          onChanged: (v) => setState(() => _startcount = v),
        ),
        const SizedBox(height: 20),
        const Text('Set End Measurement & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
     Autocomplete<String>(
  initialValue: TextEditingValue(
    text: _endMeasurement ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.measurements;
    }
    return widget.measurements.where((m) =>
        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
      _endMeasurement = selection;
    });
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: const InputDecoration(
        labelText: 'End Measurement',
        border: OutlineInputBorder(),
      ),
      onChanged: (value) {
        // Update immediately when user types
        setState(() {
          _endMeasurement = value;
        });
      },
    );
  },
),

        const SizedBox(height: 10),
        TextField(
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'End count', border: OutlineInputBorder()),
          onChanged: (v) => setState(() => _endcount = v),
        ),
      ],
    );
  }
  
   Widget _buildRateMeasurementInput() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Set unit_every & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
     Autocomplete<String>(
  initialValue: TextEditingValue(
    text: _startMeasurement ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.measurements;
    }
    return widget.measurements.where((m) =>
        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
      _startMeasurement = selection;
    });
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: const InputDecoration(
        labelText: 'unit_every',
        border: OutlineInputBorder(),
      ),
      onChanged: (value) {
        // Save value immediately as user types
        setState(() {
          _startMeasurement = value;
        });
      },
    );
  },
),

        const SizedBox(height: 10),
        TextField(
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'count', border: OutlineInputBorder()),
          onChanged: (v) => setState(() => _startcount = v),
        ),
        const SizedBox(height: 20),
        const Text('Set unit_value & count', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      Autocomplete<String>(
  initialValue: TextEditingValue(
    text: _endMeasurement ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return widget.measurements;
    }
    return widget.measurements.where((m) =>
        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    setState(() {
      _endMeasurement = selection;
    });
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: const InputDecoration(
        labelText: 'unit_value',
        border: OutlineInputBorder(),
      ),
      onChanged: (value) {
        // Save value immediately as the user types
        setState(() {
          _endMeasurement = value;
        });
      },
    );
  },
),

        const SizedBox(height: 10),
        TextField(
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'count', border: OutlineInputBorder()),
          onChanged: (v) => setState(() => _endcount = v),
        ),
      ],
    );
  }

  Widget _buildNavigationButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        if (_currentStep > 0)
          TextButton(onPressed: () => setState(() => _currentStep--), child: const Text('Back')),
        TextButton(
          onPressed: () {
            if (_currentStep < _totalSteps - 1) {
              setState(() => _currentStep++);
            } else {
              _saveAndClose();
            }
          },
          child: Text(_currentStep < _totalSteps - 1 ? 'Next' : 'Save'),
        ),
      ],
    );
  }
 
   void _saveAndClose() {
  // Save modifiers
  widget.nounRelation['nounModifiers'] ??= <String, List<String>>{};
  widget.nounRelation['nounModifiers'][widget.noun] = _selectedModifiers;

  // Save intensifiers
  widget.nounRelation['nounIntensifiers'] ??= <String, List<String>>{};
  widget.nounRelation['nounIntensifiers'][widget.noun] = _selectedIntensifiers;

  if (widget.relationType != 'Span') {
    widget.nounRelation['measureTypes'] ??= <String, String>{};
    widget.nounRelation['measureTypes'][widget.noun] = _selectedmeasureType ?? 'simple';
  }

  // Handle measurements based on type
  if (_selectedmeasureType == 'complex') {
    if (_selectedComplexType == 'rate') {
      _saveRateMeasurements();
    } else if (_selectedComplexType == 'span') {
      _saveSpanMeasurements();
    }
  } else {
    _saveSimpleMeasurements();
  }

  widget.onUpdate(widget.nounRelation);
  Navigator.pop(context);
}


   
  void _saveSpanMeasurements() {
    widget.nounRelation['startMeasurements'] ??= <String, String>{};
    widget.nounRelation['startQuantities'] ??= <String, double>{};
    widget.nounRelation['endMeasurements'] ??= <String, String>{};
    widget.nounRelation['endQuantities'] ??= <String, double>{};

    if (_startMeasurement != null && _startcount.isNotEmpty) {
      widget.nounRelation['startMeasurements'][widget.noun] = _startMeasurement!;
      widget.nounRelation['startQuantities'][widget.noun] = double.tryParse(_startcount) ?? 0.0;
    }
    if (_endMeasurement != null && _endcount.isNotEmpty) {
      widget.nounRelation['endMeasurements'][widget.noun] = _endMeasurement!;
      widget.nounRelation['endQuantities'][widget.noun] = double.tryParse(_endcount) ?? 0.0;
    }
  }
  void _saveRateMeasurements() {
  // Initialize rate-specific maps if they don't exist
  widget.nounRelation['unitEveryMeasurements'] ??= <String, String>{};
  widget.nounRelation['unitEveryQuantities'] ??= <String, double>{};
  widget.nounRelation['unitValueMeasurements'] ??= <String, String>{};
  widget.nounRelation['unitValueQuantities'] ??= <String, double>{};

  // Save unit_every measurement and count
  if (_startMeasurement != null && _startcount.isNotEmpty) {
    widget.nounRelation['unitEveryMeasurements'][widget.noun] = _startMeasurement!;
    widget.nounRelation['unitEveryQuantities'][widget.noun] = double.tryParse(_startcount) ?? 0.0;  // Fixed this line
  }

  // Save unit_value measurement and count
  if (_endMeasurement != null && _endcount.isNotEmpty) {
    widget.nounRelation['unitValueMeasurements'][widget.noun] = _endMeasurement!;
    widget.nounRelation['unitValueQuantities'][widget.noun] = double.tryParse(_endcount) ?? 0.0;
  }
  
  // Save the measure type
  widget.nounRelation['measureTypes'] ??= <String, String>{};
  widget.nounRelation['measureTypes'][widget.noun] = 'rate';

  // Print debug information
  print('Saved unit_every: ${widget.nounRelation['unitEveryMeasurements'][widget.noun]} ${widget.nounRelation['unitEveryQuantities'][widget.noun]}');
  print('Saved unit_value: ${widget.nounRelation['unitValueMeasurements'][widget.noun]} ${widget.nounRelation['unitValueQuantities'][widget.noun]}');
}

 void _saveSimpleMeasurements() {
  widget.nounRelation['simpleValues'] ??= <String, dynamic>{};

  switch (_selectedSimpleType) {
    case 'number':
       widget.nounRelation['number'] ??= <String, String>{};
      
      if (_selectedNumber != null) {
        // Store the selected quantity value
        widget.nounRelation['number'][widget.noun] = _selectedNumber;
        // Also store in simpleValues for compatibility
        widget.nounRelation['simpleValues'][widget.noun] = _selectedNumber;
      }
      break;
     case 'quantity':
      // Initialize a separate map for discrete quantities
      widget.nounRelation['quantity'] ??= <String, String>{};
      
      if (_selectedQuantity != null) {
        // Store the selected quantity value
        widget.nounRelation['quantity'][widget.noun] = _selectedQuantity;
        // Also store in simpleValues for compatibility
        widget.nounRelation['simpleValues'][widget.noun] = _selectedQuantity;
      }
      break;
    case 'measure':
      widget.nounRelation['measurements'] ??= <String, String>{};
      widget.nounRelation['quantities'] ??= <String, double>{};
      if (_selectedMeasurement != null && _count.isNotEmpty) {
        widget.nounRelation['measurements'][widget.noun] = _selectedMeasurement!;
        widget.nounRelation['quantities'][widget.noun] =
            double.tryParse(_count) ?? 0.0;
      }
      break;
    default:
      // Optionally handle unexpected types.
      break;
  }
  
  // Print the updated nounRelation map for debugging purposes.
  print(widget.nounRelation);
}
}
class MeasurementInputSection extends StatelessWidget {
  final String noun;
  final Map<String, dynamic> nounRelation;
  final List<String> measurements;

  const MeasurementInputSection({
    Key? key,
    required this.noun,
    required this.nounRelation,
    required this.measurements,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
      Autocomplete<String>(
  initialValue: TextEditingValue(
    text: nounRelation['measurements']?[noun] ?? '',
  ),
  optionsBuilder: (TextEditingValue textEditingValue) {
    if (textEditingValue.text.isEmpty) {
      return measurements;
    }
    return measurements.where((m) =>
        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
  },
  onSelected: (String selection) {
    nounRelation['measurements'][noun] = selection;
  },
  fieldViewBuilder: (BuildContext context,
      TextEditingController textEditingController,
      FocusNode focusNode,
      VoidCallback onFieldSubmitted) {
    return TextField(
      controller: textEditingController,
      focusNode: focusNode,
      decoration: const InputDecoration(
        labelText: 'Measurement',
        border: OutlineInputBorder(),
      ),
      onChanged: (value) {
        // Save value immediately as the user types
        nounRelation['measurements'][noun] = value;
      },
    );
  },
),

        const SizedBox(height: 10),
        TextField(
          controller: TextEditingController(
              text: nounRelation['quantities']?[noun]?.toString() ?? ''),
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(
            labelText: 'count',
            border: OutlineInputBorder(),
          ),
          onChanged: (v) => nounRelation['quantities'][noun] = double.tryParse(v),
        ),
      ],
    );
  }
}
