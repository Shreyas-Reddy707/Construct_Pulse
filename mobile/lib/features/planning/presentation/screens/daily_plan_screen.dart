import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

/// Daily Planning Screen (Spec §79)
class DailyPlanScreen extends StatelessWidget {
  const DailyPlanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Daily Plans'),
        actions: [IconButton(icon: const Icon(Icons.add_rounded), onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Feature available in future release')));
        })],
      ),
      body: const Center(child: Text('No daily plans found.')),
    );
  }

}

enum PlanStatus { draft, approved, completed, cancelled }
