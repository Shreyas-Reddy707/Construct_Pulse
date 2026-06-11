# ConstructPulse Demo Guide

This document outlines the standard workflow for demonstrating the ConstructPulse platform.

## 1. Demo Prerequisites
- A running PostgreSQL database instance.
- The FastAPI backend running locally (`uvicorn app.main:app --reload`).
- The Flutter application running on an emulator or physical device.
- Ensure `AppConstants.demoAuth = true` is set in the Flutter app to bypass Firebase SMS billing (if testing locally).

## 2. Test Accounts
*(Replace with actual demo credentials if available)*
- **Company Admin:** `admin@demo.constructpulse.com` / `+12345678900`
- **Worker 1:** `+15550000001`
- **Worker 2:** `+15550000002`

## 3. Demo Flow

### Phase A: Registration & Approval
1. **Worker App:** Open the app and register a new worker account via phone number.
2. **Worker App:** Show the `Registration Submitted` (Pending) screen.
3. **Admin Dashboard:** Log in as the Company Admin.
4. **Admin Dashboard:** Navigate to the **Approvals** tab in the Workforce Directory.
5. **Admin Dashboard:** Approve the newly registered worker.
6. **Worker App:** Press "Check Status" (or show automatic transition) to enter the main application.

### Phase B: Site Check-In
1. **Admin Dashboard:** Navigate to Sites and display the site's QR code.
2. **Worker App:** Tap the "Scan" floating action button.
3. **Worker App:** Scan the QR code (or use manual entry fallback if on emulator).
4. **Worker App:** Verify the screen updates to "Checked In" and the active site is displayed.
5. **Admin Dashboard:** Navigate to the Home Dashboard and show the Live Occupancy KPI increase by 1.

### Phase C: Emergency Muster
1. **Admin Dashboard:** Navigate to the Emergency section and trigger a site-wide evacuation.
2. **Worker App:** Demonstrate the push notification / red emergency alert banner appearing on the worker's device.
3. **Worker App:** Tap "Mark as Safe".
4. **Admin Dashboard:** Show the live updating muster report reflecting the worker's safety status.

## 4. Key Features to Showcase
- Instant UI updates and Riverpod state caching.
- Secure, multi-tenant RBAC (workers cannot access admin features).
- High-contrast, accessibility-friendly design system.

## 5. Common Questions & Answers
- **Q: What happens if a worker loses connectivity?**
  A: Currently requires an internet connection, but offline-sync functionality is on the roadmap.
- **Q: How does the QR scanning prevent fraud?**
  A: Site QR codes use rotating cryptographically hashed signatures validated by the backend.

## 6. Known Limitations
- The system currently assumes 1 phone number = 1 user.
- SMS OTP rates apply if `demoAuth` is disabled.
