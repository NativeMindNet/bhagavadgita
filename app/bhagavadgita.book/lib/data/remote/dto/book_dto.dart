class BookDto {
  const BookDto({
    required this.id,
    required this.languageId,
    required this.name,
    required this.initials,
    required this.chaptersCount,
  });

  final int id;
  final int languageId;
  final String? name;
  final String? initials;
  final int? chaptersCount;

  factory BookDto.fromJson(Map<String, Object?> json) {
    return BookDto(
      id: (json['id'] as num).toInt(),
      languageId: (json['languageId'] as num).toInt(),
      name: json['name'] as String?,
      initials: json['initials'] as String?,
      chaptersCount: (json['chaptersCount'] as num?)?.toInt(),
    );
  }
}

