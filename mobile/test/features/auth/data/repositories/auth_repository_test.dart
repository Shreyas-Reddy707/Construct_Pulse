import 'package:flutter_test/flutter_test.dart';
import 'package:dio/dio.dart';
import 'package:constructpulse/features/auth/data/repositories/auth_repository.dart';
import 'package:constructpulse/core/storage/secure_storage.dart';

class FakeDio extends Fake implements Dio {
  bool postCalled = false;
  
  @override
  Future<Response<T>> post<T>(
    String path, {
    Object? data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    void Function(int, int)? onSendProgress,
    void Function(int, int)? onReceiveProgress,
  }) async {
    postCalled = true;
    return Response<T>(
      requestOptions: RequestOptions(path: path),
      data: {} as T,
    );
  }
}

class FakeSecureStorage extends Fake implements SecureStorageService {
  bool cleared = false;
  bool validSession = true;
  
  @override
  Future<bool> hasValidSession() async => validSession;
  
  @override
  Future<void> clearAll() async {
    cleared = true;
  }
}

void main() {
  late AuthRepository repository;
  late FakeDio fakeDio;
  late FakeSecureStorage fakeStorage;

  setUp(() {
    fakeDio = FakeDio();
    fakeStorage = FakeSecureStorage();
    repository = AuthRepository(fakeDio, fakeStorage);
  });

  group('AuthRepository', () {
    test('hasValidSession returns true', () async {
      fakeStorage.validSession = true;
      final result = await repository.hasValidSession();
      expect(result, isTrue);
    });

    test('logout clears storage', () async {
      await repository.logout();
      expect(fakeDio.postCalled, isTrue);
      expect(fakeStorage.cleared, isTrue);
    });
  });
}
