import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:qr_flutter/qr_flutter.dart';
import '../providers/site_providers.dart';

class SiteQrScreen extends ConsumerWidget {
  final String siteId;

  const SiteQrScreen({super.key, required this.siteId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final siteAsync = ref.watch(siteProvider(siteId));
    final qrDataAsync = ref.watch(siteQrProvider(siteId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Site QR Code'),
      ),
      body: Center(
        child: qrDataAsync.when(
          data: (qrData) {
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                siteAsync.when(
                  data: (site) => Text(
                    site.name,
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  loading: () => const SizedBox(),
                  error: (_, __) => const SizedBox(),
                ),
                const SizedBox(height: 32),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.1),
                        blurRadius: 10,
                        spreadRadius: 1,
                      )
                    ],
                  ),
                  child: QrImageView(
                    data: qrData,
                    size: 250.0,
                  ),
                ),
                const SizedBox(height: 32),
                const Text(
                  'Scan this QR code to check in/out',
                  style: TextStyle(color: Colors.grey),
                ),
              ],
            );
          },
          loading: () => const CircularProgressIndicator(),
          error: (error, stack) => Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('QR Code not found or expired', style: TextStyle(color: Colors.red)),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => ref.read(siteActionNotifierProvider.notifier).generateQr(siteId),
                child: const Text('Generate QR Code'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
