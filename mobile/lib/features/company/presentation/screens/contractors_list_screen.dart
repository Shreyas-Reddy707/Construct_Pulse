import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../providers/company_providers.dart';

class ContractorsListScreen extends ConsumerWidget {
  const ContractorsListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final contractorsAsync = ref.watch(contractorsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Contractors'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_rounded),
            onPressed: () {
              // Navigate to add contractor screen
            },
          ),
        ],
      ),
      body: contractorsAsync.when(
        data: (contractors) {
          if (contractors.isEmpty) {
            return const Center(child: Text('No contractors found.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: contractors.length,
            itemBuilder: (context, index) {
              final contractor = contractors[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  title: Text(contractor.name, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
                  subtitle: Text('Trade: ${contractor.trade ?? "Unknown"} • ${contractor.phone}', style: AppTypography.caption),
                  trailing: const Icon(Icons.chevron_right_rounded, color: AppColors.textTertiary),
                  onTap: () {
                    // Navigate to contractor detail
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
