/// Standard API response wrapper matching spec §30
class ApiResponse<T> {
  final bool success;
  final String? message;
  final T? data;
  final ApiError? error;

  const ApiResponse({
    required this.success,
    this.message,
    this.data,
    this.error,
  });

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(dynamic)? fromJsonT,
  ) {
    return ApiResponse(
      success: json['success'] ?? false,
      message: json['message'],
      data: json['data'] != null && fromJsonT != null
          ? fromJsonT(json['data'])
          : json['data'] as T?,
      error: json['error'] != null
          ? ApiError.fromJson(json['error'] as Map<String, dynamic>)
          : null,
    );
  }

  bool get isSuccess => success && error == null;
  bool get isError => !success || error != null;
}

class ApiError {
  final String code;
  final String message;

  const ApiError({required this.code, required this.message});

  factory ApiError.fromJson(Map<String, dynamic> json) {
    return ApiError(
      code: json['code'] ?? 'UNKNOWN_ERROR',
      message: json['message'] ?? 'An unknown error occurred',
    );
  }
}

/// Paginated response wrapper
class PaginatedResponse<T> {
  final List<T> items;
  final int page;
  final int limit;
  final int total;
  final bool hasMore;

  const PaginatedResponse({
    required this.items,
    required this.page,
    required this.limit,
    required this.total,
    required this.hasMore,
  });
}
