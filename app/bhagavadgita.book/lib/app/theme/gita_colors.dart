import 'package:flutter/material.dart';

class GitaColors {
  // Primary palette (from requirements)
  static const red1 = Color(0xFFFF5252);
  static const red2 = Color(0xFFFB9A6A);
  static const red3 = Color(0xFFC94545);

  static const gray1 = Color(0xFF4A4A4A);
  static const gray2 = Color(0xFF9B9B9B);
  static const gray3 = Color(0xFFC7C7CC);
  static const gray4 = Color(0xFFE8E8E8);
  static const gray5 = Color(0xFFF9F9F9);

  static const white = Color(0xFFFFFFFF);
  static const white30 = Color(0x4DFFFFFF);
  static const black20 = Color(0x33000000);

  // Common gradients
  static const splashGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [red2, red1],
  );
}

