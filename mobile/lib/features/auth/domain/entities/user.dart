import '../../../../core/constants/enums.dart';

/// User entity matching spec §43 / §110
class User {
  final String id;
  final String companyId;
  final String? departmentId;
  final String? contractorId;
  final String phone;
  final String firstName;
  final String lastName;
  final String? designation;
  final UserRole role;
  final UserStatus status;
  final String? emergencyContactName;
  final String? emergencyContactPhone;
  final String? emergencyContactRelationship;
  final String? departmentName;
  final String? contractorName;
  final String? companyName;
  final String? employeeId;
  final String? profilePhoto;
  final DateTime? createdAt;

  const User({
    required this.id,
    required this.companyId,
    this.departmentId,
    this.contractorId,
    required this.phone,
    required this.firstName,
    required this.lastName,
    this.designation,
    required this.role,
    required this.status,
    this.emergencyContactName,
    this.emergencyContactPhone,
    this.emergencyContactRelationship,
    this.departmentName,
    this.contractorName,
    this.companyName,
    this.employeeId,
    this.profilePhoto,
    this.createdAt,
  });

  String get fullName => '$firstName $lastName';
  String get initials =>
      '${firstName.isNotEmpty ? firstName[0] : ''}${lastName.isNotEmpty ? lastName[0] : ''}'
          .toUpperCase();
  bool get isApproved => status == UserStatus.approved;
  bool get isPending => status == UserStatus.pending;
  bool get isRejected => status == UserStatus.rejected;
  bool get isSuspended => status == UserStatus.suspended;
  bool get isWorker => role == UserRole.worker;
  bool get isAdmin => role == UserRole.admin || role == UserRole.superAdmin;
  bool get isManager => role == UserRole.siteManager;
  bool get isEngineer => role == UserRole.siteEngineer;
  bool get isContractor => role == UserRole.contractor;
  bool get isInspector => role == UserRole.municipalityInspector;

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] ?? '',
      companyId: json['company_id'] ?? '',
      departmentId: json['department_id'],
      contractorId: json['contractor_id'],
      phone: json['phone_number'] ?? json['phone'] ?? '',
      firstName: json['first_name'] ?? (json['name'] != null ? json['name'].split(' ').first : ''),
      lastName: json['last_name'] ?? (json['name'] != null && json['name'].split(' ').length > 1 ? json['name'].split(' ').sublist(1).join(' ') : ''),
      designation: json['designation'],
      role: UserRole.fromValue(json['role'] ?? 'worker'),
      status: UserStatus.fromValue(json['status'] ?? 'pending'),
      emergencyContactName: json['emergency_contact_name'],
      emergencyContactPhone: json['emergency_contact_phone'],
      emergencyContactRelationship: json['emergency_contact_relationship'],
      departmentName: json['department_name'],
      contractorName: json['contractor_name'],
      companyName: json['company_name'],
      employeeId: json['employee_id'],
      profilePhoto: json['profile_photo'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'company_id': companyId,
        'department_id': departmentId,
        'contractor_id': contractorId,
        'phone': phone,
        'first_name': firstName,
        'last_name': lastName,
        'designation': designation,
        'role': role.value,
        'status': status.value,
        'emergency_contact_name': emergencyContactName,
        'emergency_contact_phone': emergencyContactPhone,
        'employee_id': employeeId,
        'profile_photo': profilePhoto,
      };
}
