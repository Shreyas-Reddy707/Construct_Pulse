import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../auth/domain/entities/user.dart';

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

  Future<void> approveWorker(String userId) async {
    try {
      await _dio.post('${ApiEndpoints.users}/$userId/approve');
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> suspendWorker(String userId) async {
    try {
      await _dio.post('${ApiEndpoints.users}/$userId/suspend');
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
