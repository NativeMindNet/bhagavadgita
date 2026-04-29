import 'package:flutter/foundation.dart';

class ReaderSettings {
  const ReaderSettings({
    required this.showSanskrit,
    required this.showTransliteration,
    required this.showTranslation,
    required this.showComment,
    required this.showVocabulary,
  });

  const ReaderSettings.defaults()
      : showSanskrit = true,
        showTransliteration = true,
        showTranslation = true,
        showComment = true,
        showVocabulary = true;

  final bool showSanskrit;
  final bool showTransliteration;
  final bool showTranslation;
  final bool showComment;
  final bool showVocabulary;

  ReaderSettings copyWith({
    bool? showSanskrit,
    bool? showTransliteration,
    bool? showTranslation,
    bool? showComment,
    bool? showVocabulary,
  }) {
    return ReaderSettings(
      showSanskrit: showSanskrit ?? this.showSanskrit,
      showTransliteration: showTransliteration ?? this.showTransliteration,
      showTranslation: showTranslation ?? this.showTranslation,
      showComment: showComment ?? this.showComment,
      showVocabulary: showVocabulary ?? this.showVocabulary,
    );
  }
}

class ReaderSettingsController extends ValueNotifier<ReaderSettings> {
  ReaderSettingsController() : super(const ReaderSettings.defaults());

  void update(ReaderSettings next) => value = next;
}

final ReaderSettingsController readerSettingsController = ReaderSettingsController();

