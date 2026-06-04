import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/worker_providers.dart';
import '../providers/pending_workers_provider.dart';
import '../../../attendance/presentation/providers/attendance_providers.dart';
import '../../../../core/constants/enums.dart';
import 'package:intl/intl.dart';

class WorkerDetailScreen extends ConsumerWidget {
  final String userId;
  
  const WorkerDetailScreen({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final workerAsync = ref.watch(workerDetailProvider(userId));
    final actionState = ref.watch(workerActionNotifierProvider);

    ref.listen<AsyncValue<void>>(workerActionNotifierProvider, (_, state) {
      state.whenOrNull(
        error: (error, stackTrace) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(error.toString()), backgroundColor: AppColors.danger),
          );
        },
        data: (_) {
          if (!state.isLoading && !state.hasError && state.hasValue) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Action successful')),
            );
            ref.invalidate(workerDetailProvider(userId));
          }
        },
      );
    });
    
    return Scaffold(
      appBar: AppBar(title: const Text('Worker Profile')),
      body: workerAsync.when(
        data: (worker) => SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              CircleAvatar(
                radius: 40,
                backgroundColor: AppColors.primarySurface,
                backgroundImage: worker.profilePhoto != null ? NetworkImage(worker.profilePhoto!) : null,
                child: worker.profilePhoto == null
                    ? Text(worker.initials, style: AppTypography.h3.copyWith(color: AppColors.primary))
                    : null,
              ),
              const SizedBox(height: 16),
              Text(worker.fullName, style: AppTypography.h3),
              const SizedBox(height: 4),
              if (worker.isPending) StatusBadge.pending()
              else if (worker.isRejected) StatusBadge.rejected()
              else if (worker.isSuspended) StatusBadge.suspended()
              else StatusBadge.approved(),
              const SizedBox(height: 24),
              _buildSection('Work Information', [
                _buildInfoRow(Icons.badge_outlined, 'Employee ID', worker.employeeId ?? 'N/A'),
                _buildInfoRow(Icons.work_outline, 'Designation', worker.designation ?? 'N/A'),
                _buildInfoRow(Icons.business_outlined, 'Department', worker.departmentName ?? 'N/A'),
                _buildInfoRow(Icons.apartment_outlined, 'Contractor', worker.contractorName ?? 'N/A'),
              ]),
              const SizedBox(height: 16),
              _buildSection('Contact Information', [
                _buildInfoRow(Icons.phone_outlined, 'Phone', worker.phone),
                _buildInfoRow(Icons.emergency_outlined, 'Emergency Contact', '${worker.emergencyContactName ?? 'N/A'} (${worker.emergencyContactPhone ?? 'N/A'})'),
              ]),
              const SizedBox(height: 24),
              if (worker.isPending) ...[
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton(
                        onPressed: actionState.isLoading ? null : () => ref.read(workerActionNotifierProvider.notifier).reject(worker.id),
                        style: OutlinedButton.styleFrom(foregroundColor: AppColors.danger, side: const BorderSide(color: AppColors.danger)),
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
              ] else if (worker.isApproved) ...[
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: actionState.isLoading ? null : () => ref.read(workerActionNotifierProvider.notifier).suspend(worker.id),
                    style: OutlinedButton.styleFrom(foregroundColor: AppColors.danger, side: const BorderSide(color: AppColors.danger)),
                    child: const Text('Suspend Worker'),
                  ),
                ),
              ] else if (worker.isSuspended) ...[
                SizedBox(
                  width: double.infinity,
                  child: PrimaryButton(
                    text: 'Reactivate Worker',
                    onPressed: actionState.isLoading ? null : () => ref.read(workerActionNotifierProvider.notifier).reactivate(worker.id),
                  ),
                ),
              ],
              const SizedBox(height: 24),
              _buildSection('Assigned Sites', [
                ref.watch(workerSitesProvider(userId)).when(
                  data: (sites) => sites.isEmpty
                      ? const Padding(padding: EdgeInsets.all(8.0), child: Text('No assigned sites'))
                      : Column(
                          children: sites.map((site) => ListTile(
                            leading: const Icon(Icons.location_on_rounded, color: AppColors.secondary),
                            title: Text(site.name),
                            subtitle: Text(site.status ?? 'Active'),
                          )).toList(),
                        ),
                  loading: () => const CircularProgressIndicator(),
                  error: (e, _) => Text('Error: $e'),
                )
              ]),
              const SizedBox(height: 16),
              _buildSection('Recent Attendance', [
                ref.watch(workerAttendanceHistoryProvider(userId)).when(
                  data: (attendance) {
                    if (attendance.isEmpty) return const Padding(padding: EdgeInsets.all(8.0), child: Text('No recent attendance'));
                    final recent = attendance.take(5).toList();
                    return Column(
                      children: recent.map((a) => ListTile(
                        leading: Icon(a.status == AttendanceStatus.checkedIn ? Icons.login_rounded : Icons.logout_rounded, color: a.status == AttendanceStatus.checkedIn ? AppColors.success : AppColors.surfaceVariant),
                        title: Text(a.status == AttendanceStatus.checkedIn ? 'Checked In' : 'Checked Out'),
                        subtitle: Text(DateFormat('MMM dd, yyyy - hh:mm a').format(a.checkInTime)),
                      )).toList(),
                    );
                  },
                  loading: () => const CircularProgressIndicator(),
                  error: (e, _) => Text('Error: $e'),
                )
              ]),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: AppColors.danger))),
      ),
    );
  }

  Widget _buildSection(String title, List<Widget> children) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: AppTypography.h4.copyWith(fontSize: 16)),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.border),
          ),
          child: Column(
            children: children,
          ),
        ),
      ],
    );
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
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
                Text(value, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w500)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
