import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../providers/worker_providers.dart';

/// Worker List Screen (Workforce Directory)
class WorkforceDirectoryScreen extends ConsumerStatefulWidget {
  const WorkforceDirectoryScreen({super.key});

  @override
  ConsumerState<WorkforceDirectoryScreen> createState() => _WorkforceDirectoryScreenState();
}

class _WorkforceDirectoryScreenState extends ConsumerState<WorkforceDirectoryScreen> {
  String? _statusFilter;

  @override
  Widget build(BuildContext context) {
    final workersAsync = ref.watch(workersListProvider(_statusFilter));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Workforce'),
        actions: [
          IconButton(icon: const Icon(Icons.person_add_rounded), onPressed: () => context.push('/auth/register')),
        ],
      ),
      body: Column(
        children: [
          // Search
          const Padding(
            padding: EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(
                hintText: 'Search workers...',
                prefixIcon: Icon(Icons.search_rounded, size: 20),
              ),
            ),
          ),
          // Filters
          SizedBox(
            height: 36,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              children: ['All', 'Approved', 'Pending']
                  .map((f) => Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: FilterChip(
                          label: Text(f, style: const TextStyle(fontSize: 12)),
                          selected: _statusFilter == (f == 'All' ? null : f.toLowerCase()),
                          onSelected: (selected) {
                            setState(() {
                              _statusFilter = f == 'All' ? null : f.toLowerCase();
                            });
                          },
                          selectedColor: AppColors.primarySurface,
                          visualDensity: VisualDensity.compact,
                        ),
                      ))
                  .toList(),
            ),
          ),
          const SizedBox(height: 8),
          // List
          Expanded(
            child: workersAsync.when(
              data: (workers) => ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: workers.length,
                itemBuilder: (_, i) {
                  final w = workers[i];
                  return Container(
                    margin: const EdgeInsets.only(bottom: 8),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Row(
                      children: [
                        CircleAvatar(
                          radius: 22,
                          backgroundColor: AppColors.primarySurface,
                          backgroundImage: w.profilePhoto != null ? NetworkImage(w.profilePhoto!) : null,
                          child: w.profilePhoto == null
                              ? Text(w.initials,
                                  style: AppTypography.bodySmall.copyWith(color: AppColors.primary, fontWeight: FontWeight.w700))
                              : null,
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Text(w.fullName, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
                                  const SizedBox(width: 8),
                                  if (w.isPending) StatusBadge.pending() else StatusBadge.approved(),
                                ],
                              ),
                              const SizedBox(height: 2),
                              Text('${w.designation ?? 'Worker'} · ${w.departmentName ?? ''}',
                                  style: AppTypography.caption.copyWith(fontSize: 12)),
                              if (w.contractorName != null)
                                Text(w.contractorName!, style: AppTypography.label.copyWith(fontSize: 11)),
                            ],
                          ),
                        ),
                        PopupMenuButton<String>(
                          onSelected: (value) {
                            if (value == 'view') {
                              context.push('/workforce/${w.id}');
                            }
                          },
                          itemBuilder: (_) => [
                            const PopupMenuItem(value: 'view', child: Text('View Profile')),
                            const PopupMenuItem(value: 'approve', child: Text('Approve')),
                            const PopupMenuItem(value: 'suspend', child: Text('Suspend')),
                          ],
                        ),
                      ],
                    ),
                  );
                },
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: AppColors.danger))),
            ),
          ),
        ],
      ),
    );
  }
}
