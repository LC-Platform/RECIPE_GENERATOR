import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import './SentencesDisplay.dart';

class GraphDisplaySection extends StatefulWidget {
  final bool showGraph;
  final String? graphImageBase64;
  final String? hindiSentence;
  final String? usr; 
  final VoidCallback onSentenceStateChanged; // Add this callback

  const GraphDisplaySection({
    Key? key,
    required this.showGraph,
    required this.graphImageBase64,
    required this.hindiSentence,
    required this.usr,
    
    required this.onSentenceStateChanged, // Add this parameter
  }) : super(key: key);

  @override
  State<GraphDisplaySection> createState() => _GraphDisplaySectionState();
}

class _GraphDisplaySectionState extends State<GraphDisplaySection> {
  bool showingSentences = false;
  bool showingUsr = false;
  String? currentGraphImage;
  String? currentHindiSentence;
   String? currentUsr;
   
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    currentGraphImage = widget.graphImageBase64;
    currentHindiSentence = widget.hindiSentence;
    currentUsr = widget.usr;
  }

   @override
  void didUpdateWidget(GraphDisplaySection oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.graphImageBase64 != widget.graphImageBase64) {
      currentGraphImage = widget.graphImageBase64;
    }
    if (oldWidget.hindiSentence != widget.hindiSentence) {
      currentHindiSentence = widget.hindiSentence;
    }
    if (oldWidget.usr != widget.usr) {
      currentUsr = widget.usr;
    }
  }

  Future<void> _addSentence(BuildContext context) async {
    setState(() => isLoading = true);
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');

      if (recipeId == null || widget.hindiSentence == null) {
        throw Exception('Recipe ID or Hindi sentence not found');
      }

      final response = await http.post(
        Uri.parse('http://127.0.0.1:2000/add-sentence'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'recipe_id': recipeId,
          'sentence': widget.hindiSentence
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          showingSentences = true;
          // Clear the current graph and sentence after successful addition
          currentGraphImage = null;
          currentHindiSentence = null;
        });
        widget.onSentenceStateChanged(); // Notify parent about the change
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Row(
                children: [
                  Icon(Icons.check_circle, color: Colors.white),
                  SizedBox(width: 8),
                  Text('Sentence added successfully'),
                ],
              ),
              backgroundColor: Colors.green,
            ),
          );
        }
      } else {
        throw Exception('Failed to add sentence');
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: 8),
                Text('Error: $e'),
              ],
            ),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() => isLoading = false);
    }
  }

  Future<void> _removeSentences(BuildContext context) async {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Confirm Deletion'),
          content: const Text('Are you sure you want to remove  sentence?'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () async {
                Navigator.of(context).pop();
                setState(() => isLoading = true);
                try {
                  final prefs = await SharedPreferences.getInstance();
                  final String? recipeId = prefs.getString('recipe_id');

                  if (recipeId == null) {
                    throw Exception('Recipe ID not found');
                  }

                  final response = await http.post(
                    Uri.parse('http://127.0.0.1:2000/remove-sentences'),
                    headers: {'Content-Type': 'application/json'},
                    body: json.encode({'recipe_id': recipeId}),
                  );

                  if (response.statusCode == 200) {
                    setState(() {
                      showingSentences = false;
                      currentGraphImage = null;
                      currentHindiSentence = null;
                    });
                    widget.onSentenceStateChanged(); // Notify parent about the change
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Row(
                            children: [
                              Icon(Icons.check_circle, color: Colors.white),
                              SizedBox(width: 8),
                              Text('Sentences removed successfully'),
                            ],
                          ),
                          backgroundColor: Colors.green,
                        ),
                      );
                    }
                  } else {
                    throw Exception('Failed to remove sentences');
                  }
                } catch (e) {
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Row(
                          children: [
                            const Icon(Icons.error, color: Colors.white),
                            const SizedBox(width: 8),
                            Text('Error: $e'),
                          ],
                        ),
                        backgroundColor: Colors.red,
                      ),
                    );
                  }
                } finally {
                  setState(() => isLoading = false);
                }
              },
              child: const Text('Remove', style: TextStyle(color: Colors.red)),
            ),
          ],
        );
      },
    );
  }
    void _showUsrPopup(BuildContext context) {
    if (currentUsr == null) return;

    showDialog(
      context: context,
      builder: (context) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
        child: Container(
          padding: const EdgeInsets.all(24.0),
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.9,
            maxHeight: MediaQuery.of(context).size.height * 0.9,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'USR Details',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const Divider(),
              Expanded(
                child: SingleChildScrollView(
                  child: SelectableText(
                    currentUsr!,
                    style: const TextStyle(fontSize: 16, height: 1.5),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
  // ... rest of the code remains the same ...

  void _showGraphPopup(BuildContext context) {
    if (currentGraphImage == null) return;

    showDialog(
      context: context,
      builder: (context) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
        child: Container(
          padding: const EdgeInsets.all(24.0),
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.9,
            maxHeight: MediaQuery.of(context).size.height * 0.9,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Graph Visualization',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const Divider(),
              Expanded(
                child: InteractiveViewer(
                  boundaryMargin: const EdgeInsets.all(20.0),
                  minScale: 0.5,
                  maxScale: 4.0,
                  child: Image.memory(
                    base64Decode(currentGraphImage!.split(',').last),
                    fit: BoxFit.contain,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Pinch or use mouse wheel to zoom • Drag to pan',
                style: TextStyle(color: Colors.grey, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }

 
  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          padding: const EdgeInsets.all(24.0),
          margin: const EdgeInsets.all(16.0),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16.0),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.1),
                spreadRadius: 2,
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _CustomTab(
                      icon: Icons.auto_graph,
                      label: 'Graph',
                      isSelected: !showingSentences && !showingUsr,
                      onTap: () => setState(() {
                        showingSentences = false;
                        showingUsr = false;
                      }),
                    ),
                    const SizedBox(width: 16),
                    _CustomTab(
                      icon: Icons.schema,
                      label: 'USR',
                      isSelected: showingUsr,
                      onTap: () => setState(() {
                        showingSentences = false;
                        showingUsr = true;
                      }),
                    ),
                    const SizedBox(width: 16),
                    _CustomTab(
                      icon: Icons.format_list_bulleted,
                      label: 'Sentences',
                      isSelected: showingSentences,
                      onTap: () => setState(() {
                        showingSentences = true;
                        showingUsr = false;
                      }),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              Expanded(
                child: _buildContent(),
              ),
            ],
          ),
        ),
        if (isLoading)
          Container(
            color: Colors.black.withOpacity(0.3),
            child: const Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildContent() {
    if (showingSentences) {
      return SentencesDisplaySection(
        onSentencesUpdated: () => setState(() {}),
      );
    } else if (showingUsr) {
      return SingleChildScrollView(
        child: Column(
          children: [
            if (currentUsr != null)
              _UsrCard(
                usr: currentUsr!,
                onView: () => _showUsrPopup(context),
              ),
          ],
        ),
      );
    } else {
      return SingleChildScrollView(
        child: Column(
          children: [
            if (currentGraphImage != null) ...[
              _GraphPreview(
                graphImage: currentGraphImage!,
                onTap: () => _showGraphPopup(context),
              ),
              const SizedBox(height: 24),
            ],
            if (currentHindiSentence != null) ...[
              _HindiSentenceCard(
                sentence: currentHindiSentence!,
                onAdd: () => _addSentence(context),
                onRemove: () => _removeSentences(context),
              ),
            ],
          ],
        ),
      );
    }
  }
}

// Add new USR Card widget
class _UsrCard extends StatelessWidget {
  final String usr;
  final VoidCallback onView;

  const _UsrCard({
    required this.usr,
    required this.onView,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Row(
              children: [
                const Icon(Icons.schema, color: Colors.purple),
                const SizedBox(width: 8),
                const Text(
                  'Universal Semantic Representation',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.purple,
                  ),
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.content_copy),
                  onPressed: () {
                    // Add copy functionality
                  },
                  tooltip: 'Copy to clipboard',
                ),
              ],
            ),
            const Divider(),
            const SizedBox(height: 16),
            Container(
              constraints: const BoxConstraints(maxHeight: 200),
              child: SingleChildScrollView(
                child: SelectableText(
                  usr,
                  style: const TextStyle(
                    fontSize: 16,
                    height: 1.5,
                    color: Colors.black87,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: onView,
              icon: const Icon(Icons.visibility),
              label: const Text('View Details'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.purple,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
class _CustomTab extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _CustomTab({
    required this.icon,
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? Colors.blue.shade100 : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            children: [
              Icon(
                icon,
                size: 20,
                color: isSelected ? Colors.blue.shade700 : Colors.grey,
              ),
              const SizedBox(width: 8),
              Text(
                label,
                style: TextStyle(
                  color: isSelected ? Colors.blue.shade700 : Colors.grey,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _GraphPreview extends StatelessWidget {
  final String graphImage;
  final VoidCallback onTap;

  const _GraphPreview({
    required this.graphImage,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              child: Image.memory(
                base64Decode(graphImage.split(',').last),
                fit: BoxFit.contain,
              ),
            ),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.grey.shade50,
                borderRadius: const BorderRadius.vertical(
                  bottom: Radius.circular(16),
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.zoom_in, size: 20, color: Colors.blue.shade700),
                  const SizedBox(width: 8),
                  Text(
                    'Click to zoom',
                    style: TextStyle(
                      color: Colors.blue.shade700,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HindiSentenceCard extends StatelessWidget {
  final String sentence;
  final VoidCallback onAdd;
  final VoidCallback onRemove;

  const _HindiSentenceCard({
    required this.sentence,
    required this.onAdd,
    required this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Row(
              children: [
                const Icon(Icons.translate, color: Colors.blue),
                const SizedBox(width: 8),
                const Text(
                  'Generated Hindi Sentence',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue,
                  ),
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.content_copy),
                  onPressed: () {
                    // Add copy functionality
                  },
                  tooltip: 'Copy to clipboard',
                ),
              ],
            ),
            const Divider(),
            const SizedBox(height: 16),
            SelectableText(
              sentence,
              style: const TextStyle(
                fontSize: 18,
                height: 1.5,
                fontWeight: FontWeight.w500,
                color: Colors.black87,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton.icon(
                  onPressed: onAdd,
                  icon: const Icon(Icons.add_circle_outline),
                  label: const Text('Add to List'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                OutlinedButton.icon(
                  onPressed: onRemove,
                  icon: const Icon(Icons.delete_outline),
                  label: const Text('Remove'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.red,
                    side: const BorderSide(color: Colors.red),
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}