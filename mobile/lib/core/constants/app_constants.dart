/// Application-wide constants for ConstructPulse
class AppConstants {
  AppConstants._();

  // ── App Info ──────────────────────────────────────────────
  static const String appName = 'ConstructPulse';
  static const String appVersion = '1.0.0';
  static const String appTagline = 'Workforce Intelligence Platform';

  /// Development authentication mode (bypasses Firebase SMS billing)
  static const bool demoAuth = true;

  // ── API ───────────────────────────────────────────────────
  static const String baseUrl = 'http://192.168.0.14:8000/api/v1';
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);

  // ── Auth ──────────────────────────────────────────────────
  static const int otpLength = 6;
  static const Duration otpExpiry = Duration(minutes: 5);
  static const Duration accessTokenExpiry = Duration(minutes: 15);
  static const Duration refreshTokenExpiry = Duration(days: 7);
  static const int maxOtpAttempts = 5;
  static const Duration otpCooldown = Duration(seconds: 30);

  // ── Pagination ────────────────────────────────────────────
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;

  // ── Attendance ────────────────────────────────────────────
  static const int defaultOvertimeThresholdHours = 8;

  // ── Emergency ─────────────────────────────────────────────
  static const Duration musterGenerationTimeout = Duration(seconds: 5);

  // ── Storage Keys ──────────────────────────────────────────
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  static const String companyIdKey = 'company_id';
  static const String onboardingCompleteKey = 'onboarding_complete';
  static const String themeKey = 'theme_mode';

  // ── Animation Durations ───────────────────────────────────
  static const Duration animFast = Duration(milliseconds: 150);
  static const Duration animNormal = Duration(milliseconds: 200);
  static const Duration animSlow = Duration(milliseconds: 350);

  // ── Layout ────────────────────────────────────────────────
  static const double gridUnit = 8.0;
  static const double cardRadius = 16.0;
  static const double buttonRadius = 12.0;
  static const double inputRadius = 12.0;
  static const double modalRadius = 20.0;
  static const double bottomNavHeight = 80.0;
  static const double fabSize = 64.0;
}
