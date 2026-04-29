import 'package:flutter/material.dart';

import '../../data/local/app_database.dart';

class ContentsScreen extends StatelessWidget {
  const ContentsScreen({super.key, required this.db});

  final AppDatabase db;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Contents')),
      body: const Center(
        child: Text('Contents will be loaded from local DB.'),
      ),
    );
  }
}

