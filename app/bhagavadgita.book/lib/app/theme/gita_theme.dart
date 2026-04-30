import 'package:flutter/material.dart';

import 'gita_colors.dart';

class GitaTheme {
  static ThemeData light() {
    final scheme = ColorScheme.fromSeed(
      seedColor: AppColors.red1,
      brightness: Brightness.light,
    ).copyWith(
      primary: AppColors.red1,
      secondary: AppColors.red2,
      surface: AppColors.white,
      onSurface: AppColors.gray1,
    );

    final baseTextTheme = ThemeData.light().textTheme;

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: AppColors.white,
      dividerColor: AppColors.gray3,
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.red1,
        foregroundColor: AppColors.white,
        centerTitle: true,
      ),
      switchTheme: SwitchThemeData(
        thumbColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) return AppColors.red1;
          return null;
        }),
        trackColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return AppColors.red1.withValues(alpha: 0.35);
          }
          return null;
        }),
      ),
      listTileTheme: const ListTileThemeData(
        iconColor: AppColors.gray2,
        textColor: AppColors.gray1,
      ),
      textTheme: baseTextTheme.copyWith(
        titleLarge: baseTextTheme.titleLarge?.copyWith(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: AppColors.gray1,
        ),
        titleMedium: baseTextTheme.titleMedium?.copyWith(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: AppColors.gray1,
        ),
        bodyLarge: baseTextTheme.bodyLarge?.copyWith(
          fontSize: 16,
          height: 1.35,
          color: AppColors.gray1,
        ),
        bodyMedium: baseTextTheme.bodyMedium?.copyWith(
          fontSize: 15,
          height: 1.35,
          color: AppColors.gray1,
        ),
        bodySmall: baseTextTheme.bodySmall?.copyWith(
          fontSize: 14,
          height: 1.35,
          color: AppColors.gray2,
        ),
        labelSmall: baseTextTheme.labelSmall?.copyWith(
          fontSize: 12,
          fontWeight: FontWeight.w700,
          color: AppColors.gray2,
        ),
      ),
    );
  }
}

