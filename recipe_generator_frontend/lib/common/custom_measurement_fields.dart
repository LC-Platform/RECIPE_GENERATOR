import 'package:flutter/material.dart';
import 'input_decorations.dart'; // Contains your shared _inputDecoration helper

/// Builds the rate fields using the custom measurement helper.
Widget buildRateFields({
  required Map<String, dynamic> localNounRelation,
  required List<String> measurements,
  required TextEditingController everyCountController,
  required TextEditingController valueCountController,
  required Function(String, dynamic) updateRelation,
  required Future<void> Function(String, {String? subcategory, required String option}) addCustomOptionToDB,
}) {
  return Card(
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Unit Every field with count
          buildCustomMeasurementField(
            localNounRelation: localNounRelation,
            predefinedMeasurements: measurements,
            measurementKey: 'unit_every',
            customFlagKey: 'isCustomUnitEvery',
            fieldLabel: 'Unit Every',
            selectLabel: 'Select Unit Every',
            updateRelation: updateRelation,
            addCustomOptionToDB: addCustomOptionToDB,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: everyCountController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Count',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.numbers),
            ),
            onChanged: (v) => updateRelation('every_count', double.tryParse(v)),
          ),
          const SizedBox(height: 20),
          // Unit Value field with count
          buildCustomMeasurementField(
            localNounRelation: localNounRelation,
            predefinedMeasurements: measurements,
            measurementKey: 'unit_value',
            customFlagKey: 'isCustomUnitValue',
            fieldLabel: 'Unit Value',
            selectLabel: 'Select Unit Value',
            updateRelation: updateRelation,
            addCustomOptionToDB: addCustomOptionToDB,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: valueCountController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Count',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.numbers),
            ),
            onChanged: (v) => updateRelation('value_count', double.tryParse(v)),
          ),
        ],
      ),
    ),
  );
}

/// Helper widget to build a custom measurement field.
/// [measurementKey] – key in the relation map for the measurement value.
/// [customFlagKey] – key in the relation map for the custom mode flag.
/// [fieldLabel] – label for the input field.
/// [selectLabel] – placeholder for the autocomplete field.
Widget buildCustomMeasurementField({
  required Map<String, dynamic> localNounRelation,
  required List<String> predefinedMeasurements,
  required String measurementKey,
  required String customFlagKey,
  required String fieldLabel,
  required String selectLabel,
  required Function(String, dynamic) updateRelation,
  required Future<void> Function(String, {String? subcategory, required String option}) addCustomOptionToDB,
}) {
  // Initialize flag if not already set.
  if (localNounRelation[customFlagKey] == null) {
    localNounRelation[customFlagKey] =
        localNounRelation[measurementKey] != null &&
        !predefinedMeasurements.contains(localNounRelation[measurementKey]);
  }
  return StatefulBuilder(
    builder: (context, setState) {
      bool isCustom = localNounRelation[customFlagKey] ?? false;
      TextEditingController controller = TextEditingController(
        text: isCustom ? localNounRelation[measurementKey] : '',
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
                        decoration: inputDecoration('Enter Custom $fieldLabel', measurementKey),
                        onChanged: (value) => updateRelation(measurementKey, value),
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
                            updateRelation(measurementKey, customValue);
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
                    text: localNounRelation[measurementKey] ?? '',
                  ),
                  optionsBuilder: (textEditingValue) {
                    if (textEditingValue.text.isEmpty) {
                      return predefinedMeasurements;
                    }
                    return predefinedMeasurements.where((m) =>
                        m.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                  },
                  onSelected: (selection) => updateRelation(measurementKey, selection),
                  fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
                    return TextField(
                      controller: textEditingController,
                      focusNode: focusNode,
                      decoration: inputDecoration(selectLabel, measurementKey),
                      onChanged: (value) => updateRelation(measurementKey, value),
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
                  localNounRelation[customFlagKey] = !isCustom;
                  if (localNounRelation[customFlagKey]) {
                    controller.text = localNounRelation[measurementKey] ?? '';
                    Future.delayed(Duration.zero, () => focusNode.requestFocus());
                  } else if (localNounRelation[measurementKey] != null &&
                      !predefinedMeasurements.contains(localNounRelation[measurementKey]) &&
                      predefinedMeasurements.isNotEmpty) {
                    updateRelation(measurementKey, predefinedMeasurements.first);
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

/// Builds the span fields (for start and end ranges) using the custom measurement helper.
Widget buildSpanFields({
  required Map<String, dynamic> localNounRelation,
  required List<String> predefinedMeasurements,
  required TextEditingController startQuantityController,
  required TextEditingController endQuantityController,
  required Function(String, dynamic) updateRelation,
  required Future<void> Function(String, {String? subcategory, required String option}) addCustomOptionToDB,
}) {
  return Card(
    child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Start Range
          const Text('Start Range', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          buildCustomMeasurementField(
            localNounRelation: localNounRelation,
            predefinedMeasurements: predefinedMeasurements,
            measurementKey: 'startMeasurement',
            customFlagKey: 'isCustomStartMeasurement',
            fieldLabel: 'Start Measurement',
            selectLabel: 'Select Start Measurement',
            updateRelation: updateRelation,
            addCustomOptionToDB: addCustomOptionToDB,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: startQuantityController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Start Quantity',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.numbers),
            ),
            onChanged: (v) => updateRelation('startQuantity', double.tryParse(v)),
          ),
          const SizedBox(height: 20),
          // End Range
          const Text('End Range', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          buildCustomMeasurementField(
            localNounRelation: localNounRelation,
            predefinedMeasurements: predefinedMeasurements,
            measurementKey: 'endMeasurement',
            customFlagKey: 'isCustomEndMeasurement',
            fieldLabel: 'End Measurement',
            selectLabel: 'Select End Measurement',
            updateRelation: updateRelation,
            addCustomOptionToDB: addCustomOptionToDB,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: endQuantityController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'End Quantity',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.numbers),
            ),
            onChanged: (v) => updateRelation('endQuantity', double.tryParse(v)),
          ),
        ],
      ),
    ),
  );
}
