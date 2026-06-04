import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../auth/domain/entities/user.dart';
import '../../../sites/domain/entities/site.dart';

final workerRepositoryProvider = Provider<WorkerRepository>((ref) {
  return WorkerRepository(ref.read(dioProvider));
});

class WorkerRepository {
  final Dio _dio;

  WorkerRepository(this._dio);

  Future<List<User>> getWorkers({String? status}) async {
    try {
      final queryParams = <String, dynamic>{};
      if (status != null) {
        queryParams['status'] = status;
      }
      
      final response = await _dio.get(
        ApiEndpoints.users,
        queryParameters: queryParams,
      );
      
      final data = response.data as List;
      return data.map((json) => User.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<User> getWorker(String userId) async {
    try {
      final response = await _dio.get('${ApiEndpoints.users}/$userId');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Site>> getWorkerSites(String userId) async {
    try {
      final response = await _dio.get('${ApiEndpoints.users}/$userId/sites');
      final data = response.data as List;
      return data.map((json) => Site.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<User>> getPendingWorkers() async {
    try {
      final response = await _dio.get('${ApiEndpoints.users}/pending');
      final data = response.data as List;
      return data.map((json) => User.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<User> approveWorker(String userId) async {
    try {
      final response = await _dio.put('${ApiEndpoints.users}/$userId/approve');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<User> rejectWorker(String userId) async {
    try {
      final response = await _dio.put('${ApiEndpoints.users}/$userId/reject');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<User> suspendWorker(String userId) async {
    try {
      final response = await _dio.put('${ApiEndpoints.users}/$userId/suspend');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<User> reactivateWorker(String userId) async {
    try {
      final response = await _dio.put('${ApiEndpoints.users}/$userId/reactivate');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
