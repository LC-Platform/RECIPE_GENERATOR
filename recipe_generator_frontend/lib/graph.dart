import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import './SentencesDisplay.dart';
import 'package:flutter/services.dart';

class GraphDisplaySection extends StatefulWidget {
  final bool showGraph;
  final String? graphImageBase64;
  final String? hindiSentence;
  final String? usr;
  final VoidCallback onSentenceStateChanged;

  const GraphDisplaySection({
    Key? key,
    required this.showGraph,
    required this.graphImageBase64,
    required this.hindiSentence,
    required this.usr,
    required this.onSentenceStateChanged,
  }) : super(key: key);

  @override
  State<GraphDisplaySection> createState() => _GraphDisplaySectionState();
}

class _GraphDisplaySectionState extends State<GraphDisplaySection> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  bool isLoading = false;
  bool showingSentences = false;
  String? currentGraphImage;
  String? currentHindiSentence;
  String? currentUsr;
  
  @override
  void initState() {
    super.initState();
    _initializeState();
    _initializeTabController();
  }

  @override
  void didUpdateWidget(GraphDisplaySection oldWidget) {
    super.didUpdateWidget(oldWidget);
    
    if (widget.graphImageBase64 != oldWidget.graphImageBase64 ||
        widget.hindiSentence != oldWidget.hindiSentence ||
        widget.usr != oldWidget.usr) {
      _initializeState();
      
      // Dispose old controller before creating a new one
      _tabController.dispose();
      _initializeTabController();
    }
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _initializeState() {
    currentGraphImage = widget.graphImageBase64;
    currentHindiSentence = widget.hindiSentence;
    currentUsr = widget.usr;
  }

  void _initializeTabController() {
    List<bool> availableTabs = [
      currentGraphImage != null || currentHindiSentence != null,
      currentUsr != null,
      true
    ];
    
    int activeTabCount = availableTabs.where((tab) => tab).length;
    _tabController = TabController(
      length: activeTabCount,
      vsync: this,
    );
  }

  Widget _buildGraphAndSentenceView() {
    return ConstrainedBox(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.7,
      ),
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (currentGraphImage != null)
                _GraphPreview(
                  graphImage: currentGraphImage!,
                  onTap: () => _showGraphPopup(context),
                ),
              if (currentGraphImage != null && currentHindiSentence != null)
                const SizedBox(height: 24),
              if (currentHindiSentence != null)
                _HindiSentenceCard(
                  sentence: currentHindiSentence!,
                  onAdd: () => _addSentence(context),
                  onRemove: () => _removeSentences(context),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildUsrView() {
    return ConstrainedBox(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.7,
      ),
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: _UsrCard(
            usr: currentUsr ?? '',
            onView: () => _showUsrPopup(context),
          ),
        ),
      ),
    );
  }

  Future<void> _addSentence(BuildContext context) async {
    if (currentHindiSentence == null) return;
    
    setState(() => isLoading = true);
    
    try {
      final prefs = await SharedPreferences.getInstance();
      final String? recipeId = prefs.getString('recipe_id');

      if (recipeId == null) {
        throw Exception('Recipe ID not found');
      }

      final response = await http.post(
        Uri.parse('http://127.0.0.1:2000/add-sentence'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'recipe_id': recipeId,
          'sentence': currentHindiSentence
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          currentGraphImage = null;
          currentHindiSentence = null;
        });
        widget.onSentenceStateChanged();
        _showSuccessMessage(context, 'Sentence added successfully');
      } else {
        throw Exception('Failed to add sentence');
      }
    } catch (e) {
      _showErrorMessage(context, e.toString());
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
          content: const Text('Are you sure you want to remove sentence?'),
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
                    widget.onSentenceStateChanged();
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
                            Expanded(child: Text('Error: $e')),
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

  void _showSuccessMessage(BuildContext context, String message) {
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.check_circle, color: Colors.white),
            const SizedBox(width: 8),
            Text(message),
          ],
        ),
        backgroundColor: Colors.green,
      ),
    );
  }

  void _showErrorMessage(BuildContext context, String error) {
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.error, color: Colors.white),
            const SizedBox(width: 8),
            Expanded(child: Text('Error: $error')),
          ],
        ),
        backgroundColor: Colors.red,
      ),
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
    final tabs = _getAvailableTabs();
    final views = _getTabViews();
    
    if (tabs.isEmpty || views.isEmpty) {
      return const SizedBox.shrink();
    }
    
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 2,
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.8,
        minHeight: 200,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            decoration: BoxDecoration(
              color: Colors.grey.shade50,
              borderRadius: const BorderRadius.vertical(
                top: Radius.circular(16),
              ),
            ),
            child: TabBar(
              controller: _tabController,
              tabs: tabs,
              labelColor: Colors.blue.shade700,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Colors.blue.shade700,
              indicatorWeight: 3,
              labelStyle: const TextStyle(fontWeight: FontWeight.bold),
              unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.normal),
              padding: const EdgeInsets.symmetric(horizontal: 16),
            ),
          ),
          Expanded(
            child: Stack(
              children: [
                TabBarView(
                  controller: _tabController,
                  children: views,
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
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _getAvailableTabs() {
    List<Widget> tabs = [];
    
    if (currentGraphImage != null || currentHindiSentence != null) {
      tabs.add(const Tab(
        icon: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.auto_graph),
            SizedBox(width: 8),
            Text('Graph'),
          ],
        ),
      ));
    }
    
    if (currentUsr != null) {
      tabs.add(const Tab(
        icon: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.schema),
            SizedBox(width: 8),
            Text('USR'),
          ],
        ),
      ));
    }
    
    tabs.add(const Tab(
      icon: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.format_list_bulleted),
          SizedBox(width: 8),
          Text('Sentences'),
        ],
      ),
    ));
    
    return tabs;
  }

  List<Widget> _getTabViews() {
    List<Widget> views = [];
    
    if (currentGraphImage != null || currentHindiSentence != null) {
      views.add(_buildGraphAndSentenceView());
    }
    
    if (currentUsr != null) {
      views.add(_buildUsrView());
    }
    
    views.add(SentencesDisplaySection(
      onSentencesUpdated: () => setState(() {}),
    ));
    
    return views;
  }
}

class _UsrCard extends StatelessWidget {
  final String usr;
  final VoidCallback onView;

  const _UsrCard({
    required this.usr,
    required this.onView,
  });

  void _copyToClipboard(BuildContext context) async {
    try {
      await Clipboard.setData(ClipboardData(text: usr));
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 8),
                Text('USR copied to clipboard'),
              ],
            ),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 2),
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: 8),
                Expanded(child: Text('Failed to copy: $e')),
              ],
            ),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 2),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                const Icon(Icons.schema, color: Colors.purple),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text(
                    'Universal Semantic Representation',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.purple,
                    ),
                    softWrap: true,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.content_copy),
                  onPressed: () => _copyToClipboard(context),
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

class _GraphPreview extends StatelessWidget {
  final String graphImage;
  final VoidCallback onTap;

  const _GraphPreview({
    required this.graphImage,
    required this.onTap,
  });

  Uint8List _decodeBase64Image(String base64String) {
    try {
      // Handle data URI format if present
      String processedInput = base64String;
      if (base64String.contains(',')) {
        processedInput = base64String.split(',').last;
      }
      return base64Decode(processedInput);
    } catch (e) {
      debugPrint('Error decoding base64 image: $e');
      // Return an empty byte array as fallback
      return Uint8List(0);
    }
  }

  @override
  Widget build(BuildContext context) {
    final imageData = _decodeBase64Image(graphImage);
    if (imageData.isEmpty) {
      return const Center(
        child: Text('Failed to load image'),
      );
    }

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              child: Image.memory(
                imageData,
                fit: BoxFit.contain,
                errorBuilder: (context, error, stackTrace) {
                  return const SizedBox(
                    height: 200,
                    child: Center(
                      child: Icon(Icons.broken_image, size: 48, color: Colors.grey),
                    ),
                  );
                },
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
                mainAxisSize: MainAxisSize.min,
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

  void _copyToClipboard(BuildContext context) async {
    try {
      await Clipboard.setData(ClipboardData(text: sentence));
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 8),
                Text('Hindi sentence copied to clipboard'),
              ],
            ),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 2),
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: 8),
                Expanded(child: Text('Failed to copy: $e')),
              ],
            ),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 2),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                const Icon(Icons.translate, color: Colors.blue),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text(
                    'Generated Hindi Sentence',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue,
                    ),
                    softWrap: true,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.content_copy),
                  onPressed: () => _copyToClipboard(context),
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
            LayoutBuilder(
              builder: (context, constraints) {
                if (constraints.maxWidth <400) {
                  return Column(
                    children: [
                      ElevatedButton.icon(
                        onPressed: onAdd,
                        icon: const Icon(Icons.add_circle_outline),
                        label: const Text('Add to List'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.blue,
                          foregroundColor: Colors.white,
                          minimumSize: const Size.fromHeight(48),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                      ),
                      const SizedBox(height: 8),
                      OutlinedButton.icon(
                        onPressed: onRemove,
                        icon: const Icon(Icons.delete_outline),
                        label: const Text('Remove'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.red,
                          minimumSize: const Size.fromHeight(48),
                          side: const BorderSide(color: Colors.red),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                      ),
                    ],
                  );
                } else {
                  return Row(
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
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}