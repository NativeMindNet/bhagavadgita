import 'package:drift/drift.dart' hide Column;
import 'package:flutter/material.dart';

import '../../data/local/app_database.dart';
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

    final query = widget.db.select(widget.db.slokas)
      ..orderBy([(t) => OrderingTerm.asc(t.id)]);
    if (q.isNotEmpty) {
      query.where(
        (t) =>
            t.name.like(like) |
            t.slokaText.like(like) |
            t.transcription.like(like) |
            t.translation.like(like) |
            t.comment.like(like),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Search')),
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
                final items = snap.data ?? const [];
                if (snap.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (items.isEmpty) {
                  return const Center(child: Text('Nothing found.'));
                }
                return ListView.separated(
                  itemCount: items.length,
                  separatorBuilder: (_, __) => const Divider(height: 1),
                  itemBuilder: (context, index) {
                    final s = items[index];
                    return ListTile(
                      title: Text(s.name),
                      subtitle: Text(
                        s.translation ?? s.slokaText ?? '',
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => SlokaScreen(db: widget.db, slokaId: s.id),
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

