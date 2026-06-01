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
