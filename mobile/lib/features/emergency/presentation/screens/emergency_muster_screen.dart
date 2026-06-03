import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../auth/presentation/providers/auth_provider.dart';

/// Emergency Muster Screen (Spec §82)
class EmergencyMusterScreen extends ConsumerStatefulWidget {
  const EmergencyMusterScreen({super.key});

  @override
  ConsumerState<EmergencyMusterScreen> createState() => _EmergencyMusterScreenState();
}

class _EmergencyMusterScreenState extends ConsumerState<EmergencyMusterScreen> {
  bool _generated = false;
  String _selectedType = 'fire';

  final _types = [
    {'id': 'fire', 'label': 'Fire', 'icon': Icons.local_fire_department_rounded},
    {'id': 'collapse', 'label': 'Collapse', 'icon': Icons.domain_disabled_rounded},
    {'id': 'accident', 'label': 'Accident', 'icon': Icons.warning_rounded},
    {'id': 'evacuation', 'label': 'Evacuation', 'icon': Icons.exit_to_app_rounded},
    {'id': 'safety_incident', 'label': 'Safety', 'icon': Icons.health_and_safety_rounded},
  ];

  void _generate() {
    setState(() => _generated = true);
  }

  @override
  Widget build(BuildContext context) {
    final currentUser = ref.watch(authProvider).user;
    final isWorker = currentUser?.isWorker ?? true;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(isWorker ? 'Emergency Actions' : 'Emergency Muster'),
        backgroundColor: AppColors.danger,
        foregroundColor: Colors.white,
      ),
      body: isWorker 
          ? _workerEmergencyView() 
          : (_generated ? _musterReport() : _triggerView()),
    );
  }

  Widget _workerEmergencyView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            gradient: AppColors.emergencyGradient,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(children: [
            const Icon(Icons.warning_rounded, color: Colors.white, size: 64),
            const SizedBox(height: 16),
            Text('EMERGENCY SOS', style: AppTypography.h2.copyWith(color: Colors.white, letterSpacing: 2)),
            const SizedBox(height: 8),
            Text('Tap to immediately alert all site personnel and supervisors.', style: AppTypography.body.copyWith(color: Colors.white70), textAlign: TextAlign.center),
            const SizedBox(height: 24),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: AppColors.danger,
                minimumSize: const Size(double.infinity, 64),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('SOS Alert Raised'), backgroundColor: AppColors.danger));
              },
              child: const Text('RAISE ALARM', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            ),
          ]),
        ),
        const SizedBox(height: 24),
        Text('Quick Actions', style: AppTypography.h4),
        const SizedBox(height: 16),
        ListTile(
          leading: const CircleAvatar(backgroundColor: AppColors.primaryLight, child: Icon(Icons.phone_rounded, color: AppColors.primary)),
          title: const Text('Call Supervisor'),
          subtitle: const Text('John Doe - Site Manager'),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: const BorderSide(color: AppColors.border)),
          onTap: () {},
        ),
        const SizedBox(height: 12),
        ListTile(
          leading: const CircleAvatar(backgroundColor: AppColors.secondaryLight, child: Icon(Icons.contact_phone_rounded, color: AppColors.secondary)),
          title: const Text('Emergency Contacts'),
          subtitle: const Text('View site emergency numbers'),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: const BorderSide(color: AppColors.border)),
          onTap: () {},
        ),
      ]),
    );
  }

  Widget _triggerView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Warning banner
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            gradient: AppColors.emergencyGradient,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Row(children: [
            const Icon(Icons.emergency_rounded, color: Colors.white, size: 40),
            const SizedBox(width: 16),
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Emergency Muster', style: AppTypography.h4.copyWith(color: Colors.white)),
              Text('Generate workforce accountability report', style: AppTypography.caption.copyWith(color: Colors.white70)),
            ])),
          ]),
        ),
        const SizedBox(height: 24),
        Text('Select Incident Type', style: AppTypography.h4),
        const SizedBox(height: 12),
        Wrap(spacing: 8, runSpacing: 8, children: _types.map((t) {
          final sel = _selectedType == t['id'];
          return ChoiceChip(
            label: Row(mainAxisSize: MainAxisSize.min, children: [
              Icon(t['icon'] as IconData, size: 16, color: sel ? Colors.white : AppColors.textSecondary),
              const SizedBox(width: 6),
              Text(t['label'] as String),
            ]),
            selected: sel,
            onSelected: (_) => setState(() => _selectedType = t['id'] as String),
            selectedColor: AppColors.danger,
            labelStyle: TextStyle(color: sel ? Colors.white : AppColors.textPrimary),
          );
        }).toList()),
        const SizedBox(height: 32),
        PrimaryButton(
          text: 'Generate Muster Report',
          backgroundColor: AppColors.danger,
          onPressed: _generate,
          icon: Icons.emergency_rounded,
        ),
        const SizedBox(height: 8),
        Center(child: Text('Report generates in < 5 seconds', style: AppTypography.caption.copyWith(fontSize: 12))),
      ]),
    );
  }

  Widget _musterReport() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Report Header
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: AppColors.dangerLight, borderRadius: BorderRadius.circular(16)),
          child: Column(children: [
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              Text('MUSTER REPORT', style: AppTypography.label.copyWith(color: AppColors.danger, letterSpacing: 2)),
              Text('Live', style: AppTypography.label.copyWith(color: AppColors.danger, fontWeight: FontWeight.w700)),
            ]),
            const SizedBox(height: 12),
            Row(children: [
              _reportKpi('--', 'Present', AppColors.success),
              _reportKpi('--', 'Missing', AppColors.danger),
              _reportKpi('--', 'Depts', AppColors.primary),
              _reportKpi('--', 'Contractors', AppColors.secondary),
            ]),
          ]),
        ),
        const SizedBox(height: 20),

        Text('Missing Workers', style: AppTypography.h4.copyWith(color: AppColors.danger)),
        const SizedBox(height: 8),
        const Text('No missing workers data available.'),
        const SizedBox(height: 16),

        // Department Summary
        Text('Department Summary', style: AppTypography.h4),
        const SizedBox(height: 8),
        const Text('No department data available.'),
        const SizedBox(height: 24),
        PrimaryButton(text: 'Export Report', icon: Icons.download_rounded, onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Feature available in future release')));
        }),
      ]),
    );
  }

  Widget _reportKpi(String value, String label, Color color) {
    return Expanded(child: Column(children: [
      Text(value, style: AppTypography.h3.copyWith(color: color)),
      Text(label, style: AppTypography.caption.copyWith(fontSize: 11)),
    ]));
  }
}
