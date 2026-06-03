import 'package:flutter_test/flutter_test.dart';
import 'package:dio/dio.dart';
import 'package:constructpulse/features/attendance/data/repositories/attendance_repository.dart';
import 'package:constructpulse/core/errors/exceptions.dart';

class FakeDioThrowing extends Fake implements Dio {
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
    throw DioException(requestOptions: RequestOptions(path: path));
  }
}

void main() {
  late AttendanceRepository repository;
  late FakeDioThrowing fakeDio;

  setUp(() {
    fakeDio = FakeDioThrowing();
    repository = AttendanceRepository(fakeDio);
  });

  group('AttendanceRepository', () {
    test('checkIn handles exceptions gracefully', () async {
      expect(() => repository.checkIn('site123', 'token123', lat: 10.0, lng: 10.0), throwsA(isA<AppException>()));
    });
  });
}
