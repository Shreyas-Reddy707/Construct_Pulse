import 'package:equatable/equatable.dart';
import 'exceptions.dart';

abstract class Failure extends Equatable {
  final String message;
  final String? code;

  const Failure({required this.message, this.code});

  @override
  List<Object?> get props => [message, code];
}

class ServerFailure extends Failure {
  const ServerFailure({required super.message, super.code});
}

class CacheFailure extends Failure {
  const CacheFailure({required super.message, super.code});
}

class NetworkFailure extends Failure {
  const NetworkFailure({required super.message, super.code});
}

class AuthFailure extends Failure {
  const AuthFailure({required super.message, super.code});
}

class ValidationFailure extends Failure {
  const ValidationFailure({required super.message, super.code});
}

Failure mapExceptionToFailure(Exception exception) {
  if (exception is ServerException) {
    return ServerFailure(message: exception.message, code: exception.code);
  } else if (exception is AuthException) {
    return AuthFailure(message: exception.message, code: exception.code);
  } else if (exception is NetworkException) {
    return NetworkFailure(message: exception.message, code: exception.code);
  } else if (exception is ValidationException) {
    return ValidationFailure(message: exception.message, code: exception.code);
  }
  return FailureImpl(message: exception.toString());
}

class FailureImpl extends Failure {
  const FailureImpl({required super.message});
}
