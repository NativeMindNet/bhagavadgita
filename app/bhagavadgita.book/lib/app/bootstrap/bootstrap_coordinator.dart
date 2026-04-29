import 'dart:async';

import '../sync/sync_orchestrator.dart';
import '../../data/local/app_database.dart';
import '../../data/seed/seed_installer.dart';

class BootstrapCoordinator {
  const BootstrapCoordinator({
    required this.db,
    this.seedInstaller = const SeedInstaller(),
    this.syncOrchestratorFactory = _defaultSyncOrchestratorFactory,
  });

  final AppDatabase db;
  final SeedInstaller seedInstaller;
  final SyncOrchestrator Function(AppDatabase db) syncOrchestratorFactory;

  Future<BootstrapResult> run() async {
    final meta = await db.select(db.snapshotMeta).get();
    if (meta.isNotEmpty) {
      unawaited(syncOrchestratorFactory(db).startupSync());
      return const BootstrapResult(hasSnapshot: true, installedSeed: false, syncScheduled: true);
    }

    final installedSeed = await seedInstaller.installIfNeeded(db);
    if (installedSeed) {
      unawaited(syncOrchestratorFactory(db).startupSync());
    }
    return BootstrapResult(
      hasSnapshot: installedSeed,
      installedSeed: installedSeed,
      syncScheduled: installedSeed,
    );
  }
}

SyncOrchestrator _defaultSyncOrchestratorFactory(AppDatabase db) => SyncOrchestrator(db: db);

class BootstrapResult {
  const BootstrapResult({
    required this.hasSnapshot,
    required this.installedSeed,
    required this.syncScheduled,
  });

  final bool hasSnapshot;
  final bool installedSeed;
  final bool syncScheduled;
}

