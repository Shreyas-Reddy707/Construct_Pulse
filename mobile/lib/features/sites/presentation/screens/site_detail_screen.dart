import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/site_providers.dart';
import '../../../workforce/presentation/providers/worker_providers.dart';
import '../../../auth/presentation/providers/auth_provider.dart';

class SiteDetailScreen extends ConsumerWidget {
  final String siteId;

  const SiteDetailScreen({super.key, required this.siteId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final siteAsync = ref.watch(siteProvider(siteId));
    final assignmentsAsync = ref.watch(siteAssignmentsProvider(siteId));
    
    // We can't directly read occupancyProvider if it requires a ref.watch, but we can if we import it.
    // However, I will use assignmentsAsync to get the supervisor.
    final currentUser = ref.watch(authProvider).user;
    final isWorker = currentUser?.isWorker ?? true;
    final isAdmin = currentUser?.isAdmin ?? false;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Site Details'),
        actions: [
          if (!isWorker)
            IconButton(
              icon: const Icon(Icons.qr_code_2_rounded),
              onPressed: () => context.push('/sites/$siteId/qr'),
            ),
          if (isAdmin)
            IconButton(
              icon: const Icon(Icons.edit_rounded),
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
                    content:
                        Text('Site management available in admin version')));
              },
            ),
        ],
      ),
      body: siteAsync.when(
        data: (site) => SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: AppColors.primarySurface,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    Image.asset('assets/images/logo.png', width: 64, height: 64, fit: BoxFit.contain,
                        errorBuilder: (context, error, stackTrace) => const Icon(Icons.location_city_rounded, size: 48, color: AppColors.primary)),
                    const SizedBox(height: 12),
                    Text('Demo Company', style: AppTypography.caption.copyWith(color: AppColors.primary)),
                    const SizedBox(height: 16),
                    Text(site.name,
                        style: AppTypography.h3
                            .copyWith(color: AppColors.primaryDark),
                        textAlign: TextAlign.center),
                    const SizedBox(height: 8),
                    site.status == 'active'
                        ? StatusBadge.active()
                        : const StatusBadge(
                            label: 'Inactive',
                            color: AppColors.surfaceVariant,
                            textColor: AppColors.textTertiary),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              Text('Location & Team Details',
                  style: AppTypography.h4.copyWith(fontSize: 16)),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.border),
                ),
                child: assignmentsAsync.when(
                  data: (assignments) {
                    final assignedWorkersList = (assignments['workers'] as List?) ?? [];
                    final supervisor = assignedWorkersList.cast<dynamic>().firstWhere(
                      (u) => u.role.value == 'Company Admin' || u.role.value == 'Supervisor',
                      orElse: () => null,
                    );
                    
                    return Column(
                      children: [
                        _buildInfoRow(Icons.map_outlined, 'Address', site.address ?? 'Not specified'),
                        _buildInfoRow(Icons.my_location_rounded, 'Coordinates', '${site.latitude?.toStringAsFixed(6) ?? "N/A"}, ${site.longitude?.toStringAsFixed(6) ?? "N/A"}'),
                        _buildInfoRow(Icons.radar_rounded, 'Geofence Radius', '${site.radius ?? 0} meters'),
                        _buildInfoRow(Icons.groups_rounded, 'Workers Assigned', '${assignedWorkersList.length} workers'),
                        if (supervisor != null) ...[
                          _buildInfoRow(Icons.person_rounded, 'Supervisor Name', supervisor.fullName),
                          _buildInfoRow(Icons.phone_rounded, 'Supervisor Phone', supervisor.phone),
                        ],
                        const SizedBox(height: 8),
                        _buildInfoRow(Icons.business_rounded, 'Company', 'Demo Company'),
                        _buildInfoRow(Icons.support_agent_rounded, 'Office Contact', '03 000 0000'),
                      ],
                    );
                  },
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (_, __) => const Text('Error loading assignments'),
                ),
              ),
              if (!isWorker) ...[
                const SizedBox(height: 24),
                PrimaryButton(
                  text: 'View Site QR Code',
                  icon: Icons.qr_code_rounded,
                  onPressed: () => context.push('/sites/$siteId/qr'),
                ),
                const SizedBox(height: 16),
                OutlinedButton(
                  onPressed: () => _showAssignWorkerDialog(context, ref),
                  style: OutlinedButton.styleFrom(
                    minimumSize: const Size.fromHeight(56),
                    side: const BorderSide(color: AppColors.primary),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16)),
                  ),
                  child: const Text('Assign Worker',
                      style: TextStyle(color: AppColors.primary)),
                ),
              ],
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(
            child: Text('Error: $err',
                style: const TextStyle(color: AppColors.danger))),
      ),
    );
  }

  void _showAssignWorkerDialog(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      constraints:
          BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.8),
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) => Consumer(
        builder: (context, ref, child) {
          final workersAsync = ref.watch(workersListProvider(null));
          final assignmentsAsync = ref.watch(siteAssignmentsProvider(siteId));
          final actionState = ref.watch(siteActionNotifierProvider);

          return Container(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text('Assign Worker', style: AppTypography.h3),
                const SizedBox(height: 16),
                Expanded(
                  child: workersAsync.when(
                    data: (workers) => assignmentsAsync.when(
                      data: (assignments) {
                        final assignedWorkersList =
                            (assignments['workers'] as List?) ?? [];
                        final assignedWorkerIds =
                            assignedWorkersList.map((u) => u.id).toList();

                        return ListView.builder(
                          itemCount: workers.length,
                          itemBuilder: (context, index) {
                            final worker = workers[index];
                            final isAssigned =
                                assignedWorkerIds.contains(worker.id);

                            return ListTile(
                              title: Text(worker.fullName,
                                  style: AppTypography.bodySmall
                                      .copyWith(fontWeight: FontWeight.w600)),
                              subtitle: Text(worker.phone,
                                  style: AppTypography.caption),
                              trailing: actionState.isLoading
                                  ? const SizedBox(
                                      width: 20,
                                      height: 20,
                                      child: CircularProgressIndicator(
                                          strokeWidth: 2))
                                  : isAssigned
                                      ? TextButton(
                                          onPressed: () async {
                                            await ref
                                                .read(siteActionNotifierProvider
                                                    .notifier)
                                                .unassignWorker(
                                                    siteId, worker.id);
                                            if (ctx.mounted) {
                                              ScaffoldMessenger.of(ctx)
                                                  .showSnackBar(const SnackBar(
                                                      content: Text(
                                                          'Worker unassigned'),
                                                      backgroundColor: AppColors
                                                          .surfaceVariant));
                                            }
                                          },
                                          child: const Text('Unassign',
                                              style: TextStyle(
                                                  color: AppColors.danger)),
                                        )
                                      : TextButton(
                                          onPressed: () async {
                                            await ref
                                                .read(siteActionNotifierProvider
                                                    .notifier)
                                                .assignWorker(
                                                    siteId, worker.id);
                                            if (ctx.mounted) {
                                              ScaffoldMessenger.of(ctx)
                                                  .showSnackBar(const SnackBar(
                                                      content: Text(
                                                          'Worker assigned successfully'),
                                                      backgroundColor:
                                                          AppColors.success));
                                            }
                                          },
                                          child: const Text('Assign'),
                                        ),
                            );
                          },
                        );
                      },
                      loading: () =>
                          const Center(child: CircularProgressIndicator()),
                      error: (e, _) =>
                          Center(child: Text('Error loading assignments: $e')),
                    ),
                    loading: () =>
                        const Center(child: CircularProgressIndicator()),
                    error: (e, _) => Center(child: Text('Error: $e')),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 20, color: AppColors.textSecondary),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: AppTypography.caption),
                const SizedBox(height: 2),
                Text(value,
                    style: AppTypography.bodySmall
                        .copyWith(fontWeight: FontWeight.w500)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
