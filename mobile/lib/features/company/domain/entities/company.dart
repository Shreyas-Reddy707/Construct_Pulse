import 'package:equatable/equatable.dart';

class Company extends Equatable {
  final String id;
  final String name;
  final String? logoUrl;
  final String? address;
  final String? phone;

  const Company({
    required this.id,
    required this.name,
    this.logoUrl,
    this.address,
    this.phone,
  });

  factory Company.fromJson(Map<String, dynamic> json) {
    return Company(
      id: json['id'] as String,
      name: json['name'] as String,
      logoUrl: json['logo_url'] as String?,
      address: json['address'] as String?,
      phone: json['phone'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'logo_url': logoUrl,
      'address': address,
      'phone': phone,
    };
  }

  @override
  List<Object?> get props => [id, name, logoUrl, address, phone];
}
