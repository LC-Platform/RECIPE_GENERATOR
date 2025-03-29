import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'widgets/RecipeDetailsPage.dart';

void main() => runApp(RecipeGeneratorApp());

class RecipeGeneratorApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Recipe Generator',
      home: RecipeGeneratorPage(),
    );
  }
}

class RecipeGeneratorPage extends StatefulWidget {
  @override
  _RecipeGeneratorPageState createState() => _RecipeGeneratorPageState();
}

class _RecipeGeneratorPageState extends State<RecipeGeneratorPage> {
  String? selectedRecipe;
  List<String> selectedIngredients = [];
  List<String> recipeNames = [];
  // Expecting the database structure where keys are subcategories like "सब्जियां"
  Map<String, List<String>> ingredientCategories = {};
  bool isLoading = true;
  bool isCustomRecipe = false;
  TextEditingController customRecipeController = TextEditingController();
  // Controllers for custom ingredient input per subcategory
  Map<String, TextEditingController> customIngredientControllers = {};

  @override
  void initState() {
    super.initState();
    fetchRecipesAndIngredients();
  }

  @override
  void dispose() {
    customRecipeController.dispose();
    for (var controller in customIngredientControllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  Future<void> fetchRecipesAndIngredients() async {
    const String url = 'http://127.0.0.1:2000/recipes'; // Adjust URL as needed
    try {
      final response =
          await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          recipeNames = List<String>.from(data['recipes']);
          ingredientCategories = {};
          // Expected structure: 
          // "ingredients": {
          //    "सब्जियां": ["हरा मिर्च", "काली मिर्च", ...],
          //    "दालें और अनाज": ["चना दाल", "उड़द दाल"],
          //    ... 
          // }
          data['ingredients'].forEach((subcategory, ingredients) {
            ingredientCategories[subcategory] = List<String>.from(ingredients);
            customIngredientControllers[subcategory] = TextEditingController();
          });
          isLoading = false;
        });
      } else {
        throw Exception(
            'Failed to load data with status code: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching data: $e');
      setState(() {
        recipeNames = [];
        ingredientCategories = {};
        isLoading = false;
      });
    }
  }

  Future<void> _saveRecipeId(String id) async {
    final prefs = await SharedPreferences.getInstance();
    bool success = await prefs.setString('recipe_id', id);
    if (success) {
      print('Recipe ID saved: $id');
    } else {
      print('Failed to save Recipe ID');
    }
  }

  String generateRandomId() {
    final _random = Random();
    const _chars =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return List.generate(20, (index) => _chars[_random.nextInt(_chars.length)])
        .join();
  }

  Future<void> saveRecipeSelection() async {
    final String recipeName =
        isCustomRecipe ? customRecipeController.text : selectedRecipe!;
    if (recipeName.isEmpty || selectedIngredients.isEmpty) return;
    final String recipeId = generateRandomId();
    _saveRecipeId(recipeId);
    const String url = 'http://127.0.0.1:2000/save-selection';
    final Map<String, dynamic> data = {
      'recipe_id': recipeId,
      'recipe': recipeName,
      'ingredients': selectedIngredients,
    };
    try {
      final response = await http.post(Uri.parse(url),
          headers: {'Content-Type': 'application/json'},
          body: json.encode(data));
      if (response.statusCode == 200) {
        print('Data saved successfully');
      } else {
        throw Exception('Failed to save data');
      }
    } catch (e) {
      print('Error saving data: $e');
    }
  }

  /// A generalized function to post a custom option to the backend.
  /// For custom ingredients, it sends both a main category ("ingredients") and a subcategory.
  Future<void> addCustomOptionToDB(String category,
      {String? subcategory, required String option}) async {
    const String url = 'http://127.0.0.1:2000/add-option';
    Map<String, dynamic> payload = {
      "category": category,
      "option": option,
    };
    if (subcategory != null) {
      payload["subcategory"] = subcategory;
    }
    try {
      final response = await http.post(Uri.parse(url),
          headers: {'Content-Type': 'application/json'},
          body: json.encode(payload));
      if (response.statusCode == 200) {
        print(
            '$option added successfully under ${subcategory ?? category}!');
      } else {
        print('Failed to add $option: ${response.statusCode}');
      }
    } catch (e) {
      print('Error adding $option: $e');
    }
  }

  Future<void> addCustomRecipe(String customRecipe) async {
    await addCustomOptionToDB("recipes", option: customRecipe);
    await fetchRecipesAndIngredients(); // Refresh recipes list
  }

  Future<void> addCustomIngredient(String subcategory) async {
    final controller = customIngredientControllers[subcategory];
    if (controller != null && controller.text.isNotEmpty) {
      String customIngredient = controller.text.trim();
      // Post the custom ingredient along with its subcategory
      await addCustomOptionToDB("ingredients",
          subcategory: subcategory, option: customIngredient);
      setState(() {
        if (!selectedIngredients.contains(customIngredient)) {
          selectedIngredients.add(customIngredient);
        }
        // Optionally update the local list to show the new custom ingredient
        if (!ingredientCategories[subcategory]!.contains(customIngredient)) {
          ingredientCategories[subcategory]!.add(customIngredient);
        }
      });
      controller.clear();
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Custom ingredient added to $subcategory')));
    }
  }

  /// Builds a card for each subcategory (for example, "सब्जियां")
  Widget buildIngredientCategoryCard(
      String subcategory, List<String> ingredients) {
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
                  onSelected: (bool selected) {
                    setState(() {
                      if (selected) {
                        selectedIngredients.add(ingredient);
                      } else {
                        selectedIngredients.remove(ingredient);
                      }
                    });
                  },
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
                      contentPadding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 8),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.add_circle, color: Colors.green),
                  onPressed: () => addCustomIngredient(subcategory),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget buildRecipeInputSection() {
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
                      onChanged: (value) {
                        setState(() {
                          selectedRecipe = value;
                        });
                      },
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        contentPadding: EdgeInsets.all(10),
                      ),
                    ),
            ),
            IconButton(
              icon: Icon(isCustomRecipe ? Icons.list : Icons.edit),
              tooltip: isCustomRecipe ? 'Use dropdown list' : 'Add custom recipe',
              onPressed: () {
                setState(() {
                  isCustomRecipe = !isCustomRecipe;
                });
              },
            ),
          ],
        ),
        if (isCustomRecipe) ...[
          const SizedBox(height: 10),
          Align(
            alignment: Alignment.centerRight,
            child: ElevatedButton.icon(
              onPressed: () async {
                final customRecipe = customRecipeController.text.trim();
                if (customRecipe.isNotEmpty) {
                  await addCustomRecipe(customRecipe);
                  customRecipeController.clear();
                  setState(() {
                    isCustomRecipe = false;
                    selectedRecipe = customRecipe;
                  });
                  ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Recipe added successfully!')));
                }
              },
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

  Widget buildIngredientsSection() {
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
            return buildIngredientCategoryCard(subcategory, ingredients);
          },
        ),
      ],
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
                                content: Text(
                                    'Please specify a recipe name and select ingredients'),
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
