// relation_utils.dart
import 'package:flutter/material.dart';

List<Widget> buildRadioButtons(
  Map<String, dynamic> nounRelation,
  List<String> options,
  int maxInRow,
  Function(String?) onChanged,
) {
  return [
    for (int i = 0; i < options.length; i += maxInRow)
      Row(
        children: [
          for (int j = i; j < i + maxInRow && j < options.length; j++)
            Expanded(
              child: Row(
                children: [
                  Radio<String>(
                    value: options[j],
                    groupValue: nounRelation['relationType'],
                    onChanged: onChanged,
                  ),
                  Flexible(child: Text(options[j], overflow: TextOverflow.ellipsis)),
                ],
              ),
            ),
        ],
      ),
  ];
}

void clearRelationField(Map<String, dynamic> nounRelation, String field) {
  nounRelation[field] = null;
  if (field == 'measurement') {
    nounRelation['quantity'] = null;
  }
}