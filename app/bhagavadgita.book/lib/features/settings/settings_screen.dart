import 'package:flutter/material.dart';

import '../../app/theme/gita_colors.dart';
import 'reader_settings.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ValueListenableBuilder<ReaderSettings>(
        valueListenable: readerSettingsController,
        builder: (context, settings, _) {
          final headerStyle = Theme.of(context).textTheme.labelSmall?.copyWith(
            letterSpacing: 1.2,
            color: GitaColors.gray2,
          );
          return ListView(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 18, 16, 8),
                child: Text('DISPLAY', style: headerStyle),
              ),
              SwitchListTile(
                title: const Text('Show Sanskrit'),
                value: settings.showSanskrit,
                onChanged: (v) => readerSettingsController.update(
                  settings.copyWith(showSanskrit: v),
                ),
              ),
              SwitchListTile(
                title: const Text('Show transliteration'),
                value: settings.showTransliteration,
                onChanged: (v) => readerSettingsController.update(
                  settings.copyWith(showTransliteration: v),
                ),
              ),
              SwitchListTile(
                title: const Text('Show translation'),
                value: settings.showTranslation,
                onChanged: (v) => readerSettingsController.update(
                  settings.copyWith(showTranslation: v),
                ),
              ),
              SwitchListTile(
                title: const Text('Show comment'),
                value: settings.showComment,
                onChanged: (v) => readerSettingsController.update(
                  settings.copyWith(showComment: v),
                ),
              ),
              SwitchListTile(
                title: const Text('Show vocabulary'),
                value: settings.showVocabulary,
                onChanged: (v) => readerSettingsController.update(
                  settings.copyWith(showVocabulary: v),
                ),
              ),
              const SizedBox(height: 20),
            ],
          );
        },
      ),
    );
  }
}

