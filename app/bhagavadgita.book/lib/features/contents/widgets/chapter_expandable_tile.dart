import 'package:flutter/material.dart';
import '../../../data/local/app_database.dart';
import '../../../ui/theme/app_colors.dart';
import '../../../ui/theme/app_text.dart';

class ChapterExpandableTile extends StatelessWidget {
  const ChapterExpandableTile({
    super.key,
    required this.chapter,
    required this.slokas,
    required this.isExpanded,
    required this.onExpansionChanged,
    required this.onSlokaTap,
  });

  final Chapter chapter;
  final List<Sloka> slokas;
  final bool isExpanded;
  final ValueChanged<bool> onExpansionChanged;
  final ValueChanged<Sloka> onSlokaTap;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ListTile(
          onTap: () => onExpansionChanged(!isExpanded),
          leading: Container(
            width: 36,
            height: 36,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: isExpanded ? AppColors.red1 : AppColors.gray5,
              shape: BoxShape.circle,
            ),
            child: Text(
              chapter.position.toString(),
              style: AppText.label().copyWith(
                color: isExpanded ? AppColors.white : AppColors.gray2,
              ),
            ),
          ),
          title: Text(
            chapter.name,
            style: AppText.body().copyWith(
              fontWeight: isExpanded ? FontWeight.w700 : FontWeight.w600,
            ),
          ),
          trailing: Icon(
            isExpanded ? Icons.expand_less : Icons.expand_more,
            color: AppColors.gray3,
          ),
        ),
        if (isExpanded)
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: slokas.map((s) {
                // Strip chapter prefix from name if present, e.g. "1.4" -> "4"
                final displayTitle = s.name.contains('.') 
                    ? s.name.split('.').last 
                    : s.name;
                    
                return ChoiceChip(
                  label: Text(displayTitle),
                  selected: false,
                  onSelected: (_) => onSlokaTap(s),
                  labelStyle: AppText.label().copyWith(
                    color: AppColors.gray1,
                    fontWeight: FontWeight.w500,
                  ),
                  backgroundColor: AppColors.gray5,
                  selectedColor: AppColors.red1,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                  side: BorderSide.none,
                  showCheckmark: false,
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                );
              }).toList(),
            ),
          ),
      ],
    );
  }
}
