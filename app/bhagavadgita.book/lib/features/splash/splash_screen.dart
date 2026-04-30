import 'package:flutter/material.dart';

import '../../app/bootstrap/bootstrap_coordinator.dart';
import '../../ui/theme/app_text.dart';
import '../../data/local/app_database.dart';
import '../contents/contents_screen.dart';
import '../onboarding/onboarding_screen.dart';
import '../onboarding/app_onboarding_controller.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key, required this.db});

  final AppDatabase db;

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  late Future<BootstrapResult> _future;
  double _simulatedProgress = 0.0;
  Timer? _progressTimer;

  @override
  void initState() {
    super.initState();
    _future = _bootstrap();
    _startSimulatedProgress();
  }

  void _startSimulatedProgress() {
    _progressTimer?.cancel();
    _simulatedProgress = 0.0;
    _progressTimer = Timer.periodic(const Duration(milliseconds: 50), (timer) {
      setState(() {
        if (_simulatedProgress < 0.95) {
          _simulatedProgress += 0.02;
        }
      });
    });
  }

  @override
  void dispose() {
    _progressTimer?.cancel();
    super.dispose();
  }

  Future<BootstrapResult> _bootstrap() async {
    final result = await BootstrapCoordinator(db: widget.db).run();
    if (mounted) {
      setState(() {
        _simulatedProgress = 1.0;
      });
      _progressTimer?.cancel();
    }
    return result;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<BootstrapResult>(
      future: _future,
      builder: (context, snap) {
        if (snap.connectionState != ConnectionState.done) {
          return _SplashScaffold(
            title: 'BHAGAVAD GITA',
            subtitle: 'Initializing local storage…',
            showProgress: true,
            progress: _simulatedProgress,
          );
        }
        if (snap.hasError) {
          return _SplashScaffold(
            title: 'BHAGAVAD GITA',
            subtitle: 'Startup failed. Tap to retry.',
            showProgress: false,
            onTap: () {
              _startSimulatedProgress();
              setState(() => _future = _bootstrap());
            },
          );
        }

        final result = snap.requireData;
        if (!result.hasSnapshot) {
          return const _SplashScaffold(
            title: 'BHAGAVAD GITA',
            subtitle: 'No local snapshot is available.',
            showProgress: false,
          );
        }

        return ListenableBuilder(
          listenable: appOnboardingController,
          builder: (context, _) {
            if (!appOnboardingController.value) {
              return OnboardingScreen(db: widget.db);
            }
            return ContentsScreen(db: widget.db);
          },
        );
      },
    );
  }
}

class _SplashScaffold extends StatelessWidget {
  const _SplashScaffold({
    required this.title,
    required this.subtitle,
    required this.showProgress,
    this.progress = 0.0,
    this.onTap,
  });

  final String title;
  final String subtitle;
  final bool showProgress;
  final double progress;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: InkWell(
        onTap: onTap,
        child: Container(
          width: double.infinity,
          height: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 24),
          decoration: const BoxDecoration(gradient: AppColors.splashGradient),
          child: SafeArea(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'OM',
                  style: AppText.splashTitle().copyWith(
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  title,
                  textAlign: TextAlign.center,
                  style: AppText.splashTitle(),
                ),
                const SizedBox(height: 12),
                Text(
                  subtitle,
                  textAlign: TextAlign.center,
                  style: AppText.body().copyWith(
                    color: AppColors.white.withValues(alpha: 0.92),
                  ),
                ),
                if (showProgress) ...[
                  const SizedBox(height: 32),
                  SizedBox(
                    width: 240,
                    child: Column(
                      children: [
                        ClipRRect(
                          borderRadius: BorderRadius.circular(999),
                          child: LinearProgressIndicator(
                            value: progress,
                            minHeight: 8,
                            backgroundColor: AppColors.white30,
                            valueColor:
                                const AlwaysStoppedAnimation(AppColors.white),
                          ),
                        ),
                        const SizedBox(height: 12),
                        Text(
                          '${(progress * 100).toInt()}%',
                          style: AppText.caption().copyWith(
                            color: AppColors.white,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
