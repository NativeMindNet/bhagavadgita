import 'vocabulary_dto.dart';

class SlokaDto {
  const SlokaDto({
    required this.id,
    required this.name,
    required this.text,
    required this.transcription,
    required this.translation,
    required this.comment,
    required this.order,
    required this.audio,
    required this.audioSanskrit,
    required this.vocabularies,
  });

  final int id;
  final String? name;
  final String? text;
  final String? transcription;
  final String? translation;
  final String? comment;
  final int? order;
  final String? audio;
  final String? audioSanskrit;
  final List<VocabularyDto> vocabularies;

  factory SlokaDto.fromJson(Map<String, Object?> json) {
    final vocabJson = (json['vocabularies'] as List<Object?>? ?? const []).cast<Map<String, Object?>>();
    return SlokaDto(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String?,
      text: json['text'] as String?,
      transcription: json['transcription'] as String?,
      translation: json['translation'] as String?,
      comment: json['comment'] as String?,
      order: (json['order'] as num?)?.toInt(),
      audio: json['audio'] as String?,
      audioSanskrit: json['audioSanskrit'] as String?,
      vocabularies: vocabJson.map(VocabularyDto.fromJson).toList(growable: false),
    );
  }
}

