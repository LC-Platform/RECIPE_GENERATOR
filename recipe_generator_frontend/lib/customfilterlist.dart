import 'package:flutter/material.dart';

class CustomNounFilterChipList extends StatefulWidget {
  final List<String> nouns;
  final List<String> selectedNouns;
  final Function(String, bool) onSelectionChanged;
  final Function(String) onEditPressed;

  const CustomNounFilterChipList({
    Key? key,
    required this.nouns,
    required this.selectedNouns,
    required this.onSelectionChanged,
    required this.onEditPressed,
  }) : super(key: key);

  @override
  _CustomNounFilterChipListState createState() => _CustomNounFilterChipListState();
}

class _CustomNounFilterChipListState extends State<CustomNounFilterChipList> {
  String _searchQuery = '';

  @override
  Widget build(BuildContext context) {
    List<String> filteredNouns = widget.nouns
        .where((noun) => noun.toLowerCase().contains(_searchQuery.toLowerCase()))
        .toList();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Select Noun(s):',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        TextField(
          decoration: const InputDecoration(
            labelText: 'Search Nouns',
            prefixIcon: Icon(Icons.search),
            border: OutlineInputBorder(),
          ),
          onChanged: (value) => setState(() => _searchQuery = value),
        ),
        const SizedBox(height: 10),
        Wrap(
          spacing: 8.0,
          runSpacing: 8.0,
          children: filteredNouns.map((noun) {
            bool isSelected = widget.selectedNouns.contains(noun);
            return FilterChip(
              label: Text(noun),
              selected: isSelected,
              onSelected: (selected) => widget.onSelectionChanged(noun, selected),
              avatar: isSelected ? const Icon(Icons.check, color: Colors.white) : null,
              selectedColor: Colors.blueAccent,
              backgroundColor: Colors.grey[300],
              labelStyle: TextStyle(
                color: isSelected ? Colors.white : Colors.black,
              ),
            );
          }).toList(),
        ),
        const SizedBox(height: 10),
        if (widget.selectedNouns.isNotEmpty) ...[
          const Text(
            'Selected Nouns:',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          Wrap(
            spacing: 8.0,
            children: widget.selectedNouns.map((noun) {
              return Chip(
                label: Text(noun),
                deleteIcon: const Icon(Icons.edit),
                onDeleted: () => widget.onEditPressed(noun),
                backgroundColor: Colors.blue[100],
              );
            }).toList(),
          ),
        ],
      ],
    );
  }
}
