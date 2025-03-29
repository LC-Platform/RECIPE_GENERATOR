import 'package:flutter/material.dart';
import 'input_decorations.dart'; // your shared input decoration helper

class CustomQuantityField extends StatefulWidget {
  final Map<String, dynamic> localNounRelation;
  final List<String> predefinedQuantities;
  final Function(String, dynamic) updateRelation;
  final Future<void> Function(String, {required String option}) addCustomOptionToDB;

  const CustomQuantityField({
    Key? key,
    required this.localNounRelation,
    required this.predefinedQuantities,
    required this.updateRelation,
    required this.addCustomOptionToDB,
  }) : super(key: key);

  @override
  _CustomQuantityFieldState createState() => _CustomQuantityFieldState();
}

class _CustomQuantityFieldState extends State<CustomQuantityField> {
  late TextEditingController customQuantityController;
  late FocusNode customQuantityFocusNode;

  @override
  void initState() {
    super.initState();
    _initCustomQuantityFlag();
    customQuantityController = TextEditingController(
      text: _isCustomQuantity() ? widget.localNounRelation['quantity'] ?? '' : '',
    );
    customQuantityFocusNode = FocusNode();
  }

  @override
  void dispose() {
    customQuantityController.dispose();
    customQuantityFocusNode.dispose();
    super.dispose();
  }

  // Ensure the flag is set initially.
  void _initCustomQuantityFlag() {
    if (widget.localNounRelation['isCustomQuantity'] == null) {
      widget.localNounRelation['isCustomQuantity'] =
          widget.localNounRelation['quantity'] != null &&
          !widget.predefinedQuantities.contains(widget.localNounRelation['quantity']);
    }
  }

  bool _isCustomQuantity() {
    return widget.localNounRelation['isCustomQuantity'] ?? false;
  }

  void _toggleCustomQuantityMode() {
    setState(() {
      bool isCustom = _isCustomQuantity();
      widget.localNounRelation['isCustomQuantity'] = !isCustom;
      if (!isCustom) {
        // Switching to custom mode: prefill and request focus.
        customQuantityController.text = widget.localNounRelation['quantity'] ?? '';
        Future.delayed(Duration.zero, () => customQuantityFocusNode.requestFocus());
      } else if (widget.localNounRelation['quantity'] != null &&
          !widget.predefinedQuantities.contains(widget.localNounRelation['quantity']) &&
          widget.predefinedQuantities.isNotEmpty) {
        widget.updateRelation('quantity', widget.predefinedQuantities.first);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return StatefulBuilder(
      builder: (context, setState) {
        bool isCustom = _isCustomQuantity();
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 16),
            const Text(
              'Select Quantity',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            isCustom
                ? Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: customQuantityController,
                          focusNode: customQuantityFocusNode,
                          decoration: inputDecoration('Enter Custom Quantity', 'quantity'),
                          onChanged: (value) => widget.updateRelation('quantity', value),
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.save),
                        tooltip: 'Save custom quantity',
                        onPressed: () {
                          final customQuantity = customQuantityController.text.trim();
                          if (customQuantity.isNotEmpty) {
                            widget.addCustomOptionToDB('dquantities', option: customQuantity)
                                .then((_) {
                              widget.updateRelation('quantity', customQuantity);
                            });
                          } else {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Please enter a custom quantity first.')),
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
                        return widget.predefinedQuantities;
                      }
                      return widget.predefinedQuantities.where((q) =>
                          q.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                    },
                    onSelected: (selection) => widget.updateRelation('quantity', selection),
                    fieldViewBuilder: (context, textEditingController, focusNode, onFieldSubmitted) {
                      return TextField(
                        controller: textEditingController,
                        focusNode: focusNode,
                        decoration: inputDecoration('Select Quantity', 'quantity'),
                        onChanged: (value) => widget.updateRelation('quantity', value),
                      );
                    },
                  ),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                icon: Icon(isCustom ? Icons.list : Icons.edit),
                label: Text(isCustom ? 'Use predefined quantities' : 'Add custom quantity'),
                onPressed: _toggleCustomQuantityMode,
              ),
            ),
          ],
        );
      },
    );
  }
}
