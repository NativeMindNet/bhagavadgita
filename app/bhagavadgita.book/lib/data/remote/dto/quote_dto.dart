class QuoteDto {
  const QuoteDto({required this.author, required this.text});

  final String? author;
  final String? text;

  factory QuoteDto.fromJson(Map<String, Object?> json) {
    return QuoteDto(
      author: json['author'] as String?,
      text: json['text'] as String?,
    );
  }
}

