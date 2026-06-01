import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/company_repository.dart';
import '../../domain/entities/company.dart';
import '../../domain/entities/department.dart';
import '../../domain/entities/contractor.dart';

final companiesProvider = FutureProvider<List<Company>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getCompanies();
});

final companyProvider = FutureProvider.family<Company, String>((ref, id) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getCompany(id);
});

final departmentsProvider = FutureProvider<List<Department>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getDepartments();
});

final departmentProvider = FutureProvider.family<Department, String>((ref, id) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getDepartment(id);
});

final contractorsProvider = FutureProvider<List<Contractor>>((ref) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getContractors();
});

final contractorProvider = FutureProvider.family<Contractor, String>((ref, id) async {
  final repository = ref.read(companyRepositoryProvider);
  return repository.getContractor(id);
});
