import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'app_colors.dart';
import 'app_typography.dart';
import '../constants/app_constants.dart';

/// ConstructPulse Material 3 Theme (Master Spec §84–§92)
class AppTheme {
  AppTheme._();

  // ── Light Theme ───────────────────────────────────────────
  static ThemeData get light => ThemeData(
        useMaterial3: true,
        brightness: Brightness.light,
        colorScheme: _lightColorScheme,
        textTheme: AppTypography.textTheme,
        scaffoldBackgroundColor: AppColors.background,

        // AppBar
        appBarTheme: const AppBarTheme(
          backgroundColor: AppColors.surface,
          foregroundColor: AppColors.textPrimary,
          elevation: 0,
          scrolledUnderElevation: 1,
          centerTitle: false,
          systemOverlayStyle: SystemUiOverlayStyle(
            statusBarColor: Colors.transparent,
            statusBarIconBrightness: Brightness.dark,
            statusBarBrightness: Brightness.light,
          ),
        ),

        // Cards
        cardTheme: CardThemeData(
          color: AppColors.surface,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConstants.cardRadius),
            side: const BorderSide(color: AppColors.border),
          ),
          margin: EdgeInsets.zero,
        ),

        // Elevated Buttons
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: AppColors.textOnPrimary,
            elevation: 0,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            minimumSize: const Size(double.infinity, 56),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(AppConstants.buttonRadius),
            ),
            textStyle: AppTypography.button,
          ),
        ),

        // Outlined Buttons
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.primary,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            minimumSize: const Size(double.infinity, 56),
            side: const BorderSide(color: AppColors.primary, width: 1.5),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(AppConstants.buttonRadius),
            ),
            textStyle: AppTypography.button,
          ),
        ),

        // Text Buttons
        textButtonTheme: TextButtonThemeData(
          style: TextButton.styleFrom(
            foregroundColor: AppColors.primary,
            textStyle: AppTypography.button,
          ),
        ),

        // Input Fields
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: AppColors.surfaceVariant,
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide: const BorderSide(color: AppColors.border),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide: const BorderSide(color: AppColors.primary, width: 2),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide: const BorderSide(color: AppColors.danger),
          ),
          hintStyle: AppTypography.bodySmall.copyWith(
            color: AppColors.textTertiary,
          ),
          labelStyle: AppTypography.bodySmall.copyWith(
            color: AppColors.textSecondary,
          ),
        ),

        // Bottom Navigation
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: AppColors.surface,
          selectedItemColor: AppColors.primary,
          unselectedItemColor: AppColors.textTertiary,
          type: BottomNavigationBarType.fixed,
          elevation: 8,
          showUnselectedLabels: true,
        ),

        // Floating Action Button
        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: AppColors.secondary,
          foregroundColor: AppColors.textOnSecondary,
          elevation: 4,
          highlightElevation: 8,
          shape: CircleBorder(),
        ),

        // Chips
        chipTheme: ChipThemeData(
          backgroundColor: AppColors.surfaceVariant,
          selectedColor: AppColors.primarySurface,
          labelStyle: AppTypography.label,
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          side: const BorderSide(color: AppColors.border),
        ),

        // Divider
        dividerTheme: const DividerThemeData(
          color: AppColors.divider,
          thickness: 1,
          space: 0,
        ),

        // Bottom Sheet
        bottomSheetTheme: const BottomSheetThemeData(
          backgroundColor: AppColors.surface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
          ),
          showDragHandle: true,
        ),

        // Dialog
        dialogTheme: DialogThemeData(
          backgroundColor: AppColors.surface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConstants.modalRadius),
          ),
        ),

        // Snackbar
        snackBarTheme: SnackBarThemeData(
          backgroundColor: AppColors.darkSurface,
          contentTextStyle: AppTypography.bodySmall.copyWith(
            color: AppColors.darkTextPrimary,
          ),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),

        // Tab Bar
        tabBarTheme: TabBarThemeData(
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textSecondary,
          indicatorSize: TabBarIndicatorSize.label,
          indicator: const UnderlineTabIndicator(
            borderSide: BorderSide(color: AppColors.primary, width: 2),
          ),
          labelStyle: AppTypography.button,
          unselectedLabelStyle: AppTypography.bodySmall,
        ),
      );

  // ── Dark Theme ────────────────────────────────────────────
  static ThemeData get dark => ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: _darkColorScheme,
        textTheme: AppTypography.textTheme.apply(
          bodyColor: AppColors.darkTextPrimary,
          displayColor: AppColors.darkTextPrimary,
        ),
        scaffoldBackgroundColor: AppColors.darkBackground,

        appBarTheme: const AppBarTheme(
          backgroundColor: AppColors.darkSurface,
          foregroundColor: AppColors.darkTextPrimary,
          elevation: 0,
          scrolledUnderElevation: 1,
          centerTitle: false,
          systemOverlayStyle: SystemUiOverlayStyle(
            statusBarColor: Colors.transparent,
            statusBarIconBrightness: Brightness.light,
            statusBarBrightness: Brightness.dark,
          ),
        ),

        cardTheme: CardThemeData(
          color: AppColors.darkSurface,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConstants.cardRadius),
            side: const BorderSide(color: AppColors.darkBorder),
          ),
          margin: EdgeInsets.zero,
        ),

        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: AppColors.textOnPrimary,
            elevation: 0,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            minimumSize: const Size(double.infinity, 56),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(AppConstants.buttonRadius),
            ),
            textStyle: AppTypography.button,
          ),
        ),

        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: AppColors.darkSurfaceVariant,
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide:
                const BorderSide(color: AppColors.darkBorder),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(AppConstants.inputRadius),
            borderSide: const BorderSide(color: AppColors.primary, width: 2),
          ),
        ),

        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: AppColors.darkSurface,
          selectedItemColor: AppColors.primary,
          unselectedItemColor: AppColors.darkTextSecondary,
          type: BottomNavigationBarType.fixed,
          elevation: 8,
          showUnselectedLabels: true,
        ),

        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: AppColors.secondary,
          foregroundColor: AppColors.textOnSecondary,
          elevation: 4,
          shape: CircleBorder(),
        ),

        dividerTheme: const DividerThemeData(
          color: AppColors.darkBorder,
          thickness: 1,
          space: 0,
        ),

        bottomSheetTheme: const BottomSheetThemeData(
          backgroundColor: AppColors.darkSurface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
          ),
          showDragHandle: true,
        ),

        dialogTheme: DialogThemeData(
          backgroundColor: AppColors.darkSurface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConstants.modalRadius),
          ),
        ),
      );

  // ── Color Schemes ─────────────────────────────────────────
  static const ColorScheme _lightColorScheme = ColorScheme(
    brightness: Brightness.light,
    primary: AppColors.primary,
    onPrimary: AppColors.textOnPrimary,
    primaryContainer: AppColors.primarySurface,
    onPrimaryContainer: AppColors.primaryDark,
    secondary: AppColors.secondary,
    onSecondary: AppColors.textOnSecondary,
    secondaryContainer: AppColors.secondarySurface,
    onSecondaryContainer: AppColors.secondaryDark,
    error: AppColors.danger,
    onError: AppColors.textOnPrimary,
    errorContainer: AppColors.dangerLight,
    onErrorContainer: AppColors.dangerDark,
    surface: AppColors.surface,
    onSurface: AppColors.textPrimary,
    surfaceContainerHighest: AppColors.surfaceVariant,
    onSurfaceVariant: AppColors.textSecondary,
    outline: AppColors.border,
    outlineVariant: AppColors.borderLight,
  );

  static const ColorScheme _darkColorScheme = ColorScheme(
    brightness: Brightness.dark,
    primary: AppColors.primaryLight,
    onPrimary: AppColors.textOnPrimary,
    primaryContainer: AppColors.primaryDark,
    onPrimaryContainer: AppColors.primarySurface,
    secondary: AppColors.secondaryLight,
    onSecondary: AppColors.textOnSecondary,
    secondaryContainer: AppColors.secondaryDark,
    onSecondaryContainer: AppColors.secondarySurface,
    error: AppColors.danger,
    onError: AppColors.textOnPrimary,
    errorContainer: AppColors.dangerDark,
    onErrorContainer: AppColors.dangerLight,
    surface: AppColors.darkSurface,
    onSurface: AppColors.darkTextPrimary,
    surfaceContainerHighest: AppColors.darkSurfaceVariant,
    onSurfaceVariant: AppColors.darkTextSecondary,
    outline: AppColors.darkBorder,
    outlineVariant: AppColors.darkBorder,
  );
}
