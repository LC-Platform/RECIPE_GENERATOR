import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


class MeasurementInputField extends StatefulWidget {
  final Map<String, dynamic> nounRelation;
  final List<String> predefinedMeasurements;
  final Function(String) onMeasurementChanged;
  final Function(double?) onQuantityChanged;

  const MeasurementInputField({
    required this.nounRelation,
    required this.predefinedMeasurements,
    required this.onMeasurementChanged,
    required this.onQuantityChanged,
    Key? key,
  }) : super(key: key);

  @override
  _MeasurementInputFieldState createState() => _MeasurementInputFieldState();
}


  Future<void> addCustomOptionToDB(
  BuildContext context,
  String category, {
  String? subcategory,
  required String option,
}) async {
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



class _MeasurementInputFieldState extends State<MeasurementInputField> {
  late bool isCustomMeasurement;
  late TextEditingController customMeasurementController;
  late TextEditingController quantityController;
  late FocusNode customMeasurementFocusNode;

  @override
  void initState() {
    super.initState();
    isCustomMeasurement = widget.nounRelation['isCustomMeasurement'] ?? false;
    customMeasurementController = TextEditingController(
      text: isCustomMeasurement ? widget.nounRelation['measurement'] : '',
    );
    quantityController = TextEditingController(
      text: widget.nounRelation['quantity']?.toString() ?? '',
    );
    customMeasurementFocusNode = FocusNode();
  }

  void toggleMeasurementMode() {
    setState(() {
      isCustomMeasurement = !isCustomMeasurement;
      widget.nounRelation['isCustomMeasurement'] = isCustomMeasurement;

      if (isCustomMeasurement) {
        customMeasurementController.text = widget.nounRelation['measurement'] ?? '';
        Future.delayed(Duration.zero, () => customMeasurementFocusNode.requestFocus());
      } else if (widget.nounRelation['measurement'] != null &&
          !widget.predefinedMeasurements.contains(widget.nounRelation['measurement']) &&
          widget.predefinedMeasurements.isNotEmpty) {
        widget.onMeasurementChanged(widget.predefinedMeasurements.first);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 16),
        const Text('Measurement', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        isCustomMeasurement
            ? Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: customMeasurementController,
                      focusNode: customMeasurementFocusNode,
                      decoration: const InputDecoration(labelText: 'Enter Custom Measurement'),
                      onChanged: widget.onMeasurementChanged,
                    ),
                  ),
                  IconButton(
  icon: const Icon(Icons.save),
  tooltip: 'Save custom measurement',
  onPressed: () {
    final customMeasurement = customMeasurementController.text.trim();
    if (customMeasurement.isNotEmpty) {
      widget.onMeasurementChanged(customMeasurement);
      addCustomOptionToDB(context, 'measurements', option: customMeasurement);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a custom measurement first.')),
      );
    }
  },
),

                ],
              )
            : Autocomplete<String>(
                initialValue: TextEditingValue(text: widget.nounRelation['measurement'] ?? ''),
                optionsBuilder: (textEditingValue) {
                  if (textEditingValue.text.isEmpty) {
                    return widget.predefinedMeasurements;
                  }
                  return widget.predefinedMeasurements.where((m) =>
                      m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                },
                onSelected: widget.onMeasurementChanged,
                fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
                  return TextField(
                    controller: textEditingController,
                    focusNode: focusNode,
                    decoration: const InputDecoration(labelText: 'Select Measurement'),
                    onChanged: widget.onMeasurementChanged,
                  );
                },
              ),
        Align(
          alignment: Alignment.centerRight,
          child: TextButton.icon(
            icon: Icon(isCustomMeasurement ? Icons.list : Icons.edit),
            label: Text(isCustomMeasurement ? 'Use predefined measurements' : 'Add custom measurement'),
            onPressed: toggleMeasurementMode,
          ),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: quantityController,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(
            labelText: 'Quantity',
            border: OutlineInputBorder(),
            prefixIcon: Icon(Icons.numbers),
          ),
          onChanged: (v) => widget.onQuantityChanged(double.tryParse(v)),
        ),
      ],
    );
  }

  @override
  void dispose() {
    customMeasurementController.dispose();
    quantityController.dispose();
    customMeasurementFocusNode.dispose();
    super.dispose();
  }
}