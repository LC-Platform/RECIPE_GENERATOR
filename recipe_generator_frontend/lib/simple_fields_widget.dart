import 'package:flutter/material.dart';

class SimpleFieldsWidget extends StatefulWidget {
  final Map<String, dynamic> localNounRelation;
  final List<String> dquantities;
  final List<String> measurements;
  final Function(String, dynamic) updateRelation;

  const SimpleFieldsWidget({
    Key? key,
    required this.localNounRelation,
    required this.dquantities,
    required this.measurements,
    required this.updateRelation,
  }) : super(key: key);

  @override
  _SimpleFieldsWidgetState createState() => _SimpleFieldsWidgetState();
}

class _SimpleFieldsWidgetState extends State<SimpleFieldsWidget> {
  final TextEditingController _numberController = TextEditingController();

  InputDecoration _inputDecoration(String label, String key) {
    return InputDecoration(
      labelText: label,
      border: const OutlineInputBorder(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Simple Type Fields',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),

            DropdownButtonFormField<String>(
              value: widget.localNounRelation['fieldType'] ?? 'number',
              decoration: _inputDecoration('Select Field Type', 'fieldType'),
              items: const [
                DropdownMenuItem(value: 'number', child: Text('Number')),
                DropdownMenuItem(value: 'quantity', child: Text('Quantity')),
                DropdownMenuItem(value: 'measure', child: Text('Measure')),
              ],
              onChanged: (value) {
                setState(() {
                  widget.updateRelation('fieldType', value);
                });
              },
            ),
            const SizedBox(height: 16),

            if (widget.localNounRelation['fieldType'] == 'number')
              TextField(
                controller: _numberController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Enter Number',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.confirmation_number),
                ),
                onChanged: (v) =>
                    widget.updateRelation('number', int.tryParse(v)),
              ),

            if (widget.localNounRelation['fieldType'] == 'quantity') ...[
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: widget.localNounRelation['quantity'],
                items: widget.dquantities
                    .map((i) => DropdownMenuItem(value: i, child: Text(i)))
                    .toList(),
                onChanged: (v) => widget.updateRelation('quantity', v),
                decoration: _inputDecoration('Select Quantity', 'quantity'),
              ),
            ],

            if (widget.localNounRelation['fieldType'] == 'measure') ...[
              const SizedBox(height: 16),
              Autocomplete<String>(
                initialValue: TextEditingValue(
                  text: widget.localNounRelation['measurement'] ?? '',
                ),
                optionsBuilder: (TextEditingValue textEditingValue) {
                  if (textEditingValue.text.isEmpty) {
                    return widget.measurements;
                  }
                  return widget.measurements.where((measurement) =>
                      measurement
                          .toLowerCase()
                          .contains(textEditingValue.text.toLowerCase()));
                },
                onSelected: (String selection) {
                  widget.updateRelation('measurement', selection);
                },
                fieldViewBuilder: (BuildContext context,
                    TextEditingController textEditingController,
                    FocusNode focusNode,
                    VoidCallback onFieldSubmitted) {
                  return TextField(
                    controller: textEditingController,
                    focusNode: focusNode,
                    decoration: _inputDecoration('Measurement', 'measurement'),
                    onSubmitted: (value) {
                      widget.updateRelation('measurement', value);
                    },
                  );
                },
              ),
            ],
          ],
        ),
      ),
    );
  }
}
