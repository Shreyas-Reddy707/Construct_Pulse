import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_typography.dart';
import '../../core/constants/app_constants.dart';
import '../../features/dashboard/presentation/screens/worker_dashboard_screen.dart';
import '../../features/attendance/presentation/screens/attendance_history_screen.dart';
import '../../features/sites/presentation/screens/sites_list_screen.dart';
import '../../features/profile/presentation/screens/profile_screen.dart';
import '../../features/attendance/presentation/screens/qr_scan_screen.dart';

/// Main app shell with bottom navigation (Spec §88)
class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _currentIndex = 0;

  final _screens = const [
    WorkerDashboardScreen(),
    AttendanceHistoryScreen(),
    SizedBox(), // Placeholder for FAB
    SitesListScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex >= 2 ? _currentIndex : _currentIndex,
        children: _screens,
      ),
      // Floating Action Button – QR Scan (Safety Orange per spec §88)
      floatingActionButton: Container(
        width: AppConstants.fabSize,
        height: AppConstants.fabSize,
        decoration: BoxDecoration(
          gradient: AppColors.accentGradient,
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(
              color: AppColors.secondary.withValues(alpha: 0.4),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: FloatingActionButton(
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const QrScanScreen()),
          ),
          backgroundColor: Colors.transparent,
          elevation: 0,
          highlightElevation: 0,
          child: const Icon(Icons.qr_code_scanner_rounded,
              color: Colors.white, size: 28),
        ),
      ),
      floatingActionButtonLocation:
          FloatingActionButtonLocation.centerDocked,
      // Bottom Navigation
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: AppColors.surface,
          boxShadow: [
            BoxShadow(
              color: AppColors.shadow.withValues(alpha: 0.08),
              blurRadius: 20,
              offset: const Offset(0, -4),
            ),
          ],
        ),
        child: SafeArea(
          child: SizedBox(
            height: AppConstants.bottomNavHeight,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _navItem(0, Icons.home_rounded, Icons.home_outlined, 'Home'),
                _navItem(1, Icons.access_time_filled_rounded,
                    Icons.access_time_rounded, 'Attendance'),
                const SizedBox(width: 56), // Space for FAB
                _navItem(3, Icons.location_on_rounded,
                    Icons.location_on_outlined, 'Sites'),
                _navItem(4, Icons.person_rounded,
                    Icons.person_outline_rounded, 'Profile'),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _navItem(int index, IconData activeIcon, IconData icon, String label) {
    final isActive = _currentIndex == index;
    return GestureDetector(
      onTap: () => setState(() => _currentIndex = index),
      behavior: HitTestBehavior.opaque,
      child: SizedBox(
        width: 64,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedContainer(
              duration: AppConstants.animFast,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              decoration: BoxDecoration(
                color: isActive
                    ? AppColors.primarySurface
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Icon(
                isActive ? activeIcon : icon,
                size: 24,
                color: isActive ? AppColors.primary : AppColors.textTertiary,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: AppTypography.label.copyWith(
                fontSize: 10,
                color: isActive ? AppColors.primary : AppColors.textTertiary,
                fontWeight: isActive ? FontWeight.w600 : FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
