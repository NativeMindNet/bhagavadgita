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

    final baseTextTheme = ThemeData.light().textTheme;

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
      textTheme: baseTextTheme.copyWith(
        titleLarge: baseTextTheme.titleLarge?.copyWith(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: GitaColors.gray1,
        ),
        titleMedium: baseTextTheme.titleMedium?.copyWith(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: GitaColors.gray1,
        ),
        bodyLarge: baseTextTheme.bodyLarge?.copyWith(
          fontSize: 16,
          height: 1.35,
          color: GitaColors.gray1,
        ),
        bodyMedium: baseTextTheme.bodyMedium?.copyWith(
          fontSize: 15,
          height: 1.35,
          color: GitaColors.gray1,
        ),
        bodySmall: baseTextTheme.bodySmall?.copyWith(
          fontSize: 14,
          height: 1.35,
          color: GitaColors.gray2,
        ),
        labelSmall: baseTextTheme.labelSmall?.copyWith(
          fontSize: 12,
          fontWeight: FontWeight.w700,
          color: GitaColors.gray2,
        ),
      ),
    );
  }
}

