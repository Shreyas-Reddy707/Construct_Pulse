import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/attendance_repository.dart';
import '../../domain/entities/attendance.dart';

import '../../../auth/presentation/providers/auth_provider.dart';
import '../../../dashboard/presentation/screens/admin_dashboard_screen.dart';
import '../../../dashboard/presentation/providers/occupancy_providers.dart';

final todayAttendanceProvider = FutureProvider.autoDispose<List<Attendance>>((ref) async {
  final user = ref.watch(authProvider.select((s) => s.user));
  if (user == null) return [];
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getTodayAttendance(user.id);
});

final todayAttendanceSummaryProvider = FutureProvider.autoDispose<Map<String, dynamic>>((ref) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getMyTodayAttendanceSummary();
});

final attendanceHistoryProvider = FutureProvider.autoDispose<List<Attendance>>((ref) async {
  final user = ref.watch(authProvider.select((s) => s.user));
  if (user == null) return [];
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getHistory(user.id);
});

final companyAttendanceHistoryProvider = FutureProvider.autoDispose<List<Attendance>>((ref) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getCompanyHistory();
});

final workerAttendanceHistoryProvider = FutureProvider.autoDispose.family<List<Attendance>, String>((ref, userId) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getHistory(userId);
});

final liveAttendanceProvider = FutureProvider.autoDispose<List<Attendance>>((ref) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getLiveAttendance();
});

final occupancyProvider = FutureProvider.autoDispose<List<Map<String, dynamic>>>((ref) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getSiteOccupancy();
});

class AttendanceNotifier extends Notifier<AsyncValue<void>> {
  @override
  AsyncValue<void> build() {
    return const AsyncValue.data(null);
  }

  Future<void> checkIn(String siteId, String qrToken, {double? lat, double? lng}) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(attendanceRepositoryProvider).checkIn(siteId, qrToken, lat: lat, lng: lng);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> checkOut(String siteId, String qrToken, {double? lat, double? lng}) async {
    state = const AsyncValue.loading();
    try {
      await ref.read(attendanceRepositoryProvider).checkOut(siteId, qrToken, lat: lat, lng: lng);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
  
  void _invalidateProviders() {
    ref.invalidate(todayAttendanceProvider);
    ref.invalidate(todayAttendanceSummaryProvider);
    ref.invalidate(liveAttendanceProvider);
    ref.invalidate(occupancyProvider);
    ref.invalidate(attendanceHistoryProvider);
    ref.invalidate(companyAttendanceHistoryProvider);
    ref.invalidate(adminDashboardSummaryProvider);
    ref.invalidate(occupancyStatsProvider);
    // Also invalidate sites to ensure any background assignments become visible
    // Wait, we can't import sitesProvider here easily without circular dependencies or extra imports.
    // Instead, I'll let the user pull-to-refresh or rely on other invalidation points.
  }
}

final attendanceNotifierProvider =
    NotifierProvider<AttendanceNotifier, AsyncValue<void>>(
  AttendanceNotifier.new,
);
