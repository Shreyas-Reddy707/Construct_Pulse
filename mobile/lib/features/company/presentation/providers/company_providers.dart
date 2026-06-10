import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/company_repository.dart';
import '../../domain/entities/company.dart';
import '../../domain/entities/department.dart';
import '../../domain/entities/contractor.dart';
import '../../../auth/domain/entities/user.dart';

final companiesProvider = FutureProvider.autoDispose<List<Company>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getCompanies();
});

final companyUsersProvider = FutureProvider.autoDispose.family<List<User>, String>((ref, companyId) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getCompanyUsers(companyId);
});

class AssignAdminNotifier extends StateNotifier<AsyncValue<void>> {
  final CompanyRepository _repository;
  final Ref _ref;

  AssignAdminNotifier(this._repository, this._ref) : super(const AsyncValue.data(null));

  Future<void> assignAdmin(String companyId, String userId) async {
    state = const AsyncValue.loading();
    try {
      await _repository.assignAdmin(companyId, userId);
      _ref.invalidate(companyUsersProvider(companyId));
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}

final assignAdminNotifierProvider = StateNotifierProvider<AssignAdminNotifier, AsyncValue<void>>((ref) {
  return AssignAdminNotifier(ref.read(companyRepositoryProvider), ref);
});

final companyProvider = FutureProvider.autoDispose.family<Company, String>((ref, id) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getCompany(id);
});

final departmentsProvider = FutureProvider.autoDispose<List<Department>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getDepartments();
});

final departmentProvider = FutureProvider.autoDispose.family<Department, String>((ref, id) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getDepartment(id);
});

final contractorsProvider = FutureProvider.autoDispose<List<Contractor>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getContractors();
});

final contractorProvider = FutureProvider.autoDispose.family<Contractor, String>((ref, id) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getContractor(id);
});

final publicDepartmentsProvider = FutureProvider.autoDispose<List<Department>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getPublicDepartments();
});

final publicContractorsProvider = FutureProvider.autoDispose<List<Contractor>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getPublicContractors();
});

final publicCompaniesProvider = FutureProvider.autoDispose<List<Company>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getPublicCompanies();
});
