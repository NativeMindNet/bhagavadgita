import 'package:drift/drift.dart' hide Column;
import 'package:flutter/material.dart';

import '../../app/theme/gita_colors.dart';
import '../../data/local/app_database.dart';
import '../../data/local/user_data_repository.dart';
import '../reader/sloka_screen.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key, required this.db});

  final AppDatabase db;

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _queryController = TextEditingController();
  String _query = '';

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final q = _query.trim();
    final like = '%${q.replaceAll('%', r'\%').replaceAll('_', r'\_')}%';
    final userData = UserDataRepository(widget.db);

    final query = widget.db.select(widget.db.slokas)
      ..orderBy([(t) => OrderingTerm.asc(t.id)]);
    if (q.isNotEmpty) {
      final vocabSubquery = widget.db.selectOnly(widget.db.vocabularies)
        ..addColumns([widget.db.vocabularies.slokaId])
        ..where(
          widget.db.vocabularies.tokenText.like(like) |
              widget.db.vocabularies.translation.like(like),
        );

      query.where(
        (t) =>
            t.name.like(like) |
            t.slokaText.like(like) |
            t.transcription.like(like) |
            t.translation.like(like) |
            t.comment.like(like) |
            t.id.isInQuery(vocabSubquery),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Search'),
        backgroundColor: GitaColors.white,
        foregroundColor: GitaColors.gray1,
        elevation: 0,
        scrolledUnderElevation: 0,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: TextField(
              controller: _queryController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.search),
                hintText: 'Search in slokas and translations',
              ),
              onChanged: (value) => setState(() => _query = value),
            ),
          ),
          Expanded(
            child: StreamBuilder<List<Sloka>>(
              stream: query.watch(),
              builder: (context, snap) {
                final items = snap.data ?? const <Sloka>[];
                if (snap.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (q.isNotEmpty && items.isEmpty) {
                  return const Center(child: Text('Nothing found.'));
                }
                if (q.isEmpty && items.isEmpty) {
                  return const Center(
                    child: Text('No slokas in local snapshot.'),
                  );
                }
                return ListView.separated(
                  itemCount: items.length,
                  separatorBuilder: (context, index) => const Divider(height: 1),
                  itemBuilder: (context, index) {
                    final s = items[index];
                    return ListTile(
                      title: Text(s.name),
                      subtitle: Text(
                        s.translation ?? s.slokaText ?? '',
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      trailing: StreamBuilder<bool>(
                        stream: userData.watchBookmark(s.id),
                        builder: (context, bookmarkSnap) {
                          final isBookmarked = bookmarkSnap.data ?? false;
                          return Icon(
                            isBookmarked ? Icons.bookmark : Icons.chevron_right,
                            color: isBookmarked
                                ? Theme.of(context).colorScheme.primary
                                : null,
                          );
                        },
                      ),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) =>
                                SlokaScreen(db: widget.db, slokaId: s.id),
                          ),
                        );
                      },
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
