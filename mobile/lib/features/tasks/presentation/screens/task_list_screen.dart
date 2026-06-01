import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';

/// Task List Screen (Spec §81)
class TaskListScreen extends StatelessWidget {
  const TaskListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final tasks = <Map<String, dynamic>>[];

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Tasks'),
        actions: [IconButton(icon: const Icon(Icons.add_rounded), onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Feature available in future release')));
        })],
      ),
      body: Column(children: [
        // Summary
        Container(
          margin: const EdgeInsets.all(16),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.surface, borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppColors.border),
          ),
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
            _stat('--', 'Total', AppColors.textPrimary),
            _stat('--', 'Done', AppColors.success),
            _stat('--', 'Active', AppColors.primary),
            _stat('--', 'Blocked', AppColors.danger),
          ]),
        ),
        // Filter
        SizedBox(
          height: 40,
          child: ListView(scrollDirection: Axis.horizontal, padding: const EdgeInsets.symmetric(horizontal: 16), children: [
            _chip('All', true), _chip('In Progress', false), _chip('Blocked', false), _chip('Completed', false),
          ]),
        ),
        const SizedBox(height: 8),
        // Task list
        Expanded(
          child: tasks.isEmpty ? const Center(child: Text('No tasks found.')) : ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: tasks.length,
            itemBuilder: (_, i) => _taskCard(tasks[i]),
          ),
        ),
      ]),
    );
  }

  Widget _stat(String value, String label, Color color) => Column(children: [
    Text(value, style: AppTypography.h3.copyWith(color: color)),
    Text(label, style: AppTypography.caption.copyWith(fontSize: 11)),
  ]);

  Widget _chip(String label, bool sel) => Padding(
    padding: const EdgeInsets.only(right: 8),
    child: FilterChip(label: Text(label), selected: sel, onSelected: (_) {},
        selectedColor: AppColors.primarySurface, checkmarkColor: AppColors.primary),
  );

  Widget _taskCard(Map<String, dynamic> task) {
    final badge = switch (task['status']) {
      'in_progress' => StatusBadge.inProgress(),
      'completed' => StatusBadge.completed(),
      'blocked' => StatusBadge.blocked(),
      _ => const StatusBadge(label: 'Not Started', color: AppColors.surfaceVariant, textColor: AppColors.textSecondary),
    };

    final priorityColor = switch (task['priority']) {
      'critical' => AppColors.danger,
      'high' => AppColors.secondary,
      'medium' => AppColors.warning,
      _ => AppColors.textTertiary,
    };

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.surface, borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Container(width: 4, height: 32, decoration: BoxDecoration(color: priorityColor, borderRadius: BorderRadius.circular(2))),
          const SizedBox(width: 10),
          Expanded(child: Text(task['title'] as String, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600))),
          badge,
        ]),
        const SizedBox(height: 10),
        Row(children: [
          const SizedBox(width: 14),
          const Icon(Icons.person_outline_rounded, size: 14, color: AppColors.textTertiary),
          const SizedBox(width: 4),
          Text(task['assignee'] as String, style: AppTypography.caption.copyWith(fontSize: 12)),
          const Spacer(),
          SizedBox(
            width: 80,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(3),
              child: LinearProgressIndicator(
                value: (task['progress'] as int) / 100,
                minHeight: 6,
                backgroundColor: AppColors.surfaceVariant,
                valueColor: AlwaysStoppedAnimation(task['status'] == 'completed' ? AppColors.success : AppColors.primary),
              ),
            ),
          ),
          const SizedBox(width: 6),
          Text('${task['progress']}%', style: AppTypography.label.copyWith(fontSize: 11)),
        ]),
      ]),
    );
  }
}
