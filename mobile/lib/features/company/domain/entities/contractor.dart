import 'package:equatable/equatable.dart';

class Contractor extends Equatable {
  final String id;
  final String? companyId;
  final String name;
  final String? phone;
  final String? trade;

  const Contractor({
    required this.id,
    this.companyId,
    required this.name,
    this.phone,
    this.trade,
  });

  factory Contractor.fromJson(Map<String, dynamic> json) {
    return Contractor(
      id: json['id'] as String,
      companyId: json['company_id'] as String?,
      name: json['name'] as String,
      phone: json['phone'] as String?,
      trade: json['trade'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'company_id': companyId,
      'name': name,
      'phone': phone,
      'trade': trade,
    };
  }

  @override
  List<Object?> get props => [id, companyId, name, phone, trade];
}
