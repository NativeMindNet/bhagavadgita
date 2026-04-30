import 'package:drift/drift.dart';
import 'package:flutter/material.dart';

import '../../data/local/app_database.dart';
import '../shared/widgets/quote_card.dart';
import '../reader/chapter_screen.dart';
import '../search/search_screen.dart';
import '../search/search_route.dart';
import '../settings/settings_screen.dart';

class ContentsScreen extends StatelessWidget {
  const ContentsScreen({super.key, required this.db});

  final AppDatabase db;
  static final GlobalKey _searchKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    final chaptersQuery = (db.select(db.chapters)..where((t) => t.bookId.equals(1)))
      ..orderBy([(t) => OrderingTerm.asc(t.position)]);

    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Contents'),
        actions: [
          IconButton(
            key: _searchKey,
            tooltip: 'Search',
            icon: const Icon(Icons.search),
            onPressed: () {
              final renderBox =
                  _searchKey.currentContext?.findRenderObject() as RenderBox?;
              final center = renderBox == null
                  ? (MediaQuery.of(context).size.center(Offset.zero))
                  : renderBox.localToGlobal(
                      renderBox.size.center(Offset.zero),
                    );
              Navigator.of(context).push(
                CircularRevealPageRoute(
                  center: center,
                  builder: (_) => SearchScreen(db: db),
                ),
              );
            },
          ),
          IconButton(
            tooltip: 'Reader settings',
            icon: const Icon(Icons.tune),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: StreamBuilder<List<Chapter>>(
        stream: chaptersQuery.watch(),
        builder: (context, snap) {
          final chapters = snap.data ?? const [];
          if (snap.connectionState == ConnectionState.waiting && chapters.isEmpty) {
            return const Center(child: CircularProgressIndicator());
          }
          if (chapters.isEmpty) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.menu_book_outlined,
                      size: 54,
                      color: theme.colorScheme.onSurface.withValues(alpha: 0.35),
                    ),
                    const SizedBox(height: 14),
                    Text(
                      'No chapters found',
                      style: theme.textTheme.titleMedium,
                    ),
                    const SizedBox(height: 6),
                    Text(
                      'Please check your connection and try again.',
                      textAlign: TextAlign.center,
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: theme.colorScheme.onSurface.withValues(
                          alpha: 0.6,
                        ),
                      ),
                    ),
                    const SizedBox(height: 14),
                    FilledButton(
                      onPressed: () {
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(
                            builder: (_) => ContentsScreen(db: db),
                          ),
                        );
                      },
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            );
          }

          return ListView.separated(
            itemCount: chapters.length + 1,
            padding: const EdgeInsets.only(bottom: 12),
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (context, index) {
              if (index == 0) {
                return const QuoteCard(
                  quote: '“You have a right to perform your prescribed duty…”',
                  author: 'Bhagavad Gita',
                );
              }
              final c = chapters[index - 1];
              return ListTile(
                title: Text('Chapter ${c.position}'),
                subtitle: Text(c.name),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => ChapterScreen(
                        db: db,
                        chapterId: c.id,
                        title: 'Chapter ${c.position}',
                      ),
                    ),
                  );
                },
              );
            },
          );
        },
      ),
    );
  }
}

