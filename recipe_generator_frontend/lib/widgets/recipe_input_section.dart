import 'package:flutter/material.dart';

class RecipeInputSection extends StatelessWidget {
  final bool isCustomRecipe;
  final String? selectedRecipe;
  final List<String> recipeNames;
  final TextEditingController customRecipeController;
  final ValueChanged<String?> onRecipeChanged;
  final VoidCallback onToggleCustom;
  final VoidCallback onAddCustomRecipe;

  const RecipeInputSection({
    Key? key,
    required this.isCustomRecipe,
    required this.selectedRecipe,
    required this.recipeNames,
    required this.customRecipeController,
    required this.onRecipeChanged,
    required this.onToggleCustom,
    required this.onAddCustomRecipe,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Name of the Recipe:',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: isCustomRecipe
                  ? TextFormField(
                      controller: customRecipeController,
                      decoration: const InputDecoration(
                        hintText: 'Enter custom recipe name',
                        border: OutlineInputBorder(),
                        contentPadding: EdgeInsets.all(10),
                      ),
                    )
                  : DropdownButtonFormField<String>(
                      value: selectedRecipe,
                      items: recipeNames.map((recipe) {
                        return DropdownMenuItem<String>(
                          value: recipe,
                          child: Text(recipe),
                        );
                      }).toList(),
                      onChanged: onRecipeChanged,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        contentPadding: EdgeInsets.all(10),
                      ),
                    ),
            ),
            IconButton(
              icon: Icon(isCustomRecipe ? Icons.list : Icons.edit),
              tooltip: isCustomRecipe ? 'Use dropdown list' : 'Add custom recipe',
              onPressed: onToggleCustom,
            ),
          ],
        ),
        if (isCustomRecipe) ...[
          const SizedBox(height: 10),
          Align(
            alignment: Alignment.centerRight,
            child: ElevatedButton.icon(
              onPressed: onAddCustomRecipe,
              icon: const Icon(Icons.add),
              label: const Text('Add Recipe'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 132, 172, 204),
              ),
            ),
          ),
        ],
      ],
    );
  }
}
