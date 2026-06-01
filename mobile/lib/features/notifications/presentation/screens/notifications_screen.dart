import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';

/// Notifications Screen (Spec §61)
class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final notifications = <Map<String, dynamic>>[];

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Notifications'),
        actions: [TextButton(onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Feature available in future release')));
        }, child: const Text('Mark all read'))],
      ),
      body: notifications.isEmpty ? const Center(child: Text('No new notifications.')) : ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: notifications.length,
        itemBuilder: (_, i) {
          final n = notifications[i];
          final isUnread = n['read'] == false;
          final catIcon = _catIcon(n['cat'] as String);
          final catColor = _catColor(n['cat'] as String);

          return Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: isUnread ? AppColors.primarySurface.withValues(alpha: 0.3) : AppColors.surface,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: isUnread ? AppColors.primary.withValues(alpha: 0.2) : AppColors.border),
            ),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                width: 40, height: 40,
                decoration: BoxDecoration(color: catColor.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(10)),
                child: Icon(catIcon, color: catColor, size: 20),
              ),
              const SizedBox(width: 12),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Row(children: [
                  Expanded(child: Text(n['title'] as String,
                      style: AppTypography.bodySmall.copyWith(fontWeight: isUnread ? FontWeight.w700 : FontWeight.w500))),
                  if (isUnread) Container(width: 8, height: 8, decoration: const BoxDecoration(color: AppColors.primary, shape: BoxShape.circle)),
                ]),
                const SizedBox(height: 2),
                Text(n['msg'] as String, style: AppTypography.caption.copyWith(fontSize: 12)),
                const SizedBox(height: 4),
                Text(n['time'] as String, style: AppTypography.label.copyWith(fontSize: 10)),
              ])),
            ]),
          );
        },
      ),
    );
  }

  IconData _catIcon(String cat) => switch (cat) {
    'emergency' => Icons.emergency_rounded,
    'attendance' => Icons.access_time_rounded,
    'planning' => Icons.event_note_rounded,
    'task' => Icons.assignment_rounded,
    'payroll' => Icons.payments_rounded,
    'inspection' => Icons.fact_check_rounded,
    _ => Icons.notifications_rounded,
  };

  Color _catColor(String cat) => switch (cat) {
    'emergency' => AppColors.danger,
    'attendance' => AppColors.primary,
    'planning' => AppColors.secondary,
    'task' => AppColors.info,
    'payroll' => AppColors.success,
    'inspection' => AppColors.warning,
    _ => AppColors.textSecondary,
  };
}
