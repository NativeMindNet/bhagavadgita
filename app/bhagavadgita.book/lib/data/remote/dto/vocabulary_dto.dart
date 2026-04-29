class VocabularyDto {
  const VocabularyDto({required this.id, required this.text, required this.translation});

  final int id;
  final String? text;
  final String? translation;

  factory VocabularyDto.fromJson(Map<String, Object?> json) {
    return VocabularyDto(
      id: (json['id'] as num).toInt(),
      text: json['text'] as String?,
      translation: json['translation'] as String?,
    );
  }
}

