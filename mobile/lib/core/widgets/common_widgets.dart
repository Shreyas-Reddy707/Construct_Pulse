import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';

/// Status badge for displaying user status, task status, etc.
class StatusBadge extends StatelessWidget {
  final String label;
  final Color color;
  final Color? textColor;
  final bool isSmall;

  const StatusBadge({
    super.key,
    required this.label,
    required this.color,
    this.textColor,
    this.isSmall = false,
  });

  /// Factory constructors for common statuses
  factory StatusBadge.pending() => const StatusBadge(
        label: 'Pending',
        color: AppColors.warningLight,
        textColor: AppColors.warningDark,
      );

  factory StatusBadge.approved() => const StatusBadge(
        label: 'Approved',
        color: AppColors.successLight,
        textColor: AppColors.successDark,
      );

  factory StatusBadge.rejected() => const StatusBadge(
        label: 'Rejected',
        color: AppColors.dangerLight,
        textColor: AppColors.dangerDark,
      );

  factory StatusBadge.suspended() => const StatusBadge(
        label: 'Suspended',
        color: AppColors.warningLight,
        textColor: AppColors.warningDark,
      );

  factory StatusBadge.active() => const StatusBadge(
        label: 'Active',
        color: AppColors.successLight,
        textColor: AppColors.successDark,
      );

  factory StatusBadge.checkedIn() => const StatusBadge(
        label: 'Checked In',
        color: AppColors.successLight,
        textColor: AppColors.successDark,
      );

  factory StatusBadge.checkedOut() => const StatusBadge(
        label: 'Checked Out',
        color: AppColors.surfaceVariant,
        textColor: AppColors.textSecondary,
      );

  factory StatusBadge.missing() => const StatusBadge(
        label: 'Missing',
        color: AppColors.dangerLight,
        textColor: AppColors.dangerDark,
      );

  factory StatusBadge.present() => const StatusBadge(
        label: 'Present',
        color: AppColors.successLight,
        textColor: AppColors.successDark,
      );

  factory StatusBadge.critical() => const StatusBadge(
        label: 'Critical',
        color: AppColors.dangerLight,
        textColor: AppColors.dangerDark,
      );

  factory StatusBadge.high() => const StatusBadge(
        label: 'High',
        color: AppColors.secondarySurface,
        textColor: AppColors.secondaryDark,
      );

  factory StatusBadge.inProgress() => const StatusBadge(
        label: 'In Progress',
        color: AppColors.primarySurface,
        textColor: AppColors.primaryDark,
      );

  factory StatusBadge.completed() => const StatusBadge(
        label: 'Completed',
        color: AppColors.successLight,
        textColor: AppColors.successDark,
      );

  factory StatusBadge.blocked() => const StatusBadge(
        label: 'Blocked',
        color: AppColors.dangerLight,
        textColor: AppColors.dangerDark,
      );

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: isSmall ? 8 : 12,
        vertical: isSmall ? 2 : 4,
      ),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        label,
        style: (isSmall ? AppTypography.label : AppTypography.label).copyWith(
          color: textColor ?? AppColors.textPrimary,
          fontSize: isSmall ? 10 : 12,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}

/// Empty state widget
class EmptyState extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final Widget? action;

  const EmptyState({
    super.key,
    required this.icon,
    required this.title,
    this.subtitle,
    this.action,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: AppColors.primarySurface,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Icon(icon, size: 40, color: AppColors.primary),
            ),
            const SizedBox(height: 24),
            Text(
              title,
              style: AppTypography.h4,
              textAlign: TextAlign.center,
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 8),
              Text(
                subtitle!,
                style: AppTypography.caption,
                textAlign: TextAlign.center,
              ),
            ],
            if (action != null) ...[
              const SizedBox(height: 24),
              action!,
            ],
          ],
        ),
      ),
    );
  }
}

/// Error state widget with retry
class ErrorState extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const ErrorState({
    super.key,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: AppColors.dangerLight,
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(
                Icons.error_outline_rounded,
                size: 40,
                color: AppColors.danger,
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Something went wrong',
              style: AppTypography.h4,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              message,
              style: AppTypography.caption,
              textAlign: TextAlign.center,
            ),
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              TextButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh_rounded),
                label: const Text('Try Again'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

/// Shimmer loading placeholder
class ShimmerBox extends StatelessWidget {
  final double width;
  final double height;
  final double borderRadius;

  const ShimmerBox({
    super.key,
    required this.width,
    required this.height,
    this.borderRadius = 8,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: AppColors.shimmerBase,
        borderRadius: BorderRadius.circular(borderRadius),
      ),
    );
  }
}
