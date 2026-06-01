import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/occupancy_repository.dart';
import '../../domain/entities/occupancy_stats.dart';

final occupancyStatsProvider = FutureProvider.family<OccupancyStats, String>((ref, siteId) async {
  final repository = ref.read(occupancyRepositoryProvider);
  return repository.getOccupancyStats(siteId);
});
