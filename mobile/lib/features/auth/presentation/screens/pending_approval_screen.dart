import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';

/// Pending Approval Screen (Spec §70 Screen 5)
class PendingApprovalScreen extends StatelessWidget {
  const PendingApprovalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 120, height: 120,
                decoration: BoxDecoration(
                  color: AppColors.warningLight,
                  borderRadius: BorderRadius.circular(30),
                ),
                child: const Icon(Icons.hourglass_top_rounded,
                    size: 56, color: AppColors.warning),
              ),
              const SizedBox(height: 32),
              Text('Registration Submitted', style: AppTypography.h2, textAlign: TextAlign.center),
              const SizedBox(height: 12),
              Text('Your registration is being reviewed.\nYou will be notified once approved.',
                  style: AppTypography.caption, textAlign: TextAlign.center),
              const SizedBox(height: 40),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surfaceVariant,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(children: [
                  _infoRow(Icons.check_circle_outline, 'Registration received', AppColors.success),
                  const SizedBox(height: 12),
                  _infoRow(Icons.pending_outlined, 'Admin review in progress', AppColors.warning),
                  const SizedBox(height: 12),
                  _infoRow(Icons.lock_clock_outlined, 'Access pending approval', AppColors.textTertiary),
                ]),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _infoRow(IconData icon, String text, Color color) {
    return Row(children: [
      Icon(icon, size: 20, color: color),
      const SizedBox(width: 12),
      Expanded(child: Text(text, style: AppTypography.bodySmall.copyWith(color: color))),
    ]);
  }
}
