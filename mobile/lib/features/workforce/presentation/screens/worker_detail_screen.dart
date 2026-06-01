import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../providers/worker_providers.dart';

class WorkerDetailScreen extends ConsumerWidget {
  final String userId;
  
  const WorkerDetailScreen({super.key, required this.userId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final workerAsync = ref.watch(workerDetailProvider(userId));
    
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
              if (worker.isPending) StatusBadge.pending() else StatusBadge.approved(),
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
