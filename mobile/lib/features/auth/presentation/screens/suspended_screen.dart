import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../providers/auth_provider.dart';

class SuspendedScreen extends ConsumerWidget {
  const SuspendedScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
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
                  color: AppColors.dangerLight,
                  borderRadius: BorderRadius.circular(30),
                ),
                child: const Icon(Icons.block_outlined,
                    size: 56, color: AppColors.danger),
              ),
              const SizedBox(height: 32),
              Text('Account Suspended', style: AppTypography.h2, textAlign: TextAlign.center),
              const SizedBox(height: 12),
              Text('Your account has been suspended.\nPlease contact your company administrator.',
                  style: AppTypography.caption, textAlign: TextAlign.center),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: () {
                  ref.read(authProvider.notifier).logout();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  minimumSize: const Size(double.infinity, 56),
                ),
                child: const Text('Return to Login'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
