import 'sloka_dto.dart';

class ChapterDto {
  const ChapterDto({
    required this.id,
    required this.name,
    required this.order,
    required this.slokas,
  });

  final int id;
  final String? name;
  final int? order;
  final List<SlokaDto> slokas;

  factory ChapterDto.fromJson(Map<String, Object?> json) {
    final slokaJson = (json['shlokas'] as List<Object?>? ?? const []).cast<Map<String, Object?>>();
    return ChapterDto(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String?,
      order: (json['order'] as num?)?.toInt(),
      slokas: slokaJson.map(SlokaDto.fromJson).toList(growable: false),
    );
  }
}

