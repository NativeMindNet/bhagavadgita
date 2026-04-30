import 'package:drift/drift.dart' hide Column;
import 'package:flutter/material.dart';

import '../../data/local/app_database.dart';
import '../../data/local/user_data_repository.dart';
import '../reader/sloka_screen.dart';

class BookmarksScreen extends StatelessWidget {
  const BookmarksScreen({super.key, required this.db});

  final AppDatabase db;

  @override
  Widget build(BuildContext context) {
    final userData = UserDataRepository(db);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bookmarks'),
      ),
      body: StreamBuilder<List<(Bookmark, Sloka)>>(
        stream: _watchBookmarksWithSlokas(db),
        builder: (context, snap) {
          final rows = snap.data ?? const [];
          if (snap.connectionState == ConnectionState.waiting && rows.isEmpty) {
            return const Center(child: CircularProgressIndicator());
          }
          if (rows.isEmpty) return const _EmptyBookmarks();

          return ListView.separated(
            itemCount: rows.length,
            separatorBuilder: (context, index) => const Divider(height: 1),
            itemBuilder: (context, i) {
              final (bookmark, sloka) = rows[i];
              return Dismissible(
                key: ValueKey('bookmark-${bookmark.slokaId}'),
                background: Container(
                  color: Theme.of(context).colorScheme.errorContainer,
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 16),
                  child: Icon(
                    Icons.delete_outline,
                    color: Theme.of(context).colorScheme.onErrorContainer,
                  ),
                ),
                direction: DismissDirection.endToStart,
                onDismissed: (_) => userData.setBookmark(sloka.id, false),
                child: ListTile(
                  title: Text(sloka.name),
                  subtitle: Text(
                    sloka.translation ?? sloka.slokaText ?? '',
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (context) =>
                            SlokaScreen(db: db, slokaId: sloka.id),
                      ),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class _EmptyBookmarks extends StatelessWidget {
  const _EmptyBookmarks();
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.bookmark_border,
              size: 76,
              color: Theme.of(context).colorScheme.primary.withValues(
                    alpha: 0.4,
                  ),
            ),
            const SizedBox(height: 16),
            Text(
              'No bookmarks yet',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Tap the bookmark icon on any sloka to save it here.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}

Stream<List<(Bookmark, Sloka)>> _watchBookmarksWithSlokas(AppDatabase db) {
  final q = db.select(db.bookmarks).join([
    innerJoin(db.slokas, db.slokas.id.equalsExp(db.bookmarks.slokaId)),
  ])
    ..orderBy([OrderingTerm.desc(db.bookmarks.createdAtMs)]);

  return q.watch().map((rows) {
    return rows.map((r) {
      return (r.readTable(db.bookmarks), r.readTable(db.slokas));
    }).toList(growable: false);
  });
}
