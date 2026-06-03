import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/auth_provider.dart';
import '../../../company/presentation/providers/company_providers.dart';

/// Worker Registration Screen (Spec §70 Screen 4)
class RegistrationScreen extends ConsumerStatefulWidget {
  const RegistrationScreen({super.key});

  @override
  ConsumerState<RegistrationScreen> createState() => _RegistrationScreenState();
}

class _RegistrationScreenState extends ConsumerState<RegistrationScreen> {
  final _formKey = GlobalKey<FormState>();
  final _firstNameCtrl = TextEditingController();
  final _lastNameCtrl = TextEditingController();
  final _designationCtrl = TextEditingController();
  final _emergNameCtrl = TextEditingController();
  final _emergPhoneCtrl = TextEditingController();
  String? _companyId;
  String? _deptId;
  String? _contractorId;

  @override
  void dispose() {
    _firstNameCtrl.dispose();
    _lastNameCtrl.dispose();
    _designationCtrl.dispose();
    _emergNameCtrl.dispose();
    _emergPhoneCtrl.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState?.validate() ?? false) {
      if (_companyId == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Please select a Company'),
            backgroundColor: AppColors.danger,
          ),
        );
        return;
      }
      if (_deptId == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Please select a Department'),
            backgroundColor: AppColors.danger,
          ),
        );
        return;
      }
      debugPrint('Registration Submit: Selected Company ID = $_companyId, Department ID = $_deptId, Contractor ID = $_contractorId');
      ref.read(authProvider.notifier).register(
        firstName: _firstNameCtrl.text.trim(),
        lastName: _lastNameCtrl.text.trim(),
        companyId: _companyId!,
        departmentId: _deptId!,
        contractorId: _contractorId,
        designation: _designationCtrl.text.trim(),
        emergencyContactName: _emergNameCtrl.text.trim(),
        emergencyContactPhone: _emergPhoneCtrl.text.trim(),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(authProvider);
    final loading = state.status == AuthStatus.loading;

    final companiesAsync = ref.watch(publicCompaniesProvider);
    final deptsAsync = ref.watch(publicDepartmentsProvider);
    final contractorsAsync = ref.watch(publicContractorsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Complete Registration')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _info(),
              const SizedBox(height: 24),
              _section('Personal Information'),
              const SizedBox(height: 12),
              _field('First Name', _firstNameCtrl, Icons.person_outline_rounded,
                  required: true),
              const SizedBox(height: 16),
              _field('Last Name', _lastNameCtrl, Icons.person_outline_rounded,
                  required: true),
              const SizedBox(height: 16),
              _field('Designation', _designationCtrl, Icons.badge_outlined,
                  hint: 'e.g., Electrician', required: true),
              const SizedBox(height: 24),
              _section('Work Information'),
              const SizedBox(height: 12),
              companiesAsync.when(
                data: (companies) => _dropdown(
                  'Company', 
                  _companyId, 
                  companies.map((c) => {'id': c.id, 'name': c.companyName}).toList(), 
                  (v) {
                    debugPrint('Company selected: $v');
                    setState(() => _companyId = v);
                  }, 
                  required: true
                ),
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error loading companies: $err'),
              ),
              const SizedBox(height: 16),
              deptsAsync.when(
                data: (depts) => _dropdown(
                  'Department', 
                  _deptId, 
                  depts.map((d) => {'id': d.id, 'name': d.name}).toList(), 
                  (v) {
                    debugPrint('Department selected: $v');
                    setState(() => _deptId = v);
                  }, 
                  required: true
                ),
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error loading departments: $err'),
              ),
              const SizedBox(height: 16),
              contractorsAsync.when(
                data: (contractors) => _dropdown(
                  'Contractor (Optional)', 
                  _contractorId, 
                  contractors.map((c) => {'id': c.id, 'name': c.name}).toList(), 
                  (v) {
                    debugPrint('Contractor selected: $v');
                    setState(() => _contractorId = v);
                  }
                ),
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error loading contractors: $err'),
              ),
              const SizedBox(height: 24),
              _section('Emergency Contact'),
              const SizedBox(height: 12),
              _field('Contact Name', _emergNameCtrl, Icons.emergency_rounded),
              const SizedBox(height: 16),
              _field('Contact Phone', _emergPhoneCtrl, Icons.phone_rounded,
                  keyboard: TextInputType.phone),
              const SizedBox(height: 32),
              PrimaryButton(
                text: 'Submit Registration',
                onPressed: loading || _companyId == null || _deptId == null ? null : _submit,
                isLoading: loading,
                icon: Icons.check_circle_outline_rounded,
              ),
              const SizedBox(height: 16),
              Center(child: Text('Your registration will be reviewed by an admin',
                  style: AppTypography.caption.copyWith(fontSize: 12),
                  textAlign: TextAlign.center)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _info() => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: AppColors.primarySurface, borderRadius: BorderRadius.circular(12)),
    child: Row(children: [
      const Icon(Icons.person_add_rounded, color: AppColors.primary),
      const SizedBox(width: 12),
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Worker Registration', style: AppTypography.bodySmall.copyWith(
            fontWeight: FontWeight.w600, color: AppColors.primaryDark)),
        Text('Fill in your details to join', style: AppTypography.caption.copyWith(
            fontSize: 12, color: AppColors.primary)),
      ])),
    ]),
  );

  Widget _section(String t) => Text(t, style: AppTypography.h4.copyWith(fontSize: 16));

  Widget _field(String label, TextEditingController ctrl, IconData icon,
      {String? hint, bool required = false, TextInputType keyboard = TextInputType.text}) {
    return TextFormField(
      controller: ctrl, keyboardType: keyboard, style: AppTypography.body,
      decoration: InputDecoration(labelText: label, hintText: hint, prefixIcon: Icon(icon, size: 20)),
      validator: required ? (v) => v?.isEmpty == true ? '$label is required' : null : null,
    );
  }

  Widget _dropdown(String label, String? value, List<Map<String, String>> items,
      void Function(String?) onChanged, {bool required = false}) {
    return DropdownButtonFormField<String>(
      initialValue: value,
      decoration: InputDecoration(labelText: label, prefixIcon: const Icon(Icons.list_rounded, size: 20)),
      items: items.map((i) => DropdownMenuItem(value: i['id'], child: Text(i['name']!))).toList(),
      onChanged: onChanged, style: AppTypography.body,
      validator: required ? (v) => v == null ? '$label is required' : null : null,
    );
  }
}
