import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_constants.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/auth_provider.dart';

/// OTP Login Screen (Spec §70 Screen 2)
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _phoneController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  String _countryCode = '+91';

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  void _handleSendOtp() {
    if (_formKey.currentState?.validate() ?? false) {
      final phone = '$_countryCode${_phoneController.text.trim()}';
      ref.read(authProvider.notifier).sendOtp(phone);
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final isLoading = authState.status == AuthStatus.loading;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (AppConstants.demoAuth)
                  Container(
                    margin: const EdgeInsets.only(top: 16),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.primaryLight.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: AppColors.primary),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.info_outline, color: AppColors.primary),
                        const SizedBox(width: 8),
                        Text(
                          'DEMO MODE - OTP = 123456',
                          style: AppTypography.label.copyWith(
                            color: AppColors.primary,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                const SizedBox(height: 60),

                // Logo
                Container(
                  width: 64,
                  height: 64,
                  decoration: BoxDecoration(
                    gradient: AppColors.primaryGradient,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: const Icon(
                    Icons.construction_rounded,
                    size: 32,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 32),

                // Title
                Text(
                  'Welcome to',
                  style: AppTypography.h3.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                Text(
                  AppConstants.appName,
                  style: AppTypography.h1.copyWith(
                    color: AppColors.primary,
                    fontSize: 36,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Enter your phone number to get started',
                  style: AppTypography.caption,
                ),
                const SizedBox(height: 48),

                // Phone Input
                Text(
                  'Phone Number',
                  style: AppTypography.label.copyWith(
                    color: AppColors.textPrimary,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 8),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Country Code
                    Container(
                      height: 56,
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      decoration: BoxDecoration(
                        color: AppColors.surfaceVariant,
                        borderRadius: BorderRadius.circular(
                            AppConstants.inputRadius),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Center(
                        child: DropdownButton<String>(
                          value: _countryCode,
                          underline: const SizedBox(),
                          isDense: true,
                          items: const [
                            DropdownMenuItem(
                              value: '+91',
                              child: Text('🇮🇳 +91'),
                            ),
                            DropdownMenuItem(
                              value: '+1',
                              child: Text('🇺🇸 +1'),
                            ),
                            DropdownMenuItem(
                              value: '+44',
                              child: Text('🇬🇧 +44'),
                            ),
                          ],
                          onChanged: (v) =>
                              setState(() => _countryCode = v ?? '+91'),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    // Phone Field
                    Expanded(
                      child: TextFormField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        inputFormatters: [
                          FilteringTextInputFormatter.digitsOnly,
                          LengthLimitingTextInputFormatter(10),
                        ],
                        style: AppTypography.body,
                        decoration: InputDecoration(
                          hintText: '9876543210',
                          prefixIcon: const Icon(Icons.phone_rounded, size: 20),
                          contentPadding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 16,
                          ),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(
                                AppConstants.inputRadius),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Phone number is required';
                          }
                          if (value.length < 10) {
                            return 'Enter a valid phone number';
                          }
                          return null;
                        },
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 32),

                // Send OTP Button
                PrimaryButton(
                  text: 'Send OTP',
                  onPressed: _handleSendOtp,
                  isLoading: isLoading,
                  icon: Icons.send_rounded,
                ),
                const SizedBox(height: 16),

                // Error
                if (authState.status == AuthStatus.error &&
                    authState.errorMessage != null)
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.dangerLight,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline_rounded,
                            color: AppColors.danger, size: 20),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            authState.errorMessage!,
                            style: AppTypography.bodySmall.copyWith(
                              color: AppColors.dangerDark,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),

                const SizedBox(height: 32),

                // Terms
                Center(
                  child: Text(
                    'By continuing, you agree to our Terms of Service\nand Privacy Policy',
                    style: AppTypography.caption.copyWith(fontSize: 12),
                    textAlign: TextAlign.center,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
