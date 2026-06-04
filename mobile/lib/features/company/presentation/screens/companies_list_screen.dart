import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../providers/company_providers.dart';
import 'create_company_screen.dart';
import 'company_detail_screen.dart';

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
              Navigator.push(context, MaterialPageRoute(builder: (_) => const CreateCompanyScreen()));
            },
          ),
        ],
      ),
      body: companiesAsync.when(
        data: (companies) {
          if (companies.isEmpty) {
            return const EmptyState(
              icon: Icons.business_rounded,
              title: 'No Companies Found',
              subtitle: 'Create a company to get started.',
            );
          }
          return RefreshIndicator(
            onRefresh: () async => ref.invalidate(companiesProvider),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: companies.length,
              itemBuilder: (context, index) {
                final company = companies[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    title: Text(company.name, style: AppTypography.body),
                    subtitle: Text(
                      'Registration: ${company.registrationNumber ?? 'N/A'}\n${company.contactEmail ?? ''}',
                      style: AppTypography.bodySmall,
                    ),
                    isThreeLine: true,
                    trailing: const Icon(Icons.chevron_right_rounded),
                    onTap: () {
                      Navigator.push(context, MaterialPageRoute(
                        builder: (_) => CompanyDetailScreen(company: company),
                      ));
                    },
                  ),
                );
              },
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => ErrorState(
          message: error.toString(),
          onRetry: () => ref.invalidate(companiesProvider),
        ),
      ),
    );
  }
}
