const SEED_DATA_VERSION = 1;

const CURRENT_USER = {
    id: 'prov_001',
    name: 'Dr. Sarah Mitchell',
    credentials: 'MD',
    npi: '1548293067',
    specialty: 'Family Medicine',
    email: 'sarah.mitchell@westsidemedical.io',
    epcsEnabled: true,
    deaNumber: 'FM4829301',
    practice: 'Westside Family Medicine',
    avatarColor: '#1a73e8'
};

const CURRENT_PATIENT = {
    id: 'pat_001',
    firstName: 'James',
    lastName: 'Rodriguez',
    dob: '1978-05-14',
    age: 47,
    sex: 'Male',
    weightKg: 82.5,
    heightCm: 178,
    address: '2847 Sunset Blvd, San Francisco, CA 94116',
    phone: '(415) 555-0187',
    mobile: '(415) 555-9234',
    email: 'james.rodriguez78@gmail.com',
    preferredPharmacyId: 'pharm_001',
    secondaryPharmacyId: 'pharm_003',
    insurance: {
        planName: 'Blue Shield PPO Gold',
        memberId: 'BSC-9284710',
        groupNumber: 'GRP-44821',
        bin: '610014',
        pcn: 'MCAIDNR',
        pbm: 'Express Scripts',
        copayGeneric: 10,
        copayPreferred: 35,
        copayNonPreferred: 60,
        deductible: 500,
        deductibleMet: 325
    },
    allergies: [
        { id: 'alg_001', allergen: 'Penicillin', reaction: 'Rash, hives', severity: 'Moderate', type: 'drug', onsetDate: '2005-03-20', source: 'database' },
        { id: 'alg_002', allergen: 'Sulfonamides', reaction: 'Anaphylaxis', severity: 'Severe', type: 'drug', onsetDate: '2010-11-05', source: 'database' },
        { id: 'alg_003', allergen: 'Codeine', reaction: 'Nausea, vomiting', severity: 'Mild', type: 'drug', onsetDate: '2015-07-12', source: 'patient-reported' },
        { id: 'alg_004', allergen: 'Latex', reaction: 'Contact dermatitis', severity: 'Mild', type: 'environmental', onsetDate: '2018-01-30', source: 'patient-reported' }
    ],
    problems: [
        { id: 'prob_001', description: 'Essential hypertension', icd10: 'I10', status: 'active', onsetDate: '2019-03-15' },
        { id: 'prob_002', description: 'Type 2 diabetes mellitus without complications', icd10: 'E11.9', status: 'active', onsetDate: '2020-08-22' },
        { id: 'prob_003', description: 'Hyperlipidemia, unspecified', icd10: 'E78.5', status: 'active', onsetDate: '2019-06-10' },
        { id: 'prob_004', description: 'Gastroesophageal reflux disease', icd10: 'K21.0', status: 'active', onsetDate: '2021-02-14' },
        { id: 'prob_005', description: 'Generalized anxiety disorder', icd10: 'F41.1', status: 'active', onsetDate: '2022-05-03' },
        { id: 'prob_006', description: 'Chronic low back pain', icd10: 'M54.5', status: 'active', onsetDate: '2023-01-18' },
        { id: 'prob_007', description: 'Vitamin D deficiency', icd10: 'E55.9', status: 'active', onsetDate: '2021-11-20' },
        { id: 'prob_008', description: 'Obesity, unspecified', icd10: 'E66.9', status: 'active', onsetDate: '2020-08-22' }
    ],
    lastReconciledDate: '2026-01-15T14:30:00Z'
};

const PERMANENT_RX_MEDS = [
    {
        id: 'prx_001', medicationName: 'Lisinopril 10mg tablet', ndc: '68180-0513-01',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 3, refillsRemaining: 2, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2019-04-01', lastPrescribedDate: '2025-12-15',
        lastFilledDate: '2026-01-18', nextRefillDate: '2026-02-17',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_002', medicationName: 'Metformin 500mg tablet', ndc: '00228-2717-11',
        sig: 'Take 1 tablet by mouth twice daily with meals', qty: 60, unit: 'tablets',
        refills: 5, refillsRemaining: 3, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2020-09-10', lastPrescribedDate: '2025-11-20',
        lastFilledDate: '2026-01-22', nextRefillDate: '2026-02-21',
        diagnosis: [{ code: 'E11.9', description: 'Type 2 diabetes mellitus' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_003', medicationName: 'Atorvastatin 20mg tablet', ndc: '00071-0155-23',
        sig: 'Take 1 tablet by mouth at bedtime', qty: 30, unit: 'tablets',
        refills: 5, refillsRemaining: 4, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2019-07-15', lastPrescribedDate: '2025-12-15',
        lastFilledDate: '2026-01-20', nextRefillDate: '2026-02-19',
        diagnosis: [{ code: 'E78.5', description: 'Hyperlipidemia' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_004', medicationName: 'Omeprazole 20mg capsule', ndc: '62175-0116-37',
        sig: 'Take 1 capsule by mouth once daily before breakfast', qty: 30, unit: 'capsules',
        refills: 3, refillsRemaining: 1, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2021-03-01', lastPrescribedDate: '2025-10-08',
        lastFilledDate: '2026-01-10', nextRefillDate: '2026-02-09',
        diagnosis: [{ code: 'K21.0', description: 'GERD' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_005', medicationName: 'Sertraline 50mg tablet', ndc: '16714-0628-01',
        sig: 'Take 1 tablet by mouth once daily in the morning', qty: 30, unit: 'tablets',
        refills: 5, refillsRemaining: 5, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_003', pharmacyName: 'Walgreens #7892',
        startDate: '2022-06-01', lastPrescribedDate: '2026-01-05',
        lastFilledDate: '2026-01-08', nextRefillDate: '2026-02-07',
        diagnosis: [{ code: 'F41.1', description: 'Generalized anxiety disorder' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_006', medicationName: 'Amlodipine 5mg tablet', ndc: '00069-1520-68',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 3, refillsRemaining: 3, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2024-02-20', lastPrescribedDate: '2026-01-15',
        lastFilledDate: '2026-01-18', nextRefillDate: '2026-02-17',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_007', medicationName: 'Gabapentin 300mg capsule', ndc: '59762-5025-01',
        sig: 'Take 1 capsule by mouth three times daily', qty: 90, unit: 'capsules',
        refills: 2, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2023-03-10', lastPrescribedDate: '2025-09-15',
        lastFilledDate: '2025-12-20', nextRefillDate: '2026-01-19',
        diagnosis: [{ code: 'M54.5', description: 'Chronic low back pain' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_008', medicationName: 'Metoprolol Succinate ER 50mg tablet', ndc: '00378-1053-01',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 5, refillsRemaining: 2, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2024-01-05', lastPrescribedDate: '2025-11-20',
        lastFilledDate: '2026-01-25', nextRefillDate: '2026-02-24',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_009', medicationName: 'Losartan 50mg tablet', ndc: '00093-7367-56',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 3, refillsRemaining: 1, daysSupply: 30, dispenseAsWritten: true,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_002', prescriberName: 'Dr. Michael Chen',
        pharmacyId: 'pharm_003', pharmacyName: 'Walgreens #7892',
        startDate: '2025-06-15', lastPrescribedDate: '2025-12-10',
        lastFilledDate: '2026-01-12', nextRefillDate: '2026-02-11',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'prx_010', medicationName: 'Alprazolam 0.5mg tablet', ndc: '00009-0055-14',
        sig: 'Take 1 tablet by mouth twice daily as needed for anxiety', qty: 60, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2025-08-01', lastPrescribedDate: '2026-02-01',
        lastFilledDate: '2026-02-03', nextRefillDate: '2026-03-05',
        diagnosis: [{ code: 'F41.1', description: 'Generalized anxiety disorder' }],
        isControlled: true, scheduleClass: 'IV'
    },
    {
        id: 'prx_011', medicationName: 'Montelukast 10mg tablet', ndc: '00006-0275-31',
        sig: 'Take 1 tablet by mouth at bedtime', qty: 30, unit: 'tablets',
        refills: 5, refillsRemaining: 4, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_rx',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2025-04-20', lastPrescribedDate: '2025-11-15',
        lastFilledDate: '2026-01-17', nextRefillDate: '2026-02-16',
        diagnosis: [{ code: 'J45.20', description: 'Mild intermittent asthma' }],
        isControlled: false, scheduleClass: null
    }
];

const PERMANENT_OTC_MEDS = [
    {
        id: 'otc_001', medicationName: 'Vitamin D3 2000 IU tablet', ndc: null,
        sig: 'Take 1 tablet by mouth once daily', qty: 90, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 90, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_otc',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: null, pharmacyName: null,
        startDate: '2021-12-01', lastPrescribedDate: null,
        documentedDate: '2021-12-01',
        diagnosis: [{ code: 'E55.9', description: 'Vitamin D deficiency' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'otc_002', medicationName: 'Fish Oil 1000mg softgel', ndc: null,
        sig: 'Take 2 softgels by mouth once daily with food', qty: 120, unit: 'softgels',
        refills: 0, refillsRemaining: 0, daysSupply: 60, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_otc',
        prescriberId: null, prescriberName: null,
        pharmacyId: null, pharmacyName: null,
        startDate: '2022-03-15', lastPrescribedDate: null,
        documentedDate: '2022-03-15',
        diagnosis: [{ code: 'E78.5', description: 'Hyperlipidemia' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'otc_003', medicationName: 'Calcium 600mg + Vitamin D3 400 IU tablet', ndc: null,
        sig: 'Take 1 tablet by mouth twice daily', qty: 60, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_otc',
        prescriberId: null, prescriberName: null,
        pharmacyId: null, pharmacyName: null,
        startDate: '2023-01-10', lastPrescribedDate: null,
        documentedDate: '2023-01-10',
        diagnosis: [],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'otc_004', medicationName: 'Centrum Silver Multivitamin tablet', ndc: null,
        sig: 'Take 1 tablet by mouth once daily', qty: 90, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 90, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_otc',
        prescriberId: null, prescriberName: null,
        pharmacyId: null, pharmacyName: null,
        startDate: '2020-06-01', lastPrescribedDate: null,
        documentedDate: '2020-06-01',
        diagnosis: [],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'otc_005', medicationName: 'Melatonin 3mg tablet', ndc: null,
        sig: 'Take 1 tablet by mouth at bedtime as needed', qty: 60, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 60, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_otc',
        prescriberId: null, prescriberName: null,
        pharmacyId: null, pharmacyName: null,
        startDate: '2024-09-15', lastPrescribedDate: null,
        documentedDate: '2024-09-15',
        diagnosis: [],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'otc_006', medicationName: 'Aspirin 81mg tablet (low-dose)', ndc: null,
        sig: 'Take 1 tablet by mouth once daily', qty: 90, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 90, dispenseAsWritten: false,
        status: 'active', classification: 'permanent_otc',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: null, pharmacyName: null,
        startDate: '2020-10-01', lastPrescribedDate: null,
        documentedDate: '2020-10-01',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }],
        isControlled: false, scheduleClass: null
    }
];

const TEMPORARY_MEDS = [
    {
        id: 'tmp_001', medicationName: 'Amoxicillin 500mg capsule', ndc: '65862-0015-01',
        sig: 'Take 1 capsule by mouth three times daily for 10 days', qty: 30, unit: 'capsules',
        refills: 0, refillsRemaining: 0, daysSupply: 10, dispenseAsWritten: false,
        status: 'active', classification: 'temporary',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2026-02-20', lastPrescribedDate: '2026-02-20',
        lastFilledDate: '2026-02-21', nextRefillDate: null,
        diagnosis: [{ code: 'J01.90', description: 'Acute sinusitis, unspecified' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'tmp_002', medicationName: 'Prednisone 10mg tablet', ndc: '00054-4728-25',
        sig: 'Take as directed: 4 tabs day 1-2, 3 tabs day 3-4, 2 tabs day 5-6, 1 tab day 7', qty: 21, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 7, dispenseAsWritten: false,
        status: 'active', classification: 'temporary',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2026-02-20', lastPrescribedDate: '2026-02-20',
        lastFilledDate: '2026-02-21', nextRefillDate: null,
        diagnosis: [{ code: 'J01.90', description: 'Acute sinusitis, unspecified' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'tmp_003', medicationName: 'Ciprofloxacin 500mg tablet', ndc: '00093-0862-01',
        sig: 'Take 1 tablet by mouth twice daily for 7 days', qty: 14, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 7, dispenseAsWritten: false,
        status: 'active', classification: 'temporary',
        prescriberId: 'prov_003', prescriberName: 'Dr. Lisa Park',
        pharmacyId: 'pharm_005', pharmacyName: 'Rite Aid #3456',
        startDate: '2026-02-10', lastPrescribedDate: '2026-02-10',
        lastFilledDate: '2026-02-11', nextRefillDate: null,
        diagnosis: [{ code: 'N39.0', description: 'Urinary tract infection' }],
        isControlled: false, scheduleClass: null
    }
];

const DISCONTINUED_MEDS = [
    {
        id: 'disc_001', medicationName: 'Hydrochlorothiazide 25mg tablet', ndc: '00603-3856-21',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'discontinued', classification: 'discontinued',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2019-03-20', lastPrescribedDate: '2019-03-20',
        discontinuedDate: '2019-04-01', discontinuedBy: 'Dr. Sarah Mitchell',
        discontinueReason: 'I want to discontinue this medication',
        discontinueDetails: 'Switching to Lisinopril for better BP control',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'disc_002', medicationName: 'Citalopram 20mg tablet', ndc: '00093-3183-56',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'discontinued', classification: 'discontinued',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_003', pharmacyName: 'Walgreens #7892',
        startDate: '2021-11-01', lastPrescribedDate: '2022-04-15',
        discontinuedDate: '2022-05-30', discontinuedBy: 'Dr. Sarah Mitchell',
        discontinueReason: 'I want to discontinue this medication',
        discontinueDetails: 'Inadequate response, switching to Sertraline',
        diagnosis: [{ code: 'F41.1', description: 'Generalized anxiety disorder' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'disc_003', medicationName: 'Pantoprazole 40mg tablet', ndc: '00008-0841-81',
        sig: 'Take 1 tablet by mouth once daily before breakfast', qty: 30, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'discontinued', classification: 'discontinued',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2020-08-10', lastPrescribedDate: '2021-01-15',
        discontinuedDate: '2021-02-28', discontinuedBy: 'Dr. Sarah Mitchell',
        discontinueReason: 'I want to discontinue this medication',
        discontinueDetails: 'Switching to Omeprazole 20mg - adequate symptom control at lower cost',
        diagnosis: [{ code: 'K21.0', description: 'GERD' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'disc_004', medicationName: 'Naproxen 500mg tablet', ndc: '55111-0160-01',
        sig: 'Take 1 tablet by mouth twice daily with food', qty: 60, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'discontinued', classification: 'discontinued',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2023-01-18', lastPrescribedDate: '2023-01-18',
        discontinuedDate: '2023-03-15', discontinuedBy: 'James Rodriguez',
        discontinueReason: 'Patient stopped taking medication',
        discontinueDetails: 'Patient reports GI upset, switched to Gabapentin for chronic pain',
        diagnosis: [{ code: 'M54.5', description: 'Chronic low back pain' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'disc_005', medicationName: 'Glipizide 5mg tablet', ndc: '00093-1089-01',
        sig: 'Take 1 tablet by mouth once daily before breakfast', qty: 30, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'discontinued', classification: 'discontinued',
        prescriberId: 'prov_002', prescriberName: 'Dr. Michael Chen',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2020-09-10', lastPrescribedDate: '2021-06-01',
        discontinuedDate: '2021-08-15', discontinuedBy: 'Dr. Michael Chen',
        discontinueReason: 'Discontinued by another prescriber',
        discontinueDetails: 'A1c at goal with Metformin monotherapy, Glipizide no longer needed',
        diagnosis: [{ code: 'E11.9', description: 'Type 2 diabetes mellitus' }],
        isControlled: false, scheduleClass: null
    },
    {
        id: 'disc_006', medicationName: 'Tramadol 50mg tablet', ndc: '00093-0058-01',
        sig: 'Take 1 tablet by mouth every 6 hours as needed for pain', qty: 30, unit: 'tablets',
        refills: 0, refillsRemaining: 0, daysSupply: 30, dispenseAsWritten: false,
        status: 'discontinued', classification: 'discontinued',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        startDate: '2023-02-01', lastPrescribedDate: '2023-02-01',
        discontinuedDate: '2023-03-01', discontinuedBy: 'Dr. Sarah Mitchell',
        discontinueReason: 'I want to discontinue this medication',
        discontinueDetails: 'Transitioning to non-opioid pain management with Gabapentin',
        diagnosis: [{ code: 'M54.5', description: 'Chronic low back pain' }],
        isControlled: true, scheduleClass: 'IV'
    }
];

const CANCELED_SCRIPTS = [
    {
        id: 'cxl_001', medicationName: 'Azithromycin 250mg tablet', ndc: '00093-7169-56',
        sig: 'Take 2 tablets day 1, then 1 tablet daily for days 2-5', qty: 6, unit: 'tablets',
        refills: 0, daysSupply: 5,
        status: 'canceled', classification: 'canceled',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        prescribedDate: '2026-01-25', canceledDate: '2026-01-26',
        cancelReason: 'Wrong medication prescribed - patient has QT prolongation risk',
        diagnosis: [{ code: 'J06.9', description: 'Acute upper respiratory infection' }]
    },
    {
        id: 'cxl_002', medicationName: 'Lisinopril 20mg tablet', ndc: '68180-0514-01',
        sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets',
        refills: 3, daysSupply: 30,
        status: 'canceled', classification: 'canceled',
        prescriberId: 'prov_001', prescriberName: 'Dr. Sarah Mitchell',
        pharmacyId: 'pharm_003', pharmacyName: 'Walgreens #7892',
        prescribedDate: '2025-12-10', canceledDate: '2025-12-11',
        cancelReason: 'Dose increase not needed after reviewing home BP logs',
        diagnosis: [{ code: 'I10', description: 'Essential hypertension' }]
    }
];

const PHARMACIES = [
    { id: 'pharm_001', name: 'CVS Pharmacy #4521', address: '1234 Main St', city: 'San Francisco', state: 'CA', zip: '94110', phone: '(415) 555-0101', fax: '(415) 555-0102', storeNumber: '4521', epcs: true, acceptsECancel: true, type: 'retail' },
    { id: 'pharm_002', name: 'CVS Pharmacy #4533', address: '890 Market St', city: 'San Francisco', state: 'CA', zip: '94102', phone: '(415) 555-0201', fax: '(415) 555-0202', storeNumber: '4533', epcs: true, acceptsECancel: true, type: 'retail' },
    { id: 'pharm_003', name: 'Walgreens #7892', address: '456 Mission St', city: 'San Francisco', state: 'CA', zip: '94105', phone: '(415) 555-0301', fax: '(415) 555-0302', storeNumber: '7892', epcs: true, acceptsECancel: true, type: 'retail' },
    { id: 'pharm_004', name: 'Walgreens #7901', address: '2100 Irving St', city: 'San Francisco', state: 'CA', zip: '94122', phone: '(415) 555-0401', fax: '(415) 555-0402', storeNumber: '7901', epcs: false, acceptsECancel: true, type: 'retail' },
    { id: 'pharm_005', name: 'Rite Aid #3456', address: '789 Geary Blvd', city: 'San Francisco', state: 'CA', zip: '94109', phone: '(415) 555-0501', fax: '(415) 555-0502', storeNumber: '3456', epcs: true, acceptsECancel: false, type: 'retail' },
    { id: 'pharm_006', name: 'Costco Pharmacy #1142', address: '450 10th St', city: 'San Francisco', state: 'CA', zip: '94103', phone: '(415) 555-0601', fax: '(415) 555-0602', storeNumber: '1142', epcs: false, acceptsECancel: true, type: 'retail' },
    { id: 'pharm_007', name: 'Target Pharmacy (CVS) #5678', address: '789 Mission St', city: 'San Francisco', state: 'CA', zip: '94105', phone: '(415) 555-0701', fax: '(415) 555-0702', storeNumber: '5678', epcs: true, acceptsECancel: true, type: 'retail' },
    { id: 'pharm_008', name: 'Safeway Pharmacy #2891', address: '1335 Webster St', city: 'San Francisco', state: 'CA', zip: '94115', phone: '(415) 555-0801', fax: '(415) 555-0802', storeNumber: '2891', epcs: false, acceptsECancel: false, type: 'retail' },
    { id: 'pharm_009', name: 'Alto Pharmacy', address: '600 Townsend St', city: 'San Francisco', state: 'CA', zip: '94103', phone: '(415) 555-0901', fax: '(415) 555-0902', storeNumber: null, epcs: true, acceptsECancel: true, type: 'mail_order' },
    { id: 'pharm_010', name: 'Amazon Pharmacy', address: '410 Terry Ave N', city: 'Seattle', state: 'WA', zip: '98109', phone: '(855) 745-0298', fax: null, storeNumber: null, epcs: false, acceptsECancel: true, type: 'mail_order' },
    { id: 'pharm_011', name: 'Express Scripts Mail Pharmacy', address: '4600 N Hanley Rd', city: 'St. Louis', state: 'MO', zip: '63134', phone: '(800) 282-2881', fax: '(800) 837-0959', storeNumber: null, epcs: false, acceptsECancel: true, type: 'mail_order' },
    { id: 'pharm_012', name: 'UCSF Medical Center Pharmacy', address: '505 Parnassus Ave', city: 'San Francisco', state: 'CA', zip: '94143', phone: '(415) 555-1201', fax: '(415) 555-1202', storeNumber: null, epcs: true, acceptsECancel: true, type: 'hospital' },
    { id: 'pharm_013', name: 'Kaiser Permanente Pharmacy #4102', address: '2425 Geary Blvd', city: 'San Francisco', state: 'CA', zip: '94115', phone: '(415) 555-1301', fax: '(415) 555-1302', storeNumber: '4102', epcs: true, acceptsECancel: true, type: 'hospital' },
    { id: 'pharm_014', name: 'Good Neighbor Pharmacy - Marina', address: '3298 Scott St', city: 'San Francisco', state: 'CA', zip: '94123', phone: '(415) 555-1401', fax: '(415) 555-1402', storeNumber: null, epcs: false, acceptsECancel: false, type: 'independent' },
    { id: 'pharm_015', name: 'Jade Pharmacy', address: '1122 Stockton St', city: 'San Francisco', state: 'CA', zip: '94108', phone: '(415) 555-1501', fax: '(415) 555-1502', storeNumber: null, epcs: false, acceptsECancel: false, type: 'independent' }
];

const REFILL_REQUESTS = [
    {
        id: 'rr_001', type: 'refill', status: 'pending',
        medicationName: 'Lisinopril 10mg tablet', ndc: '68180-0513-01',
        patientMedId: 'prx_001',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-28T09:15:00Z',
        lastPrescription: { sig: 'Take 1 tablet by mouth once daily', qty: 30, refills: 3, prescribedDate: '2025-12-15' },
        lastDispensed: { date: '2026-01-18', qty: 30 },
        notes: ''
    },
    {
        id: 'rr_002', type: 'refill', status: 'pending',
        medicationName: 'Atorvastatin 20mg tablet', ndc: '00071-0155-23',
        patientMedId: 'prx_003',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-28T09:20:00Z',
        lastPrescription: { sig: 'Take 1 tablet by mouth at bedtime', qty: 30, refills: 5, prescribedDate: '2025-12-15' },
        lastDispensed: { date: '2026-01-20', qty: 30 },
        notes: ''
    },
    {
        id: 'rr_003', type: 'refill', status: 'pending',
        medicationName: 'Gabapentin 300mg capsule', ndc: '59762-5025-01',
        patientMedId: 'prx_007',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-27T14:30:00Z',
        lastPrescription: { sig: 'Take 1 capsule by mouth three times daily', qty: 90, refills: 2, prescribedDate: '2025-09-15' },
        lastDispensed: { date: '2025-12-20', qty: 90 },
        notes: 'Patient reports running low, needs refill urgently'
    },
    {
        id: 'rr_004', type: 'refill', status: 'pending',
        medicationName: 'Omeprazole 20mg capsule', ndc: '62175-0116-37',
        patientMedId: 'prx_004',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-26T11:00:00Z',
        lastPrescription: { sig: 'Take 1 capsule by mouth once daily before breakfast', qty: 30, refills: 3, prescribedDate: '2025-10-08' },
        lastDispensed: { date: '2026-01-10', qty: 30 },
        notes: ''
    },
    {
        id: 'rr_005', type: 'refill', status: 'approved',
        medicationName: 'Metformin 500mg tablet', ndc: '00228-2717-11',
        patientMedId: 'prx_002',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-25T16:45:00Z',
        lastPrescription: { sig: 'Take 1 tablet by mouth twice daily with meals', qty: 60, refills: 5, prescribedDate: '2025-11-20' },
        lastDispensed: { date: '2026-01-22', qty: 60 },
        notes: '', processedDate: '2026-02-25T17:00:00Z', processedBy: 'Dr. Sarah Mitchell'
    },
    {
        id: 'rr_006', type: 'refill', status: 'denied',
        medicationName: 'Tramadol 50mg tablet', ndc: '00093-0058-01',
        patientMedId: null,
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-24T10:30:00Z',
        lastPrescription: { sig: 'Take 1 tablet by mouth every 6 hours as needed for pain', qty: 30, refills: 0, prescribedDate: '2023-02-01' },
        lastDispensed: { date: '2023-02-02', qty: 30 },
        notes: '', processedDate: '2026-02-24T11:15:00Z', processedBy: 'Dr. Sarah Mitchell',
        denyReason: 'Medication has been discontinued. Patient is now on Gabapentin for pain management.'
    },
    {
        id: 'rr_007', type: 'refill', status: 'pending',
        medicationName: 'Sertraline 50mg tablet', ndc: '16714-0628-01',
        patientMedId: 'prx_005',
        pharmacyId: 'pharm_003', pharmacyName: 'Walgreens #7892',
        requestDate: '2026-03-01T08:00:00Z',
        lastPrescription: { sig: 'Take 1 tablet by mouth once daily in the morning', qty: 30, refills: 5, prescribedDate: '2026-01-05' },
        lastDispensed: { date: '2026-01-08', qty: 30 },
        notes: ''
    },
    {
        id: 'rr_008', type: 'refill', status: 'pending',
        medicationName: 'Metoprolol Succinate ER 50mg tablet', ndc: '00378-1053-01',
        patientMedId: 'prx_008',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-03-01T09:30:00Z',
        lastPrescription: { sig: 'Take 1 tablet by mouth once daily', qty: 30, refills: 5, prescribedDate: '2025-11-20' },
        lastDispensed: { date: '2026-01-25', qty: 30 },
        notes: ''
    }
];

const CHANGE_REQUESTS = [
    {
        id: 'cr_001', type: 'change', status: 'pending',
        medicationName: 'Atorvastatin 20mg tablet',
        originalMedication: 'Atorvastatin 20mg tablet',
        requestedMedication: 'Rosuvastatin 10mg tablet',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-28T15:00:00Z',
        reason: 'Generic substitution - Rosuvastatin is preferred on patient formulary',
        notes: 'Pharmacist recommends therapeutic substitution for cost savings'
    },
    {
        id: 'cr_002', type: 'change', status: 'pending',
        medicationName: 'Gabapentin 300mg capsule',
        originalMedication: 'Gabapentin 300mg capsule',
        requestedMedication: 'Gabapentin 300mg capsule',
        pharmacyId: 'pharm_001', pharmacyName: 'CVS Pharmacy #4521',
        requestDate: '2026-02-27T16:00:00Z',
        reason: 'Clarification - Please confirm if patient should take 1 capsule TID or 2 capsules BID',
        notes: ''
    }
];

const RX_TEMPLATES = [
    { id: 'tpl_001', medicationName: 'Lisinopril 10mg tablet', sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets', refills: 3, daysSupply: 30, ndc: '68180-0513-01', createdDate: '2024-01-15' },
    { id: 'tpl_002', medicationName: 'Lisinopril 20mg tablet', sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets', refills: 3, daysSupply: 30, ndc: '68180-0514-01', createdDate: '2024-01-15' },
    { id: 'tpl_003', medicationName: 'Metformin 500mg tablet', sig: 'Take 1 tablet by mouth twice daily with meals', qty: 60, unit: 'tablets', refills: 5, daysSupply: 30, ndc: '00228-2717-11', createdDate: '2024-01-15' },
    { id: 'tpl_004', medicationName: 'Metformin 1000mg tablet', sig: 'Take 1 tablet by mouth twice daily with meals', qty: 60, unit: 'tablets', refills: 5, daysSupply: 30, ndc: '00228-2719-11', createdDate: '2024-02-20' },
    { id: 'tpl_005', medicationName: 'Atorvastatin 20mg tablet', sig: 'Take 1 tablet by mouth at bedtime', qty: 30, unit: 'tablets', refills: 5, daysSupply: 30, ndc: '00071-0155-23', createdDate: '2024-01-15' },
    { id: 'tpl_006', medicationName: 'Atorvastatin 40mg tablet', sig: 'Take 1 tablet by mouth at bedtime', qty: 30, unit: 'tablets', refills: 5, daysSupply: 30, ndc: '00071-0156-23', createdDate: '2024-03-10' },
    { id: 'tpl_007', medicationName: 'Omeprazole 20mg capsule', sig: 'Take 1 capsule by mouth once daily before breakfast', qty: 30, unit: 'capsules', refills: 3, daysSupply: 30, ndc: '62175-0116-37', createdDate: '2024-01-20' },
    { id: 'tpl_008', medicationName: 'Amoxicillin 500mg capsule', sig: 'Take 1 capsule by mouth three times daily for 10 days', qty: 30, unit: 'capsules', refills: 0, daysSupply: 10, ndc: '65862-0015-01', createdDate: '2024-02-05' },
    { id: 'tpl_009', medicationName: 'Azithromycin 250mg tablet (Z-Pack)', sig: 'Take 2 tablets day 1, then 1 tablet daily for days 2-5', qty: 6, unit: 'tablets', refills: 0, daysSupply: 5, ndc: '00093-7169-56', createdDate: '2024-02-05' },
    { id: 'tpl_010', medicationName: 'Prednisone 10mg tablet (taper)', sig: 'Take as directed: 4 tabs day 1-2, 3 tabs day 3-4, 2 tabs day 5-6, 1 tab day 7', qty: 21, unit: 'tablets', refills: 0, daysSupply: 7, ndc: '00054-4728-25', createdDate: '2024-02-05' },
    { id: 'tpl_011', medicationName: 'Sertraline 50mg tablet', sig: 'Take 1 tablet by mouth once daily in the morning', qty: 30, unit: 'tablets', refills: 5, daysSupply: 30, ndc: '16714-0628-01', createdDate: '2024-04-15' },
    { id: 'tpl_012', medicationName: 'Amlodipine 5mg tablet', sig: 'Take 1 tablet by mouth once daily', qty: 30, unit: 'tablets', refills: 3, daysSupply: 30, ndc: '00069-1520-68', createdDate: '2024-05-01' }
];

const CUSTOM_SIGS = [
    { id: 'sig_001', text: 'Take 1 tablet by mouth once daily', category: 'oral' },
    { id: 'sig_002', text: 'Take 1 tablet by mouth twice daily', category: 'oral' },
    { id: 'sig_003', text: 'Take 1 tablet by mouth three times daily', category: 'oral' },
    { id: 'sig_004', text: 'Take 1 tablet by mouth at bedtime', category: 'oral' },
    { id: 'sig_005', text: 'Take 1 tablet by mouth once daily in the morning', category: 'oral' },
    { id: 'sig_006', text: 'Take 1 tablet by mouth once daily with food', category: 'oral' },
    { id: 'sig_007', text: 'Take 1 tablet by mouth twice daily with meals', category: 'oral' },
    { id: 'sig_008', text: 'Take 1 capsule by mouth once daily', category: 'oral' },
    { id: 'sig_009', text: 'Take 1 capsule by mouth twice daily', category: 'oral' },
    { id: 'sig_010', text: 'Take 1 capsule by mouth three times daily', category: 'oral' },
    { id: 'sig_011', text: 'Take 1 capsule by mouth once daily before breakfast', category: 'oral' },
    { id: 'sig_012', text: 'Take 2 tablets by mouth once daily', category: 'oral' },
    { id: 'sig_013', text: 'Take 1 tablet by mouth every 4-6 hours as needed for pain', category: 'prn' },
    { id: 'sig_014', text: 'Take 1 tablet by mouth every 6 hours as needed for pain', category: 'prn' },
    { id: 'sig_015', text: 'Take 1 tablet by mouth every 8 hours as needed', category: 'prn' },
    { id: 'sig_016', text: 'Take 1 tablet by mouth once daily as needed', category: 'prn' },
    { id: 'sig_017', text: 'Apply topically to affected area twice daily', category: 'topical' },
    { id: 'sig_018', text: 'Apply thin layer to affected area once daily at bedtime', category: 'topical' },
    { id: 'sig_019', text: 'Instill 1 drop in affected eye(s) twice daily', category: 'ophthalmic' },
    { id: 'sig_020', text: 'Inhale 1-2 puffs every 4-6 hours as needed', category: 'inhalation' },
    { id: 'sig_021', text: 'Inhale 2 puffs twice daily', category: 'inhalation' },
    { id: 'sig_022', text: 'Inject subcutaneously once weekly', category: 'injectable' },
    { id: 'sig_023', text: 'Take 1 tablet by mouth once daily on empty stomach', category: 'oral' },
    { id: 'sig_024', text: 'Dissolve 1 tablet under the tongue as needed', category: 'sublingual' }
];

const MEDICATION_DATABASE = [
    { id: 'mdb_001', name: 'Lisinopril', strengths: ['2.5mg', '5mg', '10mg', '20mg', '40mg'], form: 'tablet', type: 'Rx', drugClass: 'ACE Inhibitor', generic: true },
    { id: 'mdb_002', name: 'Metformin', strengths: ['500mg', '850mg', '1000mg'], form: 'tablet', type: 'Rx', drugClass: 'Biguanide', generic: true },
    { id: 'mdb_003', name: 'Metformin ER', strengths: ['500mg', '750mg', '1000mg'], form: 'tablet', type: 'Rx', drugClass: 'Biguanide', generic: true },
    { id: 'mdb_004', name: 'Atorvastatin', strengths: ['10mg', '20mg', '40mg', '80mg'], form: 'tablet', type: 'Rx', drugClass: 'HMG-CoA Reductase Inhibitor', generic: true },
    { id: 'mdb_005', name: 'Rosuvastatin', strengths: ['5mg', '10mg', '20mg', '40mg'], form: 'tablet', type: 'Rx', drugClass: 'HMG-CoA Reductase Inhibitor', generic: true },
    { id: 'mdb_006', name: 'Omeprazole', strengths: ['10mg', '20mg', '40mg'], form: 'capsule', type: 'Rx', drugClass: 'Proton Pump Inhibitor', generic: true },
    { id: 'mdb_007', name: 'Pantoprazole', strengths: ['20mg', '40mg'], form: 'tablet', type: 'Rx', drugClass: 'Proton Pump Inhibitor', generic: true },
    { id: 'mdb_008', name: 'Amlodipine', strengths: ['2.5mg', '5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Calcium Channel Blocker', generic: true },
    { id: 'mdb_009', name: 'Losartan', strengths: ['25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'ARB', generic: true },
    { id: 'mdb_010', name: 'Metoprolol Tartrate', strengths: ['25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'Beta Blocker', generic: true },
    { id: 'mdb_011', name: 'Metoprolol Succinate ER', strengths: ['25mg', '50mg', '100mg', '200mg'], form: 'tablet', type: 'Rx', drugClass: 'Beta Blocker', generic: true },
    { id: 'mdb_012', name: 'Sertraline', strengths: ['25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'SSRI', generic: true },
    { id: 'mdb_013', name: 'Escitalopram', strengths: ['5mg', '10mg', '20mg'], form: 'tablet', type: 'Rx', drugClass: 'SSRI', generic: true },
    { id: 'mdb_014', name: 'Fluoxetine', strengths: ['10mg', '20mg', '40mg'], form: 'capsule', type: 'Rx', drugClass: 'SSRI', generic: true },
    { id: 'mdb_015', name: 'Gabapentin', strengths: ['100mg', '300mg', '400mg', '600mg', '800mg'], form: 'capsule', type: 'Rx', drugClass: 'Anticonvulsant', generic: true },
    { id: 'mdb_016', name: 'Pregabalin', strengths: ['25mg', '50mg', '75mg', '100mg', '150mg', '200mg', '300mg'], form: 'capsule', type: 'Rx', drugClass: 'Anticonvulsant', generic: true },
    { id: 'mdb_017', name: 'Hydrochlorothiazide', strengths: ['12.5mg', '25mg', '50mg'], form: 'tablet', type: 'Rx', drugClass: 'Thiazide Diuretic', generic: true },
    { id: 'mdb_018', name: 'Furosemide', strengths: ['20mg', '40mg', '80mg'], form: 'tablet', type: 'Rx', drugClass: 'Loop Diuretic', generic: true },
    { id: 'mdb_019', name: 'Amoxicillin', strengths: ['250mg', '500mg', '875mg'], form: 'capsule', type: 'Rx', drugClass: 'Penicillin Antibiotic', generic: true },
    { id: 'mdb_020', name: 'Amoxicillin-Clavulanate', strengths: ['500mg/125mg', '875mg/125mg'], form: 'tablet', type: 'Rx', drugClass: 'Penicillin Antibiotic', generic: true },
    { id: 'mdb_021', name: 'Azithromycin', strengths: ['250mg', '500mg'], form: 'tablet', type: 'Rx', drugClass: 'Macrolide Antibiotic', generic: true },
    { id: 'mdb_022', name: 'Ciprofloxacin', strengths: ['250mg', '500mg', '750mg'], form: 'tablet', type: 'Rx', drugClass: 'Fluoroquinolone', generic: true },
    { id: 'mdb_023', name: 'Doxycycline', strengths: ['50mg', '100mg'], form: 'capsule', type: 'Rx', drugClass: 'Tetracycline', generic: true },
    { id: 'mdb_024', name: 'Cephalexin', strengths: ['250mg', '500mg'], form: 'capsule', type: 'Rx', drugClass: 'Cephalosporin', generic: true },
    { id: 'mdb_025', name: 'Prednisone', strengths: ['1mg', '2.5mg', '5mg', '10mg', '20mg', '50mg'], form: 'tablet', type: 'Rx', drugClass: 'Corticosteroid', generic: true },
    { id: 'mdb_026', name: 'Methylprednisolone', strengths: ['4mg'], form: 'tablet (dose pack)', type: 'Rx', drugClass: 'Corticosteroid', generic: true },
    { id: 'mdb_027', name: 'Levothyroxine', strengths: ['25mcg', '50mcg', '75mcg', '88mcg', '100mcg', '112mcg', '125mcg', '137mcg', '150mcg', '175mcg', '200mcg'], form: 'tablet', type: 'Rx', drugClass: 'Thyroid Hormone', generic: true },
    { id: 'mdb_028', name: 'Albuterol', strengths: ['90mcg/actuation'], form: 'inhaler', type: 'Rx', drugClass: 'Beta-2 Agonist', generic: true },
    { id: 'mdb_029', name: 'Montelukast', strengths: ['4mg', '5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Leukotriene Modifier', generic: true },
    { id: 'mdb_030', name: 'Fluticasone', strengths: ['50mcg/actuation'], form: 'nasal spray', type: 'Rx', drugClass: 'Corticosteroid', generic: true },
    { id: 'mdb_031', name: 'Cetirizine', strengths: ['5mg', '10mg'], form: 'tablet', type: 'OTC', drugClass: 'Antihistamine', generic: true },
    { id: 'mdb_032', name: 'Loratadine', strengths: ['10mg'], form: 'tablet', type: 'OTC', drugClass: 'Antihistamine', generic: true },
    { id: 'mdb_033', name: 'Ibuprofen', strengths: ['200mg', '400mg', '600mg', '800mg'], form: 'tablet', type: 'OTC', drugClass: 'NSAID', generic: true },
    { id: 'mdb_034', name: 'Naproxen', strengths: ['220mg', '250mg', '375mg', '500mg'], form: 'tablet', type: 'OTC', drugClass: 'NSAID', generic: true },
    { id: 'mdb_035', name: 'Acetaminophen', strengths: ['325mg', '500mg', '650mg'], form: 'tablet', type: 'OTC', drugClass: 'Analgesic', generic: true },
    { id: 'mdb_036', name: 'Cyclobenzaprine', strengths: ['5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Muscle Relaxant', generic: true },
    { id: 'mdb_037', name: 'Tizanidine', strengths: ['2mg', '4mg'], form: 'tablet', type: 'Rx', drugClass: 'Muscle Relaxant', generic: true },
    { id: 'mdb_038', name: 'Warfarin', strengths: ['1mg', '2mg', '2.5mg', '3mg', '4mg', '5mg', '6mg', '7.5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Anticoagulant', generic: true },
    { id: 'mdb_039', name: 'Apixaban', strengths: ['2.5mg', '5mg'], form: 'tablet', type: 'Rx', drugClass: 'Anticoagulant', generic: false },
    { id: 'mdb_040', name: 'Clopidogrel', strengths: ['75mg'], form: 'tablet', type: 'Rx', drugClass: 'Antiplatelet', generic: true },
    { id: 'mdb_041', name: 'Alprazolam', strengths: ['0.25mg', '0.5mg', '1mg', '2mg'], form: 'tablet', type: 'Rx', drugClass: 'Benzodiazepine', generic: true, controlled: true, schedule: 'IV' },
    { id: 'mdb_042', name: 'Lorazepam', strengths: ['0.5mg', '1mg', '2mg'], form: 'tablet', type: 'Rx', drugClass: 'Benzodiazepine', generic: true, controlled: true, schedule: 'IV' },
    { id: 'mdb_043', name: 'Diazepam', strengths: ['2mg', '5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Benzodiazepine', generic: true, controlled: true, schedule: 'IV' },
    { id: 'mdb_044', name: 'Zolpidem', strengths: ['5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Sedative-Hypnotic', generic: true, controlled: true, schedule: 'IV' },
    { id: 'mdb_045', name: 'Tramadol', strengths: ['50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'Opioid Analgesic', generic: true, controlled: true, schedule: 'IV' },
    { id: 'mdb_046', name: 'Hydrocodone-Acetaminophen', strengths: ['5mg/325mg', '7.5mg/325mg', '10mg/325mg'], form: 'tablet', type: 'Rx', drugClass: 'Opioid Analgesic', generic: true, controlled: true, schedule: 'II' },
    { id: 'mdb_047', name: 'Oxycodone', strengths: ['5mg', '10mg', '15mg', '20mg', '30mg'], form: 'tablet', type: 'Rx', drugClass: 'Opioid Analgesic', generic: true, controlled: true, schedule: 'II' },
    { id: 'mdb_048', name: 'Morphine Sulfate', strengths: ['15mg', '30mg'], form: 'tablet', type: 'Rx', drugClass: 'Opioid Analgesic', generic: true, controlled: true, schedule: 'II' },
    { id: 'mdb_049', name: 'Adderall', strengths: ['5mg', '10mg', '15mg', '20mg', '25mg', '30mg'], form: 'tablet', type: 'Rx', drugClass: 'CNS Stimulant', generic: false, controlled: true, schedule: 'II' },
    { id: 'mdb_050', name: 'Methylphenidate', strengths: ['5mg', '10mg', '20mg'], form: 'tablet', type: 'Rx', drugClass: 'CNS Stimulant', generic: true, controlled: true, schedule: 'II' },
    { id: 'mdb_051', name: 'Insulin Glargine (Lantus)', strengths: ['100 units/mL'], form: 'injection', type: 'Rx', drugClass: 'Insulin', generic: false },
    { id: 'mdb_052', name: 'Insulin Lispro (Humalog)', strengths: ['100 units/mL'], form: 'injection', type: 'Rx', drugClass: 'Insulin', generic: false },
    { id: 'mdb_053', name: 'Glipizide', strengths: ['5mg', '10mg'], form: 'tablet', type: 'Rx', drugClass: 'Sulfonylurea', generic: true },
    { id: 'mdb_054', name: 'Pioglitazone', strengths: ['15mg', '30mg', '45mg'], form: 'tablet', type: 'Rx', drugClass: 'Thiazolidinedione', generic: true },
    { id: 'mdb_055', name: 'Empagliflozin', strengths: ['10mg', '25mg'], form: 'tablet', type: 'Rx', drugClass: 'SGLT2 Inhibitor', generic: false },
    { id: 'mdb_056', name: 'Sitagliptin', strengths: ['25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'DPP-4 Inhibitor', generic: false },
    { id: 'mdb_057', name: 'Semaglutide (Ozempic)', strengths: ['0.25mg', '0.5mg', '1mg', '2mg'], form: 'injection', type: 'Rx', drugClass: 'GLP-1 Agonist', generic: false },
    { id: 'mdb_058', name: 'Liraglutide (Victoza)', strengths: ['6mg/mL'], form: 'injection', type: 'Rx', drugClass: 'GLP-1 Agonist', generic: false },
    { id: 'mdb_059', name: 'Duloxetine', strengths: ['20mg', '30mg', '60mg'], form: 'capsule', type: 'Rx', drugClass: 'SNRI', generic: true },
    { id: 'mdb_060', name: 'Venlafaxine ER', strengths: ['37.5mg', '75mg', '150mg'], form: 'capsule', type: 'Rx', drugClass: 'SNRI', generic: true },
    { id: 'mdb_061', name: 'Bupropion XL', strengths: ['150mg', '300mg'], form: 'tablet', type: 'Rx', drugClass: 'NDRI', generic: true },
    { id: 'mdb_062', name: 'Trazodone', strengths: ['50mg', '100mg', '150mg'], form: 'tablet', type: 'Rx', drugClass: 'Serotonin Modulator', generic: true },
    { id: 'mdb_063', name: 'Buspirone', strengths: ['5mg', '10mg', '15mg'], form: 'tablet', type: 'Rx', drugClass: 'Anxiolytic', generic: true },
    { id: 'mdb_064', name: 'Hydroxyzine', strengths: ['10mg', '25mg', '50mg'], form: 'tablet', type: 'Rx', drugClass: 'Anxiolytic/Antihistamine', generic: true },
    { id: 'mdb_065', name: 'Tamsulosin', strengths: ['0.4mg'], form: 'capsule', type: 'Rx', drugClass: 'Alpha Blocker', generic: true },
    { id: 'mdb_066', name: 'Finasteride', strengths: ['1mg', '5mg'], form: 'tablet', type: 'Rx', drugClass: '5-Alpha Reductase Inhibitor', generic: true },
    { id: 'mdb_067', name: 'Sildenafil', strengths: ['20mg', '25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'PDE5 Inhibitor', generic: true },
    { id: 'mdb_068', name: 'Latanoprost', strengths: ['0.005%'], form: 'eye drops', type: 'Rx', drugClass: 'Prostaglandin Analog', generic: true },
    { id: 'mdb_069', name: 'Timolol', strengths: ['0.25%', '0.5%'], form: 'eye drops', type: 'Rx', drugClass: 'Beta Blocker (Ophthalmic)', generic: true },
    { id: 'mdb_070', name: 'Mupirocin', strengths: ['2%'], form: 'ointment', type: 'Rx', drugClass: 'Topical Antibiotic', generic: true },
    { id: 'mdb_071', name: 'Triamcinolone', strengths: ['0.025%', '0.1%', '0.5%'], form: 'cream', type: 'Rx', drugClass: 'Topical Corticosteroid', generic: true },
    { id: 'mdb_072', name: 'Clobetasol', strengths: ['0.05%'], form: 'cream', type: 'Rx', drugClass: 'Topical Corticosteroid', generic: true },
    { id: 'mdb_073', name: 'Spironolactone', strengths: ['25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'Potassium-Sparing Diuretic', generic: true },
    { id: 'mdb_074', name: 'Carvedilol', strengths: ['3.125mg', '6.25mg', '12.5mg', '25mg'], form: 'tablet', type: 'Rx', drugClass: 'Alpha/Beta Blocker', generic: true },
    { id: 'mdb_075', name: 'Diltiazem ER', strengths: ['120mg', '180mg', '240mg', '300mg', '360mg'], form: 'capsule', type: 'Rx', drugClass: 'Calcium Channel Blocker', generic: true },
    { id: 'mdb_076', name: 'Valsartan', strengths: ['40mg', '80mg', '160mg', '320mg'], form: 'tablet', type: 'Rx', drugClass: 'ARB', generic: true },
    { id: 'mdb_077', name: 'Benazepril', strengths: ['5mg', '10mg', '20mg', '40mg'], form: 'tablet', type: 'Rx', drugClass: 'ACE Inhibitor', generic: true },
    { id: 'mdb_078', name: 'Clonidine', strengths: ['0.1mg', '0.2mg', '0.3mg'], form: 'tablet', type: 'Rx', drugClass: 'Central Alpha Agonist', generic: true },
    { id: 'mdb_079', name: 'Allopurinol', strengths: ['100mg', '300mg'], form: 'tablet', type: 'Rx', drugClass: 'Xanthine Oxidase Inhibitor', generic: true },
    { id: 'mdb_080', name: 'Colchicine', strengths: ['0.6mg'], form: 'tablet', type: 'Rx', drugClass: 'Anti-Gout', generic: true },
    { id: 'mdb_081', name: 'Methotrexate', strengths: ['2.5mg'], form: 'tablet', type: 'Rx', drugClass: 'DMARD', generic: true },
    { id: 'mdb_082', name: 'Ondansetron', strengths: ['4mg', '8mg'], form: 'tablet', type: 'Rx', drugClass: 'Antiemetic', generic: true },
    { id: 'mdb_083', name: 'Promethazine', strengths: ['12.5mg', '25mg', '50mg'], form: 'tablet', type: 'Rx', drugClass: 'Antiemetic/Antihistamine', generic: true },
    { id: 'mdb_084', name: 'Ranitidine', strengths: ['150mg', '300mg'], form: 'tablet', type: 'Rx', drugClass: 'H2 Blocker', generic: true },
    { id: 'mdb_085', name: 'Famotidine', strengths: ['20mg', '40mg'], form: 'tablet', type: 'Rx', drugClass: 'H2 Blocker', generic: true },
    { id: 'mdb_086', name: 'Sumatriptan', strengths: ['25mg', '50mg', '100mg'], form: 'tablet', type: 'Rx', drugClass: 'Triptan', generic: true },
    { id: 'mdb_087', name: 'Topiramate', strengths: ['25mg', '50mg', '100mg', '200mg'], form: 'tablet', type: 'Rx', drugClass: 'Anticonvulsant', generic: true },
    { id: 'mdb_088', name: 'Lamotrigine', strengths: ['25mg', '100mg', '150mg', '200mg'], form: 'tablet', type: 'Rx', drugClass: 'Anticonvulsant', generic: true },
    { id: 'mdb_089', name: 'Valacyclovir', strengths: ['500mg', '1000mg'], form: 'tablet', type: 'Rx', drugClass: 'Antiviral', generic: true },
    { id: 'mdb_090', name: 'Acyclovir', strengths: ['200mg', '400mg', '800mg'], form: 'capsule', type: 'Rx', drugClass: 'Antiviral', generic: true },
    { id: 'mdb_091', name: 'Fluconazole', strengths: ['50mg', '100mg', '150mg', '200mg'], form: 'tablet', type: 'Rx', drugClass: 'Antifungal', generic: true },
    { id: 'mdb_092', name: 'Nitrofurantoin', strengths: ['50mg', '100mg'], form: 'capsule', type: 'Rx', drugClass: 'Urinary Antibiotic', generic: true },
    { id: 'mdb_093', name: 'Trimethoprim-Sulfamethoxazole', strengths: ['400mg/80mg', '800mg/160mg'], form: 'tablet', type: 'Rx', drugClass: 'Sulfonamide Antibiotic', generic: true },
    { id: 'mdb_094', name: 'Metronidazole', strengths: ['250mg', '500mg'], form: 'tablet', type: 'Rx', drugClass: 'Nitroimidazole Antibiotic', generic: true },
    { id: 'mdb_095', name: 'Clindamycin', strengths: ['150mg', '300mg'], form: 'capsule', type: 'Rx', drugClass: 'Lincosamide Antibiotic', generic: true }
];

const DRUG_INTERACTIONS = [
    { id: 'di_001', drug1: 'Lisinopril', drug2: 'Losartan', severity: 'major', description: 'Concurrent use of ACE inhibitors and ARBs increases risk of hyperkalemia, hypotension, and renal impairment. Dual RAAS blockade is generally not recommended.', recommendation: 'Avoid combination. Use one agent or the other for blood pressure control.' },
    { id: 'di_002', drug1: 'Sertraline', drug2: 'Tramadol', severity: 'major', description: 'Combined serotonergic agents increase risk of serotonin syndrome. Symptoms may include agitation, confusion, rapid heart rate, and muscle rigidity.', recommendation: 'Avoid combination if possible. If used together, monitor closely for serotonin syndrome symptoms.' },
    { id: 'di_003', drug1: 'Metformin', drug2: 'Contrast Dye', severity: 'major', description: 'Iodinated contrast media may cause acute kidney injury, increasing risk of metformin-associated lactic acidosis.', recommendation: 'Hold Metformin 48 hours before and after contrast procedures. Check renal function before restarting.' },
    { id: 'di_004', drug1: 'Warfarin', drug2: 'Aspirin', severity: 'major', description: 'Increased risk of bleeding when anticoagulants are used with antiplatelet agents.', recommendation: 'If combination necessary, monitor INR more frequently and watch for signs of bleeding.' },
    { id: 'di_005', drug1: 'Atorvastatin', drug2: 'Gemfibrozil', severity: 'major', description: 'Increased risk of myopathy and rhabdomyolysis when statins are combined with fibrates.', recommendation: 'If lipid-lowering combination needed, consider fenofibrate instead of gemfibrozil.' },
    { id: 'di_006', drug1: 'Gabapentin', drug2: 'Alprazolam', severity: 'moderate', description: 'Concurrent CNS depressants may cause additive sedation, respiratory depression, and impaired psychomotor function.', recommendation: 'Use lowest effective doses. Counsel patient about increased drowsiness and impaired coordination.' },
    { id: 'di_007', drug1: 'Omeprazole', drug2: 'Clopidogrel', severity: 'moderate', description: 'Omeprazole may reduce the antiplatelet effect of clopidogrel by inhibiting CYP2C19 metabolism.', recommendation: 'Consider pantoprazole as alternative PPI. Monitor for reduced antiplatelet efficacy.' },
    { id: 'di_008', drug1: 'Metformin', drug2: 'Alcohol', severity: 'moderate', description: 'Alcohol potentiates the effect of metformin on lactate metabolism, increasing risk of lactic acidosis.', recommendation: 'Advise patient to limit alcohol consumption. Monitor for symptoms of lactic acidosis.' },
    { id: 'di_009', drug1: 'Sertraline', drug2: 'Alprazolam', severity: 'moderate', description: 'SSRIs may increase plasma levels of benzodiazepines metabolized by CYP3A4, potentially increasing sedation.', recommendation: 'Monitor for increased sedation. Consider dose adjustment of alprazolam if needed.' },
    { id: 'di_010', drug1: 'Lisinopril', drug2: 'Spironolactone', severity: 'moderate', description: 'Concurrent ACE inhibitor and potassium-sparing diuretic use increases risk of hyperkalemia.', recommendation: 'Monitor potassium levels regularly. Consider starting with low dose of spironolactone.' },
    { id: 'di_011', drug1: 'Amlodipine', drug2: 'Simvastatin', severity: 'moderate', description: 'Amlodipine may increase simvastatin levels, increasing risk of myopathy.', recommendation: 'Limit simvastatin dose to 20mg daily when combined with amlodipine.' },
    { id: 'di_012', drug1: 'Metoprolol', drug2: 'Amlodipine', severity: 'minor', description: 'Combined calcium channel blocker and beta blocker may cause additive bradycardia and hypotension.', recommendation: 'Combination is commonly used and generally safe. Monitor heart rate and blood pressure.' },
    { id: 'di_013', drug1: 'Sertraline', drug2: 'Ibuprofen', severity: 'minor', description: 'SSRIs combined with NSAIDs may increase risk of GI bleeding.', recommendation: 'Consider gastroprotective agent if long-term combination needed.' },
    { id: 'di_014', drug1: 'Omeprazole', drug2: 'Calcium', severity: 'minor', description: 'Long-term PPI use may reduce calcium absorption, potentially increasing fracture risk.', recommendation: 'Ensure adequate calcium and vitamin D supplementation. Consider periodic bone density assessment.' },
    { id: 'di_015', drug1: 'Levothyroxine', drug2: 'Calcium', severity: 'moderate', description: 'Calcium supplements may decrease levothyroxine absorption if taken concurrently.', recommendation: 'Separate administration by at least 4 hours. Take levothyroxine on empty stomach.' }
];

const FORMULARY_DATA = {
    'Lisinopril 10mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Metformin 500mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Atorvastatin 20mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Omeprazole 20mg capsule': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Sertraline 50mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Amlodipine 5mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Gabapentin 300mg capsule': { status: 'on_formulary', tier: 2, copay: 35, requiresPA: false, alternatives: ['Pregabalin 75mg capsule'] },
    'Metoprolol Succinate ER 50mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Losartan 50mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Alprazolam 0.5mg tablet': { status: 'on_formulary', tier: 2, copay: 35, requiresPA: false, alternatives: [] },
    'Montelukast 10mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Rosuvastatin 10mg tablet': { status: 'preferred', tier: 1, copay: 10, requiresPA: false, alternatives: [] },
    'Pregabalin 75mg capsule': { status: 'non_formulary', tier: 3, copay: 60, requiresPA: true, alternatives: ['Gabapentin 300mg capsule'] },
    'Empagliflozin 10mg tablet': { status: 'non_formulary', tier: 3, copay: 60, requiresPA: true, alternatives: ['Metformin 500mg tablet', 'Glipizide 5mg tablet'] },
    'Semaglutide (Ozempic) 1mg injection': { status: 'non_reimbursable', tier: null, copay: null, requiresPA: true, alternatives: ['Liraglutide (Victoza) 6mg/mL injection'] }
};

const SETTINGS = {
    drugDecisionSupport: {
        drugToDrugLevel: 'all',
        drugToAllergyEnabled: true
    },
    defaultPharmacyId: 'pharm_001',
    autoPopulateLastPharmacy: true,
    prescriptionPrintFormat: 'standard',
    showCostEstimates: true,
    showFormularyData: true,
    epcsTokenType: 'vip_access_app'
};

const PROVIDERS = [
    { id: 'prov_001', name: 'Dr. Sarah Mitchell', credentials: 'MD', specialty: 'Family Medicine', npi: '1548293067' },
    { id: 'prov_002', name: 'Dr. Michael Chen', credentials: 'MD', specialty: 'Internal Medicine', npi: '1629384051' },
    { id: 'prov_003', name: 'Dr. Lisa Park', credentials: 'DO', specialty: 'Urgent Care', npi: '1730495162' },
    { id: 'prov_004', name: 'Dr. Robert Kim', credentials: 'MD', specialty: 'Cardiology', npi: '1841506273' },
    { id: 'prov_005', name: 'Dr. Emily Watson', credentials: 'MD', specialty: 'Endocrinology', npi: '1952617384' },
    { id: 'prov_006', name: 'Maria Santos', credentials: 'NP', specialty: 'Family Medicine', npi: '1063728495' },
    { id: 'prov_007', name: 'David Thompson', credentials: 'PA-C', specialty: 'Family Medicine', npi: '1174839506' }
];

const DIAGNOSIS_CODES = [
    { code: 'I10', description: 'Essential hypertension' },
    { code: 'E11.9', description: 'Type 2 diabetes mellitus without complications' },
    { code: 'E78.5', description: 'Hyperlipidemia, unspecified' },
    { code: 'K21.0', description: 'Gastroesophageal reflux disease' },
    { code: 'F41.1', description: 'Generalized anxiety disorder' },
    { code: 'M54.5', description: 'Chronic low back pain' },
    { code: 'E55.9', description: 'Vitamin D deficiency' },
    { code: 'E66.9', description: 'Obesity, unspecified' },
    { code: 'J45.20', description: 'Mild intermittent asthma' },
    { code: 'J06.9', description: 'Acute upper respiratory infection' },
    { code: 'J01.90', description: 'Acute sinusitis, unspecified' },
    { code: 'N39.0', description: 'Urinary tract infection' },
    { code: 'J20.9', description: 'Acute bronchitis, unspecified' },
    { code: 'R10.9', description: 'Unspecified abdominal pain' },
    { code: 'M79.3', description: 'Panniculitis, unspecified' },
    { code: 'L30.9', description: 'Dermatitis, unspecified' },
    { code: 'R51', description: 'Headache' },
    { code: 'G43.909', description: 'Migraine, unspecified' },
    { code: 'N40.0', description: 'Benign prostatic hyperplasia without urinary obstruction' },
    { code: 'G47.00', description: 'Insomnia, unspecified' },
    { code: 'M25.50', description: 'Pain in unspecified joint' },
    { code: 'R05', description: 'Cough' },
    { code: 'H10.9', description: 'Conjunctivitis, unspecified' },
    { code: 'B37.0', description: 'Candidal stomatitis' }
];

const UNIT_OPTIONS = [
    'tablets', 'capsules', 'mL', 'grams', 'each', 'patches', 'puffs',
    'drops', 'suppositories', 'packets', 'vials', 'pens', 'inhalers',
    'tubes', 'bottles', 'softgels', 'lozenges', 'sprays'
];

const FREQUENCY_OPTIONS = [
    { id: 'QD', label: 'Once daily (QD)' },
    { id: 'BID', label: 'Twice daily (BID)' },
    { id: 'TID', label: 'Three times daily (TID)' },
    { id: 'QID', label: 'Four times daily (QID)' },
    { id: 'QHS', label: 'At bedtime (QHS)' },
    { id: 'PRN', label: 'As needed (PRN)' },
    { id: 'Q4H', label: 'Every 4 hours' },
    { id: 'Q6H', label: 'Every 6 hours' },
    { id: 'Q8H', label: 'Every 8 hours' },
    { id: 'Q12H', label: 'Every 12 hours' },
    { id: 'QOD', label: 'Every other day' },
    { id: 'QWK', label: 'Once weekly' }
];

const DISCONTINUE_REASONS = [
    'I want to discontinue this medication',
    'Discontinued by another prescriber',
    'Patient stopped taking medication'
];
