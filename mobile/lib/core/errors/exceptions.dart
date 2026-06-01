import 'package:dio/dio.dart';

/// Application-level exceptions
class AppException implements Exception {
  final String message;
  final String? code;
  final dynamic originalError;

  const AppException({
    required this.message,
    this.code,
    this.originalError,
  });

  @override
  String toString() => 'AppException($code): $message';
}

class NetworkException extends AppException {
  const NetworkException({
    required super.message,
    super.code = 'NETWORK_ERROR',
    super.originalError,
  });
}

class AuthException extends AppException {
  const AuthException({
    required super.message,
    super.code = 'AUTH_ERROR',
    super.originalError,
  });
}

class ValidationException extends AppException {
  final Map<String, List<String>>? fieldErrors;

  const ValidationException({
    required super.message,
    super.code = 'VALIDATION_ERROR',
    this.fieldErrors,
    super.originalError,
  });
}

class ServerException extends AppException {
  final int? statusCode;

  const ServerException({
    required super.message,
    super.code = 'SERVER_ERROR',
    this.statusCode,
    super.originalError,
  });
}

/// Convert DioExceptions to app-level exceptions
AppException mapDioException(DioException e) {
  switch (e.type) {
    case DioExceptionType.connectionTimeout:
    case DioExceptionType.sendTimeout:
    case DioExceptionType.receiveTimeout:
      return const NetworkException(
        message: 'Connection timed out. Please check your internet.',
      );
    case DioExceptionType.connectionError:
      return const NetworkException(
        message: 'No internet connection.',
      );
    case DioExceptionType.badResponse:
      final statusCode = e.response?.statusCode;
      final data = e.response?.data;
      final errorMsg = data is Map
          ? (data['error']?['message'] ?? data['message'] ?? 'Server error')
          : 'Server error';
      final errorCode = data is Map
          ? (data['error']?['code'] ?? 'SERVER_ERROR')
          : 'SERVER_ERROR';

      switch (statusCode) {
        case 401:
          return AuthException(
            message: errorMsg,
            code: errorCode,
          );
        case 403:
          return const AuthException(
            message: 'You don\'t have permission for this action.',
            code: 'FORBIDDEN',
          );
        case 404:
          return ServerException(
            message: 'Resource not found.',
            code: 'NOT_FOUND',
            statusCode: statusCode,
          );
        case 409:
          return ServerException(
            message: errorMsg,
            code: 'CONFLICT',
            statusCode: statusCode,
          );
        case 422:
          return ValidationException(
            message: errorMsg,
            code: errorCode,
          );
        case 429:
          return const ServerException(
            message: 'Too many requests. Please wait and try again.',
            code: 'RATE_LIMIT_EXCEEDED',
            statusCode: 429,
          );
        default:
          return ServerException(
            message: errorMsg,
            statusCode: statusCode,
          );
      }
    default:
      return NetworkException(
        message: 'An unexpected error occurred.',
        originalError: e,
      );
  }
}
