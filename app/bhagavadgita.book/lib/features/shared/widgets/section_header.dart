import 'package:flutter/material.dart';

import '../../../app/theme/gita_colors.dart';

class SectionHeader extends StatelessWidget {
  const SectionHeader(this.text, {super.key});

  final String text;

  @override
  Widget build(BuildContext context) {
    final style = Theme.of(context).textTheme.labelSmall?.copyWith(
      letterSpacing: 1.2,
      color: AppColors.gray2,
    );
    return Padding(
      padding: const EdgeInsets.only(top: 10, bottom: 6),
      child: Text(text.toUpperCase(), style: style),
    );
  }
}

