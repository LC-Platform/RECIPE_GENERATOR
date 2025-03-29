import 'package:flutter/material.dart';

InputDecoration inputDecoration(String hint, String label) {
  return InputDecoration(
    labelText: label,
    hintText: hint,
    border: const OutlineInputBorder(),
    contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
  );
}
