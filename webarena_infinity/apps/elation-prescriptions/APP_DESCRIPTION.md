# Elation Prescriptions - App Description

## Summary

This app implements a comprehensive prescription management module from the Elation EHR system, focused on a patient chart view for **James Rodriguez** (47y/M). The app enables providers to prescribe medications, manage active/discontinued medication lists, process pharmacy refill and change requests, reconcile medications, and configure prescription settings. The logged-in provider is **Dr. Sarah Mitchell, MD** (Family Medicine).

## Main Sections / Pages

### 1. Chart View (default, `#/chart`)
- **Clinical Profile Sidebar** (left): Patient demographics, allergies, problem list, insurance details, preferred pharmacy
- **Main Content**: Permanent Rx Meds list, Permanent OTC Meds list, Temporary Medications list
- Each medication shows: name, sig, qty, unit, refills remaining, days supply, pharmacy, last filled date
- Actions dropdown per medication: Refill, Discontinue, Set as Temporary/Permanent, View Details

### 2. Medication History (`#/med-history`)
- Full medication history with search and filter controls
- Filter dropdown: All Medications, Permanent Rx, Permanent OTC, Temporary, Discontinued, Canceled Scripts
- Grouped by classification with counts
- Each entry shows medication name, status badge, sig, prescriber, start date, and discontinuation info if applicable
- Shortcuts: Reconcile, Bulk Refill

### 3. Rx Requests (`#/rx-requests`)
- **Requiring Action** section: Pending refill requests and change requests
- **Recently Processed** section: Approved/denied requests with history
- Refill request actions: Approve, Approve with Modifications (opens modal for sig/refill edits), Deny (opens modal for reason)
- Change request actions: Approve, Deny & Add Reason

### 4. Settings (`#/settings`)
- **Rx Templates** tab: List of saved prescription templates with Add, Edit, Delete actions
- **Custom Rx Sigs** tab: Custom sig shortcuts grouped by category (oral, prn, topical, etc.) with Add, Edit, Delete
- **Drug Decision Support** tab: Drug-to-Drug alert level dropdown (All / Major & Moderate / Major only), Drug-to-Allergy toggle
- **Preferences** tab: Default pharmacy dropdown, auto-populate last pharmacy toggle, show cost estimates toggle, show formulary data toggle

## Implemented Features and UI Interactions

### Prescription Form (modal)
- Triggered by "Prescribe" button in nav bar or "Refill" action on a medication
- **Medication search**: Auto-complete search across 95 medications (277 strength combinations); Rx Templates appear first with "Rx Template" label; controlled substances marked with schedule badge
- **Sig input**: Free text with "Saved Sigs" button that opens dropdown of 24 custom sigs
- **Qty, Unit, Refills, Days Supply** fields in a row
- **Unit dropdown**: 18 unit options (tablets, capsules, mL, grams, etc.)
- **Classification radio**: Permanent / Temporary
- **Dispense as Written checkbox**
- **Diagnosis search**: ICD-10 code search (24 codes), up to 2 diagnoses selectable with tag display
- **Pharmacy search**: Search across 15 pharmacies by name, city, zip, phone; EPCS-certified pharmacies labeled
- **Instructions to Pharmacy** textarea
- **Do Not Fill Before** date picker
- **Drug interaction alerts**: Displays drug-to-drug and drug-to-allergy alerts based on current settings
- **Coverage/Formulary panel** (right sidebar): Shows formulary status (Preferred/On Formulary/Non-Formulary/Non-Reimbursable), tier, copay, prior auth requirements, alternatives
- **Footer buttons**: Discard, Save as Rx Template, Prescribe (disabled until required fields filled)
- When refilling: form pre-populates from the existing medication's data

### Document Medication Form (modal)
- Triggered by "Document Med" button in nav bar
- Medication type radio: Rx / OTC
- Medication search field
- Start date picker
- Sig text input
- Saves to appropriate medication list

### Discontinue Medication (modal)
- Triggered by "Discontinue" action on any active medication
- Reason dropdown: 3 standard options (provider discontinue, another prescriber, patient stopped)
- Discontinued By field (pre-populated with current provider)
- Additional Details textarea
- Send cancellation request checkbox (shown only if pharmacy accepts e-cancellations)
- Moves medication from active list to discontinued list; optionally creates canceled script entry

### Medication Reconciliation (modal)
- Triggered by "Reconcile Meds" button
- Table showing all active medications with: name, sig, last filled date
- Adherence note text input per medication
- "Doc D/C" checkbox per medication to mark for discontinuation
- Complete Med Rec button (processes discontinuations, updates last reconciled date)
- Complete Without Changes button

### Bulk Refill (modal)
- Triggered by "Bulk Refill" button
- Table of all active permanent Rx meds with: select checkbox, medication, sig, qty, refills left, pharmacy
- Select All checkbox
- Refill Selected button creates new prescriptions for all checked medications

### Allergy Management
- Add allergy button in clinical profile: modal with allergen, reaction, severity, type fields
- Remove allergy button (X) next to each allergy
- Allergies trigger drug-to-allergy alerts in prescription form

### View Medication Details (modal)
- Shows all medication fields: name, status, sig, qty, unit, refills, days supply, NDC, classification, DAW, prescriber, pharmacy, dates, diagnosis, controlled substance info, discontinuation details

## Data Model

### Entities and Fields

#### CurrentUser (Provider)
- id, name, credentials, npi, specialty, email, epcsEnabled, deaNumber, practice, avatarColor

#### CurrentPatient
- id, firstName, lastName, dob, age, sex, weightKg, heightCm, address, phone, mobile, email
- preferredPharmacyId, secondaryPharmacyId
- insurance: { planName, memberId, groupNumber, bin, pcn, pbm, copayGeneric, copayPreferred, copayNonPreferred, deductible, deductibleMet }
- allergies: [{ id, allergen, reaction, severity, type, onsetDate, source }]
- problems: [{ id, description, icd10, status, onsetDate }]
- lastReconciledDate

#### Medications (permanentRxMeds, permanentOtcMeds, temporaryMeds)
- id, medicationName, ndc, sig, qty, unit, refills, refillsRemaining, daysSupply, dispenseAsWritten
- status (active), classification (permanent_rx/permanent_otc/temporary)
- prescriberId, prescriberName, pharmacyId, pharmacyName
- startDate, lastPrescribedDate, lastFilledDate, nextRefillDate
- diagnosis: [{ code, description }]
- isControlled, scheduleClass

#### DiscontinuedMeds
- Same fields as Medications plus: discontinuedDate, discontinuedBy, discontinueReason, discontinueDetails

#### CanceledScripts
- id, medicationName, ndc, sig, qty, refills, daysSupply, status, classification
- prescriberId, prescriberName, pharmacyId, pharmacyName
- prescribedDate, canceledDate, cancelReason, diagnosis

#### Pharmacies
- id, name, address, city, state, zip, phone, fax, storeNumber, epcs, acceptsECancel, type (retail/mail_order/hospital/independent)

#### RefillRequests
- id, type (refill), status (pending/approved/denied), medicationName, ndc, patientMedId
- pharmacyId, pharmacyName, requestDate
- lastPrescription: { sig, qty, refills, prescribedDate }
- lastDispensed: { date, qty }
- notes, processedDate, processedBy, denyReason, modifications

#### ChangeRequests
- id, type (change), status, medicationName, originalMedication, requestedMedication
- pharmacyId, pharmacyName, requestDate, reason, notes, processedDate, processedBy, denyReason

#### RxTemplates
- id, medicationName, sig, qty, unit, refills, daysSupply, ndc, createdDate

#### CustomSigs
- id, text, category (oral/prn/topical/ophthalmic/inhalation/injectable/sublingual)

#### MedicationDatabase (95 entries, 277 strength combos)
- id, name, strengths[], form, type (Rx/OTC), drugClass, generic, controlled, schedule

#### DrugInteractions
- id, drug1, drug2, severity (major/moderate/minor), description, recommendation

#### FormularyData (keyed by medication name)
- status (preferred/on_formulary/non_formulary/non_reimbursable), tier, copay, requiresPA, alternatives[]

#### Settings
- drugDecisionSupport: { drugToDrugLevel (all/major_moderate/major_only), drugToAllergyEnabled }
- defaultPharmacyId, autoPopulateLastPharmacy, prescriptionPrintFormat, showCostEstimates, showFormularyData, epcsTokenType

#### Providers
- id, name, credentials, specialty, npi

#### DiagnosisCodes
- code (ICD-10), description

### Relationships
- Patient.preferredPharmacyId → Pharmacies.id
- Medications.pharmacyId → Pharmacies.id
- Medications.prescriberId → Providers.id
- RefillRequests.pharmacyId → Pharmacies.id
- RefillRequests.patientMedId → Medications.id
- ChangeRequests.pharmacyId → Pharmacies.id
- DrugInteractions reference MedicationDatabase by drug name
- FormularyData keyed by medicationName matching Medications.medicationName

## Navigation Structure

| Route | View | How to Reach |
|-------|------|-------------|
| `#/chart` | Patient Chart (default) | Click "Chart" in nav bar |
| `#/med-history` | Medication History | Click "Meds Hx" in nav bar |
| `#/rx-requests` | Rx Requests | Click "Rx Requests" in nav bar |
| `#/settings` | Settings | Click "Settings" in nav bar |
| `#/settings/templates` | Rx Templates tab | Click "Rx Templates" tab in Settings |
| `#/settings/sigs` | Custom Sigs tab | Click "Custom Rx Sigs" tab in Settings |
| `#/settings/drug-support` | Drug Decision Support tab | Click "Drug Decision Support" tab |
| `#/settings/preferences` | Preferences tab | Click "Preferences" tab |

Modals are triggered by buttons and close with X button or Escape key.

## Available Form Controls, Dropdowns, Toggles, and Their Options

### Dropdowns
- **medHistoryFilter**: All Medications, Permanent Rx, Permanent OTC, Temporary, Discontinued, Canceled Scripts
- **rxUnit**: tablets, capsules, mL, grams, each, patches, puffs, drops, suppositories, packets, vials, pens, inhalers, tubes, bottles, softgels, lozenges, sprays
- **drugToDrugLevel**: All alerts (Minor, Moderate, Major) / Major and Moderate only / Major only
- **defaultPharmacy**: All 15 pharmacies
- **discReason**: "I want to discontinue this medication" / "Discontinued by another prescriber" / "Patient stopped taking medication"
- **Medication search**: 95 medications with 277 strength/form combinations
- **Pharmacy search**: 15 pharmacies (searchable by name, city, zip, phone, store number)
- **Diagnosis search**: 24 ICD-10 codes (searchable by code or description)

### Toggles
- **drugToAllergyEnabled**: Drug-to-Allergy Alerts on/off (default: on)
- **autoPopulateLastPharmacy**: Auto-populate Last Used Pharmacy on/off (default: on)
- **showCostEstimates**: Show Cost Estimates on/off (default: on)
- **showFormularyData**: Show Formulary Information on/off (default: on)

### Checkboxes
- **rxDAW**: Dispense as Written (in prescription form)
- **discSendCancel**: Send cancellation request to pharmacy (in discontinue modal)
- **Reconcile D/C checkboxes**: One per medication in reconciliation table
- **Bulk refill checkboxes**: One per medication + Select All

### Radio Buttons
- **rxClassification**: Permanent / Temporary (in prescription form)
- **docMedType**: Rx / OTC (in document med form)

### Text Inputs
- Medication search (autocomplete)
- Sig (free text + saved sigs list)
- Qty (number), Refills (number), Days Supply (number)
- Pharmacy search (autocomplete)
- Diagnosis search (autocomplete)
- Instructions to Pharmacy (textarea)
- Do Not Fill Before (date)
- Adherence notes (in reconciliation)
- Discontinued By, Additional Details (in discontinue modal)
- Denial reason (textarea, in deny modal)
- Template fields: Medication Name, Sig, Qty, Unit, Refills, Days Supply
- Custom sig text
- Allergy fields: Allergen, Reaction, Severity (select), Type (select)

## Seed Data Summary

### Patient: James Rodriguez
- 47y/M, 82.5kg, San Francisco, CA
- Insurance: Blue Shield PPO Gold, Express Scripts PBM
- 4 allergies: Penicillin (Moderate), Sulfonamides (Severe), Codeine (Mild), Latex (Mild)
- 8 active problems: hypertension, type 2 diabetes, hyperlipidemia, GERD, anxiety, chronic low back pain, vitamin D deficiency, obesity

### Active Medications
- **11 Permanent Rx Meds**: Lisinopril 10mg, Metformin 500mg, Atorvastatin 20mg, Omeprazole 20mg, Sertraline 50mg, Amlodipine 5mg, Gabapentin 300mg, Metoprolol Succinate ER 50mg, Losartan 50mg, Alprazolam 0.5mg (C-IV), Montelukast 10mg
- **6 Permanent OTC Meds**: Vitamin D3 2000 IU, Fish Oil 1000mg, Calcium 600mg+D3, Centrum Silver, Melatonin 3mg, Aspirin 81mg
- **3 Temporary Meds**: Amoxicillin 500mg, Prednisone 10mg (taper), Ciprofloxacin 500mg

### Discontinued Medications (6)
Hydrochlorothiazide 25mg, Citalopram 20mg, Pantoprazole 40mg, Naproxen 500mg, Glipizide 5mg, Tramadol 50mg

### Canceled Scripts (2)
Azithromycin 250mg, Lisinopril 20mg

### Pharmacies (15)
CVS #4521 (preferred, EPCS), CVS #4533 (EPCS), Walgreens #7892 (EPCS), Walgreens #7901, Rite Aid #3456 (EPCS), Costco #1142, Target/CVS #5678 (EPCS), Safeway #2891, Alto Pharmacy (EPCS, mail order), Amazon Pharmacy (mail order), Express Scripts (mail order), UCSF Medical Center (EPCS, hospital), Kaiser #4102 (EPCS, hospital), Good Neighbor Marina (independent), Jade Pharmacy (independent)

### Pending Refill Requests (6 pending)
Lisinopril 10mg, Atorvastatin 20mg, Gabapentin 300mg (urgent), Omeprazole 20mg, Sertraline 50mg, Metoprolol Succinate ER 50mg

### Processed Requests (2)
Metformin 500mg (approved), Tramadol 50mg (denied - discontinued)

### Change Requests (2 pending)
Atorvastatin→Rosuvastatin substitution, Gabapentin sig clarification

### Rx Templates (12)
Lisinopril 10mg, Lisinopril 20mg, Metformin 500mg, Metformin 1000mg, Atorvastatin 20mg, Atorvastatin 40mg, Omeprazole 20mg, Amoxicillin 500mg, Azithromycin Z-Pack, Prednisone taper, Sertraline 50mg, Amlodipine 5mg

### Custom Sigs (24)
Organized by category: oral (12), prn (4), topical (2), ophthalmic (1), inhalation (2), injectable (1), sublingual (1), oral-special (1)

### Drug Interactions (15)
6 major (Lisinopril+Losartan, Sertraline+Tramadol, Metformin+Contrast, Warfarin+Aspirin, Atorvastatin+Gemfibrozil), 6 moderate, 3 minor

### Formulary Data (15 entries)
Covers key medications with status, tier, copay, PA requirements, and alternatives

### Providers (7)
Dr. Sarah Mitchell (Family Med), Dr. Michael Chen (Internal Med), Dr. Lisa Park (Urgent Care), Dr. Robert Kim (Cardiology), Dr. Emily Watson (Endocrinology), Maria Santos NP, David Thompson PA-C
