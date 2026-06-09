import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:geolocator/geolocator.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/buttons.dart';
import '../providers/attendance_providers.dart';
import 'package:constructpulse/core/network/api_client.dart';

/// QR Attendance Scan Screen (Spec §72)
class QrScanScreen extends ConsumerStatefulWidget {
  const QrScanScreen({super.key});

  @override
  ConsumerState<QrScanScreen> createState() => _QrScanScreenState();
}

class _QrScanScreenState extends ConsumerState<QrScanScreen> {
  final MobileScannerController _scannerController = MobileScannerController();
  bool _isScanning = true;
  bool _isProcessing = false;
  bool _isCheckingIn = true; // Toggle state

  @override
  void dispose() {
    _scannerController.dispose();
    super.dispose();
  }

  Future<Position?> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return null;
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return null;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      return null;
    }

    return await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(accuracy: LocationAccuracy.high));
  }

  void _onDetect(BarcodeCapture capture) async {
    if (!_isScanning || _isProcessing) return;
    
    final List<Barcode> barcodes = capture.barcodes;
    if (barcodes.isEmpty) return;

    final String? rawValue = barcodes.first.rawValue;
    if (rawValue == null || rawValue.isEmpty) return;

    String siteId;
    String qrToken;
    try {
      final Map<String, dynamic> data = jsonDecode(rawValue);
      siteId = data['site_id'];
      qrToken = data['qr_token'];
    } catch (e) {
      siteId = rawValue;
      qrToken = rawValue; // fallback
    }

    setState(() {
      _isScanning = false;
      _isProcessing = true;
    });

    _scannerController.stop();

    await _processAttendance(siteId, qrToken);
  }

  Future<void> _processAttendance(String siteId, String qrToken) async {
    try {
      final position = await _determinePosition();
      
      if (_isCheckingIn) {
        await ref.read(attendanceNotifierProvider.notifier).checkIn(
          siteId,
          qrToken,
          lat: position?.latitude,
          lng: position?.longitude,
        );
      } else {
        await ref.read(attendanceNotifierProvider.notifier).checkOut(
          siteId,
          qrToken,
          lat: position?.latitude,
          lng: position?.longitude,
        );
      }
      
      final state = ref.read(attendanceNotifierProvider);
      
      if (mounted && !state.hasError) {
        _showSuccessDialog(siteId, position);
      } else {
        _resetScanner();
        if (mounted && state.hasError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error: ${state.error}', style: const TextStyle(color: Colors.white)),
              backgroundColor: AppColors.danger,
            ),
          );
        }
      }
    } catch (e) {
      _resetScanner();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to process attendance: $e', style: const TextStyle(color: Colors.white)),
            backgroundColor: AppColors.danger,
          ),
        );
      }
    }
  }

  void _resetScanner() {
    if (mounted) {
      setState(() {
        _isScanning = true;
        _isProcessing = false;
      });
      _scannerController.start();
    }
  }

  Future<void> _simulateScan() async {
    setState(() {
      _isScanning = false;
      _isProcessing = true;
    });
    
    _scannerController.stop();
    const siteId = '65a4d83f-1343-4652-a249-17b926f1b386';
    
    try {
      final dio = ref.read(dioProvider);
      final resp = await dio.get('/sites/$siteId/qr');
      final qrToken = resp.data['qr_token'];
      
      if (_isCheckingIn) {
        await ref.read(attendanceNotifierProvider.notifier).checkIn(
          siteId, qrToken, lat: 17.446492, lng: 78.2821837,
        );
      } else {
        await ref.read(attendanceNotifierProvider.notifier).checkOut(
          siteId, qrToken, lat: 17.446492, lng: 78.2821837,
        );
      }
      
      final state = ref.read(attendanceNotifierProvider);
      if (mounted && !state.hasError) {
        // Mock position for UI dialog
        final pos = Position(longitude: 78.2821837, latitude: 17.446492, timestamp: DateTime.now(), accuracy: 10, altitude: 0, heading: 0, speed: 0, speedAccuracy: 0, altitudeAccuracy: 0, headingAccuracy: 0);
        _showSuccessDialog(siteId, pos);
      } else {
        _resetScanner();
        if (mounted && state.hasError) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: ${state.error}'), backgroundColor: AppColors.danger));
        }
      }
    } catch (e) {
      _resetScanner();
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Simulate Failed: $e'), backgroundColor: AppColors.danger));
    }
  }

  void _showSuccessDialog(String siteId, Position? position) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Container(
              width: 80, height: 80,
              decoration: BoxDecoration(
                color: AppColors.successLight,
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(Icons.check_circle_rounded, color: AppColors.success, size: 48),
            ),
            const SizedBox(height: 24),
            Text('Attendance Recorded', style: AppTypography.h3),
            const SizedBox(height: 8),
            Text(_isCheckingIn ? 'Check-In Successful' : 'Check-Out Successful', style: AppTypography.caption),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.surfaceVariant,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(children: [
                _detailRow('Site ID', siteId),
                const Divider(height: 16),
                _detailRow('Time', TimeOfDay.now().format(context)),
                const Divider(height: 16),
                _detailRow('GPS', position != null 
                    ? '${position.latitude.toStringAsFixed(4)}°, ${position.longitude.toStringAsFixed(4)}°' 
                    : 'Unavailable'),
              ]),
            ),
            const SizedBox(height: 24),
            PrimaryButton(
              text: 'Done',
              backgroundColor: AppColors.success,
              onPressed: () {
                ref.invalidate(todayAttendanceProvider);
                ref.invalidate(attendanceHistoryProvider);
                Navigator.of(ctx).pop();
                Navigator.of(context).pop();
              },
            ),
          ]),
        ),
      ),
    );
  }

  Widget _detailRow(String label, String value) {
    return Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
      Text(label, style: AppTypography.caption),
      Text(value, style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.w600)),
    ]);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        title: Text(_isCheckingIn ? 'Scan QR to Check In' : 'Scan QR to Check Out', style: AppTypography.h4.copyWith(color: Colors.white, fontSize: 18)),
        elevation: 0,
      ),
      body: Column(
        children: [
          // Camera Viewfinder Area
          Expanded(
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Live Camera
                MobileScanner(
                  controller: _scannerController,
                  onDetect: _onDetect,
                ),
                // Scan Frame
                Container(
                  width: 280, height: 280,
                  decoration: BoxDecoration(
                    border: Border.all(color: AppColors.secondary, width: 3),
                    borderRadius: BorderRadius.circular(24),
                  ),
                  child: Stack(children: [
                    // Corner accents
                    ..._buildCorners(),
                    if (_isProcessing)
                      const Center(child: CircularProgressIndicator(
                        color: AppColors.secondary,
                      )),
                  ]),
                ),
                // Instructions
                Positioned(
                  bottom: 40,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                    decoration: BoxDecoration(
                      color: Colors.black54,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      _isProcessing ? 'Verifying location and recording...' : 'Align QR code within the frame',
                      style: AppTypography.bodySmall.copyWith(color: Colors.white),
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Bottom Controls
          Container(
            padding: const EdgeInsets.all(24),
            color: Colors.black,
            child: Column(children: [
              // Toggle Check In / Check Out
              Container(
                decoration: BoxDecoration(
                  color: AppColors.surfaceVariant.withValues(alpha: 0.3),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: GestureDetector(
                        onTap: () {
                          if (!_isProcessing) setState(() => _isCheckingIn = true);
                        },
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          decoration: BoxDecoration(
                            color: _isCheckingIn ? AppColors.primary : Colors.transparent,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          alignment: Alignment.center,
                          child: Text('Check In', style: AppTypography.bodySmall.copyWith(
                            color: _isCheckingIn ? Colors.white : Colors.white54,
                            fontWeight: _isCheckingIn ? FontWeight.w600 : FontWeight.w400,
                          )),
                        ),
                      ),
                    ),
                    Expanded(
                      child: GestureDetector(
                        onTap: () {
                          if (!_isProcessing) setState(() => _isCheckingIn = false);
                        },
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          decoration: BoxDecoration(
                            color: !_isCheckingIn ? AppColors.secondary : Colors.transparent,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          alignment: Alignment.center,
                          child: Text('Check Out', style: AppTypography.bodySmall.copyWith(
                            color: !_isCheckingIn ? Colors.white : Colors.white54,
                            fontWeight: !_isCheckingIn ? FontWeight.w600 : FontWeight.w400,
                          )),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              PrimaryButton(
                text: 'Simulate Scan',
                backgroundColor: _isCheckingIn ? AppColors.primary : AppColors.secondary,
                onPressed: _isScanning && !_isProcessing ? _simulateScan : null,
                isLoading: _isProcessing,
                icon: Icons.qr_code_scanner_rounded,
              ),
              const SizedBox(height: 12),
              Text('Point camera at site QR code',
                  style: AppTypography.caption.copyWith(color: Colors.white54)),
            ]),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildCorners() {
    const size = 24.0;
    const thickness = 4.0;
    const color = AppColors.secondary;
    return [
      Positioned(top: 0, left: 0, child: _corner(color, size, thickness, true, true)),
      Positioned(top: 0, right: 0, child: _corner(color, size, thickness, true, false)),
      Positioned(bottom: 0, left: 0, child: _corner(color, size, thickness, false, true)),
      Positioned(bottom: 0, right: 0, child: _corner(color, size, thickness, false, false)),
    ];
  }

  Widget _corner(Color color, double size, double t, bool top, bool left) {
    return SizedBox(
      width: size, height: size,
      child: CustomPaint(painter: _CornerPainter(color, t, top, left)),
    );
  }
}

class _CornerPainter extends CustomPainter {
  final Color color;
  final double thickness;
  final bool top;
  final bool left;

  _CornerPainter(this.color, this.thickness, this.top, this.left);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = color..strokeWidth = thickness..style = PaintingStyle.stroke..strokeCap = StrokeCap.round;
    final path = Path();
    if (top && left) {
      path.moveTo(0, size.height); path.lineTo(0, 0); path.lineTo(size.width, 0);
    } else if (top && !left) {
      path.moveTo(0, 0); path.lineTo(size.width, 0); path.lineTo(size.width, size.height);
    } else if (!top && left) {
      path.moveTo(0, 0); path.lineTo(0, size.height); path.lineTo(size.width, size.height);
    } else {
      path.moveTo(0, size.height); path.lineTo(size.width, size.height); path.lineTo(size.width, 0);
    }
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
