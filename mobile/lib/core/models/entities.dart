import '../../core/constants/enums.dart';

/// Attendance entity (Spec §48/§114)
class Attendance {
  final String id;
  final String companyId;
  final String userId;
  final String siteId;
  final DateTime checkIn;
  final DateTime? checkOut;
  final double? hoursWorked;
  final double? overtimeHours;
  final AttendanceStatus status;
  final String? siteName;
  final String? userName;

  const Attendance({
    required this.id,
    required this.companyId,
    required this.userId,
    required this.siteId,
    required this.checkIn,
    this.checkOut,
    this.hoursWorked,
    this.overtimeHours,
    required this.status,
    this.siteName,
    this.userName,
  });

  bool get isActive => status == AttendanceStatus.checkedIn;

  factory Attendance.fromJson(Map<String, dynamic> json) => Attendance(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    userId: json['user_id'] ?? '',
    siteId: json['site_id'] ?? '',
    checkIn: DateTime.parse(json['check_in']),
    checkOut: json['check_out'] != null ? DateTime.parse(json['check_out']) : null,
    hoursWorked: (json['hours_worked'] as num?)?.toDouble(),
    overtimeHours: (json['overtime_hours'] as num?)?.toDouble(),
    status: AttendanceStatus.fromValue(json['status'] ?? 'checked_out'),
    siteName: json['site_name'],
    userName: json['user_name'],
  );
}

/// Site entity (Spec §46/§112)
class Site {
  final String id;
  final String companyId;
  final String siteCode;
  final String siteName;
  final String? address;
  final double? latitude;
  final double? longitude;
  final int? radiusMeters;
  final SiteStatus status;
  final String? qrCodeUrl;

  const Site({
    required this.id,
    required this.companyId,
    required this.siteCode,
    required this.siteName,
    this.address,
    this.latitude,
    this.longitude,
    this.radiusMeters,
    required this.status,
    this.qrCodeUrl,
  });

  factory Site.fromJson(Map<String, dynamic> json) => Site(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    siteCode: json['site_code'] ?? '',
    siteName: json['site_name'] ?? '',
    address: json['address'],
    latitude: (json['latitude'] as num?)?.toDouble(),
    longitude: (json['longitude'] as num?)?.toDouble(),
    radiusMeters: json['radius_meters'],
    status: SiteStatus.fromValue(json['status'] ?? 'active'),
    qrCodeUrl: json['qr_code_url'],
  );
}

/// Department entity (Spec §44/§108)
class Department {
  final String id;
  final String companyId;
  final String name;
  final String? description;

  const Department({
    required this.id,
    required this.companyId,
    required this.name,
    this.description,
  });

  factory Department.fromJson(Map<String, dynamic> json) => Department(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    name: json['name'] ?? '',
    description: json['description'],
  );
}

/// Contractor entity (Spec §45/§109)
class Contractor {
  final String id;
  final String companyId;
  final String contractorName;
  final String? contactPerson;
  final String? phone;
  final String? email;
  final String status;

  const Contractor({
    required this.id,
    required this.companyId,
    required this.contractorName,
    this.contactPerson,
    this.phone,
    this.email,
    this.status = 'active',
  });

  factory Contractor.fromJson(Map<String, dynamic> json) => Contractor(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    contractorName: json['contractor_name'] ?? '',
    contactPerson: json['contact_person'],
    phone: json['phone'],
    email: json['email'],
    status: json['status'] ?? 'active',
  );
}

/// Task entity (Spec §53/§119)
class Task {
  final String id;
  final String companyId;
  final String siteId;
  final String? assignedTo;
  final String title;
  final String? description;
  final TaskPriority priority;
  final TaskStatus status;
  final int progressPercent;
  final DateTime? startDate;
  final DateTime? endDate;
  final String? assigneeName;

  const Task({
    required this.id,
    required this.companyId,
    required this.siteId,
    this.assignedTo,
    required this.title,
    this.description,
    required this.priority,
    required this.status,
    this.progressPercent = 0,
    this.startDate,
    this.endDate,
    this.assigneeName,
  });

  factory Task.fromJson(Map<String, dynamic> json) => Task(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    siteId: json['site_id'] ?? '',
    assignedTo: json['assigned_to'],
    title: json['title'] ?? '',
    description: json['description'],
    priority: TaskPriority.fromValue(json['priority'] ?? 'medium'),
    status: TaskStatus.fromValue(json['status'] ?? 'not_started'),
    progressPercent: json['progress_percent'] ?? 0,
    startDate: json['start_date'] != null ? DateTime.parse(json['start_date']) : null,
    endDate: json['end_date'] != null ? DateTime.parse(json['end_date']) : null,
    assigneeName: json['assignee_name'],
  );
}

/// Emergency Muster Report (Spec §55/§121)
class EmergencyMusterReport {
  final String id;
  final String companyId;
  final String siteId;
  final IncidentType incidentType;
  final DateTime generatedAt;
  final String? remarks;
  final int totalPresent;
  final int totalMissing;

  const EmergencyMusterReport({
    required this.id,
    required this.companyId,
    required this.siteId,
    required this.incidentType,
    required this.generatedAt,
    this.remarks,
    this.totalPresent = 0,
    this.totalMissing = 0,
  });

  factory EmergencyMusterReport.fromJson(Map<String, dynamic> json) => EmergencyMusterReport(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    siteId: json['site_id'] ?? '',
    incidentType: IncidentType.fromValue(json['incident_type'] ?? 'fire'),
    generatedAt: DateTime.parse(json['generated_at']),
    remarks: json['remarks'],
    totalPresent: json['total_present'] ?? 0,
    totalMissing: json['total_missing'] ?? 0,
  );
}

/// Daily Plan (Spec §50/§116)
class DailyPlan {
  final String id;
  final String companyId;
  final String siteId;
  final DateTime planDate;
  final String? remarks;
  final PlanStatus status;

  const DailyPlan({
    required this.id,
    required this.companyId,
    required this.siteId,
    required this.planDate,
    this.remarks,
    required this.status,
  });

  factory DailyPlan.fromJson(Map<String, dynamic> json) => DailyPlan(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    siteId: json['site_id'] ?? '',
    planDate: DateTime.parse(json['plan_date']),
    remarks: json['remarks'],
    status: PlanStatus.fromValue(json['status'] ?? 'draft'),
  );
}

/// Workforce Variance (Spec §54/§120)
class WorkforceVariance {
  final int plannedWorkers;
  final int actualWorkers;
  final int variance;
  final double variancePercentage;

  const WorkforceVariance({
    required this.plannedWorkers,
    required this.actualWorkers,
    required this.variance,
    required this.variancePercentage,
  });

  factory WorkforceVariance.fromJson(Map<String, dynamic> json) => WorkforceVariance(
    plannedWorkers: json['planned_workers'] ?? 0,
    actualWorkers: json['actual_workers'] ?? 0,
    variance: json['variance'] ?? 0,
    variancePercentage: (json['variance_percentage'] as num?)?.toDouble() ?? 0,
  );
}

/// Notification entity (Spec §61/§127)
class AppNotification {
  final String id;
  final String companyId;
  final String userId;
  final String title;
  final String message;
  final NotificationCategory category;
  final NotificationPriority priority;
  final bool isRead;
  final DateTime createdAt;

  const AppNotification({
    required this.id,
    required this.companyId,
    required this.userId,
    required this.title,
    required this.message,
    required this.category,
    required this.priority,
    this.isRead = false,
    required this.createdAt,
  });

  factory AppNotification.fromJson(Map<String, dynamic> json) => AppNotification(
    id: json['id'] ?? '',
    companyId: json['company_id'] ?? '',
    userId: json['user_id'] ?? '',
    title: json['title'] ?? '',
    message: json['message'] ?? '',
    category: NotificationCategory.fromValue(json['category'] ?? 'system'),
    priority: NotificationPriority.fromValue(json['priority'] ?? 'medium'),
    isRead: json['is_read'] ?? false,
    createdAt: DateTime.parse(json['created_at']),
  );
}
