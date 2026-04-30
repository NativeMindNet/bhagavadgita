import 'package:flutter/material.dart';

import '../../../ui/theme/app_colors.dart';
import '../../../ui/theme/app_text.dart';

class VariantPill extends StatelessWidget {
  const VariantPill({super.key, required this.label});

  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: AppColors.gray5,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: AppColors.gray3),
      ),
      child: Text(
        label,
        style: AppText.caption().copyWith(
          fontWeight: FontWeight.w700,
          color: AppColors.gray1,
        ),
      ),
    );
  }
}
