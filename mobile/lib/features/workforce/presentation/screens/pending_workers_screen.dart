import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/pending_workers_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';

class PendingWorkersScreen extends ConsumerWidget {
  const PendingWorkersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pendingWorkersAsync = ref.watch(pendingWorkersProvider);
    final actionState = ref.watch(workerActionNotifierProvider);

    ref.listen<AsyncValue<void>>(workerActionNotifierProvider, (_, state) {
      state.whenOrNull(
        error: (error, stackTrace) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(error.toString()),
              backgroundColor: AppColors.danger,
            ),
          );
        },
        data: (_) {
          if (!state.isLoading && !state.hasError && state.hasValue) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Action successful'),
              ),
            );
          }
        },
      );
    });

    return Scaffold(
      appBar: AppBar(
        title: const Text('Pending Workers'),
      ),
      body: pendingWorkersAsync.when(
        data: (workers) {
          if (workers.isEmpty) {
            return const Center(
              child: Text('No pending workers.'),
            );
          }
          return Stack(
            children: [
              RefreshIndicator(
                onRefresh: () async {
                  return ref.refresh(pendingWorkersProvider.future);
                },
                child: ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: workers.length,
                  itemBuilder: (context, index) {
                    final worker = workers[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                        side: const BorderSide(color: AppColors.border),
                      ),
                      elevation: 0,
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                CircleAvatar(
                                  radius: 24,
                                  backgroundColor: AppColors.primaryLight,
                                  backgroundImage: worker.profilePhoto != null ? NetworkImage(worker.profilePhoto!) : null,
                                  child: worker.profilePhoto == null
                                      ? Text(worker.initials, style: AppTypography.bodySmall.copyWith(color: AppColors.primaryDark))
                                      : null,
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(worker.fullName, style: AppTypography.h3),
                                      const SizedBox(height: 4),
                                      Text(worker.phone, style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary)),
                                      if (worker.role.value.isNotEmpty)
                                        Container(
                                          margin: const EdgeInsets.only(top: 8),
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(color: AppColors.surfaceVariant, borderRadius: BorderRadius.circular(8)),
                                          child: Text('Role: ${worker.role.value}', style: AppTypography.caption.copyWith(fontWeight: FontWeight.w600)),
                                        ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                            const Padding(padding: EdgeInsets.symmetric(vertical: 12), child: Divider(height: 1)),
                            _infoRow(Icons.business, 'Company', worker.companyName ?? 'Demo Company'),
                            if (worker.departmentName != null) _infoRow(Icons.domain, 'Department', worker.departmentName!),
                            if (worker.contractorName != null) _infoRow(Icons.handyman, 'Contractor', worker.contractorName!),
                            if (worker.emergencyContactName != null) 
                              _infoRow(Icons.emergency, 'Emergency Contact', '${worker.emergencyContactName} (${worker.emergencyContactPhone ?? ''})'),
                            if (worker.createdAt != null) 
                              _infoRow(Icons.calendar_today, 'Applied Date', worker.createdAt.toString().split(' ')[0]),
                            if (worker.assignedSiteNames != null && worker.assignedSiteNames!.isNotEmpty) 
                              _infoRow(Icons.location_on, 'Assigned Sites', worker.assignedSiteNames!),
                            const SizedBox(height: 16),
                            Row(
                              children: [
                                Expanded(
                                  child: OutlinedButton(
                                    onPressed: actionState.isLoading ? null : () => ref.read(workerActionNotifierProvider.notifier).reject(worker.id),
                                    style: OutlinedButton.styleFrom(
                                      foregroundColor: AppColors.danger,
                                      side: const BorderSide(color: AppColors.danger),
                                    ),
                                    child: const Text('Reject'),
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: PrimaryButton(
                                    text: 'Approve',
                                    onPressed: actionState.isLoading ? null : () => ref.read(workerActionNotifierProvider.notifier).approve(worker.id),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
              if (actionState.isLoading)
                const Positioned.fill(
                  child: DecoratedBox(
                    decoration: BoxDecoration(color: Colors.black26),
                    child: Center(
                      child: CircularProgressIndicator(),
                    ),
                  ),
                ),
            ],
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }

  Widget _infoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 16, color: AppColors.textTertiary),
          const SizedBox(width: 8),
          Expanded(
            child: RichText(
              text: TextSpan(
                style: AppTypography.bodySmall,
                children: [
                  TextSpan(text: '$label: ', style: const TextStyle(color: AppColors.textTertiary)),
                  TextSpan(text: value, style: const TextStyle(color: AppColors.textPrimary)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
