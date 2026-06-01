import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/occupancy_summary.dart';

final occupancyRepositoryProvider = Provider<OccupancyRepository>((ref) {
  return OccupancyRepository(ref.read(dioProvider));
});

class OccupancyRepository {
  final Dio _dio;

  OccupancyRepository(this._dio);

  Future<OccupancySummary> getCurrentOccupancy() async {
    try {
      final response = await _dio.get(ApiEndpoints.currentOccupancy);
      return OccupancySummary.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<OccupancySummary> getSiteOccupancy(String siteId) async {
    try {
      final response = await _dio.get(ApiEndpoints.siteOccupancy(siteId));
      return OccupancySummary.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
