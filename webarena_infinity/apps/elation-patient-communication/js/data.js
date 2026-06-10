/* ============================================================
   Elation Patient Communication — Seed Data
   ============================================================ */

const SEED_DATA_VERSION = 1;

// ── Current logged-in provider ──────────────────────────────
const CURRENT_USER = {
    id: 'prov_1',
    firstName: 'Sarah',
    lastName: 'Chen',
    email: 'sarah.chen@elationhealth.io',
    role: 'physician',
    avatarColor: '#4A90D9'
};

// ── Providers ───────────────────────────────────────────────
const PROVIDERS = [
    {
        id: 'prov_1',
        firstName: 'Sarah',
        lastName: 'Chen',
        email: 'sarah.chen@elationhealth.io',
        role: 'physician',
        sharingDefault: 2,
        notificationTimeframe: '48_hours',
        virtualVisitActivated: true,
        virtualVisitInstructions: 'Please join your virtual visit using this link: https://zoom.us/j/9384752610?pwd=abc123. Make sure your camera and microphone are working before the visit.',
        isAdmin: true
    },
    {
        id: 'prov_2',
        firstName: 'Michael',
        lastName: 'Torres',
        email: 'michael.torres@elationhealth.io',
        role: 'physician',
        sharingDefault: 3,
        notificationTimeframe: '24_hours',
        virtualVisitActivated: true,
        virtualVisitInstructions: 'Join your telehealth appointment here: https://zoom.us/j/7261048395?pwd=def456. Please be in a quiet, well-lit room.',
        isAdmin: false
    },
    {
        id: 'prov_3',
        firstName: 'Jessica',
        lastName: 'Okafor',
        email: 'jessica.okafor@elationhealth.io',
        role: 'nurse_practitioner',
        sharingDefault: 2,
        notificationTimeframe: '72_hours',
        virtualVisitActivated: false,
        virtualVisitInstructions: '',
        isAdmin: false
    },
    {
        id: 'prov_4',
        firstName: 'Robert',
        lastName: 'Kim',
        email: 'robert.kim@elationhealth.io',
        role: 'physician',
        sharingDefault: 1,
        notificationTimeframe: '48_hours',
        virtualVisitActivated: true,
        virtualVisitInstructions: 'Your virtual visit link: https://zoom.us/j/5029384716?pwd=ghi789. If you have trouble connecting, call our office at (555) 234-5678.',
        isAdmin: false
    },
    {
        id: 'prov_5',
        firstName: 'Amanda',
        lastName: 'Wright',
        email: 'amanda.wright@elationhealth.io',
        role: 'physician_assistant',
        sharingDefault: 2,
        notificationTimeframe: '24_hours',
        virtualVisitActivated: false,
        virtualVisitInstructions: '',
        isAdmin: true
    }
];

// ── User Groups ─────────────────────────────────────────────
const USER_GROUPS = [
    { id: 'ug_1', name: 'Front Desk', memberIds: ['prov_3', 'prov_5'] },
    { id: 'ug_2', name: 'Clinical Team', memberIds: ['prov_1', 'prov_2', 'prov_4'] },
    { id: 'ug_3', name: 'Nurses', memberIds: ['prov_3'] },
    { id: 'ug_4', name: 'All Providers', memberIds: ['prov_1', 'prov_2', 'prov_3', 'prov_4', 'prov_5'] }
];

// ── Message Categories (for patient-initiated messages) ─────
const MESSAGE_CATEGORIES = [
    'General Question',
    'Prescription Refill',
    'Appointment Request',
    'Test Results',
    'Billing Question',
    'Referral Request',
    'Medical Records Request',
    'Other'
];

// ── Message Routing (per provider, per category) ────────────
const MESSAGE_ROUTING = {
    'prov_1': {
        'General Question': ['prov_1', 'ug_1'],
        'Prescription Refill': ['prov_1'],
        'Appointment Request': ['ug_1'],
        'Test Results': ['prov_1'],
        'Billing Question': ['ug_1'],
        'Referral Request': ['prov_1'],
        'Medical Records Request': ['ug_1'],
        'Other': ['prov_1']
    },
    'prov_2': {
        'General Question': ['prov_2', 'ug_1'],
        'Prescription Refill': ['prov_2'],
        'Appointment Request': ['ug_1'],
        'Test Results': ['prov_2'],
        'Billing Question': ['ug_1'],
        'Referral Request': ['prov_2'],
        'Medical Records Request': ['ug_1'],
        'Other': ['prov_2']
    },
    'prov_3': {
        'General Question': ['prov_3'],
        'Prescription Refill': ['prov_3', 'prov_1'],
        'Appointment Request': ['ug_1'],
        'Test Results': ['prov_3'],
        'Billing Question': ['ug_1'],
        'Referral Request': ['prov_3'],
        'Medical Records Request': ['ug_1'],
        'Other': ['prov_3']
    },
    'prov_4': {
        'General Question': ['prov_4', 'ug_1'],
        'Prescription Refill': ['prov_4'],
        'Appointment Request': ['ug_1'],
        'Test Results': ['prov_4'],
        'Billing Question': ['ug_1'],
        'Referral Request': ['prov_4'],
        'Medical Records Request': ['ug_1'],
        'Other': ['prov_4']
    },
    'prov_5': {
        'General Question': ['prov_5'],
        'Prescription Refill': ['prov_5', 'prov_2'],
        'Appointment Request': ['ug_1'],
        'Test Results': ['prov_5'],
        'Billing Question': ['ug_1'],
        'Referral Request': ['prov_5'],
        'Medical Records Request': ['ug_1'],
        'Other': ['prov_5']
    }
};

// ── Patient Tags ────────────────────────────────────────────
const PATIENT_TAGS = [
    'VIP', 'Inactive', 'Chronic Care', 'Pediatric', 'Geriatric',
    'High Risk', 'New Patient', 'Diabetes Management', 'Mental Health',
    'Telehealth Preferred', 'Spanish Speaking', 'Insurance Pending'
];

// ── Sharing Levels ──────────────────────────────────────────
const SHARING_LEVELS = {
    1: { level: 1, name: 'Objective Data Only', description: 'Allergies, Drug Intolerances, Medications, Vaccines' },
    2: { level: 2, name: 'Objective Data & Problem List', description: 'Adds Problem List (satisfies MIPS)' },
    3: { level: 3, name: 'Clinical Profile, excludes Confidential', description: 'Adds History, Legal Reports, Provider List' },
    4: { level: 4, name: 'Clinical Profile, Expanded Summary', description: 'Adds Expanded Summary, Implantable Devices (CCDA)' }
};

// ── Notification Timeframes ─────────────────────────────────
const NOTIFICATION_TIMEFRAMES = [
    { value: 'none', label: 'Do not notify me' },
    { value: '24_hours', label: '24 hours' },
    { value: '48_hours', label: '48 hours' },
    { value: '72_hours', label: '72 hours' },
    { value: '1_week', label: '1 week' },
    { value: '2_weeks', label: '2 weeks' }
];

// ── Practice Settings ───────────────────────────────────────
const PRACTICE_SETTINGS = {
    practiceName: 'Bay Area Family Medicine',
    allowPatientMessaging: true,
    bookingSiteAutoInvite: true,
    bookingSiteUrl: 'https://booking.bayareafamilymed.com',
    practicePhone: '(555) 234-5678',
    practiceAddress: '1200 Market Street, Suite 400, San Francisco, CA 94103',
    practiceLocations: [
        { id: 'loc_1', name: 'Main Office', address: '1200 Market Street, Suite 400, San Francisco, CA 94103', posCode: '11', posDescription: 'Office' },
        { id: 'loc_2', name: 'Telehealth', address: '1200 Market Street, Suite 400, San Francisco, CA 94103', posCode: '02', posDescription: 'Telehealth - Other' },
        { id: 'loc_3', name: 'East Bay Clinic', address: '450 Broadway, Oakland, CA 94607', posCode: '11', posDescription: 'Office' }
    ],
    cptCodes: [
        { code: '99201', description: 'Office visit, new patient, minimal' },
        { code: '99202', description: 'Office visit, new patient, low complexity' },
        { code: '99203', description: 'Office visit, new patient, moderate complexity' },
        { code: '99211', description: 'Office visit, established patient, minimal' },
        { code: '99212', description: 'Office visit, established patient, low complexity' },
        { code: '99213', description: 'Office visit, established patient, moderate complexity' },
        { code: '99214', description: 'Office visit, established patient, high complexity' },
        { code: '99441', description: 'Telephone E/M, 5-10 minutes' },
        { code: '99442', description: 'Telephone E/M, 11-20 minutes' },
        { code: '99443', description: 'Telephone E/M, 21-30 minutes' },
        { code: '99421', description: 'Online digital E/M, 5-10 minutes' },
        { code: '99422', description: 'Online digital E/M, 11-20 minutes' },
        { code: '99423', description: 'Online digital E/M, 21+ minutes' }
    ],
    videoSettings: {
        screenSharingPatients: true,
        chatMode: 'everyone_in_meeting',
        waitingRoomAudioNotification: true
    }
};

// ── Patients (50) ───────────────────────────────────────────
function _p(id, first, last, email, phone, dob, providerId, passportStatus, smsOptIn, tags, sharingLevel, opts) {
    return {
        id,
        firstName: first,
        lastName: last,
        email,
        cellPhone: phone,
        dateOfBirth: dob,
        assignedProviderId: providerId,
        passportStatus,
        smsOptInStatus: smsOptIn,
        tags: tags || [],
        passportSharingLevel: sharingLevel || 2,
        passportAccountDisabled: false,
        invitedAt: opts?.invitedAt || null,
        registeredAt: opts?.registeredAt || null,
        invitationCode: opts?.invitationCode || null,
        emergencyContact: opts?.emergencyContact || null,
        clinicalProfile: opts?.clinicalProfile || {
            allergies: [],
            drugIntolerances: [],
            medications: [],
            vaccines: [],
            problemList: [],
            history: [],
            confidential: []
        },
        ...opts?.extra
    };
}

const PATIENTS = [
    _p('pat_1', 'James', 'Rodriguez', 'james.rodriguez@gmail.com', '(415) 555-0101', '1985-03-15', 'prov_1', 'registered', 'opted_in', ['Chronic Care', 'Diabetes Management'], 3, {
        invitedAt: '2025-06-10T09:00:00Z', registeredAt: '2025-06-12T14:30:00Z', invitationCode: '4829173',
        emergencyContact: { name: 'Maria Rodriguez', phone: '(415) 555-0102', relationship: 'Spouse' },
        clinicalProfile: {
            allergies: ['Penicillin', 'Sulfa drugs'],
            drugIntolerances: ['Codeine - nausea'],
            medications: ['Metformin 500mg twice daily', 'Lisinopril 10mg daily', 'Atorvastatin 20mg daily'],
            vaccines: ['Flu 2025-10-15', 'COVID-19 Booster 2025-09-01', 'Tdap 2023-04-20'],
            problemList: ['Type 2 Diabetes Mellitus', 'Hypertension', 'Hyperlipidemia'],
            history: ['Appendectomy 2010', 'Family history of heart disease'],
            confidential: ['Anxiety disorder - managed with therapy']
        }
    }),
    _p('pat_2', 'Emily', 'Thompson', 'emily.t@outlook.com', '(415) 555-0203', '1992-07-22', 'prov_1', 'registered', 'opted_in', ['New Patient'], 2, {
        invitedAt: '2025-09-01T10:00:00Z', registeredAt: '2025-09-03T11:15:00Z', invitationCode: '7361024',
        emergencyContact: { name: 'David Thompson', phone: '(415) 555-0204', relationship: 'Father' },
        clinicalProfile: {
            allergies: ['Latex'],
            drugIntolerances: [],
            medications: ['Sertraline 50mg daily', 'Vitamin D 2000 IU daily'],
            vaccines: ['Flu 2025-10-20', 'COVID-19 2025-04-15'],
            problemList: ['Generalized Anxiety Disorder', 'Vitamin D deficiency'],
            history: ['Tonsillectomy 2002'],
            confidential: []
        }
    }),
    _p('pat_3', 'Robert', 'Washington', 'r.washington@yahoo.com', '(510) 555-0305', '1958-11-30', 'prov_2', 'registered', 'opted_out', ['Geriatric', 'Chronic Care', 'High Risk'], 3, {
        invitedAt: '2025-04-15T08:30:00Z', registeredAt: '2025-04-18T16:45:00Z', invitationCode: '9150283',
        emergencyContact: { name: 'Patricia Washington', phone: '(510) 555-0306', relationship: 'Wife' },
        clinicalProfile: {
            allergies: ['Aspirin', 'Ibuprofen'],
            drugIntolerances: ['Metformin - GI upset', 'Lisinopril - cough'],
            medications: ['Amlodipine 5mg daily', 'Glipizide 5mg twice daily', 'Warfarin 5mg daily', 'Metoprolol 25mg twice daily', 'Omeprazole 20mg daily'],
            vaccines: ['Flu 2025-10-05', 'Pneumovax 2024-03-10', 'Shingrix dose 1 2025-01-15', 'Shingrix dose 2 2025-03-15'],
            problemList: ['Type 2 Diabetes', 'Atrial Fibrillation', 'Hypertension', 'GERD', 'Osteoarthritis - bilateral knees'],
            history: ['CABG 2018', 'Right knee replacement 2021', 'Family history of stroke'],
            confidential: ['Depression - stable on medication']
        }
    }),
    _p('pat_4', 'Sophia', 'Nguyen', 'sophia.nguyen@gmail.com', '(415) 555-0407', '1978-01-08', 'prov_1', 'registered', 'opted_in', ['Telehealth Preferred'], 2, {
        invitedAt: '2025-07-20T14:00:00Z', registeredAt: '2025-07-21T09:30:00Z', invitationCode: '6204817',
        emergencyContact: { name: 'Tuan Nguyen', phone: '(415) 555-0408', relationship: 'Husband' },
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Levothyroxine 75mcg daily'],
            vaccines: ['Flu 2025-10-12', 'COVID-19 Booster 2025-08-20'],
            problemList: ['Hypothyroidism'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_5', 'Marcus', 'Johnson', 'marcus.j@protonmail.com', '(510) 555-0509', '1995-05-19', 'prov_2', 'invited', 'never', ['New Patient'], 2, {
        invitedAt: '2026-01-15T11:00:00Z', invitationCode: '3847261'
    }),
    _p('pat_6', 'Linda', 'Garcia', 'linda.garcia@hotmail.com', '(415) 555-0611', '1970-09-03', 'prov_3', 'registered', 'opted_in', ['Chronic Care'], 3, {
        invitedAt: '2025-05-10T09:00:00Z', registeredAt: '2025-05-14T10:20:00Z', invitationCode: '5183920',
        emergencyContact: { name: 'Carlos Garcia', phone: '(415) 555-0612', relationship: 'Son' },
        clinicalProfile: {
            allergies: ['Peanuts', 'Tree nuts'],
            drugIntolerances: ['Amoxicillin - rash'],
            medications: ['Fluoxetine 20mg daily', 'Alendronate 70mg weekly', 'Calcium + Vitamin D daily'],
            vaccines: ['Flu 2025-10-18', 'COVID-19 2025-06-01', 'Shingrix dose 1 2025-08-10'],
            problemList: ['Osteoporosis', 'Major Depressive Disorder', 'Peanut allergy'],
            history: ['Hip fracture 2023', 'Hysterectomy 2015'],
            confidential: ['History of domestic violence']
        }
    }),
    _p('pat_7', 'David', 'Park', 'david.park@gmail.com', '(650) 555-0713', '1988-12-01', 'prov_4', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-08-01T13:00:00Z', registeredAt: '2025-08-02T08:45:00Z', invitationCode: '7920415',
        emergencyContact: { name: 'Jisoo Park', phone: '(650) 555-0714', relationship: 'Sister' },
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Montelukast 10mg daily', 'Albuterol inhaler PRN'],
            vaccines: ['Flu 2025-10-22', 'COVID-19 2025-07-15'],
            problemList: ['Asthma - mild persistent'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_8', 'Patricia', 'O\'Brien', 'pobrien@comcast.net', '(415) 555-0815', '1965-04-17', 'prov_1', 'registered', 'opted_in', ['VIP', 'Chronic Care'], 4, {
        invitedAt: '2025-03-01T10:00:00Z', registeredAt: '2025-03-02T15:00:00Z', invitationCode: '2648173',
        emergencyContact: { name: 'Sean O\'Brien', phone: '(415) 555-0816', relationship: 'Husband' },
        clinicalProfile: {
            allergies: ['Sulfa drugs', 'Contrast dye'],
            drugIntolerances: ['Statins - myalgia'],
            medications: ['Losartan 50mg daily', 'Metformin 1000mg twice daily', 'Ezetimibe 10mg daily', 'Aspirin 81mg daily', 'Insulin glargine 20 units nightly'],
            vaccines: ['Flu 2025-10-08', 'COVID-19 Booster 2025-09-15', 'Pneumovax 2024-11-20'],
            problemList: ['Type 2 Diabetes', 'Hypertension', 'Hyperlipidemia', 'Chronic Kidney Disease Stage 3a', 'Peripheral Neuropathy'],
            history: ['Breast cancer survivor 2019', 'Statin intolerance', 'Family history of kidney disease'],
            confidential: []
        }
    }),
    _p('pat_9', 'Anthony', 'Petrov', 'a.petrov@gmail.com', '(510) 555-0917', '2001-08-25', 'prov_2', 'not_invited', 'never', ['New Patient'], 2, {
        emergencyContact: { name: 'Elena Petrov', phone: '(510) 555-0918', relationship: 'Mother' },
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Adderall XR 20mg daily'],
            vaccines: ['COVID-19 2025-03-10'],
            problemList: ['ADHD'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_10', 'Helen', 'Matsumoto', 'helen.m@sbcglobal.net', '(415) 555-1019', '1952-02-14', 'prov_1', 'registered', 'opted_in', ['Geriatric', 'VIP'], 3, {
        invitedAt: '2025-02-10T09:00:00Z', registeredAt: '2025-02-12T11:00:00Z', invitationCode: '8371049',
        emergencyContact: { name: 'Ken Matsumoto', phone: '(415) 555-1020', relationship: 'Son' },
        clinicalProfile: {
            allergies: ['Morphine'],
            drugIntolerances: ['NSAIDs - GI bleeding risk'],
            medications: ['Donepezil 10mg daily', 'Memantine 10mg twice daily', 'Sertraline 100mg daily', 'Amlodipine 10mg daily', 'Omeprazole 20mg daily', 'Acetaminophen 500mg PRN'],
            vaccines: ['Flu 2025-10-01', 'Pneumovax 2023-10-15', 'Shingrix complete 2024'],
            problemList: ['Alzheimer\'s Disease - mild', 'Hypertension', 'Osteoarthritis', 'GERD', 'Depression'],
            history: ['Left hip replacement 2020', 'Cataract surgery bilateral 2022'],
            confidential: ['Advance directive on file - DNR']
        }
    }),
    _p('pat_11', 'Kevin', 'Adebayo', 'kevin.adebayo@gmail.com', '(650) 555-1121', '1983-06-09', 'prov_4', 'registered', 'opted_in', ['Diabetes Management'], 2, {
        invitedAt: '2025-10-01T14:00:00Z', registeredAt: '2025-10-03T09:00:00Z', invitationCode: '4017286',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Metformin 850mg twice daily', 'Januvia 100mg daily'],
            vaccines: ['Flu 2025-10-25', 'COVID-19 2025-08-01'],
            problemList: ['Type 2 Diabetes', 'Obesity BMI 34'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_12', 'Rachel', 'Steinberg', 'rachel.s@gmail.com', '(415) 555-1223', '1990-10-31', 'prov_3', 'registered', 'opted_in', ['Mental Health'], 2, {
        invitedAt: '2025-08-15T10:00:00Z', registeredAt: '2025-08-16T13:30:00Z', invitationCode: '5829041',
        clinicalProfile: {
            allergies: ['Shellfish'],
            drugIntolerances: [],
            medications: ['Escitalopram 10mg daily', 'Buspirone 10mg twice daily'],
            vaccines: ['Flu 2025-10-14', 'COVID-19 2025-05-20'],
            problemList: ['Generalized Anxiety Disorder', 'Panic Disorder'],
            history: [],
            confidential: ['Eating disorder history - recovered']
        }
    }),
    _p('pat_13', 'William', 'Chang', 'wchang@yahoo.com', '(510) 555-1325', '1975-07-04', 'prov_2', 'invited', 'opted_in', [], 2, {
        invitedAt: '2026-02-01T09:00:00Z', invitationCode: '1746290'
    }),
    _p('pat_14', 'Maria', 'Gonzalez', 'maria.gonzalez@gmail.com', '(415) 555-1427', '1968-03-22', 'prov_1', 'registered', 'opted_in', ['Spanish Speaking', 'Chronic Care'], 3, {
        invitedAt: '2025-05-20T11:00:00Z', registeredAt: '2025-05-25T16:00:00Z', invitationCode: '3082714',
        emergencyContact: { name: 'Jose Gonzalez', phone: '(415) 555-1428', relationship: 'Husband' },
        clinicalProfile: {
            allergies: [],
            drugIntolerances: ['ACE inhibitors - angioedema'],
            medications: ['Losartan 100mg daily', 'Hydrochlorothiazide 25mg daily', 'Metformin 500mg daily'],
            vaccines: ['Flu 2025-10-10', 'COVID-19 2025-07-01'],
            problemList: ['Hypertension', 'Pre-diabetes', 'Obesity BMI 31'],
            history: ['Gestational diabetes 2002'],
            confidential: []
        }
    }),
    _p('pat_15', 'Brian', 'Murphy', 'brian.murphy@icloud.com', '(650) 555-1529', '1999-12-18', 'prov_4', 'not_invited', 'never', [], 2, {
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: [],
            vaccines: ['Flu 2025-10-28', 'COVID-19 2025-06-15'],
            problemList: [],
            history: [],
            confidential: []
        }
    }),
    _p('pat_16', 'Diane', 'Foster-Hutchinson', 'diane.fh@gmail.com', '(415) 555-1631', '1981-09-07', 'prov_1', 'registered', 'opted_in', ['Telehealth Preferred'], 2, {
        invitedAt: '2025-07-01T12:00:00Z', registeredAt: '2025-07-02T10:15:00Z', invitationCode: '6194820',
        emergencyContact: { name: 'Mark Hutchinson', phone: '(415) 555-1632', relationship: 'Husband' },
        clinicalProfile: {
            allergies: ['Bee stings'],
            drugIntolerances: [],
            medications: ['EpiPen (epinephrine auto-injector) PRN', 'Cetirizine 10mg daily'],
            vaccines: ['Flu 2025-10-16', 'COVID-19 2025-08-10'],
            problemList: ['Bee venom allergy', 'Seasonal allergic rhinitis'],
            history: ['Anaphylaxis 2019'],
            confidential: []
        }
    }),
    _p('pat_17', 'Thomas', 'Nakamura', 'tom.nakamura@outlook.com', '(510) 555-1733', '1973-04-28', 'prov_2', 'registered', 'opted_out', ['High Risk'], 3, {
        invitedAt: '2025-06-05T09:00:00Z', registeredAt: '2025-06-08T14:00:00Z', invitationCode: '2957103',
        emergencyContact: { name: 'Yuki Nakamura', phone: '(510) 555-1734', relationship: 'Wife' },
        clinicalProfile: {
            allergies: ['Penicillin', 'Cephalosporins'],
            drugIntolerances: [],
            medications: ['Eliquis 5mg twice daily', 'Amiodarone 200mg daily', 'Lisinopril 20mg daily', 'Atorvastatin 40mg daily'],
            vaccines: ['Flu 2025-10-03', 'COVID-19 2025-05-01'],
            problemList: ['Atrial Fibrillation', 'Hypertension', 'Hyperlipidemia', 'History of TIA'],
            history: ['TIA 2024', 'Cardioversion 2024', 'Family history: father stroke age 62'],
            confidential: []
        }
    }),
    _p('pat_18', 'Sarah', 'Williams', 'sarah.w@gmail.com', '(415) 555-1835', '2010-06-14', 'prov_1', 'registered', 'opted_in', ['Pediatric'], 2, {
        invitedAt: '2025-09-10T10:00:00Z', registeredAt: '2025-09-11T19:00:00Z', invitationCode: '7401825',
        emergencyContact: { name: 'Jennifer Williams', phone: '(415) 555-1836', relationship: 'Mother' },
        clinicalProfile: {
            allergies: ['Amoxicillin'],
            drugIntolerances: [],
            medications: ['Fluticasone nasal spray daily'],
            vaccines: ['Flu 2025-10-20', 'HPV dose 1 2025-06-14', 'HPV dose 2 2025-08-14', 'Tdap 2025-06-14'],
            problemList: ['Allergic rhinitis', 'Mild intermittent asthma'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_19', 'Frank', 'DeLuca', 'frank.deluca@aol.com', '(650) 555-1937', '1960-01-23', 'prov_4', 'registered', 'opted_in', ['Geriatric'], 2, {
        invitedAt: '2025-04-01T09:00:00Z', registeredAt: '2025-04-05T11:30:00Z', invitationCode: '8260143',
        emergencyContact: { name: 'Angela DeLuca', phone: '(650) 555-1938', relationship: 'Wife' },
        clinicalProfile: {
            allergies: [],
            drugIntolerances: ['Tramadol - dizziness'],
            medications: ['Tamsulosin 0.4mg daily', 'Finasteride 5mg daily', 'Acetaminophen 500mg PRN'],
            vaccines: ['Flu 2025-10-06', 'COVID-19 2025-04-20', 'Pneumovax 2024-01-15'],
            problemList: ['BPH', 'Lower back pain', 'Mild hearing loss'],
            history: ['Prostate biopsy 2023 - benign'],
            confidential: []
        }
    }),
    _p('pat_20', 'Aisha', 'Patel', 'aisha.patel@gmail.com', '(415) 555-2039', '1987-08-11', 'prov_3', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-11-01T14:00:00Z', registeredAt: '2025-11-02T09:45:00Z', invitationCode: '4918360',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Prenatal vitamins daily'],
            vaccines: ['Flu 2025-10-22', 'COVID-19 2025-03-15', 'Tdap 2025-12-01'],
            problemList: ['Pregnancy - 28 weeks (as of seed date)'],
            history: ['G2P1 - prior uncomplicated delivery 2023'],
            confidential: []
        }
    }),
    _p('pat_21', 'George', 'Kowalski', 'g.kowalski@gmail.com', '(510) 555-2141', '1971-11-05', 'prov_2', 'invited', 'opted_in', [], 2, {
        invitedAt: '2026-02-10T10:00:00Z', invitationCode: '5027184'
    }),
    _p('pat_22', 'Christine', 'Lee', 'christine.lee@yahoo.com', '(415) 555-2243', '1994-02-28', 'prov_1', 'registered', 'opted_in', ['Mental Health'], 2, {
        invitedAt: '2025-12-01T09:00:00Z', registeredAt: '2025-12-02T11:00:00Z', invitationCode: '6382910',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Bupropion 150mg daily', 'Trazodone 50mg at bedtime PRN'],
            vaccines: ['Flu 2025-10-18', 'COVID-19 2025-07-20'],
            problemList: ['Major Depressive Disorder', 'Insomnia'],
            history: [],
            confidential: ['Substance use history - alcohol, 2 years sober']
        }
    }),
    _p('pat_23', 'Victor', 'Santos', 'v.santos@outlook.com', '(650) 555-2345', '1982-05-16', 'prov_4', 'not_invited', 'never', ['Insurance Pending'], 2, {}),
    _p('pat_24', 'Nancy', 'Yamamoto', 'nancy.y@gmail.com', '(415) 555-2447', '1956-10-09', 'prov_1', 'registered', 'opted_out', ['Geriatric', 'Chronic Care'], 3, {
        invitedAt: '2025-03-15T09:00:00Z', registeredAt: '2025-03-18T14:00:00Z', invitationCode: '1039482',
        emergencyContact: { name: 'Tom Yamamoto', phone: '(415) 555-2448', relationship: 'Husband' },
        clinicalProfile: {
            allergies: ['Codeine', 'Latex'],
            drugIntolerances: [],
            medications: ['Levothyroxine 100mcg daily', 'Lisinopril 10mg daily', 'Alendronate 70mg weekly', 'Calcium + Vitamin D daily'],
            vaccines: ['Flu 2025-10-04', 'Shingrix complete 2025', 'COVID-19 2025-09-10'],
            problemList: ['Hypothyroidism', 'Hypertension', 'Osteoporosis'],
            history: ['Thyroid nodule biopsy 2022 - benign', 'DEXA scan 2025 - T-score -2.8'],
            confidential: []
        }
    }),
    _p('pat_25', 'Derek', 'Hansen', 'derek.hansen@gmail.com', '(510) 555-2549', '1997-01-30', 'prov_2', 'registered', 'opted_in', [], 1, {
        invitedAt: '2025-11-15T10:00:00Z', registeredAt: '2025-11-16T08:30:00Z', invitationCode: '7284019',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: [],
            vaccines: ['Flu 2025-10-30', 'COVID-19 2025-06-10'],
            problemList: [],
            history: ['ACL repair 2020'],
            confidential: []
        }
    }),
    _p('pat_26', 'Olivia', 'Chen', 'olivia.chen@icloud.com', '(415) 555-2651', '1991-04-03', 'prov_1', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-10-20T11:00:00Z', registeredAt: '2025-10-21T09:00:00Z', invitationCode: '3591726',
        clinicalProfile: {
            allergies: ['Sulfa drugs'],
            drugIntolerances: [],
            medications: ['Oral contraceptive daily', 'Iron supplement daily'],
            vaccines: ['Flu 2025-10-19', 'COVID-19 2025-08-05'],
            problemList: ['Iron deficiency anemia'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_27', 'Howard', 'Blackwell', 'h.blackwell@protonmail.com', '(650) 555-2753', '1948-07-19', 'prov_4', 'registered', 'opted_out', ['Geriatric', 'High Risk', 'Chronic Care'], 3, {
        invitedAt: '2025-01-10T09:00:00Z', registeredAt: '2025-01-15T10:00:00Z', invitationCode: '8473920',
        emergencyContact: { name: 'Dorothy Blackwell', phone: '(650) 555-2754', relationship: 'Wife' },
        clinicalProfile: {
            allergies: ['Penicillin', 'Aspirin', 'Iodine'],
            drugIntolerances: ['Beta-blockers - bradycardia', 'Statins - liver enzyme elevation'],
            medications: ['Warfarin 3mg daily', 'Diltiazem 180mg daily', 'Furosemide 40mg daily', 'Potassium chloride 20mEq daily', 'Pantoprazole 40mg daily', 'Gabapentin 300mg three times daily'],
            vaccines: ['Flu 2025-10-02', 'Pneumovax 2023-11-01'],
            problemList: ['CHF - NYHA Class II', 'Atrial Fibrillation', 'Peripheral Neuropathy', 'CKD Stage 3b', 'Gout'],
            history: ['MI 2015', 'Pacemaker implant 2018', 'Gout flare 2025'],
            confidential: []
        }
    }),
    _p('pat_28', 'Stephanie', 'Rivera', 'stephanie.r@gmail.com', '(415) 555-2855', '1986-12-25', 'prov_3', 'invited', 'opted_in', [], 2, {
        invitedAt: '2026-02-20T14:00:00Z', invitationCode: '2648901'
    }),
    _p('pat_29', 'Andrew', 'McIntyre', 'andrew.mcintyre@gmail.com', '(510) 555-2957', '1976-03-12', 'prov_2', 'registered', 'opted_in', ['Telehealth Preferred'], 2, {
        invitedAt: '2025-06-15T09:00:00Z', registeredAt: '2025-06-17T10:30:00Z', invitationCode: '5103826',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Omeprazole 40mg daily', 'Sucralfate 1g four times daily'],
            vaccines: ['Flu 2025-10-11', 'COVID-19 2025-07-25'],
            problemList: ['Peptic ulcer disease', 'H. pylori - treated'],
            history: ['EGD 2025 - healing ulcer'],
            confidential: []
        }
    }),
    _p('pat_30', 'Janet', 'Okonkwo', 'janet.o@gmail.com', '(415) 555-3059', '1963-08-20', 'prov_1', 'registered', 'opted_in', ['Chronic Care', 'Diabetes Management'], 3, {
        invitedAt: '2025-04-10T10:00:00Z', registeredAt: '2025-04-12T13:00:00Z', invitationCode: '7349180',
        emergencyContact: { name: 'Emeka Okonkwo', phone: '(415) 555-3060', relationship: 'Husband' },
        clinicalProfile: {
            allergies: ['Erythromycin'],
            drugIntolerances: [],
            medications: ['Insulin lispro with meals', 'Insulin glargine 30 units nightly', 'Losartan 50mg daily', 'Atorvastatin 20mg daily', 'Baby aspirin 81mg daily'],
            vaccines: ['Flu 2025-10-07', 'COVID-19 Booster 2025-09-05'],
            problemList: ['Type 1 Diabetes', 'Hypertension', 'Diabetic retinopathy - mild'],
            history: ['Laser photocoagulation 2024', 'A1C 7.2% last check'],
            confidential: []
        }
    }),
    _p('pat_31', 'Craig', 'Bennet', 'craig.b@yahoo.com', '(650) 555-3161', '2003-09-08', 'prov_4', 'not_invited', 'never', ['New Patient'], 2, {}),
    _p('pat_32', 'Priya', 'Sharma', 'priya.sharma@gmail.com', '(415) 555-3263', '1989-11-15', 'prov_1', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-09-20T09:00:00Z', registeredAt: '2025-09-21T11:00:00Z', invitationCode: '4920137',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Sumatriptan 50mg PRN'],
            vaccines: ['Flu 2025-10-15', 'COVID-19 2025-06-20'],
            problemList: ['Migraine with aura'],
            history: ['MRI brain 2025 - normal'],
            confidential: []
        }
    }),
    _p('pat_33', 'Douglas', 'Fitzgerald', 'doug.fitz@outlook.com', '(510) 555-3365', '1955-06-30', 'prov_2', 'registered', 'opted_out', ['Geriatric'], 2, {
        invitedAt: '2025-05-01T09:00:00Z', registeredAt: '2025-05-06T15:00:00Z', invitationCode: '8174029',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: ['ACE inhibitors - cough'],
            medications: ['Metoprolol 50mg daily', 'Valsartan 160mg daily'],
            vaccines: ['Flu 2025-10-09', 'Pneumovax 2024-04-01'],
            problemList: ['Hypertension', 'Benign positional vertigo'],
            history: ['Epley maneuver 2025'],
            confidential: []
        }
    }),
    _p('pat_34', 'Alice', 'Johansson', 'alice.j@gmail.com', '(415) 555-3467', '1993-02-07', 'prov_3', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-12-10T10:00:00Z', registeredAt: '2025-12-11T08:00:00Z', invitationCode: '6019274',
        clinicalProfile: {
            allergies: ['Ibuprofen'],
            drugIntolerances: [],
            medications: [],
            vaccines: ['Flu 2025-10-21', 'COVID-19 2025-09-01'],
            problemList: [],
            history: [],
            confidential: []
        }
    }),
    _p('pat_35', 'Raymond', 'Copeland', 'ray.copeland@gmail.com', '(650) 555-3569', '1980-10-22', 'prov_4', 'registered', 'opted_in', ['Diabetes Management'], 2, {
        invitedAt: '2025-08-10T14:00:00Z', registeredAt: '2025-08-12T09:00:00Z', invitationCode: '3728149',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Metformin 1000mg twice daily', 'Empagliflozin 10mg daily', 'Atorvastatin 10mg daily'],
            vaccines: ['Flu 2025-10-24', 'COVID-19 2025-07-10'],
            problemList: ['Type 2 Diabetes', 'Hyperlipidemia'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_36', 'Martha', 'Reeves-Whitfield', 'martha.rw@hotmail.com', '(415) 555-3671', '1950-05-02', 'prov_1', 'registered', 'opted_in', ['Geriatric', 'High Risk'], 3, {
        invitedAt: '2025-02-01T09:00:00Z', registeredAt: '2025-02-05T12:00:00Z', invitationCode: '9201847',
        emergencyContact: { name: 'James Whitfield Jr.', phone: '(415) 555-3672', relationship: 'Son' },
        clinicalProfile: {
            allergies: ['Penicillin', 'Codeine', 'Adhesive tape'],
            drugIntolerances: ['Metformin - severe GI upset'],
            medications: ['Glipizide 10mg twice daily', 'Lisinopril 20mg daily', 'Atorvastatin 40mg daily', 'Acetaminophen 650mg PRN', 'Calcium + Vitamin D daily'],
            vaccines: ['Flu 2025-10-01', 'Pneumovax 2023-09-20', 'Shingrix complete 2024'],
            problemList: ['Type 2 Diabetes', 'Hypertension', 'Osteoporosis', 'Chronic low back pain'],
            history: ['L4-L5 laminectomy 2018', 'Falls risk - uses walker'],
            confidential: []
        }
    }),
    _p('pat_37', 'Jason', 'Liu', 'jason.liu@gmail.com', '(510) 555-3773', '1996-07-14', 'prov_2', 'not_invited', 'never', [], 2, {}),
    _p('pat_38', 'Barbara', 'Andersen', 'barbara.a@comcast.net', '(415) 555-3875', '1967-01-19', 'prov_1', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-07-10T09:00:00Z', registeredAt: '2025-07-12T10:00:00Z', invitationCode: '5283710',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Vitamin B12 1000mcg daily', 'Iron 325mg daily'],
            vaccines: ['Flu 2025-10-13', 'COVID-19 2025-06-05'],
            problemList: ['B12 deficiency', 'Iron deficiency anemia'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_39', 'Tyler', 'Robinson', 'tyler.r@protonmail.com', '(650) 555-3977', '2005-03-28', 'prov_4', 'invited', 'never', ['Pediatric'], 2, {
        invitedAt: '2026-01-20T14:00:00Z', invitationCode: '7194028'
    }),
    _p('pat_40', 'Susan', 'Cho', 'susan.cho@gmail.com', '(415) 555-4079', '1984-09-17', 'prov_3', 'registered', 'opted_in', ['Telehealth Preferred'], 2, {
        invitedAt: '2025-11-20T10:00:00Z', registeredAt: '2025-11-21T09:00:00Z', invitationCode: '6382014',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Loratadine 10mg daily'],
            vaccines: ['Flu 2025-10-17', 'COVID-19 2025-08-15'],
            problemList: ['Chronic urticaria'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_41', 'Gregory', 'Abrams', 'greg.abrams@gmail.com', '(510) 555-4181', '1972-12-06', 'prov_2', 'registered', 'opted_in', ['Chronic Care'], 2, {
        invitedAt: '2025-06-20T09:00:00Z', registeredAt: '2025-06-22T14:00:00Z', invitationCode: '2847190',
        clinicalProfile: {
            allergies: ['Shellfish', 'Iodine contrast'],
            drugIntolerances: [],
            medications: ['Atenolol 50mg daily', 'Lisinopril 10mg daily', 'Simvastatin 20mg daily'],
            vaccines: ['Flu 2025-10-08', 'COVID-19 2025-05-15'],
            problemList: ['Hypertension', 'Hyperlipidemia', 'Mitral valve prolapse'],
            history: ['Echo 2025 - mild MR, stable'],
            confidential: []
        }
    }),
    _p('pat_42', 'Megan', 'Burke', 'megan.burke@yahoo.com', '(415) 555-4283', '1998-04-12', 'prov_1', 'not_invited', 'never', ['New Patient'], 2, {}),
    _p('pat_43', 'Philip', 'Tran', 'philip.tran@gmail.com', '(650) 555-4385', '1961-08-03', 'prov_4', 'registered', 'opted_in', ['Geriatric'], 2, {
        invitedAt: '2025-03-20T09:00:00Z', registeredAt: '2025-03-24T11:00:00Z', invitationCode: '1039527',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Tamsulosin 0.4mg daily', 'Amlodipine 5mg daily'],
            vaccines: ['Flu 2025-10-05', 'COVID-19 2025-04-10', 'Shingrix dose 1 2025-07-01'],
            problemList: ['BPH', 'Hypertension'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_44', 'Lauren', 'Dubois', 'lauren.d@icloud.com', '(415) 555-4487', '1990-06-21', 'prov_3', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-10-10T10:00:00Z', registeredAt: '2025-10-11T08:30:00Z', invitationCode: '8471920',
        clinicalProfile: {
            allergies: ['Latex'],
            drugIntolerances: [],
            medications: [],
            vaccines: ['Flu 2025-10-23', 'COVID-19 2025-09-05'],
            problemList: [],
            history: [],
            confidential: []
        }
    }),
    _p('pat_45', 'Edward', 'Kowalczyk', 'ed.kowalczyk@outlook.com', '(510) 555-4589', '1977-11-27', 'prov_2', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-09-05T09:00:00Z', registeredAt: '2025-09-07T10:00:00Z', invitationCode: '3029184',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Allopurinol 300mg daily', 'Colchicine 0.6mg daily'],
            vaccines: ['Flu 2025-10-26', 'COVID-19 2025-07-30'],
            problemList: ['Gout', 'Hyperuricemia'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_46', 'Catherine', 'Morales', 'cat.morales@gmail.com', '(415) 555-4691', '1974-03-09', 'prov_1', 'registered', 'opted_in', ['Spanish Speaking'], 2, {
        invitedAt: '2025-08-20T14:00:00Z', registeredAt: '2025-08-22T09:30:00Z', invitationCode: '5948201',
        clinicalProfile: {
            allergies: [],
            drugIntolerances: [],
            medications: ['Levothyroxine 50mcg daily', 'Vitamin D 2000 IU daily'],
            vaccines: ['Flu 2025-10-14', 'COVID-19 2025-06-25'],
            problemList: ['Hypothyroidism', 'Vitamin D deficiency'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_47', 'Dennis', 'Volkov', 'dennis.v@gmail.com', '(650) 555-4793', '1959-07-08', 'prov_4', 'registered', 'opted_out', ['Geriatric', 'Chronic Care'], 2, {
        invitedAt: '2025-04-20T09:00:00Z', registeredAt: '2025-04-25T16:00:00Z', invitationCode: '7182039',
        emergencyContact: { name: 'Irina Volkov', phone: '(650) 555-4794', relationship: 'Wife' },
        clinicalProfile: {
            allergies: [],
            drugIntolerances: ['NSAIDs - renal risk'],
            medications: ['Metoprolol 100mg daily', 'Losartan 100mg daily', 'Amlodipine 10mg daily', 'Furosemide 20mg daily'],
            vaccines: ['Flu 2025-10-03', 'Pneumovax 2024-02-10'],
            problemList: ['Hypertension - resistant', 'CKD Stage 3a', 'Left ventricular hypertrophy'],
            history: ['Renal ultrasound 2025 - bilateral atrophy'],
            confidential: []
        }
    }),
    _p('pat_48', 'Michelle', 'O\'Connor', 'michelle.oc@gmail.com', '(415) 555-4895', '1985-10-14', 'prov_1', 'invited', 'opted_in', [], 2, {
        invitedAt: '2026-02-25T10:00:00Z', invitationCode: '4019283'
    }),
    _p('pat_49', 'Russell', 'Keane', 'russell.keane@yahoo.com', '(510) 555-4997', '1969-05-31', 'prov_2', 'registered', 'opted_in', [], 2, {
        invitedAt: '2025-07-05T09:00:00Z', registeredAt: '2025-07-08T14:00:00Z', invitationCode: '6290184',
        clinicalProfile: {
            allergies: ['Penicillin'],
            drugIntolerances: [],
            medications: ['Lisinopril 20mg daily', 'Metformin 1000mg twice daily'],
            vaccines: ['Flu 2025-10-10', 'COVID-19 2025-06-15'],
            problemList: ['Type 2 Diabetes', 'Hypertension'],
            history: [],
            confidential: []
        }
    }),
    _p('pat_50', 'Deborah', 'Takahashi', 'deborah.t@sbcglobal.net', '(415) 555-5099', '1957-09-24', 'prov_1', 'registered', 'opted_in', ['Geriatric', 'VIP'], 3, {
        invitedAt: '2025-01-15T09:00:00Z', registeredAt: '2025-01-18T10:30:00Z', invitationCode: '8370291',
        emergencyContact: { name: 'Ken Takahashi', phone: '(415) 555-5100', relationship: 'Husband' },
        clinicalProfile: {
            allergies: ['Sulfa drugs'],
            drugIntolerances: [],
            medications: ['Amlodipine 5mg daily', 'Omeprazole 20mg daily', 'Calcium + Vitamin D daily'],
            vaccines: ['Flu 2025-10-06', 'Shingrix complete 2024', 'Pneumovax 2024-05-01'],
            problemList: ['Hypertension', 'GERD', 'Osteopenia'],
            history: ['DEXA 2025 - T-score -1.8'],
            confidential: []
        }
    })
];

// ── Conversations & Patient Letters ─────────────────────────
// conversationId groups related messages. direction = 'to_patient' | 'from_patient'
let _nextLetterId = 200;
function _l(id, patientId, conversationId, direction, subject, body, opts) {
    return {
        id,
        patientId,
        conversationId,
        direction,
        subject,
        body,
        category: opts?.category || null,
        senderId: direction === 'to_patient' ? (opts?.senderId || 'prov_1') : patientId,
        senderType: direction === 'to_patient' ? 'provider' : 'patient',
        attachments: opts?.attachments || [],
        postDate: opts?.postDate || null,
        sentAt: opts?.sentAt || new Date().toISOString(),
        readAt: opts?.readAt || null,
        isRead: opts?.isRead !== undefined ? opts.isRead : true,
        isDraft: opts?.isDraft || false,
        conversationState: opts?.conversationState || 'open',
        doNotAllowResponse: opts?.doNotAllowResponse || false,
        unreadAlertTimeframe: opts?.unreadAlertTimeframe || 'none',
        printHeader: opts?.printHeader || 'default'
    };
}

const PATIENT_LETTERS = [
    // Conversation 1: James Rodriguez - prescription refill (open)
    _l('ltr_1', 'pat_1', 'conv_1', 'from_patient', 'Prescription Refill', 'Hi Dr. Chen, I\'m running low on my Metformin prescription. Can I get a refill? I have about 5 days left. Thank you!', {
        category: 'Prescription Refill', sentAt: '2026-02-25T10:15:00Z', readAt: '2026-02-25T11:00:00Z', isRead: true
    }),
    _l('ltr_2', 'pat_1', 'conv_1', 'to_patient', 'Re: Prescription Refill', 'Hi James, I\'ve sent a refill for your Metformin 500mg to your pharmacy on file (Walgreens on Market St). It should be ready for pickup tomorrow. Let me know if you need anything else.', {
        senderId: 'prov_1', sentAt: '2026-02-25T14:30:00Z', readAt: '2026-02-25T16:00:00Z', isRead: true
    }),
    _l('ltr_3', 'pat_1', 'conv_1', 'from_patient', 'Re: Prescription Refill', 'Thank you so much, Dr. Chen! I\'ll pick it up tomorrow. Also, I wanted to ask about my Lisinopril - should that be refilled at the same time?', {
        category: 'Prescription Refill', sentAt: '2026-02-25T16:20:00Z', readAt: '2026-02-26T08:00:00Z', isRead: true
    }),

    // Conversation 2: Emily Thompson - general question (open)
    _l('ltr_4', 'pat_2', 'conv_2', 'from_patient', 'General Question', 'Hello, I\'ve been experiencing some dizziness when standing up quickly over the past week. Is this something I should be concerned about? I\'m currently taking Sertraline 50mg.', {
        category: 'General Question', sentAt: '2026-02-26T09:30:00Z', isRead: false
    }),

    // Conversation 3: Robert Washington - test results (ended)
    _l('ltr_5', 'pat_3', 'conv_3', 'to_patient', 'Your Lab Results from Feb 15', 'Dear Mr. Washington, Your recent blood work results are in. Your INR is 2.4, which is within the therapeutic range. Your kidney function (GFR) is stable at 52. Your A1C is 7.1%, which shows improvement from last time. Keep up the good work with your diet changes. We\'ll recheck in 3 months.', {
        senderId: 'prov_2', sentAt: '2026-02-20T10:00:00Z', readAt: '2026-02-21T08:30:00Z', isRead: true,
        conversationState: 'ended',
        attachments: [{ name: 'Lab_Results_Feb2026.pdf', size: '245 KB' }]
    }),

    // Conversation 4: Sophia Nguyen - appointment request (open)
    _l('ltr_6', 'pat_4', 'conv_4', 'from_patient', 'Appointment Request', 'Hi, I need to schedule my annual thyroid check-up. I prefer a telehealth visit if possible. My schedule is flexible on Tuesdays and Thursdays. Thank you!', {
        category: 'Appointment Request', sentAt: '2026-02-27T11:00:00Z', isRead: false
    }),

    // Conversation 5: Linda Garcia - medication concern (open)
    _l('ltr_7', 'pat_6', 'conv_5', 'from_patient', 'Prescription Refill', 'Hello, I missed my Fluoxetine dose for 2 days because my pharmacy said my prescription expired. Can you please send a new prescription? I\'m starting to feel the withdrawal effects. Also, I need a refill on my Alendronate.', {
        category: 'Prescription Refill', sentAt: '2026-02-26T14:00:00Z', readAt: '2026-02-26T15:30:00Z', isRead: true
    }),
    _l('ltr_8', 'pat_6', 'conv_5', 'to_patient', 'Re: Prescription Refill', 'Hi Linda, I\'m sorry to hear about the lapse. I\'ve sent new prescriptions for both your Fluoxetine 20mg and Alendronate 70mg to CVS on Valencia Street. The Fluoxetine should be available today - please resume your normal dosing schedule. If withdrawal symptoms persist, please call our office.', {
        senderId: 'prov_3', sentAt: '2026-02-26T16:00:00Z', readAt: '2026-02-26T17:30:00Z', isRead: true
    }),

    // Conversation 6: Patricia O'Brien - visit summary sent (ended)
    _l('ltr_9', 'pat_8', 'conv_6', 'to_patient', 'Visit Summary - February 18, 2026', 'Dear Mrs. O\'Brien, Here is your visit summary from your appointment on February 18th. We discussed your diabetes management and adjusted your insulin dosing. Your A1C has improved to 7.5% from 8.1%. Please continue with the new insulin schedule and we\'ll check again in 3 months.', {
        senderId: 'prov_1', sentAt: '2026-02-18T17:00:00Z', readAt: '2026-02-19T09:00:00Z', isRead: true,
        conversationState: 'ended', doNotAllowResponse: true,
        attachments: [{ name: 'Visit_Summary_Feb18.pdf', size: '189 KB' }, { name: 'Insulin_Schedule.pdf', size: '52 KB' }]
    }),

    // Conversation 7: Helen Matsumoto - son managing care (open)
    _l('ltr_10', 'pat_10', 'conv_7', 'from_patient', 'General Question', 'This is Ken Matsumoto writing on behalf of my mother Helen. She has been more forgetful lately and had trouble recognizing my sister yesterday. Should we come in for an evaluation or is this expected with her condition?', {
        category: 'General Question', sentAt: '2026-02-27T15:00:00Z', isRead: false
    }),

    // Conversation 8: Kevin Adebayo - billing question (open)
    _l('ltr_11', 'pat_11', 'conv_8', 'from_patient', 'Billing Question', 'Hi, I received a bill for $247 from my last visit but my insurance usually covers the copay. Can someone look into this? My insurance info hasn\'t changed.', {
        category: 'Billing Question', sentAt: '2026-02-24T13:00:00Z', readAt: '2026-02-24T14:30:00Z', isRead: true
    }),
    _l('ltr_12', 'pat_11', 'conv_8', 'to_patient', 'Re: Billing Question', 'Hi Kevin, I\'ve forwarded your billing concern to our front desk team. They\'ll review your claim and insurance information. You should hear back within 2-3 business days. If you don\'t, please call our office at (555) 234-5678.', {
        senderId: 'prov_4', sentAt: '2026-02-24T16:00:00Z', readAt: '2026-02-25T08:00:00Z', isRead: true
    }),

    // Conversation 9: Maria Gonzalez - test results (open)
    _l('ltr_13', 'pat_14', 'conv_9', 'to_patient', 'Resultados de laboratorio - Febrero 2026', 'Estimada Maria, Los resultados de su examen de sangre están listos. Su nivel de azúcar en ayunas es 118 mg/dL (el rango normal es menos de 100). Esto indica que todavía estamos en el rango de pre-diabetes. Continúe con la dieta y el ejercicio. Revisaremos nuevamente en 3 meses.', {
        senderId: 'prov_1', sentAt: '2026-02-22T10:00:00Z', readAt: '2026-02-23T11:00:00Z', isRead: true,
        unreadAlertTimeframe: '48_hours',
        attachments: [{ name: 'Lab_Results_Feb2026.pdf', size: '198 KB' }]
    }),
    _l('ltr_14', 'pat_14', 'conv_9', 'from_patient', 'General Question', 'Gracias Dr. Chen. I have been walking 30 minutes every day. Should I also cut carbs more? What about the Metformin - do I still need it?', {
        category: 'General Question', sentAt: '2026-02-23T14:00:00Z', readAt: '2026-02-24T08:30:00Z', isRead: true
    }),

    // Conversation 10: Diane Foster-Hutchinson - referral request (open)
    _l('ltr_15', 'pat_16', 'conv_10', 'from_patient', 'Referral Request', 'Dr. Chen, my allergist Dr. Martin retired and I need a referral to a new allergist. I need someone who can manage my bee venom allergy and do annual testing. Preferably someone in the SF area. Thank you.', {
        category: 'Referral Request', sentAt: '2026-02-26T11:00:00Z', isRead: false
    }),

    // Conversation 11: Thomas Nakamura - follow-up (ended)
    _l('ltr_16', 'pat_17', 'conv_11', 'to_patient', 'Follow-up: Cardiology Appointment', 'Mr. Nakamura, this is a follow-up regarding your cardiology visit on Feb 10. Dr. Patel has recommended continuing your current Eliquis and Amiodarone regimen. Your next cardiac monitoring is scheduled for May. Please keep your INR checks on schedule. Call if you experience any palpitations or dizziness.', {
        senderId: 'prov_2', sentAt: '2026-02-15T09:00:00Z', readAt: '2026-02-16T10:30:00Z', isRead: true,
        conversationState: 'ended'
    }),

    // Conversation 12: Sarah Williams - pediatric vaccine reminder (ended)
    _l('ltr_17', 'pat_18', 'conv_12', 'to_patient', 'Vaccine Reminder', 'Dear Jennifer (parent/guardian of Sarah), This is a reminder that Sarah is due for her HPV dose 3 vaccination. Please schedule an appointment at your earliest convenience. The third dose should be given 6-12 months after the first dose.', {
        senderId: 'prov_1', sentAt: '2026-02-10T10:00:00Z', readAt: '2026-02-12T09:00:00Z', isRead: true,
        conversationState: 'ended', doNotAllowResponse: false
    }),
    _l('ltr_18', 'pat_18', 'conv_12', 'from_patient', 'General Question', 'Hi Dr. Chen, this is Jennifer Williams. I\'d like to schedule Sarah\'s HPV dose 3. Are there any openings next week? Also, she\'s been complaining about nasal congestion again - should we adjust her Fluticasone?', {
        category: 'General Question', sentAt: '2026-02-13T11:00:00Z', readAt: '2026-02-13T14:00:00Z', isRead: true
    }),

    // Conversation 13: Priya Sharma - medical records request (open)
    _l('ltr_19', 'pat_32', 'conv_13', 'from_patient', 'Medical Records Request', 'Hi, I\'m applying for life insurance and need copies of my medical records from the past 5 years. How do I request these? Is there a form I need to fill out? Thank you.', {
        category: 'Medical Records Request', sentAt: '2026-02-27T09:00:00Z', isRead: false
    }),

    // Conversation 14: Janet Okonkwo - diabetes management (open)
    _l('ltr_20', 'pat_30', 'conv_14', 'from_patient', 'General Question', 'Dr. Chen, my blood sugar has been running higher than usual this week (200-250 fasting). I haven\'t changed my diet or insulin routine. I also have a slight cold. Could that be causing it? Should I adjust my insulin?', {
        category: 'General Question', sentAt: '2026-02-28T08:00:00Z', isRead: false
    }),

    // Conversation 15: Rachel Steinberg - appointment scheduling (ended)
    _l('ltr_21', 'pat_12', 'conv_15', 'from_patient', 'Appointment Request', 'Hi, I need to schedule a follow-up appointment to discuss my medication. I\'ve been feeling much better on the Escitalopram and would like to discuss potentially tapering down.', {
        category: 'Appointment Request', sentAt: '2026-02-20T10:00:00Z', readAt: '2026-02-20T11:30:00Z', isRead: true
    }),
    _l('ltr_22', 'pat_12', 'conv_15', 'to_patient', 'Re: Appointment Request', 'Hi Rachel, I\'m glad to hear you\'re feeling better! I\'ve asked our front desk to schedule you for a follow-up. They\'ll reach out with available times. Please note that any medication changes should be made gradually, so we\'ll discuss a tapering plan at the appointment.', {
        senderId: 'prov_3', sentAt: '2026-02-20T14:00:00Z', readAt: '2026-02-20T15:00:00Z', isRead: true,
        conversationState: 'ended'
    }),

    // Conversation 16: Andrew McIntyre - telehealth question (open)
    _l('ltr_23', 'pat_29', 'conv_16', 'from_patient', 'General Question', 'Dr. Torres, I\'ve been having more acid reflux episodes despite the Omeprazole. The burning is worse at night. I elevated my bed like you suggested. Can we do a telehealth visit to discuss this?', {
        category: 'General Question', sentAt: '2026-02-27T20:00:00Z', isRead: false
    }),

    // Conversation 17: Deborah Takahashi - medication question (open)
    _l('ltr_24', 'pat_50', 'conv_17', 'from_patient', 'Prescription Refill', 'Good morning Dr. Chen, I need refills on my Amlodipine and Omeprazole. I\'m also wondering if I should switch to a different calcium supplement - the current one causes some stomach upset.', {
        category: 'Prescription Refill', sentAt: '2026-02-28T09:30:00Z', isRead: false
    }),

    // Conversation 18: Gregory Abrams - follow-up after echo (ended)
    _l('ltr_25', 'pat_41', 'conv_18', 'to_patient', 'Echocardiogram Results', 'Dear Mr. Abrams, Your echocardiogram results show stable mitral valve prolapse with mild mitral regurgitation, unchanged from last year. No intervention is needed at this time. We\'ll repeat the echo in 12 months. Continue your current medications.', {
        senderId: 'prov_2', sentAt: '2026-02-15T11:00:00Z', readAt: '2026-02-16T09:00:00Z', isRead: true,
        conversationState: 'ended',
        attachments: [{ name: 'Echo_Report_Feb2026.pdf', size: '312 KB' }]
    }),

    // Conversation 19: Olivia Chen - new patient welcome (ended)
    _l('ltr_26', 'pat_26', 'conv_19', 'to_patient', 'Welcome to Bay Area Family Medicine', 'Dear Olivia, Welcome to our practice! I\'m Dr. Chen and I\'ll be your primary care provider. I\'ve reviewed the records transferred from your previous physician. Let\'s schedule your initial visit to go over your health history and current medications. Please bring your insurance card and a list of any supplements you take.', {
        senderId: 'prov_1', sentAt: '2025-10-22T10:00:00Z', readAt: '2025-10-22T14:00:00Z', isRead: true,
        conversationState: 'ended', doNotAllowResponse: false
    }),

    // Conversation 20: Frank DeLuca - test results (open)
    _l('ltr_27', 'pat_19', 'conv_20', 'to_patient', 'PSA Test Results', 'Mr. DeLuca, your PSA level came back at 3.2 ng/mL, which is within the normal range for your age. This is consistent with your BPH. We\'ll continue annual monitoring. No biopsy is needed at this time.', {
        senderId: 'prov_4', sentAt: '2026-02-24T09:00:00Z', readAt: '2026-02-24T11:00:00Z', isRead: true,
        unreadAlertTimeframe: '48_hours'
    }),
    _l('ltr_28', 'pat_19', 'conv_20', 'from_patient', 'General Question', 'Thank you Dr. Kim. That\'s a relief. Quick question - my urinary symptoms seem to be getting a bit worse. Is it worth increasing the Tamsulosin?', {
        category: 'General Question', sentAt: '2026-02-25T10:00:00Z', readAt: '2026-02-25T14:00:00Z', isRead: true
    }),

    // Conversation 21: Christine Lee - new message (unread)
    _l('ltr_29', 'pat_22', 'conv_21', 'from_patient', 'General Question', 'Hi, I\'ve been having trouble sleeping even with the Trazodone. I\'m only getting about 4-5 hours a night. My mood has been okay on the Bupropion but the insomnia is really affecting my daily functioning. Any suggestions?', {
        category: 'General Question', sentAt: '2026-02-28T22:00:00Z', isRead: false
    }),

    // Conversation 22: Aisha Patel - prenatal care (open)
    _l('ltr_30', 'pat_20', 'conv_22', 'to_patient', 'Prenatal Visit Reminder', 'Hi Aisha, Just a reminder about your 32-week prenatal checkup next Tuesday. We\'ll do a growth ultrasound and glucose tolerance re-check. Please drink plenty of water before the appointment. If you have any concerns before then, don\'t hesitate to message us.', {
        senderId: 'prov_3', sentAt: '2026-02-26T09:00:00Z', readAt: '2026-02-26T10:00:00Z', isRead: true
    }),
    _l('ltr_31', 'pat_20', 'conv_22', 'from_patient', 'General Question', 'Thank you! I\'ll be there. I have been experiencing some swelling in my ankles - is this normal at this stage?', {
        category: 'General Question', sentAt: '2026-02-26T12:00:00Z', readAt: '2026-02-26T14:00:00Z', isRead: true
    }),

    // Conversation 23: Nancy Yamamoto - osteoporosis follow-up (ended)
    _l('ltr_32', 'pat_24', 'conv_23', 'to_patient', 'DEXA Scan Results', 'Dear Nancy, Your DEXA scan results show a T-score of -2.8 at the lumbar spine. This is in the osteoporosis range. I\'d like to continue your Alendronate and Calcium/Vitamin D regimen. We should discuss weight-bearing exercises at your next visit. Please avoid heavy lifting.', {
        senderId: 'prov_1', sentAt: '2026-02-10T09:00:00Z', readAt: '2026-02-11T10:00:00Z', isRead: true,
        conversationState: 'ended',
        attachments: [{ name: 'DEXA_Scan_Results_2026.pdf', size: '156 KB' }]
    }),

    // Conversation 24: Howard Blackwell - cardiac follow-up (open)
    _l('ltr_33', 'pat_27', 'conv_24', 'to_patient', 'Pacemaker Check Results', 'Mr. Blackwell, your pacemaker interrogation from Feb 20 looks good. Battery life is at 68%, estimated 5+ years remaining. No abnormal episodes detected. Your heart failure medications appear to be working well - BNP is down to 380 from 520.', {
        senderId: 'prov_4', sentAt: '2026-02-22T10:00:00Z', readAt: '2026-02-23T09:00:00Z', isRead: true,
        attachments: [{ name: 'Pacemaker_Report_Feb2026.pdf', size: '278 KB' }]
    }),
    _l('ltr_34', 'pat_27', 'conv_24', 'from_patient', 'General Question', 'Thank you Dr. Kim. My wife wants to know if I can start light gardening again this spring. I feel up to it but want to make sure it\'s safe.', {
        category: 'General Question', sentAt: '2026-02-24T11:00:00Z', readAt: '2026-02-24T15:00:00Z', isRead: true
    }),

    // Conversation 25: Draft letter to Martha Reeves-Whitfield
    _l('ltr_35', 'pat_36', 'conv_25', 'to_patient', 'Annual Wellness Visit Summary', 'Dear Mrs. Reeves-Whitfield, Thank you for coming in for your annual wellness visit on February 27th. We reviewed your medications and discussed fall prevention strategies. Your diabetes control has improved - A1C is now 7.3%. I recommend:', {
        senderId: 'prov_1', isDraft: true, sentAt: null
    }),

    // Conversation 26: Russell Keane - test results (open)
    _l('ltr_36', 'pat_49', 'conv_26', 'to_patient', 'Lab Results - Kidney Function', 'Mr. Keane, your kidney function tests came back with slightly elevated creatinine at 1.4. Your GFR is 58. While this is still in acceptable range, I\'d like to monitor more closely. Please reduce your NSAID use and increase water intake. We\'ll recheck in 6 weeks.', {
        senderId: 'prov_2', sentAt: '2026-02-21T10:00:00Z', readAt: '2026-02-22T08:00:00Z', isRead: true,
        unreadAlertTimeframe: '72_hours'
    }),

    // Conversation 27: Catherine Morales - thyroid follow-up
    _l('ltr_37', 'pat_46', 'conv_27', 'to_patient', 'Thyroid Function Update', 'Hi Catherine, your recent TSH is 4.2 mIU/L, which is slightly above the target range. I\'d like to increase your Levothyroxine from 50mcg to 75mcg. I\'ll send the new prescription to your pharmacy. Please get a recheck TSH in 6 weeks.', {
        senderId: 'prov_1', sentAt: '2026-02-25T09:00:00Z', readAt: '2026-02-25T12:00:00Z', isRead: true
    }),
    _l('ltr_38', 'pat_46', 'conv_27', 'from_patient', 'General Question', 'Thank you Dr. Chen. Should I take the new dose on an empty stomach like before? And is the Vitamin D still important?', {
        category: 'General Question', sentAt: '2026-02-25T14:00:00Z', readAt: '2026-02-26T08:00:00Z', isRead: true
    }),

    // Conversation 28: Susan Cho - telehealth follow-up (open)
    _l('ltr_39', 'pat_40', 'conv_28', 'from_patient', 'Appointment Request', 'Hi, my urticaria has flared up again and the Loratadine isn\'t helping much. Can I schedule a telehealth visit? I can send photos of the hives.', {
        category: 'Appointment Request', sentAt: '2026-02-28T10:00:00Z', isRead: false
    }),

    // Conversation 29: David Park - asthma check-in (ended)
    _l('ltr_40', 'pat_7', 'conv_29', 'to_patient', 'Asthma Action Plan Review', 'Hi David, I wanted to check in on your asthma management. Your last spirometry showed good control. Please continue your Montelukast daily and use your rescue inhaler as needed. Remember to get a flu shot each year as respiratory infections can worsen asthma.', {
        senderId: 'prov_4', sentAt: '2026-02-18T10:00:00Z', readAt: '2026-02-19T11:00:00Z', isRead: true,
        conversationState: 'ended',
        attachments: [{ name: 'Asthma_Action_Plan_2026.pdf', size: '95 KB' }]
    }),

    // Additional older conversations for depth
    _l('ltr_41', 'pat_1', 'conv_30', 'to_patient', 'A1C Results - January 2026', 'James, your A1C came back at 7.0%. This is excellent and shows great improvement from 7.8% last time. Your diabetes management is on track. Keep up the dietary changes and exercise routine.', {
        senderId: 'prov_1', sentAt: '2026-01-20T10:00:00Z', readAt: '2026-01-20T15:00:00Z', isRead: true,
        conversationState: 'ended'
    }),
    _l('ltr_42', 'pat_4', 'conv_31', 'to_patient', 'Thyroid Medication Adjustment', 'Sophia, your TSH is now 2.1, which is well within the normal range on Levothyroxine 75mcg. We\'ll continue the current dose. Next thyroid panel in 6 months.', {
        senderId: 'prov_1', sentAt: '2025-12-15T09:00:00Z', readAt: '2025-12-15T14:00:00Z', isRead: true,
        conversationState: 'ended'
    }),
    _l('ltr_43', 'pat_8', 'conv_32', 'from_patient', 'Prescription Refill', 'Dr. Chen, I need refills on all my medications: Losartan, Metformin, Ezetimibe, Aspirin, and Insulin glargine. My pharmacy is CVS on Geary Blvd.', {
        category: 'Prescription Refill', sentAt: '2026-01-05T10:00:00Z', readAt: '2026-01-05T11:00:00Z', isRead: true,
        conversationState: 'ended'
    }),
    _l('ltr_44', 'pat_8', 'conv_32', 'to_patient', 'Re: Prescription Refill', 'Patricia, all refills have been sent to CVS on Geary Blvd. They should be ready by tomorrow. I also want to check your kidney function at your next visit, so please schedule a lab draw.', {
        senderId: 'prov_1', sentAt: '2026-01-05T14:00:00Z', readAt: '2026-01-06T09:00:00Z', isRead: true,
        conversationState: 'ended'
    }),

    // Conversation 33: Bulk letter - flu shot reminder (ended)
    _l('ltr_45', 'pat_1', 'conv_33', 'to_patient', 'Flu Season Reminder', 'Dear Patient, This is a reminder that flu season is here. If you haven\'t received your flu vaccine yet, please schedule an appointment or visit your nearest pharmacy. The flu vaccine is especially important for patients with chronic conditions.', {
        senderId: 'prov_1', sentAt: '2025-10-01T08:00:00Z', readAt: '2025-10-02T09:00:00Z', isRead: true,
        conversationState: 'ended', doNotAllowResponse: true
    }),

    // More unread letters for inbox depth
    _l('ltr_46', 'pat_35', 'conv_34', 'from_patient', 'General Question', 'Dr. Kim, I\'ve been experiencing increased thirst and urination. My last A1C was 7.8%. Should I be concerned about my blood sugar control? I\'ve been trying to eat better.', {
        category: 'General Question', sentAt: '2026-02-28T14:00:00Z', isRead: false
    }),
    _l('ltr_47', 'pat_38', 'conv_35', 'from_patient', 'Test Results', 'Hi Dr. Chen, I got my blood work done last week but haven\'t heard back about the results. Can you let me know how my B12 and iron levels are looking?', {
        category: 'Test Results', sentAt: '2026-02-28T11:30:00Z', isRead: false
    })
];

// ── Appointments ────────────────────────────────────────────
const APPOINTMENTS = [
    { id: 'appt_1', patientId: 'pat_1', providerId: 'prov_1', date: '2026-03-05T10:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Diabetes follow-up' },
    { id: 'appt_2', patientId: 'pat_4', providerId: 'prov_1', date: '2026-03-04T14:00:00Z', place: 'virtual', status: 'scheduled', virtualVisitInstructions: 'Join at https://zoom.us/j/9384752610?pwd=abc123', reason: 'Thyroid check-up' },
    { id: 'appt_3', patientId: 'pat_3', providerId: 'prov_2', date: '2026-03-10T09:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Warfarin check / INR' },
    { id: 'appt_4', patientId: 'pat_10', providerId: 'prov_1', date: '2026-03-06T11:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Cognitive assessment follow-up' },
    { id: 'appt_5', patientId: 'pat_20', providerId: 'prov_3', date: '2026-03-03T10:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: '32-week prenatal checkup' },
    { id: 'appt_6', patientId: 'pat_29', providerId: 'prov_2', date: '2026-03-07T15:00:00Z', place: 'virtual', status: 'scheduled', virtualVisitInstructions: 'Join at https://zoom.us/j/7261048395?pwd=def456', reason: 'GI follow-up' },
    { id: 'appt_7', patientId: 'pat_8', providerId: 'prov_1', date: '2026-03-12T09:30:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Kidney function labs review' },
    { id: 'appt_8', patientId: 'pat_17', providerId: 'prov_2', date: '2026-05-15T10:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Cardiac monitoring' },
    { id: 'appt_9', patientId: 'pat_27', providerId: 'prov_4', date: '2026-03-15T14:00:00Z', place: 'virtual', status: 'scheduled', virtualVisitInstructions: 'Join at https://zoom.us/j/5029384716?pwd=ghi789', reason: 'CHF management review' },
    { id: 'appt_10', patientId: 'pat_12', providerId: 'prov_3', date: '2026-03-08T11:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Medication review' },
    { id: 'appt_11', patientId: 'pat_14', providerId: 'prov_1', date: '2026-03-20T10:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Pre-diabetes follow-up' },
    { id: 'appt_12', patientId: 'pat_36', providerId: 'prov_1', date: '2026-03-03T14:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Annual wellness visit follow-up' },
    { id: 'appt_13', patientId: 'pat_30', providerId: 'prov_1', date: '2026-03-04T09:00:00Z', place: 'virtual', status: 'scheduled', virtualVisitInstructions: 'Join at https://zoom.us/j/9384752610?pwd=abc123', reason: 'Urgent: Blood sugar management' },
    { id: 'appt_14', patientId: 'pat_40', providerId: 'prov_3', date: '2026-03-05T15:00:00Z', place: 'virtual', status: 'scheduled', virtualVisitInstructions: 'Join at https://zoom.us/j/3948271605?pwd=jkl012', reason: 'Urticaria flare evaluation' },
    { id: 'appt_15', patientId: 'pat_47', providerId: 'prov_4', date: '2026-03-18T10:00:00Z', place: 'in_person', status: 'scheduled', virtualVisitInstructions: null, reason: 'Blood pressure management' },
    // Past appointments
    { id: 'appt_16', patientId: 'pat_1', providerId: 'prov_1', date: '2026-02-05T10:00:00Z', place: 'in_person', status: 'completed', virtualVisitInstructions: null, reason: 'A1C review' },
    { id: 'appt_17', patientId: 'pat_8', providerId: 'prov_1', date: '2026-02-18T09:30:00Z', place: 'in_person', status: 'completed', virtualVisitInstructions: null, reason: 'Diabetes management visit' },
    { id: 'appt_18', patientId: 'pat_3', providerId: 'prov_2', date: '2026-02-15T09:00:00Z', place: 'in_person', status: 'completed', virtualVisitInstructions: null, reason: 'Lab review - INR, kidney function' },
    { id: 'appt_19', patientId: 'pat_17', providerId: 'prov_2', date: '2026-02-10T10:00:00Z', place: 'in_person', status: 'completed', virtualVisitInstructions: null, reason: 'Cardiology follow-up' },
    { id: 'appt_20', patientId: 'pat_27', providerId: 'prov_4', date: '2026-02-20T14:00:00Z', place: 'in_person', status: 'completed', virtualVisitInstructions: null, reason: 'Pacemaker interrogation' }
];

// ── Reminders (Unread Alert Notifications) ──────────────────
const REMINDERS = [
    { id: 'rem_1', type: 'unread_alert', patientLetterId: 'ltr_13', patientId: 'pat_14', createdAt: '2026-02-24T10:00:00Z', acknowledged: false, description: 'Maria Gonzalez has not read "Resultados de laboratorio" sent on Feb 22' },
    { id: 'rem_2', type: 'unread_alert', patientLetterId: 'ltr_27', patientId: 'pat_19', createdAt: '2026-02-26T09:00:00Z', acknowledged: false, description: 'Frank DeLuca read "PSA Test Results" but follow-up response pending' },
    { id: 'rem_3', type: 'unread_alert', patientLetterId: 'ltr_36', patientId: 'pat_49', createdAt: '2026-02-24T10:00:00Z', acknowledged: true, description: 'Russell Keane has read "Lab Results - Kidney Function"' },
    { id: 'rem_4', type: 'appointment_reminder', patientId: 'pat_20', createdAt: '2026-03-02T08:00:00Z', acknowledged: false, description: 'Aisha Patel - 32-week prenatal checkup tomorrow at 10:00 AM' },
    { id: 'rem_5', type: 'appointment_reminder', patientId: 'pat_36', createdAt: '2026-03-02T08:00:00Z', acknowledged: false, description: 'Martha Reeves-Whitfield - Annual wellness visit follow-up tomorrow at 2:00 PM' },
    { id: 'rem_6', type: 'unread_alert', patientLetterId: 'ltr_37', patientId: 'pat_46', createdAt: '2026-02-27T09:00:00Z', acknowledged: false, description: 'Catherine Morales has read "Thyroid Function Update" - response received' },
    { id: 'rem_7', type: 'passport_invitation', patientId: 'pat_5', createdAt: '2026-02-15T11:00:00Z', acknowledged: false, description: 'Marcus Johnson invited to Passport on Jan 15 - still not registered' },
    { id: 'rem_8', type: 'passport_invitation', patientId: 'pat_13', createdAt: '2026-02-20T09:00:00Z', acknowledged: false, description: 'William Chang invited to Passport on Feb 1 - still not registered' },
    { id: 'rem_9', type: 'appointment_reminder', patientId: 'pat_4', createdAt: '2026-03-02T08:00:00Z', acknowledged: false, description: 'Sophia Nguyen - Telehealth thyroid check-up on Mar 4 at 2:00 PM' },
    { id: 'rem_10', type: 'appointment_reminder', patientId: 'pat_1', createdAt: '2026-03-02T08:00:00Z', acknowledged: false, description: 'James Rodriguez - Diabetes follow-up on Mar 5 at 10:00 AM' }
];

// ── Bulk Letters ────────────────────────────────────────────
const BULK_LETTERS = [
    {
        id: 'bulk_1',
        description: 'Flu season reminder 2025',
        subject: 'Flu Season Reminder',
        body: 'Dear Patient, This is a reminder that flu season is here. If you haven\'t received your flu vaccine yet, please schedule an appointment or visit your nearest pharmacy. The flu vaccine is especially important for patients with chronic conditions.',
        sentAt: '2025-10-01T08:00:00Z',
        sentBy: 'prov_1',
        targetCount: 42,
        allowResponse: false
    },
    {
        id: 'bulk_2',
        description: 'Holiday office hours notification',
        subject: 'Holiday Office Hours',
        body: 'Dear Patient, Our office will have modified hours during the holiday season. Dec 24-25: Closed. Dec 31-Jan 1: Closed. All other days: Normal hours (8 AM - 5 PM). For urgent needs, please call our after-hours line at (555) 234-9999.',
        sentAt: '2025-12-15T09:00:00Z',
        sentBy: 'prov_5',
        targetCount: 50,
        allowResponse: false
    },
    {
        id: 'bulk_3',
        description: 'Patient portal reminder',
        subject: 'Access Your Health Records Online',
        body: 'Dear Patient, Did you know you can access your health records, message your doctor, and manage appointments through Patient Passport? Sign up today at our front desk or through the link in your invitation email. It\'s free, secure, and available 24/7.',
        sentAt: '2026-01-10T10:00:00Z',
        sentBy: 'prov_1',
        targetCount: 15,
        allowResponse: true
    }
];

// ── Visit Summaries ─────────────────────────────────────────
const VISIT_SUMMARIES = [
    {
        id: 'vs_1', patientId: 'pat_1', providerId: 'prov_1', date: '2026-02-05T10:00:00Z',
        category: 'Office Visit', signed: true,
        vitals: { bp: '128/82', hr: 72, temp: '98.4 F', weight: '185 lbs', bmi: 27.2 },
        procedures: ['Finger stick glucose: 142 mg/dL'],
        treatments: ['Continue Metformin 500mg BID', 'Continue Lisinopril 10mg daily', 'Continue Atorvastatin 20mg daily'],
        carePlan: 'A1C improved to 7.0%. Continue current regimen. Dietary counseling provided. Next A1C in 3 months.',
        followUp: '3 months - A1C recheck'
    },
    {
        id: 'vs_2', patientId: 'pat_8', providerId: 'prov_1', date: '2026-02-18T09:30:00Z',
        category: 'Office Visit', signed: true,
        vitals: { bp: '135/85', hr: 68, temp: '98.2 F', weight: '172 lbs', bmi: 28.5 },
        procedures: ['Comprehensive metabolic panel ordered', 'Urine microalbumin ordered'],
        treatments: ['Adjust insulin glargine: increase from 18 to 20 units nightly', 'Continue other medications'],
        carePlan: 'A1C 7.5%, improved from 8.1%. Adjusted insulin. Monitor kidney function. Referred to podiatry for neuropathy screening.',
        followUp: '3 months - labs and follow-up'
    },
    {
        id: 'vs_3', patientId: 'pat_3', providerId: 'prov_2', date: '2026-02-15T09:00:00Z',
        category: 'Office Visit', signed: true,
        vitals: { bp: '140/88', hr: 76, temp: '98.6 F', weight: '198 lbs', bmi: 30.1 },
        procedures: ['INR check: 2.4 (therapeutic)', 'Basic metabolic panel'],
        treatments: ['Continue Warfarin 5mg daily', 'Continue Metoprolol 25mg BID', 'Continue Amlodipine 5mg daily'],
        carePlan: 'INR therapeutic. GFR stable at 52. BP slightly elevated - consider medication adjustment if persistent.',
        followUp: '3 months - INR, CMP'
    },
    {
        id: 'vs_4', patientId: 'pat_17', providerId: 'prov_2', date: '2026-02-10T10:00:00Z',
        category: 'Office Visit', signed: true,
        vitals: { bp: '132/80', hr: 64, temp: '98.4 F', weight: '168 lbs', bmi: 24.8 },
        procedures: ['ECG: NSR with rare PACs'],
        treatments: ['Continue Eliquis 5mg BID', 'Continue Amiodarone 200mg daily'],
        carePlan: 'Stable on current antiarrhythmic regimen. No recurrent episodes of AF. Cardiology to repeat Holter in 3 months.',
        followUp: 'May - Cardiac monitoring'
    },
    {
        id: 'vs_5', patientId: 'pat_27', providerId: 'prov_4', date: '2026-02-20T14:00:00Z',
        category: 'Office Visit', signed: true,
        vitals: { bp: '124/76', hr: 62, temp: '97.9 F', weight: '162 lbs', bmi: 25.6 },
        procedures: ['Pacemaker interrogation', 'BNP level: 380 (down from 520)'],
        treatments: ['Continue current medications', 'Low sodium diet education'],
        carePlan: 'Pacemaker functioning well. Battery 68%. CHF compensation improving. BNP trending down. Continue diuretic management.',
        followUp: '1 month - telehealth check-in'
    }
];

// ── ID Counters ─────────────────────────────────────────────
const INITIAL_COUNTERS = {
    _nextPatientId: 51,
    _nextLetterId: 100,
    _nextConversationId: 40,
    _nextAppointmentId: 21,
    _nextReminderId: 11,
    _nextBulkLetterId: 4,
    _nextVisitSummaryId: 6,
    _nextLocationId: 4,
    _nextCptCodeId: 14
};
