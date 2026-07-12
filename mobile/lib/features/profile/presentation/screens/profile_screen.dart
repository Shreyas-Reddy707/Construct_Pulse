import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';
import '../../../auth/presentation/providers/auth_provider.dart';

/// Profile Screen
class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider).user;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(children: [
            const SizedBox(height: 24),
            // Avatar
            Container(
              width: 100, height: 100,
              decoration: BoxDecoration(
                gradient: AppColors.primaryGradient,
                borderRadius: BorderRadius.circular(30),
                boxShadow: [
                  BoxShadow(color: AppColors.primary.withValues(alpha: 0.3), blurRadius: 20, offset: const Offset(0, 10)),
                ],
              ),
              child: Center(child: Text(
                user?.initials ?? 'WK',
                style: AppTypography.h1.copyWith(color: Colors.white),
              )),
            ),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppColors.border),
              ),
              child: Row(
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: Image.asset('assets/images/logo.png', width: 60, height: 60, fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) => const Icon(Icons.business_rounded, size: 40, color: AppColors.primary),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Demo Company', style: AppTypography.h4.copyWith(color: AppColors.primary)),
                        Text('Building the Future Together', style: AppTypography.caption.copyWith(fontSize: 10)),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            const Icon(Icons.phone_rounded, size: 12, color: AppColors.textSecondary),
                            const SizedBox(width: 4),
                            Text('03 000 0000', style: AppTypography.caption.copyWith(fontSize: 11)),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: user?.status.toString().contains('APPROVED') == true || user?.status.toString().contains('approved') == true ? AppColors.successLight : AppColors.warningLight, 
                borderRadius: BorderRadius.circular(20)
              ),
              child: Text(user?.status != null ? user!.status.toString().split('.').last.toUpperCase() : 'APPROVED',
                  style: AppTypography.label.copyWith(color: user?.status.toString().contains('APPROVED') == true || user?.status.toString().contains('approved') == true ? AppColors.successDark : AppColors.warningDark)),
            ),
            const SizedBox(height: 32),
            // Menu Items
            _menuSection('Account', [
              _menuItem(Icons.person_outline_rounded, 'Edit Profile', () {}),
              _menuItem(Icons.phone_outlined, 'Phone: ${user?.phone ?? ''}', null),
              _menuItem(Icons.badge_outlined, 'Role: ${user?.role.label ?? "Worker"}', null),
              _menuItem(Icons.business_rounded, 'Dept: ${user?.departmentName ?? "N/A"}', null),
              _menuItem(Icons.handyman_rounded, 'Contractor: ${user?.contractorName ?? "N/A"}', null),
            ]),
            const SizedBox(height: 16),
            _menuSection('Work', [
              _menuItem(Icons.access_time_rounded, 'Timesheet', () {}),
              _menuItem(Icons.payments_outlined, 'Payroll Preview', () {}),
              _menuItem(Icons.location_on_outlined, 'My Sites', () {}),
            ]),
            const SizedBox(height: 16),
            _menuSection('App', [
              _menuItem(Icons.dark_mode_outlined, 'Dark Mode', () {}),
              _menuItem(Icons.language_rounded, 'Language', () {}),
              _menuItem(Icons.info_outline_rounded, 'About', () {}),
            ]),
            const SizedBox(height: 24),
            PrimaryButton(
              text: 'Logout',
              backgroundColor: AppColors.danger,
              icon: Icons.logout_rounded,
              onPressed: () => ref.read(authProvider.notifier).logout(),
            ),
            const SizedBox(height: 80),
          ]),
        ),
      ),
    );
  }

  Widget _menuSection(String title, List<Widget> items) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(
        padding: const EdgeInsets.only(left: 4, bottom: 8),
        child: Text(title, style: AppTypography.label.copyWith(fontSize: 11, letterSpacing: 1.5)),
      ),
      Container(
        decoration: BoxDecoration(
          color: AppColors.surface, borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppColors.border),
        ),
        child: Column(children: [
          for (int i = 0; i < items.length; i++) ...[
            items[i],
            if (i < items.length - 1) const Divider(height: 0, indent: 52),
          ],
        ]),
      ),
    ]);
  }

  Widget _menuItem(IconData icon, String label, VoidCallback? onTap) {
    return ListTile(
      leading: Icon(icon, size: 22, color: AppColors.textSecondary),
      title: Text(label, style: AppTypography.bodySmall),
      trailing: onTap != null ? const Icon(Icons.chevron_right_rounded, size: 20, color: AppColors.textTertiary) : null,
      onTap: onTap,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
    );
  }
}
