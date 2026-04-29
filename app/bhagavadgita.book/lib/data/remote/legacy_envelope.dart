class LegacyEnvelope<T> {
  const LegacyEnvelope({required this.code, required this.data, required this.message});

  final int code;
  final T data;
  final String? message;

  static LegacyEnvelope<T> fromJson<T>(
    Map<String, Object?> json, {
    required T Function(Object? dataJson) parseData,
  }) {
    return LegacyEnvelope<T>(
      code: (json['code'] as num?)?.toInt() ?? -1,
      data: parseData(json['data']),
      message: json['message'] as String?,
    );
  }

  bool get isOk => code == 0;
}

