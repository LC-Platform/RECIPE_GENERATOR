class Instruction {
  String? verb;
  String? tam;
  String? noun;
  String? relation;
  String? ingredient;
  String? ingredientRelation;
  bool showFullFields;

  Instruction({
    this.verb,
    this.tam,
    this.noun,
    this.relation,
    this.ingredient,
    this.ingredientRelation,
    this.showFullFields = true,
  });

  Map<String, dynamic> toMap() {
    return {
      'verb': verb,
      'tam': tam,
      'noun': noun,
      'relation': relation,
      'ingredient': ingredient,
      'ingredientRelation': ingredientRelation,
      'showFullFields': showFullFields,
    };
  }
}