import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/occupancy_repository.dart';
import '../../domain/entities/occupancy_summary.dart';

final currentOccupancyProvider = FutureProvider<OccupancySummary>((ref) async {
  final repository = ref.read(occupancyRepositoryProvider);
  return repository.getCurrentOccupancy();
});

final siteOccupancyProvider =
    FutureProvider.family<OccupancySummary, String>((ref, siteId) async {
  final repository = ref.read(occupancyRepositoryProvider);
  return repository.getSiteOccupancy(siteId);
});
