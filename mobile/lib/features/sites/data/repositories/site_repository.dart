import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/site.dart';

final siteRepositoryProvider = Provider<SiteRepository>((ref) {
  return SiteRepository(ref.read(dioProvider));
});

class SiteRepository {
  final Dio _dio;

  SiteRepository(this._dio);

  Future<List<Site>> getSites() async {
    try {
      final response = await _dio.get(ApiEndpoints.sites);
      final data = response.data as List;
      return data.map((json) => Site.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Site> getSite(String id) async {
    try {
      final response = await _dio.get(ApiEndpoints.site(id));
      return Site.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<String> getSiteQr(String siteId) async {
    try {
      final response = await _dio.get(ApiEndpoints.siteQr(siteId));
      final qrToken = response.data['qr_token'];
      return jsonEncode({'site_id': siteId, 'qr_token': qrToken});
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
  Future<String> createSite(Map<String, dynamic> data) async {
    try {
      final response = await _dio.post(ApiEndpoints.sites, data: data);
      return response.data['id'] ?? response.data['site_id'];
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> updateSite(String siteId, Map<String, dynamic> data) async {
    try {
      await _dio.put(ApiEndpoints.site(siteId), data: data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> assignWorker(String siteId, String workerId) async {
    try {
      await _dio.post(
        '${ApiEndpoints.sites}/$siteId/assign-worker',
        data: {'worker_id': workerId},
      );
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deactivateSite(String siteId) async {
    try {
      await _dio.delete(ApiEndpoints.site(siteId));
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
