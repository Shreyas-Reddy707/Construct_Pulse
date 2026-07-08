import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/site_repository.dart';
import '../../domain/entities/site.dart';

final sitesProvider = FutureProvider.autoDispose<List<Site>>((ref) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSites();
});

final siteProvider = FutureProvider.autoDispose.family<Site, String>((ref, id) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSite(id);
});

final siteQrProvider = FutureProvider.autoDispose.family<String, String>((ref, id) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSiteQr(id);
});

final siteAssignmentsProvider = FutureProvider.autoDispose.family<Map<String, dynamic>, String>((ref, id) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSiteAssignments(id);
});

class SiteActionNotifier extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }

  Future<void> assignWorker(String siteId, String workerId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(siteRepositoryProvider).assignWorker(siteId, workerId);
      ref.invalidate(siteProvider(siteId));
      ref.invalidate(siteAssignmentsProvider(siteId));
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> unassignWorker(String siteId, String workerId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(siteRepositoryProvider).unassignWorker(siteId, workerId);
      ref.invalidate(siteProvider(siteId));
      ref.invalidate(siteAssignmentsProvider(siteId));
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<String> createSite(Map<String, dynamic> data) async {
    state = const AsyncValue.loading();
    try {
      final id = await ref.read(siteRepositoryProvider).createSite(data);
      ref.invalidate(sitesProvider);
      state = const AsyncValue.data(null);
      return id;
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      rethrow;
    }
  }

  Future<void> generateQr(String siteId) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(siteRepositoryProvider).generateSiteQr(siteId);
      ref.invalidate(siteQrProvider(siteId));
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}

final siteActionNotifierProvider =
    NotifierProvider<SiteActionNotifier, AsyncValue<void>>(
  SiteActionNotifier.new,
);
