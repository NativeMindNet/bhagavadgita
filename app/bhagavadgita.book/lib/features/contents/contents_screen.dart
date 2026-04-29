import 'package:drift/drift.dart';
import 'package:flutter/material.dart';

import '../../data/local/app_database.dart';
import '../reader/chapter_screen.dart';
import '../search/search_screen.dart';
import '../settings/settings_screen.dart';

class ContentsScreen extends StatelessWidget {
  const ContentsScreen({super.key, required this.db});

  final AppDatabase db;

  @override
  Widget build(BuildContext context) {
    final chaptersQuery = (db.select(db.chapters)..where((t) => t.bookId.equals(1)))
      ..orderBy([(t) => OrderingTerm.asc(t.position)]);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Contents'),
        actions: [
          IconButton(
            tooltip: 'Search',
            icon: const Icon(Icons.search),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => SearchScreen(db: db)),
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
            return const Center(child: Text('No chapters found in local snapshot.'));
          }

          return ListView.separated(
            itemCount: chapters.length,
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (context, index) {
              final c = chapters[index];
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

