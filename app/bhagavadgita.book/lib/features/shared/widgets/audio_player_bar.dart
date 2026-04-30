import 'package:flutter/material.dart';

import '../../../app/audio/audio_controller.dart';
import '../../../app/audio/audio_state.dart';
import '../../../ui/theme/app_colors.dart';
import '../../../app/audio/audio_track.dart';

class AudioPlayerBarWithController extends StatelessWidget {
  const AudioPlayerBarWithController({
    super.key,
    required this.controller,
    required this.autoPlay,
    required this.onToggleAutoPlay,
  });

  final AudioController controller;
  final bool autoPlay;
  final ValueChanged<bool> onToggleAutoPlay;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, _) {
        final AudioState s = controller.state;
        return AudioPlayerBar(
          track: s.track,
          autoPlay: autoPlay,
          isPlaying: s.isPlaying,
          positionLabel: formatDuration(s.position),
          progress: s.progress,
          onPlayPause: () => controller.togglePlayPause(),
          onSelectTrack: (t) => controller.setTrack(t),
          onToggleAutoPlay: onToggleAutoPlay,
          onSeek: controller.seekToFraction,
          enabled: s.activeSource.isPlayable,
        );
      },
    );
  }
}

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
    this.onSeek,
    this.enabled = true,
  });

  final AudioTrack track;
  final bool isPlaying;
  final String positionLabel;
  final double progress; // 0..1

  final VoidCallback? onPlayPause;
  final ValueChanged<AudioTrack>? onSelectTrack;
  final ValueChanged<bool>? onToggleAutoPlay;
  final bool autoPlay;
  final ValueChanged<double>? onSeek;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SafeArea(
      top: false,
      child: Material(
        elevation: 8,
        color: AppColors.white,
        child: Opacity(
          opacity: enabled ? 1 : 0.55,
          child: Container(
            padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
            decoration: BoxDecoration(
              border: Border(top: BorderSide(color: AppColors.gray4)),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  children: [
                    _TrackChip(
                      label: 'Sanskrit',
                      selected: track == AudioTrack.sanskrit,
                      onTap: (!enabled || onSelectTrack == null)
                          ? null
                          : () => onSelectTrack!(AudioTrack.sanskrit),
                    ),
                    const SizedBox(width: 8),
                    _TrackChip(
                      label: 'Translation',
                      selected: track == AudioTrack.translation,
                      onTap: (!enabled || onSelectTrack == null)
                          ? null
                          : () => onSelectTrack!(AudioTrack.translation),
                    ),
                    const Spacer(),
                    InkWell(
                      onTap: (!enabled || onToggleAutoPlay == null)
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
                              color:
                                  autoPlay ? AppColors.red1 : AppColors.gray2,
                            ),
                            const SizedBox(width: 4),
                            Text(
                              'Auto',
                              style: theme.textTheme.bodySmall?.copyWith(
                                color: autoPlay
                                    ? AppColors.red1
                                    : AppColors.gray2,
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
                      onPressed: enabled ? onPlayPause : null,
                      icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
                      color: AppColors.gray1,
                    ),
                    Expanded(
                      child: _SeekBar(
                        enabled: enabled,
                        progress: progress,
                        onSeek: onSeek,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Text(
                      positionLabel,
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: AppColors.gray2,
                        fontFeatures: const [FontFeature.tabularFigures()],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _SeekBar extends StatelessWidget {
  const _SeekBar({
    required this.enabled,
    required this.progress,
    required this.onSeek,
  });

  final bool enabled;
  final double progress;
  final ValueChanged<double>? onSeek;

  @override
  Widget build(BuildContext context) {
    final p = progress.clamp(0.0, 1.0);
    return LayoutBuilder(
      builder: (context, constraints) {
        return GestureDetector(
          behavior: HitTestBehavior.opaque,
          onTapDown: (!enabled || onSeek == null)
              ? null
              : (d) {
                  final x =
                      d.localPosition.dx.clamp(0.0, constraints.maxWidth);
                  onSeek!(
                    constraints.maxWidth <= 0 ? 0 : (x / constraints.maxWidth),
                  );
                },
          onHorizontalDragUpdate: (!enabled || onSeek == null)
              ? null
              : (d) {
                  final x =
                      d.localPosition.dx.clamp(0.0, constraints.maxWidth);
                  onSeek!(
                    constraints.maxWidth <= 0 ? 0 : (x / constraints.maxWidth),
                  );
                },
          child: ClipRRect(
            borderRadius: BorderRadius.circular(999),
            child: LinearProgressIndicator(
              value: p,
              minHeight: 6,
              backgroundColor: AppColors.gray4,
              valueColor: const AlwaysStoppedAnimation(AppColors.red1),
            ),
          ),
        );
      },
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
            color: selected ? AppColors.red1 : AppColors.gray3,
          ),
          color: selected ? AppColors.red1.withValues(alpha: 0.08) : null,
        ),
        child: Text(
          label,
          style: theme.textTheme.bodySmall?.copyWith(
            color: selected ? AppColors.red1 : AppColors.gray2,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }
}

