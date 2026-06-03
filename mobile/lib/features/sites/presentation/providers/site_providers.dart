import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/site_repository.dart';
import '../../domain/entities/site.dart';

final sitesProvider = FutureProvider<List<Site>>((ref) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSites();
});

final siteProvider = FutureProvider.family<Site, String>((ref, id) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSite(id);
});

final siteQrProvider = FutureProvider.family<String, String>((ref, id) async {
  final repository = ref.read(siteRepositoryProvider);
  return repository.getSiteQr(id);
});

class SiteActionNotifier extends StateNotifier<AsyncValue<void>> {
  final SiteRepository _repository;
  final Ref _ref;

  SiteActionNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> assignWorker(String siteId, String workerId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.assignWorker(siteId, workerId);
      _ref.invalidate(siteProvider(siteId));
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<String> createSite(Map<String, dynamic> data) async {
    state = const AsyncValue.loading();
    try {
      final id = await _repository.createSite(data);
      _ref.invalidate(sitesProvider);
      state = const AsyncValue.data(null);
      return id;
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      rethrow;
    }
  }
}

final siteActionNotifierProvider = StateNotifierProvider<SiteActionNotifier, AsyncValue<void>>((ref) {
  return SiteActionNotifier(ref.read(siteRepositoryProvider), ref);
});
