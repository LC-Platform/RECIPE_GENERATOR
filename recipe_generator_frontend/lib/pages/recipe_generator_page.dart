import 'package:flutter/material.dart';
import 'dart:math';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_services.dart';
import '../widgets/recipe_input_section.dart';
import '../widgets/ingredients_section.dart';
import '../widgets/RecipeDetailsPage.dart';

class RecipeGeneratorPage extends StatefulWidget {
  @override
  _RecipeGeneratorPageState createState() => _RecipeGeneratorPageState();
}

class _RecipeGeneratorPageState extends State<RecipeGeneratorPage> {
  String? selectedRecipe;
  List<String> selectedIngredients = [];
  List<String> recipeNames = [];
  Map<String, List<String>> ingredientCategories = {};
  bool isLoading = true;
  bool isCustomRecipe = false;
  TextEditingController customRecipeController = TextEditingController();
  Map<String, TextEditingController> customIngredientControllers = {};

  @override
  void initState() {
    super.initState();
    fetchRecipesAndIngredients();
  }

  @override
  void dispose() {
    customRecipeController.dispose();
    customIngredientControllers.values.forEach((controller) => controller.dispose());
    super.dispose();
  }

  Future<void> fetchRecipesAndIngredients() async {
    try {
      final data = await ApiService.fetchData();
      setState(() {
        recipeNames = List<String>.from(data['recipes']);
        ingredientCategories = {};
        data['ingredients'].forEach((subcategory, ingredients) {
          ingredientCategories[subcategory] = List<String>.from(ingredients);
          customIngredientControllers[subcategory] = TextEditingController();
        });
        isLoading = false;
      });
    } catch (e) {
      print('Error fetching data: $e');
      setState(() {
        recipeNames = [];
        ingredientCategories = {};
        isLoading = false;
      });
    }
  }

  Future<void> saveRecipeSelection() async {
    final String recipeName = isCustomRecipe ? customRecipeController.text : selectedRecipe!;
    if (recipeName.isEmpty || selectedIngredients.isEmpty) return;
    final String recipeId = generateRandomId();
    await saveRecipeId(recipeId);
    final Map<String, dynamic> data = {
      'recipe_id': recipeId,
      'recipe': recipeName,
      'ingredients': selectedIngredients,
    };
    try {
      await ApiService.postRecipeSelection(data);
      print('Data saved successfully');
    } catch (e) {
      print('Error saving data: $e');
    }
  }

  Future<void> addCustomRecipe(String customRecipe) async {
    final payload = {"category": "recipes", "option": customRecipe};
    try {
      await ApiService.postCustomOption(payload);
      await fetchRecipesAndIngredients();
    } catch (e) {
      print('Error adding custom recipe: $e');
    }
  }

  Future<void> addCustomIngredient(String subcategory) async {
    final controller = customIngredientControllers[subcategory];
    if (controller != null && controller.text.isNotEmpty) {
      String customIngredient = controller.text.trim();
      final payload = {
        "category": "ingredients",
        "subcategory": subcategory,
        "option": customIngredient
      };
      try {
        await ApiService.postCustomOption(payload);
        setState(() {
          if (!selectedIngredients.contains(customIngredient)) {
            selectedIngredients.add(customIngredient);
          }
          if (!ingredientCategories[subcategory]!.contains(customIngredient)) {
            ingredientCategories[subcategory]!.add(customIngredient);
          }
        });
        controller.clear();
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Custom ingredient added to $subcategory')));
      } catch (e) {
        print('Error adding custom ingredient: $e');
      }
    }
  }

  // Utility functions
  String generateRandomId() {
    final _random = Random();
    const _chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return List.generate(20, (index) => _chars[_random.nextInt(_chars.length)]).join();
  }

  Future<void> saveRecipeId(String id) async {
    final prefs = await SharedPreferences.getInstance();
    bool success = await prefs.setString('recipe_id', id);
    if (success) {
      print('Recipe ID saved: $id');
    } else {
      print('Failed to save Recipe ID');
    }
  }

  Widget buildRecipeInputSection() {
    return RecipeInputSection(
      isCustomRecipe: isCustomRecipe,
      selectedRecipe: selectedRecipe,
      recipeNames: recipeNames,
      customRecipeController: customRecipeController,
      onRecipeChanged: (value) {
        setState(() {
          selectedRecipe = value;
        });
      },
      onToggleCustom: () {
        setState(() {
          isCustomRecipe = !isCustomRecipe;
        });
      },
      onAddCustomRecipe: () async {
        final customRecipe = customRecipeController.text.trim();
        if (customRecipe.isNotEmpty) {
          await addCustomRecipe(customRecipe);
          customRecipeController.clear();
          setState(() {
            isCustomRecipe = false;
            selectedRecipe = customRecipe;
          });
          ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Recipe added successfully!')));
        }
      },
    );
  }

  Widget buildIngredientsSection() {
    return IngredientsSection(
      ingredientCategories: ingredientCategories,
      customIngredientControllers: customIngredientControllers,
      selectedIngredients: selectedIngredients,
      onIngredientToggle: (ingredient, isSelected) {
        setState(() {
          if (isSelected) {
            selectedIngredients.add(ingredient);
          } else {
            selectedIngredients.remove(ingredient);
          }
        });
      },
      onAddCustomIngredient: addCustomIngredient,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 38, 91, 134),
        centerTitle: true,
        title: const Text('Recipe Generator'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: isLoading
            ? const Center(child: CircularProgressIndicator())
            : SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Text(
                        'Recipe Generator',
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue.shade900,
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    buildRecipeInputSection(),
                    const SizedBox(height: 20),
                    buildIngredientsSection(),
                    const SizedBox(height: 20),
                    Center(
                      child: ElevatedButton(
                        onPressed: () async {
                          bool hasRecipeName = isCustomRecipe
                              ? customRecipeController.text.isNotEmpty
                              : selectedRecipe != null;
                          if (!hasRecipeName || selectedIngredients.isEmpty) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Please specify a recipe name and select ingredients'),
                              ),
                            );
                          } else {
                            bool confirm = await showDialog(
                              context: context,
                              builder: (context) => AlertDialog(
                                title: const Text('Confirm Submission'),
                                content: const Text('Are you sure you want to submit?'),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(context, false),
                                    child: const Text('No'),
                                  ),
                                  TextButton(
                                    onPressed: () => Navigator.pop(context, true),
                                    child: const Text('Yes'),
                                  ),
                                ],
                              ),
                            );
                            if (confirm) {
                              await saveRecipeSelection();
                              final recipeName = isCustomRecipe
                                  ? customRecipeController.text
                                  : selectedRecipe!;
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => RecipeDetailsPage(
                                    recipe: recipeName,
                                    ingredients: selectedIngredients,
                                  ),
                                ),
                              );
                            }
                          }
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color.fromARGB(255, 97, 182, 135),
                          padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                        ),
                        child: const Text(
                          'Submit',
                          style: TextStyle(fontSize: 16),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
      ),
    );
  }
}
