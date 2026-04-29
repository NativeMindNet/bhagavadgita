import 'package:drift/drift.dart' hide Column;
import 'package:flutter/material.dart';

import '../../data/local/app_database.dart';
import '../../data/local/user_data_repository.dart';
import '../settings/reader_settings.dart';

class SlokaScreen extends StatefulWidget {
  const SlokaScreen({super.key, required this.db, required this.slokaId});

  final AppDatabase db;
  final int slokaId;

  @override
  State<SlokaScreen> createState() => _SlokaScreenState();
}

class _SlokaScreenState extends State<SlokaScreen> {
  late final UserDataRepository _userData;
  late final TextEditingController _noteController;

  @override
  void initState() {
    super.initState();
    _userData = UserDataRepository(widget.db);
    _noteController = TextEditingController();
  }

  @override
  void dispose() {
    _noteController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final slokaQuery =
        (widget.db.select(widget.db.slokas)..where((t) => t.id.equals(widget.slokaId)))..limit(1);
    final vocabQuery = (widget.db.select(widget.db.vocabularies)..where((t) => t.slokaId.equals(widget.slokaId)))
      ..orderBy([(t) => OrderingTerm.asc(t.position)]);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Sloka'),
        actions: [
          StreamBuilder<bool>(
            stream: _userData.watchBookmark(widget.slokaId),
            builder: (context, snap) {
              final isBookmarked = snap.data ?? false;
              return IconButton(
                tooltip: isBookmarked ? 'Remove bookmark' : 'Add bookmark',
                icon: Icon(isBookmarked ? Icons.bookmark : Icons.bookmark_border),
                onPressed: () => _userData.setBookmark(widget.slokaId, !isBookmarked),
              );
            },
          ),
        ],
      ),
      body: StreamBuilder<Sloka?>(
        stream: slokaQuery.watchSingleOrNull(),
        builder: (context, snap) {
          final sloka = snap.data;
          if (snap.connectionState == ConnectionState.waiting && sloka == null) {
            return const Center(child: CircularProgressIndicator());
          }
          if (sloka == null) {
            return const Center(child: Text('Sloka not found.'));
          }

          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Text(sloka.name, style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 12),
              ValueListenableBuilder<ReaderSettings>(
                valueListenable: readerSettingsController,
                builder: (context, settings, _) {
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (settings.showSanskrit && (sloka.slokaText ?? '').isNotEmpty) ...[
                        Text(sloka.slokaText!, style: Theme.of(context).textTheme.bodyLarge),
                        const SizedBox(height: 12),
                      ],
                      if (settings.showTransliteration && (sloka.transcription ?? '').isNotEmpty) ...[
                        Text(sloka.transcription!, style: Theme.of(context).textTheme.bodyMedium),
                        const SizedBox(height: 12),
                      ],
                      if (settings.showTranslation && (sloka.translation ?? '').isNotEmpty) ...[
                        Text(sloka.translation!, style: Theme.of(context).textTheme.titleMedium),
                        const SizedBox(height: 12),
                      ],
                      if (settings.showComment && (sloka.comment ?? '').isNotEmpty) ...[
                        Text(sloka.comment!, style: Theme.of(context).textTheme.bodyMedium),
                        const SizedBox(height: 16),
                      ],
                      if (settings.showVocabulary) ...[
                        Text('Vocabulary', style: Theme.of(context).textTheme.titleMedium),
                        const SizedBox(height: 8),
                        StreamBuilder<List<Vocabulary>>(
                          stream: vocabQuery.watch(),
                          builder: (context, vocabSnap) {
                            final items = vocabSnap.data ?? const [];
                            if (items.isEmpty) return const Text('No vocabulary yet.');
                            return Column(
                              children: [
                                for (final v in items)
                                  ListTile(
                                    dense: true,
                                    contentPadding: EdgeInsets.zero,
                                    title: Text(v.tokenText),
                                    subtitle: Text(v.translation),
                                  ),
                              ],
                            );
                          },
                        ),
                      ],
                    ],
                  );
                },
              ),
              const SizedBox(height: 20),
              Text('Note', style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 8),
              StreamBuilder<String?>(
                stream: _userData.watchNote(widget.slokaId),
                builder: (context, noteSnap) {
                  final note = noteSnap.data ?? '';
                  if (_noteController.text != note) {
                    _noteController.text = note;
                    _noteController.selection = TextSelection.collapsed(offset: _noteController.text.length);
                  }

                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      TextField(
                        controller: _noteController,
                        maxLines: null,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'Write your note…',
                        ),
                      ),
                      const SizedBox(height: 10),
                      FilledButton(
                        onPressed: () => _userData.saveNote(widget.slokaId, _noteController.text),
                        child: const Text('Save note'),
                      ),
                    ],
                  );
                },
              ),
            ],
          );
        },
      ),
    );
  }
}

