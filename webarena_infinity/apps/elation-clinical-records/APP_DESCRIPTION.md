# Elation Clinical Records

## Summary

A clinical records management web application inspired by Elation EHR's documentation workflows. The app serves as an electronic health records (EHR) system for a family medicine practice ("Greenwood Family Medicine"), enabling providers to manage patient charts, document visit notes, record vaccinations/injectables, track vitals, manage problem lists, create care plans, and configure practice settings. The current logged-in provider is Dr. Sarah Chen, MD, FAAFP.

## Main Sections/Pages

### 1. Patients (default view)
- **Patient List**: Searchable table of 12 patients with name, DOB, age, sex, phone, provider, and tags
- **Patient Chart**: Opens when a patient is selected, with 5 tabs:
  - **Clinical Profile**: Problem list (grouped by Active/Controlled/Resolved), recent vaccinations, latest vitals, demographics
  - **Visit Notes**: Chronological list of visit notes with search, create new notes
  - **Vaccinations**: Table of all vaccines and injectables with full CDC-style fields
  - **Vitals**: Tabular history of all vitals with ability to add historical vitals
  - **Care Plans**: List of care plan snapshots from visit notes

### 2. Templates
- Grid of 10 visit note templates (6 pre-built "E*" templates + custom templates)
- Create, edit, duplicate, and delete templates
- Each template has: name, content sections (HPI, ROS, PE, Assessment), CPT codes, POS, billing notes, document tags

### 3. Categories
- List of 10 visit note categories with MIPS toggle
- First category is default (marked with star)
- Create, edit, remove categories
- Admin-only access (current user is admin)

### 4. Settings
- **Provider Preferences**: Coded assessments toggle, show Dx codes in print toggle, default note format dropdown
- **Appointment Types & Visit Note Automation**: Table of 10 appointment types with configurable note format, category, and template associations
- **Practice Information**: Read-only display of practice name, address, phone, fax

## Complete List of Implemented Features

### Patient Management
- Patient list with search by name, DOB, phone, insurance
- Patient chart view with tabbed interface
- Patient tags (add, remove) with * prefix for priority pinning
- Patient demographics display (legal name, DOB, sex, gender, email, phone, address, insurance, mother's maiden name, Passport status)

### Problem List Management
- Add new problems with ICD-10 code search (50+ codes in database)
- Edit existing problems (title, ICD-10, onset date, status, synopsis)
- Change problem status: Active, Controlled, Resolved
- Status-specific visual styling (red border = Active, green = Controlled, gray = Resolved)
- "Save & Add Another" workflow
- Export problem to note (assessment)
- ICD-10 database search with autocomplete

### Vaccination/Injectable Documentation
- Add vaccination with full vaccine form (record type, vaccine name search, manufacturer, lot #, NDC, expiration, dose, series, method, site, given on, VIS date, ordered by, given by, recall, program, funded by, reason, notes)
- Record types: New, Historical, Declined
- Vaccine name search/autocomplete from 35+ vaccine options
- 12 manufacturer options, 7 administration methods, 14 administration sites
- 13 recall period options, 3 program (VFC) options, 7 funding options
- Injectable (non-vaccine) documentation with "not send to registry" flag
- "Save & Add Another" workflow

### Visit Note Management
- Create new visit notes with format, category, and template selection
- 5 visit note formats: Complete H&P (2-Column), H&P (Single Column), Pre-Op H&P, Simple Note, Non-Visit Note
- Template auto-population: blocks, billing items, document tags
- Draft editing with block management (add, remove, edit content)
- Block types: 21 standard blocks + 3 multi-add blocks (Lab Order, Imaging Order, Prescription)
- Sign visit note (changes status from draft to signed with timestamp)
- Billing items display and management (CPT codes)
- Document tags display
- Note search by reason, category, tags, and content

### Vitals Management
- Add historical vitals (for home BP readings, etc.)
- Fields: BP systolic/diastolic, heart rate, respiratory rate, temperature (F/C), SpO2, weight (lbs/kg), height (in/cm), BMI (auto-calculated), pain level
- "Save & Add Another" workflow
- Tabular display with full history

### Care Plans
- View care plans created from visit note Care Plan sections
- Display: date, provider, status, diagnoses (ICD codes), content
- Export care plan to new visit note

### Visit Note Templates
- Create new templates with content sections (HPI, ROS, PE, Assessment)
- Edit existing templates
- Duplicate templates
- Delete templates with confirmation
- Associate CPT codes, POS, billing notes, document tags

### Visit Note Categories
- Add new categories with MIPS toggle
- Edit category name and MIPS setting
- Remove categories (with confirmation that existing notes retain the category)
- MIPS toggle on each category in the list view
- First-in-list is default category (star indicator)

### Provider Settings
- Coded Visit Note Assessments toggle (enable/disable ICD-10 search in assessment fields)
- Show Dx Codes in Print toggle
- Default Visit Note Format dropdown (5 format options)

### Appointment Type Automation
- Edit appointment type associations: note format, category, template
- 10 appointment types with color indicators, duration, and current associations

## Data Model

### Entities and Fields

#### Provider
- id, fullName, credentials, email, npi, specialty, practiceId, practiceName, practiceAddress, practicePhone, practiceFax, defaultNoteFormat, defaultCategory, role, isAdmin

#### Patient (12 records)
- id, firstName, lastName, legalFirstName, legalLastName, dateOfBirth, sexAtBirth, gender, email, phone, address, mothersMaidenName, insurancePrimary, insuranceId, primaryProvider, tags[], passportActive, createdAt

#### Problem (31 records across 8 patients)
- id, patientId, title, icd10, icd9, snomed, dxDate, status (Active/Controlled/Resolved), synopsis, resolvedDate, sortOrder

#### Vaccination (18 records)
- id, patientId, vaccineName, cvx, ndc, manufacturer, lotNumber, expirationDate, doseAmount, doseUnits, seriesNumber, method, site, givenOn, orderedBy, givenBy, recordType (New/Historical/Declined), visDate, recall, reason, notes, program, fundedBy, source, status, isInjectable, notSendToRegistry

#### Vitals (14 records)
- id, patientId, noteId, date, bloodPressureSystolic, bloodPressureDiastolic, heartRate, respiratoryRate, temperature, temperatureUnit, oxygenSaturation, weight, weightUnit, height, heightUnit, bmi, painLevel

#### Visit Note (13 records, 12 signed + 1 draft)
- id, patientId, providerId, format, category, templateUsed, date, status (draft/signed), signedAt, reason, blocks[], billingItems[], documentTags[]

#### Visit Note Block
- type (21 standard types + 3 multi-add), content, diagnoses[] (for assessment blocks)

#### Care Plan (3 records)
- id, patientId, noteId, providerId, date, content, diagnoses[], status

#### Visit Note Category (10 records)
- id, name, countForMIPS, isDefault, sortOrder

#### Visit Note Template (10 records)
- id, name, createdBy, content{}, billingItems[], pos, billingNotes, documentTags[], createdAt

#### Appointment Type (10 records)
- id, name, duration, noteFormat, noteCategory, noteTemplate, color

#### Provider Preferences
- codedAssessments, showDxCodesInPrint, defaultNoteFormat

### Relationships
- Patient → Problems (one-to-many)
- Patient → Vaccinations (one-to-many)
- Patient → Vitals (one-to-many)
- Patient → Visit Notes (one-to-many)
- Patient → Care Plans (one-to-many)
- Visit Note → Provider (many-to-one)
- Visit Note → Category (many-to-one)
- Visit Note → Template (many-to-one, optional)
- Visit Note → Blocks (one-to-many, embedded)
- Care Plan → Visit Note (many-to-one)
- Appointment Type → Category (many-to-one)
- Appointment Type → Template (many-to-one, optional)
- Appointment Type → Format (many-to-one)
- Vaccination → Provider (orderedBy, givenBy)

## Navigation Structure

```
Sidebar Navigation:
├── Patients (default) → Patient List
│   └── Click patient row → Patient Chart
│       ├── Clinical Profile tab (default)
│       ├── Visit Notes tab
│       ├── Vaccinations tab
│       ├── Vitals tab
│       └── Care Plans tab
├── Templates → Template grid view
├── Categories → Category list view
└── Settings → Provider preferences, appointment types, practice info
```

URL hash routing: `#/patients`, `#/patients/{patientId}`, `#/templates`, `#/categories`, `#/settings`

## Available Form Controls

### Dropdowns (custom, not native <select>)
- Visit Note Format: Complete H&P Note (2-Column), H&P Note (Single Column), Pre-Op H&P Note, Simple Note, Non-Visit Note
- Visit Note Category: Office Visit, Telehealth, Annual Exam, Procedure, Follow-Up, Care Plan Review, Urgent Visit, Vaccination Only, Pre-Op Evaluation, Workers Comp
- Visit Note Template: None + all 10 templates
- Problem Status: Active, Controlled, Resolved
- Vaccine Name: 35+ options (with search)
- Vaccine Manufacturer: 12 options (Pfizer, Moderna, Janssen/J&J, Sanofi Pasteur, Merck, GlaxoSmithKline, Seqirus, AstraZeneca, Novavax, Watson Labs, Other, Unknown)
- Administration Method: Intramuscular, Subcutaneous, Intradermal, Oral, Intranasal, Intra-articular, Intravenous
- Administration Site: 14 options (Left/Right Deltoid, Thigh, Upper Arm, Gluteal, Knee, Shoulder, Oral, Intranasal)
- Dose Units: mL, mg, mcg, units
- Record Type: New, Historical, Declined
- Recall: 13 options (empty through "16 years booster")
- Program: Not VFC Eligible, VFC Eligible, Not Applicable
- Funded By: Private, Medicare, Medicaid, VFC, Self-Pay, Insurance, Other
- Ordered By: All 7 providers
- Temperature Unit: F, C
- Weight Unit: lbs, kg
- Height Unit: in, cm
- Appointment Type Note Format/Category/Template

### Toggles
- Count for MIPS (per category)
- Coded Visit Note Assessments (provider preference)
- Show Dx Codes in Print (provider preference)

### Text Inputs
- Patient search, note search, problem search (ICD-10), vaccine name search
- Problem: title, ICD-10 code, onset date, synopsis
- Vaccination: lot #, NDC, expiration, dose amount, series #, given on, VIS date, given by, reason, notes
- Vitals: systolic BP, diastolic BP, heart rate, respiratory rate, temperature, SpO2, pain level, weight, height
- Visit Note: reason, date
- Template: name, HPI, ROS, PE, assessment, CPT code, CPT description, POS, billing notes, document tags
- Category: name
- Tag: name

### Buttons
- Primary (blue), Secondary (outlined), Ghost (transparent), Danger (red text), Link
- "Save & Add Another" pattern for problems, vaccinations, vitals
- Sign Visit Note, Save Draft

## Seed Data Summary

### Patients (12)
- Robert Henderson (67, M) - Medicare, complex diabetic with 6 problems
- Emily Nakamura (40, F) - Blue Cross, anxiety + anemia
- Marcus Johnson (53, M) - Aetna, uncontrolled hypertension, smoker
- Sofia Rodriguez-Martinez (31, F) - UHC, moderate asthma
- William O'Brien (77, M) - Medicare Advantage, CHF, AFib, CKD, falls
- Priya Sharma (35, F) - Cigna, pediatric parent
- Thomas Bergstrom (60, M) - Premera, COPD + DM + depression
- Aaliyah Washington (10, F) - Molina Medicaid, pediatric, immunizations
- David Kowalski (47, M) - Kaiser, anxiety + back pain
- Helen Zhao (72, F) - Medicare, osteoporosis + hypothyroid + GERD
- James Fitzgerald (37, M) - Regence, healthy
- Mei-Ling Wu (17, F) - Premera, pediatric, sports

### Problems (31 across 8 patients)
- Mix of Active (22), Controlled (6), Resolved (3)
- Diagnoses include: diabetes, hypertension, hyperlipidemia, obesity, BPH, anxiety, anemia, migraine, asthma, COPD, CHF, AFib, CKD, osteoarthritis, osteoporosis, hypothyroidism, GERD, back pain, depression, insomnia, prediabetes, tobacco use

### Vaccinations (18)
- COVID-19 (Pfizer, Moderna) - doses 1 & 2
- Influenza, Pneumococcal, Shingrix, Tdap, DTaP, IPV, MMR, Varicella, HPV, Meningococcal
- 2 injectables (Depo-Medrol knee injection, B12 injection)
- 1 declined vaccine (influenza by Marcus Johnson)
- 2 historical records (Sofia's pharmacy COVID vaccines)

### Visit Notes (13)
- 12 signed notes + 1 draft
- Categories used: Office Visit, Annual Exam, Follow-Up, Urgent Visit
- Templates used: Annual Wellness, Hypertension, Well Child
- 1 non-visit note for historical home BP readings

### Vitals (14 records)
- Multiple readings per patient for trending
- Historical home BP readings for Robert Henderson
- Pediatric vitals for Aaliyah Washington

### Care Plans (3)
- Robert Henderson: diabetes/hypertension management
- William O'Brien: cardiac care
- Marcus Johnson: hypertension urgency

### Templates (10)
- E* Annual Wellness Visit, E* Problem-Focused Visit
- Telehealth Follow-Up, Flu Shot Administration, COVID-19 Vaccine Visit
- Diabetes Management, Hypertension Follow-Up, Well Child Visit
- Injectable Administration, Pre-Operative Evaluation

### Categories (10)
- Office Visit (default), Telehealth, Annual Exam, Procedure, Follow-Up, Care Plan Review, Urgent Visit, Vaccination Only, Pre-Op Evaluation, Workers Comp

### Appointment Types (10)
- Office Visit, Annual Exam, Telehealth Visit, Flu Shot, COVID Vaccine, Follow-Up, Procedure, Urgent Same-Day, Well Child Check, Pre-Op Clearance

### Providers (7)
- Dr. Sarah Chen (MD, Family Medicine, Admin - logged in)
- Dr. Michael Torres (MD, Internal Medicine)
- Dr. Aisha Patel (DO, Pediatrics)
- Rachel Kim (PA-C), James Okonkwo (NP), Maria Santos (RN), Lisa Chang (MA, Admin)
