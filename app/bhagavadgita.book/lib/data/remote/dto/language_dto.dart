class LanguageDto {
  const LanguageDto({required this.id, required this.name, required this.code});

  final int id;
  final String? name;
  final String? code;

  factory LanguageDto.fromJson(Map<String, Object?> json) {
    return LanguageDto(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String?,
      code: json['code'] as String?,
    );
  }
}

