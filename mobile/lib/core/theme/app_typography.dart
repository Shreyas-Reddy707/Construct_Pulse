import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

/// ConstructPulse Typography System (Master Spec §86)
class AppTypography {
  AppTypography._();

  // ── Base Text Theme ───────────────────────────────────────
  static TextTheme get textTheme => TextTheme(
        displayLarge: _heading(32, FontWeight.w700),
        displayMedium: _heading(28, FontWeight.w600),
        displaySmall: _heading(24, FontWeight.w600),
        headlineLarge: _heading(22, FontWeight.w600),
        headlineMedium: _heading(20, FontWeight.w500),
        headlineSmall: _heading(18, FontWeight.w500),
        titleLarge: _body(18, FontWeight.w600),
        titleMedium: _body(16, FontWeight.w600),
        titleSmall: _body(14, FontWeight.w600),
        bodyLarge: _body(16, FontWeight.w400),
        bodyMedium: _body(14, FontWeight.w400),
        bodySmall: _body(12, FontWeight.w400),
        labelLarge: _label(14, FontWeight.w600),
        labelMedium: _label(12, FontWeight.w500),
        labelSmall: _label(10, FontWeight.w500),
      );

  static TextStyle _heading(double size, FontWeight weight) =>
      GoogleFonts.inter(
        fontSize: size,
        fontWeight: weight,
        color: AppColors.textPrimary,
        letterSpacing: -0.02 * size,
        height: 1.3,
      );

  static TextStyle _body(double size, FontWeight weight) =>
      GoogleFonts.inter(
        fontSize: size,
        fontWeight: weight,
        color: AppColors.textPrimary,
        height: 1.5,
      );

  static TextStyle _label(double size, FontWeight weight) =>
      GoogleFonts.inter(
        fontSize: size,
        fontWeight: weight,
        color: AppColors.textSecondary,
        letterSpacing: 0.5,
        height: 1.4,
      );

  // ── Convenience Styles ────────────────────────────────────
  static TextStyle get h1 => _heading(32, FontWeight.w700);
  static TextStyle get h2 => _heading(28, FontWeight.w600);
  static TextStyle get h3 => _heading(24, FontWeight.w600);
  static TextStyle get h4 => _heading(20, FontWeight.w500);
  static TextStyle get body => _body(16, FontWeight.w400);
  static TextStyle get bodySmall => _body(14, FontWeight.w400);
  static TextStyle get caption => _body(14, FontWeight.w400).copyWith(
        color: AppColors.textSecondary,
      );
  static TextStyle get label => _label(12, FontWeight.w500);
  static TextStyle get button => _body(16, FontWeight.w600);
  static TextStyle get kpiValue => _heading(28, FontWeight.w700);
  static TextStyle get kpiLabel => _label(12, FontWeight.w500);
}
