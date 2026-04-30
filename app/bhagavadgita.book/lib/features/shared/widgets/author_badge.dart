import 'package:flutter/material.dart';

import '../../../app/theme/gita_colors.dart';

class AuthorBadge extends StatelessWidget {
  const AuthorBadge({
    super.key,
    required this.initials,
    this.size = 28,
  });

  final String initials;
  final double size;

  @override
  Widget build(BuildContext context) {
    final textStyle = Theme.of(context).textTheme.labelSmall?.copyWith(
      color: GitaColors.red1,
      fontWeight: FontWeight.w700,
    );

    return Container(
      width: size,
      height: size,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: GitaColors.white,
        border: Border.all(color: GitaColors.red1, width: 1.5),
      ),
      child: Text(initials, style: textStyle),
    );
  }
}

