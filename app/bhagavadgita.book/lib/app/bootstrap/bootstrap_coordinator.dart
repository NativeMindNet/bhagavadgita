import '../../data/local/app_database.dart';
import '../../data/seed/seed_installer.dart';

class BootstrapCoordinator {
  const BootstrapCoordinator({
    required this.db,
    this.seedInstaller = const SeedInstaller(),
  });

  final AppDatabase db;
  final SeedInstaller seedInstaller;

  Future<BootstrapResult> run() async {
    final meta = await db.select(db.snapshotMeta).get();
    if (meta.isNotEmpty) {
      return const BootstrapResult(hasSnapshot: true, installedSeed: false);
    }

    final installedSeed = await seedInstaller.installIfNeeded(db);
    return BootstrapResult(hasSnapshot: installedSeed, installedSeed: installedSeed);
  }
}

class BootstrapResult {
  const BootstrapResult({required this.hasSnapshot, required this.installedSeed});

  final bool hasSnapshot;
  final bool installedSeed;
}

