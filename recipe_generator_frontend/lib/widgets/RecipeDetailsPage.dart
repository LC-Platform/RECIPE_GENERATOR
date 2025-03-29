import 'package:flutter/material.dart';
import 'noun_relation_section.dart';
import 'graph_display_section.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class RecipeDetailsPage extends StatefulWidget {
  final String recipe;
  final List<String> ingredients;

  const RecipeDetailsPage({
    Key? key,
    required this.recipe,
    required this.ingredients,
  }) : super(key: key);

  @override
  _RecipeDetailsPageState createState() => _RecipeDetailsPageState();
}

class _RecipeDetailsPageState extends State<RecipeDetailsPage> {
  // State variables for instructions and dropdown options
  List<Map<String, dynamic>> instructions = [];
  List<String> verbs = [];
  List<String> tams = [];
  List<String> nouns = [];
  List<String> relations = [];
  List<String> modifiers = [];
  List<String> intensifiers = [];
  List<String> measurements = [];
  List<String> dquantities = [];
  bool showGraph = false;
  String? graphImageBase64;
  String? hindiSentence;
  String? usrData;
  bool showFullFields = true;

  // Cache the recipe data future so it isn't refetched on every rebuild
  late Future<Map<String, dynamic>> _recipeFuture;

  @override
  void initState() {
    super.initState();
    fetchDropdownData();
    _recipeFuture = fetchRecipeData();
    instructions = [
      {
        'verb': null,
        'tam': null,
        'nounRelations': <Map<String, dynamic>>[],
        'showFullFields': true,
      }
    ];
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
          modifiers = List<String>.from(data['modifiers'] ?? []);
          intensifiers = List<String>.from(data['intensifiers'] ?? []);
          measurements = List<String>.from(data['measurements'] ?? []);
          dquantities = List<String>.from(data['dquantities'] ?? []);
        });
      } else {
        throw Exception('Failed to fetch dropdown data');
      }
    } catch (e) {
      debugPrint('Error fetching dropdown data: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading data: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Future<Map<String, dynamic>> fetchRecipeData() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');
      if (recipeId == null) throw Exception('No recipe ID found');

      final response = await http.get(Uri.parse('http://127.0.0.1:2000/recipe/$recipeId'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load recipe');
      }
    } catch (e) {
      debugPrint('Error fetching recipe data: $e');
      rethrow;
    }
  }

  void addInstruction() async {
    setState(() {
      // Get current instruction and send it to the backend
      var currentInstruction = instructions.last;
      sendInstructionToBackend(currentInstruction);
    });
  }

  Future<void> sendInstructionToBackend(Map<String, dynamic> instruction) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');

      if (recipeId == null) {
        throw Exception('Recipe ID not found');
      }

      final instructionWithId = {
        ...instruction,
        'recipe_id': recipeId,
      };

      final response = await http.post(
        Uri.parse('http://127.0.0.1:2000/create-graph'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(instructionWithId),
      );

      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        debugPrint("Graph Image from API: ${responseData['graph_image']}");
        setState(() {
          graphImageBase64 = responseData['graph_image'];
          hindiSentence = responseData['hindi_sentence'];
          showGraph = true;
        });
        await graphtousr();
      } else {
        throw Exception('Failed to generate graph: ${response.statusCode}');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
        );
      }
    }

    // Reset instructions for new input
    setState(() {
      instructions = [
        {
          'verb': null,
          'tam': null,
          'nounRelations': <Map<String, dynamic>>[],
          'showFullFields': true,
        }
      ];
    });
  }

  Future<void> handleSubmit() async {
    final bool shouldSubmit = await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text("Confirm Submission"),
            content: const Text("Are you sure you want to submit?"),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: const Text("Cancel"),
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: const Text("Submit"),
              ),
            ],
          ),
        ) ??
        false;

    if (!shouldSubmit) return;

    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');

      if (recipeId == null) {
        throw Exception('Recipe ID not found');
      }

      final resetResponse = await http.post(
        Uri.parse('http://127.0.0.1:2000/reset-graph'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'recipe_id': recipeId}),
      );

      if (resetResponse.statusCode != 200) {
        throw Exception('Failed to reset graph');
      }

      addInstruction();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Graph created.'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error during reset: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Future<void> graphtousr() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');

      if (recipeId == null) {
        throw Exception('Recipe ID not found');
      }

      final response = await http.post(
        Uri.parse('http://127.0.0.1:2000/graphtousr'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'recipe_id': recipeId}),
      );

      if (response.statusCode == 200) {
        final responseBody = json.decode(response.body);
        setState(() {
          usrData = responseBody['result'];
        });
        await hindiGenerationRequest(responseBody);
      } else {
        final errorBody = json.decode(response.body);
        throw Exception(errorBody['error'] ?? 'Failed to process graph');
      }
    } catch (e) {
      debugPrint('Failed to call graphtousr API: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error processing graph: $e'), backgroundColor: Colors.red),
        );
      }
      rethrow;
    }
  }

  Future<void> hindiGenerationRequest(Map<String, dynamic> responseData) async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5001/hindi-generation'),
        headers: {'Content-Type': 'application/json; charset=UTF-8'},
        body: jsonEncode(responseData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['result'] is String) {
          setState(() {
            hindiSentence = data['result'];
          });
        } else {
          throw Exception('Invalid response structure');
        }
      } else {
        throw Exception('Failed to process Hindi generation: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('Failed to call Hindi generation API: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error during Hindi generation: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  void handleSentenceStateChanged() {
    setState(() {
      graphImageBase64 = null;
      hindiSentence = null;
      showGraph = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Recipe Details'),
        backgroundColor: const Color.fromARGB(255, 38, 91, 134),
        centerTitle: true,
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isDesktop = constraints.maxWidth > 900;

            // Recipe Details Section (fetched once)
            Widget recipeDetailsSection = FutureBuilder<Map<String, dynamic>>(
              future: _recipeFuture,
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
                final ingredients = List<String>.from(recipeData['ingredients'] ?? []);

                return buildMainContent(recipeName, ingredients);
              },
            );

            // Conditionally build the Graph Section only if there is content to show.
            Widget? graphSection;
            if (showGraph ||
                graphImageBase64 != null ||
                hindiSentence != null ||
                usrData != null) {
              graphSection = SizedBox(
                height: isDesktop ? constraints.maxHeight : null,
                child: GraphDisplaySection(
                  showGraph: showGraph,
                  graphImageBase64: graphImageBase64,
                  hindiSentence: hindiSentence,
                  usr: usrData,
                  onSentenceStateChanged: handleSentenceStateChanged,
                ),
              );
            }

            if (isDesktop) {
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      flex: 2,
                      child: SingleChildScrollView(child: recipeDetailsSection),
                    ),
                    if (graphSection != null) ...[
                      const SizedBox(width: 16),
                      Expanded(child: graphSection),
                    ],
                  ],
                ),
              );
            } else {
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: CustomScrollView(
                  slivers: [
                    SliverToBoxAdapter(child: recipeDetailsSection),
                    if (graphSection != null) const SliverToBoxAdapter(child: SizedBox(height: 20)),
                    if (graphSection != null) SliverToBoxAdapter(child: graphSection),
                  ],
                ),
              );
            }
          },
        ),
      ),
    );
  }

  Widget buildMainContent(String recipeName, List<String> ingredients) {
    return Column(
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
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: ingredients.map((ingredient) {
            return Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: const Color.fromARGB(255, 200, 230, 255),
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.5),
                    blurRadius: 4,
                    offset: const Offset(2, 2),
                  ),
                ],
              ),
              child: Text(
                ingredient,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                  color: Colors.black87,
                ),
              ),
            );
          }).toList(),
        ),
        const SizedBox(height: 20),
        if (instructions.isNotEmpty && instructions.first['showFullFields'])
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Select Verb and TAM:',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
              ),
              const SizedBox(height: 10),
              LayoutBuilder(
                builder: (context, constraints) {
                  if (constraints.maxWidth < 600) {
                    return Column(
                      children: [
                        buildVerbDropdown(instructions.first),
                        const SizedBox(height: 10),
                        buildTamDropdown(instructions.first),
                      ],
                    );
                  } else {
                    return Row(
                      children: [
                        Expanded(child: buildVerbDropdown(instructions.first)),
                        const SizedBox(width: 10),
                        Expanded(child: buildTamDropdown(instructions.first)),
                      ],
                    );
                  }
                },
              ),
            ],
          ),
        const SizedBox(height: 20),
        NounRelationSection(
          instructions: instructions,
          nouns: nouns,
          relations: relations,
          modifiers: modifiers,
          intensifiers: intensifiers,
          measurements: measurements,
          dquantities: dquantities,
          onUpdate: (updatedInstructions) {
            setState(() {
              instructions = updatedInstructions;
            });
          },
        ),
        const SizedBox(height: 20),
        Center(
          child: ElevatedButton(
            onPressed: handleSubmit,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
            ),
            child: const Text(
              'Submit',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ],
    );
  }


Widget buildVerbDropdown(Map<String, dynamic> instruction) {
  // State variables to track if we're using a custom verb
  bool isCustomVerb = instruction['verb'] != null && !verbs.contains(instruction['verb']);
  TextEditingController customVerbController = TextEditingController(
    text: isCustomVerb ? instruction['verb'] : '',
  );

  // Create a focus node to maintain focus
  final FocusNode customVerbFocusNode = FocusNode();

  // Function to save custom option to the database
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

  return StatefulBuilder(
    builder: (context, setState) {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: isCustomVerb
                    ? TextFormField(
                        controller: customVerbController,
                        focusNode: customVerbFocusNode,
                        decoration: const InputDecoration(
                          labelText: 'Enter Custom Verb',
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          // Only update the instruction map without triggering this.setState
                          instruction['verb'] = value;
                        },
                      )
                    : DropdownButtonFormField<String>(
                        value: instruction['verb'],
                        items: verbs
                            .map((verb) => DropdownMenuItem(
                                  value: verb,
                                  child: Text(verb),
                                ))
                            .toList(),
                        onChanged: (value) {
                          instruction['verb'] = value;
                          setState(() {}); // Refresh UI
                        },
                        decoration: const InputDecoration(
                          labelText: 'Select Verb',
                          border: OutlineInputBorder(),
                        ),
                      ),
              ),
              if (isCustomVerb)
                IconButton(
                  icon: const Icon(Icons.save),
                  tooltip: 'Save custom verb',
                  onPressed: () {
                    final customVerb = customVerbController.text.trim();
                    if (customVerb.isNotEmpty) {
                      addCustomOptionToDB('verb', option: customVerb);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Please enter a custom verb first.')),
                      );
                    }
                  },
                ),
              IconButton(
                icon: Icon(isCustomVerb ? Icons.list : Icons.edit),
                tooltip: isCustomVerb ? 'Use predefined verbs' : 'Add custom verb',
                onPressed: () {
                  setState(() {
                    isCustomVerb = !isCustomVerb;
                    if (isCustomVerb) {
                      // Store the current dropdown value if switching to custom
                      customVerbController.text = instruction['verb'] ?? '';
                      // Request focus on the text field after rendering
                      Future.delayed(Duration.zero, () {
                        customVerbFocusNode.requestFocus();
                      });
                    } else {
                      // When switching back to dropdown, preserve custom text
                      // if it doesn't exist in the dropdown, default to first verb
                      if (instruction['verb'] != null &&
                          !verbs.contains(instruction['verb']) &&
                          verbs.isNotEmpty) {
                        instruction['verb'] = verbs.first;
                        setState(() {}); // Refresh UI
                      }
                    }
                  });
                },
              ),
            ],
          ),
        ],
      );
    },
  );
}

Widget buildTamDropdown(Map<String, dynamic> instruction) {
  return DropdownButtonFormField<String>(
    value: instruction['tam'],
    items: tams
        .map((tam) => DropdownMenuItem(
              value: tam,
              child: Text(tam),
            ))
        .toList(),
    onChanged: (value) {
      setState(() {
        instruction['tam'] = value;
      });
    },
    decoration: const InputDecoration(
      labelText: 'Select TAM',
      border: OutlineInputBorder(),
    ),
  );
}
}