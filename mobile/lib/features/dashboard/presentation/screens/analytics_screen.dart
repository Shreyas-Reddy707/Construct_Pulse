import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';

class AnalyticsScreen extends StatelessWidget {
  const AnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Analytics & Reporting')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildAnalyticsCard(
            context,
            'Department Analytics',
            'View workforce distribution and attendance by department',
            Icons.business_rounded,
          ),
          const SizedBox(height: 16),
          _buildAnalyticsCard(
            context,
            'Contractor Analytics',
            'Track contractor performance and compliance metrics',
            Icons.handshake_rounded,
          ),
          const SizedBox(height: 16),
          _buildAnalyticsCard(
            context,
            'Worker Analytics',
            'Detailed individual performance and hours tracking',
            Icons.person_search_rounded,
          ),
          const SizedBox(height: 32),
          Text('Data Export', style: AppTypography.h4),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: PrimaryButton(
                  text: 'Export CSV',
                  icon: Icons.table_chart_rounded,
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('CSV Export initiated...')));
                  },
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: OutlinedButton(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('PDF Export initiated...')));
                  },
                  child: const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.picture_as_pdf_rounded),
                      SizedBox(width: 8),
                      Text('Export PDF'),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildAnalyticsCard(BuildContext context, String title, String subtitle, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.primarySurface,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: AppColors.primary),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTypography.h4.copyWith(fontSize: 16)),
                const SizedBox(height: 4),
                Text(subtitle, style: AppTypography.caption),
              ],
            ),
          ),
          const Icon(Icons.chevron_right_rounded, color: AppColors.textSecondary),
        ],
      ),
    );
  }
}
