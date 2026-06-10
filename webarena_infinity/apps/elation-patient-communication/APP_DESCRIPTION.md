# Elation Patient Communication — App Description

## Summary

This is a practice-side EHR (Electronic Health Records) portal for Elation Health focused on **Patient Communication**. It simulates the provider/staff view of a medical practice managing patient messaging (Patient Letters), Patient Passport (secure patient portal), appointment scheduling, telehealth (virtual visits), and practice settings. The logged-in user is Dr. Sarah Chen, a physician at Bay Area Family Medicine.

The app covers the workflows documented in Elation's Patient Passport, Patient Communication, Telehealth, and SMS Opt-In guides.

---

## Main Sections / Pages

### 1. Practice Home (Dashboard)
- **Route:** `#/home` (default)
- Shows three dashboard cards:
  - **Patient Letters** — recent incoming patient messages, with unread count badge
  - **Reminders** — unread alerts, appointment reminders, passport invitation reminders
  - **Upcoming Appointments** — next 5 scheduled appointments with virtual visit "Start Video" buttons

### 2. Patient Letters (Inbox)
- **Route:** `#/inbox`
- List of all incoming patient-to-provider messages sorted by date (newest first)
- Unread messages are visually highlighted (blue background, bold text)
- Click any message to open the conversation thread
- "New Letter" button opens compose overlay

### 3. Sent Letters
- **Route:** `#/sent`
- List of all provider-to-patient messages
- Shows conversation state (lock icon for ended conversations)

### 4. Drafts
- **Route:** `#/drafts`
- List of unsent draft letters
- Click to edit, send, or delete

### 5. Reminders
- **Route:** `#/reminders`
- All reminders with type badges (Unread Alert, Appointment, Passport)
- Actions per reminder type:
  - Unread Alert: Resend, Write Message, Acknowledge
  - Passport Invitation: View Patient, Acknowledge
  - Appointment: Acknowledge
- Acknowledged reminders shown as dimmed

### 6. Patients
- **Route:** `#/patients`
- Paginated table (20 per page) of all 50 patients
- **Filters:** Provider dropdown, Passport Status checkboxes (Registered/Invited/Not Invited), text search
- **Columns:** Name, Email, Phone, DOB, Provider, Passport Status, SMS Status, Tags
- **Bulk actions** (when patients selected): Send Bulk Letter, Send Passport Invitation
- Select all / individual selection via checkboxes

### 7. Patient Detail
- **Route:** `#/patient/{patientId}`
- Sub-sections:
  - **Demographics** — email, phone, DOB, provider, emergency contact, tags (add/remove), SMS opt-in status
  - **Patient Passport** — status badge, sharing level, invitation dates, invitation code (for invited patients), actions (Send Invite / Re-send / Disable)
  - **Clinical Profile** — allergies, drug intolerances, medications, vaccines, problem list, history (6-column grid)
  - **Patient Letters** — conversation history with this patient
  - **Appointments** — upcoming and past appointments
  - **Visit Summaries** — signed visit notes with clickable detail view
- **Passport Globe Button** — opens Passport Settings dialog (email, phone, sharing level, invite/save actions)
- **Write Letter** button — opens compose overlay pre-addressed to this patient

### 8. Conversation Detail
- **Route:** `#/conversation/{conversationId}/{patientId}`
- Threaded message view showing all messages in a conversation
- Provider messages have blue left border, patient messages have gray
- Each message shows sender, timestamp, category (if patient-initiated), body, attachments
- **Reply area** (if conversation is open and replies allowed):
  - Text area for reply
  - "Reply" button (sends reply)
  - "Sign Off & End Conversation" button (closes thread, prevents further replies)
- Viewing marks unread messages as read

### 9. Appointments
- **Route:** `#/appointments`
- Two sections: Upcoming and Past
- **Table columns:** Date, Time, Patient, Provider, Type (Virtual/In-person), Reason, Actions
- **Actions:** Start Video (virtual only), Cancel
- "New Appointment" button opens scheduling modal

### 10. Bulk Letters
- **Route:** `#/bulk-letters`
- History of sent bulk letters with description, subject, body preview, target count, sender
- "New Bulk Letter" button (requires patients to be selected from Patients page first)

### 11. Settings
- **Route:** `#/settings` or `#/settings/{tab}`
- **Tabs:**

#### User Settings (`#/settings/user`)
- Clinical Profile Sharing Default — dropdown with 4 levels
- Notification Preferences — Unread Letter Alert Timeframe dropdown

#### Admin Settings (`#/settings/admin`)
- Allow patients to send messages — toggle
- Auto-invite to Passport after online booking — toggle
- Booking Site URL display

#### Message Routing (`#/settings/routing`)
- Per-provider routing configuration
- Table: Message Category → Recipients (providers and/or user groups)
- Add/remove recipients per category
- "Update Routing for All Providers" bulk action

#### Telehealth (`#/settings/telehealth`)
- Per-provider virtual visit activation status
- Edit Virtual Visit Instructions per provider
- Activate/Deactivate virtual visits
- Video session settings: Screen sharing toggle, Chat mode dropdown, Waiting room audio toggle

#### Practice Locations (`#/settings/locations`)
- Table of practice locations with Name, Address, POS Code, POS Description
- Add/Edit/Remove locations

#### Billing Codes (`#/settings/billing`)
- Table of CPT codes with Code and Description
- Add/Remove codes

---

## Complete List of Implemented Features and UI Interactions

### Messaging
- Compose new letter to any patient (with patient search)
- Reply to patient messages within conversation threads
- Sign off and end conversations (prevents further replies)
- Mark messages as read when viewing conversation
- Save drafts, edit drafts, send drafts, delete drafts
- Set "Do not allow patient to respond" flag
- Set unread alert timeframe on outgoing letters
- View attachments on messages

### Patient Passport Management
- Send Passport invitation (with email, phone, sharing level)
- Re-send Passport invitation (regenerates invitation code)
- View invitation code for invited patients
- Disable Passport account for registered patients
- Update sharing level per patient
- Passport globe button on patient detail page opens settings dialog
- Bulk invite: select multiple uninvited patients and send invitations at once
- Four sharing levels with descriptions

### Patient Management
- Search patients by name, email, phone, or ID
- Filter by provider, passport status
- Paginated patient list (20 per page)
- View/edit patient demographics
- Add/remove patient tags from predefined list
- View SMS opt-in status
- Request SMS opt-in
- Bulk patient selection for bulk letters/invitations

### Bulk Letters
- Compose bulk letters with description, subject, body
- Toggle allowing patient responses
- Send to selected patients (creates individual letters)
- View history of sent bulk letters

### Appointments
- View upcoming and past appointments
- Schedule new appointment (patient search, date, time, provider, type, reason)
- Cancel appointments
- Virtual visit support: "Start Video" button shows video link
- Auto-populate virtual visit instructions from provider settings

### Reminders
- View all reminders sorted by status (unacknowledged first)
- Acknowledge reminders
- Resend letters from unread alert reminders
- Write new message from reminder
- Navigate to patient from passport reminders

### Settings
- Update provider sharing default (levels 1-4)
- Update notification timeframe
- Toggle patient messaging on/off
- Toggle booking site auto-invite
- Configure message routing per provider per category
- Add/remove routing recipients (providers or user groups)
- Bulk update routing for all providers
- Activate/deactivate virtual visits per provider
- Edit virtual visit instructions per provider
- Configure video session settings (screen sharing, chat mode, audio notification)
- Add/edit/remove practice locations with POS codes
- Add/remove CPT billing codes

### General UI
- Sidebar navigation with unread count badges
- Hash-based routing
- Responsive layout with collapsible sidebar
- Custom dropdowns (no native `<select>`)
- Custom toggle switches
- Custom modals for confirmations and forms
- Toast notifications for all actions
- Full state persistence to localStorage with seed data versioning
- SSE-based reset mechanism
- State push to server on every mutation

---

## Data Model

### Entities and Fields

#### Patient (50 records)
- `id` (pat_1..pat_50)
- `firstName`, `lastName`
- `email`
- `cellPhone`
- `dateOfBirth` (ISO date)
- `assignedProviderId` (FK to Provider)
- `passportStatus`: "registered" | "invited" | "not_invited"
- `smsOptInStatus`: "opted_in" | "opted_out" | "never"
- `tags` (array of strings from PATIENT_TAGS)
- `passportSharingLevel` (1-4)
- `passportAccountDisabled` (boolean)
- `invitedAt`, `registeredAt` (ISO datetime or null)
- `invitationCode` (7-digit string or null)
- `emergencyContact` ({ name, phone, relationship } or null)
- `clinicalProfile` ({ allergies[], drugIntolerances[], medications[], vaccines[], problemList[], history[], confidential[] })

#### Provider (5 records)
- `id` (prov_1..prov_5)
- `firstName`, `lastName`
- `email`
- `role`: "physician" | "nurse_practitioner" | "physician_assistant"
- `sharingDefault` (1-4)
- `notificationTimeframe`: "none" | "24_hours" | "48_hours" | "72_hours" | "1_week" | "2_weeks"
- `virtualVisitActivated` (boolean)
- `virtualVisitInstructions` (string)
- `isAdmin` (boolean)

#### Patient Letter (47 records)
- `id` (ltr_1..ltr_47)
- `patientId` (FK to Patient)
- `conversationId` (groups related messages)
- `direction`: "to_patient" | "from_patient"
- `subject`, `body`
- `category` (for patient-sent: from MESSAGE_CATEGORIES, or null)
- `senderId` (FK to Provider if to_patient, patientId if from_patient)
- `senderType`: "provider" | "patient"
- `attachments` (array of { name, size })
- `sentAt`, `readAt` (ISO datetime or null)
- `isRead` (boolean)
- `isDraft` (boolean)
- `conversationState`: "open" | "ended"
- `doNotAllowResponse` (boolean)
- `unreadAlertTimeframe` (string)
- `printHeader` (string)

#### Appointment (20 records)
- `id` (appt_1..appt_20)
- `patientId`, `providerId`
- `date` (ISO datetime)
- `place`: "virtual" | "in_person"
- `status`: "scheduled" | "completed" | "cancelled"
- `virtualVisitInstructions` (string or null)
- `reason` (string)

#### Reminder (10 records)
- `id` (rem_1..rem_10)
- `type`: "unread_alert" | "appointment_reminder" | "passport_invitation"
- `patientLetterId` (FK, for unread_alert)
- `patientId`
- `createdAt`
- `acknowledged` (boolean)
- `description` (string)

#### Bulk Letter (3 records)
- `id`, `description`, `subject`, `body`
- `sentAt`, `sentBy` (FK to Provider)
- `targetCount`, `allowResponse`

#### Visit Summary (5 records)
- `id`, `patientId`, `providerId`
- `date`, `category`, `signed`
- `vitals` ({ bp, hr, temp, weight, bmi })
- `procedures[]`, `treatments[]`
- `carePlan`, `followUp`

#### User Group (4 records)
- `id`, `name`, `memberIds[]`

#### Practice Settings (singleton)
- `practiceName`, `practicePhone`, `practiceAddress`
- `allowPatientMessaging` (boolean)
- `bookingSiteAutoInvite` (boolean)
- `bookingSiteUrl`
- `practiceLocations[]` ({ id, name, address, posCode, posDescription })
- `cptCodes[]` ({ code, description })
- `videoSettings` ({ screenSharingPatients, chatMode, waitingRoomAudioNotification })

#### Message Routing
- Keyed by providerId → category → recipient IDs array
- Recipients can be provider IDs or user group IDs

### Relationships
- Patient → Provider (assignedProviderId, many-to-one)
- Patient Letter → Patient (patientId)
- Patient Letter → Provider (senderId for to_patient)
- Patient Letter → Conversation (conversationId groups)
- Appointment → Patient + Provider
- Reminder → Patient, optionally → Patient Letter
- Visit Summary → Patient + Provider
- Message Routing → Provider × Category → Recipients (providers/groups)
- User Group → Provider members

---

## Navigation Structure

```
Sidebar:
├── Practice Home          #/home
├── Patient Letters        #/inbox
├── Sent                   #/sent
├── Drafts                 #/drafts
├── Reminders              #/reminders
├── ──────────────
├── Patients               #/patients
│   └── Patient Detail     #/patient/{id}
│       └── Conversation   #/conversation/{convId}/{patId}
├── Appointments           #/appointments
├── Bulk Letters           #/bulk-letters
├── ──────────────
└── Settings               #/settings
    ├── User Settings      #/settings/user
    ├── Admin Settings     #/settings/admin
    ├── Message Routing    #/settings/routing
    ├── Telehealth         #/settings/telehealth
    ├── Practice Locations #/settings/locations
    └── Billing Codes      #/settings/billing
```

---

## Available Form Controls, Dropdowns, Toggles, and Their Options

### Dropdowns
| ID | Location | Options |
|---|---|---|
| `providerFilter` | Patients page | All Providers, Sarah Chen, Michael Torres, Jessica Okafor, Robert Kim, Amanda Wright |
| `sharingDefault` | User Settings | Level 1: Objective Data Only, Level 2: Objective Data & Problem List, Level 3: Clinical Profile excludes Confidential, Level 4: Clinical Profile Expanded Summary |
| `notificationTimeframe` | User Settings | Do not notify me, 24 hours, 48 hours, 72 hours, 1 week, 2 weeks |
| `passportSharingLevel` | Passport Dialog | Same 4 levels as sharingDefault |
| `composeUnreadAlert` | Compose Letter | Same options as notificationTimeframe |
| `routingProvider` | Message Routing settings | All 5 providers |
| `chatMode` | Telehealth settings | Everyone in Meeting, Everyone in Waiting Room, Host Only |
| `apptProvider` | New Appointment modal | All 5 providers |
| `apptPlace` | New Appointment modal | In-person, Virtual |

### Toggles
| ID | Location | Default |
|---|---|---|
| `allowPatientMessaging` | Admin Settings | true (enabled) |
| `bookingSiteAutoInvite` | Admin Settings | true (enabled) |
| `screenSharingPatients` | Telehealth Settings | true (enabled) |
| `waitingRoomAudioNotification` | Telehealth Settings | true (enabled) |

### Checkboxes
| ID | Location | Purpose |
|---|---|---|
| `filter-registered` | Patient list filters | Filter passport status: Registered |
| `filter-invited` | Patient list filters | Filter passport status: Invited |
| `filter-not_invited` | Patient list filters | Filter passport status: Not Invited |
| `composeNoReply` | Compose letter | "Do not allow patient to respond" |
| `bulkAllowResponse` | Bulk letter compose | "Allow patients to respond" |
| `selectAllPatients` | Patient table header | Select/deselect all on page |

---

## Seed Data Summary

### Patients (50)
- **Registered:** 37 patients (74%)
- **Invited (not registered):** 6 patients (12%)
- **Not invited:** 7 patients (14%)
- **SMS Opted In:** 35 patients
- **SMS Opted Out:** 6 patients
- **SMS Never:** 9 patients
- **Providers:** Sarah Chen (16 patients), Michael Torres (12), Jessica Okafor (7), Robert Kim (10), Amanda Wright (5)
- **Notable patients:** James Rodriguez (pat_1, diabetes), Patricia O'Brien (pat_8, VIP complex care), Helen Matsumoto (pat_10, Alzheimer's), Howard Blackwell (pat_27, CHF with pacemaker)

### Patient Letters (47)
- **From patients:** ~22 messages
- **To patients:** ~25 messages
- **Unread:** 11 from-patient messages
- **Drafts:** 1 draft letter
- **Conversations:** 35 unique conversations
- **Ended conversations:** 9

### Appointments (20)
- **Upcoming scheduled:** 15
- **Past completed:** 5
- **Virtual visits:** 5 (with Zoom links)
- **In-person:** 15

### Providers (5)
- Dr. Sarah Chen (physician, admin, virtual visit activated)
- Dr. Michael Torres (physician, virtual visit activated)
- Jessica Okafor NP (nurse practitioner, virtual visit not activated)
- Dr. Robert Kim (physician, virtual visit activated)
- Amanda Wright PA (physician assistant, admin, virtual visit not activated)

### Other Entities
- **User Groups:** 4 (Front Desk, Clinical Team, Nurses, All Providers)
- **Message Categories:** 8 (General Question, Prescription Refill, Appointment Request, Test Results, Billing Question, Referral Request, Medical Records Request, Other)
- **Patient Tags:** 12 (VIP, Inactive, Chronic Care, Pediatric, Geriatric, High Risk, New Patient, Diabetes Management, Mental Health, Telehealth Preferred, Spanish Speaking, Insurance Pending)
- **Practice Locations:** 3 (Main Office, Telehealth, East Bay Clinic)
- **CPT Codes:** 13 (office visits, telephone E/M, online digital E/M)
- **Reminders:** 10 (4 unread alerts, 4 appointment reminders, 2 passport invitations)
- **Visit Summaries:** 5 (all signed, with vitals, procedures, treatments, care plans)
- **Bulk Letters:** 3 (flu reminder, holiday hours, portal reminder)
