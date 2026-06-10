import 'package:dio/dio.dart';

void main() async {
  final dio = Dio(BaseOptions(baseUrl: 'http://localhost:8000/api/v1'));
  try {
    // We don't have a token, but we just want to see if it follows redirect and gets 401
    final res = await dio.get('/sites');
    print('Status: \${res.statusCode}');
    print('Data: \${res.data}');
  } on DioException catch (e) {
    print('Dio Error: \${e.response?.statusCode}');
    print('Data: \${e.response?.data}');
  }
}
