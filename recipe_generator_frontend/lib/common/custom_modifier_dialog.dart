import 'package:flutter/material.dart';

Future<String?> showCustomModifierDialog(BuildContext context) async {
  final TextEditingController controller = TextEditingController();
  return showDialog<String>(
    context: context,
    builder: (context) {
      return AlertDialog(
        title: const Text('Add Custom Modifier'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            hintText: 'Enter custom modifier',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(controller.text),
            child: const Text('Add'),
          ),
        ],
      );
    },
  );
}
