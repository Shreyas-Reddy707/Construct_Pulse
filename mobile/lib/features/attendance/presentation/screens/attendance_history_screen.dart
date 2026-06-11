import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../providers/attendance_providers.dart';
import '../../domain/entities/attendance.dart';
import '../../../../core/constants/enums.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../workforce/presentation/providers/worker_providers.dart';

/// Attendance History Screen
class AttendanceHistoryScreen extends ConsumerStatefulWidget {
  final String? workerId;
  final String? initialFilter;
  const AttendanceHistoryScreen({super.key, this.workerId, this.initialFilter});

  @override
  ConsumerState<AttendanceHistoryScreen> createState() => _AttendanceHistoryScreenState();
}

class _AttendanceHistoryScreenState extends ConsumerState<AttendanceHistoryScreen> {
  late String _filter;
  String? _selectedWorkerId;
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _filter = widget.initialFilter ?? 'All Time';
    _selectedWorkerId = widget.workerId;
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authProvider.select((s) => s.user));
    final isAdmin = user?.isAdmin ?? false;
    
    AsyncValue<List<Attendance>> historyAsync;
    
    if (isAdmin && widget.workerId == null) {
      if (_selectedWorkerId == null) {
        historyAsync = ref.watch(companyAttendanceHistoryProvider);
      } else {
        historyAsync = ref.watch(workerAttendanceHistoryProvider(_selectedWorkerId!));
      }
    } else {
      final targetUserId = widget.workerId ?? user?.id;
      if (targetUserId == user?.id) {
        historyAsync = ref.watch(attendanceHistoryProvider);
      } else if (targetUserId != null) {
        historyAsync = ref.watch(workerAttendanceHistoryProvider(targetUserId));
      } else {
        historyAsync = const AsyncValue.data(<Attendance>[]);
      }
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Attendance History')),
      body: Column(
        children: [
          // Search Bar
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              onChanged: (val) {
                setState(() {
                  _searchQuery = val.toLowerCase();
                });
              },
              decoration: const InputDecoration(
                hintText: 'Search history...',
                prefixIcon: Icon(Icons.search_rounded, size: 20),
              ),
            ),
          ),
          // Filter Chips
          SizedBox(
            height: 40,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              children: [
                _filterChip('All Time', _filter == 'All Time', () => setState(() => _filter = 'All Time')),
                _filterChip('Today', _filter == 'Today', () => setState(() => _filter = 'Today')),
                _filterChip('Completed Today', _filter == 'Completed Today', () => setState(() => _filter = 'Completed Today')),
                _filterChip('This Month', _filter == 'This Month', () => setState(() => _filter = 'This Month')),
                _filterChip('Last Month', _filter == 'Last Month', () => setState(() => _filter = 'Last Month')),
              ],
            ),
          ),
          if (isAdmin && widget.workerId == null)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: ref.watch(workersListProvider(null)).when(
                data: (workers) {
                  if (workers.isEmpty) return const SizedBox();
                  return DropdownButton<String>(
                    isExpanded: true,
                    hint: const Text('Select Worker'),
                    value: _selectedWorkerId,
                    items: [
                      const DropdownMenuItem<String>(
                        child: Text('All Workers'),
                      ),
                      ...workers.map((w) => DropdownMenuItem<String>(
                            value: w.id,
                            child: Text(w.fullName),
                          )),
                    ],
                    onChanged: (val) {
                      setState(() {
                        _selectedWorkerId = val;
                      });
                    },
                  );
                },
                loading: () => const LinearProgressIndicator(),
                error: (_, __) => const SizedBox(),
              ),
            ),
          const SizedBox(height: 8),
          // List
          Expanded(
            child: historyAsync.when(
              data: (records) {
                var filtered = records;
                
                // Date filtering
                if (_filter == 'Today') {
                  final now = DateTime.now();
                  filtered = filtered.where((r) => r.checkInTime.year == now.year && r.checkInTime.month == now.month && r.checkInTime.day == now.day).toList();
                } else if (_filter == 'Completed Today') {
                  final now = DateTime.now();
                  filtered = filtered.where((r) => r.checkOutTime != null && r.checkInTime.year == now.year && r.checkInTime.month == now.month && r.checkInTime.day == now.day).toList();
                } else if (_filter == 'This Month') {
                  final now = DateTime.now();
                  filtered = filtered.where((r) => r.checkInTime.month == now.month && r.checkInTime.year == now.year).toList();
                } else if (_filter == 'Last Month') {
                  final now = DateTime.now();
                  final lastMonth = now.month == 1 ? 12 : now.month - 1;
                  final year = now.month == 1 ? now.year - 1 : now.year;
                  filtered = filtered.where((r) => r.checkInTime.month == lastMonth && r.checkInTime.year == year).toList();
                }

                // Text search filtering
                if (_searchQuery.isNotEmpty) {
                  final q = _searchQuery;
                  filtered = filtered.where((r) =>
                      (r.userName?.toLowerCase().contains(q) ?? false) ||
                      (r.contractorName?.toLowerCase().contains(q) ?? false) ||
                      (r.companyName?.toLowerCase().contains(q) ?? false) ||
                      (r.siteName?.toLowerCase().contains(q) ?? false) ||
                      (r.departmentName?.toLowerCase().contains(q) ?? false)
                  ).toList();
                }

                if (filtered.isEmpty) {
                  return const Center(child: Text('No attendance records found.'));
                }
                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: filtered.length,
                  itemBuilder: (ctx, i) => _attendanceItem(filtered[i]),
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
    final dateStr = DateFormat('dd Jun yyyy').format(record.checkInTime);
    final checkInStr = DateFormat('HH:mm').format(record.checkInTime);
    final checkOutStr = record.checkOutTime != null ? DateFormat('HH:mm').format(record.checkOutTime!) : 'Active';
    
    String hoursWorked = '--';
    if (record.checkOutTime != null) {
      final diff = record.checkOutTime!.difference(record.checkInTime);
      hoursWorked = '${(diff.inMinutes / 60).toStringAsFixed(1)}h';
    } else {
      hoursWorked = 'On Site';
    }

    final workerName = record.userName ?? 'Unknown Worker';
    final contractorName = record.contractorName ?? record.companyName ?? 'Unknown Company';
    final siteName = record.siteName ?? 'Unknown Site';

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(workerName, style: AppTypography.body.copyWith(fontWeight: FontWeight.w700)),
              record.status == AttendanceStatus.checkedIn ? StatusBadge.checkedIn() : StatusBadge.checkedOut(),
            ],
          ),
          const SizedBox(height: 8),
          Text(contractorName, style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary)),
          Text(siteName, style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary)),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(dateStr, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
              Text('$checkInStr → $checkOutStr', style: AppTypography.bodySmall),
              Text(hoursWorked, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
            ],
          ),
        ],
      ),
    );
  }
}
