import 'package:flutter/material.dart';
import '../common/input_decorations.dart'; // (if you have common input decoration helpers)
import 'package:http/http.dart' as http;
import 'dart:convert';


class ModifierSelector extends StatefulWidget {
  final List<String> predefinedModifiers;
  final List<String> predefinedIntensifiers;
  final String? currentModifier;
  final String? currentIntensifier;
  final Function(String?) onModifierChanged;
  final Function(String?) onIntensifierChanged;
  
  /// You can pass additional parameters (for complex mode, etc.) as needed.
  final bool isComplex; 

  const ModifierSelector({
    Key? key,
    required this.predefinedModifiers,
    required this.predefinedIntensifiers,
    this.currentModifier,
    this.currentIntensifier,
    required this.onModifierChanged,
    required this.onIntensifierChanged,
    this.isComplex = false,
  }) : super(key: key);

  @override
  _ModifierSelectorState createState() => _ModifierSelectorState();
}

class _ModifierSelectorState extends State<ModifierSelector> {
  bool _useCustomModifier = false;
  bool _useCustomIntensifier = false;

  late TextEditingController _modifierController;
  late TextEditingController _intensifierController;
  final FocusNode _modifierFocus = FocusNode();
  final FocusNode _intensifierFocus = FocusNode();

  @override
  void initState() {
    super.initState();
    _modifierController = TextEditingController(text: widget.currentModifier ?? '');
    _intensifierController = TextEditingController(text: widget.currentIntensifier ?? '');
  }

  @override
  void dispose() {
    _modifierController.dispose();
    _intensifierController.dispose();
    _modifierFocus.dispose();
    _intensifierFocus.dispose();
    super.dispose();
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


  Widget _buildModifierField() {
    return _useCustomModifier
        ? Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _modifierController,
                  focusNode: _modifierFocus,
                  decoration: inputDecoration('Enter Custom Modifier', 'Modifier'),
                  onChanged: (value) {
                    widget.onModifierChanged(value);
                  },
                ),
              ),
              IconButton(
                icon: const Icon(Icons.save),
                tooltip: 'Save custom modifier',
                onPressed: () async {
                  final customModifier = _modifierController.text.trim();
                  if (customModifier.isNotEmpty) {
                    // Here you could call an API to add the modifier to the database
                    // For example: await addCustomOptionToDB('modifiers', option: customModifier);
                    widget.onModifierChanged(customModifier);
                    addCustomOptionToDB('modifiers', option: customModifier);

                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Please enter a custom modifier.')),
                    );
                  }
                },
              ),
            ],
          )
        : Autocomplete<String>(
            initialValue: TextEditingValue(text: widget.currentModifier ?? ''),
            optionsBuilder: (textEditingValue) {
              if (textEditingValue.text.isEmpty) {
                return widget.predefinedModifiers;
              }
              return widget.predefinedModifiers.where((modifier) => modifier
                  .toLowerCase()
                  .contains(textEditingValue.text.toLowerCase()));
            },
            onSelected: widget.onModifierChanged,
            fieldViewBuilder: (context, controller, focusNode, onFieldSubmitted) {
              return TextField(
                controller: controller,
                focusNode: focusNode,
                decoration: inputDecoration('Select Modifier', 'Modifier'),
                onChanged: widget.onModifierChanged,
              );
            },
          );
  }

  Widget _buildIntensifierField() {
    return _useCustomIntensifier
        ? Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _intensifierController,
                  focusNode: _intensifierFocus,
                  decoration: inputDecoration('Enter Custom Intensifier', 'Intensifier'),
                  onChanged: (value) {
                    widget.onIntensifierChanged(value);
                  },
                ),
              ),
              IconButton(
                icon: const Icon(Icons.save),
                tooltip: 'Save custom intensifier',
                onPressed: () async {
                  final customIntensifier = _intensifierController.text.trim();
                  if (customIntensifier.isNotEmpty) {
                    // Optionally add the custom option to the DB here.
                    widget.onIntensifierChanged(customIntensifier);
                    addCustomOptionToDB('intensifiers', option: customIntensifier);
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Please enter a custom intensifier.')),
                    );
                  }
                },
              ),
            ],
          )
        : Autocomplete<String>(
            initialValue: TextEditingValue(text: widget.currentIntensifier ?? ''),
            optionsBuilder: (textEditingValue) {
              if (textEditingValue.text.isEmpty) {
                return widget.predefinedIntensifiers;
              }
              return widget.predefinedIntensifiers.where((intensifier) => intensifier
                  .toLowerCase()
                  .contains(textEditingValue.text.toLowerCase()));
            },
            onSelected: widget.onIntensifierChanged,
            fieldViewBuilder: (context, controller, focusNode, onFieldSubmitted) {
              return TextField(
                controller: controller,
                focusNode: focusNode,
                decoration: inputDecoration('Select Intensifier', 'Intensifier'),
                onChanged: widget.onIntensifierChanged,
              );
            },
          );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Toggle between custom and predefined for modifiers.
        _buildToggleButton(
          label: _useCustomModifier ? 'Use predefined modifiers' : 'Add custom modifier',
          onPressed: () {
            setState(() {
              _useCustomModifier = !_useCustomModifier;
              if (_useCustomModifier) {
                _modifierController.text = widget.currentModifier ?? '';
                Future.delayed(Duration.zero, () => _modifierFocus.requestFocus());
              }
            });
          },
        ),
        _buildModifierField(),
        const SizedBox(height: 16),
        if (widget.isComplex) ...[
          // In complex mode, you might want to select an intensifier as well.
          _buildToggleButton(
            label: _useCustomIntensifier ? 'Use predefined intensifiers' : 'Add custom intensifier',
            onPressed: () {
              setState(() {
                _useCustomIntensifier = !_useCustomIntensifier;
                if (_useCustomIntensifier) {
                  _intensifierController.text = widget.currentIntensifier ?? '';
                  Future.delayed(Duration.zero, () => _intensifierFocus.requestFocus());
                }
              });
            },
          ),
          _buildIntensifierField(),
        ],
      ],
    );
  }

  Widget _buildToggleButton({required String label, required VoidCallback onPressed}) {
    return Align(
      alignment: Alignment.centerRight,
      child: TextButton.icon(
        icon: const Icon(Icons.edit),
        label: Text(label),
        onPressed: onPressed,
      ),
    );
  }
}
