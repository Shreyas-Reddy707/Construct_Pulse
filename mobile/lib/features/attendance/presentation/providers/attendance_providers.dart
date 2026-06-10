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

class AttendanceNotifier extends StateNotifier<AsyncValue<void>> {
  final AttendanceRepository _repository;
  final Ref _ref;

  AttendanceNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> checkIn(String siteId, String qrToken, {double? lat, double? lng}) async {
    state = const AsyncValue.loading();
    try {
      await _repository.checkIn(siteId, qrToken, lat: lat, lng: lng);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> checkOut(String siteId, String qrToken, {double? lat, double? lng}) async {
    state = const AsyncValue.loading();
    try {
      await _repository.checkOut(siteId, qrToken, lat: lat, lng: lng);
      _invalidateProviders();
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
  
  void _invalidateProviders() {
    _ref.invalidate(todayAttendanceProvider);
    _ref.invalidate(todayAttendanceSummaryProvider);
    _ref.invalidate(liveAttendanceProvider);
    _ref.invalidate(occupancyProvider);
    _ref.invalidate(attendanceHistoryProvider);
    _ref.invalidate(companyAttendanceHistoryProvider);
    _ref.invalidate(adminDashboardSummaryProvider);
    // Since occupancyStatsProvider is family, we can't easily invalidate all unless we know the siteIds.
    // Wait, Riverpod allows invalidating the family itself:
    _ref.invalidate(occupancyStatsProvider);
  }
}

final attendanceNotifierProvider =
    StateNotifierProvider<AttendanceNotifier, AsyncValue<void>>((ref) {
  return AttendanceNotifier(ref.read(attendanceRepositoryProvider), ref);
});
