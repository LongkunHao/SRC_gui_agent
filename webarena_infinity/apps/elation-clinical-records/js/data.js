/* ============================================================
   data.js — Seed data for Elation Clinical Records
   ============================================================ */

const SEED_DATA_VERSION = 1;

// ── Current Provider (logged-in user) ──
const CURRENT_PROVIDER = {
    id: 'prov_001',
    fullName: 'Dr. Sarah Chen',
    credentials: 'MD, FAAFP',
    email: 'sarah.chen@greenwoodmedical.com',
    npi: '1234567890',
    specialty: 'Family Medicine',
    practiceId: 'prac_001',
    practiceName: 'Greenwood Family Medicine',
    practiceAddress: '2847 Greenwood Ave, Suite 300, Seattle, WA 98103',
    practicePhone: '(206) 555-0142',
    practiceFax: '(206) 555-0143',
    defaultNoteFormat: 'complete_hp',
    defaultCategory: 'cat_001',
    role: 'physician',
    isAdmin: true
};

// ── Other Providers in Practice ──
const PROVIDERS = [
    CURRENT_PROVIDER,
    { id: 'prov_002', fullName: 'Dr. Michael Torres', credentials: 'MD', email: 'michael.torres@greenwoodmedical.com', npi: '2345678901', specialty: 'Internal Medicine', role: 'physician', isAdmin: false },
    { id: 'prov_003', fullName: 'Dr. Aisha Patel', credentials: 'DO', email: 'aisha.patel@greenwoodmedical.com', npi: '3456789012', specialty: 'Pediatrics', role: 'physician', isAdmin: false },
    { id: 'prov_004', fullName: 'Rachel Kim', credentials: 'PA-C', email: 'rachel.kim@greenwoodmedical.com', npi: '4567890123', specialty: 'Family Medicine', role: 'pa', isAdmin: false },
    { id: 'prov_005', fullName: 'James Okonkwo', credentials: 'NP', email: 'james.okonkwo@greenwoodmedical.com', npi: '5678901234', specialty: 'Family Medicine', role: 'np', isAdmin: false },
    { id: 'prov_006', fullName: 'Maria Santos', credentials: 'RN', email: 'maria.santos@greenwoodmedical.com', npi: '', specialty: '', role: 'nurse', isAdmin: false },
    { id: 'prov_007', fullName: 'Lisa Chang', credentials: 'MA', email: 'lisa.chang@greenwoodmedical.com', npi: '', specialty: '', role: 'ma', isAdmin: true }
];

// ── Patients ──
const PATIENTS = [
    {
        id: 'pat_001',
        firstName: 'Robert',
        lastName: 'Henderson',
        legalFirstName: 'Robert',
        legalLastName: 'Henderson',
        dateOfBirth: '1958-03-14',
        sexAtBirth: 'Male',
        gender: 'Male',
        email: 'robert.henderson@email.com',
        phone: '(206) 555-1001',
        address: '1422 Maple St, Seattle, WA 98101',
        mothersMaidenName: 'Williams',
        insurancePrimary: 'Medicare Part B',
        insuranceId: 'MED-8827341',
        primaryProvider: 'prov_001',
        tags: ['*COVID-Dose-2-Complete', 'Diabetes-Management', 'Annual-Due'],
        passportActive: true,
        createdAt: '2019-05-12T10:00:00Z'
    },
    {
        id: 'pat_002',
        firstName: 'Emily',
        lastName: 'Nakamura',
        legalFirstName: 'Emily',
        legalLastName: 'Nakamura',
        dateOfBirth: '1985-07-22',
        sexAtBirth: 'Female',
        gender: 'Female',
        email: 'emily.nakamura@email.com',
        phone: '(206) 555-1002',
        address: '783 Pine Ave, Seattle, WA 98102',
        mothersMaidenName: 'Tanaka',
        insurancePrimary: 'Blue Cross PPO',
        insuranceId: 'BCB-4419823',
        primaryProvider: 'prov_001',
        tags: ['*COVID-Dose-1-Only', 'Prenatal'],
        passportActive: true,
        createdAt: '2020-01-15T09:30:00Z'
    },
    {
        id: 'pat_003',
        firstName: 'Marcus',
        lastName: 'Johnson',
        legalFirstName: 'Marcus',
        legalLastName: 'Johnson',
        dateOfBirth: '1972-11-08',
        sexAtBirth: 'Male',
        gender: 'Male',
        email: 'marcus.johnson@email.com',
        phone: '(206) 555-1003',
        address: '5091 Oak Dr, Bellevue, WA 98004',
        mothersMaidenName: 'Davis',
        insurancePrimary: 'Aetna HMO',
        insuranceId: 'AET-7723019',
        primaryProvider: 'prov_002',
        tags: ['Hypertension-Monitoring', 'Smoker'],
        passportActive: false,
        createdAt: '2018-09-20T14:00:00Z'
    },
    {
        id: 'pat_004',
        firstName: 'Sofia',
        lastName: 'Rodriguez-Martinez',
        legalFirstName: 'Sofia',
        legalLastName: 'Rodriguez-Martinez',
        dateOfBirth: '1995-02-28',
        sexAtBirth: 'Female',
        gender: 'Female',
        email: 'sofia.rodmart@email.com',
        phone: '(206) 555-1004',
        address: '2210 Cedar Ln, Seattle, WA 98103',
        mothersMaidenName: 'Gutierrez',
        insurancePrimary: 'United Healthcare',
        insuranceId: 'UHC-3310598',
        primaryProvider: 'prov_001',
        tags: ['*COVID-Dose-2-Complete', 'Asthma'],
        passportActive: true,
        createdAt: '2021-03-10T11:15:00Z'
    },
    {
        id: 'pat_005',
        firstName: 'William',
        lastName: 'O\'Brien',
        legalFirstName: 'William',
        legalLastName: 'O\'Brien',
        dateOfBirth: '1948-06-30',
        sexAtBirth: 'Male',
        gender: 'Male',
        email: 'wobrien@email.com',
        phone: '(206) 555-1005',
        address: '8834 Elm Way, Kirkland, WA 98033',
        mothersMaidenName: 'Murphy',
        insurancePrimary: 'Medicare Advantage',
        insuranceId: 'MCA-1128374',
        primaryProvider: 'prov_002',
        tags: ['*COVID-Booster-Due', 'CHF', 'Fall-Risk'],
        passportActive: false,
        createdAt: '2017-02-28T08:45:00Z'
    },
    {
        id: 'pat_006',
        firstName: 'Priya',
        lastName: 'Sharma',
        legalFirstName: 'Priya',
        legalLastName: 'Sharma',
        dateOfBirth: '1990-12-15',
        sexAtBirth: 'Female',
        gender: 'Female',
        email: 'priya.sharma@email.com',
        phone: '(206) 555-1006',
        address: '4401 Birch Ct, Redmond, WA 98052',
        mothersMaidenName: 'Gupta',
        insurancePrimary: 'Cigna PPO',
        insuranceId: 'CIG-5528914',
        primaryProvider: 'prov_003',
        tags: ['Pediatric-Parent'],
        passportActive: true,
        createdAt: '2022-06-01T10:30:00Z'
    },
    {
        id: 'pat_007',
        firstName: 'Thomas',
        lastName: 'Bergstrom',
        legalFirstName: 'Thomas',
        legalLastName: 'Bergstrom',
        dateOfBirth: '1965-09-03',
        sexAtBirth: 'Male',
        gender: 'Male',
        email: 'tbergstrom@email.com',
        phone: '(425) 555-1007',
        address: '1190 Walnut Ave, Bellevue, WA 98005',
        mothersMaidenName: 'Lindgren',
        insurancePrimary: 'Premera Blue Cross',
        insuranceId: 'PBC-8891234',
        primaryProvider: 'prov_001',
        tags: ['COPD', 'Diabetes-Management'],
        passportActive: true,
        createdAt: '2019-11-14T13:00:00Z'
    },
    {
        id: 'pat_008',
        firstName: 'Aaliyah',
        lastName: 'Washington',
        legalFirstName: 'Aaliyah',
        legalLastName: 'Washington',
        dateOfBirth: '2015-04-18',
        sexAtBirth: 'Female',
        gender: 'Female',
        email: 'dwashington.parent@email.com',
        phone: '(206) 555-1008',
        address: '3302 Spruce St, Seattle, WA 98108',
        mothersMaidenName: 'Jackson',
        insurancePrimary: 'Molina Medicaid',
        insuranceId: 'MOL-2293481',
        primaryProvider: 'prov_003',
        tags: ['Pediatric', 'Immunizations-Due'],
        passportActive: false,
        createdAt: '2020-08-22T09:00:00Z'
    },
    {
        id: 'pat_009',
        firstName: 'David',
        lastName: 'Kowalski',
        legalFirstName: 'David',
        legalLastName: 'Kowalski',
        dateOfBirth: '1979-01-25',
        sexAtBirth: 'Male',
        gender: 'Male',
        email: 'david.kowalski@email.com',
        phone: '(425) 555-1009',
        address: '6678 Alder Pl, Renton, WA 98055',
        mothersMaidenName: 'Nowak',
        insurancePrimary: 'Kaiser Permanente',
        insuranceId: 'KP-7712093',
        primaryProvider: 'prov_004',
        tags: ['Anxiety', 'Back-Pain'],
        passportActive: true,
        createdAt: '2021-07-19T15:30:00Z'
    },
    {
        id: 'pat_010',
        firstName: 'Helen',
        lastName: 'Zhao',
        legalFirstName: 'Helen',
        legalLastName: 'Zhao',
        dateOfBirth: '1953-08-09',
        sexAtBirth: 'Female',
        gender: 'Female',
        email: 'helen.zhao@email.com',
        phone: '(206) 555-1010',
        address: '924 Cherry St, Seattle, WA 98104',
        mothersMaidenName: 'Li',
        insurancePrimary: 'Medicare Part B',
        insuranceId: 'MED-3345812',
        primaryProvider: 'prov_001',
        tags: ['*COVID-Dose-2-Complete', 'Osteoporosis', 'Annual-Due'],
        passportActive: true,
        createdAt: '2018-04-05T10:00:00Z'
    },
    {
        id: 'pat_011',
        firstName: 'James',
        lastName: 'Fitzgerald',
        legalFirstName: 'James',
        legalLastName: 'Fitzgerald',
        dateOfBirth: '1988-05-11',
        sexAtBirth: 'Male',
        gender: 'Male',
        email: 'jfitzgerald@email.com',
        phone: '(206) 555-1011',
        address: '5543 Poplar Way, Seattle, WA 98105',
        mothersMaidenName: 'Kelly',
        insurancePrimary: 'Regence BlueCross',
        insuranceId: 'REG-4456123',
        primaryProvider: 'prov_004',
        tags: [],
        passportActive: true,
        createdAt: '2023-01-10T12:00:00Z'
    },
    {
        id: 'pat_012',
        firstName: 'Mei-Ling',
        lastName: 'Wu',
        legalFirstName: 'Mei-Ling',
        legalLastName: 'Wu',
        dateOfBirth: '2008-10-29',
        sexAtBirth: 'Female',
        gender: 'Female',
        email: 'wu.family@email.com',
        phone: '(425) 555-1012',
        address: '1887 Fir Dr, Issaquah, WA 98027',
        mothersMaidenName: 'Chen',
        insurancePrimary: 'Premera Blue Cross',
        insuranceId: 'PBC-1123987',
        primaryProvider: 'prov_003',
        tags: ['Pediatric', 'Sports-Physical'],
        passportActive: false,
        createdAt: '2021-09-15T14:30:00Z'
    }
];

// ── Visit Note Categories ──
const VISIT_NOTE_CATEGORIES = [
    { id: 'cat_001', name: 'Office Visit', countForMIPS: true, isDefault: true, sortOrder: 0 },
    { id: 'cat_002', name: 'Telehealth', countForMIPS: true, isDefault: false, sortOrder: 1 },
    { id: 'cat_003', name: 'Annual Exam', countForMIPS: true, isDefault: false, sortOrder: 2 },
    { id: 'cat_004', name: 'Procedure', countForMIPS: true, isDefault: false, sortOrder: 3 },
    { id: 'cat_005', name: 'Follow-Up', countForMIPS: true, isDefault: false, sortOrder: 4 },
    { id: 'cat_006', name: 'Care Plan Review', countForMIPS: true, isDefault: false, sortOrder: 5 },
    { id: 'cat_007', name: 'Urgent Visit', countForMIPS: true, isDefault: false, sortOrder: 6 },
    { id: 'cat_008', name: 'Vaccination Only', countForMIPS: false, isDefault: false, sortOrder: 7 },
    { id: 'cat_009', name: 'Pre-Op Evaluation', countForMIPS: true, isDefault: false, sortOrder: 8 },
    { id: 'cat_010', name: 'Workers Comp', countForMIPS: false, isDefault: false, sortOrder: 9 }
];

// ── Visit Note Formats ──
const VISIT_NOTE_FORMATS = [
    { id: 'complete_hp', name: 'Complete H&P Note (2-Column)', hasAssessment: true, hasCarePlan: true },
    { id: 'hp_single', name: 'H&P Note (Single Column)', hasAssessment: true, hasCarePlan: true },
    { id: 'pre_op', name: 'Pre-Op H&P Note', hasAssessment: true, hasCarePlan: true },
    { id: 'simple', name: 'Simple Note', hasAssessment: false, hasCarePlan: false },
    { id: 'non_visit', name: 'Non-Visit Note', hasAssessment: false, hasCarePlan: false }
];

// ── Visit Note Templates ──
const VISIT_NOTE_TEMPLATES = [
    {
        id: 'tmpl_001', name: 'E* Annual Wellness Visit', createdBy: 'prov_001',
        content: { hpi: 'Patient presents for annual wellness visit.', ros: 'Constitutional: Denies fever, chills, weight changes.\nENT: Denies sore throat, ear pain.\nCardiovascular: Denies chest pain, palpitations.\nRespiratory: Denies cough, shortness of breath.\nGI: Denies nausea, vomiting, diarrhea.\nMusculoskeletal: Denies joint pain, swelling.\nNeurological: Denies headaches, dizziness.\nPsych: Denies depression, anxiety.', pe: 'General: Alert, oriented, in no acute distress.\nHEENT: Normocephalic, atraumatic. PERRL. TMs clear bilaterally.\nNeck: Supple, no lymphadenopathy.\nCardiac: RRR, no murmurs.\nLungs: CTAB, no wheezes or rales.\nAbdomen: Soft, non-tender, non-distended.\nExtremities: No edema, pulses intact.\nSkin: No rashes or lesions.\nNeuro: CN II-XII intact.' },
        billingItems: [{ cptCode: '99395', description: 'Preventive visit, 18-39 years' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Annual', 'Preventive'],
        createdAt: '2024-01-15T10:00:00Z'
    },
    {
        id: 'tmpl_002', name: 'E* Problem-Focused Visit', createdBy: 'prov_001',
        content: { hpi: 'Patient presents with chief complaint of [CC].', assessment: 'Assessment and plan documented below.' },
        billingItems: [{ cptCode: '99213', description: 'Office visit, established, low complexity' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Problem-Focused'],
        createdAt: '2024-01-15T10:05:00Z'
    },
    {
        id: 'tmpl_003', name: 'Telehealth Follow-Up', createdBy: 'prov_001',
        content: { hpi: 'Telehealth visit conducted via video. Patient connected from home.', assessment: 'Follow-up on previously discussed concerns.' },
        billingItems: [{ cptCode: '99214', description: 'Office visit, established, moderate complexity' }],
        pos: '02',
        billingNotes: 'Telehealth visit - Place of Service 02',
        documentTags: ['Telehealth', 'Follow-Up'],
        createdAt: '2024-02-20T09:00:00Z'
    },
    {
        id: 'tmpl_004', name: 'Flu Shot Administration', createdBy: 'prov_006',
        content: { proceduresAdministered: 'Influenza vaccine administered.' },
        billingItems: [{ cptCode: '90686', description: 'IIV4 vaccine, preservative free' }, { cptCode: '90471', description: 'Immunization administration' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Vaccination', 'Flu'],
        createdAt: '2024-03-01T14:00:00Z'
    },
    {
        id: 'tmpl_005', name: 'COVID-19 Vaccine Visit', createdBy: 'prov_001',
        content: { proceduresAdministered: 'COVID-19 vaccine administered per CDC guidelines.', assessment: 'Patient tolerated vaccine well. Monitored for 15 minutes post-administration. No adverse reactions observed.' },
        billingItems: [{ cptCode: '91301', description: 'COVID-19 vaccine, mRNA-LNP' }, { cptCode: '0003A', description: 'COVID admin, 3rd dose' }],
        pos: '',
        billingNotes: '',
        documentTags: ['COVID-19', 'Vaccination'],
        createdAt: '2024-03-15T11:00:00Z'
    },
    {
        id: 'tmpl_006', name: 'Diabetes Management', createdBy: 'prov_002',
        content: { hpi: 'Patient presents for diabetes management follow-up. Reviewing glucose logs, medication adherence, and lifestyle modifications.', ros: 'Constitutional: Denies fever, significant weight changes.\nEndocrine: Reports [glucose control status]. Denies polydipsia, polyuria.\nCardiovascular: Denies chest pain.\nNeurological: Denies numbness, tingling in extremities.\nEyes: Last dilated exam [date].', pe: 'General: Well-appearing, in no distress.\nVitals: As documented.\nFeet: Skin intact, sensation intact to monofilament testing bilaterally.\nCardiac: RRR, no murmurs.\nExtremities: No edema.' },
        billingItems: [{ cptCode: '99214', description: 'Office visit, established, moderate complexity' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Diabetes', 'Chronic-Care'],
        createdAt: '2024-04-10T09:30:00Z'
    },
    {
        id: 'tmpl_007', name: 'Hypertension Follow-Up', createdBy: 'prov_002',
        content: { hpi: 'Patient returns for blood pressure management. Home BP readings reviewed.', assessment: 'Hypertension management - [controlled/uncontrolled].' },
        billingItems: [{ cptCode: '99213', description: 'Office visit, established, low complexity' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Hypertension', 'Chronic-Care'],
        createdAt: '2024-04-20T10:00:00Z'
    },
    {
        id: 'tmpl_008', name: 'Well Child Visit (2-5 years)', createdBy: 'prov_003',
        content: { hpi: 'Well child visit for age-appropriate screening and immunizations.', ros: 'Constitutional: Active, appropriate weight gain.\nDevelopment: Meeting milestones per parent report.\nNutrition: Balanced diet, adequate intake.\nSleep: Regular sleep schedule.', pe: 'General: Well-nourished, active child in no distress.\nHEENT: Normocephalic. TMs clear. Throat clear.\nCardiac: RRR, no murmurs.\nLungs: Clear.\nAbdomen: Soft, non-tender.\nMusculoskeletal: Normal gait, full ROM.\nNeuro: Age-appropriate development.\nSkin: No rashes.' },
        billingItems: [{ cptCode: '99392', description: 'Preventive visit, 1-4 years' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Pediatric', 'Well-Child'],
        createdAt: '2024-05-05T08:00:00Z'
    },
    {
        id: 'tmpl_009', name: 'Injectable Administration', createdBy: 'prov_006',
        content: { proceduresAdministered: '[Injectable name] administered via [route]. Patient tolerated procedure well.' },
        billingItems: [{ cptCode: '96372', description: 'Injection of drug or substance under skin or into muscle' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Injectable', 'Procedure'],
        createdAt: '2024-05-15T13:00:00Z'
    },
    {
        id: 'tmpl_010', name: 'Pre-Operative Evaluation', createdBy: 'prov_001',
        content: { hpi: 'Patient presents for pre-operative evaluation prior to scheduled [procedure]. Surgery date: [date]. Surgeon: [name].', ros: 'Full 14-point ROS reviewed and documented.', pe: 'Comprehensive examination as documented.', assessment: 'Patient cleared for surgery from a medical standpoint pending [conditions].' },
        billingItems: [{ cptCode: '99215', description: 'Office visit, established, high complexity' }],
        pos: '',
        billingNotes: '',
        documentTags: ['Pre-Op', 'Clearance'],
        createdAt: '2024-06-01T09:00:00Z'
    }
];

// ── Appointment Types ──
const APPOINTMENT_TYPES = [
    { id: 'apt_001', name: 'Office Visit', duration: 30, noteFormat: 'complete_hp', noteCategory: 'cat_001', noteTemplate: 'tmpl_002', color: '#4A90D9' },
    { id: 'apt_002', name: 'Annual Exam', duration: 60, noteFormat: 'complete_hp', noteCategory: 'cat_003', noteTemplate: 'tmpl_001', color: '#50C878' },
    { id: 'apt_003', name: 'Telehealth Visit', duration: 20, noteFormat: 'hp_single', noteCategory: 'cat_002', noteTemplate: 'tmpl_003', color: '#9B59B6' },
    { id: 'apt_004', name: 'Flu Shot', duration: 15, noteFormat: 'simple', noteCategory: 'cat_008', noteTemplate: 'tmpl_004', color: '#E67E22' },
    { id: 'apt_005', name: 'COVID Vaccine', duration: 30, noteFormat: 'simple', noteCategory: 'cat_008', noteTemplate: 'tmpl_005', color: '#E74C3C' },
    { id: 'apt_006', name: 'Follow-Up', duration: 20, noteFormat: 'complete_hp', noteCategory: 'cat_005', noteTemplate: '', color: '#1ABC9C' },
    { id: 'apt_007', name: 'Procedure', duration: 45, noteFormat: 'complete_hp', noteCategory: 'cat_004', noteTemplate: '', color: '#F39C12' },
    { id: 'apt_008', name: 'Urgent Same-Day', duration: 20, noteFormat: 'complete_hp', noteCategory: 'cat_007', noteTemplate: '', color: '#E74C3C' },
    { id: 'apt_009', name: 'Well Child Check', duration: 45, noteFormat: 'complete_hp', noteCategory: 'cat_003', noteTemplate: 'tmpl_008', color: '#2ECC71' },
    { id: 'apt_010', name: 'Pre-Op Clearance', duration: 60, noteFormat: 'pre_op', noteCategory: 'cat_009', noteTemplate: 'tmpl_010', color: '#3498DB' }
];

// ── Problem List (per patient) ──
const PROBLEMS = [
    // Robert Henderson (pat_001) — complex chronic conditions
    { id: 'prob_001', patientId: 'pat_001', title: 'Type 2 Diabetes Mellitus', icd10: 'E11.65', icd9: '250.00', snomed: '44054006', dxDate: '2012-06-15', status: 'Active', synopsis: 'A1C 7.2% at last check. On metformin 1000mg BID and glipizide 5mg daily. Diet controlled with moderate compliance.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_002', patientId: 'pat_001', title: 'Essential Hypertension', icd10: 'I10', icd9: '401.9', snomed: '59621000', dxDate: '2010-03-22', status: 'Controlled', synopsis: 'BP well-controlled on lisinopril 20mg daily. Home monitoring shows 128/78 average.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_003', patientId: 'pat_001', title: 'Hyperlipidemia', icd10: 'E78.5', icd9: '272.4', snomed: '55822004', dxDate: '2011-09-10', status: 'Active', synopsis: 'On atorvastatin 40mg. LDL 102 at last labs, target <100.', resolvedDate: '', sortOrder: 2 },
    { id: 'prob_004', patientId: 'pat_001', title: 'Obesity, BMI 32.1', icd10: 'E66.01', icd9: '278.01', snomed: '414916001', dxDate: '2015-01-20', status: 'Active', synopsis: 'Weight loss counseling provided. Referred to nutritionist.', resolvedDate: '', sortOrder: 3 },
    { id: 'prob_005', patientId: 'pat_001', title: 'Benign Prostatic Hyperplasia', icd10: 'N40.0', icd9: '600.00', snomed: '266569009', dxDate: '2020-11-05', status: 'Active', synopsis: 'On tamsulosin 0.4mg nightly. Symptoms improved. PSA 2.1.', resolvedDate: '', sortOrder: 4 },
    { id: 'prob_006', patientId: 'pat_001', title: 'Seasonal Allergic Rhinitis', icd10: 'J30.2', icd9: '477.9', snomed: '367498001', dxDate: '2019-04-10', status: 'Controlled', synopsis: 'Managed with cetirizine PRN during spring/summer.', resolvedDate: '', sortOrder: 5 },

    // Emily Nakamura (pat_002)
    { id: 'prob_007', patientId: 'pat_002', title: 'Generalized Anxiety Disorder', icd10: 'F41.1', icd9: '300.02', snomed: '21897009', dxDate: '2019-08-14', status: 'Active', synopsis: 'On sertraline 50mg daily. Therapy ongoing with CBT. Moderate improvement reported.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_008', patientId: 'pat_002', title: 'Iron Deficiency Anemia', icd10: 'D50.9', icd9: '280.9', snomed: '87522002', dxDate: '2023-03-20', status: 'Active', synopsis: 'Ferrous sulfate 325mg daily. Ferritin 18 at last check, target >50.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_009', patientId: 'pat_002', title: 'Migraine without Aura', icd10: 'G43.009', icd9: '346.90', snomed: '37796009', dxDate: '2018-11-02', status: 'Active', synopsis: 'Sumatriptan 50mg PRN. ~2 episodes/month. Triggers: stress, sleep deprivation.', resolvedDate: '', sortOrder: 2 },
    { id: 'prob_010', patientId: 'pat_002', title: 'Plantar Fasciitis, Right Foot', icd10: 'M72.2', icd9: '728.71', snomed: '202882003', dxDate: '2025-09-15', status: 'Resolved', synopsis: 'Resolved with stretching protocol and orthotic inserts.', resolvedDate: '2026-01-10', sortOrder: 3 },

    // Marcus Johnson (pat_003)
    { id: 'prob_011', patientId: 'pat_003', title: 'Essential Hypertension, Uncontrolled', icd10: 'I10', icd9: '401.9', snomed: '59621000', dxDate: '2016-05-18', status: 'Active', synopsis: 'BP remains elevated despite amlodipine 10mg + losartan 100mg. Adding HCTZ 25mg. Non-compliant with low-sodium diet.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_012', patientId: 'pat_003', title: 'Tobacco Use Disorder', icd10: 'F17.210', icd9: '305.1', snomed: '89765005', dxDate: '2018-09-20', status: 'Active', synopsis: '1 PPD x 20 years. Declined NRT. Counseled on cessation at every visit.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_013', patientId: 'pat_003', title: 'Chronic Low Back Pain', icd10: 'M54.5', icd9: '724.2', snomed: '278860009', dxDate: '2020-02-14', status: 'Active', synopsis: 'MRI shows disc degeneration L4-L5. PT in progress. NSAIDs PRN. No surgery recommended at this time.', resolvedDate: '', sortOrder: 2 },
    { id: 'prob_014', patientId: 'pat_003', title: 'Prediabetes', icd10: 'R73.03', icd9: '790.29', snomed: '714628002', dxDate: '2024-01-10', status: 'Active', synopsis: 'A1C 5.9%. Lifestyle modification counseling. Recheck in 6 months.', resolvedDate: '', sortOrder: 3 },

    // Sofia Rodriguez-Martinez (pat_004)
    { id: 'prob_015', patientId: 'pat_004', title: 'Persistent Asthma, Moderate', icd10: 'J45.40', icd9: '493.20', snomed: '195967001', dxDate: '2015-07-22', status: 'Active', synopsis: 'On fluticasone/salmeterol 250/50 BID. Albuterol PRN ~2x/week. Asthma action plan updated.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_016', patientId: 'pat_004', title: 'Allergic Rhinitis', icd10: 'J30.9', icd9: '477.9', snomed: '61582004', dxDate: '2016-03-10', status: 'Controlled', synopsis: 'Fluticasone nasal spray daily. Well-controlled.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_017', patientId: 'pat_004', title: 'Vitamin D Deficiency', icd10: 'E55.9', icd9: '268.9', snomed: '34713006', dxDate: '2023-11-01', status: 'Active', synopsis: 'Level 18 ng/mL. Started D3 2000 IU daily. Recheck in 3 months.', resolvedDate: '', sortOrder: 2 },

    // William O'Brien (pat_005) — elderly with complex conditions
    { id: 'prob_018', patientId: 'pat_005', title: 'Heart Failure with Reduced EF', icd10: 'I50.22', icd9: '428.22', snomed: '417996009', dxDate: '2019-08-30', status: 'Active', synopsis: 'EF 35%. On carvedilol 12.5mg BID, lisinopril 10mg, furosemide 40mg. Weight monitoring daily. Last echo 2025-09.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_019', patientId: 'pat_005', title: 'Atrial Fibrillation, Persistent', icd10: 'I48.1', icd9: '427.31', snomed: '49436004', dxDate: '2018-12-05', status: 'Active', synopsis: 'On apixaban 5mg BID for anticoagulation. Rate controlled with carvedilol. CHA2DS2-VASc score 4.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_020', patientId: 'pat_005', title: 'Chronic Kidney Disease Stage 3a', icd10: 'N18.31', icd9: '585.3', snomed: '433144002', dxDate: '2021-03-15', status: 'Active', synopsis: 'eGFR 52. Monitoring q6months. Avoiding nephrotoxins. Creatinine 1.4.', resolvedDate: '', sortOrder: 2 },
    { id: 'prob_021', patientId: 'pat_005', title: 'Osteoarthritis, Bilateral Knees', icd10: 'M17.0', icd9: '715.36', snomed: '239873007', dxDate: '2017-06-20', status: 'Active', synopsis: 'Acetaminophen PRN. Physical therapy completed. Considering joint injections.', resolvedDate: '', sortOrder: 3 },
    { id: 'prob_022', patientId: 'pat_005', title: 'History of Falls', icd10: 'Z91.81', icd9: 'V15.88', snomed: '129839007', dxDate: '2024-10-01', status: 'Active', synopsis: 'Fall risk assessment completed. Home safety evaluation ordered. PT for balance training.', resolvedDate: '', sortOrder: 4 },

    // Helen Zhao (pat_010)
    { id: 'prob_023', patientId: 'pat_010', title: 'Osteoporosis, Postmenopausal', icd10: 'M81.0', icd9: '733.01', snomed: '64859006', dxDate: '2020-02-28', status: 'Active', synopsis: 'T-score -2.8 lumbar spine. On alendronate 70mg weekly. Calcium + Vit D supplementation.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_024', patientId: 'pat_010', title: 'Hypothyroidism', icd10: 'E03.9', icd9: '244.9', snomed: '40930008', dxDate: '2015-05-10', status: 'Controlled', synopsis: 'On levothyroxine 75mcg daily. TSH 2.1 at last check - within range.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_025', patientId: 'pat_010', title: 'GERD', icd10: 'K21.0', icd9: '530.81', snomed: '235595009', dxDate: '2019-09-15', status: 'Active', synopsis: 'On omeprazole 20mg daily. Symptoms well-controlled. Dietary modifications in place.', resolvedDate: '', sortOrder: 2 },

    // Thomas Bergstrom (pat_007)
    { id: 'prob_026', patientId: 'pat_007', title: 'COPD, Moderate', icd10: 'J44.1', icd9: '491.21', snomed: '13645005', dxDate: '2020-05-20', status: 'Active', synopsis: 'FEV1 62% predicted. On tiotropium + PRN albuterol. Former smoker, quit 2018. Pulmonary rehab completed.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_027', patientId: 'pat_007', title: 'Type 2 Diabetes Mellitus, Well-Controlled', icd10: 'E11.65', icd9: '250.00', snomed: '44054006', dxDate: '2017-08-14', status: 'Controlled', synopsis: 'A1C 6.4%. On metformin 500mg BID. Good dietary compliance.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_028', patientId: 'pat_007', title: 'Major Depressive Disorder, Recurrent, in Remission', icd10: 'F33.40', icd9: '296.36', snomed: '66344007', dxDate: '2019-01-10', status: 'Controlled', synopsis: 'On bupropion 150mg daily. Stable. Therapy discontinued per patient preference. PHQ-9 score 3.', resolvedDate: '', sortOrder: 2 },

    // David Kowalski (pat_009)
    { id: 'prob_029', patientId: 'pat_009', title: 'Generalized Anxiety Disorder', icd10: 'F41.1', icd9: '300.02', snomed: '21897009', dxDate: '2021-07-19', status: 'Active', synopsis: 'On buspirone 10mg BID. GAD-7 score 12. Therapy biweekly.', resolvedDate: '', sortOrder: 0 },
    { id: 'prob_030', patientId: 'pat_009', title: 'Chronic Low Back Pain with Radiculopathy', icd10: 'M54.41', icd9: '724.4', snomed: '279039007', dxDate: '2022-03-05', status: 'Active', synopsis: 'Lumbar MRI shows L5-S1 disc herniation. Conservative management. PT ongoing. Gabapentin 300mg TID.', resolvedDate: '', sortOrder: 1 },
    { id: 'prob_031', patientId: 'pat_009', title: 'Insomnia', icd10: 'G47.00', icd9: '780.52', snomed: '193462001', dxDate: '2023-05-15', status: 'Active', synopsis: 'Sleep hygiene counseling provided. Trial of melatonin 3mg. Avoiding sedatives per patient preference.', resolvedDate: '', sortOrder: 2 }
];

// ── Vaccinations / Immunizations ──
const VACCINATIONS = [
    // Robert Henderson — older adult
    { id: 'vax_001', patientId: 'pat_001', vaccineName: 'COVID-19 Pfizer-BioNTech', cvx: '208', ndc: '59267-1000-02', manufacturer: 'Pfizer', lotNumber: 'EW0182', expirationDate: '2025-09-30', doseAmount: '0.3', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-04-15T09:30:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2025-04-15', recall: '3 weeks', reason: 'Primary series', notes: 'Monitored 15 min. No adverse reactions.', program: 'Not VFC Eligible', fundedBy: 'Private', source: 'New Immunization', status: 'completed' },
    { id: 'vax_002', patientId: 'pat_001', vaccineName: 'COVID-19 Pfizer-BioNTech', cvx: '208', ndc: '59267-1000-02', manufacturer: 'Pfizer', lotNumber: 'EW0183', expirationDate: '2025-10-15', doseAmount: '0.3', doseUnits: 'mL', seriesNumber: '2', method: 'Intramuscular', site: 'Right Deltoid', givenOn: '2025-05-06T10:00:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2025-05-06', recall: '', reason: 'Primary series completion', notes: 'No adverse reactions.', program: 'Not VFC Eligible', fundedBy: 'Private', source: 'New Immunization', status: 'completed' },
    { id: 'vax_003', patientId: 'pat_001', vaccineName: 'Influenza (IIV4) Preservative Free', cvx: '185', ndc: '49281-0718-50', manufacturer: 'Sanofi Pasteur', lotNumber: 'UJ421AA', expirationDate: '2026-06-30', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-10-12T14:00:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2025-10-12', recall: '1 year', reason: 'Annual influenza vaccination', notes: '', program: 'Not VFC Eligible', fundedBy: 'Private', source: 'New Immunization', status: 'completed' },
    { id: 'vax_004', patientId: 'pat_001', vaccineName: 'Pneumococcal 20-valent (PCV20)', cvx: '216', ndc: '00005-2000-02', manufacturer: 'Pfizer', lotNumber: 'AA1234', expirationDate: '2026-03-31', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-10-12T14:15:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2025-10-12', recall: '', reason: 'Age-appropriate pneumococcal vaccination', notes: 'Administered same visit as influenza vaccine, different arm.', program: 'Not VFC Eligible', fundedBy: 'Medicare', source: 'New Immunization', status: 'completed' },
    { id: 'vax_005', patientId: 'pat_001', vaccineName: 'Shingrix (Zoster Recombinant)', cvx: '187', ndc: '58160-0823-01', manufacturer: 'GlaxoSmithKline', lotNumber: 'ZR9001', expirationDate: '2026-08-15', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Right Deltoid', givenOn: '2024-11-20T10:30:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2024-11-20', recall: '2-6 months', reason: 'Zoster prevention, age >50', notes: 'Second dose due in 2-6 months.', program: 'Not VFC Eligible', fundedBy: 'Private', source: 'New Immunization', status: 'completed' },

    // Emily Nakamura — younger adult
    { id: 'vax_006', patientId: 'pat_002', vaccineName: 'COVID-19 Pfizer-BioNTech', cvx: '208', ndc: '59267-1000-02', manufacturer: 'Pfizer', lotNumber: 'FF2190', expirationDate: '2025-08-15', doseAmount: '0.3', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-03-20T11:00:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2025-03-20', recall: '3 weeks', reason: 'Primary series', notes: 'Patient reported mild soreness at injection site.', program: 'Not VFC Eligible', fundedBy: 'Private', source: 'New Immunization', status: 'completed' },
    { id: 'vax_007', patientId: 'pat_002', vaccineName: 'Tdap (Adacel)', cvx: '115', ndc: '49281-0400-10', manufacturer: 'Sanofi Pasteur', lotNumber: 'TP5521', expirationDate: '2026-12-31', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Right Deltoid', givenOn: '2024-02-10T09:00:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2024-02-10', recall: '10 years', reason: 'Tdap booster', notes: '', program: 'Not VFC Eligible', fundedBy: 'Private', source: 'New Immunization', status: 'completed' },

    // Aaliyah Washington — pediatric
    { id: 'vax_008', patientId: 'pat_008', vaccineName: 'DTaP (Daptacel)', cvx: '20', ndc: '49281-0286-10', manufacturer: 'Sanofi Pasteur', lotNumber: 'DC8712', expirationDate: '2026-04-30', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '5', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-09-10T10:00:00Z', orderedBy: 'prov_003', givenBy: 'prov_006', recordType: 'New', visDate: '2025-09-10', recall: '', reason: '5th dose DTaP series', notes: '', program: 'VFC Eligible', fundedBy: 'VFC', source: 'New Immunization', status: 'completed' },
    { id: 'vax_009', patientId: 'pat_008', vaccineName: 'IPV (Polio)', cvx: '10', ndc: '49281-0860-10', manufacturer: 'Sanofi Pasteur', lotNumber: 'IP3344', expirationDate: '2026-07-31', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '4', method: 'Intramuscular', site: 'Right Deltoid', givenOn: '2025-09-10T10:05:00Z', orderedBy: 'prov_003', givenBy: 'prov_006', recordType: 'New', visDate: '2025-09-10', recall: '', reason: '4th dose IPV series', notes: 'Administered same visit as DTaP.', program: 'VFC Eligible', fundedBy: 'VFC', source: 'New Immunization', status: 'completed' },
    { id: 'vax_010', patientId: 'pat_008', vaccineName: 'MMR (M-M-R II)', cvx: '03', ndc: '00006-4681-00', manufacturer: 'Merck', lotNumber: 'MM8823', expirationDate: '2026-05-15', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '2', method: 'Subcutaneous', site: 'Left Upper Arm', givenOn: '2025-09-10T10:10:00Z', orderedBy: 'prov_003', givenBy: 'prov_006', recordType: 'New', visDate: '2025-09-10', recall: '', reason: '2nd dose MMR', notes: '', program: 'VFC Eligible', fundedBy: 'VFC', source: 'New Immunization', status: 'completed' },
    { id: 'vax_011', patientId: 'pat_008', vaccineName: 'Varicella (Varivax)', cvx: '21', ndc: '00006-4827-00', manufacturer: 'Merck', lotNumber: 'VV1927', expirationDate: '2026-06-30', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '2', method: 'Subcutaneous', site: 'Right Upper Arm', givenOn: '2025-09-10T10:15:00Z', orderedBy: 'prov_003', givenBy: 'prov_006', recordType: 'New', visDate: '2025-09-10', recall: '', reason: '2nd dose Varicella', notes: '', program: 'VFC Eligible', fundedBy: 'VFC', source: 'New Immunization', status: 'completed' },

    // Historical/external vaccines
    { id: 'vax_012', patientId: 'pat_004', vaccineName: 'COVID-19 Moderna', cvx: '207', ndc: '80777-0273-10', manufacturer: 'Moderna', lotNumber: 'MOD-EXT', expirationDate: '', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-02-01T00:00:00Z', orderedBy: '', givenBy: 'Walgreens Pharmacy #4521', recordType: 'Historical', visDate: '', recall: '', reason: 'Primary series', notes: 'Documented from patient report. Given at pharmacy.', program: '', fundedBy: '', source: 'Historical', status: 'completed' },
    { id: 'vax_013', patientId: 'pat_004', vaccineName: 'COVID-19 Moderna', cvx: '207', ndc: '80777-0273-10', manufacturer: 'Moderna', lotNumber: 'MOD-EXT2', expirationDate: '', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '2', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-03-01T00:00:00Z', orderedBy: '', givenBy: 'Walgreens Pharmacy #4521', recordType: 'Historical', visDate: '', recall: '', reason: 'Primary series completion', notes: 'Documented from patient report.', program: '', fundedBy: '', source: 'Historical', status: 'completed' },

    // Declined vaccine
    { id: 'vax_014', patientId: 'pat_003', vaccineName: 'Influenza (IIV4)', cvx: '185', ndc: '', manufacturer: '', lotNumber: '', expirationDate: '', doseAmount: '', doseUnits: '', seriesNumber: '', method: '', site: '', givenOn: '2025-10-15T00:00:00Z', orderedBy: 'prov_002', givenBy: '', recordType: 'Declined', visDate: '2025-10-15', recall: '', reason: 'Patient declined - personal preference', notes: 'Patient counseled on benefits. Declined. Will reconsider.', program: '', fundedBy: '', source: '', status: 'declined' },

    // Mei-Ling Wu — adolescent
    { id: 'vax_015', patientId: 'pat_012', vaccineName: 'HPV (Gardasil 9)', cvx: '165', ndc: '00006-4119-03', manufacturer: 'Merck', lotNumber: 'HP7821', expirationDate: '2026-11-30', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Left Deltoid', givenOn: '2025-11-05T14:00:00Z', orderedBy: 'prov_003', givenBy: 'prov_006', recordType: 'New', visDate: '2025-11-05', recall: '6 months', reason: 'HPV vaccination series, dose 1', notes: 'Parent consent obtained.', program: 'VFC Eligible', fundedBy: 'VFC', source: 'New Immunization', status: 'completed' },
    { id: 'vax_016', patientId: 'pat_012', vaccineName: 'Meningococcal (MenACWY)', cvx: '114', ndc: '49281-0589-05', manufacturer: 'Sanofi Pasteur', lotNumber: 'MN2255', expirationDate: '2027-01-31', doseAmount: '0.5', doseUnits: 'mL', seriesNumber: '1', method: 'Intramuscular', site: 'Right Deltoid', givenOn: '2025-11-05T14:10:00Z', orderedBy: 'prov_003', givenBy: 'prov_006', recordType: 'New', visDate: '2025-11-05', recall: '16 years booster', reason: 'Meningococcal vaccination', notes: '', program: 'VFC Eligible', fundedBy: 'VFC', source: 'New Immunization', status: 'completed' },

    // Injectables (non-vaccine)
    { id: 'vax_017', patientId: 'pat_005', vaccineName: 'Depo-Medrol (Methylprednisolone)', cvx: '', ndc: '00009-0280-02', manufacturer: 'Pfizer', lotNumber: 'DM4419', expirationDate: '2026-09-30', doseAmount: '40', doseUnits: 'mg', seriesNumber: '', method: 'Intra-articular', site: 'Right Knee', givenOn: '2026-01-15T11:00:00Z', orderedBy: 'prov_002', givenBy: 'prov_002', recordType: 'New', visDate: '2026-01-15', recall: '3 months', reason: 'Osteoarthritis pain management', notes: 'Corticosteroid injection for knee OA. Patient tolerated well.', program: '', fundedBy: 'Private', source: 'New Immunization', status: 'completed', isInjectable: true, notSendToRegistry: true },
    { id: 'vax_018', patientId: 'pat_001', vaccineName: 'Vitamin B12 (Cyanocobalamin)', cvx: '', ndc: '00591-3380-01', manufacturer: 'Watson Labs', lotNumber: 'B12-8832', expirationDate: '2027-02-28', doseAmount: '1000', doseUnits: 'mcg', seriesNumber: '', method: 'Intramuscular', site: 'Right Deltoid', givenOn: '2026-02-10T15:30:00Z', orderedBy: 'prov_001', givenBy: 'prov_006', recordType: 'New', visDate: '2026-02-10', recall: '1 month', reason: 'B12 deficiency supplementation', notes: 'Monthly injection. Patient tolerating well.', program: '', fundedBy: 'Private', source: 'New Immunization', status: 'completed', isInjectable: true, notSendToRegistry: true }
];

// ── Vitals ──
const VITALS = [
    // Robert Henderson — multiple visits
    { id: 'vit_001', patientId: 'pat_001', noteId: 'note_001', date: '2026-02-15T09:00:00Z', bloodPressureSystolic: 132, bloodPressureDiastolic: 82, heartRate: 78, respiratoryRate: 16, temperature: 98.4, temperatureUnit: 'F', oxygenSaturation: 97, weight: 218, weightUnit: 'lbs', height: 70, heightUnit: 'in', bmi: 31.3, painLevel: 2 },
    { id: 'vit_002', patientId: 'pat_001', noteId: 'note_002', date: '2025-11-20T10:30:00Z', bloodPressureSystolic: 128, bloodPressureDiastolic: 78, heartRate: 72, respiratoryRate: 14, temperature: 98.6, temperatureUnit: 'F', oxygenSaturation: 98, weight: 220, weightUnit: 'lbs', height: 70, heightUnit: 'in', bmi: 31.6, painLevel: 0 },
    { id: 'vit_003', patientId: 'pat_001', noteId: 'note_003', date: '2025-08-10T09:15:00Z', bloodPressureSystolic: 136, bloodPressureDiastolic: 84, heartRate: 80, respiratoryRate: 16, temperature: 98.2, temperatureUnit: 'F', oxygenSaturation: 97, weight: 222, weightUnit: 'lbs', height: 70, heightUnit: 'in', bmi: 31.8, painLevel: 0 },
    // Historical home BP readings for Robert
    { id: 'vit_004', patientId: 'pat_001', noteId: 'note_hist_001', date: '2026-02-01T08:00:00Z', bloodPressureSystolic: 130, bloodPressureDiastolic: 80, heartRate: 74, respiratoryRate: null, temperature: null, temperatureUnit: '', oxygenSaturation: null, weight: null, weightUnit: '', height: null, heightUnit: '', bmi: null, painLevel: null },
    { id: 'vit_005', patientId: 'pat_001', noteId: 'note_hist_001', date: '2026-01-25T07:30:00Z', bloodPressureSystolic: 134, bloodPressureDiastolic: 82, heartRate: 76, respiratoryRate: null, temperature: null, temperatureUnit: '', oxygenSaturation: null, weight: null, weightUnit: '', height: null, heightUnit: '', bmi: null, painLevel: null },
    { id: 'vit_006', patientId: 'pat_001', noteId: 'note_hist_001', date: '2026-01-18T08:15:00Z', bloodPressureSystolic: 126, bloodPressureDiastolic: 76, heartRate: 70, respiratoryRate: null, temperature: null, temperatureUnit: '', oxygenSaturation: null, weight: null, weightUnit: '', height: null, heightUnit: '', bmi: null, painLevel: null },

    // Emily Nakamura
    { id: 'vit_007', patientId: 'pat_002', noteId: 'note_004', date: '2026-01-22T11:00:00Z', bloodPressureSystolic: 118, bloodPressureDiastolic: 72, heartRate: 68, respiratoryRate: 14, temperature: 98.6, temperatureUnit: 'F', oxygenSaturation: 99, weight: 135, weightUnit: 'lbs', height: 64, heightUnit: 'in', bmi: 23.2, painLevel: 0 },

    // Marcus Johnson — elevated BP
    { id: 'vit_008', patientId: 'pat_003', noteId: 'note_005', date: '2026-02-05T14:30:00Z', bloodPressureSystolic: 158, bloodPressureDiastolic: 96, heartRate: 82, respiratoryRate: 16, temperature: 98.8, temperatureUnit: 'F', oxygenSaturation: 96, weight: 245, weightUnit: 'lbs', height: 72, heightUnit: 'in', bmi: 33.2, painLevel: 4 },
    { id: 'vit_009', patientId: 'pat_003', noteId: 'note_006', date: '2025-10-15T10:00:00Z', bloodPressureSystolic: 152, bloodPressureDiastolic: 94, heartRate: 84, respiratoryRate: 18, temperature: 98.4, temperatureUnit: 'F', oxygenSaturation: 95, weight: 242, weightUnit: 'lbs', height: 72, heightUnit: 'in', bmi: 32.8, painLevel: 5 },

    // William O'Brien — elderly
    { id: 'vit_010', patientId: 'pat_005', noteId: 'note_007', date: '2026-01-15T09:30:00Z', bloodPressureSystolic: 140, bloodPressureDiastolic: 88, heartRate: 72, respiratoryRate: 18, temperature: 97.8, temperatureUnit: 'F', oxygenSaturation: 94, weight: 192, weightUnit: 'lbs', height: 68, heightUnit: 'in', bmi: 29.2, painLevel: 3 },

    // Aaliyah Washington — pediatric
    { id: 'vit_011', patientId: 'pat_008', noteId: 'note_008', date: '2025-09-10T10:00:00Z', bloodPressureSystolic: 100, bloodPressureDiastolic: 65, heartRate: 90, respiratoryRate: 20, temperature: 98.6, temperatureUnit: 'F', oxygenSaturation: 99, weight: 42, weightUnit: 'lbs', height: 42, heightUnit: 'in', bmi: 16.8, painLevel: 0 },

    // Sofia Rodriguez-Martinez
    { id: 'vit_012', patientId: 'pat_004', noteId: 'note_009', date: '2026-01-08T13:00:00Z', bloodPressureSystolic: 112, bloodPressureDiastolic: 68, heartRate: 72, respiratoryRate: 16, temperature: 98.4, temperatureUnit: 'F', oxygenSaturation: 97, weight: 140, weightUnit: 'lbs', height: 65, heightUnit: 'in', bmi: 23.3, painLevel: 0 },

    // Helen Zhao
    { id: 'vit_013', patientId: 'pat_010', noteId: 'note_010', date: '2026-02-20T10:00:00Z', bloodPressureSystolic: 124, bloodPressureDiastolic: 74, heartRate: 68, respiratoryRate: 14, temperature: 97.6, temperatureUnit: 'F', oxygenSaturation: 97, weight: 128, weightUnit: 'lbs', height: 62, heightUnit: 'in', bmi: 23.4, painLevel: 1 },

    // Thomas Bergstrom
    { id: 'vit_014', patientId: 'pat_007', noteId: 'note_011', date: '2026-02-12T14:00:00Z', bloodPressureSystolic: 130, bloodPressureDiastolic: 80, heartRate: 76, respiratoryRate: 16, temperature: 98.2, temperatureUnit: 'F', oxygenSaturation: 93, weight: 198, weightUnit: 'lbs', height: 71, heightUnit: 'in', bmi: 27.6, painLevel: 2 }
];

// ── Visit Notes ──
const VISIT_NOTES = [
    {
        id: 'note_001', patientId: 'pat_001', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_005', templateUsed: 'tmpl_007',
        date: '2026-02-15T09:00:00Z', status: 'signed', signedAt: '2026-02-15T11:30:00Z',
        reason: 'Follow-up: Hypertension and Diabetes Management',
        blocks: [
            { type: 'hpi', content: 'Patient returns for 3-month follow-up of hypertension and diabetes. Reports compliance with medications. Home BP readings averaging 130/80. No hypoglycemic episodes. Last A1C 7.2% drawn 2025-12.' },
            { type: 'vitals', content: 'See vitals section' },
            { type: 'ros', content: 'Constitutional: Denies fever, weight changes.\nCardiovascular: Denies chest pain, palpitations, edema.\nEndocrine: Denies polydipsia, polyuria.\nNeurological: Denies numbness, tingling.\nPsych: Denies depression.' },
            { type: 'pe', content: 'General: Alert, oriented, in no acute distress. Overweight.\nCardiac: RRR, no murmurs, rubs, or gallops.\nLungs: CTAB.\nExtremities: No edema. Pedal pulses palpable.\nFeet: Skin intact, sensation intact to monofilament.' },
            { type: 'assessment', content: 'Type 2 Diabetes Mellitus (E11.65) - A1C slightly above goal, increase metformin.\nEssential Hypertension (I10) - Well-controlled on current regimen.\nHyperlipidemia (E78.5) - Recheck lipid panel.', diagnoses: ['E11.65', 'I10', 'E78.5'] },
            { type: 'carePlan', content: 'Increase metformin to 1000mg BID (from 500mg BID).\nContinue lisinopril 20mg daily.\nOrder lipid panel.\nDietary counseling reinforced.\nReturn in 3 months for A1C recheck.\nAnnual eye exam referral placed.' },
            { type: 'reconciled_medications', content: 'Metformin 1000mg BID, Lisinopril 20mg daily, Atorvastatin 40mg daily, Glipizide 5mg daily, Tamsulosin 0.4mg nightly' }
        ],
        billingItems: [{ cptCode: '99214', description: 'Office visit, established, moderate complexity' }],
        documentTags: ['Diabetes', 'Hypertension', 'Chronic-Care']
    },
    {
        id: 'note_002', patientId: 'pat_001', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_003', templateUsed: 'tmpl_001',
        date: '2025-11-20T10:30:00Z', status: 'signed', signedAt: '2025-11-20T14:00:00Z',
        reason: 'Annual Exam',
        blocks: [
            { type: 'hpi', content: 'Patient presents for annual wellness visit. No new complaints. Chronic conditions stable.' },
            { type: 'vitals', content: 'See vitals section' },
            { type: 'ros', content: 'Full 14-point ROS reviewed and negative except as noted in HPI.' },
            { type: 'pe', content: 'Comprehensive exam performed. See documentation.' },
            { type: 'assessment', content: 'Annual wellness visit. Chronic conditions reviewed and stable.', diagnoses: ['Z00.00'] },
            { type: 'carePlan', content: 'Continue current medications.\nScreening labs ordered: CBC, CMP, Lipid, A1C, PSA, TSH.\nColorectal cancer screening: up to date.\nInfluenza and Pneumococcal vaccines administered today.\nReturn in 3 months for chronic care follow-up.' }
        ],
        billingItems: [{ cptCode: '99395', description: 'Preventive visit, 40-64 years' }],
        documentTags: ['Annual', 'Preventive']
    },
    {
        id: 'note_003', patientId: 'pat_001', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_001', templateUsed: '',
        date: '2025-08-10T09:15:00Z', status: 'signed', signedAt: '2025-08-10T11:45:00Z',
        reason: 'Follow-up: Diabetes and BPH',
        blocks: [
            { type: 'hpi', content: 'Follow-up visit. A1C improved to 7.2% from 7.8%. BPH symptoms improved on tamsulosin.' },
            { type: 'assessment', content: 'Diabetes improving. BPH controlled.', diagnoses: ['E11.65', 'N40.0'] },
            { type: 'carePlan', content: 'Continue current regimen. Follow up 3 months.' }
        ],
        billingItems: [{ cptCode: '99213', description: 'Office visit, established, low complexity' }],
        documentTags: ['Diabetes', 'Follow-Up']
    },
    {
        id: 'note_004', patientId: 'pat_002', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_001', templateUsed: '',
        date: '2026-01-22T11:00:00Z', status: 'signed', signedAt: '2026-01-22T13:00:00Z',
        reason: 'Follow-up: Anxiety and Anemia',
        blocks: [
            { type: 'hpi', content: 'Patient reports moderate improvement in anxiety symptoms on sertraline. PHQ-9 score 8. GAD-7 score 10. Iron levels slowly improving.' },
            { type: 'assessment', content: 'GAD - partially improved on sertraline 50mg.\nIron deficiency anemia - improving, ferritin 18 trending up from 12.', diagnoses: ['F41.1', 'D50.9'] },
            { type: 'carePlan', content: 'Increase sertraline to 75mg daily.\nContinue ferrous sulfate 325mg daily with vitamin C.\nRecheck ferritin and CBC in 6 weeks.\nContinue CBT therapy.\nReturn 6 weeks.' }
        ],
        billingItems: [{ cptCode: '99214', description: 'Office visit, established, moderate complexity' }],
        documentTags: ['Mental-Health', 'Anemia']
    },
    {
        id: 'note_005', patientId: 'pat_003', providerId: 'prov_002',
        format: 'complete_hp', category: 'cat_007', templateUsed: '',
        date: '2026-02-05T14:30:00Z', status: 'signed', signedAt: '2026-02-05T16:00:00Z',
        reason: 'Urgent: Elevated Blood Pressure',
        blocks: [
            { type: 'hpi', content: 'Patient presents with headache and dizziness. Home BP readings 160s/100s over past 3 days. Non-compliant with low-sodium diet. Missed last 2 days of medications.' },
            { type: 'assessment', content: 'Hypertensive urgency (I10). Non-adherence to treatment plan.', diagnoses: ['I10'] },
            { type: 'carePlan', content: 'Add HCTZ 25mg daily.\nSmoke cessation counseling - patient declined NRT again.\nRecheck BP in 1 week.\nDietary counseling reinforced.\nReturn 2 weeks.' }
        ],
        billingItems: [{ cptCode: '99214', description: 'Office visit, established, moderate complexity' }],
        documentTags: ['Hypertension', 'Urgent']
    },
    {
        id: 'note_006', patientId: 'pat_003', providerId: 'prov_002',
        format: 'complete_hp', category: 'cat_001', templateUsed: '',
        date: '2025-10-15T10:00:00Z', status: 'signed', signedAt: '2025-10-15T12:30:00Z',
        reason: 'Follow-up: Hypertension and Back Pain',
        blocks: [
            { type: 'hpi', content: 'Follow-up visit. BP still elevated. Low back pain ongoing, 5/10 severity.' },
            { type: 'assessment', content: 'Uncontrolled hypertension. Chronic low back pain.', diagnoses: ['I10', 'M54.5'] },
            { type: 'carePlan', content: 'Increase losartan to 100mg. Continue PT for back. Recheck 6 weeks.' }
        ],
        billingItems: [{ cptCode: '99213', description: 'Office visit, established, low complexity' }],
        documentTags: ['Hypertension', 'Back-Pain']
    },
    {
        id: 'note_007', patientId: 'pat_005', providerId: 'prov_002',
        format: 'complete_hp', category: 'cat_001', templateUsed: '',
        date: '2026-01-15T09:30:00Z', status: 'signed', signedAt: '2026-01-15T12:00:00Z',
        reason: 'Follow-up: CHF and Atrial Fibrillation',
        blocks: [
            { type: 'hpi', content: 'Patient returns for cardiac follow-up. Reports mild DOE with stairs but no PND or orthopnea. Weight stable. Taking all medications as prescribed. Daily weight log reviewed.' },
            { type: 'assessment', content: 'HFrEF (I50.22) - stable, NYHA class II.\nAtrial fibrillation (I48.1) - rate controlled.\nCKD 3a (N18.31) - stable.', diagnoses: ['I50.22', 'I48.1', 'N18.31'] },
            { type: 'carePlan', content: 'Continue current cardiac regimen.\nBMP and BNP ordered.\nEcho scheduled for April.\nFall prevention discussed.\nReturn 3 months.' }
        ],
        billingItems: [{ cptCode: '99215', description: 'Office visit, established, high complexity' }],
        documentTags: ['Cardiology', 'CHF', 'Complex']
    },
    {
        id: 'note_008', patientId: 'pat_008', providerId: 'prov_003',
        format: 'complete_hp', category: 'cat_003', templateUsed: 'tmpl_008',
        date: '2025-09-10T10:00:00Z', status: 'signed', signedAt: '2025-09-10T11:30:00Z',
        reason: 'Well Child Visit - 10 years',
        blocks: [
            { type: 'hpi', content: 'Well child visit. No parental concerns. Doing well in school. Active in soccer.' },
            { type: 'vitals', content: 'See vitals section' },
            { type: 'pe', content: 'Well-nourished child in no distress. Growth parameters within normal limits.' },
            { type: 'assessment', content: 'Healthy child, age-appropriate development.', diagnoses: ['Z00.129'] },
            { type: 'carePlan', content: 'Vaccines administered: DTaP #5, IPV #4, MMR #2, Varicella #2.\nAnticipatory guidance provided.\nReturn in 1 year.' },
            { type: 'procedures_administered', content: 'DTaP (Daptacel) dose 5, IPV dose 4, MMR (M-M-R II) dose 2, Varicella (Varivax) dose 2' }
        ],
        billingItems: [{ cptCode: '99394', description: 'Preventive visit, 5-11 years' }],
        documentTags: ['Pediatric', 'Well-Child', 'Immunizations']
    },
    {
        id: 'note_009', patientId: 'pat_004', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_005', templateUsed: '',
        date: '2026-01-08T13:00:00Z', status: 'signed', signedAt: '2026-01-08T14:30:00Z',
        reason: 'Follow-up: Asthma',
        blocks: [
            { type: 'hpi', content: 'Asthma follow-up. Using rescue inhaler ~2x/week. No ER visits. Allergy symptoms well-controlled.' },
            { type: 'assessment', content: 'Moderate persistent asthma - stable on current therapy.\nVitamin D deficiency - recheck level.', diagnoses: ['J45.40', 'E55.9'] },
            { type: 'carePlan', content: 'Continue fluticasone/salmeterol. Vitamin D level ordered. Return 3 months.' }
        ],
        billingItems: [{ cptCode: '99213', description: 'Office visit, established, low complexity' }],
        documentTags: ['Asthma', 'Follow-Up']
    },
    {
        id: 'note_010', patientId: 'pat_010', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_003', templateUsed: 'tmpl_001',
        date: '2026-02-20T10:00:00Z', status: 'signed', signedAt: '2026-02-20T13:00:00Z',
        reason: 'Annual Exam',
        blocks: [
            { type: 'hpi', content: 'Annual wellness visit. Reports occasional heartburn controlled with omeprazole. No falls. Taking alendronate weekly as prescribed.' },
            { type: 'assessment', content: 'Annual wellness visit. Chronic conditions stable.\nOsteoporosis (M81.0) - on treatment.\nHypothyroidism (E03.9) - well controlled.\nGERD (K21.0) - controlled.', diagnoses: ['Z00.00', 'M81.0', 'E03.9', 'K21.0'] },
            { type: 'carePlan', content: 'Labs ordered: TSH, CMP, CBC, DEXA scan.\nContinue current medications.\nBone density scan scheduled.\nReturn 1 year or sooner if concerns.' }
        ],
        billingItems: [{ cptCode: '99396', description: 'Preventive visit, 65+ years' }],
        documentTags: ['Annual', 'Preventive', 'Geriatric']
    },
    {
        id: 'note_011', patientId: 'pat_007', providerId: 'prov_001',
        format: 'complete_hp', category: 'cat_005', templateUsed: '',
        date: '2026-02-12T14:00:00Z', status: 'signed', signedAt: '2026-02-12T16:00:00Z',
        reason: 'Follow-up: COPD and Diabetes',
        blocks: [
            { type: 'hpi', content: 'Patient returns for chronic disease management. COPD stable, using tiotropium daily. No exacerbations. Diabetes well-controlled. A1C 6.4%. PHQ-9 score 3.' },
            { type: 'assessment', content: 'COPD moderate (J44.1) - stable.\nType 2 DM (E11.65) - well controlled.\nMDD in remission (F33.40) - stable.', diagnoses: ['J44.1', 'E11.65', 'F33.40'] },
            { type: 'carePlan', content: 'Continue current regimen.\nSpirometry scheduled for May.\nA1C recheck in 6 months.\nContinue bupropion.\nReturn 3 months.' }
        ],
        billingItems: [{ cptCode: '99214', description: 'Office visit, established, moderate complexity' }],
        documentTags: ['COPD', 'Diabetes', 'Chronic-Care']
    },
    // Draft note
    {
        id: 'note_012', patientId: 'pat_009', providerId: 'prov_004',
        format: 'complete_hp', category: 'cat_001', templateUsed: '',
        date: '2026-03-05T10:00:00Z', status: 'draft', signedAt: '',
        reason: 'Follow-up: Anxiety and Back Pain',
        blocks: [
            { type: 'hpi', content: 'Patient presents for follow-up of anxiety and chronic low back pain with radiculopathy. Reports minimal improvement with gabapentin.' }
        ],
        billingItems: [],
        documentTags: []
    },
    // Non-visit note for historical vitals
    {
        id: 'note_hist_001', patientId: 'pat_001', providerId: 'prov_001',
        format: 'non_visit', category: 'cat_001', templateUsed: '',
        date: '2026-02-01T08:00:00Z', status: 'signed', signedAt: '2026-02-01T08:15:00Z',
        reason: 'Historical Home BP Readings',
        blocks: [
            { type: 'vitals', content: 'Home blood pressure readings documented for trending.' }
        ],
        billingItems: [],
        documentTags: ['Home-Monitoring', 'BP']
    }
];

// ── Care Plans ──
const CARE_PLANS = [
    {
        id: 'cp_001', patientId: 'pat_001', noteId: 'note_001', providerId: 'prov_001',
        date: '2026-02-15T09:00:00Z',
        content: 'Increase metformin to 1000mg BID (from 500mg BID).\nContinue lisinopril 20mg daily.\nOrder lipid panel.\nDietary counseling reinforced.\nReturn in 3 months for A1C recheck.\nAnnual eye exam referral placed.',
        diagnoses: ['E11.65', 'I10', 'E78.5'],
        status: 'active'
    },
    {
        id: 'cp_002', patientId: 'pat_005', noteId: 'note_007', providerId: 'prov_002',
        date: '2026-01-15T09:30:00Z',
        content: 'Continue current cardiac regimen.\nBMP and BNP ordered.\nEcho scheduled for April.\nFall prevention discussed.\nReturn 3 months.',
        diagnoses: ['I50.22', 'I48.1', 'N18.31'],
        status: 'active'
    },
    {
        id: 'cp_003', patientId: 'pat_003', noteId: 'note_005', providerId: 'prov_002',
        date: '2026-02-05T14:30:00Z',
        content: 'Add HCTZ 25mg daily.\nSmoke cessation counseling.\nRecheck BP in 1 week.\nDietary counseling.\nReturn 2 weeks.',
        diagnoses: ['I10'],
        status: 'active'
    }
];

// ── Document Tags ──
const DOCUMENT_TAGS = [
    'Annual', 'Anemia', 'Asthma', 'Back-Pain', 'BP', 'COVID-19', 'COPD',
    'Cardiology', 'CHF', 'Chronic-Care', 'Clearance', 'Complex', 'Diabetes',
    'Flu', 'Follow-Up', 'Geriatric', 'Home-Monitoring', 'Hypertension',
    'Immunizations', 'Injectable', 'Mental-Health', 'Pediatric', 'Pre-Op',
    'Preventive', 'Procedure', 'Problem-Focused', 'Sports-Physical',
    'Telehealth', 'Urgent', 'Vaccination', 'Well-Child'
];

// ── Vaccine Name Options (for dropdown) ──
const VACCINE_NAME_OPTIONS = [
    'COVID-19 Pfizer-BioNTech', 'COVID-19 Moderna', 'COVID-19 J&J/Janssen',
    'Influenza (IIV4) Preservative Free', 'Influenza (IIV4) Standard',
    'Tdap (Adacel)', 'Td (Tenivac)', 'DTaP (Daptacel)', 'DTaP (Infanrix)',
    'MMR (M-M-R II)', 'Varicella (Varivax)', 'MMRV (ProQuad)',
    'Hepatitis A (Havrix)', 'Hepatitis A (Vaqta)', 'Hepatitis B (Engerix-B)',
    'Hepatitis B (Recombivax HB)', 'Hep A-Hep B (Twinrix)',
    'IPV (Polio)', 'HPV (Gardasil 9)',
    'Pneumococcal 20-valent (PCV20)', 'Pneumococcal 23-valent (PPSV23)',
    'Meningococcal (MenACWY)', 'Meningococcal B (Bexsero)',
    'Shingrix (Zoster Recombinant)', 'Rotavirus (RotaTeq)', 'Rotavirus (Rotarix)',
    'Hib (ActHIB)', 'Hib (PedvaxHIB)',
    'Vitamin B12 (Cyanocobalamin)', 'Depo-Medrol (Methylprednisolone)',
    'Testosterone Cypionate', 'Ketorolac (Toradol)', 'Epinephrine',
    'Dexamethasone', 'Ceftriaxone (Rocephin)', 'Penicillin G Benzathine'
];

// ── Vaccine Manufacturers ──
const VACCINE_MANUFACTURERS = [
    'Pfizer', 'Moderna', 'Janssen/J&J', 'Sanofi Pasteur', 'Merck',
    'GlaxoSmithKline', 'Seqirus', 'AstraZeneca', 'Novavax', 'Watson Labs',
    'Other', 'Unknown'
];

// ── Administration Methods ──
const ADMIN_METHODS = [
    'Intramuscular', 'Subcutaneous', 'Intradermal', 'Oral', 'Intranasal',
    'Intra-articular', 'Intravenous'
];

// ── Administration Sites ──
const ADMIN_SITES = [
    'Left Deltoid', 'Right Deltoid', 'Left Thigh', 'Right Thigh',
    'Left Upper Arm', 'Right Upper Arm', 'Left Gluteal', 'Right Gluteal',
    'Left Knee', 'Right Knee', 'Left Shoulder', 'Right Shoulder',
    'Oral', 'Intranasal'
];

// ── Recall Options ──
const RECALL_OPTIONS = [
    '', '1 week', '2 weeks', '3 weeks', '1 month', '2 months', '3 months',
    '6 months', '1 year', '2-6 months', '5 years', '10 years', '16 years booster'
];

// ── Program/VFC Options ──
const PROGRAM_OPTIONS = [
    'Not VFC Eligible', 'VFC Eligible', 'Not Applicable'
];

// ── Funded By Options ──
const FUNDED_BY_OPTIONS = [
    'Private', 'Medicare', 'Medicaid', 'VFC', 'Self-Pay', 'Insurance', 'Other'
];

// ── Standard Visit Note Blocks ──
const STANDARD_BLOCKS = [
    { type: 'allergies', name: 'Allergies', canAddMultiple: false },
    { type: 'assessment', name: 'Assessment & Plan', canAddMultiple: false },
    { type: 'carePlan', name: 'Care Plan', canAddMultiple: false },
    { type: 'cognitive_status', name: 'Cognitive Status', canAddMultiple: false },
    { type: 'data', name: 'Data', canAddMultiple: false },
    { type: 'diet', name: 'Diet', canAddMultiple: false },
    { type: 'exercise', name: 'Exercise History', canAddMultiple: false },
    { type: 'family_history', name: 'Family History', canAddMultiple: false },
    { type: 'follow_up', name: 'Follow Up', canAddMultiple: false },
    { type: 'functional_status', name: 'Functional Status', canAddMultiple: false },
    { type: 'habits', name: 'Habits', canAddMultiple: false },
    { type: 'hpi', name: 'HPI', canAddMultiple: false },
    { type: 'past_medical_history', name: 'Past Medical History', canAddMultiple: false },
    { type: 'past_surgical_history', name: 'Past Surgical History', canAddMultiple: false },
    { type: 'pe', name: 'Physical Exam', canAddMultiple: false },
    { type: 'procedures_administered', name: 'Procedures Administered', canAddMultiple: false },
    { type: 'psychological_status', name: 'Psychological Status', canAddMultiple: false },
    { type: 'reconciled_medications', name: 'Reconciled Medications', canAddMultiple: false },
    { type: 'ros', name: 'Review of Systems', canAddMultiple: false },
    { type: 'social_history', name: 'Social History', canAddMultiple: false },
    { type: 'vitals', name: 'Vitals', canAddMultiple: false },
    { type: 'lab_order', name: 'Lab Order', canAddMultiple: true },
    { type: 'imaging_order', name: 'Imaging Order', canAddMultiple: true },
    { type: 'prescription', name: 'Prescription', canAddMultiple: true }
];

// ── Common ICD-10 Codes (for assessment search) ──
const ICD10_DATABASE = [
    { code: 'E11.65', description: 'Type 2 diabetes mellitus with hyperglycemia' },
    { code: 'E11.9', description: 'Type 2 diabetes mellitus without complications' },
    { code: 'I10', description: 'Essential (primary) hypertension' },
    { code: 'E78.5', description: 'Hyperlipidemia, unspecified' },
    { code: 'E78.0', description: 'Pure hypercholesterolemia, unspecified' },
    { code: 'E66.01', description: 'Morbid (severe) obesity due to excess calories' },
    { code: 'E66.09', description: 'Other obesity due to excess calories' },
    { code: 'J45.40', description: 'Moderate persistent asthma, uncomplicated' },
    { code: 'J45.20', description: 'Mild intermittent asthma, uncomplicated' },
    { code: 'J44.1', description: 'Chronic obstructive pulmonary disease with acute exacerbation' },
    { code: 'J44.0', description: 'COPD with acute lower respiratory infection' },
    { code: 'F41.1', description: 'Generalized anxiety disorder' },
    { code: 'F41.9', description: 'Anxiety disorder, unspecified' },
    { code: 'F32.1', description: 'Major depressive disorder, single episode, moderate' },
    { code: 'F33.0', description: 'Major depressive disorder, recurrent, mild' },
    { code: 'F33.40', description: 'Major depressive disorder, recurrent, in remission' },
    { code: 'I50.22', description: 'Chronic systolic (congestive) heart failure' },
    { code: 'I48.1', description: 'Persistent atrial fibrillation' },
    { code: 'I48.91', description: 'Unspecified atrial fibrillation' },
    { code: 'N18.31', description: 'Chronic kidney disease, stage 3a' },
    { code: 'N18.4', description: 'Chronic kidney disease, stage 4' },
    { code: 'M54.5', description: 'Low back pain' },
    { code: 'M54.41', description: 'Lumbago with sciatica, right side' },
    { code: 'M17.0', description: 'Bilateral primary osteoarthritis of knee' },
    { code: 'M81.0', description: 'Age-related osteoporosis without current pathological fracture' },
    { code: 'D50.9', description: 'Iron deficiency anemia, unspecified' },
    { code: 'G43.009', description: 'Migraine without aura, not intractable, without status migrainosus' },
    { code: 'G47.00', description: 'Insomnia, unspecified' },
    { code: 'E03.9', description: 'Hypothyroidism, unspecified' },
    { code: 'K21.0', description: 'Gastro-esophageal reflux disease with esophagitis' },
    { code: 'K21.9', description: 'Gastro-esophageal reflux disease without esophagitis' },
    { code: 'J30.2', description: 'Other seasonal allergic rhinitis' },
    { code: 'J30.9', description: 'Allergic rhinitis, unspecified' },
    { code: 'N40.0', description: 'Benign prostatic hyperplasia without lower urinary tract symptoms' },
    { code: 'E55.9', description: 'Vitamin D deficiency, unspecified' },
    { code: 'R73.03', description: 'Prediabetes' },
    { code: 'F17.210', description: 'Nicotine dependence, cigarettes, uncomplicated' },
    { code: 'M72.2', description: 'Plantar fascial fibromatosis' },
    { code: 'Z00.00', description: 'Encounter for general adult medical examination without abnormal findings' },
    { code: 'Z00.129', description: 'Encounter for routine child health examination without abnormal findings' },
    { code: 'Z91.81', description: 'History of falling' },
    { code: 'Z87.891', description: 'Personal history of nicotine dependence' },
    { code: 'R50.9', description: 'Fever, unspecified' },
    { code: 'R05.9', description: 'Cough, unspecified' },
    { code: 'R10.9', description: 'Unspecified abdominal pain' },
    { code: 'R51.9', description: 'Headache, unspecified' },
    { code: 'J06.9', description: 'Acute upper respiratory infection, unspecified' },
    { code: 'N39.0', description: 'Urinary tract infection, site not specified' },
    { code: 'L30.9', description: 'Dermatitis, unspecified' },
    { code: 'R42', description: 'Dizziness and giddiness' }
];

// ── Provider Preferences ──
const PROVIDER_PREFERENCES = {
    codedAssessments: true,
    showDxCodesInPrint: false,
    defaultNoteFormat: 'complete_hp'
};

// ── Immunization Schedule (CDC) ──
const CDC_SCHEDULE_VACCINES = [
    'DTaP', 'IPV', 'MMR', 'Varicella', 'Hepatitis A', 'Hepatitis B',
    'Hib', 'PCV', 'Rotavirus', 'Influenza', 'HPV', 'Meningococcal ACWY',
    'Meningococcal B', 'Tdap', 'Td', 'Pneumococcal', 'Zoster', 'COVID-19'
];
