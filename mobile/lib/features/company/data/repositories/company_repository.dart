import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/company.dart';
import '../../domain/entities/department.dart';
import '../../domain/entities/contractor.dart';
import '../../../auth/domain/entities/user.dart';

final companyRepositoryProvider = Provider<CompanyRepository>((ref) {
  return CompanyRepository(ref.read(dioProvider));
});

class CompanyRepository {
  final Dio _dio;

  CompanyRepository(this._dio);

  Future<List<Department>> getPublicDepartments() async {
    try {
      final response = await _dio.get(ApiEndpoints.publicDepartments);
      final data = response.data as List;
      return data.map((json) => Department.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Contractor>> getPublicContractors() async {
    try {
      final response = await _dio.get(ApiEndpoints.publicContractors);
      final data = response.data as List;
      return data.map((json) => Contractor.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Company>> getPublicCompanies() async {
    try {
      final response = await _dio.get(ApiEndpoints.publicCompanies);
      final data = response.data as List;
      return data.map((json) => Company.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Company>> getCompanies() async {
    try {
      final response = await _dio.get(ApiEndpoints.companies);
      final data = response.data as List;
      return data.map((json) => Company.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Company> createCompany(Map<String, dynamic> payload) async {
    try {
      final response = await _dio.post(ApiEndpoints.companies, data: payload);
      return Company.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<User>> getCompanyUsers(String companyId) async {
    try {
      final response = await _dio.get('${ApiEndpoints.companies}/$companyId/users');
      final data = response.data as List;
      return data.map((json) => User.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<User> assignAdmin(String companyId, String userId) async {
    try {
      final response = await _dio.put('${ApiEndpoints.companies}/$companyId/assign-admin/$userId');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Company> getCompany(String id) async {
    try {
      final response = await _dio.get(ApiEndpoints.company(id));
      return Company.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }



  Future<void> updateCompany(String id, Map<String, dynamic> data) async {
    try {
      await _dio.put(ApiEndpoints.company(id), data: data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deactivateCompany(String id) async {
    try {
      await _dio.delete(ApiEndpoints.company(id));
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  // ── Departments ──────────────────────────────────────────────
  Future<List<Department>> getDepartments() async {
    try {
      final response = await _dio.get(ApiEndpoints.departments);
      final data = response.data as List;
      return data.map((json) => Department.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Department> getDepartment(String id) async {
    try {
      final response = await _dio.get(ApiEndpoints.department(id));
      return Department.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> createDepartment(Map<String, dynamic> data) async {
    try {
      await _dio.post(ApiEndpoints.departments, data: data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> updateDepartment(String id, Map<String, dynamic> data) async {
    try {
      await _dio.put(ApiEndpoints.department(id), data: data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deleteDepartment(String id) async {
    try {
      await _dio.delete(ApiEndpoints.department(id));
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  // ── Contractors ──────────────────────────────────────────────
  Future<List<Contractor>> getContractors() async {
    try {
      final response = await _dio.get(ApiEndpoints.contractors);
      final data = response.data as List;
      return data.map((json) => Contractor.fromJson(json)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Contractor> getContractor(String id) async {
    try {
      final response = await _dio.get(ApiEndpoints.contractor(id));
      return Contractor.fromJson(response.data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<String> createContractor(Map<String, dynamic> data) async {
    try {
      final response = await _dio.post(ApiEndpoints.contractors, data: data);
      return response.data['id'] ?? response.data['contractor_id'];
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> updateContractor(String id, Map<String, dynamic> data) async {
    try {
      await _dio.put(ApiEndpoints.contractor(id), data: data);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deactivateContractor(String id) async {
    try {
      await _dio.delete(ApiEndpoints.contractor(id));
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
