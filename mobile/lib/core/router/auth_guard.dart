import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';

String? authGuard(BuildContext context, GoRouterState state, AuthState authState) {
  final path = state.matchedLocation;
  final status = authState.status;
  
  debugPrint('RouterGuard: path=$path, status=$status');

  // Redirect from splash once session check is complete
  if (path == '/splash') {
    if (status == AuthStatus.authenticated) return '/';
    if (status == AuthStatus.unauthenticated) return '/auth/login';
    return null;
  }

  // Auth redirects
  if (status == AuthStatus.unauthenticated) {
    if (path.startsWith('/auth')) return null;
    return '/auth/login';
  }
  
  if (status == AuthStatus.otpSent && path != '/auth/otp') {
    return '/auth/otp';
  }
  
  if (status == AuthStatus.registering && path != '/auth/register') {
    return '/auth/register';
  }
  
  if (status == AuthStatus.pendingApproval && path != '/auth/pending') {
    return '/auth/pending';
  }
  
  if (status == AuthStatus.rejected && path != '/auth/rejected') {
    return '/auth/rejected';
  }
  
  if (status == AuthStatus.suspended && path != '/auth/suspended') {
    return '/auth/suspended';
  }
  
  if (status == AuthStatus.authenticated && path.startsWith('/auth')) {
    return '/'; // Go to home if already authenticated and trying to access auth pages
  }

  return null;
}
