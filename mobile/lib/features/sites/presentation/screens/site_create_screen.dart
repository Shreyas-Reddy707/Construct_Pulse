import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../providers/site_providers.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';

class SiteCreateScreen extends ConsumerStatefulWidget {
  const SiteCreateScreen({super.key});

  @override
  ConsumerState<SiteCreateScreen> createState() => _SiteCreateScreenState();
}

class _SiteCreateScreenState extends ConsumerState<SiteCreateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _addressController = TextEditingController();
  final _latController = TextEditingController();
  final _lngController = TextEditingController();
  final _radiusController = TextEditingController();
  bool _enableGps = false;

  @override
  void dispose() {
    _nameController.dispose();
    _addressController.dispose();
    _latController.dispose();
    _lngController.dispose();
    _radiusController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    try {
      final Map<String, dynamic> data = {
        'name': _nameController.text.trim(),
        'address': _addressController.text.trim(),
      };
      
      if (_enableGps) {
        data['latitude'] = double.parse(_latController.text.trim());
        data['longitude'] = double.parse(_lngController.text.trim());
        data['geofence_radius_meters'] = double.parse(_radiusController.text.trim());
      }
      
      await ref.read(siteActionNotifierProvider.notifier).createSite(data);
      if (mounted) {
        context.pop();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Site created successfully!'), backgroundColor: AppColors.success),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed: $e'), backgroundColor: AppColors.danger),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final actionState = ref.watch(siteActionNotifierProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Create Site')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Site Details', style: AppTypography.h3),
              const SizedBox(height: 16),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Site Name', border: OutlineInputBorder()),
                controller: _nameController,
                validator: (v) => v!.isEmpty ? 'Required' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Address', border: OutlineInputBorder()),
                controller: _addressController,
                validator: (v) => v!.isEmpty ? 'Required' : null,
              ),
              const SizedBox(height: 16),
              SwitchListTile(
                title: const Text('Enable GPS Verification'),
                subtitle: const Text('Require workers to be within geofence for QR attendance'),
                value: _enableGps,
                onChanged: (val) => setState(() => _enableGps = val),
                contentPadding: EdgeInsets.zero,
                activeTrackColor: AppColors.primary,
              ),
              if (_enableGps) ...[
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        decoration: const InputDecoration(labelText: 'Latitude', border: OutlineInputBorder()),
                        controller: _latController,
                        keyboardType: const TextInputType.numberWithOptions(decimal: true),
                        validator: (v) => _enableGps && double.tryParse(v ?? '') == null ? 'Invalid' : null,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: TextFormField(
                        decoration: const InputDecoration(labelText: 'Longitude', border: OutlineInputBorder()),
                        controller: _lngController,
                        keyboardType: const TextInputType.numberWithOptions(decimal: true),
                        validator: (v) => _enableGps && double.tryParse(v ?? '') == null ? 'Invalid' : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'Geofence Radius (meters)', border: OutlineInputBorder()),
                  controller: _radiusController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  validator: (v) => _enableGps && double.tryParse(v ?? '') == null ? 'Invalid' : null,
                ),
              ],
              const SizedBox(height: 32),
              PrimaryButton(
                text: 'Create Site',
                isLoading: actionState.isLoading,
                onPressed: _submit,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
