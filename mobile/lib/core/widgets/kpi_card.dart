import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';

/// KPI Card widget used across all dashboards (Spec §89)
class KpiCard extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  final String? trend;
  final Color? iconColor;
  final Color? backgroundColor;
  final VoidCallback? onTap;

  const KpiCard({
    super.key,
    required this.icon,
    required this.value,
    required this.label,
    this.trend,
    this.iconColor,
    this.backgroundColor,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: backgroundColor ??
              (isDark ? AppColors.darkSurface : AppColors.surface),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isDark ? AppColors.darkBorder : AppColors.border,
          ),
          boxShadow: [
            BoxShadow(
              color: AppColors.shadow.withValues(alpha: 0.05),
              blurRadius: 10,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            // Icon
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: (iconColor ?? AppColors.primary).withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                icon,
                size: 20,
                color: iconColor ?? AppColors.primary,
              ),
            ),
            const SizedBox(height: 12),
            // Value
            Text(
              value,
              style: AppTypography.kpiValue.copyWith(
                color: isDark
                    ? AppColors.darkTextPrimary
                    : AppColors.textPrimary,
              ),
            ),
            const SizedBox(height: 4),
            // Label
            Text(
              label,
              style: AppTypography.kpiLabel.copyWith(
                color: isDark
                    ? AppColors.darkTextSecondary
                    : AppColors.textSecondary,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            // Trend
            if (trend != null) ...[
              const SizedBox(height: 8),
              _buildTrend(),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildTrend() {
    final isPositive = trend!.startsWith('+');
    final isNegative = trend!.startsWith('-');
    final color = isPositive
        ? AppColors.success
        : isNegative
            ? AppColors.danger
            : AppColors.textSecondary;
    final icon = isPositive
        ? Icons.trending_up_rounded
        : isNegative
            ? Icons.trending_down_rounded
            : Icons.trending_flat_rounded;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 14, color: color),
        const SizedBox(width: 4),
        Text(
          trend!,
          style: AppTypography.label.copyWith(color: color),
        ),
      ],
    );
  }
}
