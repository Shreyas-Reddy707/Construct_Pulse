import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/kpi_card.dart';
import '../../../../core/network/api_client.dart';
import '../../../attendance/presentation/providers/attendance_providers.dart';

final adminDashboardSummaryProvider = FutureProvider.autoDispose<Map<String, dynamic>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/dashboard/summary');
  return response.data as Map<String, dynamic>;
});

class AdminDashboardScreen extends ConsumerStatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  ConsumerState<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends ConsumerState<AdminDashboardScreen> {
  Timer? _refreshTimer;

  @override
  void initState() {
    super.initState();
    // Timer retained as fallback protection only. Primary invalidation happens via provider chains on check-in/out.
    _refreshTimer = Timer.periodic(const Duration(seconds: 60), (_) {
      ref.invalidate(adminDashboardSummaryProvider);
      ref.invalidate(occupancyProvider);
      ref.invalidate(liveAttendanceProvider);
      ref.invalidate(companyAttendanceHistoryProvider);
    });
  }

  @override
  void dispose() {
    _refreshTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final summaryAsync = ref.watch(adminDashboardSummaryProvider);
    final occupancyAsync = ref.watch(occupancyProvider);

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
                _header(context),
                const SizedBox(height: 24),
                summaryAsync.when(
                  data: (data) => Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Workforce', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/workforce'),
                              child: KpiCard(label: 'Total Workers', value: data['total_workers'].toString(), icon: Icons.people_rounded, iconColor: AppColors.primary),
                            )
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/pending-workers'),
                              child: KpiCard(label: 'Pending', value: data['pending_workers'].toString(), icon: Icons.pending_actions_rounded, iconColor: AppColors.warning),
                            )
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/workforce?status=approved'),
                              child: KpiCard(label: 'Approved', value: data['approved_workers'].toString(), icon: Icons.check_circle_rounded, iconColor: AppColors.success),
                            )
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/workforce?status=suspended'),
                              child: KpiCard(label: 'Suspended', value: data['suspended_workers'].toString(), icon: Icons.block_rounded, iconColor: AppColors.danger),
                            )
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),
                      Text('Attendance Today', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/attendance-live'),
                              child: KpiCard(label: 'Currently On Site', value: data['workers_on_site'].toString(), icon: Icons.engineering_rounded, iconColor: AppColors.primary),
                            )
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/attendance-live'),
                              child: KpiCard(label: 'Checked In Today', value: data['checked_in_today'].toString(), icon: Icons.login_rounded, iconColor: AppColors.success),
                            )
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/attendance-history'),
                              child: KpiCard(label: 'Completed Shifts', value: data['checked_out_today'].toString(), icon: Icons.logout_rounded, iconColor: AppColors.surfaceVariant),
                            )
                          ),
                          const SizedBox(width: 12),
                          Expanded(child: Container()), // Empty space to keep sizing consistent
                        ],
                      ),
                      const SizedBox(height: 16),
                      Text('Currently On Site Preview', style: AppTypography.body.copyWith(fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Consumer(
                        builder: (context, ref, child) {
                          return ref.watch(liveAttendanceProvider).when(
                            data: (live) {
                              if (live.isEmpty) return const Text('No active workers.');
                              final displayed = live.take(3).toList();
                              final remaining = live.length - displayed.length;
                              return Card(
                                elevation: 0,
                                color: AppColors.surface,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                  side: const BorderSide(color: AppColors.border),
                                ),
                                child: Column(
                                  children: [
                                    ...displayed.map((a) => ListTile(
                                          leading: const CircleAvatar(
                                            backgroundColor: AppColors.primarySurface,
                                            child: Icon(Icons.person, color: AppColors.primary, size: 20),
                                          ),
                                          title: Text(a.userName ?? 'Unknown', style: const TextStyle(fontWeight: FontWeight.w600)),
                                          subtitle: Text('${a.siteName ?? 'Unknown'} · Checked In: ${DateFormat('HH:mm').format(a.checkInTime)}'),
                                        )),
                                    if (remaining > 0)
                                      Padding(
                                        padding: const EdgeInsets.symmetric(vertical: 8),
                                        child: Text('+$remaining more active', style: const TextStyle(color: AppColors.textSecondary, fontSize: 12, fontWeight: FontWeight.bold)),
                                      ),
                                    const Divider(height: 1),
                                    TextButton(
                                      onPressed: () => context.push('/attendance-live'),
                                      child: const Text('View All Active →'),
                                    )
                                  ],
                                ),
                              );
                            },
                            loading: () => const LinearProgressIndicator(),
                            error: (_, __) => const SizedBox(),
                          );
                        },
                      ),
                      const SizedBox(height: 16),
                      Text('Recent Completed Shifts', style: AppTypography.body.copyWith(fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Consumer(
                        builder: (context, ref, child) {
                          return ref.watch(companyAttendanceHistoryProvider).when(
                            data: (history) {
                              final completed = history.where((a) => a.checkOutTime != null).toList();
                              if (completed.isEmpty) return const Text('No completed shifts today.');
                              return Card(
                                elevation: 0,
                                color: AppColors.surface,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                  side: const BorderSide(color: AppColors.border),
                                ),
                                child: Column(
                                  children: [
                                    ...completed.take(3).map((a) {
                                      final diff = a.checkOutTime!.difference(a.checkInTime);
                                      final duration = '${(diff.inMinutes / 60).toStringAsFixed(1)}h';
                                      return ListTile(
                                        leading: const CircleAvatar(
                                          backgroundColor: AppColors.background,
                                          child: Icon(Icons.logout, color: AppColors.textSecondary, size: 20),
                                        ),
                                        title: Text(a.userName ?? 'Unknown', style: const TextStyle(fontWeight: FontWeight.w600)),
                                        subtitle: Text('${a.siteName ?? 'Unknown'} · $duration'),
                                        trailing: Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(
                                            color: AppColors.background,
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                          child: const Text('Checked Out', style: TextStyle(fontSize: 10, color: AppColors.textSecondary, fontWeight: FontWeight.bold)),
                                        ),
                                      );
                                    }),
                                    const Divider(height: 1),
                                    TextButton(
                                      onPressed: () => context.push('/attendance-history'),
                                      child: const Text('View All History →'),
                                    )
                                  ],
                                ),
                              );
                            },
                            loading: () => const LinearProgressIndicator(),
                            error: (_, __) => const SizedBox(),
                          );
                        },
                      ),
                      const SizedBox(height: 24),
                      Text('Sites Overview', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/sites'),
                              child: KpiCard(label: 'Active Sites', value: data['active_sites'].toString(), icon: Icons.location_on_rounded, iconColor: AppColors.secondary),
                            )
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: GestureDetector(
                              onTap: () => context.push('/occupancy'),
                              child: KpiCard(label: 'Workers On Site', value: data['workers_on_site'].toString(), icon: Icons.engineering_rounded, iconColor: AppColors.primaryDark),
                            )
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),
                      Text('Site Occupancy', style: AppTypography.h4),
                      const SizedBox(height: 12),
                      occupancyAsync.when(
                        data: (occupancy) {
                          if (occupancy.isEmpty) {
                            return const Text('No active workers on site.');
                          }
                          return Column(
                            children: occupancy.map((site) {
                              return Card(
                                margin: const EdgeInsets.only(bottom: 8),
                                child: ListTile(
                                  onTap: () => context.push('/attendance-live?siteId=${site['site_id']}'),
                                  leading: const Icon(Icons.business_rounded, color: AppColors.primary),
                                  title: Text(site['site_name']),
                                  trailing: Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                    decoration: BoxDecoration(
                                      color: AppColors.primarySurface,
                                      borderRadius: BorderRadius.circular(16),
                                    ),
                                    child: Text(
                                      '${site['workers_on_site']} active',
                                      style: AppTypography.bodySmall.copyWith(
                                        color: AppColors.primary,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ),
                              );
                            }).toList(),
                          );
                        },
                        loading: () => const LinearProgressIndicator(),
                        error: (_, __) => const Text('Failed to load occupancy data'),
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

  Widget _header(BuildContext context) {
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
        IconButton(
          icon: const Icon(Icons.analytics_rounded, color: AppColors.textSecondary),
          onPressed: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Analytics & Reporting: Coming Soon')),
            );
          },
          tooltip: 'Analytics & Reporting (Coming Soon)',
        ),
      ],
    );
  }
}
