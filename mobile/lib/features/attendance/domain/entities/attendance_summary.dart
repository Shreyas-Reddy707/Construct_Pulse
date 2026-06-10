class AttendanceSummary {
  final bool checkedIn;
  final String? siteId;
  final String? siteName;
  final String? checkInTime;
  final String? checkOutTime;
  final double hoursToday;

  AttendanceSummary({
    required this.checkedIn,
    this.siteId,
    this.siteName,
    this.checkInTime,
    this.checkOutTime,
    required this.hoursToday,
  });

  factory AttendanceSummary.fromJson(Map<String, dynamic> json) {
    return AttendanceSummary(
      checkedIn: json['checked_in'] as bool? ?? false,
      siteId: json['site_id'] as String?,
      siteName: json['site_name'] as String?,
      checkInTime: json['check_in_time'] as String?,
      checkOutTime: json['check_out_time'] as String?,
      hoursToday: (json['hours_today'] as num?)?.toDouble() ?? 0.0,
    );
  }
}
