import 'package:equatable/equatable.dart';
import '../../../../core/constants/enums.dart';

class Attendance extends Equatable {
  final String id;
  final String userId;
  final String siteId;
  final String? siteName;
  final DateTime checkInTime;
  final DateTime? checkOutTime;
  final AttendanceStatus status;

  const Attendance({
    required this.id,
    required this.userId,
    required this.siteId,
    this.siteName,
    required this.checkInTime,
    this.checkOutTime,
    required this.status,
  });

  factory Attendance.fromJson(Map<String, dynamic> json) {
    return Attendance(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      siteId: json['site_id'] as String,
      siteName: json['site_name'] as String?,
      checkInTime: DateTime.parse(json['check_in_time'] as String),
      checkOutTime: json['check_out_time'] != null
          ? DateTime.parse(json['check_out_time'] as String)
          : null,
      status: AttendanceStatus.fromValue(json['status'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'site_id': siteId,
      if (siteName != null) 'site_name': siteName,
      'check_in_time': checkInTime.toIso8601String(),
      'check_out_time': checkOutTime?.toIso8601String(),
      'status': status.value,
    };
  }

  @override
  List<Object?> get props => [
        id,
        userId,
        siteId,
        siteName,
        checkInTime,
        checkOutTime,
        status,
      ];
}
