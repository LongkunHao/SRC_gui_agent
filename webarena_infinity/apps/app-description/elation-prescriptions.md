# Elation Health — Prescriptions

Elation Health is an electronic health record (EHR) platform for primary care. This environment covers the **Prescriptions** (e-prescribing) module.

## Components to Implement

### Active Medications List
- Table of patient's current medications: drug name, dosage, frequency, route, prescribing provider, start date, refills remaining, status (active, discontinued, on hold)
- Filter by status (active, all, discontinued)
- Search by medication name
- Sort by name, date, or status

### Prescribe New Medication
- Patient header (name, DOB, allergies displayed prominently)
- Drug search (searchable by brand or generic name)
- Drug selection with form/strength options (e.g., Amoxicillin 500mg capsule, 250mg/5mL suspension)
- Dosage, frequency, route, quantity, days supply fields
- Number of refills
- Directions / sig field (free text with common presets like "Take 1 tablet by mouth twice daily")
- DAW (Dispense As Written) toggle
- Pharmacy selection (searchable, with patient's preferred pharmacy pre-selected)
- Drug interaction and allergy alerts (warning banners)
- Prior authorization flag
- Prescribe (e-prescribe) or print/fax options

### Prescription Detail View
- Full prescription details with all fields
- Prescription history (original, renewals, modifications)
- Fill status from pharmacy (if available)
- Actions: renew, modify, discontinue, cancel

### Renewal / Refill Requests
- List of incoming refill requests from pharmacies
- Request details: medication, pharmacy, patient, original prescription
- Approve, deny, or modify-and-approve actions
- Deny reason selection (no longer needed, changed therapy, need appointment, etc.)

### Medication History
- Chronological list of all prescriptions (past and present) for a patient
- Filter by date range, medication, provider
- View discontinued medications with discontinuation reason

### Prescription Settings
- Default pharmacy preferences
- Prescriber DEA number and NPI configuration
- E-prescribe controlled substance (EPCS) enrollment status
- Prescription printing format preferences
- Formulary preference list / favorites

### Drug Interaction Checker
- Interaction check panel showing alerts when prescribing
- Severity levels (major, moderate, minor)
- Interaction details and clinical recommendations
- Override option with reason documentation
