import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/worker_repository.dart';
import '../../../dashboard/presentation/screens/admin_dashboard_screen.dart';

import 'worker_providers.dart';


class WorkerActionNotifier extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }

  void _invalidateProviders() {
    ref.invalidate(workersListProvider);
    ref.invalidate(adminDashboardSummaryProvider);
  }

  Future<void> approve(String userId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(workerRepositoryProvider).approveWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> reject(String userId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(workerRepositoryProvider).rejectWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> suspend(String userId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(workerRepositoryProvider).suspendWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> reactivate(String userId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(workerRepositoryProvider).reactivateWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}

final workerActionNotifierProvider =
    NotifierProvider<WorkerActionNotifier, AsyncValue<void>>(
  WorkerActionNotifier.new,
);
