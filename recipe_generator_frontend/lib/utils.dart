import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class RecipeUtils {
  static void clearField(Map<String, dynamic> relation, String field) {
    relation[field] = null;
    if (field == 'measurement') {
      relation['quantity'] = null;
    }
  }

  static Future<void> resetBackendGraph() async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:2000/reset-graph'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to reset graph on backend');
      }
    } catch (e) {
      throw Exception('Error resetting graph: $e');
    }
  }

  static Future<void> graphToUsr() async {
    try {
      await http.get(Uri.parse('http://127.0.0.1:2000/graphtousr'));
    } catch (e) {
      throw Exception('Failed to call graphtousr API: $e');
    }
  }

  static Future<Map<String, dynamic>> fetchRecipeData(String recipeId) async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:2000/recipe/$recipeId')
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load recipe');
      }
    } catch (e) {
      throw Exception('Error fetching recipe data: $e');
    }
  }

  static Future<Map<String, List<String>>> fetchDropdownData() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:2000/get-options')
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {
          'verbs': List<String>.from(data['verbs'] ?? []),
          'tams': List<String>.from(data['tams'] ?? []),
          'nouns': List<String>.from(data['nouns'] ?? []),
          'relations': List<String>.from(data['relations'] ?? []),
          'modifiers': List<String>.from(data['modifiers'] ?? []),
          'measurements': List<String>.from(data['measurements'] ?? []),
        };
      } else {
        throw Exception('Failed to load dropdown data');
      }
    } catch (e) {
      throw Exception('Error fetching dropdown data: $e');
    }
  }

  static Future<Map<String, dynamic>> sendInstructionToBackend(
    Map<String, dynamic> instruction
  ) async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:2000/create-graph'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(instruction),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to generate graph: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error sending instruction: $e');
    }
  }
}