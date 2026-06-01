import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../providers/company_providers.dart';

class DepartmentsListScreen extends ConsumerWidget {
  const DepartmentsListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final departmentsAsync = ref.watch(departmentsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Departments'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_rounded),
            onPressed: () {
              // Navigate to add department screen
            },
          ),
        ],
      ),
      body: departmentsAsync.when(
        data: (departments) {
          if (departments.isEmpty) {
            return const Center(child: Text('No departments found.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: departments.length,
            itemBuilder: (context, index) {
              final dept = departments[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  title: Text(dept.name, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
                  subtitle: Text(dept.description ?? 'No description', style: AppTypography.caption, maxLines: 2, overflow: TextOverflow.ellipsis),
                  trailing: const Icon(Icons.chevron_right_rounded, color: AppColors.textTertiary),
                  onTap: () {
                    // Navigate to department detail
                  },
                ),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: AppColors.danger))),
      ),
    );
  }
}
