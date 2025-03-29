import 'package:flutter/foundation.dart';

class RecipeState extends ChangeNotifier {
  String? selectedRecipe;
  List<String> selectedIngredients = [];
  String? recipeId;
  
  void setRecipe(String recipe) {
    selectedRecipe = recipe;
    notifyListeners();
  }
  
  void setIngredients(List<String> ingredients) {
    selectedIngredients = ingredients;
    notifyListeners();
  }
  
  void setRecipeId(String id) {
    recipeId = id;
    notifyListeners();
  }
  
  void clearSelections() {
    selectedRecipe = null;
    selectedIngredients = [];
    recipeId = null;
    notifyListeners();
  }
}