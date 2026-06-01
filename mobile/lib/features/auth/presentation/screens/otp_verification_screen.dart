import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_constants.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/auth_provider.dart';

/// OTP Verification Screen (Spec §70 Screen 3)
class OtpVerificationScreen extends ConsumerStatefulWidget {
  const OtpVerificationScreen({super.key});

  @override
  ConsumerState<OtpVerificationScreen> createState() =>
      _OtpVerificationScreenState();
}

class _OtpVerificationScreenState
    extends ConsumerState<OtpVerificationScreen> {
  final List<TextEditingController> _controllers =
      List.generate(AppConstants.otpLength, (_) => TextEditingController());
  final List<FocusNode> _focusNodes =
      List.generate(AppConstants.otpLength, (_) => FocusNode());

  @override
  void dispose() {
    for (final c in _controllers) {
      c.dispose();
    }
    for (final f in _focusNodes) {
      f.dispose();
    }
    super.dispose();
  }

  String get _otp => _controllers.map((c) => c.text).join();
  bool get _isOtpComplete => _otp.length == AppConstants.otpLength;

  void _handleVerify() {
    if (_isOtpComplete) {
      ref.read(authProvider.notifier).verifyOtp(_otp);
    }
  }

  void _onDigitEntered(String value, int index) {
    if (value.isNotEmpty && index < AppConstants.otpLength - 1) {
      _focusNodes[index + 1].requestFocus();
    }
    if (_isOtpComplete) {
      _handleVerify();
    }
  }


  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final isLoading = authState.status == AuthStatus.loading;
    final phone = authState.phone ?? '';

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 24),

              if (AppConstants.demoAuth)
                Container(
                  margin: const EdgeInsets.only(bottom: 24),
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

              // Header
              Text(
                'Verify OTP',
                style: AppTypography.h2,
              ),
              const SizedBox(height: 8),
              RichText(
                text: TextSpan(
                  style: AppTypography.caption,
                  children: [
                    const TextSpan(text: 'We sent a verification code to '),
                    TextSpan(
                      text: phone,
                      style: AppTypography.bodySmall.copyWith(
                        fontWeight: FontWeight.w600,
                        color: AppColors.textPrimary,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 48),

              // OTP Fields
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: List.generate(AppConstants.otpLength, (index) {
                  return SizedBox(
                    width: 50,
                    height: 60,
                    child: TextFormField(
                      controller: _controllers[index],
                      focusNode: _focusNodes[index],
                      keyboardType: TextInputType.number,
                      textAlign: TextAlign.center,
                      maxLength: 1,
                      style: AppTypography.h3.copyWith(
                        fontWeight: FontWeight.w700,
                      ),
                      inputFormatters: [
                        FilteringTextInputFormatter.digitsOnly,
                      ],
                      decoration: InputDecoration(
                        counterText: '',
                        contentPadding: EdgeInsets.zero,
                        filled: true,
                        fillColor: _controllers[index].text.isNotEmpty
                            ? AppColors.primarySurface
                            : AppColors.surfaceVariant,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide.none,
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(
                            color: AppColors.primary,
                            width: 2,
                          ),
                        ),
                      ),
                      onChanged: (v) {
                        setState(() {});
                        _onDigitEntered(v, index);
                      },
                      onEditingComplete: () {},
                    ),
                  );
                }),
              ),
              const SizedBox(height: 32),

              // Verify Button
              PrimaryButton(
                text: 'Verify & Continue',
                onPressed: _isOtpComplete ? _handleVerify : null,
                isLoading: isLoading,
                icon: Icons.verified_rounded,
              ),
              const SizedBox(height: 24),

              // Resend
              Center(
                child: authState.otpCooldownSeconds > 0
                    ? Text(
                        'Resend OTP in ${authState.otpCooldownSeconds}s',
                        style: AppTypography.caption,
                      )
                    : TextButton(
                        onPressed: () =>
                            ref.read(authProvider.notifier).resendOtp(),
                        child: Text(
                          'Resend OTP',
                          style: AppTypography.button.copyWith(
                            color: AppColors.primary,
                          ),
                        ),
                      ),
              ),

              // Error
              if (authState.status == AuthStatus.error &&
                  authState.errorMessage != null) ...[
                const SizedBox(height: 16),
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
              ],
            ],
          ),
        ),
      ),
    );
  }
}
