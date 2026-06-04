import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../../core/theme/app_colors.dart';
import '../providers/attendance_providers.dart';

class LiveAttendanceScreen extends ConsumerWidget {
  const LiveAttendanceScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final liveAsync = ref.watch(liveAttendanceProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Live Attendance')),
      body: liveAsync.when(
        data: (attendance) {
          if (attendance.isEmpty) {
            return const Center(child: Text('No active workers on site right now.'));
          }
          return RefreshIndicator(
            onRefresh: () async => ref.refresh(liveAttendanceProvider),
            child: ListView.separated(
              itemCount: attendance.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final record = attendance[index];
                return ListTile(
                  leading: const CircleAvatar(
                    backgroundColor: AppColors.primarySurface,
                    child: Icon(Icons.person_rounded, color: AppColors.primary),
                  ),
                  title: Text(record.userName ?? 'Unknown Worker'),
                  subtitle: Text('Site: ${record.siteName ?? 'Unknown'}\nChecked In: ${DateFormat.jm().format(record.checkInTime)}'),
                  isThreeLine: true,
                  trailing: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.success.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text('ON SITE', style: TextStyle(color: AppColors.success, fontWeight: FontWeight.bold, fontSize: 12)),
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
