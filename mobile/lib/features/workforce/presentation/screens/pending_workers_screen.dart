import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/pending_workers_provider.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';

class PendingWorkersScreen extends ConsumerWidget {
  const PendingWorkersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pendingWorkersAsync = ref.watch(pendingWorkersProvider);
    final actionState = ref.watch(workerActionNotifierProvider);

    ref.listen<AsyncValue<void>>(workerActionNotifierProvider, (_, state) {
      state.whenOrNull(
        error: (error, stackTrace) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(error.toString()),
              backgroundColor: AppColors.danger,
            ),
          );
        },
        data: (_) {
          if (!state.isLoading && !state.hasError && state.hasValue) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Action successful'),
              ),
            );
          }
        },
      );
    });

    return Scaffold(
      appBar: AppBar(
        title: const Text('Pending Workers'),
      ),
      body: pendingWorkersAsync.when(
        data: (workers) {
          if (workers.isEmpty) {
            return const Center(
              child: Text('No pending workers.'),
            );
          }
          return Stack(
            children: [
              ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: workers.length,
                itemBuilder: (context, index) {
                  final worker = workers[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${worker.firstName} ${worker.lastName}',
                            style: AppTypography.h3,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            worker.phone,
                            style: AppTypography.bodySmall,
                          ),
                          const SizedBox(height: 16),
                          Row(
                            children: [
                              Expanded(
                                child: OutlinedButton(
                                  onPressed: actionState.isLoading
                                      ? null
                                      : () => ref.read(workerActionNotifierProvider.notifier).reject(worker.id),
                                  style: OutlinedButton.styleFrom(
                                    foregroundColor: AppColors.danger,
                                    side: const BorderSide(color: AppColors.danger),
                                  ),
                                  child: const Text('Reject'),
                                ),
                              ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: PrimaryButton(
                                  text: 'Approve',
                                  onPressed: actionState.isLoading
                                      ? null
                                      : () => ref.read(workerActionNotifierProvider.notifier).approve(worker.id),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
              if (actionState.isLoading)
                const Positioned.fill(
                  child: DecoratedBox(
                    decoration: BoxDecoration(color: Colors.black26),
                    child: Center(
                      child: CircularProgressIndicator(),
                    ),
                  ),
                ),
            ],
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }
}
