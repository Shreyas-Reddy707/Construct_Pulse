import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../attendance/presentation/providers/attendance_providers.dart';

class SiteOccupancyScreen extends ConsumerWidget {
  const SiteOccupancyScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final occAsync = ref.watch(occupancyProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Live Occupancy')),
      body: occAsync.when(
        data: (sites) {
          if (sites.isEmpty) {
            return const Center(child: Text('No active sites.'));
          }
          return RefreshIndicator(
            onRefresh: () async => ref.refresh(occupancyProvider),
            child: ListView.separated(
              itemCount: sites.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final site = sites[index];
                return ListTile(
                  leading: const CircleAvatar(
                    backgroundColor: AppColors.secondarySurface,
                    child: Icon(Icons.location_city_rounded, color: AppColors.secondary),
                  ),
                  title: Text(site['site_name'] as String),
                  trailing: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Text(
                      '${site['workers_on_site']} Workers',
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                );
              },
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(child: Text('Error: $err')),
      ),
    );
  }
}
