import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/kpi_card.dart';
import '../../../../core/network/api_client.dart';

final adminDashboardSummaryProvider = FutureProvider.autoDispose<Map<String, dynamic>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/dashboard/summary');
  return response.data as Map<String, dynamic>;
});

class AdminDashboardScreen extends ConsumerWidget {
  const AdminDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summaryAsync = ref.watch(adminDashboardSummaryProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async => ref.invalidate(adminDashboardSummaryProvider),
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _header(),
                const SizedBox(height: 24),
                summaryAsync.when(
                  data: (data) => Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Workforce', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(child: KpiCard(label: 'Total Workers', value: data['total_workers'].toString(), icon: Icons.people_rounded, iconColor: AppColors.primary)),
                          const SizedBox(width: 12),
                          Expanded(child: KpiCard(label: 'Pending', value: data['pending_workers'].toString(), icon: Icons.pending_actions_rounded, iconColor: AppColors.warning)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(child: KpiCard(label: 'Approved', value: data['approved_workers'].toString(), icon: Icons.check_circle_rounded, iconColor: AppColors.success)),
                          const SizedBox(width: 12),
                          Expanded(child: KpiCard(label: 'Suspended', value: data['suspended_workers'].toString(), icon: Icons.block_rounded, iconColor: AppColors.danger)),
                        ],
                      ),
                      const SizedBox(height: 24),
                      Text('Attendance (Today)', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(child: KpiCard(label: 'Checked In', value: data['checked_in_today'].toString(), icon: Icons.login_rounded, iconColor: AppColors.success)),
                          const SizedBox(width: 12),
                          Expanded(child: KpiCard(label: 'Checked Out', value: data['checked_out_today'].toString(), icon: Icons.logout_rounded, iconColor: AppColors.surfaceVariant)),
                        ],
                      ),
                      const SizedBox(height: 24),
                      Text('Sites Overview', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(child: KpiCard(label: 'Active Sites', value: data['active_sites'].toString(), icon: Icons.location_on_rounded, iconColor: AppColors.secondary)),
                          const SizedBox(width: 12),
                          Expanded(child: KpiCard(label: 'Workers On Site', value: data['workers_on_site'].toString(), icon: Icons.engineering_rounded, iconColor: AppColors.primaryDark)),
                        ],
                      ),
                    ],
                  ),
                  loading: () => const Center(child: Padding(padding: EdgeInsets.all(40), child: CircularProgressIndicator())),
                  error: (error, _) => Center(child: Text('Error: $error', style: const TextStyle(color: AppColors.danger))),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _header() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Admin Dashboard', style: AppTypography.h2),
            const SizedBox(height: 4),
            Text('Platform Overview', style: AppTypography.body.copyWith(color: AppColors.textSecondary)),
          ],
        ),
      ],
    );
  }
}
