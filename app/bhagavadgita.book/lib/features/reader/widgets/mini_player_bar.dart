import 'package:flutter/material.dart';

import '../../../ui/theme/app_colors.dart';
import '../../../ui/theme/app_text.dart';
import '../../../app/audio/audio_controller.dart';

class MiniPlayerBar extends StatelessWidget {
  const MiniPlayerBar({
    super.key,
    required this.controller,
    required this.slokaName,
  });

  final AudioController controller;
  final String slokaName;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: AppColors.white,
        border: Border(top: BorderSide(color: AppColors.gray4)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: SafeArea(
        top: false,
        child: Row(
          children: [
            Expanded(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(slokaName, style: AppText.caption().copyWith(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 4),
                  ValueListenableBuilder(
                    valueListenable: controller.progress,
                    builder: (context, progress, _) => LinearProgressIndicator(
                      value: progress,
                      backgroundColor: AppColors.gray4,
                      color: AppColors.red1,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 16),
            IconButton(
              icon: const Icon(Icons.play_arrow, color: AppColors.red1),
              onPressed: controller.togglePlay,
            ),
          ],
        ),
      ),
    );
  }
}
