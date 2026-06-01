import 'package:equatable/equatable.dart';

class OccupancyStats extends Equatable {
  final int totalWorkers;
  final int expectedWorkers;
  final int openTasks;
  final List<DepartmentOccupancy> departmentBreakdown;
  final List<ContractorOccupancy> contractorBreakdown;
  final List<VarianceRecord> plannedVsActual;

  const OccupancyStats({
    required this.totalWorkers,
    required this.expectedWorkers,
    required this.openTasks,
    required this.departmentBreakdown,
    required this.contractorBreakdown,
    required this.plannedVsActual,
  });

  factory OccupancyStats.fromJson(Map<String, dynamic> json) {
    return OccupancyStats(
      totalWorkers: json['total_workers'] as int? ?? 0,
      expectedWorkers: json['expected_workers'] as int? ?? 0,
      openTasks: json['open_tasks'] as int? ?? 0,
      departmentBreakdown: (json['department_breakdown'] as List?)
              ?.map((e) => DepartmentOccupancy.fromJson(e))
              .toList() ??
          [],
      contractorBreakdown: (json['contractor_breakdown'] as List?)
              ?.map((e) => ContractorOccupancy.fromJson(e))
              .toList() ??
          [],
      plannedVsActual: (json['planned_vs_actual'] as List?)
              ?.map((e) => VarianceRecord.fromJson(e))
              .toList() ??
          [],
    );
  }

  @override
  List<Object?> get props => [
        totalWorkers,
        expectedWorkers,
        openTasks,
        departmentBreakdown,
        contractorBreakdown,
        plannedVsActual,
      ];
}

class DepartmentOccupancy extends Equatable {
  final String departmentName;
  final int count;

  const DepartmentOccupancy({required this.departmentName, required this.count});

  factory DepartmentOccupancy.fromJson(Map<String, dynamic> json) {
    return DepartmentOccupancy(
      departmentName: json['department_name'] as String,
      count: json['count'] as int,
    );
  }

  @override
  List<Object?> get props => [departmentName, count];
}

class ContractorOccupancy extends Equatable {
  final String contractorName;
  final int count;

  const ContractorOccupancy({required this.contractorName, required this.count});

  factory ContractorOccupancy.fromJson(Map<String, dynamic> json) {
    return ContractorOccupancy(
      contractorName: json['contractor_name'] as String,
      count: json['count'] as int,
    );
  }

  @override
  List<Object?> get props => [contractorName, count];
}

class VarianceRecord extends Equatable {
  final String departmentName;
  final int planned;
  final int actual;

  const VarianceRecord({
    required this.departmentName,
    required this.planned,
    required this.actual,
  });

  factory VarianceRecord.fromJson(Map<String, dynamic> json) {
    return VarianceRecord(
      departmentName: json['department_name'] as String,
      planned: json['planned'] as int,
      actual: json['actual'] as int,
    );
  }

  @override
  List<Object?> get props => [departmentName, planned, actual];
}
