import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';
import 'worker_shell.dart';
import 'company_admin_shell.dart';
import 'system_admin_shell.dart';

class AppShell extends ConsumerWidget {
  const AppShell({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider).user;
    
    if (user == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    switch (user.role.value) {
      case 'System Admin':
        return const SystemAdminShell();
      case 'Company Admin':
        return const CompanyAdminShell();
      default:
        return const WorkerShell();
    }
  }
}
