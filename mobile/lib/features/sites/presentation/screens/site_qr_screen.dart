import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:intl/intl.dart';
import '../providers/site_providers.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';

class SiteQrScreen extends ConsumerWidget {
  final String siteId;

  const SiteQrScreen({super.key, required this.siteId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final siteAsync = ref.watch(siteProvider(siteId));
    final qrDataAsync = ref.watch(siteQrProvider(siteId));
    final assignmentsAsync = ref.watch(siteAssignmentsProvider(siteId));

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('Printable Poster'),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: siteAsync.when(
              data: (site) => assignmentsAsync.when(
                data: (assignments) {
                  final assignedWorkersList = (assignments['workers'] as List?) ?? [];
                  final supervisor = assignedWorkersList.cast<dynamic>().firstWhere(
                    (u) => u.role.value == 'Company Admin' || u.role.value == 'Supervisor',
                    orElse: () => null,
                  );

                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Header
                      Column(
                        children: [
                          Image.asset('assets/images/logo.png', height: 80, errorBuilder: (_, __, ___) => const Icon(Icons.business, size: 80, color: AppColors.primary)),
                          const SizedBox(height: 16),
                          Text('Limelite Construction', style: AppTypography.h1.copyWith(fontSize: 28, color: Colors.black)),
                          const SizedBox(height: 8),
                          Text('Masters of Consistency and Quality', style: AppTypography.h4.copyWith(color: AppColors.primary)),
                        ],
                      ),
                      const SizedBox(height: 32),
                      const Divider(color: Colors.black26, thickness: 2),
                      const SizedBox(height: 24),
                      
                      // Site Info
                      Text('SITE DETAILS', style: AppTypography.label.copyWith(color: Colors.grey[700], letterSpacing: 1.5)),
                      const SizedBox(height: 12),
                      Text(site.name, style: AppTypography.h2.copyWith(color: Colors.black)),
                      const SizedBox(height: 8),
                      Text('Site ID: ${site.id.substring(0, 8).toUpperCase()}', style: AppTypography.body.copyWith(fontFamily: 'monospace')),
                      const SizedBox(height: 4),
                      Text(site.address ?? 'Address not specified', style: AppTypography.body),
                      const SizedBox(height: 4),
                      Text('Coordinates: ${site.latitude?.toStringAsFixed(6)}, ${site.longitude?.toStringAsFixed(6)}', style: AppTypography.caption),
                      
                      const SizedBox(height: 24),
                      const Divider(color: Colors.black26, thickness: 2),
                      const SizedBox(height: 24),

                      // Supervisor
                      Text('SUPERVISOR', style: AppTypography.label.copyWith(color: Colors.grey[700], letterSpacing: 1.5)),
                      const SizedBox(height: 12),
                      Text(supervisor != null ? supervisor.fullName : 'Nilesh Patel', style: AppTypography.h3.copyWith(color: Colors.black)),
                      const SizedBox(height: 4),
                      Text(supervisor != null ? supervisor.phone : '+640212869009', style: AppTypography.h4.copyWith(color: Colors.black87)),

                      const SizedBox(height: 24),
                      const Divider(color: Colors.black26, thickness: 2),
                      const SizedBox(height: 32),

                      // QR Code
                      Center(
                        child: qrDataAsync.when(
                          data: (qrData) => Container(
                            padding: const EdgeInsets.all(24),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              border: Border.all(color: Colors.black, width: 4),
                              borderRadius: BorderRadius.circular(16),
                            ),
                            child: QrImageView(
                              data: qrData,
                              size: 300.0,
                            ),
                          ),
                          loading: () => const SizedBox(height: 300, child: Center(child: CircularProgressIndicator())),
                          error: (_, __) => const SizedBox(height: 300, child: Center(child: Text('Error generating QR', style: TextStyle(color: Colors.red)))),
                        ),
                      ),

                      const SizedBox(height: 32),
                      const Divider(color: Colors.black26, thickness: 2),
                      const SizedBox(height: 24),

                      // Instructions
                      Text('WORKER INSTRUCTIONS', style: AppTypography.label.copyWith(color: Colors.grey[700], letterSpacing: 1.5)),
                      const SizedBox(height: 12),
                      _buildInstructionItem('Scan BEFORE entering site'),
                      _buildInstructionItem('Scan AFTER leaving site'),
                      _buildInstructionItem('PPE must be worn at all times'),
                      _buildInstructionItem('Report hazards immediately to supervisor'),

                      const SizedBox(height: 24),
                      Container(
                        padding: const EdgeInsets.all(16),
                        color: Colors.red[50],
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('EMERGENCY CONTACTS', style: AppTypography.h4.copyWith(color: Colors.red[900])),
                            const SizedBox(height: 12),
                            _buildEmergencyContact('Emergency Services', '111'),
                            _buildEmergencyContact('Company Office', '03 925 9705'),
                            _buildEmergencyContact('Site Supervisor', supervisor != null ? supervisor.phone : '+640212869009'),
                          ],
                        ),
                      ),

                      const SizedBox(height: 40),
                      Center(
                        child: Column(
                          children: [
                            Text('Generated ${DateFormat('dd MMM yyyy, HH:mm').format(DateTime.now())}', style: AppTypography.caption),
                            const SizedBox(height: 4),
                            Text('ConstructPulse Attendance System', style: AppTypography.caption.copyWith(fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ),
                      const SizedBox(height: 40),
                    ],
                  );
                },
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (_, __) => const Text('Error loading assignments'),
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (_, __) => const Text('Error loading site'),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInstructionItem(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.check_circle_outline, color: Colors.black54, size: 20),
          const SizedBox(width: 12),
          Expanded(child: Text(text, style: AppTypography.h4.copyWith(color: Colors.black87, fontWeight: FontWeight.normal))),
        ],
      ),
    );
  }

  Widget _buildEmergencyContact(String label, String phone) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: AppTypography.body.copyWith(color: Colors.red[900], fontWeight: FontWeight.bold)),
          Text(phone, style: AppTypography.h4.copyWith(color: Colors.red[900], fontWeight: FontWeight.w900)),
        ],
      ),
    );
  }
}
