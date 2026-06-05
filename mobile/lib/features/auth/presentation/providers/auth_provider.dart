import 'package:flutter/foundation.dart';
import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/auth_repository.dart';
import '../../domain/entities/user.dart';
import '../../../../core/constants/app_constants.dart';
import '../../../../core/errors/exceptions.dart';

// ── Auth State ──────────────────────────────────────────────
enum AuthStatus {
  initial,
  loading,
  otpSent,
  otpVerified,
  authenticated,
  pendingApproval,
  registering,
  unauthenticated,
  error,
}

class AuthState {
  final AuthStatus status;
  final User? user;
  final String? phone;
  final String? errorMessage;
  final bool isNewUser;
  final int otpCooldownSeconds;
  final String? verificationId;

  const AuthState({
    this.status = AuthStatus.initial,
    this.user,
    this.phone,
    this.errorMessage,
    this.isNewUser = false,
    this.otpCooldownSeconds = 0,
    this.verificationId,
  });

  AuthState copyWith({
    AuthStatus? status,
    User? user,
    String? phone,
    String? errorMessage,
    bool? isNewUser,
    int? otpCooldownSeconds,
    String? verificationId,
  }) =>
      AuthState(
        status: status ?? this.status,
        user: user ?? this.user,
        phone: phone ?? this.phone,
        errorMessage: errorMessage,
        isNewUser: isNewUser ?? this.isNewUser,
        otpCooldownSeconds: otpCooldownSeconds ?? this.otpCooldownSeconds,
        verificationId: verificationId ?? this.verificationId,
      );
}

// ── Auth Notifier ───────────────────────────────────────────
final authProvider =
    StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.read(authRepositoryProvider));
});

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repo;
  Timer? _cooldownTimer;

  AuthNotifier(this._repo) : super(const AuthState());

  /// Check existing session on app start
  Future<void> checkSession() async {
    state = state.copyWith(status: AuthStatus.loading);
    try {
      final hasSession = await _repo.hasValidSession();
      if (hasSession) {
        final user = await _repo.getCurrentUser();
        state = state.copyWith(
          status: AuthStatus.authenticated,
          user: user,
        );
      } else {
        state = state.copyWith(status: AuthStatus.unauthenticated);
      }
    } catch (_) {
      state = state.copyWith(status: AuthStatus.unauthenticated);
    }
  }

  /// Send OTP
  Future<void> sendOtp(String phone) async {
    debugPrint('AuthNotifier: sendOtp() called with phone: $phone');
    debugPrint('AuthNotifier: Current status before sendOtp: ${state.status}');

    state = state.copyWith(status: AuthStatus.loading, phone: phone);
    try {
      await _repo.sendOtp(
        phone: phone,
        verificationCompleted: (credential) async {
          debugPrint('AuthNotifier: verificationCompleted() fired');
          // Auto-resolution (Android only)
          try {
            state = state.copyWith(status: AuthStatus.loading);
            final result = await _repo.signInWithCredential(credential);
            _handleSignInResult(result);
          } catch (e) {
            debugPrint('AuthNotifier: verificationCompleted Error: $e');
            state = state.copyWith(
              status: AuthStatus.error,
              errorMessage: e.toString(),
            );
          }
        },
        verificationFailed: (error) {
          debugPrint('AuthNotifier: verificationFailed() fired.');
          debugPrint('Firebase code: ${error.code}');
          debugPrint('Firebase message: ${error.message}');
          debugPrint('Firebase exception: $error');
          state = state.copyWith(
            status: AuthStatus.error,
            errorMessage: error.message ?? 'Verification failed',
          );
        },
        codeSent: (verificationId, resendToken) {
          debugPrint('AuthNotifier: codeSent() fired with verificationId: $verificationId');
          state = state.copyWith(
            status: AuthStatus.otpSent,
            verificationId: verificationId,
            otpCooldownSeconds: 30,
          );
          _startCooldown();
        },
        codeAutoRetrievalTimeout: (verificationId) {
          debugPrint('AuthNotifier: codeAutoRetrievalTimeout() fired');
          state = state.copyWith(verificationId: verificationId);
        },
      );
      debugPrint('AuthNotifier: sendOtp() repo call completed');
    } catch (e) {
      debugPrint('AuthNotifier: sendOtp() caught error: $e');
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: e.toString(),
      );
    }
  }

  /// Verify OTP
  Future<void> verifyOtp(String code) async {
    state = state.copyWith(status: AuthStatus.loading);
    try {
      if (state.verificationId == null) {
        throw const AuthException(message: 'Session expired. Please request a new OTP.');
      }
      
      final result = await _repo.verifyOtp(state.verificationId!, code);
      await _handleSignInResult(result);
    } catch (e) {
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: e.toString(),
      );
    }
  }

  Future<void> _handleSignInResult(({bool isNewUser, String? accessToken, String? refreshToken}) result) async {
    if (result.isNewUser) {
      state = state.copyWith(
        status: AuthStatus.registering,
        isNewUser: true,
      );
    } else {
      // Fetch user profile
      try {
        final user = await _repo.getCurrentUser();
        if (user.isPending) {
          state = state.copyWith(
            status: AuthStatus.pendingApproval,
            user: user,
          );
        } else {
          state = state.copyWith(
            status: AuthStatus.authenticated,
            user: user,
          );
        }
      } catch (_) {
        // If getting user fails after login, assume registering or error
        state = state.copyWith(
          status: AuthStatus.registering,
          isNewUser: true,
        );
      }
    }
  }

  /// Register worker
  Future<void> register({
    required String firstName,
    required String lastName,
    required String companyId,
    required String departmentId,
    String? contractorId,
    required String designation,
    String? emergencyContactName,
    String? emergencyContactPhone,
  }) async {
    state = state.copyWith(status: AuthStatus.loading);
    try {
      await _repo.register(
        firstName: firstName,
        lastName: lastName,
        phone: state.phone!,
        companyId: companyId,
        departmentId: departmentId,
        contractorId: contractorId,
        designation: designation,
        emergencyContactName: emergencyContactName,
        emergencyContactPhone: emergencyContactPhone,
      );
      if (AppConstants.demoAuth) {
        try {
          final user = await _repo.getCurrentUser();
          state = state.copyWith(
            status: AuthStatus.authenticated,
            user: user,
          );
        } catch (_) {
          // If fetching user fails, fallback to pending
          state = state.copyWith(status: AuthStatus.pendingApproval);
        }
      } else {
        state = state.copyWith(status: AuthStatus.pendingApproval);
      }
    } catch (e) {
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: e.toString(),
      );
    }
  }

  /// Logout
  Future<void> logout([String? reason]) async {
    await _repo.logout();
    state = AuthState(status: AuthStatus.unauthenticated, errorMessage: reason);
  }

  /// Resend OTP
  Future<void> resendOtp() async {
    if (state.otpCooldownSeconds > 0 || state.phone == null) return;
    await sendOtp(state.phone!);
  }

  void _startCooldown() {
    _cooldownTimer?.cancel();
    _cooldownTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (state.otpCooldownSeconds <= 1) {
        timer.cancel();
        state = state.copyWith(otpCooldownSeconds: 0);
      } else {
        state = state.copyWith(
          otpCooldownSeconds: state.otpCooldownSeconds - 1,
        );
      }
    });
  }

  @override
  void dispose() {
    _cooldownTimer?.cancel();
    super.dispose();
  }
}
