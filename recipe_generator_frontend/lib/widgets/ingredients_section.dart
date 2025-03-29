import 'package:flutter/material.dart';

class IngredientsSection extends StatelessWidget {
  final Map<String, List<String>> ingredientCategories;
  final Map<String, TextEditingController> customIngredientControllers;
  final List<String> selectedIngredients;
  final Function(String ingredient, bool isSelected) onIngredientToggle;
  final Future<void> Function(String subcategory) onAddCustomIngredient;

  const IngredientsSection({
    Key? key,
    required this.ingredientCategories,
    required this.customIngredientControllers,
    required this.selectedIngredients,
    required this.onIngredientToggle,
    required this.onAddCustomIngredient,
  }) : super(key: key);

  Widget buildIngredientCategoryCard(String subcategory, List<String> ingredients, BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6.0),
      elevation: 2,
      child: ExpansionTile(
        title: Text(
          subcategory,
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8),
            child: Wrap(
              spacing: 8.0,
              runSpacing: 4.0,
              children: ingredients.map((ingredient) {
                bool isSelected = selectedIngredients.contains(ingredient);
                return FilterChip(
                  label: Text(ingredient),
                  selected: isSelected,
                  onSelected: (bool selected) => onIngredientToggle(ingredient, selected),
                );
              }).toList(),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: customIngredientControllers[subcategory],
                    decoration: InputDecoration(
                      hintText: 'Add custom ingredient...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8.0),
                      ),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.add_circle, color: Colors.green),
                  onPressed: () => onAddCustomIngredient(subcategory),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Select Ingredients by Subcategory:',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 8),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: ingredientCategories.keys.length,
          itemBuilder: (context, index) {
            final subcategory = ingredientCategories.keys.elementAt(index);
            final ingredients = ingredientCategories[subcategory]!;
            return buildIngredientCategoryCard(subcategory, ingredients, context);
          },
        ),
      ],
    );
  }
}
