import 'package:flutter/material.dart';

import '../data/local/app_database.dart';
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
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFB71C1C)),
        useMaterial3: true,
      ),
      home: SplashScreen(db: _db),
    );
  }
}

