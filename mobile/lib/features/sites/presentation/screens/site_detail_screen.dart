import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/site_providers.dart';

class SiteDetailScreen extends ConsumerWidget {
  final String siteId;
  
  const SiteDetailScreen({super.key, required this.siteId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final siteAsync = ref.watch(siteProvider(siteId));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Site Details'),
        actions: [
          IconButton(
            icon: const Icon(Icons.qr_code_2_rounded),
            onPressed: () => context.push('/sites/$siteId/qr'),
          ),
          IconButton(
            icon: const Icon(Icons.edit_rounded),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Site management available in admin version')));
            },
          ),
        ],
      ),
      body: siteAsync.when(
        data: (site) => SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: AppColors.primarySurface,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    const Icon(Icons.location_city_rounded, size: 48, color: AppColors.primary),
                    const SizedBox(height: 16),
                    Text(site.name, style: AppTypography.h3.copyWith(color: AppColors.primaryDark), textAlign: TextAlign.center),
                    const SizedBox(height: 8),
                    site.status == 'active' ? StatusBadge.active() : const StatusBadge(label: 'Inactive', color: AppColors.surfaceVariant, textColor: AppColors.textTertiary),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              Text('Location Details', style: AppTypography.h4.copyWith(fontSize: 16)),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  children: [
                    _buildInfoRow(Icons.map_outlined, 'Address', site.address ?? 'Not specified'),
                    _buildInfoRow(Icons.my_location_rounded, 'Coordinates', '${site.latitude?.toStringAsFixed(6) ?? "N/A"}, ${site.longitude?.toStringAsFixed(6) ?? "N/A"}'),
                    _buildInfoRow(Icons.radar_rounded, 'Geofence Radius', '${site.radius ?? 0} meters'),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              PrimaryButton(
                text: 'View Site QR Code',
                icon: Icons.qr_code_rounded,
                onPressed: () => context.push('/sites/$siteId/qr'),
              ),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: AppColors.danger))),
      ),
    );
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 20, color: AppColors.textSecondary),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: AppTypography.caption),
                const SizedBox(height: 2),
                Text(value, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w500)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
