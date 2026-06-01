import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';

/// Reports Screen (Spec §83)
class ReportsScreen extends StatelessWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final reportTypes = [
      {'title': 'Attendance Report', 'icon': Icons.access_time_rounded, 'color': AppColors.primary, 'desc': 'Daily/weekly/monthly attendance'},
      {'title': 'Occupancy Report', 'icon': Icons.groups_rounded, 'color': AppColors.success, 'desc': 'Workforce presence data'},
      {'title': 'Planned vs Actual', 'icon': Icons.compare_arrows_rounded, 'color': AppColors.secondary, 'desc': 'Variance analysis'},
      {'title': 'Emergency Report', 'icon': Icons.emergency_rounded, 'color': AppColors.danger, 'desc': 'Muster & incident data'},
      {'title': 'Contractor Report', 'icon': Icons.engineering_rounded, 'color': AppColors.info, 'desc': 'Contractor workforce summary'},
      {'title': 'Department Report', 'icon': Icons.business_rounded, 'color': AppColors.warning, 'desc': 'Department-wise analytics'},
      {'title': 'Payroll Preview', 'icon': Icons.payments_rounded, 'color': AppColors.success, 'desc': 'Hours & earnings estimate'},
      {'title': 'Inspection Report', 'icon': Icons.fact_check_rounded, 'color': AppColors.primary, 'desc': 'Municipality compliance'},
    ];

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Reports')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Recent reports
          Text('Generate Report', style: AppTypography.h4),
          const SizedBox(height: 12),
          ...reportTypes.map((r) => Container(
            margin: const EdgeInsets.only(bottom: 10),
            decoration: BoxDecoration(
              color: AppColors.surface, borderRadius: BorderRadius.circular(14),
              border: Border.all(color: AppColors.border),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              leading: Container(
                width: 44, height: 44,
                decoration: BoxDecoration(
                  color: (r['color'] as Color).withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(r['icon'] as IconData, color: r['color'] as Color, size: 22),
              ),
              title: Text(r['title'] as String, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
              subtitle: Text(r['desc'] as String, style: AppTypography.caption.copyWith(fontSize: 12)),
              trailing: const Icon(Icons.chevron_right_rounded, color: AppColors.textTertiary),
              onTap: () => _showGenerateSheet(context, r['title'] as String),
            ),
          )),
        ],
      ),
    );
  }

  void _showGenerateSheet(BuildContext context, String title) {
    showModalBottomSheet(context: context, builder: (ctx) => Padding(
      padding: const EdgeInsets.all(24),
      child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Generate $title', style: AppTypography.h4),
        const SizedBox(height: 16),
        Text('Format', style: AppTypography.label),
        const SizedBox(height: 8),
        Row(children: [
          _formatChip('PDF', true), const SizedBox(width: 8),
          _formatChip('Excel', false), const SizedBox(width: 8),
          _formatChip('CSV', false),
        ]),
        const SizedBox(height: 24),
        PrimaryButton(text: 'Generate', icon: Icons.download_rounded, onPressed: () => Navigator.pop(ctx)),
      ]),
    ));
  }

  Widget _formatChip(String label, bool sel) => ChoiceChip(
    label: Text(label), selected: sel, onSelected: (_) {},
    selectedColor: AppColors.primarySurface,
  );
}
