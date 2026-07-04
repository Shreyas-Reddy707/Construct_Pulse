# Changelog

All notable changes to ConstructPulse are documented in this file.

The format is inspired by Keep a Changelog.

---

# v0.4.0 – Sprint 4 (Attendance & Occupancy Foundation)

**Released:** July 2026

## Added

### Attendance Lifecycle Foundation (Batch 4A)

- AttendanceService introduced as the domain owner of attendance lifecycle.
- Secure Check-In workflow integrated with AccessVerificationService.
- Secure Check-Out workflow.
- Attendance method tracking.
- Immutable access verification snapshots.

### Attendance Governance (Batch 4B)

- AttendanceGovernanceService.
- Administrative force checkout.
- Attendance correction workflow.
- Immutable AttendanceCorrectionLog.
- GovernanceResult projection.
- Attendance versioning.
- Correction batch tracking.
- Standardized Attendance reason codes.

### Attendance Reporting Foundation (Batch 4C)

- AttendanceReportingService.
- AttendanceReportQuery.
- AttendanceReportRow.
- AttendanceReportResponse.
- Standardized pagination.
- Filtering.
- Streaming CSV exports.
- Report metadata.
- Projection DTO architecture.

### Occupancy Foundation (Batch 4D)

- OccupancyService.
- OccupancyQuery.
- OccupancyDashboard.
- OccupancySummary.
- Department occupancy aggregation.
- Contractor occupancy aggregation.
- Visitor occupancy aggregation.
- Emergency Muster foundation endpoint.
- Occupancy snapshots.
- Snapshot metadata.
- Snapshot projection DTOs.

## Changed

- Attendance controllers refactored into thin controllers.
- Occupancy controllers refactored into thin controllers.
- Business logic centralized into dedicated services.
- Reporting endpoints moved to dedicated reporting module.
- Occupancy calculations migrated from controller logic to optimized SQL aggregations.

## Improved

- Eliminated N+1 occupancy queries.
- Introduced standardized Projection DTO architecture.
- Introduced Query Object pattern.
- Added immutable governance audit trail.
- Improved reporting scalability with pagination and streaming exports.
- Strengthened service boundaries and domain ownership.

---

# Upcoming

## Sprint 5

- Emergency Muster
- Incident Management
- Visitor Operations
- Safety Operations
- Operational Read Models
