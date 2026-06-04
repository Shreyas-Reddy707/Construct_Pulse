import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/attendance_repository.dart';
import '../../domain/entities/attendance.dart';

import '../../../auth/presentation/providers/auth_provider.dart';

final todayAttendanceProvider = FutureProvider<List<Attendance>>((ref) async {
  final user = ref.watch(authProvider.select((s) => s.user));
  if (user == null) return [];
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getTodayAttendance(user.id);
});

final attendanceHistoryProvider = FutureProvider<List<Attendance>>((ref) async {
  final user = ref.watch(authProvider.select((s) => s.user));
  if (user == null) return [];
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getHistory(user.id);
});

final workerAttendanceHistoryProvider = FutureProvider.family<List<Attendance>, String>((ref, userId) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getHistory(userId);
});

final liveAttendanceProvider = FutureProvider<List<Attendance>>((ref) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getLiveAttendance();
});

final occupancyProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final repository = ref.read(attendanceRepositoryProvider);
  return repository.getSiteOccupancy();
});

class AttendanceNotifier extends StateNotifier<AsyncValue<void>> {
  final AttendanceRepository _repository;

  AttendanceNotifier(this._repository) : super(const AsyncValue.data(null));

  Future<void> checkIn(String siteId, String qrToken, {double? lat, double? lng}) async {
    state = const AsyncValue.loading();
    try {
      await _repository.checkIn(siteId, qrToken, lat: lat, lng: lng);
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> checkOut(String siteId, String qrToken, {double? lat, double? lng}) async {
    state = const AsyncValue.loading();
    try {
      await _repository.checkOut(siteId, qrToken, lat: lat, lng: lng);
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}

final attendanceNotifierProvider =
    StateNotifierProvider<AttendanceNotifier, AsyncValue<void>>((ref) {
  return AttendanceNotifier(ref.read(attendanceRepositoryProvider));
});
