




import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:graphview/GraphView.dart';
import 'package:shared_preferences/shared_preferences.dart';

class RecipeDetailsPage extends StatefulWidget {
  final String recipe;
  final List<String> ingredients;

  RecipeDetailsPage({required this.recipe, required this.ingredients});

  @override
  _RecipeDetailsPageState createState() => _RecipeDetailsPageState();
}

class _RecipeDetailsPageState extends State<RecipeDetailsPage> {
  List<Map<String, dynamic>> instructions = [
    {
      'verb': null,
      'tam': null,
      'nounRelations': <Map<String, dynamic>>[],  // List to store multiple noun-relation pairs
      'ingredient': null,
      'showFullFields': true,
    }
  ];
  String generatedSentence = '';

  List<String> verbs = [];
  List<String> tams = [];
  List<String> nouns = [];
  List<String> relations = [];
  List<String> listofmeasuring = [];

  bool showGraph = false;
  late Graph graph;
  late FruchtermanReingoldAlgorithm algorithm;

  @override
  void initState() {
    super.initState();
    fetchDropdownData();
    graph = Graph();
    algorithm = FruchtermanReingoldAlgorithm();
  }

  void addNounRelationPair(int instructionIndex) {
    setState(() {
      if (instructions[instructionIndex]['nounRelations'] == null) {
        instructions[instructionIndex]['nounRelations'] = [];
      }
      instructions[instructionIndex]['nounRelations'].add({
        'noun': null,
        'relation': null,
      });
    });
  }

  Future<Map<String, dynamic>> fetchRecipeData() async {
    final prefs = await SharedPreferences.getInstance();
    final String? recipeId = prefs.getString('recipe_id');

    if (recipeId == null) {
      throw Exception('No recipe ID found');
    }

    final response = await http.get(Uri.parse('http://127.0.0.1:2000/recipe/$recipeId'));

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load recipe');
    }
  }

  Future<void> fetchDropdownData() async {
    try {
      final response = await http.get(Uri.parse('http://127.0.0.1:2000/get-options'));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          verbs = List<String>.from(data['verbs'] ?? []);
          tams = List<String>.from(data['tams'] ?? []);
          nouns = List<String>.from(data['nouns'] ?? []);
          relations = List<String>.from(data['relations'] ?? []);
        });
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  String generateSentenceFromGraph(Graph graph) {
    List<String> sentenceParts = [];
    for (var node in graph.nodes) {
      if (node.key!.value.toString().contains('Verb+TAM')) {
        continue;
      } else if (node.key!.value.toString().contains('Relation')) {
        sentenceParts.add('के साथ ${node.key!.value.toString().split(": ")[1]}');
      } else if (node.key!.value.toString().contains('Noun')) {
        sentenceParts.add('वह ${node.key!.value.toString().split(": ")[1]}');
      } else if (node.key!.value.toString().contains('Ingredient')) {
        if (sentenceParts.isEmpty) {
          sentenceParts.add('का उपयोग करके ${node.key!.value.toString().split(": ")[1]}');
        } else {
          sentenceParts.add('और ${node.key!.value.toString().split(": ")[1]} का उपयोग');
        }
      }
    }
    return sentenceParts.join(' ');
  }

  void convertInstructionToGraph() {
    setState(() {
      showGraph = true;
      var instruction = instructions.last;

      Node? verbTamNode = (instruction['verb'] != null && instruction['tam'] != null)
          ? Node.Id('Verb+TAM: ${instruction['verb']} ${instruction['tam']}')
          : null;

      // Handle multiple noun-relation pairs
      List<Node> nounNodes = [];
      List<Node> relationNodes = [];
      
      for (var nounRelation in instruction['nounRelations']) {
        if (nounRelation['noun'] != null && nounRelation['relation'] != null) {
          Node nounNode = Node.Id('Noun: ${nounRelation['noun']}');
          Node relationNode = Node(customCircularRelationNode('Relation:\n${nounRelation['relation']}'));
          
          nounNodes.add(nounNode);
          relationNodes.add(relationNode);
          graph.addNode(nounNode);
          graph.addNode(relationNode);
          
          if (verbTamNode != null) {
            graph.addEdge(verbTamNode, relationNode);
          }
          graph.addEdge(relationNode, nounNode);
        }
      }

      // Handle ingredients
      if (instruction['ingredient'] != null) {
        Node ingredientNode = Node.Id('Ingredient: ${instruction['ingredient']}');
        graph.addNode(ingredientNode);
        
        // Connect ingredient to all noun nodes
        for (var nounNode in nounNodes) {
          graph.addEdge(nounNode, ingredientNode);
        }
        
        if (verbTamNode != null) {
          graph.addEdge(ingredientNode, verbTamNode);
        }
      }

      instructions.removeLast();
      instructions.add({
        'ingredient': instruction['ingredient'],
        'nounRelations': [],
        'verb': null,
        'tam': null,
        'showFullFields': false,
      });
    });
  }

  Widget customCircularRelationNode(String text) {
    double size = 60 + (text.length * 2);
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: const Color.fromARGB(255, 17, 121, 78),
        shape: BoxShape.circle,
      ),
      alignment: Alignment.center,
      child: Text(
        text,
        textAlign: TextAlign.center,
        style: TextStyle(color: Colors.white, fontSize: 12),
      ),
    );
  }

  String getVerbTamDisplay(Map<String, dynamic> instruction) {
    return instruction['verb'] != null && instruction['tam'] != null
        ? '${instruction['verb']} + ${instruction['tam']}'
        : '';
  }

  Color determineNodeColor(String nodeValue) {
    if (nodeValue.contains('Verb')) {
      return Colors.blueAccent;
    } else if (nodeValue.contains('TAM')) {
      return Colors.greenAccent;
    } else if (nodeValue.contains('Noun')) {
      return Colors.orangeAccent;
    } else if (nodeValue.contains('Relation')) {
      return Colors.purpleAccent;
    } else {
      return Colors.redAccent;
    }
  }

  // ... [Previous code remains the same until the determineNodeColor method] ...

  void addInstruction() {
    setState(() {
      // Validate that required fields are filled
      var currentInstruction = instructions.last;
      if (currentInstruction['verb'] != null && 
          currentInstruction['tam'] != null && 
          currentInstruction['nounRelations'].isNotEmpty &&
          currentInstruction['ingredient'] != null) {
        
        convertInstructionToGraph();
        
        // Add a new blank instruction
        instructions.add({
          'verb': null,
          'tam': null,
          'nounRelations': <Map<String, dynamic>>[],
          
          'ingredient': null,
          'showFullFields': true,
        });
      } else {
        // Show error message if required fields are missing
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Please fill all required fields before adding a new instruction'),
            backgroundColor: Colors.red,
          ),
        );
      }
    });
  }

// ... [Rest of the code remains the same] ...

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Recipe Details'),
        backgroundColor: const Color.fromARGB(255, 38, 91, 134),
        centerTitle: true,
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: fetchRecipeData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData) {
            return const Center(child: Text('No recipe data available'));
          }

          final recipeData = snapshot.data!;
          final recipeName = recipeData['recipe'];
          final ingredients = recipeData['ingredients'];

        

// ... [Previous imports and class definitions remain the same until FutureBuilder] ...

          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  flex: 2,
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Recipe: $recipeName',
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 32, 72, 117),
                          ),
                        ),
                        const SizedBox(height: 20),
                        ...instructions.asMap().entries.map((entry) {
                          final index = entry.key;
                          final instruction = entry.value;
                          
                          return Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              if (instruction['showFullFields']) ...[
                                const Text(
                                  'Select Verb and TAM:',
                                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
                                ),
                                Row(
                                  children: [
                                    Expanded(
                                      child: DropdownButtonFormField<String>(
                                        value: instruction['verb'],
                                        items: verbs.map<DropdownMenuItem<String>>((String verb) {
                                          return DropdownMenuItem<String>(
                                            value: verb,
                                            child: Text(verb),
                                          );
                                        }).toList(),
                                        onChanged: (value) {
                                          setState(() {
                                            instruction['verb'] = value;
                                          });
                                        },
                                        decoration: const InputDecoration(
                                          labelText: 'Select Verb',
                                          border: OutlineInputBorder(),
                                        ),
                                      ),
                                    ),
                                    const SizedBox(width: 10),
                                    Expanded(
                                      child: DropdownButtonFormField<String>(
                                        value: instruction['tam'],
                                        items: tams.map<DropdownMenuItem<String>>((String tam) {
                                          return DropdownMenuItem<String>(
                                            value: tam,
                                            child: Text(tam),
                                          );
                                        }).toList(),
                                        onChanged: (value) {
                                          setState(() {
                                            instruction['tam'] = value;
                                          });
                                        },
                                        decoration: const InputDecoration(
                                          labelText: 'Select TAM',
                                          border: OutlineInputBorder(),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 20),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    const Text(
                                      'Noun-Relation Pairs:',
                                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                                    ),
                                    IconButton(
                                      icon: const Icon(Icons.add_circle),
                                      onPressed: () => addNounRelationPair(index),
                                      color: Colors.blue,
                                    ),
                                  ],
                                ),
                                ...instruction['nounRelations'].asMap().entries.map((nounRelEntry) {
                                  final nounRelation = nounRelEntry.value;
                                  return Column(
                                    children: [
                                      DropdownButtonFormField<String>(
                                        value: nounRelation['noun'],
                                        items: nouns.map<DropdownMenuItem<String>>((String noun) {
                                          return DropdownMenuItem<String>(
                                            value: noun,
                                            child: Text(noun),
                                          );
                                        }).toList(),
                                        onChanged: (value) {
                                          setState(() {
                                            nounRelation['noun'] = value;
                                          });
                                        },
                                        decoration: const InputDecoration(
                                          labelText: 'Select Noun',
                                          border: OutlineInputBorder(),
                                        ),
                                      ),
                                      const SizedBox(height: 10),
                                      DropdownButtonFormField<String>(
                                        value: nounRelation['relation'],
                                        items: relations.map<DropdownMenuItem<String>>((String relation) {
                                          return DropdownMenuItem<String>(
                                            value: relation,
                                            child: Text(relation),
                                          );
                                        }).toList(),
                                        onChanged: (value) {
                                          setState(() {
                                            nounRelation['relation'] = value;
                                          });
                                        },
                                        decoration: const InputDecoration(
                                          labelText: 'Select Relation',
                                          border: OutlineInputBorder(),
                                        ),
                                      ),
                                      const SizedBox(height: 20),
                                    ],
                                  );
                                }).toList(),
                                const Text(
                                  'Select Ingredient:',
                                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                                ),
                                DropdownButtonFormField<String>(
                                  value: instruction['ingredient'],
                                  items: (ingredients as List<dynamic>).map<DropdownMenuItem<String>>((dynamic ingredient) {
                                    return DropdownMenuItem<String>(
                                      value: ingredient.toString(),
                                      child: Text(ingredient.toString()),
                                    );
                                  }).toList(),
                                  onChanged: (value) {
                                    setState(() {
                                      instruction['ingredient'] = value;
                                    });
                                  },
                                  decoration: const InputDecoration(
                                    labelText: 'Select Ingredient',
                                    border: OutlineInputBorder(),
                                  ),
                                ),
                              ],
                            ],
                          );
                        }).toList(),
                        const SizedBox(height: 20),
                        Center(
                          child: ElevatedButton(
                            onPressed: addInstruction,
                            child: const Text('Add Instruction'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  flex: 3,
                  child: showGraph
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Instruction Graph:',
                              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                            ),
                            ClipRRect(
                              borderRadius: BorderRadius.circular(10),
                              child: Card(
                                elevation: 5,
                                child: Container(
                                  constraints: BoxConstraints(
                                    maxHeight: MediaQuery.of(context).size.height * 0.6,
                                    maxWidth: double.infinity,
                                  ),
                                  child: GraphView(
                                    graph: graph,
                                    algorithm: algorithm,
                                    builder: (Node node){
                                      final nodeColor = determineNodeColor(
                                          node.key!.value.toString());
                                      return Padding(
                                        padding: const EdgeInsets.all(8.0),
                                        child: Material(
                                          color: nodeColor,
                                          borderRadius: BorderRadius.circular(5),
                                          child: Padding(
                                            padding: const EdgeInsets.all(10.0),
                                            child: Text(
                                              node.key!.value.toString(),
                                              style: const TextStyle(
                                                  color: Colors.white,
                                                  fontWeight: FontWeight.bold),
                                            ),
                                          ),
                                        ),
                                      );
                                    },
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),
                            Text(
                              generateSentenceFromGraph(graph),
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.black87,
                              ),
                            ),
                          ],
                        )
                      : const SizedBox.shrink(),
                ),
              ],
            ),
          );
        }
    ),
  );
}
}