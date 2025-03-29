import 'package:flutter/material.dart';

class QuantitySelector extends StatefulWidget {
  final Map<String, dynamic> localNounRelation;
  final List<String> dquantities;
  final Function(String, dynamic) updateRelation;
  final Future<void> Function(String, {required String option}) addCustomOptionToDB;

  const QuantitySelector({
    Key? key,
    required this.localNounRelation,
    required this.dquantities,
    required this.updateRelation,
    required this.addCustomOptionToDB,
  }) : super(key: key);

  @override
  _QuantitySelectorState createState() => _QuantitySelectorState();
}

class _QuantitySelectorState extends State<QuantitySelector> {
  late TextEditingController customQuantityController;
  late FocusNode customQuantityFocusNode;

  @override
  void initState() {
    super.initState();
    initCustomQuantityFlag();
    customQuantityController = TextEditingController(
      text: isCustomQuantity() ? widget.localNounRelation['quantity'] : '',
    );
    customQuantityFocusNode = FocusNode();
  }

  @override
  void dispose() {
    customQuantityController.dispose();
    customQuantityFocusNode.dispose();
    super.dispose();
  }

  void initCustomQuantityFlag() {
    if (widget.localNounRelation['isCustomQuantity'] == null) {
      widget.localNounRelation['isCustomQuantity'] =
          widget.localNounRelation['quantity'] != null &&
          !widget.dquantities.contains(widget.localNounRelation['quantity']);
    }
  }

  bool isCustomQuantity() {
    return widget.localNounRelation['isCustomQuantity'] ?? false;
  }

  void _toggleCustomQuantity() {
    setState(() {
      widget.localNounRelation['isCustomQuantity'] = !isCustomQuantity();
      if (isCustomQuantity()) {
        customQuantityController.text = widget.localNounRelation['quantity'] ?? '';
        Future.delayed(Duration.zero, () => customQuantityFocusNode.requestFocus());
      } else if (widget.localNounRelation['quantity'] != null &&
          !widget.dquantities.contains(widget.localNounRelation['quantity']) &&
          widget.dquantities.isNotEmpty) {
        widget.updateRelation('quantity', widget.dquantities.first);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 16),
        const Text(
          'Select Quantity',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 16),
        isCustomQuantity()
            ? Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: customQuantityController,
                      focusNode: customQuantityFocusNode,
                      decoration: InputDecoration(
                        labelText: 'Enter Custom Quantity',
                        border: OutlineInputBorder(),
                      ),
                      onChanged: (value) => widget.updateRelation('quantity', value),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.save),
                    tooltip: 'Save custom quantity',
                    onPressed: () {
                      final customQuantity = customQuantityController.text.trim();
                      if (customQuantity.isNotEmpty) {
                        widget.addCustomOptionToDB('dquantities', option: customQuantity).then((_) {
                          widget.updateRelation('quantity', customQuantity);
                        });
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Please enter a custom quantity first.'),
                          ),
                        );
                      }
                    },
                  ),
                ],
              )
            : Autocomplete<String>(
                initialValue: TextEditingValue(
                  text: widget.localNounRelation['quantity'] ?? '',
                ),
                optionsBuilder: (textEditingValue) {
                  if (textEditingValue.text.isEmpty) {
                    return widget.dquantities;
                  }
                  return widget.dquantities.where((q) =>
                      q.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                },
                onSelected: (selection) => widget.updateRelation('quantity', selection),
                fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
                  return TextField(
                    controller: textEditingController,
                    focusNode: focusNode,
                    decoration: InputDecoration(
                      labelText: 'Select Quantity',
                      border: OutlineInputBorder(),
                    ),
                    onChanged: (value) => widget.updateRelation('quantity', value),
                  );
                },
              ),
        Align(
          alignment: Alignment.centerRight,
          child: TextButton.icon(
            icon: Icon(isCustomQuantity() ? Icons.list : Icons.edit),
            label: Text(isCustomQuantity()
                ? 'Use predefined quantities'
                : 'Add custom quantity'),
            onPressed: _toggleCustomQuantity,
          ),
        ),
      ],
    );
  }
}
