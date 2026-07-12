import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/auth_provider.dart';
import '../../../company/presentation/providers/company_providers.dart';
import '../../../company/domain/entities/company.dart';
import '../../../company/domain/entities/department.dart';
import '../../../company/domain/entities/contractor.dart';

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
  String? _trade;
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

  void _showContractorSelector(List<Contractor> contractors, List<Company> companies) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: AppColors.surface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) {
        return DraggableScrollableSheet(
          expand: false,
          initialChildSize: 0.6,
          maxChildSize: 0.9,
          builder: (_, controller) {
            return Column(
              children: [
                const SizedBox(height: 16),
                Container(width: 40, height: 4, decoration: BoxDecoration(color: AppColors.surfaceVariant, borderRadius: BorderRadius.circular(2))),
                const SizedBox(height: 16),
                Text('Select Contractor', style: AppTypography.h3),
                const SizedBox(height: 16),
                Expanded(
                  child: ListView.separated(
                    controller: controller,
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                    itemCount: contractors.length,
                    separatorBuilder: (_, __) => const Divider(height: 1),
                    itemBuilder: (ctx, i) {
                      final c = contractors[i];
                      final compName = companies.firstWhere((cp) => cp.id == c.companyId, orElse: () => const Company(id: '', companyName: 'Unknown', name: 'Unknown')).companyName;
                      return InkWell(
                        onTap: () {
                          setState(() {
                            _contractorId = c.id;
                          });
                          Navigator.pop(ctx);
                        },
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(c.name, style: AppTypography.body.copyWith(fontWeight: FontWeight.w600)),
                              const SizedBox(height: 4),
                              if (c.trade != null) Text('Trade: ${c.trade}', style: AppTypography.caption),
                              Text('Phone: ${c.phone}', style: AppTypography.caption),
                              Text('Company: $compName', style: AppTypography.caption),
                              Text('ID: ${c.id.substring(0, 8)}', style: AppTypography.caption.copyWith(color: AppColors.textTertiary, fontSize: 10)),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            );
          },
        );
      },
    );
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
              _field('First Name', _firstNameCtrl, Icons.person_outline_rounded, required: true),
              const SizedBox(height: 16),
              _field('Last Name', _lastNameCtrl, Icons.person_outline_rounded, required: true),
              const SizedBox(height: 16),
              _field('Designation', _designationCtrl, Icons.badge_outlined, hint: 'e.g., Electrician', required: true),
              const SizedBox(height: 24),
              _section('Work Information'),
              const SizedBox(height: 12),
              
              companiesAsync.when(
                data: (companies) => _dropdown(
                  'Company', 
                  _companyId, 
                  companies.map((c) => {'id': c.id, 'name': c.companyName}).toList(), 
                  (v) {
                    setState(() {
                      _companyId = v;
                      _deptId = null;
                      _trade = null;
                      _contractorId = null;
                    });
                  }, 
                  required: true
                ),
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (err, _) => Text('Error loading companies: $err'),
              ),
              const SizedBox(height: 16),
              
              if (_companyId != null)
                deptsAsync.when(
                  data: (depts) {
                    final filteredDepts = depts.where((d) => d.companyId == _companyId).toList();
                    return _dropdown(
                      'Department', 
                      _deptId, 
                      filteredDepts.map((d) => {'id': d.id, 'name': d.name}).toList(), 
                      (v) {
                        setState(() {
                          _deptId = v;
                          _trade = null;
                          _contractorId = null;
                        });
                      }, 
                      required: true
                    );
                  },
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (err, _) => Text('Error loading departments: $err'),
                ),
              if (_companyId != null) const SizedBox(height: 16),

              if (_deptId != null)
                contractorsAsync.when(
                  data: (contractors) {
                    final companyContractors = contractors.where((c) => c.companyId == _companyId).toList();
                    final trades = companyContractors.map((c) => c.trade ?? 'Other').toSet().toList()..sort();
                    
                    if (trades.isEmpty) return const SizedBox.shrink();
                    
                    return _dropdown(
                      'Trade', 
                      _trade, 
                      trades.map((t) => {'id': t, 'name': t}).toList(), 
                      (v) {
                        setState(() {
                          _trade = v;
                          _contractorId = null;
                        });
                      }
                    );
                  },
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (err, _) => Text('Error loading contractors: $err'),
                ),
              if (_deptId != null) const SizedBox(height: 16),

              if (_trade != null)
                contractorsAsync.when(
                  data: (contractors) {
                    final filteredContractors = contractors.where((c) => 
                      c.companyId == _companyId && 
                      (c.trade == _trade || (c.trade == null && _trade == 'Other'))
                    ).toList();

                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Contractor (Optional)', style: AppTypography.caption),
                        const SizedBox(height: 8),
                        InkWell(
                          onTap: () {
                            if (filteredContractors.isNotEmpty) {
                              _showContractorSelector(filteredContractors, companiesAsync.value ?? []);
                            }
                          },
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                            decoration: BoxDecoration(
                              border: Border.all(color: AppColors.border),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.business_center_outlined, size: 20, color: AppColors.textSecondary),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Text(
                                    _contractorId == null 
                                      ? (filteredContractors.isEmpty ? 'No contractors available' : 'Select a Contractor')
                                      : filteredContractors.firstWhere((c) => c.id == _contractorId, orElse: () => const Contractor(id: '', name: 'Unknown', phone: '')).name,
                                    style: AppTypography.body,
                                  ),
                                ),
                                const Icon(Icons.arrow_drop_down, color: AppColors.textSecondary),
                              ],
                            ),
                          ),
                        ),
                        if (_contractorId != null)
                          Align(
                            alignment: Alignment.centerRight,
                            child: TextButton(
                              onPressed: () => setState(() => _contractorId = null),
                              child: const Text('Clear Selection'),
                            ),
                          ),
                      ],
                    );
                  },
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (err, _) => Text('Error loading contractors: $err'),
                ),

              const SizedBox(height: 24),
              _section('Emergency Contact'),
              const SizedBox(height: 12),
              _field('Contact Name', _emergNameCtrl, Icons.emergency_rounded),
              const SizedBox(height: 16),
              _field('Contact Phone', _emergPhoneCtrl, Icons.phone_rounded, keyboard: TextInputType.phone),
              const SizedBox(height: 32),
              PrimaryButton(
                text: 'Submit Registration',
                onPressed: loading || _companyId == null || _deptId == null ? null : _submit,
                isLoading: loading,
                icon: Icons.check_circle_outline_rounded,
              ),
              const SizedBox(height: 16),
              Center(child: Text('Your registration will be reviewed by an admin', style: AppTypography.caption.copyWith(fontSize: 12), textAlign: TextAlign.center)),
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
      value: items.any((i) => i['id'] == value) ? value : null,
      decoration: InputDecoration(labelText: label, prefixIcon: const Icon(Icons.list_rounded, size: 20)),
      items: items.map((i) => DropdownMenuItem(value: i['id'], child: Text(i['name']!))).toList(),
      onChanged: onChanged, style: AppTypography.body,
      validator: required ? (v) => v == null ? '$label is required' : null : null,
    );
  }
}
