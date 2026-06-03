import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../providers/company_providers.dart';

class CompaniesListScreen extends ConsumerWidget {
  const CompaniesListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final companiesAsync = ref.watch(companiesProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Companies'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_rounded),
            onPressed: () {
              // Navigate to add company screen
            },
          ),
        ],
      ),
      body: companiesAsync.when(
        data: (companies) {
          if (companies.isEmpty) {
            return const Center(child: Text('No companies found.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: companies.length,
            itemBuilder: (context, index) {
              final company = companies[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  title: Text(company.companyName, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
                  subtitle: Text('${company.contactEmail ?? "No email"} • ${company.contactPhone ?? "No phone"}', style: AppTypography.caption),
                  trailing: const Icon(Icons.chevron_right_rounded, color: AppColors.textTertiary),
                  onTap: () {
                    // Navigate to company detail
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
