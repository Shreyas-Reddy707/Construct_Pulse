import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/errors/exceptions.dart';

final firebaseAuthProvider = Provider<FirebaseAuthService>((ref) {
  return FirebaseAuthService(FirebaseAuth.instance);
});

class FirebaseAuthService {
  final FirebaseAuth _auth;

  FirebaseAuthService(this._auth);

  String? _verificationId;

  Future<void> sendOtp({
    required String phone,
    required Function(String) onCodeSent,
    required Function(String) onError,
  }) async {
    try {
      await _auth.verifyPhoneNumber(
        phoneNumber: phone,
        verificationCompleted: (PhoneAuthCredential credential) async {
          // Auto-resolution (mostly Android)
          await _auth.signInWithCredential(credential);
        },
        verificationFailed: (FirebaseAuthException e) {
          onError(e.message ?? 'Verification failed');
        },
        codeSent: (String verificationId, int? resendToken) {
          _verificationId = verificationId;
          onCodeSent(verificationId);
        },
        codeAutoRetrievalTimeout: (String verificationId) {
          _verificationId = verificationId;
        },
      );
    } catch (e) {
      onError(e.toString());
    }
  }

  Future<UserCredential> verifyOtp(String otp) async {
    if (_verificationId == null) {
      throw const AuthException(message: 'Verification ID is null. Request OTP again.');
    }
    
    try {
      final credential = PhoneAuthProvider.credential(
        verificationId: _verificationId!,
        smsCode: otp,
      );
      
      return await _auth.signInWithCredential(credential);
    } on FirebaseAuthException catch (e) {
      throw AuthException(message: e.message ?? 'Invalid OTP');
    }
  }

  Future<void> logout() async {
    await _auth.signOut();
  }

  User? get currentUser => _auth.currentUser;
  
  Stream<User?> get authStateChanges => _auth.authStateChanges();
}
