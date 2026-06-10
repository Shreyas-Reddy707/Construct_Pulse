import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../../core/theme/app_colors.dart';
import '../providers/attendance_providers.dart';

class LiveAttendanceScreen extends ConsumerWidget {
  final String? siteId;
  const LiveAttendanceScreen({super.key, this.siteId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final liveAsync = ref.watch(liveAttendanceProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Live Attendance')),
      body: liveAsync.when(
        data: (attendance) {
          final filteredAttendance = siteId != null
              ? attendance.where((a) => a.siteId == siteId).toList()
              : attendance;

          if (filteredAttendance.isEmpty) {
            return const Center(child: Text('No active workers on site right now.'));
          }
          return RefreshIndicator(
            onRefresh: () async => ref.refresh(liveAttendanceProvider),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: filteredAttendance.length,
              itemBuilder: (context, index) {
                final record = filteredAttendance[index];
                final duration = DateTime.now().difference(record.checkInTime);
                final decimalHours = duration.inMinutes / 60.0;
                final durationStr = '${decimalHours.toStringAsFixed(1)}h';
                
                final workerName = record.userName ?? 'Unknown Worker';
                final departmentName = record.departmentName ?? 'General Worker';
                final contractorName = record.contractorName ?? record.companyName ?? 'Unknown Contractor';
                final siteName = record.siteName ?? 'Unknown Site';
                final checkInStr = DateFormat.jm().format(record.checkInTime);

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(workerName, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        const SizedBox(height: 8),
                        Text(departmentName, style: const TextStyle(color: AppColors.textSecondary)),
                        Text(contractorName, style: const TextStyle(color: AppColors.textSecondary)),
                        Text(siteName, style: const TextStyle(color: AppColors.textSecondary)),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text('Checked In: $checkInStr'),
                            Text('Duration: $durationStr'),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: AppColors.success.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Text('ACTIVE', style: TextStyle(color: AppColors.success, fontWeight: FontWeight.bold, fontSize: 12)),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(child: Text('Error: $err')),
      ),
    );
  }
}
