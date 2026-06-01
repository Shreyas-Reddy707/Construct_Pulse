import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/kpi_card.dart';

/// Occupancy Dashboard Screen (Spec §33/§73)
class OccupancyDashboardScreen extends StatelessWidget {
  const OccupancyDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Live Occupancy')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Live count banner
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(gradient: AppColors.primaryGradient, borderRadius: BorderRadius.circular(20)),
            child: Row(children: [
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Current Workers', style: AppTypography.caption.copyWith(color: Colors.white70)),
                Text('--', style: AppTypography.h1.copyWith(color: Colors.white, fontSize: 52)),
                Text('Active Site', style: AppTypography.bodySmall.copyWith(color: Colors.white70)),
              ])),
              Container(
                width: 64, height: 64,
                decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.15), borderRadius: BorderRadius.circular(16)),
                child: const Icon(Icons.people_rounded, color: Colors.white, size: 32),
              ),
            ]),
          ),
          const SizedBox(height: 20),
          // KPIs
          GridView.count(crossAxisCount: 2, shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
            crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.5,
            children: [
              const KpiCard(icon: Icons.groups_rounded, value: '--', label: 'Departments', iconColor: AppColors.primary),
              const KpiCard(icon: Icons.engineering_rounded, value: '--', label: 'Contractors', iconColor: AppColors.secondary),
              const KpiCard(icon: Icons.login_rounded, value: '--', label: 'Check-Ins Today', iconColor: AppColors.success),
              const KpiCard(icon: Icons.logout_rounded, value: '--', label: 'Check-Outs', iconColor: AppColors.warning),
            ],
          ),
          const SizedBox(height: 24),
          // Department breakdown
          Text('By Department', style: AppTypography.h4),
          const SizedBox(height: 12),
          const Center(child: Text('No department data available.')),
          const SizedBox(height: 24),
          // Contractor breakdown
          Text('By Contractor', style: AppTypography.h4),
          const SizedBox(height: 12),
          const Center(child: Text('No contractor data available.')),
        ]),
      ),
    );
  }

}
