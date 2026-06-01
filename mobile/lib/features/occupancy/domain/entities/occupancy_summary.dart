import 'package:equatable/equatable.dart';

class OccupancySummary extends Equatable {
  final int totalOccupancy;
  final int activeWorkers;
  final int contractors;
  final int departments;
  final Map<String, int> occupancyByDepartment;
  final Map<String, int> occupancyByContractor;

  const OccupancySummary({
    required this.totalOccupancy,
    required this.activeWorkers,
    required this.contractors,
    required this.departments,
    required this.occupancyByDepartment,
    required this.occupancyByContractor,
  });

  factory OccupancySummary.fromJson(Map<String, dynamic> json) {
    return OccupancySummary(
      totalOccupancy: json['total_occupancy'] as int? ?? 0,
      activeWorkers: json['active_workers'] as int? ?? 0,
      contractors: json['contractors'] as int? ?? 0,
      departments: json['departments'] as int? ?? 0,
      occupancyByDepartment: Map<String, int>.from(json['by_department'] ?? {}),
      occupancyByContractor: Map<String, int>.from(json['by_contractor'] ?? {}),
    );
  }

  @override
  List<Object?> get props => [
        totalOccupancy,
        activeWorkers,
        contractors,
        departments,
        occupancyByDepartment,
        occupancyByContractor,
      ];
}
