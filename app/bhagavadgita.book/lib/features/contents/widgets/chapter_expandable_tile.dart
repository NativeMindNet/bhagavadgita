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
    required this.selectedSlokaId,
    required this.onExpansionChanged,
    required this.onSlokaTap,
  });

  final Chapter chapter;
  final List<Sloka> slokas;
  final bool isExpanded;
  final int? selectedSlokaId;
  final ValueChanged<bool> onExpansionChanged;
  final ValueChanged<Sloka> onSlokaTap;

  @override
  Widget build(BuildContext context) {
    final ranges = _groupSlokaRanges(slokas);

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
              children: ranges.map((range) {
                final isSelected = range.slokas.any((s) => s.id == selectedSlokaId);
                return ChoiceChip(
                  label: Text(range.label),
                  selected: isSelected,
                  onSelected: (_) => onSlokaTap(range.slokas.first),
                  labelStyle: AppText.label().copyWith(
                    color: isSelected ? AppColors.white : AppColors.gray1,
                    fontWeight: FontWeight.w600,
                  ),
                  backgroundColor: AppColors.gray5,
                  selectedColor: AppColors.red1,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                    side: isSelected ? BorderSide.none : const BorderSide(color: AppColors.gray4),
                  ),
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

class _SlokaRange {
  _SlokaRange(this.slokas);
  final List<Sloka> slokas;

  String get label {
    if (slokas.length == 1) {
      final s = slokas.first;
      return s.name.contains('.') ? s.name.split('.').last : s.position.toString();
    }
    final first = slokas.first;
    final last = slokas.last;
    final firstNum = first.name.contains('.') ? first.name.split('.').last : first.position.toString();
    final lastNum = last.name.contains('.') ? last.name.split('.').last : last.position.toString();
    return '$firstNum-$lastNum';
  }
}

List<_SlokaRange> _groupSlokaRanges(List<Sloka> slokas) {
  if (slokas.isEmpty) return [];

  final ranges = <_SlokaRange>[];
  var currentGroup = <Sloka>[slokas.first];

  for (var i = 1; i < slokas.length; i++) {
    final prev = slokas[i - 1];
    final curr = slokas[i];
    if (curr.position == prev.position + 1) {
      currentGroup.add(curr);
    } else {
      ranges.add(_SlokaRange(currentGroup));
      currentGroup = [curr];
    }
  }
  ranges.add(_SlokaRange(currentGroup));

  return ranges;
}
