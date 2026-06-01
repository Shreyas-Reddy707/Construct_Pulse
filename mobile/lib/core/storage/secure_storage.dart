import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';

final secureStorageProvider = Provider<SecureStorageService>((ref) {
  return SecureStorageService();
});

/// Secure storage for JWT tokens and sensitive user data
class SecureStorageService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
    iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
  );

  // ── Token Management ──────────────────────────────────────
  Future<String?> getAccessToken() async =>
      await _storage.read(key: AppConstants.accessTokenKey);

  Future<void> setAccessToken(String token) async =>
      await _storage.write(key: AppConstants.accessTokenKey, value: token);

  Future<String?> getRefreshToken() async =>
      await _storage.read(key: AppConstants.refreshTokenKey);

  Future<void> setRefreshToken(String token) async =>
      await _storage.write(key: AppConstants.refreshTokenKey, value: token);

  // ── User Data ─────────────────────────────────────────────
  Future<String?> getUserData() async =>
      await _storage.read(key: AppConstants.userDataKey);

  Future<void> setUserData(String data) async =>
      await _storage.write(key: AppConstants.userDataKey, value: data);

  Future<String?> getCompanyId() async =>
      await _storage.read(key: AppConstants.companyIdKey);

  Future<void> setCompanyId(String id) async =>
      await _storage.write(key: AppConstants.companyIdKey, value: id);

  // ── Session Management ────────────────────────────────────
  Future<bool> hasValidSession() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  Future<void> clearAll() async => await _storage.deleteAll();
}
