import 'package:flutter/material.dart';

import 'gita_colors.dart';

class GitaTheme {
  static ThemeData light() {
    final scheme = ColorScheme.fromSeed(
      seedColor: GitaColors.red1,
      brightness: Brightness.light,
    ).copyWith(
      primary: GitaColors.red1,
      secondary: GitaColors.red2,
      surface: GitaColors.white,
      onSurface: GitaColors.gray1,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: GitaColors.white,
      dividerColor: GitaColors.gray3,
      appBarTheme: const AppBarTheme(
        backgroundColor: GitaColors.red1,
        foregroundColor: GitaColors.white,
        centerTitle: true,
      ),
      switchTheme: SwitchThemeData(
        thumbColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) return GitaColors.red1;
          return null;
        }),
        trackColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return GitaColors.red1.withValues(alpha: 0.35);
          }
          return null;
        }),
      ),
      listTileTheme: const ListTileThemeData(
        iconColor: GitaColors.gray2,
        textColor: GitaColors.gray1,
      ),
      textTheme: const TextTheme(
        titleLarge: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        titleMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        bodyLarge: TextStyle(fontSize: 16, height: 1.35),
        bodyMedium: TextStyle(fontSize: 15, height: 1.35),
        bodySmall: TextStyle(fontSize: 14, height: 1.35),
        labelSmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
      ),
    );
  }
}

