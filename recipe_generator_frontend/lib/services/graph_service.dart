import 'package:graphview/GraphView.dart';
import 'package:flutter/material.dart';

class GraphService {
  static Graph createGraph() {
    return Graph();
  }

  static Widget customCircularRelationNode(String text) {
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
  static Color determineNodeColor(String nodeValue) {
    if (nodeValue.contains('Verb')) {
      return Colors.blueAccent;
    } else if (nodeValue.contains('TAM')) {
      return Colors.greenAccent;
    } else if (nodeValue.contains('Noun')) {
      return Colors.orangeAccent;
    } else if (nodeValue.contains('Relation')) {
      return Colors.purpleAccent;
    }
    return Colors.redAccent;
  }

  static String generateSentenceFromGraph(Graph graph) {
    List<String> sentenceParts = [];
    Node? verbTamNode;
    Node? relationNode;
    Node? nounNode;
    List<Node> ingredientNodes = [];
    bool isFirstIngredient = true;

    for (var node in graph.nodes) {
      if (node.key!.value.toString().contains('Verb+TAM')) {
        continue;
      } else if (node.key!.value.toString().contains('Relation')) {
        relationNode = node;
        sentenceParts.add('के साथ ${node.key!.value.toString().split(": ")[1]}');
      } else if (node.key!.value.toString().contains('Noun')) {
        nounNode = node;
        sentenceParts.add('वह ${node.key!.value.toString().split(": ")[1]}');
      } else if (node.key!.value.toString().contains('Ingredient')) {
        ingredientNodes.add(node);
      }
    }

    for (var ingredientNode in ingredientNodes) {
      if (isFirstIngredient) {
        sentenceParts.add('का उपयोग करके ${ingredientNode.key!.value.toString().split(": ")[1]}');
        isFirstIngredient = false;
      } else {
        sentenceParts.add('और ${ingredientNode.key!.value.toString().split(": ")[1]} का उपयोग');
      }
    }

    return sentenceParts.join(' ');
  }
}


