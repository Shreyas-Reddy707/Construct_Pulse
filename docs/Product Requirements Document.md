# Product Requirements Document (PRD)

# ConstructPulse
### Enterprise Construction Workforce Management Platform

---

Version: 3.0

Status: Production Planning

Client: Limelite Construction Ltd.

Region: New Zealand

Prepared By:
ConstructPulse Development Team

---

# Table of Contents

1. Executive Summary
2. Product Vision
3. Business Goals
4. Problem Statement
5. Stakeholders
6. Organization Hierarchy
7. User Roles
8. Role Permission Matrix
9. Core Business Workflows
10. Functional Requirements
11. Modules
12. User Stories
13. Non Functional Requirements
14. Security Requirements
15. System Constraints
16. Risks
17. MVP Scope
18. Future Roadmap
19. Acceptance Criteria
20. Glossary

---

# 1 Executive Summary

ConstructPulse is an enterprise workforce management platform built specifically for construction companies operating multiple active construction sites.

The platform replaces fragmented paper-based attendance systems, manual onboarding, subcontractor spreadsheets, and disconnected communication channels with a centralized digital platform capable of managing workforce operations in real time.

The system is designed around the operational workflows of Limelite Construction and supports thousands of workers across multiple sites throughout New Zealand.

---

# 2 Product Vision

To become the central operating platform for workforce management, attendance, safety compliance, emergency response, and subcontractor coordination across every Limelite Construction site.

---

# 3 Business Goals

The platform should enable Limelite Construction to:

• Digitize attendance

• Eliminate paper registers

• Improve worker accountability

• Improve health & safety compliance

• Track live workforce occupancy

• Manage subcontractors efficiently

• Simplify onboarding

• Reduce payroll discrepancies

• Improve emergency preparedness

• Provide real-time management analytics

---

# 4 Problem Statement

Current operational processes rely heavily on

• Excel

• Paper attendance

• Phone calls

• WhatsApp

• Manual approvals

• Physical induction documents

This creates

• Unknown workforce numbers

• Attendance errors

• Payroll mistakes

• Slow onboarding

• Missing compliance records

• Poor emergency visibility

ConstructPulse eliminates these problems through centralized digital workflows.

---

# 5 Stakeholders

Primary

• Limelite Directors

• Operations Team

• Site Managers

• Site Supervisors

• HR

Secondary

• Workers

• Subcontractor Companies

• Visitors

• Safety Officers

---

# 6 Organizational Hierarchy

Platform Owner
│
▼
Company Administrator
│
▼
Operations Manager
│
├───────────────┐
▼               ▼
Site Manager    Site Manager
│               │
▼               ▼
Supervisor      Supervisor
│               │
▼               ▼
Workers         Workers

The hierarchy ensures every permission originates from a higher authority.

No user may assign themselves a privileged role.

---

# 7 User Roles

## Platform Owner

Managed by ConstructPulse.

Responsibilities

• Create companies

• Assign Company Administrators

• Platform configuration

• Licensing

---

## Company Administrator

Highest authority inside Limelite.

Can

• Invite Operations Managers

• Invite Directors

• Invite Site Managers

• Create Departments

• Create Subcontractor Companies

• Configure Company Settings

Cannot

• Create another Company

---

## Operations Manager

Responsible for workforce planning.

Can

• Create Sites

• Assign Site Managers

• Assign Workers

• Transfer Workers

• Manage Projects

---

## Site Manager

Responsible for a specific construction site.

Can

• Approve Worker Registrations

• Reject Workers

• Suspend Workers

• Manage Attendance

• Generate QR Codes

• Emergency Muster

• Site Notices

---

## Supervisor

Can

• Monitor Attendance

• Verify Workforce

• Report Incidents

• Emergency Operations

Cannot

• Approve Registrations

• Create Sites

---

## Worker

Can

• Register

• Check In

• Check Out

• Complete Safety Induction

• View Attendance

• View Assigned Sites

---

## Subcontractor Administrator

Represents an external company.

Can

• Manage Company Workers

• Upload Documents

• View Assigned Sites

Cannot

• Approve Attendance

• Create Sites

---

# 8 Permission Matrix

| Permission | Platform | Company Admin | Ops | Site Manager | Supervisor | Worker |
|------------|----------|---------------|-----|--------------|------------|--------|
| Create Company | ✓ | | | | | |
| Invite Admin | ✓ | | | | | |
| Invite Site Manager | | ✓ | ✓ | | | |
| Create Site | | | ✓ | | | |
| Approve Workers | | | | ✓ | | |
| Transfer Workers | | | ✓ | ✓ | | |
| QR Attendance | | | | | | ✓ |
| Emergency Muster | | | ✓ | ✓ | ✓ | |

---

# 9 Core Business Workflows

## Worker Registration

Worker

↓

OTP Login

↓

Registration

↓

Pending Approval

↓

Site Manager Approval

↓

Worker Active

---

## Site Manager Invitation

Operations Manager

↓

Create Site

↓

Invite Site Manager

↓

SMS Invitation

↓

Login

↓

Ready

---

## Worker Transfer

Operations

↓

Assign Worker

↓

Multiple Sites

↓

GPS decides active attendance

---

## Attendance

Worker

↓

QR Scan

↓

GPS Validation

↓

Site Validation

↓

Attendance Recorded

---

## Emergency

Emergency Trigger

↓

Freeze Attendance

↓

Generate Muster List

↓

Identify Missing Workers

↓

Emergency Contacts

---

# 10 Functional Requirements

Authentication

• OTP Login

• Session Management

• Logout

• Refresh Tokens

---

Worker Management

• Registration

• Approval

• Suspension

• Multi-site Assignment

• Certifications

---

Company Management

• Departments

• Subcontractors

• Contacts

---

Site Management

Every Site stores

• GPS Coordinates

• Radius

• QR Code

• Emergency Contacts

• Safety Documents

• Site Manager

---

Attendance

Attendance only succeeds if

✓ Worker Approved

✓ GPS Valid

✓ QR Valid

✓ Assigned Site

✓ Active Status

---

Safety

Before first attendance

Worker must complete

• Site Induction

• PPE Checklist

• Emergency Information

---

Emergency

One click

↓

Generate Live Muster

↓

Current Occupancy

↓

Missing Workers

↓

Emergency Contacts

---

# 11 System Modules

Authentication

User Management

Company Management

Department Management

Subcontractor Management

Site Management

Attendance

Safety

Emergency

Reporting

Notifications

Analytics

Settings

---

# 12 User Stories

As a Worker

I want to register once

So I can work across multiple Limelite sites.

---

As a Site Manager

I want to approve workers

So only authorized workers enter my site.

---

As an Operations Manager

I want to assign workers across multiple projects

So workforce utilization is optimized.

---

As a Director

I want company-wide dashboards

So I can monitor operations.

---

# 13 Non Functional Requirements

Performance

Dashboard <2 sec

Attendance <3 sec

QR <2 sec

Availability

99.9%

Scalability

100 Sites

10,000 Workers

Unlimited Attendance Records

---

# 14 Security

JWT

RBAC

Encrypted Storage

HTTPS

Audit Logs

GPS Validation

Session Expiry

OTP Authentication

---

# 15 Assumptions

Every site has GPS coordinates.

Every worker owns a smartphone.

Every site has internet connectivity.

Each worker belongs to one company.

Workers may belong to multiple sites.

---

# 16 Risks

GPS spoofing

QR sharing

Network outages

Manager absence

Lost devices

Each risk shall have mitigation strategies documented separately.

---

# 17 MVP Scope

Included

✓ Authentication

✓ Worker Registration

✓ Site Management

✓ Worker Approval

✓ QR Attendance

✓ GPS Validation

✓ Emergency Muster

✓ Safety Induction

✓ Live Occupancy

✓ Multi-site Assignment

✓ Subcontractor Companies

---

# 18 Future Roadmap

Payroll

Visitor Management

Equipment Tracking

Incident Reporting

Vehicle Tracking

Digital Forms

AI Analytics

IoT Integration

Predictive Workforce Planning

---

# 19 Acceptance Criteria

The platform shall be considered production-ready when

• Attendance is GPS validated.

• Every worker is approved by a Site Manager.

• Workers cannot check into unauthorized sites.

• Emergency Muster accurately reflects live occupancy.

• Multi-site attendance is handled correctly.

• Directors have complete operational visibility.

---

# 20 Glossary

Company

A client organization using ConstructPulse.

Subcontractor

External company supplying workers.

Site

Construction location.

Attendance

Worker check-in/check-out records.

Emergency Muster

Live accountability during emergencies.

Geofence

GPS boundary surrounding a site.

Site Manager

Primary authority responsible for a construction site.

Operations Manager

Responsible for workforce allocation across multiple sites.

Platform Owner

ConstructPulse system administrator responsible for onboarding client organizations.
