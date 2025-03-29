import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:2000';

  static Future<Map<String, dynamic>> fetchData() async {
    final String url = '$baseUrl/recipes';
    final response = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load data with status code: ${response.statusCode}');
  }

  static Future<void> postRecipeSelection(Map<String, dynamic> data) async {
    final String url = '$baseUrl/save-selection';
    final response = await http.post(Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data));
    if (response.statusCode != 200) {
      throw Exception('Failed to save data');
    }
  }

  static Future<void> postCustomOption(Map<String, dynamic> payload) async {
    final String url = '$baseUrl/add-option';
    final response = await http.post(Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(payload));
    if (response.statusCode != 200) {
      throw Exception('Failed to add ${payload["option"]}');
    }
  }

   static Future<Map<String, dynamic>> getDropdownData() async {
    final response = await http.get(Uri.parse('$baseUrl/get-options'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to fetch dropdown data');
  }

  static Future<Map<String, dynamic>> getRecipeData(String recipeId) async {
    final response = await http.get(Uri.parse('$baseUrl/recipe/$recipeId'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load recipe');
  }

  static Future<void> postInstruction(Map<String, dynamic> instruction) async {
    final response = await http.post(
      Uri.parse('$baseUrl/create-graph'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(instruction),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to generate graph: ${response.statusCode}');
    }
  }

  static Future<void> addCustomOptionToDB(String category,
      {String? subcategory, required String option}) async {
    const String url = '$baseUrl/add-option';
    Map<String, dynamic> payload = {
      "category": category,
      "option": option,
    };
    if (subcategory != null) {
      payload["subcategory"] = subcategory;
    }
    final response = await http.post(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(payload),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to add $option: ${response.statusCode}');
    }
  }
}

