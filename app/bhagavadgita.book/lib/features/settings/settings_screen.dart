import 'package:flutter/material.dart';

import 'reader_settings.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Reader settings')),
      body: ValueListenableBuilder<ReaderSettings>(
        valueListenable: readerSettingsController,
        builder: (context, settings, _) {
          return ListView(
            children: [
              SwitchListTile(
                title: const Text('Show Sanskrit'),
                value: settings.showSanskrit,
                onChanged: (v) => readerSettingsController.update(settings.copyWith(showSanskrit: v)),
              ),
              SwitchListTile(
                title: const Text('Show transliteration'),
                value: settings.showTransliteration,
                onChanged: (v) => readerSettingsController.update(settings.copyWith(showTransliteration: v)),
              ),
              SwitchListTile(
                title: const Text('Show translation'),
                value: settings.showTranslation,
                onChanged: (v) => readerSettingsController.update(settings.copyWith(showTranslation: v)),
              ),
              SwitchListTile(
                title: const Text('Show comment'),
                value: settings.showComment,
                onChanged: (v) => readerSettingsController.update(settings.copyWith(showComment: v)),
              ),
              SwitchListTile(
                title: const Text('Show vocabulary'),
                value: settings.showVocabulary,
                onChanged: (v) => readerSettingsController.update(settings.copyWith(showVocabulary: v)),
              ),
            ],
          );
        },
      ),
    );
  }
}

