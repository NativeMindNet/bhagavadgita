import 'package:flutter/material.dart';

import '../../app/bootstrap/bootstrap_coordinator.dart';
import '../../data/local/app_database.dart';
import '../contents/contents_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key, required this.db});

  final AppDatabase db;

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  late final Future<BootstrapResult> _future;

  @override
  void initState() {
    super.initState();
    _future = _bootstrap();
  }

  Future<BootstrapResult> _bootstrap() async {
    return BootstrapCoordinator(db: widget.db).run();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<BootstrapResult>(
      future: _future,
      builder: (context, snap) {
        if (snap.connectionState != ConnectionState.done) {
          return const _SplashScaffold(
            title: 'Bhagavad Gita',
            subtitle: 'Initializing local storage…',
            showProgress: true,
          );
        }
        if (snap.hasError) {
          return _SplashScaffold(
            title: 'Bhagavad Gita',
            subtitle: 'Startup failed. Tap to retry.',
            showProgress: false,
            onTap: () => setState(() => _future = _bootstrap()),
          );
        }

        final result = snap.requireData;
        if (!result.hasSnapshot) {
          return const _SplashScaffold(
            title: 'Bhagavad Gita',
            subtitle: 'No local snapshot is available.',
            showProgress: false,
          );
        }

        return ContentsScreen(db: widget.db);
      },
    );
  }
}

class _SplashScaffold extends StatelessWidget {
  const _SplashScaffold({
    required this.title,
    required this.subtitle,
    required this.showProgress,
    this.onTap,
  });

  final String title;
  final String subtitle;
  final bool showProgress;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: InkWell(
        onTap: onTap,
        child: Container(
          width: double.infinity,
          height: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 24),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                theme.colorScheme.primary.withValues(alpha: 0.12),
                theme.colorScheme.surface,
              ],
            ),
          ),
          child: SafeArea(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(title, style: theme.textTheme.headlineMedium),
                const SizedBox(height: 12),
                Text(subtitle, style: theme.textTheme.bodyLarge),
                if (showProgress) ...[
                  const SizedBox(height: 24),
                  const SizedBox(width: 220, child: LinearProgressIndicator()),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

