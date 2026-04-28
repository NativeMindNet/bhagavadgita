import 'dart:io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import 'tables.dart';

part 'app_database.g.dart';

@DriftDatabase(
  tables: [
    SnapshotMeta,
    Languages,
    Books,
    Chapters,
    Slokas,
    Vocabularies,
    Bookmarks,
    Notes,
  ],
)
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dir = await getApplicationDocumentsDirectory();
    final file = p.join(dir.path, 'bhagavadgita.sqlite');
    return NativeDatabase.createInBackground(File(file));
  });
}
