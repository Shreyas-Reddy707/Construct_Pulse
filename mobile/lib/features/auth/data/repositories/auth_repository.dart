import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/storage/secure_storage.dart';
import '../../../../core/constants/app_constants.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/user.dart';

import 'package:firebase_auth/firebase_auth.dart' as firebase;

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(ref.read(dioProvider), ref.read(secureStorageProvider));
});

/// Auth repository handling OTP login, registration, and session management
class AuthRepository {
  final Dio _dio;
  final SecureStorageService _storage;
  final firebase.FirebaseAuth _firebaseAuth = firebase.FirebaseAuth.instance;

  AuthRepository(this._dio, this._storage);

  /// Send OTP to phone number
  Future<void> sendOtp({
    required String phone,
    required Function(firebase.PhoneAuthCredential) verificationCompleted,
    required Function(firebase.FirebaseAuthException) verificationFailed,
    required Function(String, int?) codeSent,
    required Function(String) codeAutoRetrievalTimeout,
  }) async {
    debugPrint('AuthRepository: sendOtp() starting for phone: $phone');
    try {
      await _firebaseAuth.verifyPhoneNumber(
        phoneNumber: phone,
        verificationCompleted: verificationCompleted,
        verificationFailed: verificationFailed,
        codeSent: codeSent,
        codeAutoRetrievalTimeout: codeAutoRetrievalTimeout,
      );
      debugPrint('AuthRepository: verifyPhoneNumber() called without throwing synchronous exception');
    } catch (e) {
      debugPrint('AuthRepository: sendOtp() caught exception: $e');
      throw AuthException(message: e.toString());
    }
  }

  /// Verify OTP
  Future<({bool isNewUser, String? accessToken, String? refreshToken})> verifyOtp(
      String verificationId, String smsCode) async {
    try {
      final credential = firebase.PhoneAuthProvider.credential(
        verificationId: verificationId,
        smsCode: smsCode,
      );
      return await signInWithCredential(credential);
    } on firebase.FirebaseAuthException catch (e) {
      throw AuthException(message: e.message ?? 'Invalid OTP');
    } catch (e) {
      throw AuthException(message: 'Verification failed: $e');
    }
  }

  /// Sign in with credential and exchange for JWT
  Future<({bool isNewUser, String? accessToken, String? refreshToken})> signInWithCredential(
      firebase.PhoneAuthCredential credential) async {
    try {
      final userCredential = await _firebaseAuth.signInWithCredential(credential);
      final idToken = await userCredential.user?.getIdToken();
      
      if (idToken == null) throw const AuthException(message: 'Failed to get Firebase ID token');
      
      return await loginWithFirebaseToken(idToken);
    } on firebase.FirebaseAuthException catch (e) {
      throw AuthException(message: e.message ?? 'Authentication failed');
    }
  }

  /// Send Firebase ID token to backend to get JWT
  Future<({bool isNewUser, String? accessToken, String? refreshToken})> loginWithFirebaseToken(String idToken) async {
    try {
      final response = await _dio.post(
        ApiEndpoints.login,
        data: {'token': idToken},
      );
      
      final data = response.data;
      await _storage.setAccessToken(data['access_token']);
      // We don't get a refresh_token yet, but let's adapt
      final refreshToken = data['refresh_token'] as String?;
      if (refreshToken != null) {
        await _storage.setRefreshToken(refreshToken);
      }

      return (
        isNewUser: false,
        accessToken: data['access_token'] as String?,
        refreshToken: refreshToken,
      );
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        // "User not registered" - proceed to registration
        return (isNewUser: true, accessToken: null, refreshToken: null);
      }
      throw mapDioException(e);
    }
  }

  /// Register new worker
  Future<({String userId, String status})> register({
    required String firstName,
    required String lastName,
    required String phone,
    required String departmentId,
    String? contractorId,
    required String designation,
    String? emergencyContactName,
    String? emergencyContactPhone,
  }) async {
    try {
      final response = await _dio.post(
        ApiEndpoints.register,
        data: {
          'first_name': firstName,
          'last_name': lastName,
          'phone': phone,
          'department_id': departmentId,
          'contractor_id': contractorId,
          'designation': designation,
          'emergency_contact_name': emergencyContactName,
          'emergency_contact_phone': emergencyContactPhone,
        },
      );

      final data = response.data;
      final accessToken = data['access_token'] as String?;
      if (AppConstants.demoAuth && accessToken != null) {
        await _storage.setAccessToken(accessToken);
      }

      return (
        userId: data['user_id'] as String,
        status: data['status'] as String,
      );
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  /// Get current user profile
  Future<User> getCurrentUser() async {
    try {
      final response = await _dio.get('/users/me');
      final user = User.fromJson(response.data);
      await saveUserData(user);
      return user;
    } on DioException catch (e) {
      // Fallback to local storage if network fails
      try {
        final userData = await _storage.getUserData();
        if (userData != null) {
          return User.fromJson(jsonDecode(userData));
        }
      } catch (_) {}
      throw mapDioException(e);
    } catch (_) {
      throw const AppException(message: 'Failed to load user data');
    }
  }

  /// Save user data locally
  Future<void> saveUserData(User user) async {
    await _storage.setUserData(jsonEncode(user.toJson()));
  }

  /// Logout
  Future<void> logout() async {
    try {
      await _dio.post(ApiEndpoints.logout);
    } catch (_) {
      // Logout silently even if API call fails
    } finally {
      await _storage.clearAll();
    }
  }

  /// Check if user has valid session
  Future<bool> hasValidSession() async {
    return await _storage.hasValidSession();
  }

  /// Refresh token
  Future<void> refreshToken() async {
    try {
      final refreshToken = await _storage.getRefreshToken();
      if (refreshToken == null) throw const AuthException(message: 'No refresh token');

      final response = await _dio.post(
        ApiEndpoints.refreshToken,
        data: {'refresh_token': refreshToken},
      );

      final newToken = response.data['access_token'];
      await _storage.setAccessToken(newToken);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}
