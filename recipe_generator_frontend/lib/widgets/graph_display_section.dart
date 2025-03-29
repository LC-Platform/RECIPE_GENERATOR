import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../SentencesDisplay.dart';
import 'package:flutter/services.dart';
import '../download.dart';

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

class _GraphDisplaySectionState extends State<GraphDisplaySection> with TickerProviderStateMixin {
  TabController? _tabController;
  bool isLoading = false;
  bool showingSentences = false;
  String? currentGraphImage;
  String? currentHindiSentence;
  String? currentUsr;

  final List<String> addedSentences = [];
  final List<String> addedUsrs = [];

  @override
  void initState() {
    super.initState();
    _initializeState();
  }

  void _initializeState() {
    currentGraphImage = widget.graphImageBase64;
    currentHindiSentence = widget.hindiSentence;
    currentUsr = widget.usr;
    _initializeTabController();
  }

  @override
  void didUpdateWidget(covariant GraphDisplaySection oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.graphImageBase64 != oldWidget.graphImageBase64 ||
        widget.hindiSentence != oldWidget.hindiSentence ||
        widget.usr != oldWidget.usr ||
        widget.showGraph != oldWidget.showGraph) {
      _updateTabController();
    }
  }

  void _initializeTabController() {
    List<bool> availableTabs = _getActiveTabFlags();
    int activeTabCount = availableTabs.where((tab) => tab).length;
    
    _tabController?.dispose();
    _tabController = TabController(
      length: activeTabCount,
      vsync: this,
    );
  }

  void _updateTabController() {
    List<bool> availableTabs = _getActiveTabFlags();
    int activeTabCount = availableTabs.where((tab) => tab).length;
    
    if (_tabController?.length != activeTabCount) {
      _tabController?.dispose();
      _tabController = TabController(
        length: activeTabCount,
        vsync: this,
      );
    }

    setState(() {
      currentGraphImage = widget.graphImageBase64;
      currentHindiSentence = widget.hindiSentence;
      currentUsr = widget.usr;
    });
  }

  List<bool> _getActiveTabFlags() {
    return [
      widget.showGraph || (currentGraphImage != null || currentHindiSentence != null),
      currentUsr != null,
      true, // Sentences tab is always available
    ];
  }

  @override
  void dispose() {
    _tabController?.dispose();
    super.dispose();
  }

  // Rest of the existing code remains the same

  /// Build a view containing the graph (if available) and the Hindi sentence.
  Widget _buildGraphAndSentenceView() {
    return ConstrainedBox(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.8,
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
                )
              else
                const Text(
                  'Graph will be displayed here once available.',
                  textAlign: TextAlign.center,
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

  /// Build the USR view.
  Widget _buildUsrView() {
    return ConstrainedBox(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.8,
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
        // Add the sentence and associated USR to the lists.
        setState(() {
          addedSentences.add(currentHindiSentence!);
          if (currentUsr != null && currentUsr!.isNotEmpty) {
            addedUsrs.add(currentUsr!);
          }
          // Clear current values.
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

  /// Modified _removeSentences to clear the lists.
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
                      // Clear the stored lists.
                      addedSentences.clear();
                      addedUsrs.clear();
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
        shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
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

  Future<void> fetchAndDownloadUSRs() async {
  final prefs = await SharedPreferences.getInstance();
  final String? recipeId = prefs.getString('recipe_id');

  if (recipeId == null) {
    print("No recipe_id found in SharedPreferences");
    return;
  }

  final response = await http.get(Uri.parse('http://127.0.0.1:2000/usrs?recipe_id=$recipeId'));

  if (response.statusCode == 200) {
    final List<String> usrs = List<String>.from(json.decode(response.body));
    final content = usrs.join('\n');
    downloadTextFile(content, 'added_usrs.txt');
  } else {
    print("Failed to fetch USRs: ${response.statusCode}");
  }
}
Future<void> fetchAndDownloadSentences() async {
  final prefs = await SharedPreferences.getInstance();
  final String? recipeId = prefs.getString('recipe_id');

  if (recipeId == null) {
    print("No recipe_id found in SharedPreferences");
    return;
  }

  final response = await http.get(Uri.parse('http://127.0.0.1:2000/se?recipe_id=$recipeId'));

  if (response.statusCode == 200) {
    final List<String> usrs = List<String>.from(json.decode(response.body));
    final content = usrs.join('\n');
    downloadTextFile(content, 'added_usrs.txt');
  } else {
    print("Failed to fetch USRs: ${response.statusCode}");
  }
}

  void _showGraphPopup(BuildContext context) {
    if (currentGraphImage == null) return;

    showDialog(
      context: context,
      builder: (context) => Dialog(
        shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
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
                    base64Decode(_getBase64String(currentGraphImage!)),
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

  String _getBase64String(String image) {
    return image.contains(',') ? image.split(',').last : image;
  }

  @override
  Widget build(BuildContext context) {
    final tabs = _getAvailableTabs();
    final views = _getTabViews();

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
              isScrollable: true,
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
                SizedBox.expand(
                  child: TabBarView(
                    controller: _tabController,
                    children: views,
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
            ),
          ),
        ],
      ),
    );
  }
   List<Widget> _getAvailableTabs() {
    List<Widget> tabs = [];

    // Only add the Graph/Sentence tab if we have data (or the flag is set)
    if (widget.showGraph ||
        (currentGraphImage != null || currentHindiSentence != null)) {
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

    // Always add the Sentences tab.
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

  /// Wrap the SentencesDisplaySection with a download section.
  List<Widget> _getTabViews() {
    List<Widget> views = [];

    if (widget.showGraph ||
        (currentGraphImage != null || currentHindiSentence != null)) {
      views.add(_buildGraphAndSentenceView());
    }

    if (currentUsr != null) {
      views.add(_buildUsrView());
    }

    // Wrap the Sentences tab in a Column that shows the SentencesDisplaySection
    // plus a row with two download buttons.
    views.add(Column(
      children: [
        Expanded(
          child: SentencesDisplaySection(
            onSentencesUpdated: () => setState(() {}),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              ElevatedButton.icon(
                onPressed: () {
                  // Aggregate the added sentences into one string.
                 
                },
                icon: const Icon(Icons.download),
                label: const Text('Download Sentences'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
              ElevatedButton.icon(
                onPressed: fetchAndDownloadUSRs,
                icon: const Icon(Icons.download),
                label: const Text('Download USRs'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.purple,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
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
                Text('Failed to copy: $e'),
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
      shape:
          RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
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
                padding:
                    const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
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

  @override
  Widget build(BuildContext context) {
    // Decode the Base64 string robustly:
    final String base64Str =
        graphImage.contains(',') ? graphImage.split(',').last : graphImage;
    final imageBytes = base64Decode(base64Str);

    return Card(
      elevation: 4,
      shape:
          RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              child: Image.memory(
                imageBytes,
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
                Text('Failed to copy: $e'),
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
      shape:
          RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
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
                    padding: const EdgeInsets.symmetric(
                        horizontal: 24, vertical: 12),
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
                    padding: const EdgeInsets.symmetric(
                        horizontal: 24, vertical: 12),
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
