import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/kpi_card.dart';

/// Payroll Preview Screen (Spec §60/Module 12)
class PayrollPreviewScreen extends StatelessWidget {
  const PayrollPreviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Payroll Preview')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Disclaimer
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: AppColors.infoLight, borderRadius: BorderRadius.circular(12)),
            child: Row(children: [
              const Icon(Icons.info_outline_rounded, color: AppColors.info, size: 20),
              const SizedBox(width: 8),
              Expanded(child: Text('This is an estimate. ConstructPulse does not process payroll.',
                  style: AppTypography.caption.copyWith(color: AppColors.info, fontSize: 12))),
            ]),
          ),
          const SizedBox(height: 20),
          // Estimated Pay
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(gradient: AppColors.successGradient, borderRadius: BorderRadius.circular(20)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Estimated Pay', style: AppTypography.caption.copyWith(color: Colors.white70)),
              const SizedBox(height: 4),
              Text('--', style: AppTypography.h1.copyWith(color: Colors.white, fontSize: 42)),
              Text('Current Month', style: AppTypography.bodySmall.copyWith(color: Colors.white70)),
            ]),
          ),
          const SizedBox(height: 20),
          // KPIs
          GridView.count(crossAxisCount: 2, shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
            crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.5,
            children: [
              const KpiCard(icon: Icons.calendar_today_rounded, value: '--', label: 'Days Worked', iconColor: AppColors.primary),
              const KpiCard(icon: Icons.access_time_rounded, value: '--', label: 'Total Hours', iconColor: AppColors.success),
              const KpiCard(icon: Icons.timer_rounded, value: '--', label: 'Overtime', iconColor: AppColors.secondary),
              const KpiCard(icon: Icons.payments_rounded, value: '--', label: 'Daily Rate', iconColor: AppColors.info),
            ],
          ),
          const SizedBox(height: 24),
          // Breakdown
          Text('Breakdown', style: AppTypography.h4),
          const SizedBox(height: 12),
          const Center(child: Text('No payroll data available yet.')),
        ]),
      ),
    );
  }

}
