import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class SentencesDisplaySection extends StatefulWidget {
  final VoidCallback onSentencesUpdated;

  const SentencesDisplaySection({
    Key? key,
    required this.onSentencesUpdated,
  }) : super(key: key);

  @override
  State<SentencesDisplaySection> createState() => _SentencesDisplaySectionState();
}

class _SentencesDisplaySectionState extends State<SentencesDisplaySection> {
  List<String> sentences = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchSentences();
  }

  Future<void> fetchSentences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');

      if (recipeId == null) {
        throw Exception('Recipe ID not found');
      }

      final response = await http.get(
        Uri.parse('http://127.0.0.1:2000/get-sentences/$recipeId'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          sentences = List<String>.from(data['sentences']);
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load sentences');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (sentences.isEmpty) {
      return const Center(
        child: Text(
          'No sentences added yet',
          style: TextStyle(fontSize: 16, color: Colors.grey),
        ),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      itemCount: sentences.length,
      itemBuilder: (context, index) {
        return Card(
          margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              sentences[index],
              style: const TextStyle(fontSize: 16),
            ),
          ),
        );
      },
    );
  }
}