import 'package:equatable/equatable.dart';

class Department extends Equatable {
  final String id;
  final String? companyId;
  final String name;
  final String? description;

  const Department({
    required this.id,
    this.companyId,
    required this.name,
    this.description,
  });

  factory Department.fromJson(Map<String, dynamic> json) {
    return Department(
      id: json['id'] as String,
      companyId: json['company_id'] as String?,
      name: json['name'] as String,
      description: json['description'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'company_id': companyId,
      'name': name,
      'description': description,
    };
  }

  @override
  List<Object?> get props => [id, companyId, name, description];
}
