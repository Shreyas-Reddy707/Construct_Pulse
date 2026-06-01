import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../constants/app_constants.dart';
import '../storage/secure_storage.dart';
import '../constants/api_endpoints.dart';

/// Dio HTTP client configured for ConstructPulse API
final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: AppConstants.baseUrl,
    connectTimeout: AppConstants.connectTimeout,
    receiveTimeout: AppConstants.receiveTimeout,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  ));

  dio.interceptors.add(AuthInterceptor(ref));
  dio.interceptors.add(LogInterceptor(
    requestBody: true,
    responseBody: true,
    logPrint: (o) => debugPrint('[API] $o'),
  ));

  return dio;
});

/// JWT Authentication interceptor with automatic token refresh
class AuthInterceptor extends Interceptor {
  final Ref _ref;

  AuthInterceptor(this._ref);

  @override
  void onRequest(
      RequestOptions options, RequestInterceptorHandler handler) async {
    // Skip auth for public endpoints
    final publicPaths = [
      ApiEndpoints.sendOtp,
      ApiEndpoints.verifyOtp,
      ApiEndpoints.register,
    ];

    if (!publicPaths.contains(options.path)) {
      final storage = _ref.read(secureStorageProvider);
      final token = await storage.getAccessToken();
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }

    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      // Attempt token refresh
      try {
        final storage = _ref.read(secureStorageProvider);
        final refreshToken = await storage.getRefreshToken();

        if (refreshToken != null) {
          final dio = Dio(BaseOptions(baseUrl: AppConstants.baseUrl));
          final response = await dio.post(
            ApiEndpoints.refreshToken,
            data: {'refresh_token': refreshToken},
          );

          if (response.statusCode == 200) {
            final newToken = response.data['access_token'];
            await storage.setAccessToken(newToken);

            // Retry the original request
            err.requestOptions.headers['Authorization'] = 'Bearer $newToken';
            final retryResponse = await dio.fetch(err.requestOptions);
            return handler.resolve(retryResponse);
          }
        }
      } catch (_) {
        // Token refresh failed, clear session
        final storage = _ref.read(secureStorageProvider);
        await storage.clearAll();
      }
    }

    handler.next(err);
  }
}
