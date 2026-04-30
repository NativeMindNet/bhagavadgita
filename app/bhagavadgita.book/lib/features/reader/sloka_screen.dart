import 'package:drift/drift.dart' hide Column;
import 'package:flutter/material.dart';

import '../../app/audio/audio_controller_scope.dart';
import '../../app/audio/audio_state.dart';
import '../../app/audio/audio_storage.dart';
import '../../app/audio/audio_track.dart';
import '../../data/local/app_database.dart';
import '../../data/local/user_data_repository.dart';
import '../settings/audio_settings_controller.dart';
import '../settings/reader_settings.dart';
import '../shared/widgets/audio_player_bar.dart';
import '../shared/widgets/author_badge.dart';
import '../shared/widgets/section_header.dart';

class SlokaScreen extends StatefulWidget {
  const SlokaScreen({
    super.key,
    required this.db,
    required this.slokaId,
    this.chapterId,
    this.position,
    this.embedded = false,
  });

  final AppDatabase db;
  final int slokaId;
  final int? chapterId;
  final int? position;
  final bool embedded;

  @override
  State<SlokaScreen> createState() => _SlokaScreenState();
}

class _SlokaScreenState extends State<SlokaScreen> {
  late final UserDataRepository _userData;
  late final TextEditingController _noteController;
  int? _boundSlokaId;
  bool _wiredCompletion = false;

  @override
  void initState() {
    super.initState();
    _userData = UserDataRepository(widget.db);
    _noteController = TextEditingController();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_wiredCompletion) return;
    _wiredCompletion = true;
    AudioControllerScope.of(context).onCompleted = _handleAudioCompleted;
  }

  @override
  void dispose() {
    _noteController.dispose();
    super.dispose();
  }

  static const _legacyHost = 'http://app.bhagavadgitaapp.online';

  Uri? _resolveAudioUri(String? raw) {
    final s = (raw ?? '').trim();
    if (s.isEmpty) return null;
    final parsed = Uri.tryParse(s);
    if (parsed == null) return null;
    if (parsed.hasScheme) return parsed;
    return Uri.parse('$_legacyHost$s');
  }

  void _bindAudioIfNeeded(Sloka sloka) {
    if (_boundSlokaId == sloka.id) return;
    _boundSlokaId = sloka.id;

    final audio = AudioControllerScope.of(context);
    final sanskritUri = _resolveAudioUri(sloka.audioSanskrit);
    final translationUri = _resolveAudioUri(sloka.audio);

    () async {
      final audioSettings = audioSettingsController.value;
      final chapterId = widget.chapterId;

      final sanskrit = await _resolveBestSource(
        isEnabled: audioSettings.useSanskritAudio,
        trackLabel: 'Sanskrit',
        chapterId: chapterId,
        slokaNetworkUri: sanskritUri,
        chapter1AssetPath: 'assets/audio/sanskrit/chapter_1_sanskrit.mp3',
        track: AudioTrack.sanskrit,
      );
      final translation = await _resolveBestSource(
        isEnabled: audioSettings.useTranslationAudio,
        trackLabel: 'Translation',
        chapterId: chapterId,
        slokaNetworkUri: translationUri,
        chapter1AssetPath: 'assets/audio/ru/chapter_1_ru.mp3',
        track: AudioTrack.translation,
      );

      if (!mounted) return;
      await audio.setSources(sanskrit: sanskrit, translation: translation);
    }();
  }

  Future<AudioSourceRef> _resolveBestSource({
    required bool isEnabled,
    required String trackLabel,
    required int? chapterId,
    required Uri? slokaNetworkUri,
    required String chapter1AssetPath,
    required AudioTrack track,
  }) async {
    if (!isEnabled) return const AudioSourceRef.none();

    if (chapterId != null) {
      final local = await audioStorage.chapterLocalUriIfExists(track, chapterId);
      if (local != null) return AudioSourceRef.file(local, label: trackLabel);
    }

    if (slokaNetworkUri != null) {
      return AudioSourceRef.network(slokaNetworkUri, label: trackLabel);
    }

    if (chapterId == 1) {
      return AudioSourceRef.asset(chapter1AssetPath, label: trackLabel);
    }

    return const AudioSourceRef.none();
  }

  Future<void> _handleAudioCompleted() async {
    if (!audioSettingsController.value.autoPlayNext) return;
    final chapterId = widget.chapterId;
    final position = widget.position;
    if (chapterId == null || position == null) return;

    AudioControllerScope.of(context).requestPlayOnNextSourceBind();

    final next = await (widget.db.select(widget.db.slokas)
          ..where(
            (t) =>
                t.chapterId.equals(chapterId) &
                t.position.isBiggerThanValue(position),
          )
          ..orderBy([(t) => OrderingTerm.asc(t.position)])
          ..limit(1))
        .getSingleOrNull();

    if (!mounted || next == null) return;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => SlokaScreen(
          db: widget.db,
          slokaId: next.id,
          chapterId: chapterId,
          position: next.position,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final slokaQuery = (widget.db.select(
      widget.db.slokas,
    )..where((t) => t.id.equals(widget.slokaId)))..limit(1);
    final vocabQuery =
        (widget.db.select(widget.db.vocabularies)
            ..where((t) => t.slokaId.equals(widget.slokaId)))
          ..orderBy([(t) => OrderingTerm.asc(t.position)]);

    final body = StreamBuilder<Sloka?>(
      stream: slokaQuery.watchSingleOrNull(),
      builder: (context, snap) {
          final sloka = snap.data;
          if (snap.connectionState == ConnectionState.waiting &&
              sloka == null) {
            return const Center(child: CircularProgressIndicator());
          }
          if (sloka == null) {
            return const Center(child: Text('Sloka not found.'));
          }

          _bindAudioIfNeeded(sloka);

          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              if (widget.chapterId != null && widget.position != null) ...[
                _SlokaNavigator(
                  db: widget.db,
                  chapterId: widget.chapterId!,
                  position: widget.position!,
                ),
                const SizedBox(height: 12),
              ],
              Center(
                child: Text(
                  sloka.position.toString(),
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                sloka.name,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 12),
              ValueListenableBuilder<ReaderSettings>(
                valueListenable: readerSettingsController,
                builder: (context, settings, _) {
                  final theme = Theme.of(context);
                  final divider = Padding(
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    child: Divider(color: theme.dividerColor, height: 1),
                  );
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      if (settings.showSanskrit &&
                          (sloka.slokaText ?? '').isNotEmpty) ...[
                        const SectionHeader('Sanskrit'),
                        Text(
                          sloka.slokaText!,
                          textAlign: TextAlign.center,
                          style: theme.textTheme.bodyLarge?.copyWith(
                            height: 1.55,
                          ),
                        ),
                        divider,
                      ],
                      if (settings.showTransliteration &&
                          (sloka.transcription ?? '').isNotEmpty) ...[
                        const SectionHeader('Transcription'),
                        Text(
                          sloka.transcription!,
                          style: theme.textTheme.bodyMedium?.copyWith(
                            fontStyle: FontStyle.italic,
                          ),
                        ),
                        divider,
                      ],
                      if (settings.showTranslation &&
                          (sloka.translation ?? '').isNotEmpty) ...[
                        const SectionHeader('Translation'),
                        Text(sloka.translation!, style: theme.textTheme.bodyLarge),
                        divider,
                      ],
                      if (settings.showComment &&
                          (sloka.comment ?? '').isNotEmpty) ...[
                        const SectionHeader('Commentary'),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const AuthorBadge(initials: 'BG'),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                sloka.comment!,
                                style: theme.textTheme.bodyMedium,
                              ),
                            ),
                          ],
                        ),
                        divider,
                      ],
                      if (settings.showVocabulary) ...[
                        const SectionHeader('Vocabulary'),
                        StreamBuilder<List<Vocabulary>>(
                          stream: vocabQuery.watch(),
                          builder: (context, vocabSnap) {
                            final items = vocabSnap.data ?? const [];
                            if (items.isEmpty) {
                              return Text(
                                'No vocabulary yet.',
                                style: theme.textTheme.bodySmall,
                              );
                            }
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
              const SectionHeader('Note'),
              const SizedBox(height: 8),
              StreamBuilder<String?>(
                stream: _userData.watchNote(widget.slokaId),
                builder: (context, noteSnap) {
                  final note = noteSnap.data ?? '';
                  if (_noteController.text != note) {
                    _noteController.text = note;
                    _noteController.selection = TextSelection.collapsed(
                      offset: _noteController.text.length,
                    );
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
                        onPressed: () => _userData.saveNote(
                          widget.slokaId,
                          _noteController.text,
                        ),
                        child: const Text('Save note'),
                      ),
                    ],
                  );
                },
              ),
            ],
          );
      },
    );

    if (widget.embedded) return body;

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
                icon: Icon(
                  isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                ),
                onPressed: () =>
                    _userData.setBookmark(widget.slokaId, !isBookmarked),
              );
            },
          ),
        ],
      ),
      bottomNavigationBar: AnimatedBuilder(
        animation: audioSettingsController,
        builder: (context, _) {
          final audioSettings = audioSettingsController.value;
          return AudioPlayerBarWithController(
            controller: AudioControllerScope.of(context),
            autoPlay: audioSettings.autoPlayNext,
            onToggleAutoPlay: (v) => audioSettingsController.update(
              audioSettings.copyWith(autoPlayNext: v),
            ),
          );
        },
      ),
      body: body,
    );
  }
}

class _SlokaNavigator extends StatelessWidget {
  const _SlokaNavigator({
    required this.db,
    required this.chapterId,
    required this.position,
  });

  final AppDatabase db;
  final int chapterId;
  final int position;

  @override
  Widget build(BuildContext context) {
    final previousQuery =
        (db.select(db.slokas)
              ..where(
                (t) =>
                    t.chapterId.equals(chapterId) &
                    t.position.isSmallerThanValue(position),
              )
              ..orderBy([(t) => OrderingTerm.desc(t.position)])
              ..limit(1))
            .watchSingleOrNull();
    final nextQuery =
        (db.select(db.slokas)
              ..where(
                (t) =>
                    t.chapterId.equals(chapterId) &
                    t.position.isBiggerThanValue(position),
              )
              ..orderBy([(t) => OrderingTerm.asc(t.position)])
              ..limit(1))
            .watchSingleOrNull();

    return StreamBuilder<Sloka?>(
      stream: previousQuery,
      builder: (context, prevSnap) {
        return StreamBuilder<Sloka?>(
          stream: nextQuery,
          builder: (context, nextSnap) {
            final previous = prevSnap.data;
            final next = nextSnap.data;
            return Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: previous == null
                        ? null
                        : () {
                            Navigator.of(context).pushReplacement(
                              MaterialPageRoute(
                                builder: (_) => SlokaScreen(
                                  db: db,
                                  slokaId: previous.id,
                                  chapterId: chapterId,
                                  position: previous.position,
                                ),
                              ),
                            );
                          },
                    icon: const Icon(Icons.chevron_left),
                    label: const Text('Previous'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: next == null
                        ? null
                        : () {
                            Navigator.of(context).pushReplacement(
                              MaterialPageRoute(
                                builder: (_) => SlokaScreen(
                                  db: db,
                                  slokaId: next.id,
                                  chapterId: chapterId,
                                  position: next.position,
                                ),
                              ),
                            );
                          },
                    icon: const Icon(Icons.chevron_right),
                    label: const Text('Next'),
                  ),
                ),
              ],
            );
          },
        );
      },
    );
  }
}
