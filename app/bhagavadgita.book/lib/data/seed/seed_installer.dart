import 'dart:convert';

import 'package:drift/drift.dart';
import 'package:flutter/services.dart';

import '../local/app_database.dart';

class SeedInstaller {
  const SeedInstaller();

  static const String _seedAssetPath = 'assets/seed/seed_v1_minimal.json';

  Future<bool> installIfNeeded(AppDatabase db) async {
    final meta = await db.select(db.snapshotMeta).get();
    if (meta.isNotEmpty) return false;

    final raw = await rootBundle.loadString(_seedAssetPath);
    final json = jsonDecode(raw) as Map<String, Object?>;

    final schemaVersion = (json['schemaVersion'] as num?)?.toInt() ?? db.schemaVersion;
    final contentHash = (json['contentHash'] as String?) ?? 'seed-unknown';
    final nowMs = DateTime.now().millisecondsSinceEpoch;

    final languageJson = (json['languages'] as List<Object?>? ?? const []).cast<Map<String, Object?>>();
    final bookJson = (json['books'] as List<Object?>? ?? const []).cast<Map<String, Object?>>();
    final chapterJson = (json['chapters'] as List<Object?>? ?? const []).cast<Map<String, Object?>>();

    final languages = languageJson
        .map(
          (l) => LanguagesCompanion(
            id: Value((l['id'] as num).toInt()),
            code: Value(l['code'] as String),
            name: Value(l['name'] as String?),
            nativeName: Value(l['nativeName'] as String?),
            script: Value(l['script'] as String?),
            direction: Value(l['direction'] as String?),
            type: Value(l['type'] as String?),
          ),
        )
        .toList(growable: false);

    final books = bookJson
        .map(
          (b) => BooksCompanion(
            id: Value((b['id'] as num).toInt()),
            languageId: Value((b['languageId'] as num).toInt()),
            name: Value(b['name'] as String),
            initials: Value(b['initials'] as String?),
          ),
        )
        .toList(growable: false);

    final chapters = chapterJson
        .map(
          (c) => ChaptersCompanion(
            id: Value((c['id'] as num).toInt()),
            bookId: Value((c['bookId'] as num).toInt()),
            name: Value(c['name'] as String),
            position: Value((c['position'] as num).toInt()),
          ),
        )
        .toList(growable: false);

    await db.transaction(() async {
      await db.batch((batch) async {
        batch.insertAll(db.languages, languages, mode: InsertMode.insertOrReplace);
        batch.insertAll(db.books, books, mode: InsertMode.insertOrReplace);
        batch.insertAll(db.chapters, chapters, mode: InsertMode.insertOrReplace);

        batch.insert(
          db.snapshotMeta,
          SnapshotMetaCompanion.insert(
            contentHash: contentHash,
            fetchedAtMs: nowMs,
            source: 'bundled_seed',
            schemaVersion: schemaVersion,
          ),
          mode: InsertMode.insertOrReplace,
        );
      });
    });

    return true;
  }
}

