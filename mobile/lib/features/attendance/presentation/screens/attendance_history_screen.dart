import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../providers/attendance_providers.dart';
import '../../domain/entities/attendance.dart';
import '../../../../core/constants/enums.dart';

/// Attendance History Screen
class AttendanceHistoryScreen extends ConsumerStatefulWidget {
  const AttendanceHistoryScreen({super.key});

  @override
  ConsumerState<AttendanceHistoryScreen> createState() => _AttendanceHistoryScreenState();
}

class _AttendanceHistoryScreenState extends ConsumerState<AttendanceHistoryScreen> {
  String _filter = 'This Month';

  @override
  Widget build(BuildContext context) {
    final historyAsync = ref.watch(attendanceHistoryProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Attendance History')),
      body: Column(
        children: [
          // Summary Card
          Container(
            margin: const EdgeInsets.all(16),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.surface, borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppColors.border),
            ),
            child: Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
              _summaryItem('Days', '24', AppColors.primary),
              _divider(),
              _summaryItem('Hours', '208', AppColors.success),
              _divider(),
              _summaryItem('Overtime', '12h', AppColors.secondary),
            ]),
          ),
          // Filter Chips
          SizedBox(
            height: 40,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              children: [
                _filterChip('This Month', _filter == 'This Month', () => setState(() => _filter = 'This Month')),
                _filterChip('Last Month', _filter == 'Last Month', () => setState(() => _filter = 'Last Month')),
                _filterChip('Custom', _filter == 'Custom', () => setState(() => _filter = 'Custom')),
              ],
            ),
          ),
          const SizedBox(height: 8),
          // List
          Expanded(
            child: historyAsync.when(
              data: (history) {
                if (history.isEmpty) {
                  return const Center(child: Text('No attendance records found.'));
                }
                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: history.length,
                  itemBuilder: (ctx, i) => _attendanceItem(history[i]),
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: AppColors.danger))),
            ),
          ),
        ],
      ),
    );
  }

  Widget _summaryItem(String label, String value, Color color) {
    return Column(children: [
      Text(value, style: AppTypography.h3.copyWith(color: color)),
      const SizedBox(height: 4),
      Text(label, style: AppTypography.caption.copyWith(fontSize: 12)),
    ]);
  }

  Widget _divider() => Container(width: 1, height: 40, color: AppColors.border);

  Widget _filterChip(String label, bool selected, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: FilterChip(
        label: Text(label),
        selected: selected,
        onSelected: (_) => onTap(),
        selectedColor: AppColors.primarySurface,
        checkmarkColor: AppColors.primary,
      ),
    );
  }

  Widget _attendanceItem(Attendance record) {
    final dateStr = DateFormat('MMM dd, yyyy').format(record.checkInTime);
    final isToday = DateFormat('yyyy-MM-dd').format(record.checkInTime) == DateFormat('yyyy-MM-dd').format(DateTime.now());
    
    final checkInStr = DateFormat('HH:mm').format(record.checkInTime);
    final checkOutStr = record.checkOutTime != null ? DateFormat('HH:mm').format(record.checkOutTime!) : '--:--';
    
    String hoursWorked = '--';
    if (record.checkOutTime != null) {
      final diff = record.checkOutTime!.difference(record.checkInTime);
      hoursWorked = '${(diff.inMinutes / 60).toStringAsFixed(1)}h';
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.surface, borderRadius: BorderRadius.circular(12),
        border: Border.all(color: isToday ? AppColors.primary.withValues(alpha: 0.3) : AppColors.border),
      ),
      child: Row(children: [
        Container(
          width: 44, height: 44,
          decoration: BoxDecoration(
            color: isToday ? AppColors.primarySurface : AppColors.surfaceVariant,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Center(child: Text(DateFormat('dd').format(record.checkInTime), style: AppTypography.bodySmall.copyWith(
            fontWeight: FontWeight.w700,
            color: isToday ? AppColors.primary : AppColors.textSecondary,
          ))),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(isToday ? 'Today' : dateStr, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
          const SizedBox(height: 2),
          Text('$checkInStr → $checkOutStr', style: AppTypography.caption.copyWith(fontSize: 12)),
        ])),
        Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text(hoursWorked, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
          const SizedBox(height: 2),
          record.status == AttendanceStatus.checkedIn ? StatusBadge.checkedIn() : StatusBadge.checkedOut(),
        ]),
      ]),
    );
  }
}
