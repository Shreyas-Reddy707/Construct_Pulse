import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';

import '../../domain/entities/company.dart';
import '../providers/company_providers.dart';

class CompanyDetailScreen extends ConsumerWidget {
  final Company company;

  const CompanyDetailScreen({super.key, required this.company});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(companyUsersProvider(company.id));
    final actionState = ref.watch(assignAdminNotifierProvider);

    ref.listen<AsyncValue<void>>(assignAdminNotifierProvider, (_, state) {
      state.whenOrNull(
        error: (e, _) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString()), backgroundColor: AppColors.danger)),
        data: (_) {
          if (!state.isLoading && !state.hasError && state.hasValue) {
            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Admin assigned successfully')));
          }
        },
      );
    });

    return Scaffold(
      appBar: AppBar(title: Text(company.name)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildInfoCard(),
          const SizedBox(height: 24),
          Text('Company Users', style: AppTypography.h4),
          const SizedBox(height: 16),
          usersAsync.when(
            data: (users) {
              if (users.isEmpty) return const Text('No users in this company.');
              
              final admins = users.where((u) => u.role.value == 'Company Admin').toList();
              final others = users.where((u) => u.role.value != 'Company Admin' && u.role.value != 'System Admin').toList();

              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (admins.isNotEmpty) ...[
                    Text('Current Admins', style: AppTypography.body),
                    ...admins.map((u) => ListTile(
                      title: Text(u.fullName),
                      subtitle: Text(u.phone),
                      leading: const CircleAvatar(child: Icon(Icons.admin_panel_settings)),
                    )),
                    const Divider(),
                  ],
                  if (others.isNotEmpty) ...[
                    Text('Available Users', style: AppTypography.body),
                    ...others.map((u) => ListTile(
                      title: Text(u.fullName),
                      subtitle: Text(u.phone),
                      trailing: actionState.isLoading
                          ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                          : TextButton(
                              onPressed: () => ref.read(assignAdminNotifierProvider.notifier).assignAdmin(company.id, u.id),
                              child: const Text('Assign Admin'),
                            ),
                    )),
                  ],
                ],
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Text('Error: $e', style: const TextStyle(color: AppColors.danger)),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoCard() {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: AppColors.border),
      ),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.asset(
              'assets/images/logo.png',
              width: 80,
              height: 80,
              errorBuilder: (context, error, stackTrace) => const Icon(Icons.business, size: 80, color: AppColors.primary),
            ),
            const SizedBox(height: 16),
            Text(company.name, style: AppTypography.h3, textAlign: TextAlign.center),
            const SizedBox(height: 4),
            Text('Masters of Consistency and Quality', style: AppTypography.bodySmall.copyWith(color: AppColors.primary, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 16),
            _infoRow('Admin', 'Nilesh Patel'),
            _infoRow('Phone', company.contactPhone ?? 'N/A'),
          ],
        ),
      ),
    );
  }

  Widget _infoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 100, child: Text(label, style: AppTypography.caption)),
          Expanded(child: Text(value, style: AppTypography.body)),
        ],
      ),
    );
  }
}
