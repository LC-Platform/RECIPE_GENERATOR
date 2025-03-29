import 'package:flutter/material.dart';
import 'pages/recipe_generator_page.dart';

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

