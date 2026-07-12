import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/kpi_card.dart';
import '../../../../core/widgets/buttons.dart';
import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../attendance/presentation/providers/attendance_providers.dart';
import '../../../attendance/domain/entities/attendance.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../../../attendance/presentation/screens/attendance_history_screen.dart';
import '../../../../core/constants/enums.dart';

/// Worker Dashboard (Spec §71)
class WorkerDashboardScreen extends ConsumerWidget {
  const WorkerDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider).user;
    final now = DateTime.now();
    final attendanceHistoryAsync = ref.watch(attendanceHistoryProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ── Greeting Header ─────────────────────────
              _buildHeader(context, user?.firstName ?? 'Worker', now),
              const SizedBox(height: 24),

              // ── Attendance Status Card ──────────────────
              attendanceHistoryAsync.when(
                data: (attendanceList) => _buildAttendanceCard(context, attendanceList),
                loading: () => const CircularProgressIndicator(),
                error: (e, _) => const Text('Failed to load attendance'),
              ),
              const SizedBox(height: 20),

              // ── Quick Actions ───────────────────────────
              Text('Quick Actions', style: AppTypography.h4),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(child: QuickActionButton(
                    icon: Icons.qr_code_scanner_rounded,
                    label: 'Scan QR',
                    color: AppColors.secondary,
                    onTap: () => context.push('/scan'),
                  )),
                  Expanded(child: QuickActionButton(
                    icon: Icons.history_rounded,
                    label: 'Attendance',
                    color: AppColors.primary,
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AttendanceHistoryScreen())),
                  )),
                  Expanded(child: QuickActionButton(
                    icon: Icons.location_on_rounded,
                    label: 'My Sites',
                    color: AppColors.success,
                    onTap: () => context.push('/sites'),
                  )),
                  Expanded(child: QuickActionButton(
                    icon: Icons.emergency_rounded,
                    label: 'Emergency',
                    color: AppColors.danger,
                    onTap: () => context.push('/emergency'),
                  )),
                ],
              ),
              const SizedBox(height: 24),

              // ── KPI Cards ──────────────────────────────
              Text('Today\'s Summary', style: AppTypography.h4),
              const SizedBox(height: 12),
              attendanceHistoryAsync.when(
                data: (attendanceList) {
                  if (attendanceList.isEmpty) {
                    return GridView.count(
                      crossAxisCount: 2,
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      crossAxisSpacing: 12,
                      mainAxisSpacing: 12,
                      childAspectRatio: 1.4,
                      children: const [
                        KpiCard(icon: Icons.access_time_rounded, value: '--', label: "Today's Hours", trend: '--', iconColor: AppColors.primary),
                        KpiCard(icon: Icons.calendar_month_rounded, value: '--', label: 'Days This Month', iconColor: AppColors.success),
                        KpiCard(icon: Icons.timer_rounded, value: '--', label: 'Overtime (Month)', trend: '--', iconColor: AppColors.secondary),
                        KpiCard(icon: Icons.trending_up_rounded, value: '--', label: 'Total Hours', iconColor: AppColors.info),
                      ],
                    );
                  }
                  
                  // Compute actual stats from history
                  final currentMonth = DateTime.now().month;
                  final currentYear = DateTime.now().year;
                  
                  int daysThisMonth = 0;
                  int totalHoursThisMonth = 0;
                  int totalHoursAllTime = 0;
                  int todayHours = 0;
                  
                  Set<String> uniqueDaysThisMonth = {};
                  
                  for (var a in attendanceList) {
                    final dt = a.checkInTime.toLocal();
                    int durationHours = 0;
                    if (a.checkOutTime != null) {
                      durationHours = a.checkOutTime!.difference(a.checkInTime).inHours;
                    } else {
                      durationHours = DateTime.now().difference(a.checkInTime).inHours;
                    }
                    
                    totalHoursAllTime += durationHours;
                    
                    if (dt.month == currentMonth && dt.year == currentYear) {
                        uniqueDaysThisMonth.add("${dt.day}");
                        totalHoursThisMonth += durationHours;
                        
                        if (dt.day == DateTime.now().day) {
                            todayHours += durationHours;
                        }
                    }
                  }
                  
                  daysThisMonth = uniqueDaysThisMonth.length;
                  int overtime = (totalHoursThisMonth > (daysThisMonth * 8)) ? totalHoursThisMonth - (daysThisMonth * 8) : 0;
                  
                  return GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.4,
                    children: [
                      KpiCard(icon: Icons.access_time_rounded, value: '${todayHours}h', label: "Today's Hours", trend: '+0', iconColor: AppColors.primary),
                      KpiCard(icon: Icons.calendar_month_rounded, value: '$daysThisMonth', label: 'Days This Month', iconColor: AppColors.success),
                      KpiCard(icon: Icons.timer_rounded, value: '${overtime}h', label: 'Overtime (Month)', trend: '--', iconColor: AppColors.secondary),
                      KpiCard(icon: Icons.trending_up_rounded, value: '${totalHoursAllTime}h', label: 'Total Hours', iconColor: AppColors.info),
                    ],
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (e, _) => const SizedBox(),
              ),
              const SizedBox(height: 24),

              // ── Recent Attendance ───────────────────────
              attendanceHistoryAsync.when(
                data: (attendanceList) => _buildRecentAttendance(context, attendanceList),
                loading: () => const CircularProgressIndicator(),
                error: (e, _) => const Text('Failed to load recent attendance'),
              ),
              const SizedBox(height: 24),

              // ── Assigned Site ───────────────────────────
              attendanceHistoryAsync.when(
                data: (attendanceList) => _buildAssignedSite(attendanceList),
                loading: () => const CircularProgressIndicator(),
                error: (e, _) => const SizedBox.shrink(),
              ),
              const SizedBox(height: 80),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, String name, DateTime now) {
    final greeting = now.hour < 12 ? 'Good Morning' : now.hour < 17 ? 'Good Afternoon' : 'Good Evening';
    return Row(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(14),
          child: Image.asset('assets/images/logo.png', width: 48, height: 48, fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) => Container(
              width: 48, height: 48,
              decoration: BoxDecoration(
                gradient: AppColors.primaryGradient,
                borderRadius: BorderRadius.circular(14),
              ),
              child: Center(child: Text(name.isNotEmpty ? name[0].toUpperCase() : 'W',
                  style: AppTypography.h4.copyWith(color: Colors.white))),
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Limelite Construction', style: AppTypography.caption.copyWith(fontSize: 12, color: AppColors.primary)),
            Text(name, style: AppTypography.h4),
            Text('Masters of Consistency and Quality', style: AppTypography.caption.copyWith(fontSize: 10)),
          ],
        )),
        IconButton(
          onPressed: () {
            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Feature available in future release')));
          },
          icon: const Badge(
            smallSize: 8,
            child: Icon(Icons.notifications_outlined),
          ),
        ),
      ],
    );
  }

  Widget _buildAttendanceCard(BuildContext context, List<Attendance> attendanceList) {
    final recent = attendanceList.isNotEmpty ? attendanceList.first : null;
    final hasActiveCheckIn = recent != null && recent.status == AttendanceStatus.checkedIn;
    final currentStatus = hasActiveCheckIn ? '● Checked In' : '● Not Checked In';
    final statusColor = hasActiveCheckIn ? AppColors.success : AppColors.textTertiary;
    final inTime = recent != null ? "${recent.checkInTime.toLocal().hour.toString().padLeft(2, '0')}:${recent.checkInTime.toLocal().minute.toString().padLeft(2, '0')}" : '--:--';
    final hours = recent != null && recent.checkOutTime != null ? 
        "${recent.checkOutTime!.difference(recent.checkInTime).inHours}h" : (recent != null ? "${DateTime.now().difference(recent.checkInTime).inHours}h" : '--');
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: AppColors.primaryGradient,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(
          color: AppColors.primary.withValues(alpha: 0.3),
          blurRadius: 20, offset: const Offset(0, 8),
        )],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Current Status', style: AppTypography.caption.copyWith(
                    color: Colors.white70, fontSize: 12)),
                const SizedBox(height: 4),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.success.withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: statusColor.withValues(alpha: 0.4)),
                  ),
                  child: Text(currentStatus, style: AppTypography.label.copyWith(
                      color: statusColor, fontWeight: FontWeight.w600)),
                ),
              ]),
              Container(
                width: 56, height: 56,
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Icon(Icons.qr_code_scanner_rounded,
                    color: Colors.white, size: 28),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(children: [
            _statusItem('Check In', inTime),
            const SizedBox(width: 24),
            Expanded(child: _statusItem('Site', recent != null ? (recent.siteName ?? recent.siteId) : 'N/A')),
            const SizedBox(width: 12),
            _statusItem('Hours', hours),
          ]),
        ],
      ),
    );
  }

  Widget _statusItem(String label, String value) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(label, style: AppTypography.caption.copyWith(color: Colors.white60, fontSize: 11)),
      const SizedBox(height: 2),
      Text(value, style: AppTypography.bodySmall.copyWith(
          color: Colors.white, fontWeight: FontWeight.w600)),
    ]);
  }

  Widget _buildRecentAttendance(BuildContext context, List<Attendance> attendanceList) {
    if (attendanceList.isEmpty) {
      return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Recent Attendance', style: AppTypography.h4),
        const SizedBox(height: 8),
        const Text('No recent attendance found.'),
      ]);
    }

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
        Text('Recent Attendance', style: AppTypography.h4),
        TextButton(onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Feature available in future release')));
        }, child: const Text('View All')),
      ]),
      const SizedBox(height: 8),
      ...attendanceList.take(3).map((a) {
        final inStr = "${a.checkInTime.toLocal().hour.toString().padLeft(2, '0')}:${a.checkInTime.toLocal().minute.toString().padLeft(2, '0')}";
        final outStr = a.checkOutTime != null ? "${a.checkOutTime!.toLocal().hour.toString().padLeft(2, '0')}:${a.checkOutTime!.toLocal().minute.toString().padLeft(2, '0')}" : 'Active';
        final isActive = a.status == AttendanceStatus.checkedIn;
        final duration = a.checkOutTime != null ? "${a.checkOutTime!.difference(a.checkInTime).inHours}h" : "${DateTime.now().difference(a.checkInTime).inHours}h";

        return Container(
          margin: const EdgeInsets.only(bottom: 8),
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.border),
          ),
          child: Row(children: [
            Container(
              width: 40, height: 40,
              decoration: BoxDecoration(
                color: isActive ? AppColors.successLight : AppColors.surfaceVariant,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                isActive ? Icons.radio_button_on : Icons.check_circle_outline,
                size: 18,
                color: isActive ? AppColors.success : AppColors.textTertiary,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(DateFormat('MMM dd, yyyy').format(a.checkInTime), style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
              Text('$inStr → $outStr', style: AppTypography.caption.copyWith(fontSize: 12)),
            ])),
            Text(duration, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
          ]),
        );
      }),
    ]);
  }

  Widget _buildAssignedSite(List<Attendance> attendanceList) {
    if (attendanceList.isEmpty) {
      return Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppColors.border),
        ),
        child: const Text('No site assigned / checked-in recently.'),
      );
    }
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(children: [
        Container(
          width: 48, height: 48,
          decoration: BoxDecoration(
            color: AppColors.primarySurface,
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Icon(Icons.location_on_rounded, color: AppColors.primary),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(attendanceList.first.siteName ?? attendanceList.first.siteId, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
          Text('Active Site', style: AppTypography.caption.copyWith(fontSize: 12)),
        ])),
        const Icon(Icons.chevron_right_rounded, color: AppColors.textTertiary),
      ]),
    );
  }
}
