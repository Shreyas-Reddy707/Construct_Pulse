# DATABASE_DESIGN.md

> **Project:** ConstructPulse
> **Version:** 2.0
> **Document Type:** Database Design Specification
> **Status:** Production Design
> **Prepared By:** Engineering Team
> **Last Updated:** July 2026

---

# Database Design

## 1. Introduction

This document defines the logical and physical database architecture for ConstructPulse.

It serves as the single source of truth for all database entities, relationships, constraints, indexing strategies, audit requirements, and multi-tenant data isolation.

The design has been created for a production-scale Construction Workforce Operating System (CWOS) capable of supporting multiple companies, projects, construction sites, subcontractors, workers, compliance records, attendance, safety operations, emergency response, analytics, and future enterprise modules.

---

# 2. Database Objectives

The database has been designed to achieve the following objectives.

- Ensure complete data integrity
- Support multi-company architecture
- Maintain tenant isolation
- Support high transaction volumes
- Enable efficient reporting
- Optimize query performance
- Maintain complete auditability
- Support future horizontal scaling
- Provide long-term maintainability

---

# 3. Database Technology

Primary Database

- PostgreSQL

ORM

- SQLAlchemy

Migration Framework

- Alembic

Primary Key Strategy

- UUID Version 4

Timestamp Format

- UTC (ISO 8601)

Character Encoding

- UTF-8

---

# 4. Database Design Principles

The database follows the following principles.

## Normalization

All operational tables are normalized to Third Normal Form (3NF) unless denormalization is required for performance.

## Referential Integrity

Foreign key constraints enforce valid relationships between entities.

## Soft Delete

Operational records are archived using soft deletion where appropriate.

## Immutable Audit Records

Audit tables are append-only.

## Multi-Tenant Isolation

Every business entity belongs to exactly one company unless explicitly defined as global.

## Configurable Architecture

Business rules are stored as configurable data rather than hardcoded values wherever possible.

---

# 5. Naming Conventions

## Tables

- snake_case
- plural names

Examples

users

companies

sites

attendance_records

incident_reports

---

## Columns

snake_case

Examples

company_id

site_id

created_at

updated_at

phone_number

emergency_contact

---

## Primary Keys

All tables use:

id UUID PRIMARY KEY

---

## Foreign Keys

Format:

referenced_table_id

Examples

company_id

site_id

worker_id

project_id

department_id

---

## Timestamps

Every operational table includes:

created_at

updated_at

Optional:

deleted_at

approved_at

completed_at

---

# 6. Database Architecture Overview

The database is divided into multiple business domains.

Identity

Organization

Projects

Sites

Workforce

Attendance

Compliance

Emergency

Safety

Assets

Visitors

Communications

Analytics

Administration

Audit

Each domain owns its entities while maintaining defined relationships with other domains.

---

# 7. Domain Overview

ConstructPulse currently contains the following database domains.

## Identity Domain

Authentication

Roles

Permissions

Sessions

---

## Organization Domain

Companies

Projects

Departments

Trades

Subcontractors

---

## Workforce Domain

Workers

Assignments

Transfers

Employment History

---

## Attendance Domain

QR Codes

GPS Validation

Attendance Records

Occupancy

Attendance Events

---

## Compliance Domain

Certificates

Licences

Training

Inductions

Expiry Tracking

---

## Safety Domain

Hazards

Incidents

Near Misses

Corrective Actions

Toolbox Talks

---

## Emergency Domain

Emergency Events

Musters

Worker Status

Emergency Reports

---

## Assets Domain

Assets

Equipment

Maintenance

Inspections

Assignments

---

## Communication Domain

Announcements

Notifications

Acknowledgements

Documents

---

## Administration Domain

Configuration

Company Settings

Feature Flags

Approval Workflows

---

## Audit Domain

Audit Logs

Activity History

Security Events

Data Change History

---

# 8. Next Section

The following sections define every table individually.

Each table specification includes:

- Purpose
- Columns
- Data Types
- Constraints
- Relationships
- Indexes
- Business Rules
- Validation Rules
- Future Expansion

---

# 9. Organization Domain

The Organization Domain represents the top-level business structure of ConstructPulse.

Every operational record ultimately belongs to a Company and is organized into Projects, Sites, Departments, Trades, and Subcontractors.

This hierarchy provides complete tenant isolation while supporting organizations operating across multiple construction projects simultaneously.

---

# 9.1 Companies

## Purpose

Represents an organization using ConstructPulse.

Each company owns its workforce, projects, sites, assets, compliance rules, reports, and configuration.

---

### Primary Fields

- id
- company_name
- legal_name
- nzbn
- logo_url
- email
- phone_number
- website
- address
- country
- timezone
- status
- created_at
- updated_at

---

### Relationships

Company

├── Projects

├── Sites

├── Departments

├── Trades

├── Subcontractors

├── Users

├── Assets

├── Incidents

├── Visitors

└── Reports

---

### Business Rules

- Company names must be unique.
- Companies cannot access another company's data.
- Soft deletion is supported.
- Branding is company-specific.

---

# 9.2 Projects

## Purpose

Represents a construction project undertaken by a company.

A project may contain one or more physical construction sites.

---

### Primary Fields

- id
- company_id
- project_code
- project_name
- client_name
- contract_number
- start_date
- expected_completion
- project_status
- project_manager_id
- created_at
- updated_at

---

### Relationships

Project

├── Sites

├── Workers

├── Assets

├── Incidents

├── Reports

└── Documents

---

### Business Rules

- Projects belong to exactly one company.
- Multiple active sites may exist within a project.
- Workers may transfer between sites under the same project.
- Archived projects become read-only.

---

# 9.3 Sites

## Purpose

Represents an operational construction site.

Attendance, GPS validation, QR codes, emergencies, occupancy, toolbox talks, and incidents are managed at the site level.

---

### Primary Fields

- id
- project_id
- company_id
- site_code
- site_name
- address
- latitude
- longitude
- attendance_radius
- capacity
- site_manager_id
- emergency_contact
- emergency_phone
- status
- created_at
- updated_at

---

### Relationships

Site

├── Worker Assignments

├── Attendance

├── Visitors

├── Vehicles

├── Assets

├── Toolbox Talks

├── Incidents

├── Emergencies

└── QR Codes

---

### Business Rules

- GPS radius is configurable.
- Every site has at least one Site Manager.
- A site belongs to exactly one project.
- Emergency information is mandatory.
- QR codes are site-specific.

---

# 9.4 Departments

## Purpose

Represents internal functional departments.

Examples include:

- Safety
- Engineering
- Survey
- Administration
- Commercial
- Planning

---

### Business Rules

- Departments are company-specific.
- Workers may belong to only one primary department.
- Departments support reporting and analytics.

---

# 9.5 Trades

## Purpose

Represents construction trade classifications.

Examples include:

- Carpenter
- Electrician
- Steel Fixer
- Scaffolder
- Painter
- Welder
- Concrete Finisher
- Crane Operator

---

### Business Rules

- Companies may configure custom trades.
- Compliance requirements may differ by trade.
- Trade analytics are supported.

---

# 9.6 Subcontractors

## Purpose

Represents subcontracting companies engaged by the primary company.

Examples include:

- ABC Electrical Ltd
- XYZ Scaffolding
- Elite Plumbing
- Prime Concrete

---

### Primary Fields

- id
- company_id
- subcontractor_name
- registration_number
- contact_person
- email
- phone
- address
- status

---

### Relationships

Subcontractor

├── Workers

├── Projects

├── Sites

├── Assets

└── Compliance

---

### Business Rules

- Workers belong to one employer (either the primary company or a subcontractor).
- Subcontractors may operate across multiple projects and sites.
- Performance metrics are tracked for subcontractors.
- Compliance is monitored independently for each subcontractor.

---

# 10. Workforce Domain

The Workforce Domain manages every individual who interacts with ConstructPulse.

This includes company employees, subcontractor employees, site management, safety personnel, directors, visitors, and future system users.

The Workforce Domain serves as the central identity layer for all operational activities including attendance, compliance, emergency management, communications, incident reporting, approvals, analytics, and reporting.

---

# 10.1 User Roles

ConstructPulse implements Role-Based Access Control (RBAC).

The default hierarchy is:

Platform Owner

↓

Company Director

↓

Operations Manager

↓

Company Administrator

↓

Project Manager

↓

Site Manager

↓

Safety Officer

↓

Supervisor / Foreman

↓

Worker

↓

Visitor

Custom roles may be created through the Administration Module.

---

# 10.2 Users

## Purpose

Represents every authenticated person in the system.

Every worker, manager, administrator, or visitor has exactly one User record.

---

## Primary Fields

- id
- company_id
- subcontractor_id (nullable)
- department_id
- trade_id
- role_id
- employee_number
- first_name
- last_name
- phone_number
- email
- date_of_birth
- gender
- profile_photo
- emergency_contact_name
- emergency_contact_number
- emergency_contact_relationship
- employment_type
- hire_date
- employment_status
- approval_status
- created_at
- updated_at

---

## Relationships

User

├── Site Assignments

├── Attendance Records

├── Compliance Records

├── Emergency Muster Status

├── Incident Reports

├── Asset Assignments

├── Notifications

├── Documents

├── Audit Logs

└── Employment History

---

## Business Rules

- Phone number must be unique.
- Email is optional.
- Every user belongs to exactly one company.
- Every user has exactly one primary role.
- Workers may belong to either:
  - Primary Company
  - Subcontractor
- Approval is mandatory before access.
- Soft deletion only.

---

# 10.3 Employment Types

Supported employment types include:

- Full Time
- Part Time
- Casual
- Contractor
- Subcontractor
- Temporary
- Visitor

Additional employment types may be configured.

---

# 10.4 Worker Approval

Every newly registered worker enters the approval workflow.

Registration

↓

Pending

↓

Site Manager Review

↓

Operations Review (Optional)

↓

Approved

↓

Active

Rejected registrations remain archived.

---

## Business Rules

- Workers cannot access operational features until approved.
- Approval history is retained permanently.
- Rejected workers may be reactivated.
- Every approval action is audited.

---

# 10.5 Site Assignments

Purpose

Allows workers to operate across multiple construction sites.

---

Primary Fields

- id
- worker_id
- site_id
- assignment_type
- start_date
- end_date
- assigned_by
- status

---

Relationships

Worker

↓

Multiple Site Assignments

↓

Attendance

↓

Analytics

---

Business Rules

- Workers may have multiple site assignments.
- Only one active check-in at a time.
- Site transfers require checkout from the previous site.
- Historical assignments remain immutable.

---

# 10.6 Worker Transfers

Purpose

Tracks transfers between sites.

Transfer Types

- Temporary
- Permanent
- Emergency
- Project Completion

Primary Fields

- id
- worker_id
- from_site_id
- to_site_id
- transfer_reason
- approved_by
- transfer_date

Business Rules

- Transfer history is permanent.
- Attendance follows the latest assignment.
- GPS validation uses the active assignment.

---

# 10.7 Employment History

Purpose

Maintains a complete employment timeline.

Recorded Events

- Registration
- Approval
- Site Assignment
- Transfer
- Promotion
- Role Change
- Suspension
- Reactivation
- Termination

Business Rules

- History cannot be deleted.
- Events are chronological.
- Every event is auditable.

---

# 10.8 Skills & Competencies

Purpose

Stores worker skills.

Examples

- Working at Heights
- First Aid
- Crane Operation
- Forklift Operation
- Confined Space
- Traffic Control

Business Rules

- Skills support workforce planning.
- Skills may expire.
- Skills link to certifications where applicable.

---

# 10.9 Emergency Contacts

Each worker stores emergency contact information.

Required Fields

- Contact Name
- Relationship
- Phone Number

Future Enhancements

- Multiple Emergency Contacts
- Medical Information
- Allergies
- Blood Group

---

# 10.10 Worker Availability

Purpose

Tracks worker availability.

Supported Statuses

- Available
- Checked In
- On Leave
- Sick Leave
- Training
- Suspended
- Terminated

This status is updated automatically through attendance and administrative workflows.

---

# 10.11 Workforce Analytics

The Workforce Domain supports reporting on:

- Total Workforce
- Company Employees
- Subcontractor Employees
- Workers per Project
- Workers per Site
- Workers per Trade
- Workers per Department
- Workforce Growth
- Worker Turnover
- Average Site Occupancy
- Compliance Rate

---

# 10.12 Future Expansion

Future versions may include:

- Digital Employee ID Cards
- Facial Recognition
- NFC Identification
- Biometric Attendance
- Digital Employment Contracts
- Training Records
- Performance Reviews
- Payroll Integration
- Leave Management
- Workforce Forecasting
- AI Workforce Allocation

---

# 11. Attendance Domain

The Attendance Domain is responsible for accurately recording workforce presence across construction projects while ensuring that attendance can only be recorded under valid operational and safety conditions.

Unlike traditional attendance systems, ConstructPulse combines QR verification, GPS validation, worker approval status, compliance verification, site assignment validation, and configurable business rules before attendance is accepted.

This ensures that only authorized personnel physically present at an approved construction site are able to check in.

---

# 11.1 Attendance Philosophy

Attendance is not simply recording a timestamp.

Attendance represents the beginning and end of a worker's authorized presence at a construction site.

Every attendance event contributes to:

- Live Site Occupancy
- Emergency Muster
- Workforce Analytics
- Compliance Reporting
- Payroll Export
- Safety Monitoring
- Historical Reporting

---

# 11.2 Attendance Workflow

Worker Opens App

↓

Authentication Verified

↓

Daily Safety Briefing Completed

↓

GPS Validation

↓

Site QR Scan

↓

Worker Assignment Validation

↓

Compliance Verification

↓

Attendance Rules Validation

↓

Attendance Recorded

↓

Live Occupancy Updated

↓

Attendance Confirmation

---

# 11.3 Attendance Record

Purpose

Represents one complete work session.

---

Primary Fields

- id
- worker_id
- company_id
- project_id
- site_id
- qr_code_id
- check_in_time
- check_out_time
- check_in_latitude
- check_in_longitude
- check_out_latitude
- check_out_longitude
- gps_accuracy
- attendance_status
- attendance_source
- approved_by
- notes
- created_at
- updated_at

---

Relationships

Attendance

↓

Worker

↓

Site

↓

Project

↓

Company

↓

Emergency Muster

↓

Analytics

---

Business Rules

- One active attendance session per worker.
- Check-out required before new site check-in.
- GPS validation mandatory.
- QR validation mandatory.
- Attendance history cannot be deleted.

---

# 11.4 Attendance Status

Supported statuses:

- Checked In
- Checked Out
- Late
- Early Departure
- Missed Checkout
- Manual Override
- Rejected

---

# 11.5 QR Code

Each site has a unique QR code.

Primary Fields

- id
- site_id
- qr_value
- generated_at
- expires_at
- is_active

Business Rules

- QR codes belong to exactly one site.
- QR codes may be regenerated.
- Expired QR codes cannot be used.
- QR codes are digitally signed.

Future Enhancements

- Rotating QR Codes
- Dynamic QR Codes
- Time-limited QR Tokens

---

# 11.6 GPS Validation

Purpose

Verifies that the worker is physically located within the approved attendance zone.

Primary Fields

- latitude
- longitude
- accuracy
- distance_from_site
- validation_result

Business Rules

- GPS permission mandatory.
- GPS accuracy configurable.
- Attendance radius configurable per site.
- Spoofed locations rejected where supported.

---

# 11.7 Attendance Radius

Each site defines its own attendance radius.

Example

Office Site

25m

Residential Site

75m

Infrastructure Project

150m

Airport Project

300m

Radius is configurable by administrators.

---

# 11.8 Shift Management

Supported shift types

- Day Shift
- Night Shift
- Weekend Shift
- Split Shift
- Overtime
- Emergency Shift

Primary Fields

- shift_name
- start_time
- end_time
- grace_period
- overtime_threshold

Business Rules

- Workers may belong to one active shift.
- Attendance validated against assigned shift.

---

# 11.9 Site Transfers

Purpose

Supports workers moving between sites during the same day.

Workflow

Check Out

↓

Transfer Approved

↓

GPS Validation

↓

Scan New Site QR

↓

Check In

Business Rules

- Multiple active attendance sessions prohibited.
- Transfer history retained permanently.
- Transfer analytics available.

---

# 11.10 Attendance Overrides

Authorized personnel may override attendance.

Allowed Roles

- Site Manager
- Company Administrator
- Operations Manager

Reasons include

- Phone Failure
- GPS Failure
- Emergency
- QR Damage
- Manual Correction

Business Rules

- Overrides require reason.
- Overrides require approval.
- Overrides are fully audited.

---

# 11.11 Live Site Occupancy

Occupancy updates immediately after:

- Check In
- Check Out
- Emergency Muster
- Worker Transfer

Occupancy Metrics

- Current Workforce
- Visitors
- Contractors
- Company Employees
- Subcontractors

Supports emergency reporting.

---

# 11.12 Attendance Validation Engine

Attendance is accepted only when all validations pass.

Required Validations

✓ User Approved

✓ Worker Active

✓ Site Assignment Exists

✓ Daily Safety Briefing Completed

✓ GPS Enabled

✓ GPS Within Radius

✓ QR Valid

✓ QR Matches Site

✓ Compliance Valid

✓ No Existing Active Attendance

Failure of any validation rejects attendance.

---

# 11.13 Offline Attendance

If internet is unavailable

Attendance is temporarily stored locally.

Queued Data

- GPS
- QR
- Timestamp
- Worker ID
- Site ID

Automatic synchronization occurs once connectivity returns.

Business Rules

- Offline attendance marked accordingly.
- Synchronization conflicts logged.
- Duplicate submissions prevented.

---

# 11.14 Attendance Analytics

Supports reporting for

- Daily Attendance
- Weekly Attendance
- Monthly Attendance
- Worker Hours
- Site Occupancy
- Attendance Trends
- Late Arrivals
- Missed Checkouts
- Overtime
- Workforce Distribution

---

# 11.15 Future Expansion

Future versions may include

- NFC Attendance
- BLE Beacon Attendance
- Facial Recognition
- Biometric Verification
- Smartwatch Check-In
- AI Attendance Anomaly Detection
- Automatic Shift Detection
- Payroll Synchronization
- Indoor Positioning
- Digital Site Entry Gates

---

# 12. Compliance Domain

The Compliance Domain ensures that every worker entering a construction site satisfies all mandatory legal, contractual, and company-specific compliance requirements.

Rather than relying on paper records, ConstructPulse maintains a digital compliance passport for every worker, automatically validating eligibility before site access is granted.

The Compliance Engine integrates directly with Attendance, Workforce Management, Emergency Management, and Reporting to enforce compliance across all construction operations.

---

# 12.1 Compliance Philosophy

ConstructPulse follows the principle:

"No Compliance = No Site Access"

Every attendance attempt is evaluated against the worker's compliance profile before access is granted.

Compliance validation occurs automatically without requiring manual intervention.

---

# 12.2 Compliance Workflow

Worker Registered

↓

Approval Completed

↓

Safety Induction Assigned

↓

Required Certifications Assigned

↓

Worker Completes Requirements

↓

Compliance Verified

↓

Compliance Passport Updated

↓

Worker Eligible for Site Access

↓

Attendance Allowed

---

# 12.3 Compliance Passport

## Purpose

Each worker has a digital Compliance Passport containing all certifications, licences, inductions, training records, and competency validations.

The passport replaces manual document verification.

---

## Primary Fields

- id
- worker_id
- compliance_status
- last_verified_at
- next_review_date
- created_at
- updated_at

---

## Relationships

Compliance Passport

├── Safety Inductions

├── Certifications

├── Licences

├── Competencies

├── Medical Clearances

├── Site Requirements

└── Compliance History

---

## Business Rules

- Every worker has exactly one Compliance Passport.
- Compliance status updates automatically.
- Passport history is permanent.
- Passport cannot be deleted.

---

# 12.4 Safety Inductions

## Purpose

Tracks mandatory safety inductions completed by workers.

Examples

- Company Induction
- Site Induction
- Project Induction
- Environmental Induction
- Emergency Procedure Training

---

## Primary Fields

- id
- worker_id
- induction_type
- project_id (optional)
- site_id (optional)
- completion_date
- expiry_date
- completed_by
- certificate_url
- status

---

## Business Rules

- Company induction required before first site access.
- Site-specific inductions required before entering new sites.
- Expired inductions invalidate compliance.
- Inductions are version-controlled.

---

# 12.5 Certifications

## Purpose

Stores trade and safety certifications.

Examples

- Working at Heights
- Confined Space
- First Aid
- Elevated Work Platform
- Forklift
- Crane Operator
- Traffic Management
- Scaffolding

---

## Primary Fields

- id
- worker_id
- certification_type
- issuing_authority
- certificate_number
- issue_date
- expiry_date
- document_url
- verification_status

---

## Business Rules

- Expiry dates are mandatory.
- Multiple certificates of the same type may exist historically.
- Only verified certificates satisfy compliance.
- Automatic expiry notifications generated.

---

# 12.6 Licences

Purpose

Tracks government-issued licences.

Examples

- Driver Licence
- Heavy Vehicle Licence
- Machinery Licence
- Electrical Licence
- Plumbing Licence

---

Primary Fields

- licence_number
- licence_type
- issuing_authority
- issue_date
- expiry_date
- verification_status

---

Business Rules

- Licence validity checked before attendance where required.
- Expired licences immediately affect compliance.

---

# 12.7 Competencies

Purpose

Represents practical competencies that may not require formal licences.

Examples

- Crane Spotter
- Fire Warden
- Traffic Controller
- Rescue Team
- Lift Supervisor

---

Business Rules

- Competencies may be site-specific.
- Competencies may expire.
- Competencies support workforce planning.

---

# 12.8 Medical Clearances

Purpose

Stores worker medical fitness information required for specific work activities.

Examples

- Fit for Heights
- Respirator Clearance
- Hearing Assessment
- Vision Test
- Drug & Alcohol Clearance

---

Business Rules

- Medical information is access-controlled.
- Expired medical clearance blocks site access where applicable.
- Sensitive information follows privacy regulations.

---

# 12.9 Site Compliance Requirements

Each construction site defines its own mandatory requirements.

Examples

Site A

- Company Induction
- Working at Heights
- First Aid

Site B

- Confined Space
- Respirator Fit Test
- Environmental Induction

Site C

- Heavy Vehicle Licence
- Traffic Management

---

Business Rules

- Requirements configurable per site.
- Compliance evaluated dynamically.
- Future requirements automatically inherited.

---

# 12.10 Compliance Validation Engine

Every attendance request executes the following validations:

✓ Worker Approved

✓ Company Induction Complete

✓ Site Induction Complete

✓ Required Certifications Valid

✓ Required Licences Valid

✓ Medical Clearance Valid

✓ Competencies Satisfied

✓ No Compliance Suspension

Only when all validations succeed is attendance permitted.

---

# 12.11 Compliance Status

Supported statuses:

- Fully Compliant
- Partially Compliant
- Pending Verification
- Expired
- Suspended
- Non-Compliant

Compliance status updates automatically whenever related records change.

---

# 12.12 Compliance Notifications

Automatic notifications include:

- Certification Expiry
- Licence Expiry
- Induction Renewal
- Missing Documentation
- Compliance Suspension
- Compliance Restored

Notification Channels

- In-App
- Push Notification

Future:

- Email
- SMS

---

# 12.13 Compliance Analytics

Supports reporting for:

- Compliance Rate
- Expiring Certifications
- Expiring Licences
- Workers Missing Inductions
- Compliance by Site
- Compliance by Trade
- Compliance by Department
- Compliance by Subcontractor
- Compliance Trends

---

# 12.14 Future Expansion

Future versions may include:

- Digital Signature Verification
- QR Verification of Certificates
- Government Licence Validation APIs
- AI Compliance Risk Assessment
- Automatic Training Recommendations
- LMS (Learning Management System) Integration
- Digital Training Modules
- eLearning Completion Tracking

---

# 13. Safety & Emergency Domain

The Safety & Emergency Domain ensures that every worker, subcontractor, visitor, and site manager can operate safely while providing immediate access to emergency procedures, incident reporting, hazard management, and emergency response capabilities.

Safety is treated as a core operational function rather than a standalone feature. Every attendance session, site assignment, and emergency response is integrated with this domain.

---

# 13.1 Safety Philosophy

ConstructPulse follows the principle:

**"Everyone Goes Home Safe."**

The platform proactively prevents unsafe site access, provides immediate emergency assistance, and maintains complete digital safety records.

Safety is embedded into every operational workflow.

---

# 13.2 Safety Workflow

Worker Assigned

↓

Daily Safety Briefing

↓

Toolbox Talk

↓

Hazard Awareness

↓

Site Entry

↓

Continuous Safety Monitoring

↓

Incident Reporting

↓

Emergency Response (If Required)

↓

Safe Site Exit

---

# 13.3 Daily Safety Briefing

## Purpose

Before starting work, every worker must review and acknowledge the daily safety briefing for the assigned site.

Daily briefings may include:

- Weather Conditions
- Site Risks
- Planned Activities
- Restricted Areas
- PPE Requirements
- Emergency Instructions
- Site Notices

---

### Primary Fields

- id
- site_id
- briefing_date
- prepared_by
- title
- description
- acknowledgement_required
- created_at

---

### Business Rules

- One briefing per site per day.
- Workers acknowledge once per day.
- Attendance cannot proceed until acknowledgement is completed (configurable).
- Acknowledgements are permanently recorded.

---

# 13.4 Toolbox Talks

## Purpose

Stores scheduled safety meetings conducted by supervisors or safety officers.

Examples

- Working at Heights
- Heat Stress
- Electrical Safety
- Excavation Safety
- Crane Operations
- Manual Handling
- Fire Prevention

---

### Primary Fields

- id
- site_id
- topic
- presenter
- meeting_date
- attendance_required
- attachments

---

### Business Rules

- Workers digitally acknowledge attendance.
- Historical records retained permanently.
- Reports available by site and project.

---

# 13.5 Hazard Register

## Purpose

Maintains all identified workplace hazards.

Examples

- Open Excavation
- Live Electrical Work
- Falling Objects
- Confined Spaces
- Heavy Machinery
- Slippery Surfaces
- High Winds

---

### Primary Fields

- id
- site_id
- hazard_type
- description
- severity
- likelihood
- risk_level
- reported_by
- assigned_to
- status
- created_at

---

### Business Rules

- Hazards remain active until resolved.
- Every hazard has an owner.
- Risk level calculated automatically.
- Historical hazard records retained.

---

# 13.6 Incident Reporting

## Purpose

Allows workers and supervisors to report workplace incidents.

Incident Types

- Injury
- Property Damage
- Environmental
- Equipment Failure
- Security
- Vehicle
- Medical Emergency

---

### Primary Fields

- id
- site_id
- incident_type
- severity
- description
- reported_by
- witnesses
- attachments
- corrective_actions
- status

---

### Business Rules

- Incidents receive unique reference numbers.
- Photos may be attached.
- Investigation history maintained.
- Reports cannot be deleted.

---

# 13.7 Near Miss Reporting

## Purpose

Encourages proactive reporting of unsafe situations before injuries occur.

Examples

- Falling Material
- Unstable Ladder
- Unsafe Scaffolding
- Electrical Exposure
- Vehicle Near Collision

---

### Business Rules

- Workers may report anonymously (configurable).
- Near misses contribute to safety analytics.
- Management receives notifications.

---

# 13.8 Emergency Contacts

Every site maintains dedicated emergency contacts.

Examples

- Site Manager
- Safety Officer
- First Aid Officer
- Fire Warden
- Emergency Coordinator

---

### Primary Fields

- id
- site_id
- contact_name
- designation
- phone_number
- priority

---

Business Rules

- Contacts are configurable per site.
- Displayed prominently inside the mobile application.
- Available without internet connectivity.

---

# 13.9 National Emergency Services

ConstructPulse stores emergency services information based on country.

For New Zealand

Emergency Number

**111**

Available Services

- Ambulance
- Fire
- Police

Additional Contacts

- Poison Centre
- Healthline
- Local Hospital
- Site Medical Provider

---

Business Rules

- Country-specific emergency numbers configurable.
- One-touch calling from mobile app.
- Available directly from the Home Screen.
- Accessible during emergency mode.

---

# 13.10 Emergency Muster

## Purpose

Tracks all personnel during emergencies.

Workflow

Emergency Declared

↓

Push Notifications Sent

↓

Workers Report to Muster Point

↓

GPS Verification (Optional)

↓

Attendance Confirmed

↓

Missing Persons Identified

↓

Final Muster Report Generated

---

### Primary Fields

- id
- emergency_id
- worker_id
- muster_status
- reported_time
- verified_by

---

Supported Statuses

- Safe
- Missing
- Injured
- Evacuated
- Assisting Others

---

Business Rules

- Muster uses current live occupancy.
- Reports generated in real time.
- Missing workers highlighted.

---

# 13.11 Emergency Events

Supported Emergency Types

- Fire
- Earthquake
- Flood
- Chemical Spill
- Gas Leak
- Medical Emergency
- Structural Collapse
- Severe Weather
- Security Threat
- Evacuation

---

Business Rules

- Emergency events timestamped.
- Incident commander assigned.
- Full audit trail maintained.

---

# 13.12 Safety Documents

Supports storage of

- SWMS
- JSA
- SOP
- Emergency Procedures
- Site Maps
- Evacuation Plans
- Environmental Plans
- Company Policies

Workers may acknowledge document review digitally.

---

# 13.13 PPE Management

Purpose

Tracks Personal Protective Equipment requirements.

Examples

- Hard Hat
- Safety Glasses
- Gloves
- High Visibility Vest
- Hearing Protection
- Respirator
- Safety Boots

---

Business Rules

- PPE requirements configurable per site.
- PPE reminders displayed during check-in.
- Future PPE inspection support.

---

# 13.14 Safety Analytics

Supports reporting for

- Incident Frequency
- Near Miss Frequency
- Hazard Resolution Time
- Toolbox Talk Attendance
- Safety Briefing Completion
- Emergency Muster Time
- Lost Time Injuries
- Total Recordable Incident Rate (TRIFR)
- Hazard Trends
- Site Safety Score

---

# 13.15 Future Expansion

Future versions may include

- AI Hazard Detection
- Computer Vision PPE Detection
- Drone Safety Inspections
- IoT Gas Sensors
- Wearable Safety Devices
- Lone Worker Monitoring
- Fatigue Detection
- Heat Stress Prediction
- Digital Permit to Work
- Lockout/Tagout Management
- Visitor Safety Passport
- Automatic Weather Alerts
- AI Safety Assistant

---

# 14. Assets, Equipment & Fleet Domain

The Assets, Equipment & Fleet Domain manages all physical resources owned, leased, or assigned to the company, including construction equipment, machinery, tools, vehicles, temporary facilities, and site assets.

The purpose of this domain is to ensure accountability, improve utilization, schedule maintenance, reduce losses, and maintain inspection records while supporting future IoT and telematics integrations.

---

# 14.1 Asset Philosophy

Every physical resource should have a digital identity.

ConstructPulse enables organizations to know:

- What assets exist
- Where they are located
- Who is responsible
- Current operational status
- Maintenance history
- Inspection history
- Utilization trends

---

# 14.2 Asset Lifecycle

Asset Registered

↓

Asset Categorized

↓

Assigned to Project

↓

Assigned to Site

↓

Assigned to Worker (Optional)

↓

Operational Use

↓

Inspection

↓

Maintenance

↓

Transfer

↓

Retirement / Disposal

---

# 14.3 Asset Categories

Supported categories include:

Heavy Machinery

- Excavators
- Bulldozers
- Cranes
- Rollers
- Loaders
- Graders

Light Equipment

- Generators
- Compressors
- Pumps
- Concrete Mixers

Power Tools

- Drills
- Grinders
- Saws
- Jackhammers

Safety Equipment

- Fire Extinguishers
- Spill Kits
- Rescue Equipment

Temporary Site Assets

- Site Offices
- Storage Containers
- Temporary Fencing
- Lighting Towers

IT Equipment

- Tablets
- Phones
- Laptops
- Printers

---

# 14.4 Assets

## Purpose

Represents every physical asset managed by the company.

---

### Primary Fields

- id
- company_id
- asset_code
- asset_name
- asset_category
- manufacturer
- model
- serial_number
- purchase_date
- purchase_cost
- warranty_expiry
- ownership_type
- operational_status
- created_at
- updated_at

---

### Relationships

Asset

├── Project

├── Site

├── Worker Assignment

├── Maintenance Records

├── Inspection Records

├── QR Code

├── Documents

└── Audit History

---

### Business Rules

- Every asset has a unique Asset Code.
- Every asset has a QR code.
- Soft deletion only.
- Full history retained.

---

# 14.5 Asset Assignment

Assets may be assigned to:

- Project
- Site
- Worker
- Department
- Subcontractor

---

### Business Rules

- Asset assignment history retained permanently.
- Assets cannot have conflicting assignments.
- Transfers require authorization.

---

# 14.6 Asset Transfers

Purpose

Tracks movement between locations.

Workflow

Current Site

↓

Transfer Requested

↓

Approved

↓

Asset Delivered

↓

Receiving Confirmation

↓

Transfer Completed

---

Business Rules

- Every transfer audited.
- GPS location optional.
- Delivery confirmation mandatory.

---

# 14.7 Equipment Inspections

Purpose

Ensures operational safety.

Inspection Types

- Daily
- Weekly
- Monthly
- Annual
- Pre-Use
- Post-Use

---

### Primary Fields

- equipment_id
- inspection_type
- inspection_date
- inspector
- findings
- photographs
- status

---

Business Rules

- Failed inspections lock equipment.
- Inspection reminders generated.
- Inspection reports retained permanently.

---

# 14.8 Preventive Maintenance

Purpose

Schedules planned maintenance.

Maintenance Types

- Scheduled
- Corrective
- Emergency
- Manufacturer Service

---

### Business Rules

- Maintenance schedules configurable.
- Overdue maintenance generates alerts.
- Maintenance history immutable.

---

# 14.9 Fleet Management

Purpose

Manages company vehicles.

Examples

- Utility Vehicles
- Trucks
- Vans
- Forklifts
- Site Buggies

---

### Primary Fields

- vehicle_id
- registration_number
- vehicle_type
- assigned_driver
- fuel_type
- odometer
- insurance_expiry
- registration_expiry

---

Business Rules

- Driver licence validation.
- Vehicle inspections required.
- Insurance monitoring.
- Registration reminders.

---

# 14.10 Consumables

Purpose

Tracks non-returnable inventory.

Examples

- Cement
- Rebar
- Bolts
- Welding Rods
- Safety Gloves
- Masks
- Fuel

---

Business Rules

- Stock movements recorded.
- Minimum stock alerts.
- Future procurement integration.

---

# 14.11 Asset QR Codes

Each asset receives a QR code.

Workers may scan to:

- View Details
- Report Damage
- Submit Inspection
- Check Assignment
- Request Maintenance

Future:

- NFC Tags
- RFID Tags

---

# 14.12 Asset Status

Supported statuses:

- Available
- Assigned
- In Use
- Under Inspection
- Under Maintenance
- Out of Service
- Retired
- Lost
- Disposed

---

# 14.13 Asset Documents

Supported documents:

- Purchase Invoice
- Warranty
- Manuals
- Inspection Reports
- Service Records
- Calibration Certificates

---

# 14.14 Asset Analytics

Supports reporting for:

- Asset Utilization
- Downtime
- Maintenance Cost
- Inspection Compliance
- Fleet Utilization
- Equipment Availability
- Asset Lifecycle Cost
- Replacement Forecast
- Fuel Consumption
- Idle Equipment

---

# 14.15 Future Expansion

Future versions may include:

- IoT Sensors
- GPS Tracking
- RFID Asset Tracking
- Predictive Maintenance
- Fuel Monitoring
- Engine Diagnostics
- Fleet Route Optimization
- AI Maintenance Prediction
- Equipment Reservation
- Digital Twin Integration

---

# 15. Visitor, Contractor & Site Access Domain

The Visitor, Contractor & Site Access Domain manages all non-permanent personnel entering construction sites while ensuring compliance with safety, security, attendance, and emergency procedures.

Unlike permanent employees, visitors and temporary personnel require controlled site access, limited permissions, digital inductions, and real-time visibility.

Every individual entering a construction site must be digitally recorded, verified, and included in emergency mustering.

---

# 15.1 Site Access Philosophy

Every person entering a construction site must be known.

ConstructPulse maintains a complete digital record of:

- Who entered
- Why they entered
- Which company they belong to
- Who approved them
- Which site they visited
- Entry time
- Exit time
- Emergency status

This replaces traditional paper visitor books.

---

# 15.2 Site Access Categories

ConstructPulse supports multiple categories of temporary site access.

Company Visitors

Client Representatives

Consultants

Architects

Engineers

Government Inspectors

Council Inspectors

Health & Safety Auditors

Suppliers

Delivery Drivers

Equipment Vendors

Interview Candidates

Temporary Labour

Training Personnel

Emergency Responders

---

# 15.3 Visitors

## Purpose

Represents temporary individuals entering construction sites.

---

### Primary Fields

- id
- visitor_name
- company_name
- phone_number
- email
- identification_type
- identification_number
- vehicle_registration
- emergency_contact
- photo
- created_at
- updated_at

---

### Relationships

Visitor

↓

Site Visit

↓

Visitor Pass

↓

Emergency Muster

↓

Safety Induction

↓

Audit Logs

---

### Business Rules

- Every visitor must have a purpose.
- Visitors must check out before leaving.
- Visitor history retained permanently.
- Visitors cannot access employee features.

---

# 15.4 Site Visits

Purpose

Represents a single visit to a construction site.

---

Primary Fields

- id
- visitor_id
- company_id
- project_id
- site_id
- purpose
- host_user_id
- approved_by
- check_in_time
- check_out_time
- visit_status

---

Business Rules

- Multiple historical visits allowed.
- One active visit per visitor.
- Automatic occupancy updates.

---

# 15.5 Digital Visitor Pass

Purpose

Generates a temporary digital site access pass.

Information displayed

- Visitor Name
- Company
- Site
- Host
- Date
- QR Code
- Access Level
- Emergency Contact

Future

- NFC Badge
- Bluetooth Badge
- Smart Access Cards

---

# 15.6 Visitor Safety Induction

Purpose

Ensures visitors understand basic site safety before entry.

Topics include

- PPE Requirements
- Emergency Exits
- Muster Point
- Restricted Areas
- Site Rules
- Speed Limits
- Hazard Awareness

---

Business Rules

- Induction acknowledgement mandatory.
- Configurable by site.
- Stored permanently.

---

# 15.7 Visitor Approval

Workflow

Visitor Registered

↓

Host Approval

↓

Site Manager Approval (Optional)

↓

Safety Induction

↓

QR Pass Generated

↓

GPS Validation

↓

Site Entry

↓

Checkout

---

Business Rules

- Approval workflow configurable.
- High-security sites may require multiple approvals.
- Visitor validity expires automatically.

---

# 15.8 Escort Management

Purpose

Some visitors require escorts.

Examples

- Government Officials
- Students
- Media
- New Contractors

---

Primary Fields

- escort_required
- escort_user_id

---

Business Rules

- Escort remains responsible.
- Escort history retained.
- Alerts generated if escort unavailable.

---

# 15.9 Delivery Management

Purpose

Tracks deliveries entering construction sites.

Examples

- Concrete Trucks
- Steel Delivery
- Fuel Tankers
- Material Suppliers

---

Primary Fields

- delivery_company
- driver_name
- vehicle_registration
- delivery_type
- arrival_time
- departure_time

---

Business Rules

- Delivery vehicles included in occupancy.
- Delivery logs retained.

---

# 15.10 Contractor Companies

Purpose

Represents subcontracting organizations working for the primary company.

Examples

Electrical Company

Scaffolding Company

Plumbing Company

Painting Company

Traffic Management Company

Concrete Company

---

Primary Fields

- id
- company_name
- registration_number
- contact_person
- phone
- email
- insurance_expiry
- status

---

Business Rules

- Contractor companies may work across multiple projects.
- Performance metrics tracked.
- Insurance expiry monitored.
- Compliance evaluated separately.

---

# 15.11 Contractor Workers

Contractor workers inherit:

- Attendance
- Compliance
- Safety
- Emergency
- Site Assignment

The only difference is employer ownership.

Business Rules

- Employer remains subcontractor.
- Operational control remains primary company.

---

# 15.12 Visitor Occupancy

Visitors contribute to live occupancy.

Dashboard includes

Workers

Visitors

Inspectors

Contractors

Suppliers

Delivery Personnel

Total People On Site

---

# 15.13 Visitor Emergency Muster

Visitors automatically appear in emergency events.

Supported statuses

Safe

Missing

Evacuated

Injured

Left Site

Visitors are treated exactly like workers during emergencies.

---

# 15.14 Visitor Analytics

Supports reporting for

- Daily Visitors
- Visitor Companies
- Contractor Companies
- Deliveries
- Average Visit Duration
- Visitor Frequency
- Site Traffic
- Contractor Performance
- Visitor Trends

---

# 15.15 Future Expansion

Future versions may include

- Facial Recognition Entry
- Smart Visitor Kiosks
- Driver Licence Verification
- Passport Scanning
- OCR Document Capture
- Vehicle ANPR Recognition
- Bluetooth Access Cards
- Digital NDA Signing
- Digital Visitor Agreements
- Contractor Rating System

---

# 16. Communications, Notifications & Document Management Domain

The Communications, Notifications & Document Management Domain serves as the central information distribution system for ConstructPulse.

It enables management to communicate with workers, subcontractors, site managers, visitors, and project teams through announcements, notifications, alerts, digital documents, acknowledgements, and operational communications.

Every important operational event should be communicated through this domain.

---

# 16.1 Communication Philosophy

The right information must reach the right people at the right time.

ConstructPulse ensures that communication is:

- Role Based
- Site Specific
- Project Specific
- Company Specific
- Traceable
- Auditable
- Actionable

---

# 16.2 Communication Types

ConstructPulse supports multiple communication channels.

Operational Announcements

Safety Alerts

Emergency Alerts

Project Updates

Maintenance Notices

Policy Updates

Compliance Notifications

Attendance Notifications

Document Notifications

Administrative Messages

Future

Instant Messaging

Video Announcements

Voice Broadcasts

---

# 16.3 Announcements

## Purpose

Allows administrators and managers to publish announcements.

Examples

- Site Closure
- Weather Warning
- New PPE Requirement
- Project Milestone
- Holiday Notice
- Equipment Downtime

---

### Primary Fields

- id
- company_id
- project_id (optional)
- site_id (optional)
- title
- description
- priority
- publish_date
- expiry_date
- created_by
- created_at

---

### Business Rules

- Announcements may target:
  - Entire Company
  - Specific Project
  - Specific Site
  - Specific Role
- Expired announcements archive automatically.
- Read history retained.

---

# 16.4 Push Notifications

## Purpose

Sends real-time notifications to mobile devices.

Supported Events

- Worker Approved
- Attendance Successful
- Attendance Rejected
- Emergency Declared
- New Safety Briefing
- Toolbox Talk Scheduled
- Incident Assigned
- Asset Assigned
- Compliance Expiry
- Site Transfer Approved

---

### Business Rules

- Notifications delivered instantly.
- Delivery status tracked.
- Retry mechanism supported.

---

# 16.5 Notification Categories

Information

Success

Warning

Critical

Emergency

Reminder

Approval

Assignment

Compliance

Maintenance

---

# 16.6 Notification Preferences

Users may configure:

- Push Notifications
- Email (Future)
- SMS (Future)
- Emergency Alerts (Mandatory)
- Quiet Hours
- Language

---

Business Rules

- Emergency notifications cannot be disabled.
- Preferences stored per user.

---

# 16.7 Digital Documents

Purpose

Stores operational documentation.

Supported Documents

- Company Policies
- Safety Procedures
- SWMS
- SOP
- JSA
- Emergency Plans
- Site Maps
- Equipment Manuals
- Induction Material
- Compliance Documents

---

### Primary Fields

- id
- company_id
- document_type
- title
- description
- version
- uploaded_by
- upload_date
- expiry_date
- file_location

---

Business Rules

- Documents version controlled.
- Previous versions retained.
- Soft delete only.

---

# 16.8 Document Acknowledgements

Purpose

Tracks whether workers have read mandatory documents.

Workflow

Document Published

↓

Worker Notification

↓

Document Opened

↓

Acknowledgement

↓

Recorded

---

Business Rules

- Mandatory acknowledgements configurable.
- Reports available.
- Attendance may require acknowledgement (configurable).

---

# 16.9 Broadcast Messages

Purpose

Allows management to send messages to groups.

Examples

Entire Company

Specific Project

Specific Site

Safety Officers

Site Managers

Workers

Visitors

Subcontractors

---

Business Rules

- Broadcast delivery tracked.
- Read receipts supported.
- Future reply support.

---

# 16.10 Emergency Broadcasts

Purpose

Distributes emergency alerts.

Examples

- Fire
- Evacuation
- Severe Weather
- Medical Emergency
- Security Threat

Workflow

Emergency Created

↓

Push Notification

↓

Emergency Screen Opens

↓

Worker Responds

↓

Emergency Dashboard Updates

---

Business Rules

- Highest priority.
- Cannot be muted.
- Supports repeated alerts.

---

# 16.11 Operational Inbox

Each user has a centralized inbox.

Contains

- Announcements
- Notifications
- Assigned Tasks
- Compliance Alerts
- Safety Alerts
- Emergency Messages
- Document Requests

---

Business Rules

- Searchable.
- Filterable.
- Read history retained.

---

# 16.12 Media Management

Supported Attachments

- Images
- PDF
- Word Documents
- Excel
- Videos
- Audio
- CAD Drawings (Future)

---

Business Rules

- File size configurable.
- Virus scanning (future).
- Version history maintained.

---

# 16.13 Communication Analytics

Supports reporting for

- Announcement Reach
- Read Rate
- Notification Delivery Rate
- Notification Failure Rate
- Average Read Time
- Mandatory Document Completion
- Broadcast Effectiveness
- Emergency Notification Response Time

---

# 16.14 Future Expansion

Future versions may include

- Team Chat
- Project Chat Rooms
- Voice Messaging
- AI Announcement Summaries
- AI Translation
- Microsoft Teams Integration
- Slack Integration
- WhatsApp Integration
- Email Integration
- SMS Gateway
- Video Training Portal
- Knowledge Base
- Digital Forms
- Electronic Signatures

---

# 17. Analytics, Reporting & Business Intelligence Domain

The Analytics, Reporting & Business Intelligence Domain transforms operational data into actionable insights for every level of the organization.

Rather than simply displaying raw data, ConstructPulse provides real-time dashboards, operational KPIs, workforce intelligence, safety metrics, compliance tracking, executive summaries, and predictive analytics to support informed decision-making.

Analytics are generated continuously from attendance, workforce movements, safety events, compliance records, asset utilization, incidents, communications, and operational activities.

---

# 17.1 Analytics Philosophy

Every action performed within ConstructPulse generates valuable operational intelligence.

The platform aims to answer questions such as:

- How many people are currently on every site?
- Which projects are understaffed?
- Which subcontractors perform best?
- Which workers have expiring certifications?
- Which sites have the highest safety risks?
- Which equipment is underutilized?
- What are today's attendance trends?
- Where are operational bottlenecks occurring?

---

# 17.2 Executive Dashboard

## Purpose

Provides Directors and Executives with a complete organization-wide overview.

---

### Executive KPIs

- Total Companies (Platform)
- Active Projects
- Active Sites
- Total Workforce
- Workers On Site
- Workers Off Site
- Visitors
- Active Contractors
- Current Site Occupancy
- Attendance Rate
- Compliance Rate
- Safety Score
- Incident Count
- Near Miss Count
- Equipment Utilization
- Open Actions
- Emergency Status

---

### Executive Charts

- Workforce Trend
- Attendance Trend
- Project Progress
- Safety Trend
- Compliance Trend
- Asset Utilization
- Incident Distribution
- Workforce Distribution
- Productivity Overview

---

# 17.3 Operations Dashboard

## Purpose

Provides Operations Managers with live operational visibility.

---

Displays

- Site Occupancy
- Worker Distribution
- Attendance Exceptions
- Site Transfers
- Pending Approvals
- Compliance Issues
- Delayed Projects
- Active Emergencies
- Equipment Downtime
- Open Incidents

---

# 17.4 Company Administrator Dashboard

Provides company administrators with management tools.

Displays

- Pending Worker Approvals
- Pending Site Assignments
- Expiring Certifications
- New Registrations
- Subcontractor Status
- User Management
- Configuration Alerts
- Document Expiry
- Communication Statistics

---

# 17.5 Project Manager Dashboard

Provides project-specific analytics.

Displays

- Workforce Count
- Attendance
- Daily Progress
- Site Occupancy
- Incidents
- Open Hazards
- Asset Utilization
- Contractor Distribution
- Daily Productivity

---

# 17.6 Site Manager Dashboard

Provides live site information.

Displays

- Workers Currently On Site
- Visitors
- Deliveries
- Active Equipment
- Toolbox Talks
- Daily Safety Briefing Status
- Attendance Exceptions
- Missing Checkouts
- Site Occupancy
- Emergency Contacts

---

# 17.7 Safety Officer Dashboard

Displays

- Active Hazards
- Near Miss Reports
- Open Incidents
- Safety Briefing Completion
- Toolbox Talk Attendance
- Emergency Muster Status
- Compliance Failures
- PPE Compliance
- Corrective Actions

---

# 17.8 Workforce Analytics

Supports reporting for

- Total Workforce
- Company Employees
- Subcontractor Employees
- Workers Per Site
- Workers Per Project
- Workers Per Trade
- Workers Per Department
- Workforce Growth
- Worker Turnover
- Average Daily Attendance
- Overtime
- Leave Statistics

---

# 17.9 Attendance Analytics

Provides

- Daily Attendance
- Weekly Attendance
- Monthly Attendance
- Late Arrivals
- Missed Checkouts
- GPS Validation Failures
- QR Scan Success Rate
- Attendance Trends
- Attendance Heat Maps
- Site Attendance Comparison

---

# 17.10 Compliance Analytics

Provides

- Compliance Percentage
- Expiring Certifications
- Missing Inductions
- Expired Licences
- Compliance By Site
- Compliance By Project
- Compliance By Trade
- Compliance By Contractor

---

# 17.11 Safety Analytics

Provides

- Incident Frequency
- Near Miss Frequency
- Lost Time Injuries
- Hazard Resolution Time
- Emergency Muster Time
- Safety Briefing Completion
- Toolbox Talk Attendance
- Site Safety Score
- Corrective Action Closure Rate

---

# 17.12 Asset Analytics

Provides

- Asset Utilization
- Equipment Downtime
- Maintenance Cost
- Maintenance Compliance
- Fleet Utilization
- Fuel Consumption (Future)
- Asset Lifecycle
- Replacement Forecast

---

# 17.13 Contractor Analytics

Provides

- Contractor Workforce
- Contractor Attendance
- Compliance Percentage
- Safety Performance
- Incident Rate
- Average Workforce
- Project Allocation
- Contractor Ranking

---

# 17.14 Project Analytics

Provides

- Workforce Allocation
- Attendance
- Compliance
- Productivity
- Equipment Usage
- Safety Performance
- Delays
- Active Risks
- Daily Progress

---

# 17.15 Reports

Supports generation of

Operational Reports

Attendance Reports

Compliance Reports

Safety Reports

Emergency Reports

Asset Reports

Contractor Reports

Visitor Reports

Inspection Reports

Incident Reports

Audit Reports

Management Reports

---

# 17.16 Report Export

Supported Formats

- PDF
- Excel
- CSV

Future

- Power BI
- Tableau
- Microsoft Fabric
- API Integrations

---

# 17.17 Scheduled Reports

Reports may be automatically generated.

Examples

Daily Attendance

Weekly Compliance

Monthly Safety

Executive Summary

Project Status

Equipment Maintenance

Incident Summary

Contractor Performance

---

# 17.18 Predictive Analytics

Future AI capabilities

- Workforce Forecasting
- Attendance Prediction
- Labour Demand Forecast
- Incident Risk Prediction
- Safety Risk Scoring
- Equipment Failure Prediction
- Compliance Risk Prediction
- Project Delay Prediction

---

# 17.19 Business Intelligence

Future Business Intelligence Features

- Interactive Dashboards
- Drill Down Reports
- KPI Builder
- Dashboard Builder
- Custom Widgets
- Cross Company Benchmarking
- Geographic Heat Maps
- AI Generated Insights

---

# 17.20 Future Expansion

Future versions may include

- AI Executive Assistant
- Voice Analytics
- Natural Language Reporting

Examples

"Show today's workforce"

"Which sites are understaffed?"

"Show attendance for Auckland projects."

"List expiring certifications."

"Compare contractor performance."

Generate automatic executive summaries.

---

# 18. Administration, Configuration & System Management Domain

The Administration, Configuration & System Management Domain is the control center of ConstructPulse.

This domain enables authorized personnel to configure, manage, and govern the platform without requiring software modifications. All configurable business rules, organizational settings, user permissions, workflows, branding, and operational parameters are managed centrally.

The objective is to ensure that ConstructPulse remains flexible enough to support different construction companies, projects, countries, regulations, and future business growth while maintaining security, auditability, and operational consistency.

---

# 18.1 Administration Philosophy

ConstructPulse follows the principle:

**"Configuration Over Custom Development."**

Administrators should be able to configure business operations through the platform rather than requiring developers to modify source code.

Configuration changes should take effect immediately while maintaining complete audit history.

---

# 18.2 Administration Hierarchy

Platform Owner

↓

Company Director

↓

Operations Manager

↓

Company Administrator

↓

Project Manager

↓

Site Manager

↓

Safety Officer

↓

Supervisor

Each level has predefined permissions that may be customized through Role-Based Access Control (RBAC).

---

# 18.3 Company Configuration

Purpose

Stores organization-specific settings.

Configuration Includes

- Company Name
- Legal Name
- Company Logo
- Brand Colours
- NZBN
- GST Number
- Contact Information
- Address
- Time Zone
- Country
- Language
- Currency
- Date Format
- Working Week
- Default Shift

---

Business Rules

- One configuration per company.
- Company branding automatically applies throughout the mobile application.
- Settings are versioned and auditable.

---

# 18.4 Project Configuration

Administrators may configure:

- Projects
- Project Codes
- Project Managers
- Client Information
- Project Status
- Start & End Dates
- Project Documentation
- Reporting Rules

Projects may contain multiple construction sites.

---

# 18.5 Site Configuration

Each site may configure:

- GPS Coordinates
- Attendance Radius
- Site QR Code
- Emergency Contacts
- Muster Points
- Working Hours
- Site Capacity
- Visitor Rules
- Safety Briefings
- PPE Requirements
- Required Inductions
- Required Certifications

---

Business Rules

- Every site belongs to one project.
- QR codes regenerate securely.
- Radius configurable individually.

---

# 18.6 Workforce Configuration

Administrators may configure:

Departments

Trades

Employment Types

Shift Types

Worker Categories

Approval Workflows

Default Permissions

Emergency Contacts

---

Business Rules

Configuration changes affect future records while preserving historical data.

---

# 18.7 Role & Permission Management

ConstructPulse implements Role-Based Access Control.

Default Roles

- Director
- Operations Manager
- Company Administrator
- Project Manager
- Site Manager
- Safety Officer
- Supervisor
- Worker
- Visitor

Administrators may create additional custom roles.

---

Permission Categories

- View
- Create
- Edit
- Delete
- Approve
- Export
- Configure
- Audit

Permissions are configurable at module level.

---

# 18.8 Approval Workflow Configuration

Approval workflows may be configured independently for:

- Worker Registration
- Site Assignment
- Worker Transfer
- Visitor Entry
- Asset Assignment
- Incident Closure
- Hazard Resolution
- Compliance Approval

---

Approval levels may include:

Single Approval

Dual Approval

Multi-Level Approval

Automatic Approval (Configurable)

---

# 18.9 Notification Configuration

Administrators configure:

Push Notifications

Announcement Templates

Reminder Schedules

Emergency Alerts

Compliance Alerts

Maintenance Alerts

Attendance Alerts

Future

Email Templates

SMS Templates

---

# 18.10 Country Configuration

ConstructPulse supports country-specific operational settings.

Examples

New Zealand

Australia

Singapore

United Kingdom

Future countries may be added without modifying application code.

Country-specific configuration includes:

- Emergency Numbers
- Public Holidays
- Date Format
- Time Zone
- Labour Regulations
- Compliance Requirements

---

# 18.11 Branding Configuration

Each company may customize:

- Logo
- Splash Screen
- Primary Colour
- Secondary Colour
- Accent Colour
- Login Screen
- Reports
- Email Templates (Future)

---

Business Rules

Branding changes apply immediately across the platform.

---

# 18.12 Feature Flags

Purpose

Allows features to be enabled or disabled without software deployment.

Examples

GPS Attendance

Offline Mode

Visitor Management

Asset Management

Emergency Muster

Fleet Management

AI Features

Payroll Integration

---

Business Rules

Feature availability is configurable per company.

---

# 18.13 Audit Configuration

Administrators configure:

Audit Retention

Login History

Security Events

Attendance Logs

Configuration Changes

Approval History

Document Access

Export History

---

Audit logs cannot be modified.

---

# 18.14 Data Retention Policies

Administrators define retention periods for:

Attendance

Visitors

Notifications

Documents

Incidents

Audit Logs

Communications

Historical Reports

---

Retention policies comply with company and legal requirements.

---

# 18.15 Backup Configuration

Configuration Includes

Automatic Backup

Backup Frequency

Retention Period

Recovery Validation

Disaster Recovery Settings

Future Cloud Replication

---

# 18.16 System Health Dashboard

Displays

API Status

Database Status

Storage Usage

Notification Queue

Background Jobs

Application Version

Connected Devices

Worker Sessions

Current Occupancy

---

# 18.17 License & Subscription Management

Future SaaS capabilities include:

Company Licences

Subscription Plans

User Limits

Storage Limits

Feature Access

Billing Integration

---

# 18.18 Multi-Tenant Management

ConstructPulse supports complete tenant isolation.

Each company has isolated:

- Users
- Projects
- Sites
- Assets
- Attendance
- Reports
- Documents
- Notifications
- Analytics

No company can access another company's data.

---

# 18.19 Future Expansion

Future administration capabilities include:

- Multi-language Management
- AI Configuration Assistant
- Dynamic Workflow Builder
- Form Builder
- Dashboard Builder
- Report Builder
- Custom Approval Engine
- Integration Marketplace
- Third-party Plugin Support
- White-label Platform Management

---

# 19. Audit, Logging & Security Domain

The Audit, Logging & Security Domain provides complete visibility into every significant action performed within ConstructPulse while protecting organizational data, ensuring regulatory compliance, detecting suspicious activities, and supporting forensic investigations.

Every important action performed by users, administrators, background services, and external integrations is recorded in an immutable audit trail.

Security is implemented as a foundational layer across the platform rather than an isolated feature.

---

# 19.1 Security Philosophy

ConstructPulse follows the principles:

- Zero Trust
- Least Privilege Access
- Defense in Depth
- Secure by Default
- Privacy by Design
- Complete Auditability
- Immutable History

Every request is authenticated, authorized, validated, and audited.

---

# 19.2 Security Layers

Platform Security

↓

Network Security

↓

Authentication

↓

Authorization

↓

Application Security

↓

Business Rule Validation

↓

Audit Logging

↓

Monitoring

↓

Incident Response

---

# 19.3 Audit Logs

## Purpose

Maintains an immutable record of all important activities performed within the platform.

---

### Primary Fields

- id
- company_id
- user_id
- module
- action
- entity_type
- entity_id
- previous_value
- new_value
- ip_address
- device_information
- location
- timestamp

---

### Business Rules

- Audit logs cannot be modified.
- Audit logs cannot be deleted.
- Every critical business action generates an audit event.
- Audit records remain searchable.

---

# 19.4 Activity Logging

The system records:

Authentication

Authorization

Attendance

Worker Approval

Transfers

Asset Assignment

Document Uploads

Configuration Changes

Emergency Events

Incident Updates

Hazard Updates

Visitor Entries

Notification Broadcasts

Report Generation

Data Export

Administrative Actions

---

# 19.5 Login History

Every login stores:

- User
- Device
- Operating System
- App Version
- IP Address
- Country
- Login Time
- Logout Time
- Session Duration

---

Business Rules

- Failed logins recorded.
- Suspicious login attempts flagged.
- Multiple simultaneous sessions configurable.

---

# 19.6 Session Management

Each authenticated device receives an active session.

Session Information

- Device Name
- Device Type
- App Version
- Login Time
- Last Activity
- Current Status

---

Business Rules

- Administrators may terminate sessions.
- Idle sessions expire automatically.
- Refresh tokens rotate securely.

---

# 19.7 Device Management

Registered devices maintain:

- Device Identifier
- Platform
- Manufacturer
- Model
- OS Version
- Last Login
- Push Notification Token

---

Business Rules

- Device history retained.
- Lost devices may be revoked.
- Maximum active devices configurable.

---

# 19.8 GPS Security

Purpose

Prevents fraudulent attendance.

Validation Includes

- GPS Radius
- GPS Accuracy
- Mock Location Detection (Supported Devices)
- Timestamp Validation
- Site Coordinate Verification

---

Business Rules

- Invalid GPS rejects attendance.
- GPS anomalies recorded.
- Repeated violations flagged.

---

# 19.9 QR Security

QR Security Features

- Unique QR Per Site
- Digitally Signed QR
- Configurable QR Expiry
- Regeneration Support
- Dynamic QR (Future)

---

Business Rules

- Screenshot sharing discouraged through rotating QR codes.
- Invalid QR usage logged.
- Repeated invalid scans flagged.

---

# 19.10 Authentication Security

Authentication Methods

- Firebase Phone OTP
- JWT Access Token
- Refresh Token

Future

- Microsoft Entra ID
- Google Workspace
- Multi-Factor Authentication
- SSO

---

Business Rules

- OTP expires automatically.
- Tokens rotate securely.
- Refresh tokens may be revoked.

---

# 19.11 Authorization Security

Authorization follows Role-Based Access Control.

Hierarchy

Permission

↓

Permission Group

↓

Role

↓

User

---

Every API request validates:

- Authentication
- Company Ownership
- Role Permission
- Module Permission
- Record Ownership

---

# 19.12 Data Protection

Sensitive information includes:

- Personal Details
- Emergency Contacts
- Medical Information
- Compliance Documents
- Incident Reports

---

Protection Measures

- HTTPS
- Encryption at Rest
- Encryption in Transit
- Secure Storage
- Access Logging

---

# 19.13 Privacy Compliance

ConstructPulse supports compliance with:

- New Zealand Privacy Act
- GDPR (Future)
- ISO 27001 Best Practices
- Company Data Retention Policies

---

Features Include

- Data Export
- Data Retention
- Data Access Logs
- Consent Tracking
- Privacy Settings

---

# 19.14 Security Monitoring

The platform continuously monitors:

- Failed Logins
- Brute Force Attempts
- GPS Anomalies
- Invalid QR Scans
- Unauthorized API Requests
- Suspicious Device Activity
- Excessive Data Exports

---

Business Rules

- High-risk events generate alerts.
- Security incidents remain auditable.

---

# 19.15 Account Protection

Supported Features

- Account Lockout
- Passwordless Authentication
- OTP Retry Limits
- Session Timeout
- Device Revocation
- Emergency Account Disable

---

# 19.16 API Security

Security Measures

- JWT Validation
- HTTPS Only
- Rate Limiting
- Request Validation
- Input Sanitization
- SQL Injection Prevention
- CORS Configuration
- Secure Headers

---

# 19.17 Backup Security

All backups include:

- Encryption
- Integrity Verification
- Retention Policies
- Recovery Testing

Future

- Multi-region Replication
- Automated Disaster Recovery

---

# 19.18 Security Analytics

Supports reporting for:

- Login Success Rate
- Failed Login Attempts
- Active Sessions
- Device Distribution
- GPS Validation Failures
- QR Validation Failures
- Security Alerts
- Audit Activity
- API Usage
- Data Exports

---

# 19.19 Future Expansion

Future versions may include:

- AI Threat Detection
- Behavioral Analytics
- Risk-Based Authentication
- Device Trust Scoring
- Biometric Authentication
- Security Operations Dashboard
- SIEM Integration
- SOC Monitoring
- Advanced Fraud Detection
- Continuous Security Assessment

---

# 20. Integration & External Services Domain

The Integration & External Services Domain enables ConstructPulse to securely exchange information with third-party platforms, government systems, enterprise software, cloud services, and future AI services.

Rather than tightly coupling external integrations with business logic, ConstructPulse follows an Integration Layer architecture where every external dependency communicates through standardized interfaces and service adapters.

This ensures scalability, maintainability, and the ability to replace or extend integrations without affecting core platform functionality.

---

# 20.1 Integration Philosophy

ConstructPulse follows the principle:

**"Integrate, Don't Duplicate."**

External systems remain the source of truth for their respective domains while ConstructPulse consumes or publishes information through secure APIs.

Integrations should be:

- Secure
- Loosely Coupled
- Event Ready
- Version Controlled
- Auditable
- Configurable

---

# 20.2 Integration Architecture

Mobile Application

↓

ConstructPulse API

↓

Integration Layer

↓

External Systems

↓

Response Processing

↓

Business Logic

↓

Database

---

# 20.3 Authentication Integrations

Current

- Firebase Phone Authentication

Future

- Microsoft Entra ID
- Google Workspace
- Okta
- Auth0
- Apple Sign-In

Business Rules

- Authentication providers are configurable.
- User identities remain unique.
- Single Sign-On supported in future.

---

# 20.4 Mapping & Location Services

Current

- Google Maps
- GPS Services

Future

- Mapbox
- OpenStreetMap
- HERE Maps

Supported Features

- Site Locations
- Geofencing
- Route Navigation
- Distance Calculation
- Live Worker Position (Future)

---

# 20.5 Notification Services

Current

- Firebase Cloud Messaging

Future

- Twilio SMS
- SendGrid Email
- Microsoft Teams
- Slack
- WhatsApp Business API

Supported Notifications

- Attendance
- Compliance
- Safety
- Emergency
- Administration

---

# 20.6 Government & Regulatory Integrations

Future integrations may include:

- NZ Business Register (NZBN)
- WorkSafe New Zealand
- Immigration Verification
- Driver Licence Verification
- Trade Certification Validation

Business Rules

- API failures do not interrupt platform operation.
- Integration status monitored continuously.

---

# 20.7 Payroll Integrations

Future Supported Platforms

- Xero Payroll
- MYOB
- Employment Hero
- SAP SuccessFactors
- Oracle HCM

Exported Information

- Attendance
- Hours Worked
- Overtime
- Leave
- Shift Information

---

# 20.8 ERP Integrations

Future Supported Systems

- SAP
- Oracle ERP
- Microsoft Dynamics 365
- Procore
- Autodesk Construction Cloud

Data Exchange

- Projects
- Assets
- Workforce
- Cost Codes
- Equipment

---

# 20.9 IoT Integrations

Future Support

- GPS Trackers
- RFID Readers
- BLE Beacons
- Smart Helmets
- Wearable Devices
- Environmental Sensors
- Fuel Sensors
- Machine Telemetry

---

# 20.10 Document Storage

Current

- Local Storage

Future

- AWS S3
- Azure Blob Storage
- Google Cloud Storage
- SharePoint

Supported Documents

- Images
- PDFs
- Videos
- CAD Drawings
- Certificates
- Site Plans

---

# 20.11 AI Integrations

Future AI Services

- OpenAI
- Azure OpenAI
- Anthropic Claude
- Local LLM Deployment

Capabilities

- Incident Summaries
- Safety Recommendations
- Workforce Forecasting
- Risk Analysis
- Executive Reports
- Natural Language Search

---

# 20.12 Weather Services

Future Integrations

- MetService New Zealand
- OpenWeather
- Tomorrow.io

Supported Features

- Severe Weather Alerts
- Wind Warnings
- Heat Stress Warnings
- Rain Forecasts
- Lightning Alerts

Weather data may influence attendance, safety briefings, and project planning.

---

# 20.13 Emergency Services

Country-specific emergency information.

New Zealand

Emergency Number

111

Future countries may define:

- Police
- Fire
- Ambulance
- Poison Centre
- Health Services

Emergency contacts are configurable at both country and site level.

---

# 20.14 Integration Monitoring

The platform monitors:

- API Availability
- Response Time
- Authentication Failures
- Data Synchronization
- Queue Failures
- Retry Attempts
- Integration Health

Integration dashboards provide operational visibility.

---

# 20.15 Future Expansion

Future integrations may include:

- BIM Platforms
- Digital Twin Platforms
- Drone Inspection Systems
- Facial Recognition Providers
- Smart Access Gates
- Financial Systems
- Procurement Platforms
- ESG Reporting Systems
- Carbon Tracking Platforms
- AI Construction Copilots

---

# 21. AI, Automation & Workflow Engine Domain

The AI, Automation & Workflow Engine Domain provides intelligent decision support, automated business processes, configurable workflow orchestration, and predictive operational insights across the ConstructPulse platform.

Unlike traditional construction management systems that rely on manual administration, ConstructPulse continuously analyzes operational data to automate repetitive tasks, assist decision-makers, and proactively identify risks before they become operational problems.

The AI layer is designed as an enhancement layer rather than a replacement for human decision making.

---

# 21.1 Design Philosophy

ConstructPulse follows three core principles.

Automate Repetitive Tasks

Assist Human Decisions

Predict Operational Risks

The platform should reduce administrative effort while allowing managers to retain complete control over final business decisions.

---

# 21.2 Automation Engine

The Automation Engine executes configurable business rules whenever predefined events occur.

Examples

Worker Registered

↓

Assign Default Safety Induction

↓

Notify Site Manager

↓

Create Approval Request

↓

Schedule Compliance Review

↓

Enable Site Access After Approval

---

Automation events may be triggered by:

- User Registration
- Attendance
- Worker Transfer
- Incident Reporting
- Compliance Expiry
- Asset Assignment
- Visitor Registration
- Project Creation
- Site Creation
- Emergency Declaration

---

# 21.3 Workflow Engine

Every operational process is defined as a configurable workflow.

Supported Workflows

- Worker Registration
- Worker Approval
- Visitor Approval
- Site Assignment
- Worker Transfer
- Incident Investigation
- Hazard Resolution
- Asset Assignment
- Maintenance Approval
- Emergency Response

---

Workflow States

Draft

↓

Pending

↓

Under Review

↓

Approved

↓

Completed

↓

Archived

---

Business Rules

- Workflow steps configurable.
- Multiple approval levels supported.
- SLA timers configurable.
- Escalation supported.

---

# 21.4 Intelligent Approval Engine

Approval routing is determined automatically based on configurable rules.

Examples

Worker Registration

↓

Assigned Site

↓

Responsible Site Manager

↓

Approve

-------------------------

High Risk Incident

↓

Safety Officer

↓

Operations Manager

↓

Director

↓

Close Investigation

---

Approval routing supports:

- Role Based Routing
- Project Based Routing
- Site Based Routing
- Department Based Routing
- Conditional Routing

---

# 21.5 Smart Notifications

The system automatically generates notifications for:

- Expiring Certifications
- Missing Check-Outs
- Site Capacity Exceeded
- Worker Transfer Requests
- Emergency Alerts
- New Incidents
- Pending Approvals
- Overdue Maintenance
- Compliance Failures
- Weather Warnings

Notification frequency is configurable.

---

# 21.6 AI Workforce Planning

Future AI capabilities include:

- Workforce Demand Forecasting
- Skill Gap Analysis
- Labour Allocation Optimization
- Shift Optimization
- Workforce Utilization
- Recruitment Forecasting

AI recommendations remain advisory.

Managers make final decisions.

---

# 21.7 AI Safety Assistant

Future capabilities include:

- Hazard Prediction
- Incident Trend Analysis
- Near Miss Analysis
- Toolbox Talk Recommendations
- Daily Safety Summary
- PPE Compliance Suggestions
- High Risk Worker Detection

---

# 21.8 AI Compliance Assistant

Future capabilities include:

- Compliance Gap Detection
- Certification Expiry Forecasting
- Training Recommendations
- Site Readiness Scoring
- Contractor Compliance Monitoring

---

# 21.9 AI Reporting Assistant

Managers may request reports using natural language.

Examples

"Show today's attendance."

"Which workers have expired certificates?"

"List all active hazards."

"Generate this week's executive summary."

"Compare contractor performance."

The assistant generates reports automatically using platform data.

---

# 21.10 Predictive Analytics

Future predictive capabilities include:

- Incident Probability
- Project Delay Prediction
- Equipment Failure Prediction
- Workforce Shortage Prediction
- Attendance Forecasting
- Compliance Risk Prediction
- Site Safety Scoring

---

# 21.11 Rule Engine

ConstructPulse provides a configurable business rule engine.

Examples

IF

Attendance Radius > 100m

AND

GPS Accuracy < 20m

THEN

Allow Attendance

-------------------------

IF

Certification Expired

THEN

Reject Site Entry

-------------------------

IF

Site Capacity Exceeded

THEN

Notify Site Manager

Reject Additional Check-Ins

---

Business Rules

- Rules configurable by administrators.
- No code changes required.
- Rules version controlled.

---

# 21.12 AI Knowledge Assistant

Future enterprise assistant capable of answering operational questions.

Examples

"What is the evacuation procedure?"

"Who is currently on Site A?"

"Where is Excavator EX-102?"

"When does John's Working at Heights certificate expire?"

"How many workers are allocated to Project Alpha?"

---

# 21.13 Automation Analytics

Reports include:

- Workflow Completion Time
- Approval Delays
- Automation Success Rate
- Escalation Frequency
- Average Resolution Time
- Manual Override Rate
- AI Recommendation Usage

---

# 21.14 Future Expansion

Future versions may include:

- Autonomous Scheduling
- Voice Assistants
- AI Project Manager
- AI Safety Coach
- AI Compliance Auditor
- Digital Twin Integration
- Construction Copilot
- Generative Reporting
- Autonomous Site Monitoring
- Multi-Agent Workflow Automation

---

# 22. Entity Relationship Model (ERM) & Database Relationships

The Entity Relationship Model (ERM) defines how all business entities within ConstructPulse interact with one another.

The objective is to maintain data integrity, eliminate redundancy, enforce referential integrity, and support efficient operational workflows across the platform.

The database follows a normalized relational model using PostgreSQL with UUID primary keys and foreign key constraints.

---

# 22.1 Core Entity Hierarchy

Platform

↓

Companies

↓

Projects

↓

Sites

↓

Zones (Optional Future)

↓

Operations

Every operational record ultimately belongs to a Company and is associated with a Project and Site where applicable.

---

# 22.2 Organization Relationships

Company

├── Projects (1:N)

├── Sites (1:N)

├── Departments (1:N)

├── Trades (1:N)

├── Users (1:N)

├── Contractor Companies (1:N)

├── Assets (1:N)

├── Visitors (1:N)

├── Reports (1:N)

└── Configuration (1:1)

---

# 22.3 Project Relationships

Project

├── Sites (1:N)

├── Site Managers (1:N)

├── Workers (M:N)

├── Assets (M:N)

├── Incidents (1:N)

├── Hazards (1:N)

├── Documents (1:N)

└── Reports (1:N)

---

# 22.4 Site Relationships

Site

├── Attendance Records (1:N)

├── Worker Assignments (1:N)

├── Visitors (1:N)

├── Safety Briefings (1:N)

├── Toolbox Talks (1:N)

├── Hazards (1:N)

├── Incidents (1:N)

├── Emergency Events (1:N)

├── Muster Records (1:N)

├── Assets (1:N)

├── Deliveries (1:N)

└── QR Codes (1:N)

---

# 22.5 Workforce Relationships

User

├── Attendance Records (1:N)

├── Site Assignments (1:N)

├── Compliance Passport (1:1)

├── Certifications (1:N)

├── Licences (1:N)

├── Competencies (1:N)

├── Incident Reports (1:N)

├── Asset Assignments (1:N)

├── Notifications (1:N)

├── Audit Logs (1:N)

└── Employment History (1:N)

---

# 22.6 Attendance Relationships

Attendance Record

↓

Worker

↓

Site

↓

Project

↓

Company

↓

Emergency Muster

↓

Analytics

↓

Payroll Export (Future)

---

# 22.7 Compliance Relationships

Compliance Passport

├── Safety Inductions

├── Certifications

├── Licences

├── Medical Clearances

├── Competencies

└── Compliance History

---

# 22.8 Safety Relationships

Incident

↓

Hazards

↓

Corrective Actions

↓

Investigation

↓

Closure

Emergency Event

↓

Emergency Muster

↓

Workers

↓

Visitors

↓

Contractors

---

# 22.9 Asset Relationships

Asset

↓

Company

↓

Project

↓

Site

↓

Assignment

↓

Maintenance

↓

Inspection

↓

Documents

↓

Audit Logs

---

# 22.10 Visitor Relationships

Visitor

↓

Site Visit

↓

Host User

↓

Visitor Pass

↓

Emergency Muster

↓

Audit Logs

---

# 22.11 Notification Relationships

Announcement

↓

Target Audience

↓

Notification

↓

Acknowledgement

↓

Audit Log

---

# 22.12 Administration Relationships

Role

↓

Permission Group

↓

Permission

↓

User

↓

Module Access

↓

Audit Log

---

# 22.13 Cross-Domain Relationships

Attendance

↔ Compliance

Attendance

↔ Safety

Attendance

↔ Analytics

Attendance

↔ Emergency Muster

Assets

↔ Maintenance

Visitors

↔ Emergency

Projects

↔ Workforce

Projects

↔ Assets

Projects

↔ Reports

---

# 22.14 Data Ownership

Every operational record contains:

- Company ID
- Project ID (where applicable)
- Site ID (where applicable)

This ensures strict multi-tenant isolation and enables project-level and site-level reporting.

---

# 22.15 Future Relationship Expansion

Future versions may introduce relationships for:

- BIM Models
- Digital Twins
- ESG Metrics
- Carbon Tracking
- Procurement
- Financial Cost Codes
- AI Recommendations
- IoT Devices
- Smart Wearables
- Construction Scheduling Systems

---

# 23. Database Indexing Strategy

The Database Indexing Strategy defines how ConstructPulse optimizes query performance while maintaining efficient write operations across high-volume construction workforce data.

Indexes are designed to support operational workloads, analytical reporting, audit searches, attendance tracking, compliance validation, and real-time dashboard updates.

The strategy prioritizes low-latency lookups, scalable filtering, and efficient joins across all major business domains.

---

# 23.1 Indexing Philosophy

ConstructPulse follows the principles:

- Index Frequently Queried Data
- Minimize Write Overhead
- Optimize Join Performance
- Support Multi-Tenant Queries
- Support Time-Series Queries
- Avoid Duplicate Indexes

Indexes should improve performance without unnecessarily increasing storage or insert/update costs.

---

# 23.2 Primary Key Indexes

Every table uses:

UUID PRIMARY KEY

Primary keys are automatically indexed.

Example

users.id

companies.id

projects.id

sites.id

attendance.id

assets.id

incidents.id

---

# 23.3 Foreign Key Indexes

All foreign key columns must be indexed.

Examples

company_id

project_id

site_id

worker_id

department_id

trade_id

subcontractor_id

asset_id

visitor_id

emergency_id

This significantly improves JOIN performance.

---

# 23.4 Multi-Tenant Indexes

Every operational table should include composite indexes for tenant isolation.

Examples

(company_id, status)

(company_id, project_id)

(company_id, site_id)

(company_id, created_at)

These indexes ensure queries remain efficient as multiple companies are onboarded.

---

# 23.5 Attendance Indexes

Recommended indexes

(worker_id, check_in_time)

(site_id, attendance_status)

(site_id, check_in_time)

(project_id, check_in_time)

(company_id, check_in_time)

(check_out_time)

(status)

Purpose

- Live Occupancy
- Attendance History
- Payroll Export
- Site Dashboard

---

# 23.6 Workforce Indexes

Recommended indexes

(phone_number)

(employee_number)

(role_id)

(department_id)

(trade_id)

(subcontractor_id)

(employment_status)

(approval_status)

(company_id, role_id)

(company_id, department_id)

---

# 23.7 Compliance Indexes

(certification_expiry)

(licence_expiry)

(compliance_status)

(worker_id)

(site_id)

(company_id)

Purpose

- Expiry Reports
- Compliance Dashboard
- Site Entry Validation

---

# 23.8 Safety Indexes

(site_id)

(status)

(severity)

(risk_level)

(created_at)

(incident_type)

Purpose

- Incident Reporting
- Hazard Dashboard
- Safety Analytics

---

# 23.9 Asset Indexes

(asset_code)

(serial_number)

(asset_status)

(site_id)

(project_id)

(asset_category)

Purpose

- QR Lookup
- Asset Search
- Maintenance Dashboard

---

# 23.10 Visitor Indexes

(visitor_name)

(phone_number)

(company_name)

(site_id)

(check_in_time)

(visit_status)

Purpose

- Fast Visitor Lookup
- Occupancy
- Security Audits

---

# 23.11 Notification Indexes

(user_id)

(notification_status)

(priority)

(created_at)

(read_status)

Purpose

- User Inbox
- Push Delivery
- Notification History

---

# 23.12 Audit Indexes

(user_id)

(module)

(action)

(entity_type)

(entity_id)

(timestamp)

Purpose

- Audit Search
- Investigation
- Security Monitoring

---

# 23.13 Full Text Search

ConstructPulse supports PostgreSQL Full Text Search for:

Projects

Sites

Workers

Assets

Visitors

Documents

Incidents

Announcements

This enables fast keyword-based searching across the platform.

---

# 23.14 Partial Indexes

Partial indexes are recommended for frequently queried subsets.

Examples

Only Active Workers

Only Pending Approvals

Only Open Incidents

Only Active Projects

Only Available Assets

This reduces index size while improving query performance.

---

# 23.15 Composite Indexes

Examples

(company_id, project_id, site_id)

(site_id, attendance_status)

(worker_id, attendance_status)

(company_id, created_at)

(project_id, status)

These indexes optimize common filtering patterns.

---

# 23.16 Performance Monitoring

Database performance should be continuously monitored.

Metrics include:

- Slow Queries
- Index Usage
- Sequential Scans
- Cache Hit Ratio
- Lock Contention
- Query Latency
- Deadlocks

Unused indexes should be reviewed periodically.

---

# 23.17 Future Expansion

Future optimizations may include:

- Table Partitioning
- Read Replicas
- Materialized Views
- Distributed PostgreSQL
- Query Caching
- Search Engine Integration (Elasticsearch/OpenSearch)
- Time-Series Optimization

---

# 24. Database Performance Optimization

The Database Performance Optimization strategy ensures that ConstructPulse maintains high performance, low latency, and reliable operation under increasing workloads while supporting enterprise-scale construction operations.

The objective is to provide consistent response times for operational workflows, analytics, reporting, and real-time dashboards regardless of database growth.

Performance optimization is considered throughout the database lifecycle rather than as a post-deployment activity.

---

# 24.1 Performance Objectives

ConstructPulse is designed to achieve the following targets under normal operating conditions.

Target API Response Time

- Less than 300 milliseconds

Attendance Check-In

- Less than 2 seconds

Dashboard Load Time

- Less than 3 seconds

Worker Search

- Less than 500 milliseconds

Emergency Muster Dashboard

- Less than 2 seconds

Notification Delivery

- Less than 5 seconds

---

# 24.2 Optimization Principles

The database follows these principles.

- Optimize Read Performance
- Maintain Fast Write Operations
- Reduce Lock Contention
- Minimize Database Round Trips
- Efficient Query Planning
- Predictable Performance
- Horizontal Scalability

---

# 24.3 Query Optimization

All production queries should:

- Use indexed columns
- Avoid unnecessary SELECT *
- Retrieve only required fields
- Limit returned records
- Support pagination
- Minimize nested joins
- Avoid N+1 query patterns

Business Rules

- ORM queries should use eager loading where appropriate.
- Complex reports should be executed asynchronously.
- Frequently used queries should be reviewed regularly.

---

# 24.4 Connection Pooling

The application shall use database connection pooling.

Recommended Configuration

- Minimum Connections: Configurable
- Maximum Connections: Configurable
- Connection Timeout: Configurable
- Idle Timeout: Configurable

Benefits

- Faster request processing
- Reduced connection overhead
- Improved scalability

---

# 24.5 Caching Strategy

Frequently accessed data may be cached.

Examples

- Company Configuration
- Site Configuration
- Department Lists
- Trade Lists
- User Permissions
- Role Definitions
- Feature Flags

Future

Redis may be introduced for distributed caching.

---

# 24.6 Background Processing

Long-running operations should execute outside user requests.

Examples

- Report Generation
- Notification Broadcasting
- Compliance Evaluation
- Backup Jobs
- AI Processing
- Data Export
- Scheduled Reports

Future Technologies

- Celery
- RabbitMQ
- Redis Queue
- Kafka

---

# 24.7 Pagination Strategy

All list endpoints must support pagination.

Supported Parameters

- page
- page_size
- sort_by
- sort_order
- filters

Business Rules

- Default page size configurable.
- Maximum page size enforced.
- Cursor-based pagination may be introduced for very large datasets.

---

# 24.8 Database Maintenance

Routine maintenance includes:

- VACUUM
- ANALYZE
- REINDEX (when required)
- Statistics Updates
- Partition Maintenance

Maintenance schedules should minimize operational impact.

---

# 24.9 Materialized Views

Materialized views may be used for expensive reporting queries.

Examples

- Daily Attendance Summary
- Monthly Workforce Statistics
- Site Occupancy Trends
- Compliance Overview
- Safety Dashboard

Business Rules

- Refresh schedules configurable.
- Critical dashboards use fresh operational data where required.

---

# 24.10 Read and Write Scaling

Future scaling options include:

- Read Replicas
- Dedicated Reporting Database
- Database Sharding (if required)
- Multi-region Replication

Operational transactions always use the primary database.

---

# 24.11 Monitoring & Observability

Performance metrics include:

- Query Execution Time
- API Response Time
- Database CPU Usage
- Memory Usage
- Disk Utilization
- Connection Pool Usage
- Lock Wait Time
- Slow Query Log
- Cache Hit Ratio

Alerts should be generated for threshold violations.

---

# 24.12 Capacity Planning

Capacity planning should monitor:

- Workforce Growth
- Attendance Volume
- Asset Growth
- Audit Log Growth
- Document Storage
- Notification Volume
- API Traffic

Growth forecasts should be reviewed periodically.

---

# 24.13 Future Optimization

Future enhancements may include:

- Query Plan Automation
- AI Query Optimization
- Distributed PostgreSQL
- Columnar Analytics Database
- Real-Time Stream Processing
- Automatic Index Recommendations
- Intelligent Cache Management

---

# 25. Backup & Disaster Recovery

The Backup & Disaster Recovery Strategy ensures that ConstructPulse can recover quickly from hardware failures, software defects, accidental data loss, cybersecurity incidents, and cloud infrastructure failures while minimizing operational disruption.

Construction operations rely heavily on real-time workforce visibility and attendance records. Therefore, data availability and recoverability are considered business-critical requirements.

The platform shall implement automated backup, disaster recovery, integrity verification, and business continuity procedures.

---

# 25.1 Objectives

The Backup Strategy aims to:

- Prevent permanent data loss
- Support rapid recovery
- Protect critical operational data
- Maintain business continuity
- Meet organizational compliance requirements

---

# 25.2 Backup Types

ConstructPulse supports multiple backup types.

Full Backup

- Complete database snapshot.

Incremental Backup

- Stores only changes since the previous backup.

Differential Backup

- Stores changes since the last full backup.

Point-in-Time Recovery (PITR)

- Allows restoration to a specific timestamp.

---

# 25.3 Backup Schedule

Recommended Schedule

Daily

- Incremental Backup

Weekly

- Full Backup

Monthly

- Long-Term Archive

Backup schedules are configurable by administrators.

---

# 25.4 Backup Scope

The following data must be protected.

- Companies
- Projects
- Sites
- Workforce
- Attendance
- Compliance Records
- Incidents
- Hazards
- Assets
- Visitors
- Notifications
- Documents
- Audit Logs
- Configuration
- AI Workflow Rules

---

# 25.5 Storage Strategy

Recommended Storage

Primary

- Production Database

Secondary

- Encrypted Backup Storage

Future

- AWS S3
- Azure Blob Storage
- Google Cloud Storage

Backups should be geographically redundant.

---

# 25.6 Backup Security

Backups must be:

- Encrypted
- Access Controlled
- Integrity Verified
- Versioned

Only authorized administrators may initiate restoration.

---

# 25.7 Disaster Recovery

Supported recovery scenarios

- Database Corruption
- Server Failure
- Cloud Failure
- Accidental Deletion
- Cybersecurity Incident
- Application Failure

Recovery procedures are documented and tested periodically.

---

# 25.8 Recovery Objectives

Recommended Targets

Recovery Time Objective (RTO)

Less than 2 hours

Recovery Point Objective (RPO)

Less than 15 minutes

These values may be adjusted according to organizational requirements.

---

# 25.9 Backup Verification

Every backup should be verified through:

- Checksum Validation
- Automated Restore Testing
- Integrity Verification
- Recovery Simulation

A backup is considered valid only after successful verification.

---

# 25.10 Business Continuity

During major outages, the platform should support:

- Read-only reporting (where possible)
- Emergency contact access
- Emergency muster information
- Recovery status dashboard

Critical emergency information should remain accessible even during recovery operations.

---

# 25.11 Disaster Recovery Testing

Recovery drills should be performed regularly.

Recommended Frequency

- Quarterly Restore Test
- Annual Disaster Recovery Simulation

Test results should be documented and reviewed.

---

# 25.12 Future Expansion

Future enhancements may include:

- Cross-Region Replication
- Multi-Cloud Disaster Recovery
- Automatic Failover
- Active-Active Database Clusters
- Continuous Backup Validation
- AI-Assisted Recovery Planning

---

# 26. Database Migration Strategy

The Database Migration Strategy defines how ConstructPulse evolves its database schema safely throughout the platform lifecycle while ensuring data integrity, zero unnecessary downtime, and backward compatibility.

As ConstructPulse grows from a single-company deployment into a multi-company enterprise platform, schema changes must be predictable, reversible, fully auditable, and automated through controlled migration processes.

All schema modifications shall be managed through version-controlled database migrations.

---

# 26.1 Migration Philosophy

ConstructPulse follows the principles:

- Migration First Development
- Version Controlled Database
- Backward Compatibility
- Reversible Changes
- Zero Data Loss
- Automated Deployment
- Continuous Validation

Database schema changes shall never be performed manually in production.

---

# 26.2 Migration Framework

Current Framework

- Alembic

Database

- PostgreSQL

ORM

- SQLAlchemy

Migration files shall be committed to source control together with application code.

---

# 26.3 Migration Lifecycle

Developer Creates Model

↓

Generate Migration

↓

Review Migration

↓

Automated Testing

↓

Staging Deployment

↓

Validation

↓

Production Deployment

↓

Post-Deployment Verification

---

# 26.4 Migration Categories

Supported migration types

Schema Migration

- New Tables
- New Columns
- Constraints
- Indexes

Data Migration

- Data Cleanup
- Data Transformation
- Default Values

Reference Data Migration

- Countries
- Roles
- Permissions
- Departments
- Trades
- Configuration

---

# 26.5 Version Control

Every migration receives:

- Sequential Revision ID
- Creation Timestamp
- Author
- Description

Migration history remains permanently stored.

---

# 26.6 Rollback Strategy

Every migration should include a rollback path.

Supported rollback scenarios

- Failed Deployment
- Data Validation Failure
- Application Compatibility Issue

Business Rules

- Rollbacks must preserve data whenever possible.
- Irreversible migrations require explicit approval.

---

# 26.7 Production Deployment

Recommended deployment workflow

Backup

↓

Run Migrations

↓

Verify Schema

↓

Run Health Checks

↓

Enable Application

↓

Monitor Logs

↓

Confirm Success

---

# 26.8 Seed Data

ConstructPulse maintains reference data through managed seed scripts.

Examples

Countries

Emergency Numbers

Roles

Permission Groups

Permissions

Trades

Departments

Shift Types

Employment Types

Default Configuration

Seed scripts remain idempotent.

---

# 26.9 Data Integrity Validation

Validation checks include:

- Foreign Keys
- Orphan Records
- Duplicate Records
- Null Constraints
- Unique Constraints
- Reference Consistency

Deployment fails if validation fails.

---

# 26.10 Environment Strategy

ConstructPulse supports:

Development

Testing

Staging

Production

Each environment maintains independent databases and migration histories.

---

# 26.11 Continuous Integration

Future CI/CD pipeline

Developer Push

↓

Automated Tests

↓

Migration Validation

↓

Schema Verification

↓

Deploy to Staging

↓

Approval

↓

Production Deployment

---

# 26.12 Migration Monitoring

Deployment monitoring includes:

- Migration Duration
- Failed Statements
- Lock Time
- Database Load
- Validation Results

Alerts generated for failed migrations.

---

# 26.13 Future Expansion

Future improvements include:

- Online Schema Changes
- Blue-Green Database Deployment
- Zero-Downtime Migrations
- Automated Drift Detection
- Schema Comparison Tools
- AI Migration Validation
- Multi-Region Migration Coordination

---

# 27. Database Roadmap & Future Expansion

The ConstructPulse database has been designed using a modular, scalable, and domain-driven architecture to support long-term growth without requiring major structural redesign.

Rather than optimizing solely for current business requirements, the database has been architected to accommodate future operational, analytical, and enterprise capabilities while preserving backward compatibility.

This roadmap outlines the planned evolution of the data platform across multiple implementation phases.

---

# 27.1 Design Goals

The long-term objectives of the ConstructPulse database are:

- Support unlimited projects and sites.
- Support multiple construction companies.
- Maintain complete tenant isolation.
- Scale horizontally as operational data grows.
- Enable AI-powered analytics.
- Support cloud-native deployment.
- Integrate with external enterprise systems.
- Minimize schema changes during future feature development.

---

# 27.2 Phase 1 — Workforce Operations

Primary Focus

- Authentication
- Workforce Management
- Projects
- Sites
- Attendance
- GPS Validation
- QR Attendance
- Worker Approvals
- Emergency Muster
- Dashboards
- Notifications

Outcome

A production-ready workforce management platform for construction companies.

---

# 27.3 Phase 2 — Safety & Compliance

Enhancements

- Digital Compliance Passport
- Toolbox Talks
- Daily Safety Briefings
- Hazard Register
- Incident Management
- Near Miss Reporting
- Corrective Actions
- PPE Management
- Safety Analytics

Outcome

A complete digital safety management platform integrated with workforce operations.

---

# 27.4 Phase 3 — Assets & Fleet

Enhancements

- Asset Management
- Fleet Management
- Equipment Maintenance
- Preventive Maintenance
- Equipment Inspections
- Asset QR Codes
- Asset Analytics
- Maintenance Scheduling

Outcome

Unified management of workforce and physical assets.

---

# 27.5 Phase 4 — Enterprise Operations

Enhancements

- Payroll Integration
- ERP Integration
- Procurement
- Cost Codes
- Vendor Management
- Budget Tracking
- Contract Management
- Financial Reporting

Outcome

Enterprise-wide operational visibility.

---

# 27.6 Phase 5 — Artificial Intelligence

AI Capabilities

- Workforce Forecasting
- Attendance Prediction
- Safety Risk Prediction
- Incident Prediction
- Equipment Failure Prediction
- Compliance Forecasting
- AI Report Generation
- Natural Language Search
- AI Operations Assistant

Outcome

Predictive construction operations powered by AI.

---

# 27.7 Phase 6 — Smart Construction

Future Technologies

- IoT Sensors
- Smart Helmets
- Wearable Devices
- RFID Tracking
- BLE Beacons
- Drone Integration
- Digital Twins
- BIM Integration
- Computer Vision
- Environmental Monitoring

Outcome

A connected smart construction ecosystem.

---

# 27.8 Scalability Strategy

The platform is designed to scale through:

- PostgreSQL Partitioning
- Read Replicas
- Distributed Caching
- Background Processing
- Event-Driven Architecture
- Microservice Readiness
- API Gateway
- Backend-for-Frontend (BFF)

The architecture supports gradual migration without disrupting existing functionality.

---

# 27.9 Multi-Country Expansion

ConstructPulse is designed to support international deployment.

Future localization includes:

- Country-specific regulations
- Emergency numbers
- Labour laws
- Languages
- Time zones
- Currencies
- Date formats
- Compliance requirements

The platform should support additional countries without requiring database redesign.

---

# 27.10 Data Growth Strategy

As operational data increases, ConstructPulse will implement:

- Table Partitioning
- Archive Policies
- Cold Storage
- Materialized Views
- Search Optimization
- Distributed Reporting
- Historical Data Warehousing

This ensures consistent performance as the platform scales.

---

# 27.11 Enterprise Integration Roadmap

Future integrations include:

- Microsoft Entra ID
- SAP
- Oracle ERP
- Microsoft Dynamics 365
- Xero
- MYOB
- Autodesk Construction Cloud
- Procore
- Microsoft Teams
- Slack
- Power BI
- Tableau
- Azure OpenAI
- OpenAI
- IoT Platforms

---

# 27.12 Platform Vision

ConstructPulse is envisioned as a comprehensive Construction Workforce Operating System (CWOS).

The platform will unify:

- Workforce Management
- Attendance
- Safety
- Compliance
- Emergency Management
- Assets & Fleet
- Visitors
- Communications
- Analytics
- Artificial Intelligence

into a single operational platform that improves workforce visibility, enhances safety, simplifies compliance, and enables data-driven decision making across construction projects.

---

# 27.13 Architectural Principles

The long-term architecture will continue to follow these principles:

- Domain-Driven Design (DDD)
- Event-Driven Architecture
- Configuration Over Customization
- API-First Development
- Cloud-Native Deployment
- Security by Design
- Privacy by Design
- Observability by Default
- AI-Ready Data Model
- Modular Expansion

These principles ensure that ConstructPulse remains maintainable, extensible, and adaptable as business requirements evolve.

---

# 27.14 Success Criteria

The database architecture will be considered successful when it can:

- Support multiple enterprise customers.
- Scale to hundreds of construction sites.
- Process millions of attendance records.
- Maintain high availability.
- Deliver low-latency operational dashboards.
- Integrate seamlessly with external enterprise systems.
- Enable advanced analytics and AI capabilities.
- Adapt to future business requirements with minimal schema changes.

---


