import 'package:flutter/material.dart';

import '../../../app/theme/gita_colors.dart';

enum AudioTrack { sanskrit, translation }

class AudioPlayerBar extends StatelessWidget {
  const AudioPlayerBar({
    super.key,
    this.track = AudioTrack.sanskrit,
    this.isPlaying = false,
    this.positionLabel = '0:00',
    this.progress = 0,
    this.onPlayPause,
    this.onSelectTrack,
    this.onToggleAutoPlay,
    this.autoPlay = false,
  });

  final AudioTrack track;
  final bool isPlaying;
  final String positionLabel;
  final double progress; // 0..1

  final VoidCallback? onPlayPause;
  final ValueChanged<AudioTrack>? onSelectTrack;
  final ValueChanged<bool>? onToggleAutoPlay;
  final bool autoPlay;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SafeArea(
      top: false,
      child: Material(
        elevation: 8,
        color: GitaColors.white,
        child: Container(
          padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
          decoration: BoxDecoration(
            border: Border(top: BorderSide(color: GitaColors.gray4)),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                children: [
                  _TrackChip(
                    label: 'Sanskrit',
                    selected: track == AudioTrack.sanskrit,
                    onTap: onSelectTrack == null
                        ? null
                        : () => onSelectTrack!(AudioTrack.sanskrit),
                  ),
                  const SizedBox(width: 8),
                  _TrackChip(
                    label: 'Translation',
                    selected: track == AudioTrack.translation,
                    onTap: onSelectTrack == null
                        ? null
                        : () => onSelectTrack!(AudioTrack.translation),
                  ),
                  const Spacer(),
                  InkWell(
                    onTap: onToggleAutoPlay == null
                        ? null
                        : () => onToggleAutoPlay!(!autoPlay),
                    borderRadius: BorderRadius.circular(12),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 6,
                      ),
                      child: Row(
                        children: [
                          Icon(
                            autoPlay ? Icons.repeat_one : Icons.repeat,
                            size: 18,
                            color: autoPlay ? GitaColors.red1 : GitaColors.gray2,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            'Auto',
                            style: theme.textTheme.bodySmall?.copyWith(
                              color: autoPlay ? GitaColors.red1 : GitaColors.gray2,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  IconButton(
                    onPressed: onPlayPause,
                    icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
                    color: GitaColors.gray1,
                  ),
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(999),
                      child: LinearProgressIndicator(
                        value: progress.clamp(0, 1),
                        minHeight: 6,
                        backgroundColor: GitaColors.gray4,
                        valueColor: const AlwaysStoppedAnimation(GitaColors.red1),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    positionLabel,
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: GitaColors.gray2,
                      fontFeatures: const [FontFeature.tabularFigures()],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _TrackChip extends StatelessWidget {
  const _TrackChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final bool selected;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(999),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(999),
          border: Border.all(
            color: selected ? GitaColors.red1 : GitaColors.gray3,
          ),
          color: selected ? GitaColors.red1.withValues(alpha: 0.08) : null,
        ),
        child: Text(
          label,
          style: theme.textTheme.bodySmall?.copyWith(
            color: selected ? GitaColors.red1 : GitaColors.gray2,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }
}

