# Elation Health — Clinical Records

Elation Health is an electronic health record (EHR) platform for primary care. This environment covers the **Clinical Records** module — the core patient chart and documentation system.

## Components to Implement

### Patient Chart Overview
- Patient header: name, DOB, age, sex, MRN, allergies, primary provider
- Summary dashboard with key clinical data at a glance
- Navigation tabs/sections for different chart areas

### Problems List
- Active and resolved problems/diagnoses
- Each entry: diagnosis name, ICD-10 code, date onset, status (active/resolved), notes
- Add/edit/remove problems
- Search diagnoses by name or ICD code
- Mark as resolved with resolution date

### Allergies
- List of documented allergies: allergen, reaction type (rash, anaphylaxis, GI upset, etc.), severity (mild, moderate, severe), status (active/inactive)
- Add/edit/remove allergies
- NKDA (No Known Drug Allergies) toggle

### Vital Signs
- Table/chart of vital sign entries: date, blood pressure, heart rate, temperature, respiratory rate, SpO2, height, weight, BMI
- Add new vitals entry form
- Trend charts for individual vitals over time

### Visit Notes / Encounters
- List of clinical encounters with date, visit type (office visit, telehealth, phone), provider, chief complaint
- Create new encounter note
- Note editor with sections: chief complaint, HPI (history of present illness), review of systems, physical exam, assessment & plan
- Note status: in-progress, signed, addendum
- Sign/lock note functionality

### Lab Results
- List of lab orders and results: test name, date ordered, date resulted, ordering provider, status (ordered, pending, resulted)
- Result detail view with values, reference ranges, abnormal flags
- Trend view for recurring labs (e.g., A1C over time, lipid panels)

### Immunization Records
- Table of immunizations: vaccine name, date administered, lot number, site, administering provider
- Add new immunization record
- Immunization schedule comparison (due/overdue indicators)

### Documents / Attachments
- Uploaded clinical documents (referral letters, outside records, imaging reports)
- Document metadata: name, type, date, source
- Upload and categorize documents

### Family History
- List of family members with conditions (e.g., Father — Type 2 Diabetes, Mother — Breast Cancer)
- Add/edit/remove entries
- Relationship, condition, age of onset fields

### Social History
- Smoking status (current, former, never) with details
- Alcohol use
- Drug use
- Occupation, exercise habits, diet notes
- Editable form fields
