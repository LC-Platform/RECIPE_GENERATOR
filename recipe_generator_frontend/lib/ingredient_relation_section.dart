import 'package:flutter/material.dart';

class IngredientRelationSection extends StatefulWidget {
  final List<Map<String, dynamic>> instructions;
  final List<String> ingredients;
  final List<String> relations;
  final List<String> modifiers;
  final List<String> measurements;
  final Function(List<Map<String, dynamic>>) onUpdate;

  const IngredientRelationSection({
    Key? key,
    required this.instructions,
    required this.ingredients,
    required this.relations,
    required this.modifiers,
    required this.measurements,
    required this.onUpdate,
  }) : super(key: key);

  @override
  _IngredientRelationSectionState createState() => _IngredientRelationSectionState();
}

class _IngredientRelationSectionState extends State<IngredientRelationSection> {
  void addIngredientRelationPair(int instructionIndex) {
    final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
    var currentInstruction = updatedInstructions[instructionIndex];
    
    if (currentInstruction['ingredientRelations'] == null) {
      currentInstruction['ingredientRelations'] = <Map<String, dynamic>>[];
    }
    
    currentInstruction['ingredientRelations'].add({
      'ingredient': null,
      'relation': null,
      'modifier': null,
      'measurement': null,
      'quantity': null,
    });
    
    widget.onUpdate(updatedInstructions);
  }

  void removeIngredientRelationPair(int instructionIndex, int relationIndex) {
    final updatedInstructions = List<Map<String, dynamic>>.from(widget.instructions);
    updatedInstructions[instructionIndex]['ingredientRelations'].removeAt(relationIndex);
    widget.onUpdate(updatedInstructions);
  }

  void clearField(Map<String, dynamic> ingredientRelation, String field) {
    setState(() {
      ingredientRelation[field] = null;
      if (field == 'measurement') {
        ingredientRelation['quantity'] = null;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: widget.instructions.length,
      itemBuilder: (context, index) {
        final instruction = widget.instructions[index];
        if (instruction['ingredientRelations'] == null) {
          instruction['ingredientRelations'] = <Map<String, dynamic>>[];
        }

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Ingredient-Relation Pairs:',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.add_circle),
                  onPressed: () => addIngredientRelationPair(index),
                  color: Colors.blue,
                ),
              ],
            ),
            ...instruction['ingredientRelations'].asMap().entries.map((ingredientRelEntry) {
              final ingredientRelIndex = ingredientRelEntry.key;
              final ingredientRelation = ingredientRelEntry.value;
              return Card(
                margin: const EdgeInsets.symmetric(vertical: 8),
                child: Stack(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          DropdownButtonFormField<String>(
                            value: ingredientRelation['ingredient'],
                            items: widget.ingredients.map<DropdownMenuItem<String>>((String ingredient) {
                              return DropdownMenuItem<String>(
                                value: ingredient,
                                child: Text(ingredient),
                              );
                            }).toList(),
                            onChanged: (value) {
                              setState(() {
                                ingredientRelation['ingredient'] = value;
                              });
                            },
                            decoration: InputDecoration(
                              labelText: 'Select Ingredient',
                              border: const OutlineInputBorder(),
                              suffixIcon: ingredientRelation['ingredient'] != null
                                  ? IconButton(
                                      icon: const Icon(Icons.clear),
                                      onPressed: () => clearField(ingredientRelation, 'ingredient'),
                                    )
                                  : null,
                            ),
                          ),
                          const SizedBox(height: 10),
                          Padding(
                            padding: const EdgeInsets.only(left: 16.0),
                            child: DropdownButtonFormField<String>(
                              value: ingredientRelation['modifier'],
                              items: widget.modifiers.map<DropdownMenuItem<String>>((String modifier) {
                                return DropdownMenuItem<String>(
                                  value: modifier,
                                  child: Text(modifier, style: const TextStyle(fontSize: 14)),
                                );
                              }).toList(),
                              onChanged: (value) {
                                setState(() {
                                  ingredientRelation['modifier'] = value;
                                });
                              },
                              decoration: InputDecoration(
                                labelText: 'Select Modifier (if any)',
                                border: const OutlineInputBorder(),
                                suffixIcon: ingredientRelation['modifier'] != null
                                    ? IconButton(
                                        icon: const Icon(Icons.clear),
                                        onPressed: () => clearField(ingredientRelation, 'modifier'),
                                      )
                                    : null,
                              ),
                            ),
                          ),
                          const SizedBox(height: 10),
                          Padding(
                            padding: const EdgeInsets.only(left: 16.0),
                            child: DropdownButtonFormField<String>(
                              value: ingredientRelation['measurement'],
                              items: widget.measurements.map<DropdownMenuItem<String>>((String measurement) {
                                return DropdownMenuItem<String>(
                                  value: measurement,
                                  child: Text(measurement, style: const TextStyle(fontSize: 14)),
                                );
                              }).toList(),
                              onChanged: (value) {
                                setState(() {
                                  ingredientRelation['measurement'] = value;
                                  if (value == null) {
                                    ingredientRelation['quantity'] = null;
                                  }
                                });
                              },
                              decoration: InputDecoration(
                                labelText: 'Select Measurement (if any)',
                                border: const OutlineInputBorder(),
                                suffixIcon: ingredientRelation['measurement'] != null
                                    ? IconButton(
                                        icon: const Icon(Icons.clear),
                                        onPressed: () => clearField(ingredientRelation, 'measurement'),
                                      )
                                    : null,
                              ),
                            ),
                          ),
                          if (ingredientRelation['measurement'] != null) ...[
                            const SizedBox(height: 10),
                            Padding(
                              padding: const EdgeInsets.only(left: 32.0),
                              child: TextFormField(
                                key: ValueKey('ingredient_${ingredientRelIndex}_quantity'),
                                initialValue: ingredientRelation['quantity']?.toString(),
                                onChanged: (value) {
                                  if (value.isNotEmpty) {
                                    setState(() {
                                      ingredientRelation['quantity'] = int.tryParse(value);
                                    });
                                  }
                                },
                                keyboardType: TextInputType.number,
                                decoration: const InputDecoration(
                                  labelText: 'Enter Quantity',
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 14),
                              ),
                            ),
                          ],
                          const SizedBox(height: 10),
                          DropdownButtonFormField<String>(
                            value: ingredientRelation['relation'],
                            items: widget.relations.map<DropdownMenuItem<String>>((String relation) {
                              return DropdownMenuItem<String>(
                                value: relation,
                                child: Text(relation),
                              );
                            }).toList(),
                            onChanged: (value) {
                              setState(() {
                                ingredientRelation['relation'] = value;
                              });
                            },
                            decoration: InputDecoration(
                              labelText: 'Select Relation',
                              border: const OutlineInputBorder(),
                              suffixIcon: ingredientRelation['relation'] != null
                                  ? IconButton(
                                      icon: const Icon(Icons.clear),
                                      onPressed: () => clearField(ingredientRelation, 'relation'),
                                    )
                                  : null,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Positioned(
                      top: -3,
                      right: 8,
                      child: IconButton(
                        icon: const Icon(Icons.close, color: Color.fromARGB(255, 20, 20, 20)),
                        onPressed: () => removeIngredientRelationPair(index, ingredientRelIndex),
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
          ],
        );
      },
    );
  }
}