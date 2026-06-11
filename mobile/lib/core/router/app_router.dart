import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app_shell.dart';
import 'auth_guard.dart';
import '../../features/auth/presentation/screens/splash_screen.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/screens/otp_verification_screen.dart';
import '../../features/auth/presentation/screens/registration_screen.dart';
import '../../features/auth/presentation/screens/pending_approval_screen.dart';
import '../../features/attendance/presentation/screens/qr_scan_screen.dart';
import '../../features/emergency/presentation/screens/emergency_muster_screen.dart';
import '../../features/workforce/presentation/screens/worker_detail_screen.dart';
import '../../features/company/presentation/screens/companies_list_screen.dart';
import '../../features/company/presentation/screens/departments_list_screen.dart';
import '../../features/company/presentation/screens/contractors_list_screen.dart';
import '../../features/sites/presentation/screens/site_detail_screen.dart';
import '../../features/sites/presentation/screens/site_qr_screen.dart';
import '../../features/sites/presentation/screens/site_create_screen.dart';
import '../../features/sites/presentation/screens/sites_list_screen.dart';

import '../../features/workforce/presentation/screens/workforce_directory_screen.dart';
import '../../features/attendance/presentation/screens/live_attendance_screen.dart';
import '../../features/attendance/presentation/screens/attendance_history_screen.dart';
import '../../features/sites/presentation/screens/site_occupancy_screen.dart';
import '../../features/dashboard/presentation/screens/analytics_screen.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';

class RouterNotifier extends ChangeNotifier {
  final Ref ref;
  RouterNotifier(this.ref) {
    ref.listen(authProvider.select((state) => state.status), (_, __) => notifyListeners());
  }
}

final routerProvider = Provider<GoRouter>((ref) {
  final notifier = RouterNotifier(ref);

  return GoRouter(
    initialLocation: '/splash',
    refreshListenable: notifier,
    redirect: (context, state) {
      final authState = ref.read(authProvider);
      return authGuard(context, state, authState);
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      // Auth routes
      GoRoute(path: '/auth/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/auth/otp', builder: (_, __) => const OtpVerificationScreen()),
      GoRoute(path: '/auth/register', builder: (_, __) => const RegistrationScreen()),
      GoRoute(path: '/auth/pending', builder: (_, __) => const PendingApprovalScreen()),
      // Main app
      GoRoute(path: '/', builder: (_, __) => const AppShell()),
      GoRoute(path: '/scan', builder: (_, __) => const QrScanScreen()),
      GoRoute(path: '/emergency', builder: (_, __) => const EmergencyMusterScreen()),
      GoRoute(
        path: '/workforce/:id',
        builder: (_, state) => WorkerDetailScreen(userId: state.pathParameters['id']!),
      ),
      GoRoute(path: '/companies', builder: (_, __) => const CompaniesListScreen()),
      GoRoute(path: '/departments', builder: (_, __) => const DepartmentsListScreen()),
      GoRoute(path: '/contractors', builder: (_, __) => const ContractorsListScreen()),
      GoRoute(path: '/sites', builder: (_, __) => const SitesListScreen()),
      GoRoute(
        path: '/sites/create',
        builder: (_, __) => const SiteCreateScreen(),
      ),
      GoRoute(
        path: '/sites/:id',
        builder: (_, state) => SiteDetailScreen(siteId: state.pathParameters['id']!),
      ),
      GoRoute(
        path: '/sites/:id/qr',
        builder: (_, state) => SiteQrScreen(siteId: state.pathParameters['id']!),
      ),

      GoRoute(
        path: '/workforce',
        builder: (_, state) => WorkforceDirectoryScreen(initialStatus: state.uri.queryParameters['status']),
      ),
      GoRoute(
        path: '/attendance-live',
        builder: (_, state) => LiveAttendanceScreen(siteId: state.uri.queryParameters['siteId']),
      ),
      GoRoute(
        path: '/attendance-history',
        builder: (_, state) => AttendanceHistoryScreen(
          initialFilter: state.uri.queryParameters['filter'],
        ),
      ),
      GoRoute(
        path: '/attendance-history/:workerId',
        builder: (_, state) => AttendanceHistoryScreen(workerId: state.pathParameters['workerId']),
      ),
      GoRoute(
        path: '/occupancy',
        builder: (_, __) => const SiteOccupancyScreen(),
      ),
      GoRoute(
        path: '/analytics',
        builder: (_, __) => const AnalyticsScreen(),
      ),
    ],
  );
});
