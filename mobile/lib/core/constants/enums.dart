// All enumerations as defined in the Master Spec §65

enum UserRole {
  worker('worker', 'Worker'),
  contractor('contractor', 'Contractor'),
  siteEngineer('site_engineer', 'Site Engineer'),
  siteManager('site_manager', 'Site Manager'),
  admin('admin', 'Admin'),
  superAdmin('super_admin', 'Super Admin'),
  municipalityInspector('municipality_inspector', 'Municipality Inspector');

  const UserRole(this.value, this.label);
  final String value;
  final String label;

  static UserRole fromValue(String value) =>
      UserRole.values.firstWhere((e) => e.value == value,
          orElse: () => UserRole.worker);
}

enum UserStatus {
  pending('pending', 'Pending'),
  approved('approved', 'Approved'),
  rejected('rejected', 'Rejected'),
  suspended('suspended', 'Suspended');

  const UserStatus(this.value, this.label);
  final String value;
  final String label;

  static UserStatus fromValue(String value) =>
      UserStatus.values.firstWhere((e) => e.value == value,
          orElse: () => UserStatus.pending);
}

enum TaskStatus {
  notStarted('not_started', 'Not Started'),
  inProgress('in_progress', 'In Progress'),
  blocked('blocked', 'Blocked'),
  completed('completed', 'Completed');

  const TaskStatus(this.value, this.label);
  final String value;
  final String label;

  static TaskStatus fromValue(String value) =>
      TaskStatus.values.firstWhere((e) => e.value == value,
          orElse: () => TaskStatus.notStarted);
}

enum TaskPriority {
  low('low', 'Low'),
  medium('medium', 'Medium'),
  high('high', 'High'),
  critical('critical', 'Critical');

  const TaskPriority(this.value, this.label);
  final String value;
  final String label;

  static TaskPriority fromValue(String value) =>
      TaskPriority.values.firstWhere((e) => e.value == value,
          orElse: () => TaskPriority.medium);
}

enum PlanStatus {
  draft('draft', 'Draft'),
  approved('approved', 'Approved'),
  completed('completed', 'Completed'),
  cancelled('cancelled', 'Cancelled');

  const PlanStatus(this.value, this.label);
  final String value;
  final String label;

  static PlanStatus fromValue(String value) =>
      PlanStatus.values.firstWhere((e) => e.value == value,
          orElse: () => PlanStatus.draft);
}

enum AttendanceStatus {
  checkedIn('checked_in', 'Checked In'),
  checkedOut('checked_out', 'Checked Out');

  const AttendanceStatus(this.value, this.label);
  final String value;
  final String label;

  static AttendanceStatus fromValue(String value) =>
      AttendanceStatus.values.firstWhere((e) => e.value == value,
          orElse: () => AttendanceStatus.checkedOut);
}

enum MusterStatus {
  present('present', 'Present'),
  missing('missing', 'Missing'),
  evacuated('evacuated', 'Evacuated'),
  injured('injured', 'Injured');

  const MusterStatus(this.value, this.label);
  final String value;
  final String label;

  static MusterStatus fromValue(String value) =>
      MusterStatus.values.firstWhere((e) => e.value == value,
          orElse: () => MusterStatus.missing);
}

enum IncidentType {
  fire('fire', 'Fire'),
  collapse('collapse', 'Collapse'),
  accident('accident', 'Accident'),
  evacuation('evacuation', 'Evacuation'),
  safetyIncident('safety_incident', 'Safety Incident'),
  naturalDisaster('natural_disaster', 'Natural Disaster');

  const IncidentType(this.value, this.label);
  final String value;
  final String label;

  static IncidentType fromValue(String value) =>
      IncidentType.values.firstWhere((e) => e.value == value,
          orElse: () => IncidentType.fire);
}

enum PayType {
  daily('daily', 'Daily'),
  hourly('hourly', 'Hourly'),
  monthly('monthly', 'Monthly');

  const PayType(this.value, this.label);
  final String value;
  final String label;

  static PayType fromValue(String value) =>
      PayType.values.firstWhere((e) => e.value == value,
          orElse: () => PayType.daily);
}

enum NotificationCategory {
  attendance('attendance', 'Attendance'),
  planning('planning', 'Planning'),
  task('task', 'Task'),
  emergency('emergency', 'Emergency'),
  inspection('inspection', 'Inspection'),
  payroll('payroll', 'Payroll'),
  system('system', 'System');

  const NotificationCategory(this.value, this.label);
  final String value;
  final String label;

  static NotificationCategory fromValue(String value) =>
      NotificationCategory.values.firstWhere((e) => e.value == value,
          orElse: () => NotificationCategory.system);
}

enum NotificationPriority {
  low('low', 'Low'),
  medium('medium', 'Medium'),
  high('high', 'High'),
  critical('critical', 'Critical');

  const NotificationPriority(this.value, this.label);
  final String value;
  final String label;

  static NotificationPriority fromValue(String value) =>
      NotificationPriority.values.firstWhere((e) => e.value == value,
          orElse: () => NotificationPriority.medium);
}

enum ReportType {
  attendance('attendance', 'Attendance'),
  occupancy('occupancy', 'Occupancy'),
  department('department', 'Department'),
  contractor('contractor', 'Contractor'),
  inspection('inspection', 'Inspection'),
  emergency('emergency', 'Emergency'),
  plannedVsActual('planned_vs_actual', 'Planned vs Actual'),
  planning('planning', 'Planning'),
  payrollPreview('payroll_preview', 'Payroll Preview'),
  timesheet('timesheet', 'Timesheet');

  const ReportType(this.value, this.label);
  final String value;
  final String label;

  static ReportType fromValue(String value) =>
      ReportType.values.firstWhere((e) => e.value == value,
          orElse: () => ReportType.attendance);
}

enum ReportFormat {
  pdf('pdf', 'PDF'),
  excel('excel', 'Excel'),
  csv('csv', 'CSV');

  const ReportFormat(this.value, this.label);
  final String value;
  final String label;
}

enum ReportStatus {
  pending('pending', 'Pending'),
  processing('processing', 'Processing'),
  completed('completed', 'Completed'),
  failed('failed', 'Failed');

  const ReportStatus(this.value, this.label);
  final String value;
  final String label;

  static ReportStatus fromValue(String value) =>
      ReportStatus.values.firstWhere((e) => e.value == value,
          orElse: () => ReportStatus.pending);
}

enum SiteStatus {
  active('active', 'Active'),
  inactive('inactive', 'Inactive');

  const SiteStatus(this.value, this.label);
  final String value;
  final String label;

  static SiteStatus fromValue(String value) =>
      SiteStatus.values.firstWhere((e) => e.value == value,
          orElse: () => SiteStatus.active);
}
