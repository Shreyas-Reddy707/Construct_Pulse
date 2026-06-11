import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';
import '../constants/app_constants.dart';
import '../../features/dashboard/presentation/screens/admin_dashboard_screen.dart';
import '../../features/sites/presentation/screens/sites_list_screen.dart';
import '../../features/workforce/presentation/screens/workforce_directory_screen.dart';
import '../../features/profile/presentation/screens/profile_screen.dart';

class CompanyAdminShell extends StatefulWidget {
  const CompanyAdminShell({super.key});

  @override
  State<CompanyAdminShell> createState() => _CompanyAdminShellState();
}

class _CompanyAdminShellState extends State<CompanyAdminShell> {
  int _currentIndex = 0;

  final _screens = const [
    AdminDashboardScreen(),
    SitesListScreen(),
    WorkforceDirectoryScreen(),
    WorkforceDirectoryScreen(initialStatus: 'pending'),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
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
                _navItem(0, Icons.dashboard_rounded, Icons.dashboard_outlined, 'Dashboard'),
                _navItem(1, Icons.location_city_rounded, Icons.location_city_outlined, 'Sites'),
                _navItem(2, Icons.people_rounded, Icons.people_outline_rounded, 'Workers'),
                _navItem(3, Icons.pending_actions_rounded, Icons.pending_actions_outlined, 'Approvals'),
                _navItem(4, Icons.person_rounded, Icons.person_outline_rounded, 'Profile'),
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
                color: isActive ? AppColors.primarySurface : Colors.transparent,
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
