import 'package:flutter/material.dart';

import '../data/local/app_database.dart';
import 'theme/gita_theme.dart';
import '../features/splash/splash_screen.dart';

class GitaBookApp extends StatefulWidget {
  const GitaBookApp({super.key});

  @override
  State<GitaBookApp> createState() => _GitaBookAppState();
}

class _GitaBookAppState extends State<GitaBookApp> {
  late final AppDatabase _db;

  @override
  void initState() {
    super.initState();
    _db = AppDatabase();
  }

  @override
  void dispose() {
    _db.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bhagavad Gita',
      theme: GitaTheme.light(),
      home: SplashScreen(db: _db),
    );
  }
}

