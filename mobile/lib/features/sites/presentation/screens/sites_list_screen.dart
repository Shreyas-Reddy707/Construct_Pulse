import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/common_widgets.dart';
import '../providers/site_providers.dart';
import '../../../auth/presentation/providers/auth_provider.dart';

/// Sites List Screen (Spec §78)
class SitesListScreen extends ConsumerWidget {
  const SitesListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider).user;
    final sitesAsync = ref.watch(sitesProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Sites'),
        actions: [
          if (user?.isAdmin ?? false)
            IconButton(icon: const Icon(Icons.add_rounded), onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Site management available in admin version')));
            }),
        ],
      ),
      body: Column(
        children: [
          // Search
          const Padding(
            padding: EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(
                hintText: 'Search sites...',
                prefixIcon: Icon(Icons.search_rounded, size: 20),
                contentPadding: EdgeInsets.symmetric(vertical: 12),
              ),
            ),
          ),
          // List
          Expanded(
            child: sitesAsync.when(
              data: (sites) {
                if (sites.isEmpty) {
                  return const Center(child: Text('No sites found.'));
                }
                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: sites.length,
                  itemBuilder: (ctx, i) {
                    final s = sites[i];
                    return GestureDetector(
                      onTap: () => context.push('/sites/${s.id}'),
                      child: Container(
                        margin: const EdgeInsets.only(bottom: 12),
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: AppColors.surface,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: AppColors.border),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Container(
                                  width: 44,
                                  height: 44,
                                  decoration: BoxDecoration(
                                    color: AppColors.primarySurface,
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: const Icon(Icons.location_on_rounded, color: AppColors.primary, size: 22),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(s.name, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
                                      Text(s.address ?? 'No address', style: AppTypography.caption.copyWith(fontSize: 12), maxLines: 1, overflow: TextOverflow.ellipsis),
                                    ],
                                  ),
                                ),
                                s.status == 'active'
                                    ? StatusBadge.active()
                                    : const StatusBadge(label: 'Inactive', color: AppColors.surfaceVariant, textColor: AppColors.textTertiary),
                              ],
                            ),
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                _siteMetric(Icons.my_location_rounded, '${s.latitude?.toStringAsFixed(4) ?? '0.0'}, ${s.longitude?.toStringAsFixed(4) ?? '0.0'}'),
                                const SizedBox(width: 16),
                                _siteMetric(Icons.qr_code_rounded, 'QR Ready'),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: AppColors.danger))),
            ),
          ),
        ],
      ),
    );
  }

  Widget _siteMetric(IconData icon, String label) {
    return Row(
      children: [
        Icon(icon, size: 14, color: AppColors.textTertiary),
        const SizedBox(width: 4),
        Text(label, style: AppTypography.caption.copyWith(fontSize: 12)),
      ],
    );
  }
}
