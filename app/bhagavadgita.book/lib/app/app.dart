import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import '../l10n/gen/app_localizations.dart';

import '../data/local/app_database.dart';
import 'theme/gita_theme.dart';
import '../features/splash/splash_screen.dart';
import '../features/settings/app_language_controller.dart';

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
    return ValueListenableBuilder<AppLanguageSettings>(
      valueListenable: appLanguageController,
      builder: (context, settings, _) => MaterialApp(
        title: 'Bhagavad Gita',
        theme: GitaTheme.light(),
        locale: settings.effectiveLocale,
        supportedLocales: AppLanguageController.supported,
        localizationsDelegates: const [
          AppLocalizations.delegate,
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        home: SplashScreen(db: _db),
      ),
    );
  }
}

