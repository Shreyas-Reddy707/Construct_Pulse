import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/worker_repository.dart';
import '../../../auth/domain/entities/user.dart';

final workersListProvider = FutureProvider.family<List<User>, String?>((ref, status) async {
  final repository = ref.read(workerRepositoryProvider);
  return repository.getWorkers(status: status);
});

final workerDetailProvider = FutureProvider.family<User, String>((ref, userId) async {
  final repository = ref.read(workerRepositoryProvider);
  return repository.getWorker(userId);
});
