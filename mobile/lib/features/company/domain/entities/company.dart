import 'package:equatable/equatable.dart';

class Company extends Equatable {
  final String id;
  final String companyName;
  final String name;
  final String? registrationNumber;
  final String? contactEmail;
  final String? contactPhone;

  const Company({
    required this.id,
    required this.companyName,
    required this.name,
    this.registrationNumber,
    this.contactEmail,
    this.contactPhone,
  });

  factory Company.fromJson(Map<String, dynamic> json) {
    return Company(
      id: json['id'] as String,
      name: json['company_name'] as String? ?? 'Unknown',
      companyName: json['company_name'] as String? ?? 'Unknown',
      registrationNumber: json['registration_number'] as String?,
      contactEmail: json['contact_email'] as String?,
      contactPhone: json['contact_phone'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'company_name': companyName,
      'name': companyName,
      'registration_number': registrationNumber,
      'contact_email': contactEmail,
      'contact_phone': contactPhone,
    };
  }

  @override
  List<Object?> get props => [id, companyName, registrationNumber, contactEmail, contactPhone];
}
