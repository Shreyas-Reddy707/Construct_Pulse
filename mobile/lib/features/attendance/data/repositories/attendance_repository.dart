import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/attendance.dart';

final attendanceRepositoryProvider = Provider<AttendanceRepository>((ref) {
  return AttendanceRepository(ref.read(dioProvider));
});

class AttendanceRepository {
  final Dio _dio;

  AttendanceRepository(this._dio);

  Future<Attendance> checkIn(String siteId, String qrToken, {double? lat, double? lng}) async {
    try {
      final response = await _dio.post(
        ApiEndpoints.checkIn,
        data: {
          'site_id': siteId,
          'qr_token': qrToken,
          if (lat != null) 'gps_latitude': lat,
          if (lng != null) 'gps_longitude': lng,
        },
      );
      return Attendance.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Attendance> checkOut(String siteId, String qrToken, {double? lat, double? lng}) async {
    try {
      final response = await _dio.post(
        ApiEndpoints.checkOut,
        data: {
          'site_id': siteId,
          'qr_token': qrToken,
          if (lat != null) 'gps_latitude': lat,
          if (lng != null) 'gps_longitude': lng,
        },
      );
      return Attendance.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Attendance>> getTodayAttendance(String userId) async {
    try {
      final response = await _dio.get(ApiEndpoints.userAttendance(userId));
      final data = response.data as List;
      final list = data.map((json) => Attendance.fromJson(json)).toList();
      // Filter for today client-side since there's no backend endpoint
      final now = DateTime.now();
      return list.where((a) => a.checkInTime.year == now.year && a.checkInTime.month == now.month && a.checkInTime.day == now.day).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Attendance>> getHistory(String userId) async {
    try {
      final response = await _dio.get(ApiEndpoints.userAttendance(userId));
      final data = response.data as List;
      return data.map((json) => Attendance.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
