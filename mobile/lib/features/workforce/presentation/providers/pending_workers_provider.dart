import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/worker_repository.dart';
import '../../../auth/domain/entities/user.dart';
import '../../../dashboard/presentation/screens/admin_dashboard_screen.dart';
import 'worker_providers.dart';

final pendingWorkersProvider = FutureProvider.autoDispose<List<User>>((ref) async {
  final repository = ref.read(workerRepositoryProvider);
  return repository.getPendingWorkers();
});

class WorkerActionNotifier extends StateNotifier<AsyncValue<void>> {
  final WorkerRepository _repository;
  final Ref _ref;

  WorkerActionNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  void _invalidateProviders() {
    _ref.invalidate(pendingWorkersProvider);
    _ref.invalidate(workersListProvider);
    _ref.invalidate(adminDashboardSummaryProvider);
  }

  Future<void> approve(String userId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.approveWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> reject(String userId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.rejectWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> suspend(String userId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.suspendWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> reactivate(String userId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.reactivateWorker(userId);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}

final workerActionNotifierProvider = StateNotifierProvider<WorkerActionNotifier, AsyncValue<void>>((ref) {
  return WorkerActionNotifier(ref.read(workerRepositoryProvider), ref);
});
