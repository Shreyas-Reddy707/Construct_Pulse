import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/kpi_card.dart';
import '../providers/occupancy_providers.dart';
import '../../domain/entities/occupancy_stats.dart';

/// Site Manager Dashboard (Spec §75)
class ManagerDashboardScreen extends ConsumerWidget {
  final String siteId = 'S-12345'; // Default site for this demo

  const ManagerDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final occupancyAsync = ref.watch(occupancyStatsProvider(siteId));

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _header(context),
              const SizedBox(height: 20),
              
              occupancyAsync.when(
                data: (stats) => Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _occupancyBanner(stats.totalWorkers),
                    const SizedBox(height: 20),
                    Text('Workforce Overview', style: AppTypography.h4),
                    const SizedBox(height: 12),
                    _kpiGrid(stats),
                    const SizedBox(height: 24),
                    _varianceCard(context, stats.plannedVsActual),
                    const SizedBox(height: 24),
                    _deptBreakdown(stats.departmentBreakdown),
                    const SizedBox(height: 24),
                    _contractorChart(stats.contractorBreakdown),
                    const SizedBox(height: 80),
                  ],
                ),
                loading: () => const Center(
                  child: Padding(
                    padding: EdgeInsets.all(32.0),
                    child: CircularProgressIndicator(),
                  ),
                ),
                error: (err, _) => Center(
                  child: Padding(
                    padding: const EdgeInsets.all(32.0),
                    child: Text('Failed to load dashboard: $err', style: const TextStyle(color: AppColors.danger)),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _header(BuildContext context) => Row(children: [
    Container(
      width: 48, height: 48,
      decoration: BoxDecoration(gradient: AppColors.primaryGradient, borderRadius: BorderRadius.circular(14)),
      child: const Icon(Icons.dashboard_rounded, color: Colors.white, size: 24),
    ),
    const SizedBox(width: 12),
    Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text('Site Manager', style: AppTypography.caption.copyWith(fontSize: 12)),
      Text('Site Dashboard', style: AppTypography.h4),
    ])),
    IconButton(onPressed: () {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Coming in v1.1')));
    }, icon: const Badge(smallSize: 8, child: Icon(Icons.notifications_outlined))),
  ]);

  Widget _occupancyBanner(int totalWorkers) => Container(
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(
      gradient: AppColors.primaryGradient,
      borderRadius: BorderRadius.circular(20),
      boxShadow: [BoxShadow(color: AppColors.primary.withValues(alpha: 0.3), blurRadius: 20, offset: const Offset(0, 8))],
    ),
    child: Row(children: [
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Live Occupancy', style: AppTypography.caption.copyWith(color: Colors.white70, fontSize: 12)),
        const SizedBox(height: 4),
        Text('$totalWorkers', style: AppTypography.h1.copyWith(color: Colors.white, fontSize: 48)),
        Text('workers on site', style: AppTypography.bodySmall.copyWith(color: Colors.white70)),
      ])),
      Container(
        width: 80, height: 80,
        decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.15), borderRadius: BorderRadius.circular(20)),
        child: const Icon(Icons.groups_rounded, color: Colors.white, size: 40),
      ),
    ]),
  );

  Widget _kpiGrid(OccupancyStats stats) {
    final shortage = stats.totalWorkers - stats.expectedWorkers;
    return GridView.count(
      crossAxisCount: 2, shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
      crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.4,
      children: [
        KpiCard(icon: Icons.groups_rounded, value: '${stats.totalWorkers}', label: 'Present', iconColor: AppColors.success),
        KpiCard(icon: Icons.trending_up, value: '${stats.expectedWorkers}', label: 'Expected', iconColor: AppColors.primary),
        KpiCard(
          icon: Icons.warning_rounded, 
          value: '$shortage', 
          label: shortage < 0 ? 'Shortage' : 'Surplus', 
          iconColor: shortage < 0 ? AppColors.danger : AppColors.success
        ),
        KpiCard(icon: Icons.assignment_rounded, value: '${stats.openTasks}', label: 'Open Tasks', iconColor: AppColors.secondary),
      ],
    );
  }

  Widget _varianceCard(BuildContext context, List<VarianceRecord> varianceRecords) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: AppColors.surface, borderRadius: BorderRadius.circular(16),
      border: Border.all(color: AppColors.border),
    ),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
        Text('Planned vs Actual', style: AppTypography.h4.copyWith(fontSize: 16)),
        TextButton(onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Coming in v1.1')));
        }, child: const Text('Details')),
      ]),
      const SizedBox(height: 12),
      if (varianceRecords.isEmpty)
        const Padding(
          padding: EdgeInsets.all(8.0),
          child: Text('No variance data available.'),
        ),
      ...varianceRecords.map((v) => _varianceRow(v.departmentName, v.planned, v.actual)),
    ]),
  );

  Widget _varianceRow(String dept, int planned, int actual) {
    final diff = actual - planned;
    final color = diff >= 0 ? AppColors.success : AppColors.danger;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(children: [
        Expanded(flex: 3, child: Text(dept, style: AppTypography.bodySmall, maxLines: 1, overflow: TextOverflow.ellipsis)),
        Expanded(child: Text('$planned', style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary), textAlign: TextAlign.center)),
        Expanded(child: Text('$actual', style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600), textAlign: TextAlign.center)),
        Expanded(child: Text('${diff >= 0 ? '+' : ''}$diff', style: AppTypography.bodySmall.copyWith(color: color, fontWeight: FontWeight.w600), textAlign: TextAlign.right)),
      ]),
    );
  }

  Widget _deptBreakdown(List<DepartmentOccupancy> breakdown) {
    // Generate dynamic colors for the breakdown
    final colors = [AppColors.primary, AppColors.secondary, AppColors.success, AppColors.info, AppColors.warning, AppColors.danger];
    
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text('Department Breakdown', style: AppTypography.h4),
      const SizedBox(height: 12),
      if (breakdown.isEmpty)
        const Text('No department data available.'),
      ...breakdown.asMap().entries.map((entry) {
        final i = entry.key;
        final d = entry.value;
        final color = colors[i % colors.length];
        return Container(
          margin: const EdgeInsets.only(bottom: 8),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(12), border: Border.all(color: AppColors.border)),
          child: Row(children: [
            Container(width: 4, height: 32, decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(2))),
            const SizedBox(width: 12),
            Expanded(child: Text(d.departmentName, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w500))),
            Text('${d.count}', style: AppTypography.h4.copyWith(fontSize: 18)),
            const SizedBox(width: 4),
            Text('workers', style: AppTypography.caption.copyWith(fontSize: 11)),
          ]),
        );
      }),
    ]);
  }
  
  Widget _contractorChart(List<ContractorOccupancy> breakdown) {
    if (breakdown.isEmpty) return const SizedBox();
    
    // Using fl_chart to render a PieChart for contractors
    final colors = [AppColors.secondary, AppColors.primary, AppColors.info, AppColors.success, AppColors.warning];
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface, borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Contractor Distribution', style: AppTypography.h4.copyWith(fontSize: 16)),
          const SizedBox(height: 24),
          SizedBox(
            height: 200,
            child: PieChart(
              PieChartData(
                sectionsSpace: 2,
                centerSpaceRadius: 40,
                sections: breakdown.asMap().entries.map((entry) {
                  final i = entry.key;
                  final c = entry.value;
                  return PieChartSectionData(
                    color: colors[i % colors.length],
                    value: c.count.toDouble(),
                    title: '${c.count}',
                    radius: 50,
                    titleStyle: AppTypography.bodySmall.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
                  );
                }).toList(),
              ),
            ),
          ),
          const SizedBox(height: 24),
          Wrap(
            spacing: 12,
            runSpacing: 8,
            children: breakdown.asMap().entries.map((entry) {
              final i = entry.key;
              final c = entry.value;
              return Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(width: 12, height: 12, decoration: BoxDecoration(color: colors[i % colors.length], shape: BoxShape.circle)),
                  const SizedBox(width: 4),
                  Text(c.contractorName, style: AppTypography.caption),
                ],
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
