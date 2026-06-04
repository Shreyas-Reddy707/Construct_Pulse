/// All API endpoints as defined in OpenAPI V1.1–V1.5
class ApiEndpoints {
  ApiEndpoints._();

  // ── Auth (V1.1) ──────────────────────────────────────────
  static const String login = '/auth/login';
  static const String sendOtp = '/auth/send-otp';
  static const String verifyOtp = '/auth/verify-otp';
  static const String refreshToken = '/auth/refresh';
  static const String logout = '/auth/logout';
  static const String register = '/auth/register';

  // ── Companies (V1.1) ─────────────────────────────────────
  static const String companies = '/companies';
  static const String publicCompanies = '/public/companies';
  static String company(String id) => '/companies/$id';

  // ── Users (V1.1) ─────────────────────────────────────────
  static const String users = '/users';
  static String user(String id) => '/users/$id';
  static String approveUser(String id) => '/users/$id/approve';
  static String rejectUser(String id) => '/users/$id/reject';
  static String suspendUser(String id) => '/users/$id/suspend';

  // ── Departments (V1.1) ───────────────────────────────────
  static const String departments = '/departments';
  static const String publicDepartments = '/public/departments';
  static String department(String id) => '/departments/$id';

  // ── Contractors (V1.1) ───────────────────────────────────
  static const String contractors = '/contractors';
  static const String publicContractors = '/public/contractors';
  static String contractor(String id) => '/contractors/$id';

  // ── Sites (V1.2) ─────────────────────────────────────────
  static const String sites = '/sites';
  static String site(String id) => '/sites/$id';
  static String generateQr(String siteId) => '/sites/$siteId/qr/generate';
  static String siteQr(String siteId) => '/sites/$siteId/qr';
  static String downloadQr(String siteId) => '/sites/$siteId/qr/download';
  static String regenerateQr(String siteId) => '/sites/$siteId/qr/regenerate';
  static String assignWorker(String siteId) => '/sites/$siteId/assign-worker';
  static String removeWorker(String siteId, String userId) =>
      '/sites/$siteId/workers/$userId';
  static String assignContractor(String siteId) =>
      '/sites/$siteId/assign-contractor';
  static String siteWorkers(String siteId) => '/sites/$siteId/workers';
  static String siteContractors(String siteId) =>
      '/sites/$siteId/contractors';

  // ── Attendance (V1.2) ────────────────────────────────────
  static const String checkIn = '/attendance/check-in';
  static const String checkOut = '/attendance/check-out';
  static const String attendanceScan = '/attendance/scan';
  static const String attendanceToday = '/attendance/today';
  static const String attendanceHistory = '/attendance/history';
  static String siteAttendance(String siteId) => '/attendance/site/$siteId';
  static String userAttendance(String userId) => '/attendance/worker/$userId';
  static String userAttendanceHistory(String userId) => '/attendance/history/$userId';
  static const String liveAttendance = '/attendance/live';
  static const String occupancy = '/attendance/occupancy';
  static const String attendanceSummary = '/attendance/summary';
  static String attendanceEvents(String attendanceId) =>
      '/attendance/$attendanceId/events';
  static String attendanceGps(String attendanceId) =>
      '/attendance/$attendanceId/gps';

  // ── Timesheets (V1.2) ────────────────────────────────────
  static const String myTimesheet = '/timesheets/me';
  static String userTimesheet(String userId) => '/timesheets/users/$userId';
  static String siteTimesheet(String siteId) => '/timesheets/site/$siteId';

  // ── Occupancy (V1.2) ─────────────────────────────────────
  static const String currentOccupancy = '/occupancy/current';
  static String siteOccupancy(String siteId) => '/occupancy/site/$siteId';
  static String occupancyDepartments(String siteId) =>
      '/occupancy/site/$siteId/departments';
  static String occupancyContractors(String siteId) =>
      '/occupancy/site/$siteId/contractors';
  static String occupancyWorkers(String siteId) =>
      '/occupancy/site/$siteId/workers';
  static String occupancyTrend(String siteId) =>
      '/occupancy/site/$siteId/trend';

  // ── Plans (V1.3) ─────────────────────────────────────────
  static const String plans = '/plans';
  static String plan(String id) => '/plans/$id';
  static String approvePlan(String id) => '/plans/$id/approve';
  static String completePlan(String id) => '/plans/$id/complete';
  static String planWorkforce(String planId) => '/plans/$planId/workforce';
  static String planWorkforceItem(String planId, String wfId) =>
      '/plans/$planId/workforce/$wfId';
  static String planTasks(String planId) => '/plans/$planId/tasks';
  static String planTask(String planId, String taskId) =>
      '/plans/$planId/tasks/$taskId';

  // ── Variance (V1.3) ──────────────────────────────────────
  static String siteVariance(String siteId) => '/variance/site/$siteId';
  static String planVariance(String planId) => '/variance/plan/$planId';
  static String deptVariance(String siteId) =>
      '/variance/site/$siteId/departments';
  static String contractorVariance(String siteId) =>
      '/variance/site/$siteId/contractors';
  static String shortages(String siteId) =>
      '/variance/site/$siteId/shortages';
  static String surplus(String siteId) => '/variance/site/$siteId/surplus';
  static String varianceTrend(String siteId) =>
      '/variance/site/$siteId/trend';

  // ── Tasks (V1.3) ─────────────────────────────────────────
  static const String tasks = '/tasks';
  static String task(String id) => '/tasks/$id';
  static String assignTask(String id) => '/tasks/$id/assign';
  static String startTask(String id) => '/tasks/$id/start';
  static String completeTask(String id) => '/tasks/$id/complete';
  static String blockTask(String id) => '/tasks/$id/block';
  static String taskProgress(String id) => '/tasks/$id/progress';
  static String taskAttachments(String id) => '/tasks/$id/attachments';
  static String siteTaskSummary(String siteId) =>
      '/tasks/site/$siteId/summary';
  static String siteDeptTasks(String siteId) =>
      '/tasks/site/$siteId/departments';
  static String siteTaskTrend(String siteId) => '/tasks/site/$siteId/trend';

  // ── Emergency (V1.4) ─────────────────────────────────────
  static const String generateMuster = '/emergency/muster';
  static String musterReport(String id) => '/emergency/muster/$id';
  static String musterWorkers(String id) => '/emergency/muster/$id/workers';
  static String musterMissing(String id) => '/emergency/muster/$id/missing';
  static String musterDepts(String id) =>
      '/emergency/muster/$id/departments';
  static String musterContractors(String id) =>
      '/emergency/muster/$id/contractors';
  static const String emergencyHistory = '/emergency/history';
  static String exportMuster(String id) => '/emergency/muster/$id/export';

  // ── Inspection (V1.4) ────────────────────────────────────
  static const String inspectionDashboard = '/inspection/dashboard';
  static String siteInspection(String siteId) => '/inspection/site/$siteId';
  static String inspectionOccupancy(String siteId) =>
      '/inspection/site/$siteId/occupancy';
  static String inspectionWorkforce(String siteId) =>
      '/inspection/site/$siteId/workforce';
  static String inspectionDepts(String siteId) =>
      '/inspection/site/$siteId/departments';
  static String inspectionContractors(String siteId) =>
      '/inspection/site/$siteId/contractors';
  static const String inspectionLogs = '/inspection/logs';
  static String inspectionLog(String id) => '/inspection/logs/$id';

  // ── Reports (V1.4) ───────────────────────────────────────
  static const String generateReport = '/reports/generate';
  static String reportStatus(String id) => '/reports/$id/status';
  static const String reports = '/reports';
  static String report(String id) => '/reports/$id';
  static String downloadReport(String id) => '/reports/$id/download';
  static String reportPdf(String id) => '/reports/$id/pdf';
  static String reportExcel(String id) => '/reports/$id/excel';
  static String reportCsv(String id) => '/reports/$id/csv';

  // ── Municipality Reports (V1.4) ──────────────────────────
  static const String municipalityOccupancy =
      '/reports/municipality/occupancy';
  static const String municipalityWorkforce =
      '/reports/municipality/workforce';
  static const String municipalityEmergency =
      '/reports/municipality/emergency';
  static const String municipalityPlannedVsActual =
      '/reports/municipality/planned-vs-actual';

  // ── Compliance (V1.4) ────────────────────────────────────
  static const String complianceSummary = '/compliance/summary';
  static String complianceSite(String siteId) => '/compliance/site/$siteId';

  // ── Payroll (V1.5) ───────────────────────────────────────
  static const String myPayroll = '/payroll/me';
  static String userPayroll(String userId) => '/payroll/users/$userId';
  static String sitePayroll(String siteId) => '/payroll/site/$siteId';
  static const String payrollProfile = '/payroll/profile';
  static String updatePayrollProfile(String userId) =>
      '/payroll/profile/$userId';
  static const String payrollTrend = '/payroll/trend';

  // ── Notifications (V1.5) ─────────────────────────────────
  static const String notifications = '/notifications';
  static String notification(String id) => '/notifications/$id';
  static String markRead(String id) => '/notifications/$id/read';
  static const String markAllRead = '/notifications/read-all';

  // ── Analytics (V1.5) ─────────────────────────────────────
  static const String executiveDashboard = '/analytics/executive';
  static const String companyDashboard = '/analytics/company';
  static String siteDashboard(String siteId) => '/analytics/site/$siteId';
  static const String municipalityDashboard = '/analytics/municipality';

  // ── KPIs (V1.5) ──────────────────────────────────────────
  static const String workforceKpis = '/analytics/kpis/workforce';
  static const String attendanceKpis = '/analytics/kpis/attendance';
  static const String planningKpis = '/analytics/kpis/planning';
  static const String contractorKpis = '/analytics/kpis/contractors';
  static const String departmentKpis = '/analytics/kpis/departments';

  // ── Trends (V1.5) ────────────────────────────────────────
  static const String attendanceTrend = '/analytics/trends/attendance';
  static const String occupancyAnalyticsTrend = '/analytics/trends/occupancy';
  static const String workforceGrowthTrend =
      '/analytics/trends/workforce-growth';
  static const String contractorTrend = '/analytics/trends/contractors';
  static const String departmentTrend = '/analytics/trends/departments';

  // ── Planning Analytics (V1.5) ─────────────────────────────
  static const String planningAccuracy = '/analytics/planning/accuracy';
  static const String planningVarianceTrend =
      '/analytics/planning/variance-trend';
  static String sitePlanningAccuracy(String siteId) =>
      '/analytics/planning/site/$siteId';
  static const String contractorPlanningAccuracy =
      '/analytics/planning/contractors';
  static const String departmentPlanningAccuracy =
      '/analytics/planning/departments';
}
