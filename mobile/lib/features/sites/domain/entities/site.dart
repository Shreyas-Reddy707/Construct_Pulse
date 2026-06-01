import 'package:equatable/equatable.dart';

class Site extends Equatable {
  final String id;
  final String companyId;
  final String name;
  final String? address;
  final double? latitude;
  final double? longitude;
  final String status;
  final double? radius; // Geofence radius in meters

  const Site({
    required this.id,
    required this.companyId,
    required this.name,
    this.address,
    this.latitude,
    this.longitude,
    required this.status,
    this.radius,
  });

  factory Site.fromJson(Map<String, dynamic> json) {
    return Site(
      id: json['id'] as String,
      companyId: json['company_id'] as String,
      name: json['name'] as String,
      address: json['address'] as String?,
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
      status: json['status'] as String? ?? 'active',
      radius: (json['radius'] as num?)?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'company_id': companyId,
      'name': name,
      'address': address,
      'latitude': latitude,
      'longitude': longitude,
      'status': status,
      'radius': radius,
    };
  }

  @override
  List<Object?> get props => [
        id,
        companyId,
        name,
        address,
        latitude,
        longitude,
        status,
        radius,
      ];
}
